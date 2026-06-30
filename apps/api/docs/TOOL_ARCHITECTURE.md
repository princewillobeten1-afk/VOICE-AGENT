# Tool Architecture

Task 018 introduces the Universal Tool Calling and MCP Framework for VoiceSense. AI employees must never call tools directly. All tool use flows through the Tool Runtime for discovery, validation, permission checks, execution, logging, and analytics.

## Scope

The tool platform owns tool registration, schemas, permissions, credentials by reference, execution records, runtime logs, health metrics, analytics, and future MCP server definitions.

It does not implement real third-party integrations, external MCP communication, marketplace publishing, or AI reasoning.

## Modules

- `app/tools/models.py`: tool registry, versions, permissions, credentials, executions, logs, health, and MCP server models.
- `app/tools/service.py`: validation, permission checks, simulated execution runtime, event emission, and analytics.
- `app/tools/router.py`: REST APIs for registry, runtime, history, analytics, and MCP placeholders.

## Runtime Boundary

Every tool call follows request normalization, permission check, schema validation, authentication lookup, execution, response validation, logging, result return, and analytics. Task 018 simulates execution after guardrails pass.
