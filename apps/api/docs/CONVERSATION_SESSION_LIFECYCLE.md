# Conversation Session Lifecycle

Sessions represent active channel interactions inside a conversation.

## States

- `active`
- `paused`
- `ended`
- `expired`
- `recovering`

## Operations

- Create session: `POST /v1/conversations/{conversation_id}/sessions`
- Pause session: `POST /v1/conversations/{conversation_id}/sessions/{session_id}/pause`
- Resume session: `POST /v1/conversations/{conversation_id}/sessions/{session_id}/resume`
- End session: `POST /v1/conversations/{conversation_id}/sessions/{session_id}/end`

Session state includes current speaker, active intent, pending questions, tool state, workflow state, memory references, recovery state, and expiration.