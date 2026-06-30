# Voice Latency Optimization Strategy

VoiceSense optimizes for perceived conversational speed.

## Budget

Default target budget:

- Audio ingest: 30 ms
- VAD: 20 ms
- STT: 250 ms
- Reasoning: 700 ms
- TTS: 250 ms
- Total: 1200 ms

## Techniques

- Use full-duplex streaming.
- Process VAD and buffering in small chunks.
- Emit partial transcripts and partial responses.
- Start TTS as soon as safe response fragments are available.
- Keep provider clients warm through connection pooling.
- Record per-stage latency metrics.
- Fail over to configured providers when health degrades.

## Future Production Work

- Regional voice gateways.
- Provider connection pools.
- Backpressure-aware audio buffers.
- Jitter buffer tuning.
- Distributed session state.
- Load tests for concurrent sessions.