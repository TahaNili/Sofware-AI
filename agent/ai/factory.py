"""AI provider factory to manage different AI implementations

This factory lazily imports provider implementations to avoid raising
ImportError at module import time when optional dependencies are missing.
It will fall back to the `MockClient` when no API keys or providers are
available.
"""

import os
from typing import Optional


class AIFactory:
    """Factory class to create appropriate AI client based on configuration"""

    @staticmethod
    def create_client(provider: Optional[str] = None, model: Optional[str] = None):
        """Create and return appropriate AI client based on environment variables or args.

        Args:
            provider: Optional override for provider name ('gemini' or 'openai')
            model: Optional model name (passed to client if supported)

        Returns:
            An instance of a client class (GeminiClient, OpenAIClient or MockClient)
        """
        # If provider explicitly requested, normalize
        if provider is not None:
            provider = provider.lower()

        # Try Google Gemini first if requested or if GOOGLE_API_KEY present
        if provider == 'gemini' or (provider is None and os.getenv('GOOGLE_API_KEY')):
            try:
                from .gemini_client import GeminiClient
                return GeminiClient()
            except Exception:
                # Fallthrough to try OpenAI or Mock
                pass

        # Try OpenAI next
        if provider == 'openai' or (provider is None and os.getenv('OPENAI_API_KEY')):
            try:
                from .openai_client import OpenAIClient
                return OpenAIClient()
            except Exception:
                pass

        # Last resort: return MockClient for local testing
        try:
            from .mock_client import MockClient
            return MockClient()
        except Exception:
            raise RuntimeError('No AI client available')