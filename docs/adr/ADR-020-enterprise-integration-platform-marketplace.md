# ADR-020: Enterprise Integration Platform and Connector Marketplace

## Status

Accepted

## Context

VoiceSense needs an ecosystem where organizations, developers, and future partners can connect external systems to AI employees without changing core platform code. The previous integration foundation provided marketplace seeds, connected accounts, credentials, actions, triggers, logs, health checks, API keys, and webhooks. Task 023 expands that foundation into a full connector marketplace and lifecycle platform.

## Decision

We will extend the existing Integration Platform instead of creating a parallel module. Connector registry, marketplace metadata, installations, credentials, sync jobs, playground runs, version records, health, analytics, and dependency mapping will share one integration namespace and data model.

Connector code will follow a universal lifecycle: install, authenticate, configure, validate permissions, health check, sync, emit events, execute actions/triggers, report analytics, and manage versions. Credentials remain secret-reference based.

## Consequences

- Organizations get one marketplace and installation flow for all connector types.
- Developers get a consistent SDK contract for future connector implementations.
- Sync, health, versioning, playground, and analytics become reusable platform primitives.
- Production credentials, paid marketplace functionality, community publishing workflows, and revenue sharing remain outside this task.

## Alternatives Considered

- Create a new marketplace service separate from integrations. Rejected because it would duplicate connected-account, credential, health, webhook, and action/trigger concepts.
- Keep marketplace as static seed data only. Rejected because enterprise connectors need installation lifecycle, versioning, sync, health, and analytics.