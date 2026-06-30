# Telephony Developer Guide

## Adding A Provider

1. Add the provider key to the provider catalog.
2. Define capability metadata for calls, media streams, recordings, DTMF, SIP, failover, and webhooks.
3. Implement the adapter behind the future provider interface.
4. Store credentials as secret references, never plaintext database fields.
5. Normalize provider webhooks into `telephony_call_events`.

## Integrating With Voice Engine

Create or attach a `voice_sessions` row when call audio should be processed by AI. Store the `voice_session_id` on `telephony_calls` and let Voice Engine handle streaming, latency budgets, interruption, STT, TTS, and audio events.

## Observability

Emit domain events for lifecycle changes and write call metrics for call duration, queue time, provider latency, transfer count, recording status, and error classes.

## Testing Guidance

Provider adapters should use contract tests with signed webhook fixtures and simulated call state transitions. Product-level tests should verify routing, tenant isolation, permissions, and event emission.