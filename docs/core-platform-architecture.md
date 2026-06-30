# Core Platform Architecture

VoiceSense is organized as a modular, domain-oriented platform. The architecture separates identity, workspace hierarchy, AI employee configuration, knowledge, conversations, workflow, integrations, storage, analytics, billing placeholders, notifications, and audit concerns.

## Architectural Principles

- Clean Architecture: domain logic should not depend on transport, UI, or provider implementations.
- Domain-Driven Design: each feature area owns its models, schemas, repositories, services, and events.
- Organization Isolation: all tenant data is scoped by `organization_id`, and product work is further scoped by `workspace_id` where applicable.
- Provider Agnosticism: storage, AI providers, telephony, messaging, and integrations use replaceable references and adapters.
- Observability First: requests, security actions, domain events, audit logs, and performance signals are structured.

## Backend Folder Standard

Each backend domain follows this shape as it becomes active:

```text
app/<domain>/
  models.py
  schemas.py
  repository.py
  service.py
  router.py
  events.py
```

Current domain foundations:

- `identity`: users, organizations, memberships, teams, roles, sessions, invitations.
- `workspace`: workspaces and projects.
- `ai`: agents, agent versions, voices, prompts.
- `knowledge`: knowledge bases, data sources, documents, embedding placeholders.
- `conversations`: conversations, messages, calls, call events.
- `workflow`: workflows, runs, automation events.
- `integrations`: connected accounts, API keys, webhook endpoints, external integrations.
- `storage`: files and uploads.
- `analytics`: usage records, analytics events, metric snapshots.
- `billing`: placeholder billing account and subscription records.
- `notifications`: notifications and preferences.
- `audit`: security events and domain event records.

## Dependency Direction

Domain modules may depend on `app.core` and identity primitives, but should not depend on each other directly unless the database relationship requires it. Cross-domain behavior should be coordinated through services and events.

## Hierarchy

```text
Organization
  Workspace
    Project
      Agent
        AgentVersion
      Conversation
        Message
        Call
          CallEvent
      KnowledgeBase
        DataSource
        Document
      Workflow
        WorkflowRun
```

## Foundation Code Added

- `app/core/responses.py`: response envelopes and pagination metadata.
- `app/core/errors.py`: standard application exceptions and FastAPI handlers.
- `app/core/logging.py`: structured JSON logging and request ID middleware.
- `app/core/events.py`: domain event envelope and event publisher interface.
- `app/core/repository.py`: base repository convention.
- `app/core/models.py`: shared SQLAlchemy mixins.
- `migrations/versions/0002_core_platform_foundation.sql`: platform schema expansion.