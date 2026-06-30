# ADR-021: Enterprise Developer Platform

## Status

Accepted

## Context

VoiceSense needs a world-class developer ecosystem, not just individual API endpoints. Developers need API keys, OAuth applications, SDKs, CLI, webhooks, OpenAPI, API explorer, sandbox resources, request analytics, rate limiting, versioning, and documentation that stays aligned with the product.

## Decision

We will extend the existing Developer Platform module with API version records, OAuth token records, rate-limit policies, sandbox resources, API explorer runs, SDK release records, and CLI release records. API keys and webhook endpoints remain shared platform primitives already modeled through integrations/developer modules.

The platform will treat OpenAPI as the source for API explorer execution, SDK generation, code samples, and documentation synchronization. Production package publishing and third-party SDK maintenance pipelines are deferred.

## Consequences

- Developers get one portal for authentication, exploration, SDKs, CLI, sandbox, webhooks, analytics, and versions.
- Enterprise customers can reason about rate limits, API health, request timelines, and migration windows.
- Future AI-powered API assistant features have durable request, endpoint, and code-sample context.
- Public package publishing and marketplace billing remain outside this task.

## Alternatives Considered

- Keep developer tooling as static documentation only. Rejected because enterprise developers need executable explorer, credentials, sandbox, analytics, and lifecycle records.
- Build SDKs manually first. Rejected because SDK consistency should be driven by OpenAPI and generated contracts.