# Conversation Engine API

Base path: `/v1/conversations`

## Conversations

- `GET /?workspace_id=...`
- `POST /`
- `GET /{conversation_id}`
- `POST /{conversation_id}/complete`

## Sessions

- `POST /{conversation_id}/sessions`
- `POST /{conversation_id}/sessions/{session_id}/pause`
- `POST /{conversation_id}/sessions/{session_id}/resume`
- `POST /{conversation_id}/sessions/{session_id}/end`

## Turns and Context

- `POST /{conversation_id}/turns`
- `POST /{conversation_id}/context-snapshots`
- `POST /{conversation_id}/goals`

## Handoff and Analytics

- `POST /{conversation_id}/handoff`
- `GET /{conversation_id}/analytics`