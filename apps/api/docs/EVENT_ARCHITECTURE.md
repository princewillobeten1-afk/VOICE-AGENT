# Event Architecture

VoiceSense uses domain events to decouple future automation, analytics, notifications, workflow triggers, and audit trails.

## Event Envelope

Domain events use this shape:

```json
{
  "id": "uuid",
  "name": "conversation.started",
  "occurred_at": "timestamp",
  "organization_id": "uuid",
  "workspace_id": "uuid",
  "actor_user_id": "uuid",
  "aggregate_type": "conversation",
  "aggregate_id": "uuid",
  "payload": {}
}
```

## Initial Event Names

- `user.created`
- `agent.created`
- `conversation.started`
- `conversation.ended`
- `call.started`
- `call.finished`
- `knowledge.uploaded`
- `workflow.executed`

## Storage

Durable records live in `domain_event_records`. Future async delivery can publish to Redis Streams, Kafka, SQS, or another broker through the `EventPublisher` interface.

## Rules

- Events describe facts that already happened.
- Events should be immutable.
- Events should include tenant scope when available.
- Events should not contain secrets or raw credentials.