# Connector Development Guide

Connectors isolate provider-specific logic from the VoiceSense core application.

## Required Interface

Each connector must implement:

```python
connect(context, credentials_ref)
disconnect(context)
validate(context)
execute_action(context, action_key, payload)
execute_trigger(context, trigger_key, payload)
refresh_credentials(context)
test_connection(context)
```

## Connector Rules

- Do not expose provider SDK objects to application services.
- Do not return raw credentials or tokens.
- Use `credentials_ref` to retrieve secrets from the configured secret manager.
- Return structured `ConnectorResult` values.
- Emit events through the integration service, not directly from provider code.
- Log execution and health outcomes through connection logs and health checks.

## Registration

Future connectors should register with `connector_registry.register(key, connector)` and be referenced by `connector_definitions.connector_key`.

## Actions and Triggers

Actions and triggers should be declared in database definitions so the marketplace, workflow builder, and API documentation can discover them dynamically.