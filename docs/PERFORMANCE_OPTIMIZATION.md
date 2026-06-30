# Performance Optimization Plan

## Frontend

- Use Next.js route-level code splitting.
- Keep heavy runtime demos out of first render.
- Prefer stable dimensions for cards, widgets, tables, and skeletons.
- Respect reduced-motion preferences.
- Track bundle growth before adding rich editors, canvas, or replay engines.

## Backend

- Preserve organization and workspace indexes on every multi-tenant table.
- Use pagination for high-volume records before public launch.
- Move expensive analytics to background aggregation jobs.
- Keep request IDs in every response and log event.
- Replace in-memory rate limiting with Redis-backed distributed limits before multi-instance deployment.

## Database

- Continue composite indexes by workspace/status/type/time.
- Consider partitioning for event, analytics, audit, metrics, and message tables as volume grows.
- Keep migrations idempotent for local developer recovery.