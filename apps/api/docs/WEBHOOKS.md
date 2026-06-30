# Webhook Guide

Webhooks let external systems subscribe to VoiceSense platform events.

## Placeholder Events

- `user.created`
- `agent.created`
- `conversation.started`
- `conversation.ended`
- `call.started`
- `call.finished`
- `knowledge.uploaded`
- `workflow.executed`

## Delivery Records

Each delivery attempt should record:

- Endpoint
- Event type
- Attempt number
- Status
- Request ID
- Response status code
- Response time
- Error message

## Signing

Webhook signing secrets are shown only once on creation. Store only a secure reference or hash.

## Retries

Default policy: exponential backoff with a maximum of 8 attempts. Future implementations should make this configurable per endpoint.