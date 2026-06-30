# Real-Time Voice Engine Architecture

Task 013 establishes the reusable Voice Engine foundation for VoiceSense real-time conversations. The system is channel-independent and designed for browser audio, mobile, inbound calls, outbound calls, and future transports.

## Pipeline

```mermaid
flowchart LR
  A[Incoming audio] --> B[Audio Stream Manager]
  B --> C[VAD]
  C --> D[STT Provider]
  D --> E[Conversation Manager]
  E --> F[AI Orchestrator Placeholder]
  F --> G[Tool Execution Placeholder]
  G --> H[Response Generator]
  H --> I[TTS Provider]
  I --> J[Audio Stream Manager]
  J --> K[Outgoing audio]
```

Every stage communicates through typed events and can be replaced independently.

## Backend Modules

- `app.voice.models`: persistence for provider settings, configurations, sessions, metrics, audio metadata, and stream events.
- `app.voice.providers`: provider-neutral STT, TTS, and VAD contracts plus placeholder adapters.
- `app.voice.service`: session lifecycle, event processing, interruption handling, metrics, and domain event emission.
- `app.voice.router`: REST foundation for management and simulation.

## Core Boundaries

- Raw audio is not stored by default. `voice_audio_metadata.storage_policy` defaults to `metadata_only`.
- Provider credentials are represented by `secret_ref`; APIs do not return raw secrets.
- Voice sessions are organization and workspace scoped.
- AI reasoning, tool execution, telephony, SIP, and billing remain placeholders by design.

## Scalability Direction

The current implementation is a foundation API. Production streaming should add a dedicated low-latency gateway with WebSocket/WebRTC adapters, regional routing, provider connection pools, async workers, and distributed session state.