"""
OpenAI client implementation for Sofware-AI
"""

import os
import openai
from typing import Optional, Dict, Any
from dotenv import load_dotenv

class OpenAIClient:
    """Client for interacting with OpenAI models"""
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
        if not self.api_key:
            logger.error("OPENAI_API_KEY not found in environment variables after loading .env")
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        # Prefer the new OpenAI client when available (OpenAI Python SDK v1+),
        # otherwise fall back to setting the global api_key for older versions.
        try:
            # Newer OpenAI SDK exposes an OpenAI client class; older versions use module-level api_key.
            if hasattr(openai, "OpenAI"):
                # initialize the new client
                self.client = openai.OpenAI(api_key=self.api_key)
                self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
            else:
                # fallback for older openai package
                openai.api_key = self.api_key
                self.client = None
                self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        except Exception as e:
            raise RuntimeError("Failed to initialize OpenAI client") from e

    def process_request(self, prompt: str) -> Dict[str, Any]:
        """Process a user request using OpenAI API
        Args:
            prompt: User's request text
        Returns:
            Dictionary containing the response and action type
        """
        try:
            # Use the new OpenAI client when available, otherwise fall back to older API
            if getattr(self, "client", None) is not None:
                # narrow the type for the type checker and ensure client is not None
                client = self.client
                assert client is not None
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )
            else:
                # older openai package
                chat_comp = getattr(openai, "ChatCompletion", None)
                if chat_comp is not None and hasattr(chat_comp, "create"):
                    response = chat_comp.create(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}]
                    )
                else:
                    # Fallback to older Completion API if ChatCompletion isn't available.
                    # The Completion API expects a single prompt string instead of messages.
                    completion_cls = getattr(openai, "Completion", None)
                    if completion_cls is not None and hasattr(completion_cls, "create"):
                        response = completion_cls.create(
                            model=self.model,
                            prompt=prompt,
                            max_tokens=150
                        )
                    else:
                        # No known completion API available on this openai package
                        raise RuntimeError("No ChatCompletion or Completion API found in installed openai package")

            # Extract text from different possible response shapes
            text = ""
            try:
                choice = response.choices[0]
                # new SDK may present message as dict or object
                if hasattr(choice, "message"):
                    msg = choice.message
                    # If msg is a dict-like mapping, use dict access only
                    if isinstance(msg, dict):
                        content = msg.get("content")
                        if isinstance(content, str) and content:
                            text = content.strip()
                        else:
                            # try other common keys if present
                            for k in ("content", "text"):
                                if k in msg and isinstance(msg[k], str) and msg[k]:
                                    text = msg[k].strip()
                                    break
                    else:
                        # msg may be an object with .content attribute
                        content = getattr(msg, "content", None)
                        if isinstance(content, str) and content:
                            text = content.strip()
                        else:
                            # content might itself be a dict-like with 'content'
                            if isinstance(content, dict) and "content" in content and isinstance(content["content"], str):
                                text = content["content"].strip()
                            else:
                                # fallback to string representation of the message object
                                text = str(msg).strip()
                else:
                    # try attribute 'text' safely, or inspect 'message' attribute or mapping safely
                    content = getattr(choice, "text", None)
                    if isinstance(content, str) and content:
                        text = content.strip()
                    else:
                        # prefer attribute 'message' if present
                        msg_attr = getattr(choice, "message", None)
                        if isinstance(msg_attr, dict):
                            content_val = msg_attr.get("content") or msg_attr.get("text")
                            if isinstance(content_val, str) and content_val:
                                text = content_val.strip()
                            else:
                                text = str(choice).strip()
                        elif msg_attr is not None:
                            # msg_attr might be an object with .content
                            content_val = getattr(msg_attr, "content", None)
                            if isinstance(content_val, str) and content_val:
                                text = content_val.strip()
                            else:
                                text = str(msg_attr).strip() or str(choice).strip()
                        else:
                            # finally, if choice is a dict-like mapping use .get safely; avoid __getitem__ on unknown objects
                            if isinstance(choice, dict):
                                msg = choice.get("message")
                                if isinstance(msg, dict):
                                    content_val = msg.get("content") or msg.get("text")
                                    if isinstance(content_val, str) and content_val:
                                        text = content_val.strip()
                                    else:
                                        text = str(choice).strip()
                                else:
                                    # try other top-level string keys
                                    for k in ("text", "content"):
                                        v = choice.get(k)
                                        if isinstance(v, str) and v:
                                            text = v.strip()
                                            break
                                    else:
                                        text = str(choice).strip()
                            else:
                                text = str(choice).strip()
            except Exception:
                # final fallback
                text = str(response).strip()

            # Simple action type detection (can be improved)
            lower_prompt = prompt.lower()
            if any(keyword in lower_prompt for keyword in ['price', 'cost', 'buy', 'purchase']):
                return {
                    'type': 'product_search',
                    'search_params': {
                        'query': prompt,
                        'response': text
                    }
                }
            elif any(keyword in lower_prompt for keyword in ['analyze', 'review', 'compare']):
                return {
                    'type': 'product_analysis',
                    'analysis': text
                }
            elif any(keyword in lower_prompt for keyword in ['recommend', 'suggest', 'alternative']):
                return {
                    'type': 'recommendation',
                    'recommendations': [r.strip() for r in text.split('\n') if r.strip()]
                }
            else:
                return {
                    'type': 'general_response',
                    'response': text
                }
        except Exception as e:
            return {
                'type': 'error',
                'error': str(e)
            }