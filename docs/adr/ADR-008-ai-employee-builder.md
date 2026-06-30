# ADR-008: AI Employee Builder

## Status

Accepted

## Date

2026-06-27

## Related Task

Task 012 - AI Employee Builder

## Context

VoiceSense needs a flagship experience for creating AI employees. The builder must be simple enough for beginners while supporting advanced configuration for prompts, voice, knowledge, tools, memory, channels, versioning, templates, testing, and publishing.

Task 011 defined the AI Intelligence Layer. Task 012 turns that architecture into a product and API foundation without implementing runtime AI, voice, RAG, tool execution, or workflow execution.

## Decision

VoiceSense will model AI employees as `agents` with versioned operating configuration in `agent_versions`. Builder progress, readiness checks, and playground state live in `agent_configurations`. Reusable starting points live in `agent_templates`. Publishing and lifecycle actions are tracked in `agent_publishing_history`.

The frontend will provide an AI Employees dashboard, guided 10-step builder, management profile, and safe playground. All runtime behavior remains placeholder-only until future tasks implement the actual AI orchestrator and provider layer.

## Rationale

Separating identity from versioned configuration allows teams to draft safely, publish deliberately, and audit changes over time. It also aligns with the Task 011 architecture: prompts, context, memory, voice, tools, workflows, channels, and collaboration are explicit configuration domains rather than hardcoded behavior.

## Alternatives Considered

- Store the entire employee as one JSON blob: faster, but weak for versioning, validation, and auditability.
- Build runtime AI testing immediately: attractive, but violates the constraint and would bypass provider/orchestrator architecture.
- Make templates only frontend mock data: simpler, but backend template records are needed for reusable creation flows.

## Consequences

### Positive

- Users get a premium guided creation experience.
- Backend supports create, update, delete, publish, duplicate, templates, versions, and builder state.
- Future runtime tasks can consume versioned configuration cleanly.
- Publishing history creates an audit trail for lifecycle changes.

### Negative

- Playground behavior is placeholder-only until runtime AI arrives.
- Version rollback is architecture-ready but not deeply implemented.
- Builder validation is UI/foundation-level until policy engines are built.

### Follow-Up Work

- Implement real prompt validation and evaluation suites.
- Add rollback API and export endpoint.
- Connect builder state to real form persistence.
- Implement runtime playground through AI Orchestrator.
- Add permission separation for draft editing and publishing.

## Related Documents

- `apps/api/docs/AI_EMPLOYEE_LIFECYCLE.md`
- `apps/api/docs/AI_EMPLOYEE_BUILDER.md`
- `apps/api/docs/AI_EMPLOYEE_CONFIGURATION_GUIDE.md`
- `apps/api/docs/AI_EMPLOYEE_TEMPLATES.md`
- `apps/api/docs/AI_EMPLOYEE_VERSIONING.md`
- `apps/api/docs/AI_EMPLOYEE_API.md`
- `apps/api/migrations/versions/0007_ai_employee_builder.sql`