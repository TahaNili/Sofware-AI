"""Google Gemini AI client implementation

This module provides a small wrapper around the `google.generativeai`
library. It normalizes the client interface for the application and
attempts to safely extract text from multiple response shapes.
"""

import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

import google.generativeai as genai


class GeminiClient:
    """Google Gemini AI client for processing requests.

    Args:
        model: Optional model name override. If not provided the
            `GEMINI_MODEL` environment variable is used or the
            default `gemini-pro`.
    """

    def __init__(self, model: Optional[str] = None):
        from utils.logger import logger
        logger.info("Initializing Gemini client...")
        
        # Try to load .env file
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
        logger.info(f"Looking for .env file at: {dotenv_path}")
        if os.path.exists(dotenv_path):
            logger.info(".env file found, loading...")
            load_dotenv(dotenv_path)
        else:
            logger.warning(f".env file not found at {dotenv_path}")
            load_dotenv()  # Try default locations

        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.error("GOOGLE_API_KEY not found in environment variables after loading .env")
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

        # Some versions of the google.generativeai package do not export a
        # `configure` function; ensure the API key is available via environment
        # variable so the SDK can read it.
        os.environ["GOOGLE_API_KEY"] = api_key
        self.model_name = model or os.getenv("GEMINI_MODEL") or "gemini-pro"

    def _extract_text(self, raw: Any) -> str:
        """Attempt to extract a text string from different response shapes."""
        if raw is None:
            return ""

        # If the response is a mapping/dict prefer common keys
        try:
            if isinstance(raw, dict):
                for key in ("output", "text", "content", "candidates"):
                    if key in raw and raw[key]:
                        val = raw[key]
                        if isinstance(val, list):
                            # Join candidate items if they're dicts or simple strings
                            parts = []
                            for item in val:
                                if isinstance(item, dict):
                                    parts.append(str(item.get("content") or item.get("text") or ""))
                                else:
                                    parts.append(str(item))
                            return "\n".join(p for p in parts if p)
                        return str(val)

            # Otherwise try common attributes on returned objects
            for attr in ("text", "output", "content"):
                val = getattr(raw, attr, None)
                if val:
                    if isinstance(val, list):
                        return "\n".join(str(v) for v in val if v)
                    return str(val)
        except Exception:
            # If extraction fails, fall back to string conversion
            pass

        try:
            return str(raw)
        except Exception:
            return ""

    async def process_request(self, prompt: str) -> str:
        """Asynchronously process a user request with Gemini and return plain text.

        This method will:
        - Run the (possibly blocking) SDK calls in a background thread.
        - Extract the text portion of the response.
        - Clean out system prefixes and common English greetings.
        - Return a single plain string (not a structured dict) so callers that
          expect a simple message will receive the `response` text directly.

        Note: For more complex agent behavior (product_search, analysis, etc.)
        the caller can still implement intent detection on the returned text.
        """
        try:
            # encapsulate the original synchronous generation logic so we can
            # run it in a thread without blocking the event loop
            def _sync_generate(p: str):
                raw = None
                try:
                    GenModel = getattr(genai, "GenerativeModel", None)
                    if GenModel:
                        model = GenModel(self.model_name)
                        if hasattr(model, "generate_content"):
                            return model.generate_content(p)

                    ClientClass = getattr(genai, "Client", None) or getattr(genai, "TextGenerationClient", None)
                    if ClientClass:
                        client = ClientClass()
                        if hasattr(client, "generate"):
                            return client.generate(model=self.model_name, input=p)
                        if hasattr(client, "text_generation") and hasattr(client.text_generation, "generate"):
                            return client.text_generation.generate(model=self.model_name, input=p)

                    responses = getattr(genai, "responses", None)
                    if responses and hasattr(responses, "generate"):
                        return responses.generate(model=self.model_name, input=p)
                except Exception:
                    return None
                return None

            # Run the generator in a background thread
            raw = await __import__('asyncio').to_thread(_sync_generate, prompt)
            if raw is None:
                raise RuntimeError("Failed to call generation API: 'generate' method not found on google.generativeai")

            # Extract text and clean/localize
            response_text = self._extract_text(raw)
            cleaned = self._clean_and_localize(response_text, prompt)

            return cleaned

        except Exception as exc:
            # Return a simple error message string (callers expect text)
            return f"خطا: {str(exc)}"

    def _clean_and_localize(self, text: str, prompt: str) -> str:
        """Perform lightweight cleaning and localization of model output.

        - Strip common system messages and metadata
        - Remove or replace short English greetings with Persian equivalents
        - Preserve the main content. Full translation is not performed here;
          we only handle common prefixes and greetings to make output cleaner.
        """
        if not text:
            return ""

        # Remove common system prefixes or bracketed metadata
        import re
        # Remove leading 'System:' or similar labels
        text = re.sub(r"^\s*(System:|Assistant:|\[system\]|\(system\))\s*", "", text, flags=re.IGNORECASE)
        # Remove bracketed metadata at start
        text = re.sub(r"^\s*\[[^\]]+\]\s*", "", text)

        # Map a few common English greetings/phrases to Persian equivalents
        greetings_map = {
            r"^Hello\b[:,.!?]*\s*": "سلام! ",
            r"^Hi\b[:,.!?]*\s*": "سلام! ",
            r"^Hey\b[:,.!?]*\s*": "سلام! ",
            r"^Greetings\b[:,.!?]*\s*": "سلام! ",
            r"How can I help you( today)?\?*$": "چطور می‌تونم کمکتون کنم؟",
            r"How can I assist you( today)?\?*$": "چطور می‌تونم کمکتون کنم؟",
        }

        # If the prompt contains Persian characters, prefer a Persian greeting replacement
        prefer_persian = bool(re.search(r"[\u0600-\u06FF]", prompt))

        # Apply greeting replacements at the start
        for pattern, replacement in greetings_map.items():
            try:
                new_text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
                if new_text != text:
                    text = new_text
                    # stop after first successful greeting replacement
                    break
            except re.error:
                continue

        # Trim whitespace
        text = text.strip()

        # If output is still English and prompt is Persian, we can't auto-translate here;
        # instead leave the core content but remove obvious English-only system notes.
        # (Full translation would require an external translation API.)

        return text