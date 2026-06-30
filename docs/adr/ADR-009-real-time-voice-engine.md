# ADR-009: Real-Time Voice Engine

## Status

Accepted

## Date

2026-06-28

## Related Task

Task 013 - Real-Time Voice Engine

## Context

VoiceSense needs a provider-agnostic, low-latency voice foundation for AI employees. The engine must eventually support browser voice, mobile, inbound calls, outbound calls, and future channels without binding the platform to one STT, TTS, VAD, or transport vendor.

## Decision

VoiceSense will implement a modular Voice Engine with explicit provider contracts, voice configurations, provider settings, voice sessions, stream events, audio metadata, and per-stage metrics.

The first implementation provides REST management and simulation endpoints, typed placeholder providers, VAD/interruption handling, and metadata-only audio storage. Real telephony, SIP, provider calls, workflow execution, and advanced reasoning remain outside Task 013.

## Rationale

Voice systems age poorly when transport, provider, and conversation logic are coupled. Separating provider contracts from session state and stream events keeps the platform flexible, testable, observable, and ready for failover.

Metadata-only audio storage is the safer default for enterprise customers because it avoids retaining sensitive voice content unless a later policy explicitly enables recording.

## Alternatives Considered

- Build directly against one voice provider: faster initially, but creates vendor lock-in and weaker failover.
- Implement telephony first: useful commercially, but premature before the core engine boundaries are stable.
- Store raw audio by default: helpful for debugging, but privacy and compliance risk is too high.

## Consequences

### Positive

- STT, TTS, VAD, and transport can be swapped by configuration and provider registry changes.
- Sessions have durable state, stream events, interruption counts, and metrics.
- The dashboard can monitor provider health, latency, active sessions, and test simulations.
- Future WebSocket/WebRTC/SIP adapters have a clear backend contract to target.

### Negative

- Real provider streaming is not implemented yet.
- The REST stream-event endpoint is a foundation, not the final high-throughput media gateway.
- Session timeout and distributed recovery need background workers in a later task.

## Follow-Up Work

- Add WebSocket and WebRTC media gateway adapters.
- Implement provider clients for selected STT/TTS vendors.
- Add distributed session state and regional routing.
- Add load tests and audio quality scoring.
- Add explicit recording policies and consent workflows.

## Related Documents

- `apps/api/docs/VOICE_ENGINE_ARCHITECTURE.md`
- `apps/api/docs/VOICE_STREAMING_LIFECYCLE.md`
- `apps/api/docs/VOICE_PROVIDER_INTERFACE.md`
- `apps/api/docs/VOICE_SESSION_LIFECYCLE.md`
- `apps/api/docs/VOICE_LATENCY_STRATEGY.md`
- `apps/api/docs/VOICE_ERROR_RECOVERY.md`
- `apps/api/docs/VOICE_ENGINE_API.md`
- `apps/api/docs/VOICE_SEQUENCE_DIAGRAMS.md`
- `apps/api/migrations/versions/0008_real_time_voice_engine.sql`