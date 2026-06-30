# ADR-006: Universal Integration Framework

## Status

Accepted

## Date

2026-06-27

## Related Task

Task 010 - Universal Integration Framework

## Context

VoiceSense will eventually connect AI employees to hundreds of external systems across communication, CRM, calendars, storage, automation, messaging, payments, AI providers, databases, and project management. Implementing each provider directly inside business logic would create coupling, security risk, and long-term maintenance problems.

## Decision

VoiceSense will use a provider-agnostic integration framework built around connector definitions, installed connections, secret references, action definitions, trigger definitions, health checks, and connection logs.

Provider-specific behavior must live behind the `IntegrationConnector` interface. The application stores marketplace metadata, connection metadata, and credential references, but not raw provider secrets. Integration lifecycle operations emit domain events through the Task 009 event system.

## Rationale

This creates a stable extension point for future provider implementations while preserving tenant isolation, auditability, and marketplace discovery. It also allows the workflow builder, AI employees, API docs, and dashboard to discover integration capabilities from standardized action and trigger definitions.

Secrets are intentionally represented as external secret references plus fingerprints. This avoids building insecure app-database secret storage before KMS or a managed secret provider is selected.

## Alternatives Considered

- Implement specific integrations first: faster visible demos, but risks provider logic leaking into core modules.
- Store raw encrypted credentials in PostgreSQL now: convenient, but unsafe without a hardened KMS/envelope encryption design.
- Use only webhooks for integrations: simple, but insufficient for actions, auth refresh, health checks, and triggers.
- Add a marketplace UI without backend contracts: visually useful, but not a real platform foundation.

## Consequences

### Positive

- New providers can be added behind a common connector interface.
- Marketplace, actions, triggers, credentials, health, and logs have normalized data models.
- Credential handling is secret-manager-ready and does not expose raw secrets.
- Integration activity emits platform events for notifications, audits, and future automation.

### Negative

- Real provider integrations require additional connector implementation work.
- Secret-manager/KMS integration is still required before production credentials can be stored.
- Placeholder connector behavior is not a substitute for provider validation.

### Follow-Up Work

- Add KMS or managed secret provider integration.
- Implement OAuth authorization flows and PKCE callbacks.
- Add queue-backed action/trigger execution.
- Add provider SDK adapters one integration at a time.
- Add marketplace install/version compatibility workflows.

## Related Documents

- `apps/api/docs/INTEGRATION_FRAMEWORK.md`
- `apps/api/docs/CONNECTOR_DEVELOPMENT_GUIDE.md`
- `apps/api/docs/INTEGRATION_AUTHENTICATION.md`
- `apps/api/docs/INTEGRATION_API.md`
- `apps/api/migrations/versions/0006_universal_integration_framework.sql`