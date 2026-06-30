# ADR-010: Universal Conversation Engine

## Status

Accepted

## Date

2026-06-28

## Related Task

Task 014 - Universal Conversation Engine

## Context

VoiceSense needs one conversation architecture for voice, chat, SMS, WhatsApp, Slack, Teams, email, and future channels. Channel-specific implementations must not fragment state, analytics, handoff, or AI decision flow.

## Decision

VoiceSense will use `conversations` as the aggregate root and add normalized engine tables for sessions, turns, goals, context snapshots, engine events, and analytics. Channel adapters normalize inputs into the same session and turn model. Voice sessions can link to conversation sessions, but the Conversation Engine owns conversation state.

## Rationale

A universal model keeps AI employees consistent across channels and lets future memory, RAG, workflows, and human handoff plug into a stable contract. It also makes analytics comparable across voice and text channels.

## Alternatives Considered

- Build separate conversation models per channel: simpler initially, but would fracture state and analytics.
- Put all state in one JSON blob: flexible, but weak for querying, auditing, and scaling.
- Implement live human handoff now: premature before the handoff contract and summary flow are stable.

## Consequences

### Positive

- Channel-independent lifecycle and turn model.
- Session pause, resume, end, and recovery state are explicit.
- Context, goals, intent placeholders, and analytics are ready for future AI systems.
- Domain events integrate with the notification/event architecture.

### Negative

- Intent detection, RAG, memory persistence, workflow execution, and live agents remain placeholders.
- High-throughput streaming adapters need future WebSocket/channel gateway work.

## Follow-Up Work

- Implement real intent detection and entity extraction.
- Connect memory, knowledge, and workflow engines.
- Add live human agent transfer.
- Add distributed session state and conversation workers.
- Build deeper analytics dashboards.

## Related Documents

- `apps/api/docs/CONVERSATION_ENGINE_ARCHITECTURE.md`
- `apps/api/docs/CONVERSATION_LIFECYCLE.md`
- `apps/api/docs/CONVERSATION_SESSION_LIFECYCLE.md`
- `apps/api/docs/CONVERSATION_STATE_MANAGEMENT.md`
- `apps/api/docs/CONVERSATION_CONTEXT_MANAGEMENT.md`
- `apps/api/docs/CONVERSATION_ENGINE_API.md`
- `apps/api/docs/CONVERSATION_EXTENSION_GUIDE.md`
- `apps/api/docs/CONVERSATION_SEQUENCE_DIAGRAMS.md`
- `apps/api/migrations/versions/0009_universal_conversation_engine.sql`