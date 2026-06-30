from __future__ import annotations

import base64
import time
from dataclasses import dataclass
from typing import Any

import httpx

from app.core.config import get_settings
from app.voice.providers import SpeechChunk, TranscriptChunk


class ProviderConfigurationError(RuntimeError):
    """Raised when a provider is not configured with required credentials."""


@dataclass(frozen=True)
class CartesiaAudioResult:
    payload: str
    duration_ms: int | None = None
    latency_ms: int | None = None


class CartesiaRealtimeProvider:
    """Cartesia adapter for Ink STT and Sonic TTS.

    The adapter is intentionally HTTP-first so tests can mock requests cleanly. Cartesia's
    streaming endpoints can be wired behind these methods without changing the pipeline API.
    Twilio Media Streams sends base64-encoded 8 kHz mu-law audio; the default config keeps
    Cartesia output in the same shape so it can be sent back to Twilio as a media payload.
    """

    name = "cartesia"
    stt_product = "ink"
    tts_product = "sonic"

    def __init__(self, api_key: str | None = None, client: httpx.AsyncClient | None = None) -> None:
        settings = get_settings()
        self.api_key = api_key or settings.cartesia_api_key
        self.stt_model = settings.cartesia_stt_model
        self.tts_model = settings.cartesia_tts_model
        self.voice_id = settings.cartesia_voice_id
        self.output_format = settings.cartesia_output_format
        self.sample_rate = settings.cartesia_sample_rate
        self._client = client

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            raise ProviderConfigurationError("CARTESIA_API_KEY is required for Cartesia providers")
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def transcribe_audio(
        self,
        payload: str,
        *,
        encoding: str = "mulaw",
        sample_rate: int | None = None,
        language: str = "en",
        config: dict[str, Any] | None = None,
    ) -> TranscriptChunk:
        """Transcribe a Twilio media payload with Cartesia Ink.

        If Cartesia has not returned a final transcript yet, callers can treat the returned
        chunk as non-final and continue buffering. Tests can pass mock config values to avoid
        external API calls.
        """
        started = time.perf_counter()
        config = config or {}
        mock_text = config.get("mock_transcript")
        if mock_text is not None:
            return TranscriptChunk(
                text=str(mock_text),
                is_final=bool(config.get("mock_is_final", True)),
                confidence=float(config.get("mock_confidence", 0.95)),
                language=language,
                latency_ms=int((time.perf_counter() - started) * 1000),
            )

        data = {
            "model_id": config.get("model", self.stt_model),
            "audio": payload,
            "audio_format": {
                "encoding": encoding,
                "sample_rate": sample_rate or self.sample_rate,
            },
            "language": language,
            "turn_detection": config.get("turn_detection", True),
        }

        # Endpoint path is isolated here so Cartesia API updates only affect this adapter.
        url = str(config.get("stt_url", "https://api.cartesia.ai/stt/transcribe"))
        client = self._client or httpx.AsyncClient(timeout=15)
        close_client = self._client is None
        try:
            response = await client.post(url, headers=self._headers(), json=data)
            response.raise_for_status()
            body = response.json()
        finally:
            if close_client:
                await client.aclose()

        return TranscriptChunk(
            text=str(body.get("text") or body.get("transcript") or ""),
            is_final=bool(body.get("is_final", True)),
            confidence=body.get("confidence"),
            language=body.get("language", language),
            latency_ms=int((time.perf_counter() - started) * 1000),
        )

    async def synthesize_speech(
        self,
        text: str,
        *,
        voice_id: str | None = None,
        config: dict[str, Any] | None = None,
    ) -> SpeechChunk:
        """Synthesize assistant text with Cartesia Sonic and return Twilio-ready audio."""
        started = time.perf_counter()
        config = config or {}
        if "mock_audio_payload" in config:
            return SpeechChunk(
                payload_ref=str(config["mock_audio_payload"]),
                text=text,
                is_final=True,
                duration_ms=config.get("mock_duration_ms"),
                latency_ms=int((time.perf_counter() - started) * 1000),
            )

        selected_voice_id = voice_id or config.get("voice_id") or self.voice_id
        if not selected_voice_id:
            raise ProviderConfigurationError("CARTESIA_VOICE_ID is required for Cartesia Sonic TTS")

        data = {
            "model_id": config.get("model", self.tts_model),
            "transcript": text,
            "voice": {"mode": "id", "id": selected_voice_id},
            "output_format": {
                "container": "raw",
                "encoding": self.output_format,
                "sample_rate": self.sample_rate,
            },
        }
        url = str(config.get("tts_url", "https://api.cartesia.ai/tts/bytes"))
        client = self._client or httpx.AsyncClient(timeout=30)
        close_client = self._client is None
        try:
            response = await client.post(url, headers=self._headers(), json=data)
            response.raise_for_status()
            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type:
                body = response.json()
                payload = body.get("audio") or body.get("payload") or ""
            else:
                payload = base64.b64encode(response.content).decode("ascii")
        finally:
            if close_client:
                await client.aclose()

        return SpeechChunk(
            payload_ref=payload,
            text=text,
            is_final=True,
            duration_ms=None,
            latency_ms=int((time.perf_counter() - started) * 1000),
        )

    async def transcribe_stream(self, chunk, config: dict) -> TranscriptChunk:
        payload = str(config.get("payload") or chunk.payload_ref or "")
        return await self.transcribe_audio(
            payload,
            encoding=config.get("encoding", "mulaw"),
            sample_rate=int(config.get("sample_rate", self.sample_rate)),
            language=config.get("language", "en"),
            config=config,
        )

    async def synthesize_stream(self, text: str, config: dict) -> SpeechChunk:
        return await self.synthesize_speech(text, voice_id=config.get("voice_id"), config=config)
