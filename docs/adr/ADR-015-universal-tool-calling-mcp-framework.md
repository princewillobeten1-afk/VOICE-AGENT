# ADR-015: Universal Tool Calling and MCP Framework

## Status

Accepted

## Context

VoiceSense AI employees need a safe, observable way to use internal tools, integrations, APIs, workflows, enterprise services, custom functions, and future MCP servers. Direct model-to-tool calls would make permissions, validation, retries, auditability, and provider neutrality difficult to enforce consistently.

## Decision

VoiceSense will route all tool use through a Universal Tool Runtime. Tools are registered with metadata, schemas, auth requirements, permission requirements, timeout, retry policy, version, health, and category. Executions are durable records with validation results, permission results, logs, latency, retry count, cost estimates, and structured outputs.

The framework also models MCP server definitions, resource discovery, prompt discovery, session policy, and transport abstraction, while deferring external MCP communication.

## Consequences

This creates a secure tool boundary for AI employees and workflows. New tools can be registered dynamically without changing core runtime code. The trade-off is that Task 018 execution is simulated until concrete provider and MCP adapters are implemented.

## Alternatives Considered

- Let LLM providers call functions directly: fast but weakens central control and auditability.
- Put tool execution inside each AI employee: duplicates security and runtime concerns.
- Treat integrations as tools without a registry: simpler but makes discovery, versioning, and permissioning brittle.

## Follow-Ups

- Add concrete runtime adapters.
- Add queue-backed execution for long-running tools.
- Add full JSON Schema validation.
- Add circuit breakers and timeout enforcement.
- Implement MCP transport adapters.
- Add tool evaluation and safety test suites.
