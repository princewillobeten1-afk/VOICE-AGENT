# Event Publishing Guidelines

Use events when a platform action may need downstream processing, notifications, analytics, webhooks, automation, or audit visibility.

## Event Naming

Use past-tense dot notation:

- `user.created`
- `api_key.created`
- `file.uploaded`
- `conversation.started`
- `workflow.executed`

## Payload Design

Payloads should be small, explicit, and versionable. Store IDs and display-safe labels, not secrets or large records.

Good payload example:

```json
{
  "user_name": "Ada Lovelace",
  "organization_name": "Acme Co",
  "file_name": "support-policy.pdf"
}
```

## Required Metadata

Every event should include:

- `organization_id`
- `workspace_id` when workspace scoped
- `actor_user_id` when user initiated
- `aggregate_type`
- `aggregate_id`
- `event_version`
- `correlation_id` for multi-step flows

## Do Not

- Do not send provider credentials or tokens in event payloads.
- Do not let business modules call email/SMS/webhook providers directly.
- Do not encode notification-specific copy in core business logic.
- Do not rely on event payloads as the only source of truth for critical state.