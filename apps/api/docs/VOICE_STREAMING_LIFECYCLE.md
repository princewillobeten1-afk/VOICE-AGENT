# Voice Streaming Lifecycle

## Session Start

1. Client requests `POST /v1/voice/sessions`.
2. VoiceSense authenticates the user and scopes the session to organization/workspace.
3. The session stores transport mode, configuration, context snapshot, timeout, and initial stream event.
4. Metadata-only inbound/outbound audio records are created.

## Streaming Events

Clients submit stream lifecycle events to `POST /v1/voice/sessions/{session_id}/stream-events`.

Supported foundational events include:

- `audio.chunk`
- `vad.speech_detected`
- `vad.silence`
- `stt.partial`
- `stt.final`
- `response.partial`
- `tts.partial`
- `playback.stop`
- `user.interrupt`
- `session.resumed`
- `session.ended`

## Audio Chunk Path

When an `audio.chunk` event is received, the foundation pipeline creates a typed `AudioChunk`, runs placeholder VAD, emits VAD events, and emits placeholder STT partials when speech is detected.

## Barge-In

`POST /v1/voice/sessions/{session_id}/interrupt` increments `interrupt_count`, clears the active response, records state preservation, and emits `playback.stop`.

## Termination

`POST /v1/voice/sessions/{session_id}/terminate` marks the session ended and records the termination reason.