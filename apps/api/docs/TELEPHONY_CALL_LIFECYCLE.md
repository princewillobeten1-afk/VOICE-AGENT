# Telephony Call Lifecycle

## States

`created` -> `started` -> `queued` -> `ringing` -> `answered` -> `bridged` -> `held` -> `transferring` -> `ended`.

Failure states include `failed`, `busy`, `no_answer`, `canceled`, and `provider_error`.

## Event Timeline

Each meaningful transition creates a `telephony_call_events` row. Events are append-only and sequence-numbered so future live monitoring can replay a call timeline.

Recommended events:

- `call.started`
- `provider.selected`
- `routing.matched`
- `queue.entered`
- `voice_session.opened`
- `dtmf.received`
- `recording.started`
- `transfer.requested`
- `call.ended`

## Voice Handoff

When a call needs AI audio, Telephony creates or references a Voice Engine session and stores `voice_session_id`. Voice Engine then handles stream processing while Telephony remains the call-control source of truth.

## Domain Events

Call events publish names under `telephony.*` through the existing notification/event system so AIOps, workflows, webhooks, and analytics can subscribe without tight coupling.