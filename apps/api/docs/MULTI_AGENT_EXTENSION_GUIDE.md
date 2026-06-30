# Multi-Agent Developer Extension Guide

Use this guide when extending collaboration behavior.

## Add Routing Logic

Routing should remain in service-level strategy modules. It should not be embedded inside AI model prompts. Add scoring dimensions such as expertise, tool access, availability, latency, success rate, cost, or supervisor preference.

## Add Communication Events

Use collaboration messages for direct messages, broadcasts, status updates, and task requests. Use collaboration logs for audit timeline events.

## Integrate Memory and Workflows

Shared memory references should point to memory records and include permission summaries. Workflow integration should attach `workflow_run_id` to collaboration sessions so delegations remain traceable.
