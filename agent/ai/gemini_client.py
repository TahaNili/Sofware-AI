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
        load_dotenv()

        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
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

    def process_request(self, prompt: str) -> Dict[str, Any]:
        """Process a user request with Gemini and return a structured dict.

        The return value is a dictionary containing a `type` key which
        indicates how the UI/agent should handle the response. Possible
        types include: `product_search`, `product_analysis`,
        `recommendation`, `general_response` and `error`.
        """
        try:
            # Create model instance and generate response using multiple SDK shapes
            raw = None
            try:
                # Preferred: genai.GenerativeModel (some versions); may not be present.
                GenModel = getattr(genai, "GenerativeModel", None)
                if GenModel:
                    model = GenModel(self.model_name)
                    if hasattr(model, "generate_content"):
                        raw = model.generate_content(prompt)

                # Fallback: genai.Client or TextGenerationClient
                if not raw:
                    ClientClass = getattr(genai, "Client", None) or getattr(genai, "TextGenerationClient", None)
                    if ClientClass:
                        client = ClientClass()
                        if hasattr(client, "generate"):
                            raw = client.generate(model=self.model_name, input=prompt)
                        elif hasattr(client, "text_generation") and hasattr(client.text_generation, "generate"):
                            raw = client.text_generation.generate(model=self.model_name, input=prompt)

                # Fallback: genai.responses.generate
                if not raw:
                    responses = getattr(genai, "responses", None)
                    if responses and hasattr(responses, "generate"):
                        raw = responses.generate(model=self.model_name, input=prompt)
            except Exception:
                raw = None

            if raw is None:
                raise RuntimeError("Failed to call generation API: 'generate' method not found on google.generativeai")

            response_text = self._extract_text(raw)

            lprompt = prompt.lower()
            if any(k in lprompt for k in ("price", "cost", "buy", "purchase")):
                return {
                    "type": "product_search",
                    "search_params": {"query": prompt, "response": response_text},
                }
            if any(k in lprompt for k in ("analyze", "review", "compare")):
                return {"type": "product_analysis", "analysis": response_text}
            if any(k in lprompt for k in ("recommend", "suggest", "alternative")):
                recommendations = [r.strip() for r in response_text.splitlines() if r.strip()]
                return {"type": "recommendation", "recommendations": recommendations}

            return {"type": "general_response", "response": response_text}

        except Exception as exc:  # pragma: no cover - runtime errors
            return {"type": "error", "error": str(exc)}