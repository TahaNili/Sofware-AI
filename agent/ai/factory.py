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

    # Available models by provider
    MODELS = {
        'gemini': [
            'gemini-2.5-flash'
        ],
        'openai': [
            'gpt-oss-120b'
        ],
    }

    @staticmethod
    def get_available_providers():
        """Return list of available providers based on API keys"""
        from utils.logger import logger
        providers = []
        
        google_key = os.getenv('GOOGLE_API_KEY')
        openai_key = os.getenv('OPENAI_API_KEY')
        
        logger.info(f"Checking API Keys - Google: {'Available' if google_key else 'Not found'}, OpenAI: {'Available' if openai_key else 'Not found'}")
        
        if google_key:
            logger.info("Adding Google Gemini provider")
            providers.append(('Google Gemini', 'gemini'))
        if openai_key:
            logger.info("Adding OpenAI provider")
            providers.append(('OpenAI', 'openai'))
        if not providers:
            logger.warning("No API keys found, falling back to mock provider")
            providers.append(('Local Test', 'mock'))
        
        logger.info(f"Available providers: {[p[0] for p in providers]}")
        return providers

    @staticmethod
    def get_models(provider: str) -> list:
        """Get available models for a provider"""
        return AIFactory.MODELS.get(provider, ['mock-model'])

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
                return GeminiClient(model)
            except Exception:
                # Fallthrough to try OpenAI or Mock
                pass

        # Try OpenAI next
        if provider == 'openai' or (provider is None and os.getenv('OPENAI_API_KEY')):
            try:
                from .openai_client import OpenAIClient
                # OpenAIClient expects no positional arguments; create instance first
                client = OpenAIClient()
                # If a model was provided, try to configure the client with it.
                # Prefer a setter method if available, otherwise fall back to setting an attribute.
                if model is not None:
                    setter = getattr(client, 'set_model', None)
                    if callable(setter):
                        setter(model)
                    else:
                        setattr(client, 'model', model)
                return client
            except Exception:
                pass

        # Last resort: return MockClient for local testing
        try:
            from .mock_client import MockClient
            return MockClient()
        except Exception:
            raise RuntimeError('No AI client available')