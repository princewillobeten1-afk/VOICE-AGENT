# Logging Strategy

VoiceSense uses structured JSON logs with request IDs.

## Log Categories

- Request logs: method, path, duration, request ID.
- Error logs: exception type, message, request ID.
- Security logs: login attempts, token revocation, suspicious access.
- Audit logs: business-relevant changes and operator actions.
- Performance logs: latency, provider timings, queue delays.

## Request IDs

Every request receives `request.state.request_id`. If the caller sends `x-request-id`, VoiceSense preserves it; otherwise a UUID is generated.

## Sensitive Data

Never log passwords, refresh tokens, API keys, OAuth credentials, raw customer secrets, or full authorization headers.

## Future Direction

Logs should eventually flow to a centralized observability backend with traces and metrics. The current formatter keeps the output compatible with most log collectors.