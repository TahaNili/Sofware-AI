"""
OpenAI client implementation for Sofware-AI with async support
"""

import os
import re
import asyncio
from typing import Optional, Any, Dict, Union, Mapping, TypedDict

# Import OpenAI but handle both old and new SDK versions
try:
    # Try importing new style OpenAI SDK first
    from openai import OpenAI, AsyncOpenAI
    OPENAI_NEW_SDK = True
except ImportError:
    try:
        # Try importing just OpenAI for newer versions without async
        from openai import OpenAI
        AsyncOpenAI = None
        OPENAI_NEW_SDK = True
    except ImportError:
        # Fall back to old style openai package
        import openai
        OpenAI = AsyncOpenAI = None
        OPENAI_NEW_SDK = False

from dotenv import load_dotenv

class ResponseDict(TypedDict, total=False):
    type: str
    error: str
    response: str
    search_params: Dict[str, str]
    analysis: str
    recommendations: list[str]

class OpenAIClient:
    """Client for interacting with OpenAI models asynchronously"""
    def __init__(self):
        from utils.logger import logger
        logger.info("Initializing OpenAI client...")
        
        # Try to load .env file
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
        logger.info(f"Looking for .env file at: {dotenv_path}")
        if os.path.exists(dotenv_path):
            logger.info(".env file found, loading...")
            load_dotenv(dotenv_path)
        else:
            logger.warning(f".env file not found at {dotenv_path}")
            load_dotenv()  # Try default locations

        self.api_key = os.getenv("OPENAI_API_KEY")
        self.api_base = os.getenv("OPENAI_API_BASE")  # Optional API base URL override
        
        if not self.api_key:
            logger.error("OPENAI_API_KEY not found in environment variables after loading .env")
            raise ValueError("OPENAI_API_KEY not found in environment variables")
            
        try:
            # Initialize client based on available SDK version
            client_kwargs: Dict[str, Any] = {
                "api_key": self.api_key,
                "max_retries": 3,
            }
            
            if self.api_base:
                client_kwargs["base_url"] = self.api_base
            
            if AsyncOpenAI is not None:
                # Use async client (newest SDK)
                self.client = AsyncOpenAI(**client_kwargs)
                self.is_async = True
            elif OpenAI is not None:
                # Use sync client (newer SDK)
                self.client = OpenAI(**client_kwargs)
                self.is_async = False
            else:
                # Very old SDK - use global settings
                # We imported the old-style openai package earlier
                if OPENAI_NEW_SDK:
                    raise RuntimeError("OpenAI client initialization failed - incompatible SDK version")
                else:
                    import openai  # type: ignore
                    openai.api_key = self.api_key
                    if self.api_base:
                        # Use setattr to avoid type checker complaints about old SDK
                        setattr(openai, 'api_base', self.api_base)
                    self.client = None
                    self.is_async = False
                    # Store module for later use
                    self._openai = openai
                
            self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            logger.info(f"OpenAI client initialized with model: {self.model}")
            if self.api_base:
                logger.info(f"Using custom API base: {self.api_base}")
                
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise RuntimeError("Failed to initialize OpenAI client") from e

    def _clean_and_localize(self, text: str, prompt: str) -> str:
        """Clean and localize the response text.
        
        - Remove system messages and metadata
        - Replace English greetings with Persian equivalents when appropriate
        - Clean up formatting
        """
        if not text:
            return ""

        # Remove common system prefixes
        text = re.sub(r"^\s*(System:|Assistant:|\[system\]|\(system\))\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"^\s*\[[^\]]+\]\s*", "", text)

        # Map common English phrases to Persian
        greetings_map = {
            r"^Hello\b[:,.!?]*\s*": "سلام! ",
            r"^Hi\b[:,.!?]*\s*": "سلام! ",
            r"^Hey\b[:,.!?]*\s*": "سلام! ",
            r"^Greetings\b[:,.!?]*\s*": "سلام! ",
            r"How can I help you( today)?\?*$": "چطور می‌تونم کمکتون کنم؟",
            r"How can I assist you( today)?\?*$": "چطور می‌تونم کمکتون کنم؟",
        }

        # Check if prompt contains Persian to decide on replacements
        has_persian = bool(re.search(r"[\u0600-\u06FF]", prompt))

        # Apply greeting replacements
        if has_persian:
            for pattern, replacement in greetings_map.items():
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

        return text.strip()

    async def process_request(self, prompt: str) -> ResponseDict:
        """Process a user request using OpenAI API asynchronously.
        Args:
            prompt: User's request text
        Returns:
            A dictionary containing the response data with type information and optional fields
            based on the type of response generated
        """
        try:
            response = None
            
            if self.client and hasattr(self.client, "chat"):
                if self.is_async:
                    # New SDK with async support
                    response = await self.client.chat.completions.create(  # type: ignore
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}]
                    )
                else:
                    # New SDK sync client
                    response = self.client.chat.completions.create(  # type: ignore
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}]
                    )
            else:
                # older openai package
                if hasattr(self, '_openai'):
                    chat_comp = getattr(self._openai, "ChatCompletion", None)
                    if chat_comp is not None and hasattr(chat_comp, "create"):
                        response = chat_comp.create(
                            model=self.model,
                            messages=[{"role": "user", "content": prompt}]
                        )
                    else:
                        # Fallback to older Completion API if ChatCompletion isn't available.
                        # The Completion API expects a single prompt string instead of messages.
                        completion_cls = getattr(self._openai, "Completion", None)
                        if completion_cls is not None and hasattr(completion_cls, "create"):
                            response = completion_cls.create(
                                model=self.model,
                                prompt=prompt,
                                max_tokens=150
                            )
                else:
                    # No old-style openai package available
                    raise RuntimeError("No ChatCompletion or Completion API found in installed openai package")

            # Extract text from different possible response shapes
            text = ""
            try:
                if response is None:
                    raise ValueError("No response received from API")

                # Handle async response
                if self.is_async and asyncio.iscoroutine(response):
                    response_obj = await response
                else:
                    response_obj = response

                # Extract choice safely handling both object and dict responses
                if isinstance(response_obj, dict):
                    choices = response_obj.get('choices', [])
                    choice = choices[0] if choices else None
                else:
                    # Handle non-dict response object
                    choices = getattr(response_obj, 'choices', [])
                    choice = choices[0] if choices else None
                
                if choice is None:
                    raise ValueError("No valid choices in response")

                # Extract text from choice
                if isinstance(choice, dict):
                    # Handle dictionary response format
                    if 'message' in choice and isinstance(choice['message'], dict):
                        text = choice['message'].get('content', '')
                    elif 'text' in choice:
                        text = choice.get('text', '')
                else:
                    # Handle object response format
                    if hasattr(choice, 'message'):
                        msg = choice.message
                        if hasattr(msg, 'content'):
                            text = getattr(msg, 'content', '')
                        elif isinstance(msg, dict):
                            text = msg.get('content', '')
                    elif hasattr(choice, 'text'):
                        text = getattr(choice, 'text', '')
                
                # Ensure text is stripped
                text = text.strip() if isinstance(text, str) else ""

                # If we still don't have text, try to get a string representation
                if not text and choice is not None:
                    text = str(choice).strip()

                if not text and response_obj is not None:
                    text = str(response_obj).strip()
                    
            except Exception as e:
                from utils.logger import logger
                logger.error(f"Error processing response: {str(e)}")
                text = str(response).strip() if response else ""

            # Simple action type detection (can be improved)
            lower_prompt = prompt.lower()
            
            response_dict: ResponseDict = {'type': 'general_response'}
            
            if any(keyword in lower_prompt for keyword in ['price', 'cost', 'buy', 'purchase']):
                response_dict.update({
                    'type': 'product_search',
                    'search_params': {
                        'query': prompt,
                        'response': text
                    }
                })
            elif any(keyword in lower_prompt for keyword in ['analyze', 'review', 'compare']):
                response_dict.update({
                    'type': 'product_analysis',
                    'analysis': text
                })
            elif any(keyword in lower_prompt for keyword in ['recommend', 'suggest', 'alternative']):
                response_dict.update({
                    'type': 'recommendation',
                    'recommendations': [r.strip() for r in text.split('\n') if r.strip()]
                })
            else:
                response_dict.update({
                    'type': 'general_response',
                    'response': text
                })
                
            return response_dict
            
        except Exception as e:
            return {'type': 'error', 'error': str(e)}