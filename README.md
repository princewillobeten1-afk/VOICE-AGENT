# VoiceSense

VoiceSense is an AI Employee Platform for creating, managing, observing, and integrating AI employees across voice, chat, email, SMS, WhatsApp, scheduling, knowledge search, business tools, and workflow automation.

The goal is not to clone existing voice AI tools. The goal is to build the operating system for reliable AI employees: beautiful for operators, powerful for developers, and durable enough for enterprise use.

## Product Principles

- Premium UX: calm, fast, accessible, and thoughtfully designed.
- AI-native architecture: provider-agnostic, observable, configurable, and extensible.
- Developer-first platform: every dashboard capability should eventually be available through APIs.
- Enterprise-grade foundation: security, scalability, reliability, and maintainability from day one.
- Modular systems: each domain should evolve independently without creating a tangled product.

## Initial Repository Shape

- `apps/dashboard`: web app for customers, teams, and operators.
- `apps/api`: public and internal API surface.
- `apps/voice-gateway`: real-time voice session boundary.
- `packages/shared`: shared types, contracts, and utilities.
- `packages/ui`: reusable design system components.
- `packages/config`: shared linting, TypeScript, and app configuration.
- `infra`: deployment, environments, and infrastructure definitions.
- `docs`: architecture, product, and decision records.

## First Platform Slice

The first meaningful slice should prove the core product loop:

1. Create an AI employee.
2. Configure instructions, model provider, voice, and tools.
3. Test the employee in a simulated conversation.
4. Inspect logs, latency, transcript, tool calls, and outcomes.
5. Expose the same operations through an API contract.

## Project Operating Documents

- [Architecture](docs/architecture.md)
- [Product Foundation](docs/product-foundation.md)
- [Roadmap](docs/roadmap.md)
- [Required Skills and Expertise](docs/required-expertise.md)


## Release Candidate Quality

Task 028 adds product-wide polish and release-candidate readiness guidance.

- [Product Audit](docs/PRODUCT_AUDIT.md)
- [UX and Accessibility Audit](docs/UX_ACCESSIBILITY_AUDIT.md)
- [Performance Optimization](docs/PERFORMANCE_OPTIMIZATION.md)
- [Security and Reliability Review](docs/SECURITY_RELIABILITY_REVIEW.md)
- [Demo Workspace](docs/DEMO_WORKSPACE.md)
- [Production Readiness Checklist](docs/PRODUCTION_READINESS_CHECKLIST.md)
- [Final Release Candidate](docs/FINAL_RELEASE_CANDIDATE.md)
- [Quality Gates](docs/QUALITY_GATES.md)