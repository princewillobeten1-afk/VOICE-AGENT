# Workflow Architecture

Task 017 introduces the Enterprise Visual Workflow Automation Engine for VoiceSense. The engine lets teams model, version, execute, pause, resume, and monitor business automations that coordinate AI employees, integrations, APIs, events, approvals, and custom logic.

## Scope

The workflow layer owns visual workflow metadata, node registry, trigger contracts, variable references, version history, durable execution records, execution logs, schedules, approval requests, and monitoring.

It does not execute real provider integrations, AI reasoning, billing, or marketplace publishing in this task.

## Core Modules

- `app/workflow/models.py`: workflow, version, graph, execution, variable, schedule, template, and approval models.
- `app/workflow/registry.py`: reusable node registry for core, control, AI, human, trigger, data, utility, and integration nodes.
- `app/workflow/service.py`: version snapshots, expression interpolation, simulated execution, domain event publishing, and monitoring summary.
- `app/workflow/router.py`: REST API endpoints.

## Execution Model

Executions are durable records in `workflow_runs`. Each run can track trigger source, current node, execution state, variables, retry count, pause state, resume state, output, duration, and errors. Node execution writes structured rows to `workflow_execution_logs`.

## Event Integration

The workflow service emits domain events such as `workflow.created`, `workflow.updated`, `workflow.published`, `workflow.started`, `workflow.paused`, and `workflow.completed` through the existing event system.
