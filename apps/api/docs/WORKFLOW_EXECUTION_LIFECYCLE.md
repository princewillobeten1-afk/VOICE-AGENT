# Workflow Execution Lifecycle

1. A workflow is created as a draft.
2. Draft changes create `workflow_versions` snapshots.
3. Publishing marks a version as published and stores it as the current version.
4. A trigger creates a `workflow_runs` record.
5. The execution engine evaluates nodes and writes `workflow_execution_logs`.
6. Long-running nodes can pause the run.
7. A run can resume from persisted execution state.
8. Completion stores output payload, duration, status, and monitoring metrics.

## Fault Tolerance

Task 017 models restart-safe execution state but runs locally. Production workers should use queues, idempotency keys, lease/heartbeat records, retry policies, and dead-letter handling.

## Pause and Resume

Pause-capable nodes include delay, wait, and human approval. A paused run stores current node and resume metadata. Resume changes the run status and records completion in the foundation implementation.
