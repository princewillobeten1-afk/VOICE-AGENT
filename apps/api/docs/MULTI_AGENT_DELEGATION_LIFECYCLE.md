# Delegation Lifecycle

1. A source AI employee, workflow, conversation, or user creates a delegation request.
2. The routing engine evaluates role, team membership, availability, workload, permissions, and policy placeholders.
3. A collaboration session is created or reused.
4. A delegation event records source, target, task payload, depth, confidence, status, and routing reason.
5. A task request message is written to the communication bus.
6. Shared context is attached to the session.
7. Timeline logs and domain events make the delegation auditable.
8. Future runtime workers complete, retry, escalate, or reassign the delegation.

## Guardrails

Delegation depth, allowed delegation paths, department restrictions, approval requirements, and escalation rules are modeled in collaboration policies.
