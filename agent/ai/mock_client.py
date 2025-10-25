"""
Mock AI client for local testing when no API keys are available.
Returns canned responses synchronously/asynchronously to let the UI be tested.
"""
from typing import Dict, Any

class MockClient:
    def __init__(self):
        self.name = "mock"

    async def process_request(self, prompt: str) -> Dict[str, Any]:
        # Return a predictable response for testing
        text = f"{prompt}"
        return {"type": "general_response", "response": text}
