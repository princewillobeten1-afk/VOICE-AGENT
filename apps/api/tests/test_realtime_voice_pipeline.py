import pytest

from app.telephony.router import _websocket_url_from_base
from app.voice.providers import SpeechChunk, TranscriptChunk, provider_registry
from app.voice.realtime_pipeline import RealtimeVoicePipeline


class MockCartesiaStt:
    async def transcribe_stream(self, chunk, config):
        return TranscriptChunk(
            text="I need an appointment tomorrow",
            is_final=True,
            confidence=0.99,
            language="en",
            latency_ms=10,
        )


class MockCartesiaTts:
    async def synthesize_stream(self, text, config):
        return SpeechChunk(
            payload_ref="base64-audio",
            text=text,
            is_final=True,
            duration_ms=250,
            latency_ms=12,
        )


class MockGemini:
    async def generate_response(self, *, user_text, system_prompt, history=None, config=None):
        return {"text": "Sure, what time works best?", "model": "gemini-test", "latency_ms": 15}


def test_provider_catalog_uses_cartesia_and_gemini():
    catalog = provider_registry.provider_catalog()
    implemented = {(item["type"], item["provider"]) for item in catalog if item["status"] == "implemented"}
    assert ("stt", "cartesia") in implemented
    assert ("llm", "gemini") in implemented
    assert ("tts", "cartesia") in implemented
    assert ("stt", "deepgram") not in implemented
    assert ("tts", "elevenlabs") not in implemented
    assert ("llm", "openai") not in implemented


def test_twilio_websocket_url_conversion():
    assert _websocket_url_from_base("https://api.example.com") == "wss://api.example.com/v1/voice/twilio/stream"
    assert _websocket_url_from_base("http://localhost:8000") == "ws://localhost:8000/v1/voice/twilio/stream"


@pytest.mark.asyncio
async def test_realtime_pipeline_mocked_cartesia_gemini_flow(monkeypatch):
    monkeypatch.setitem(provider_registry._stt, "cartesia", MockCartesiaStt())
    monkeypatch.setitem(provider_registry._tts, "cartesia", MockCartesiaTts())
    monkeypatch.setitem(provider_registry._llm, "gemini", MockGemini())

    pipeline = RealtimeVoicePipeline()
    await pipeline.handle_twilio_event(
        {
            "event": "start",
            "start": {
                "streamSid": "MZ123",
                "callSid": "CA123",
                "customParameters": {"system_prompt": "You are a helpful receptionist."},
            },
        }
    )
    outbound = await pipeline.handle_twilio_event(
        {"event": "media", "streamSid": "MZ123", "media": {"payload": "caller-audio"}}
    )

    assert outbound == [
        {
            "event": "media",
            "streamSid": "MZ123",
            "media": {"payload": "base64-audio"},
            "voicesense": {
                "transcript": "I need an appointment tomorrow",
                "response": "Sure, what time works best?",
                "providers": {"stt": "cartesia", "llm": "gemini", "tts": "cartesia"},
                "latency_ms": {"stt": 10, "llm": 15, "tts": 12},
            },
        }
    ]
