# ADR-005: Event-Driven Notification System

## Status

Accepted

## Date

2026-06-27

## Related Task

Task 009 - Notification & Event System

## Context

VoiceSense needs a communication backbone for user notifications, internal processing, auditability, realtime updates, future webhooks, and future integrations. The platform will eventually process high event volume across many tenants, and product modules should not be tightly coupled to delivery mechanisms such as in-app notifications, email, SMS, Slack, or webhooks.

## Decision

VoiceSense will use a durable internal event system and a separate notification engine.

Product modules publish domain events. Subscribers consume those events and perform side effects. The notification engine is one subscriber that creates in-app notifications and records delivery attempts. External notification channels remain placeholders until provider infrastructure is selected.

Events are stored in `domain_event_records` with correlation IDs, causation IDs, event versioning, retry state, and processing state. Subscriber processing is tracked in `event_logs`. Notification delivery is tracked in `delivery_attempts`.

## Rationale

This keeps business logic focused on business state while allowing notifications, webhooks, analytics, and future automation to evolve independently. Durable event records also improve observability, auditability, debugging, and future replay/backfill workflows.

The architecture can start synchronously inside FastAPI while preserving a clean path to queue-backed workers and dead-letter queues.

## Alternatives Considered

- Directly create notifications inside each feature module: simpler initially, but creates coupling and makes external channels harder to add.
- Use only audit logs as events: avoids new tables, but audit logs are not designed for retries, subscribers, delivery attempts, or replay.
- Add a full queue system immediately: powerful, but premature before background worker infrastructure is established.
- Build provider-specific email/SMS integrations now: out of scope and would distract from the platform foundation.

## Consequences

### Positive

- Publishers and consumers are loosely coupled.
- Notification channels can be added without changing business modules.
- Events are queryable, auditable, and correlation-ready.
- Retry, dead-letter, and queue-backed processing have a clear schema path.
- The UI can expose notification and event health independently.

### Negative

- Synchronous subscriber processing is not enough for high throughput production workloads.
- Event schemas need discipline to prevent payload drift.
- Additional tables increase operational complexity.

### Follow-Up Work

- Add queue-backed event dispatch workers.
- Add dead-letter queue handling and replay tools.
- Add WebSocket or SSE transport implementation.
- Add provider-backed email and webhook delivery.
- Add event metrics dashboards and alerting.

## Related Documents

- `apps/api/docs/EVENT_SYSTEM.md`
- `apps/api/docs/NOTIFICATIONS.md`
- `apps/api/docs/NOTIFICATION_API.md`
- `apps/api/docs/EVENT_PUBLISHING_GUIDELINES.md`
- `apps/api/migrations/versions/0005_notification_event_system.sql`