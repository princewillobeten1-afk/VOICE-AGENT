# ADR-024: VoiceSense AI Studio Platform

## Status

Accepted

## Context

VoiceSense needs a flagship AI engineering workspace where developers, prompt engineers, product teams, and businesses can build, test, evaluate, compare, deploy, replay, and continuously improve AI Employees. This must go beyond a prompt editor and become a provider-agnostic AI development platform.

## Decision

Create a dedicated `app/aistudio` module with AI Studio-specific tables and APIs for prompts, prompt versions, templates, playground runs, simulations, evaluations, test suites, benchmarks, experiments, deployments, comments, activity logs, analytics records, interaction timelines, and replay sessions.

AI Studio references existing modules such as AI employees, voice, conversations, knowledge, memory, tools, workflows, AIOps, and security rather than owning their runtime behavior. Prompt deployments are treated as independently deployable artifacts with approval and rollback metadata.

## Consequences

- Prompt engineering becomes version-controlled and auditable.
- Evaluation, regression testing, benchmarking, and deployment can evolve as first-class platform workflows.
- Provider-specific execution can be added behind adapters without changing the AI Studio data model.
- Automatic prompt generation, autonomous optimization, reinforcement learning, and model training remain explicitly out of scope for this foundation.

## Alternatives Considered

- Extend the existing AI employee `prompts` table. Rejected because AI Studio needs a much broader lifecycle and would overload the employee configuration module.
- Build live model execution first. Deferred because durable engineering workflows and contracts should exist before provider-specific runtime orchestration.
- Couple prompt deployments to app releases. Rejected because AI teams need safe prompt iteration independent of platform deployments.