# Workflow Trigger Guide

Supported trigger types are modeled as strings so new trigger families can be added without changing the core schema.

## Trigger Types

- Manual
- Schedule
- Webhook
- Event
- API
- Integration trigger
- Conversation event
- AI event

Triggers should validate authorization, normalize payloads, create a workflow run, and record trigger metadata in `trigger_ref` and `input_payload`.
