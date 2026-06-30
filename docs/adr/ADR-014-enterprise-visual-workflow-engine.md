# ADR-014: Enterprise Visual Workflow Automation Engine

## Status

Accepted

## Context

VoiceSense needs a flagship workflow automation platform that is intuitive for operators and powerful enough for developers and enterprise teams. Workflows must coordinate AI employees, integrations, APIs, events, approvals, variables, schedules, and long-running execution without coupling the product to any single provider or runtime implementation.

## Decision

VoiceSense will implement workflows as a first-class platform layer with visual graph metadata, version snapshots, node registry, trigger contracts, variable storage, durable runs, execution logs, schedules, templates, approval requests, and monitoring APIs.

The initial execution engine is durable and simulated. It creates workflow runs, walks configured nodes, logs node execution, models pause/resume, and emits domain events. Real AI reasoning, provider integrations, queue workers, and marketplace publishing are deferred behind extension points.

## Consequences

This creates a strong foundation for visual automation without mixing workflow orchestration with AI reasoning or integration-provider implementation. The trade-off is that early workflows do not perform real external actions. They are structurally complete but operationally simulated until adapters and workers are added.

## Alternatives Considered

- Embed workflow logic inside AI employee runtime: faster short term, but tightly couples automation to AI reasoning.
- Adopt a third-party workflow engine directly: useful for execution, but risks constraining VoiceSense's UX and AI-native product model.
- Build only a frontend canvas first: visually impressive, but weakens the platform foundation.

## Follow-Ups

- Add queue-backed execution workers.
- Add idempotency, leases, heartbeats, retries, and dead-letter handling.
- Connect integration actions through the Integration Framework.
- Connect AI nodes through the AI architecture and Retrieval/Memory systems.
- Add collaborative editing for workflow builders.
