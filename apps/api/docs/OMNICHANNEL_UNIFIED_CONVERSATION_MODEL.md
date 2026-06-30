# Unified Conversation Model

A unified conversation lets a customer move from call to WhatsApp to email to web chat to SMS without losing context.

## Records

- `customer_identities` maps phone, email, CRM ID, external ID, workspace identity, and provider user IDs to one canonical customer reference.
- `channel_sessions` captures channel-specific thread/session context.
- `omnichannel_messages` stores normalized inbound and outbound messages.
- `customer_timeline_events` replays the customer journey across calls, messages, workflows, tools, and AI decisions.

## Continuation

Channel switching should preserve `conversation_id`, `customer_identity_id`, workflow state, memory references, and context state.