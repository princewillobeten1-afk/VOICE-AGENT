from __future__ import annotations

import time
from typing import Any

import httpx

from app.core.config import get_settings


class GeminiConfigurationError(RuntimeError):
    """Raised when Gemini is not configured with required credentials."""


class GeminiReasoningProvider:
    """Gemini adapter used as the realtime voice agent reasoning layer."""

    name = "gemini"

    def __init__(self, api_key: str | None = None, client: httpx.AsyncClient | None = None) -> None:
        settings = get_settings()
        self.api_key = api_key or settings.gemini_api_key
        self.model = settings.gemini_model
        self._client = client

    def _require_api_key(self) -> str:
        if not self.api_key:
            raise GeminiConfigurationError("GEMINI_API_KEY is required for Gemini reasoning")
        return self.api_key

    async def generate_response(
        self,
        *,
        user_text: str,
        system_prompt: str,
        history: list[dict[str, str]] | None = None,
        config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Generate the next assistant turn with Gemini.

        Returns a dict so the realtime pipeline can preserve latency/model metadata without
        leaking provider-specific response shapes into WebSocket handling.
        """
        started = time.perf_counter()
        config = config or {}
        if "mock_response" in config:
            return {
                "text": str(config["mock_response"]),
                "model": config.get("model", self.model),
                "latency_ms": int((time.perf_counter() - started) * 1000),
            }

        api_key = self._require_api_key()
        model = str(config.get("model", self.model))
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

        contents: list[dict[str, Any]] = []
        for item in history or []:
            role = "model" if item.get("role") in {"assistant", "model"} else "user"
            text = item.get("content") or item.get("text") or ""
            if text:
                contents.append({"role": role, "parts": [{"text": text}]})
        contents.append({"role": "user", "parts": [{"text": user_text}]})

        payload = {
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": contents,
            "generationConfig": {
                "temperature": float(config.get("temperature", 0.4)),
                "maxOutputTokens": int(config.get("max_output_tokens", 220)),
            },
        }

        client = self._client or httpx.AsyncClient(timeout=20)
        close_client = self._client is None
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            body = response.json()
        finally:
            if close_client:
                await client.aclose()

        text = ""
        candidates = body.get("candidates") or []
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            text = "".join(str(part.get("text", "")) for part in parts).strip()

        return {
            "text": text,
            "model": model,
            "latency_ms": int((time.perf_counter() - started) * 1000),
            "raw_finish_reason": candidates[0].get("finishReason") if candidates else None,
        }
