# ADR-023: Enterprise Security, Administration, Compliance, and Governance Platform

## Status

Accepted

## Context

VoiceSense must support enterprise tenants that need centralized identity administration, RBAC, ABAC, SSO, MFA, audit logs, secrets management, compliance readiness, data governance, encryption metadata, risk monitoring, and AI-specific governance. These capabilities must apply across AI employees, workflows, tools, knowledge, memory, integrations, billing, telephony, omnichannel, and developer APIs.

## Decision

Create a dedicated `app/security` module that extends the identity foundation with enterprise governance records and APIs. The module stores organization-scoped and workspace-scoped policy, access, SSO, secret, compliance, data-governance, encryption, risk, health, and governance graph data.

The platform will keep authentication and base membership in `app/identity`, while security owns enterprise policy and governance concerns. Secrets are stored as references, not plaintext. Compliance records are readiness artifacts, not certification claims.

## Consequences

- Future product areas can attach to a shared security policy model.
- Enterprise readiness improves without hard-coding individual customer controls.
- ABAC evaluation, SCIM provisioning, SIEM export, live MFA challenges, HSM/KMS integrations, and formal compliance automation remain future runtime layers.
- The governance graph can evolve into a cross-platform security analytics surface without changing the foundational schema.

## Alternatives Considered

- Embed security fields inside every feature module. Rejected because it would fragment authorization and compliance behavior.
- Use only built-in RBAC. Rejected because enterprise customers need contextual policies and data governance.
- Build live SSO/SCIM/MFA providers immediately. Deferred to keep Task 026 focused on durable platform contracts rather than provider-specific runtime behavior.