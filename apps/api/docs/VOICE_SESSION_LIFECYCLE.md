# Voice Session Lifecycle

Voice sessions are long-running, recoverable records for real-time conversations.

## States

- `initializing`
- `active`
- `recovering`
- `interrupted`
- `ended`
- `failed`
- `timed_out`

## Tracked State

`voice_sessions` tracks current speaker, active response, pending tool calls, context snapshot, memory update placeholders, conversation state, transport state, timeout, and termination details.

## Recovery

Session resume emits `session.resumed` and preserves conversation state. Production recovery should restore transport state from distributed session storage and reconnect provider streams when supported.

## Timeout

Each session has `timeout_at`. Background workers should eventually close expired sessions and emit timeout events.