# Voice Engine API

Base path: `/v1/voice`

## Providers

- `GET /providers`: returns architecture-ready STT, TTS, VAD, and transport provider catalog.

## Configurations

- `GET /configurations?workspace_id=...`
- `POST /configurations`
- `PATCH /configurations/{configuration_id}`

Configurations define language, STT/TTS providers, voice model, VAD settings, interruption settings, latency budget, and fallback chain.

## Provider Settings

- `GET /provider-settings?workspace_id=...`
- `POST /provider-settings`

Provider settings store secret references, health state, capabilities, and priority. Raw provider secrets are never stored in this API surface.

## Sessions

- `GET /sessions?workspace_id=...`
- `POST /sessions`
- `GET /sessions/{session_id}`
- `POST /sessions/{session_id}/stream-events`
- `POST /sessions/{session_id}/interrupt`
- `POST /sessions/{session_id}/resume`
- `POST /sessions/{session_id}/terminate`
- `GET /sessions/{session_id}/metrics`

## Test Run

- `POST /test-run`: returns a safe simulation response without calling real providers.