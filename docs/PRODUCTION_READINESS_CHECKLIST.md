# Production Readiness Checklist

## Application

- Dashboard production build passes.
- API imports and OpenAPI generation pass.
- Database migrations apply idempotently.
- Environment variables are documented.
- Health endpoints are available.

## Operations

- Logs include request IDs.
- Security headers are enabled.
- Rate limiting is configured.
- Backups and restore process are documented.
- Monitoring and alerting are configured.
- Release process and rollback plan are documented.

## Product Quality

- Core journeys have loading, empty, and error states.
- Navigation works on desktop, tablet, and mobile.
- Accessibility checks are performed before release.
- Demo workspace is available.
- User, admin, developer, API, and architecture docs are linked.