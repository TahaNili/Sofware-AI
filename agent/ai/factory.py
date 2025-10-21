"""
AI provider factory to manage different AI implementations
"""

import os
from typing import Optional
from .openai_client import OpenAIClient
from .gemini_client import GeminiClient

class AIFactory:
    """Factory class to create appropriate AI client based on configuration"""
    
    @staticmethod
    def create_client():
        """Create and return appropriate AI client based on environment variables
        
        Returns:
            An instance of OpenAIClient or GeminiClient
        """
        # Check for Google API key first
        if os.getenv("GOOGLE_API_KEY"):
            return GeminiClient()
        
        # Fall back to OpenAI
        elif os.getenv("OPENAI_API_KEY"):
            return OpenAIClient()
        
        else:
            raise ValueError("No API key found for any AI provider. Please set either GOOGLE_API_KEY or OPENAI_API_KEY in your .env file")