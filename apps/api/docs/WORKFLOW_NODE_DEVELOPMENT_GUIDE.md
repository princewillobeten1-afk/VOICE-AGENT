# Workflow Node Development Guide

Nodes are registered through `NodeRegistry`. A node definition includes type, label, group, description, inputs, outputs, config schema, async capability, and pause capability.

## Node Families

- Core: start, end.
- Control: delay, condition, loop, switch, merge, split, wait, error handler, sub workflow.
- Human: human approval.
- Trigger: webhook, schedule.
- Data: variable, transform.
- AI: AI employee, prompt, memory, knowledge search, tool call, decision, supervisor, multi-agent coordinator.
- Integration: email, CRM, calendar, database, Slack, WhatsApp, storage, payments, HTTP request, custom API.

## Adding Nodes

Add a node definition to the registry, define its config schema, and implement an execution adapter. Keep provider-specific code outside core workflow execution.
