# VoiceSense Architecture

## Recommended Foundation

VoiceSense should begin as a modular TypeScript monorepo with clear boundaries between product UI, APIs, real-time voice infrastructure, shared contracts, and deployment infrastructure.

## Core Domains

### Identity and Workspace

Handles users, organizations, roles, permissions, billing boundaries, audit trails, and enterprise controls.

### AI Employees

Defines employee profiles, instructions, behavior policies, channels, memory settings, provider configuration, and deployment state.

### Conversations

Stores sessions, turns, transcripts, audio metadata, messages, outcomes, evaluations, and observability events.

### Voice Runtime

Owns low-latency audio sessions, streaming STT, LLM orchestration, TTS playback, barge-in behavior, interruption handling, and phone-provider integration.

### Tools and Workflows

Provides safe access to business systems, actions, approval gates, scheduled workflows, webhooks, and integration credentials.

### Knowledge and Memory

Indexes company knowledge, retrieves context, stores customer memory, and enforces retention and privacy policies.

### Developer Platform

Provides REST APIs, WebSocket APIs, SDKs, webhooks, API keys, docs, examples, and an API playground.

## Architectural Rules

- Domain logic should not depend on UI frameworks.
- Provider-specific code should live behind adapters.
- Runtime events should be structured and observable from the beginning.
- Public API contracts should be versioned.
- Secrets must never be exposed to the browser.
- Voice runtime must be isolated enough to scale independently from the dashboard.


## Architecture Decision Records

Major architectural decisions are tracked in [docs/adr](adr/README.md). Starting with Task 008, every major task should include an ADR when it introduces a durable platform decision.


## AI Intelligence Layer

The AI employee architecture blueprint is tracked in [AI Architecture Blueprint](../apps/api/docs/AI_ARCHITECTURE_BLUEPRINT.md). It defines the provider-agnostic orchestration, prompt, context, memory, tool, multi-agent, voice, observability, and security model for Tasks 012 onward.
