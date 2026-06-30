# Universal Integration Framework

The Universal Integration Framework is the provider-agnostic backbone for third-party services in VoiceSense. It is designed around reusable connectors, secure connection management, marketplace metadata, action definitions, trigger definitions, health checks, and event emission.

## Goals

- Add new integrations without changing core application architecture.
- Keep provider-specific behavior behind connector implementations.
- Support OAuth 2.0, OAuth PKCE, API keys, bearer tokens, basic auth, JWT, and custom headers.
- Store only secret references and fingerprints in the application database.
- Emit integration events through the Task 009 event system.
- Prepare for marketplace discovery, versioning, compatibility, documentation, and installation flows.

## Core Tables

- `external_integrations`: marketplace provider records.
- `integration_categories`: marketplace category taxonomy.
- `connector_definitions`: connector handler metadata and interface versioning.
- `connected_accounts`: tenant/workspace-scoped installed connections.
- `integration_credentials`: secret references, fingerprints, rotation and expiry metadata.
- `integration_action_definitions`: reusable provider action contracts.
- `integration_trigger_definitions`: reusable trigger contracts.
- `connection_logs`: connection lifecycle and execution logs.
- `integration_health_checks`: health status history.

## Connector Boundary

The application calls `IntegrationConnector`, not provider SDKs. Connectors expose:

- `connect()`
- `disconnect()`
- `validate()`
- `execute_action()`
- `execute_trigger()`
- `refresh_credentials()`
- `test_connection()`

Task 010 includes a placeholder connector only. Real providers will register behind this interface later.

## Event Integration

The framework emits events such as:

- `integration.connection.created`
- `integration.connection.updated`
- `integration.connection.deleted`
- `integration.connection.reconnected`
- `integration.credentials.rotated`
- `integration.action.executed`
- `integration.trigger.fired`

## Non-Goals

- No provider-specific integrations.
- No real OAuth flow implementation.
- No external provider SDKs.
- No AI workflows.