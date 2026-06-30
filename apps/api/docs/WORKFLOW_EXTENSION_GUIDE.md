# Workflow Extension Guide

Workflow extensions should preserve the core engine boundary.

## Add an Execution Adapter

1. Register or reference a node type.
2. Validate node config against its schema.
3. Execute provider-specific logic outside the core service.
4. Return structured output and latency.
5. Write execution logs.
6. Emit domain events for major state changes.

## Add Queue Workers

Production workers should claim queued runs, heartbeat active execution, apply retry policy, persist current node state, and release or dead-letter failed runs.

## Add Provider Integrations

Use the Task 010 Integration Framework. Workflow nodes should reference integration actions and connected accounts, not embed provider credentials.
