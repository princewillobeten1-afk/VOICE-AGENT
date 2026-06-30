# Voice Provider Interface Guide

VoiceSense uses provider contracts instead of direct provider coupling.

## Speech-to-Text

`SpeechToTextProvider` exposes `transcribe_stream(AudioChunk, config) -> TranscriptChunk`.

The contract supports incremental transcription, final transcripts, confidence, language, and latency metadata.

## Text-to-Speech

`TextToSpeechProvider` exposes `synthesize_stream(text, config) -> SpeechChunk`.

The contract supports partial audio references, duration, final chunks, and latency metadata.

## Voice Activity Detection

`VoiceActivityDetector` exposes `detect(AudioChunk, config) -> VadSignal`.

The VAD contract supports speech start, silence, confidence, and noise scoring.

## Provider Selection

Provider settings are stored in `voice_provider_settings` with:

- provider type: `stt`, `tts`, `vad`, `transport`
- provider slug
- status
- priority
- secret reference
- capabilities
- health state

Configurations can define fallback chains. Production provider selection should choose the highest-priority healthy provider and fail over by configured chain.