from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class AudioChunk:
    sequence_number: int
    payload_ref: str | None
    duration_ms: int
    codec: str = "pcm16"
    sample_rate_hz: int = 16000


@dataclass(frozen=True)
class TranscriptChunk:
    text: str
    is_final: bool
    confidence: float | None = None
    language: str | None = None
    latency_ms: int | None = None


@dataclass(frozen=True)
class SpeechChunk:
    payload_ref: str | None
    text: str
    is_final: bool
    duration_ms: int | None = None
    latency_ms: int | None = None


@dataclass(frozen=True)
class VadSignal:
    event: str
    confidence: float
    silence_ms: int = 0
    noise_score: float | None = None


class SpeechToTextProvider(Protocol):
    name: str

    async def transcribe_stream(self, chunk: AudioChunk, config: dict) -> TranscriptChunk:
        ...


class TextToSpeechProvider(Protocol):
    name: str

    async def synthesize_stream(self, text: str, config: dict) -> SpeechChunk:
        ...


class VoiceActivityDetector(Protocol):
    name: str

    async def detect(self, chunk: AudioChunk, config: dict) -> VadSignal:
        ...


class PlaceholderSpeechToTextProvider:
    name = "placeholder-stt"

    async def transcribe_stream(self, chunk: AudioChunk, config: dict) -> TranscriptChunk:
        language = config.get("language", "en")
        return TranscriptChunk(text="Partial transcript placeholder", is_final=False, confidence=0.91, language=language, latency_ms=45)


class PlaceholderTextToSpeechProvider:
    name = "placeholder-tts"

    async def synthesize_stream(self, text: str, config: dict) -> SpeechChunk:
        return SpeechChunk(payload_ref="memory://placeholder-audio-chunk", text=text, is_final=False, duration_ms=480, latency_ms=62)


class EnergyThresholdVad:
    name = "energy-threshold-vad"

    async def detect(self, chunk: AudioChunk, config: dict) -> VadSignal:
        min_duration_ms = int(config.get("min_speech_ms", 120))
        if chunk.duration_ms >= min_duration_ms:
            return VadSignal(event="speech_detected", confidence=0.88, silence_ms=0, noise_score=0.08)
        return VadSignal(event="silence", confidence=0.77, silence_ms=chunk.duration_ms, noise_score=0.04)


class VoiceProviderRegistry:
    def __init__(self) -> None:
        self._stt: dict[str, SpeechToTextProvider] = {"placeholder": PlaceholderSpeechToTextProvider()}
        self._tts: dict[str, TextToSpeechProvider] = {"placeholder": PlaceholderTextToSpeechProvider()}
        self._vad: dict[str, VoiceActivityDetector] = {"energy_threshold": EnergyThresholdVad()}

    def stt(self, provider: str) -> SpeechToTextProvider:
        return self._stt.get(provider, self._stt["placeholder"])

    def tts(self, provider: str) -> TextToSpeechProvider:
        return self._tts.get(provider, self._tts["placeholder"])

    def vad(self, provider: str = "energy_threshold") -> VoiceActivityDetector:
        return self._vad.get(provider, self._vad["energy_threshold"])

    def provider_catalog(self) -> list[dict]:
        return [
            {"type": "stt", "provider": "deepgram", "status": "architecture_ready", "capabilities": ["streaming", "interim_transcripts", "language_detection"]},
            {"type": "stt", "provider": "assemblyai", "status": "architecture_ready", "capabilities": ["streaming", "speaker_labels"]},
            {"type": "stt", "provider": "openai", "status": "architecture_ready", "capabilities": ["streaming", "multilingual"]},
            {"type": "stt", "provider": "google", "status": "architecture_ready", "capabilities": ["streaming", "enterprise_regions"]},
            {"type": "stt", "provider": "azure", "status": "architecture_ready", "capabilities": ["streaming", "private_networking"]},
            {"type": "tts", "provider": "elevenlabs", "status": "architecture_ready", "capabilities": ["streaming", "voice_cloning", "emotion"]},
            {"type": "tts", "provider": "cartesia", "status": "architecture_ready", "capabilities": ["low_latency", "streaming"]},
            {"type": "tts", "provider": "openai", "status": "architecture_ready", "capabilities": ["streaming", "multilingual"]},
            {"type": "tts", "provider": "azure", "status": "architecture_ready", "capabilities": ["enterprise_regions"]},
            {"type": "tts", "provider": "google", "status": "architecture_ready", "capabilities": ["custom_voice"]},
            {"type": "vad", "provider": "energy_threshold", "status": "implemented_placeholder", "capabilities": ["speech_start", "silence"]},
        ]


provider_registry = VoiceProviderRegistry()