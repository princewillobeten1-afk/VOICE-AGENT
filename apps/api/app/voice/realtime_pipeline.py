from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from app.core.config import get_settings
from app.voice.providers import AudioChunk, provider_registry


DEFAULT_SYSTEM_PROMPT = (
    "You are VoiceSense, a concise professional AI phone agent. "
    "Answer naturally, ask one question at a time, and keep replies short for voice calls."
)


@dataclass
class RealtimeVoicePipeline:
    """Coordinates Twilio Media Streams with Cartesia Ink, Gemini, and Cartesia Sonic."""

    stream_sid: str | None = None
    call_sid: str | None = None
    sequence_number: int = 0
    system_prompt: str = DEFAULT_SYSTEM_PROMPT
    conversation_history: list[dict[str, str]] = field(default_factory=list)
    started_at: float = field(default_factory=time.perf_counter)
    last_transcript: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    async def handle_twilio_event(self, event: dict[str, Any]) -> list[dict[str, Any]]:
        event_type = event.get("event")
        if event_type == "connected":
            return []
        if event_type == "start":
            start = event.get("start") or {}
            self.stream_sid = start.get("streamSid") or event.get("streamSid") or self.stream_sid
            self.call_sid = start.get("callSid") or self.call_sid
            self.metadata = {
                "account_sid": start.get("accountSid"),
                "tracks": start.get("tracks"),
                "media_format": start.get("mediaFormat"),
                "custom_parameters": start.get("customParameters") or {},
            }
            custom_parameters = self.metadata.get("custom_parameters") or {}
            if custom_parameters.get("system_prompt"):
                self.system_prompt = custom_parameters["system_prompt"]
            return []
        if event_type == "media":
            return await self._handle_media(event)
        if event_type == "mark":
            return []
        if event_type == "stop":
            return []
        return []

    async def _handle_media(self, event: dict[str, Any]) -> list[dict[str, Any]]:
        media = event.get("media") or {}
        payload = media.get("payload")
        if not payload:
            return []

        self.sequence_number += 1
        settings = get_settings()
        chunk = AudioChunk(
            sequence_number=self.sequence_number,
            payload_ref=payload,
            duration_ms=20,
            codec="pcm_mulaw",
            sample_rate_hz=settings.cartesia_sample_rate,
        )
        transcript = await provider_registry.stt("cartesia").transcribe_stream(
            chunk,
            {
                "payload": payload,
                "encoding": "mulaw",
                "sample_rate": settings.cartesia_sample_rate,
                "language": "en",
            },
        )
        if not transcript.text or not transcript.is_final:
            return []

        self.last_transcript = transcript.text
        self.conversation_history.append({"role": "user", "content": transcript.text})
        gemini = await provider_registry.llm("gemini").generate_response(
            user_text=transcript.text,
            system_prompt=self.system_prompt,
            history=self.conversation_history[:-1],
            config={},
        )
        assistant_text = str(gemini.get("text") or "").strip()
        if not assistant_text:
            return []

        self.conversation_history.append({"role": "assistant", "content": assistant_text})
        speech = await provider_registry.tts("cartesia").synthesize_stream(
            assistant_text,
            {
                "voice_id": settings.cartesia_voice_id,
                "model": settings.cartesia_tts_model,
            },
        )
        if not speech.payload_ref:
            return []

        return [
            {
                "event": "media",
                "streamSid": self.stream_sid or event.get("streamSid"),
                "media": {"payload": speech.payload_ref},
                "voicesense": {
                    "transcript": transcript.text,
                    "response": assistant_text,
                    "providers": {"stt": "cartesia", "llm": "gemini", "tts": "cartesia"},
                    "latency_ms": {
                        "stt": transcript.latency_ms,
                        "llm": gemini.get("latency_ms"),
                        "tts": speech.latency_ms,
                    },
                },
            }
        ]
