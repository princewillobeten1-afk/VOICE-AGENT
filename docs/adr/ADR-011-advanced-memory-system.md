# ADR-011: Advanced Memory System

## Status

Accepted

## Date

2026-06-28

## Related Task

Task 015 - Advanced Memory System

## Context

VoiceSense AI employees need durable memory that spans conversations and time. This memory must be more than transcripts: it needs layered memory types, evaluation, privacy, retrieval, versioning, policies, access control, and analytics.

## Decision

VoiceSense will implement a provider-agnostic Memory System with normalized tables for memories, categories, versions, links, policies, access grants, events, and statistics. Retrieval will begin with metadata/text ranking and leave embeddings/vector search to a future RAG task.

## Rationale

Memory is a high-trust domain. Storing everything would create privacy, compliance, and quality risk. A dedicated evaluator, policy model, visibility model, and forget action make memory useful without becoming uncontrolled surveillance or unbounded transcript storage.

## Alternatives Considered

- Store conversation history as memory: too noisy and not semantically useful.
- Implement vector search immediately: premature before memory governance and lifecycle are stable.
- Use one JSON table: flexible initially, but weak for audit, permissions, analytics, and scale.

## Consequences

### Positive

- AI employees can persist useful facts across conversations.
- Retrieval is provider-neutral and future vector-ready.
- Privacy, policy, access, versioning, and audit events are core concepts.
- The dashboard gives operators visibility into memory health and governance.

### Negative

- Retrieval is not semantic/vector-based yet.
- Retention cleanup workers are modeled but not implemented.
- Rollback is version-ready but not exposed as a dedicated endpoint yet.

## Follow-Up Work

- Add vector provider abstraction and embedding generation.
- Add background retention and cleanup workers.
- Add rollback endpoint.
- Add memory evaluation powered by the AI Orchestrator.
- Add deeper memory analytics and cache metrics.

## Related Documents

- `apps/api/docs/MEMORY_ARCHITECTURE.md`
- `apps/api/docs/MEMORY_LIFECYCLE.md`
- `apps/api/docs/MEMORY_RETRIEVAL_STRATEGY.md`
- `apps/api/docs/MEMORY_VERSIONING.md`
- `apps/api/docs/MEMORY_PRIVACY_MODEL.md`
- `apps/api/docs/MEMORY_API.md`
- `apps/api/docs/MEMORY_EXTENSION_GUIDE.md`
- `apps/api/migrations/versions/0010_advanced_memory_system.sql`