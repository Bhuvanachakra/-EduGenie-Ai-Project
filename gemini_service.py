import os
from functools import lru_cache

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


class GeminiService:
    """Small wrapper around the current Google GenAI SDK."""

    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
        self._client = None

    @property
    def configured(self) -> bool:
        return bool(self.api_key) and self.api_key != "your_gemini_api_key_here"

    def _get_client(self):
        if not self.configured:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. Add it to the .env file and restart EduGenie."
            )
        if self._client is None:
            self._client = genai.Client(api_key=self.api_key)
        return self._client

    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.4,
        max_output_tokens: int = 2048,
        json_mode: bool = False,
    ) -> str:
        client = self._get_client()
        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            response_mime_type="application/json" if json_mode else "text/plain",
        )
        response = client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=config,
        )
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()


@lru_cache(maxsize=1)
def get_gemini_service() -> GeminiService:
    return GeminiService()
