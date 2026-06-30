# AI Extension Guidelines

These guidelines define how future tasks should extend the AI Intelligence Layer after Task 011.

## Golden Rules

- Do not call model providers directly from product modules.
- Do not hardcode production prompts in feature code.
- Do not let channels own reasoning behavior.
- Do not let models execute tools directly.
- Do not expose secrets, credentials, or unrestricted raw data to prompts.
- Do not store memory without explicit scope, retention, and policy decisions.
- Emit events and trace spans for every meaningful AI action.

## Adding a Model Provider

1. Implement provider adapter behind the Provider Manager contract.
2. Declare provider capabilities.
3. Add health and failover behavior.
4. Normalize usage and cost metrics.
5. Add provider policy controls per organization.
6. Add tests for streaming, tool calls, errors, and fallback.

## Adding a Prompt Feature

1. Add prompt template and version metadata.
2. Define variables and required context inputs.
3. Add prompt test cases.
4. Record prompt history and evaluation results.
5. Keep prompt assembly centralized in Prompt Manager.

## Adding Memory

1. Choose memory layer and scope.
2. Define retention and expiration.
3. Define sensitivity and access policy.
4. Define retrieval scoring.
5. Add audit and deletion behavior.
6. Add evaluation for memory precision and recall.

## Adding a Tool

1. Register tool schema.
2. Define permissions and risk level.
3. Validate parameters before execution.
4. Execute through Tool Manager.
5. Return a structured observation.
6. Emit `ai.tool.invoked` and `ai.tool.completed`.

## Adding a Channel

1. Normalize inbound messages into conversation turns.
2. Keep channel metadata separate from reasoning context.
3. Convert AI responses into channel output format.
4. Preserve trace and latency metadata.
5. Do not fork the reasoning layer.

## Adding Multi-Agent Behavior

1. Define delegation policy.
2. Create shared context boundary.
3. Assign bounded tasks.
4. Track result confidence.
5. Resolve conflicts before final response.
6. Emit collaboration events.

## Readiness Checklist

A future AI feature is ready when it has provider abstraction, prompt management, context policy, memory policy, tool safety, observability, event emission, tenant isolation, and tests.