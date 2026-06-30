# ADR-026: Live Data Integration Layer

## Status

Accepted

## Context

VoiceSense has a polished dashboard shell, authentication foundation, AI employee APIs, and seeded platform architecture. The dashboard still rendered static mock data for AI employees, which made the product feel disconnected from the running FastAPI backend.

The next platform step is not to wire every module at once. The safer foundation is a reusable live data pattern that starts with authentication, workspace bootstrap, AI employees, and realtime summary updates. Once this pattern is stable, conversations, notifications, analytics, billing, security, and workflow runs can follow the same approach.

## Decision

VoiceSense will introduce a frontend live data integration layer backed by the existing REST API and a lightweight server-sent event stream.

The initial implementation will:

- Store API auth tokens from real sign-in and sign-up flows in browser session storage primitives.
- Bootstrap a demo workspace and project for newly signed-in users when no active workspace exists.
- Fetch AI employees from `GET /v1/ai-employees` instead of static dashboard fixtures.
- Add a workspace live stream at `GET /v1/live/workspace-stream` for low-frequency dashboard summary events.
- Keep loading, empty, and error states inside the dashboard UI rather than hiding API failures.

Server-sent events are used first for dashboard summaries because they are simple, browser-native, and adequate for one-way realtime updates. WebSockets remain the planned mechanism for bidirectional conversation, voice, workflow, and collaboration surfaces.

## Consequences

### Positive

- The dashboard now reflects real backend state for the first core platform object: AI employees.
- Auth, workspace selection, and project seed data become part of the real user journey.
- The frontend gains a small API client that future modules can reuse and harden.
- Realtime dashboard behavior can be introduced without overbuilding the voice/conversation transport prematurely.
- Demo data is generated through backend domain models instead of static UI-only fixtures.

### Trade-offs

- Access tokens are currently passed to the SSE endpoint through a query parameter because browser `EventSource` does not support custom authorization headers. This is acceptable for local development but should move to secure cookie-backed sessions or a short-lived stream token before production.
- The first live dashboard still uses placeholder metrics for conversations, latency, and resolution until those modules expose stable aggregate APIs.
- Client-side local storage is sufficient for the current development workflow but should be revisited when production session strategy is finalized.

## Alternatives Considered

### Keep Static Fixtures Until All APIs Are Complete

Rejected. It preserves visual polish but delays discovery of auth, workspace, CORS, and data-contract issues.

### Use WebSockets Immediately

Deferred. WebSockets are necessary for conversations, voice sessions, and collaboration, but SSE is a smaller fit for read-only workspace summaries.

### Build a Full Query Cache Layer Immediately

Deferred. React Query or an equivalent cache layer is likely valuable, but the first integration benefits from a transparent API client before introducing another dependency and set of conventions.

## Follow-up Work

- Add refresh-token rotation and automatic auth recovery in the dashboard API client.
- Replace local storage stream auth with secure cookies or short-lived stream tokens.
- Add live endpoints for conversations, notifications, activity feeds, workflow runs, and call status.
- Introduce a query/cache layer once at least three dashboard modules are live.
- Add integration tests covering demo bootstrap, AI employee fetch, and stream authorization.
