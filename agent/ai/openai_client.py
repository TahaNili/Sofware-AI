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
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        openai.api_key = self.api_key
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    async def process_request(self, prompt: str) -> Dict[str, Any]:
        """Process a user request using OpenAI API
        Args:
            prompt: User's request text
        Returns:
            Dictionary containing the response and action type
        """
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            text = response.choices[0].message.content.strip()
            # Simple action type detection (can be improved)
            if any(keyword in prompt.lower() for keyword in ['price', 'cost', 'buy', 'purchase']):
                return {
                    'type': 'product_search',
                    'search_params': {
                        'query': prompt,
                        'response': text
                    }
                }
            elif any(keyword in prompt.lower() for keyword in ['analyze', 'review', 'compare']):
                return {
                    'type': 'product_analysis',
                    'analysis': text
                }
            elif any(keyword in prompt.lower() for keyword in ['recommend', 'suggest', 'alternative']):
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