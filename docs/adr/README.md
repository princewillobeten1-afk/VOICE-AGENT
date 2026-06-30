# Architecture Decision Records

This directory contains Architecture Decision Records for VoiceSense.

ADRs capture major technical and product architecture decisions so future work can understand not only what was built, but why the decision was made, which alternatives were considered, and what trade-offs were accepted.

## ADR Policy

Starting with Task 008, every major platform task must include at least one ADR when it introduces or materially changes:

- System architecture
- Data model design
- Provider abstractions
- Security boundaries
- Multi-tenant behavior
- Infrastructure strategy
- API contracts
- Developer experience foundations
- Long-term product platform decisions

## Records

| ADR | Title | Status | Related Task |
| --- | --- | --- | --- |
| [ADR-004](ADR-004-storage-provider-abstraction.md) | Storage Provider Abstraction | Accepted | Task 008 - Storage & Asset Management System |
| [ADR-005](ADR-005-event-driven-notification-system.md) | Event-Driven Notification System | Accepted | Task 009 - Notification & Event System |
| [ADR-006](ADR-006-universal-integration-framework.md) | Universal Integration Framework | Accepted | Task 010 - Universal Integration Framework |
| [ADR-007](ADR-007-ai-intelligence-layer-blueprint.md) | AI Intelligence Layer Blueprint | Accepted | Task 011 - AI Architecture Blueprint |
| [ADR-008](ADR-008-ai-employee-builder.md) | AI Employee Builder | Accepted | Task 012 - AI Employee Builder |
| [ADR-009](ADR-009-real-time-voice-engine.md) | Real-Time Voice Engine | Accepted | Task 013 - Real-Time Voice Engine |
| [ADR-010](ADR-010-universal-conversation-engine.md) | Universal Conversation Engine | Accepted | Task 014 - Universal Conversation Engine |
| [ADR-011](ADR-011-advanced-memory-system.md) | Advanced Memory System | Accepted | Task 015 - Advanced Memory System |
| [ADR-012](ADR-012-enterprise-knowledge-management-platform.md) | Enterprise Knowledge Management Platform | Accepted | Task 016A - Enterprise Knowledge Management Platform |
| [ADR-013](ADR-013-enterprise-rag-retrieval-engine.md) | Enterprise RAG Retrieval Engine | Accepted | Task 016B - Enterprise RAG & Intelligent Retrieval Engine |
| [ADR-014](ADR-014-enterprise-visual-workflow-engine.md) | Enterprise Visual Workflow Automation Engine | Accepted | Task 017 - Enterprise Visual Workflow Automation Engine |
| [ADR-015](ADR-015-universal-tool-calling-mcp-framework.md) | Universal Tool Calling and MCP Framework | Accepted | Task 018 - Universal Tool Calling & MCP Framework |
| [ADR-016](ADR-016-multi-agent-collaboration-engine.md) | Multi-Agent Collaboration Engine | Accepted | Task 019 - Multi-Agent Collaboration Engine |
| [ADR-017](ADR-017-aiops-observability-analytics-platform.md) | AI Operations Center Observability and Analytics Platform | Accepted | Task 020 - AI Operations Center (AIOps), Observability & Analytics Platform |
| [ADR-018](ADR-018-enterprise-telephony-infrastructure.md) | Enterprise Telephony Infrastructure | Accepted | Task 021 - Enterprise Telephony Infrastructure |
| [ADR-019](ADR-019-omnichannel-communication-platform.md) | Omnichannel Communication Platform | Accepted | Task 022 - Omnichannel Communication Platform |
| [ADR-020](ADR-020-enterprise-integration-platform-marketplace.md) | Enterprise Integration Platform and Connector Marketplace | Accepted | Task 023 - Enterprise Integration Platform & Connector Marketplace |
| [ADR-021](ADR-021-enterprise-developer-platform.md) | Enterprise Developer Platform | Accepted | Task 024 - Enterprise Developer Platform |
| [ADR-022](ADR-022-enterprise-billing-platform.md) | Enterprise Billing, Usage Metering, and Subscription Platform | Accepted | Task 025 - Enterprise Billing, Usage Metering & Subscription Platform |
| [ADR-023](ADR-023-enterprise-security-governance-platform.md) | Enterprise Security, Administration, Compliance, and Governance Platform | Accepted | Task 026 - Enterprise Security, Administration, Compliance & Governance Platform |
| [ADR-024](ADR-024-ai-studio-platform.md) | VoiceSense AI Studio Platform | Accepted | Task 027 - VoiceSense AI Studio |
| [ADR-025](ADR-025-release-candidate-quality-strategy.md) | Release-Candidate Quality Strategy | Accepted | Task 028 - Final Product Polish & Production Readiness |
| [ADR-026](ADR-026-live-data-integration-layer.md) | Live Data Integration Layer | Accepted | Live Data Integration Layer |

## Numbering

ADR numbering follows long-lived architectural decisions, not only task numbers. Earlier foundational decisions can be documented retroactively when needed. New major tasks should continue from the latest ADR number unless a task requires multiple related ADRs.
