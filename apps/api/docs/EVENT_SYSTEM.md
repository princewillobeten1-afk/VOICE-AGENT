# Event System

VoiceSense uses a durable internal event system to decouple product modules from side effects such as notifications, webhooks, analytics, and future workflow triggers.

## Core Concepts

- `DomainEvent`: application-level event object emitted by modules.
- `domain_event_records`: durable event store for metadata, payload, correlation IDs, processing state, and retry metadata.
- `event_subscribers`: registry of consumers that can process matching event types.
- `event_logs`: per-subscriber processing records for observability, retries, and dead-letter readiness.
- `DeliveryAttempt`: channel-level delivery tracking for notifications and future external channels.

## Publishing Flow

1. A module creates a `DomainEvent`.
2. The module publishes through `DurableEventPublisher` or `publish_domain_event`.
3. The event is persisted to `domain_event_records`.
4. Subscribers process the event without requiring the publishing module to know about notification delivery.
5. Subscriber outcomes are written to `event_logs`.

## Reliability Model

The current implementation processes the notification subscriber synchronously after persistence. The schema is ready for background workers, retries, and dead-letter queues by tracking `status`, `retry_count`, `processed_at`, and `error_message`.

## Correlation

Events support:

- `correlation_id` for tracing a user or workflow journey.
- `causation_id` for linking child events to parent events.
- `event_version` for schema evolution.
- `idempotency_key` for duplicate prevention.

## Future Expansion

- Queue-backed dispatcher using Redis, Celery, or a managed queue.
- Dead-letter queue table or topic.
- Subscriber filtering by event type and tenant.
- Metrics export for queue health and processing latency.