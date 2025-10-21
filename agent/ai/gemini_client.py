"""
Google Gemini AI client implementation
"""

import os
import google.generativeai as genai
from typing import Optional, Dict, Any
from dotenv import load_dotenv

class GeminiClient:
    """Google Gemini AI client for processing requests"""
    
    def __init__(self):
        """Initialize the Gemini client"""
        load_dotenv()
        
        # Configure Gemini
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    async def process_request(self, prompt: str) -> Dict[str, Any]:
        """Process a user request using Gemini AI
        
        Args:
            prompt: User's request text
            
        Returns:
            Dictionary containing the response and action type
        """
        try:
            # Generate response
            response = await self.model.generate_content_async(prompt)
            
            # Determine action type based on content
            if any(keyword in prompt.lower() for keyword in ['price', 'cost', 'buy', 'purchase']):
                return {
                    'type': 'product_search',
                    'search_params': {
                        'query': prompt,
                        'response': response.text
                    }
                }
            elif any(keyword in prompt.lower() for keyword in ['analyze', 'review', 'compare']):
                return {
                    'type': 'product_analysis',
                    'analysis': response.text
                }
            elif any(keyword in prompt.lower() for keyword in ['recommend', 'suggest', 'alternative']):
                return {
                    'type': 'recommendation',
                    'recommendations': [r.strip() for r in response.text.split('\n') if r.strip()]
                }
            else:
                return {
                    'type': 'general_response',
                    'response': response.text
                }
                
        except Exception as e:
            return {
                'type': 'error',
                'error': str(e)
            }