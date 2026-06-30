# ADR-004: Storage Provider Abstraction

## Status

Accepted

## Date

2026-06-27

## Related Task

Task 008 - Storage & Asset Management System

## Context

VoiceSense needs a durable asset management foundation for documents, PDFs, images, audio files, call recordings, archives, reports, and future platform artifacts.

The platform is being designed as a multi-tenant SaaS product that must support startups, agencies, and enterprise organizations. Storage must therefore be portable across deployment environments and cloud providers, while keeping file metadata, ownership, permissions, auditability, and lifecycle operations consistent inside the VoiceSense application layer.

Task 008 explicitly excludes AI indexing, RAG ingestion, transcription, malware scanning implementation, and file processing. The immediate goal is to establish the storage foundation without coupling future AI systems to provider-specific storage code.

## Decision

VoiceSense will use a provider abstraction for storage operations.

Application services will depend on a `StorageProviderAdapter` interface instead of directly calling cloud SDKs or local filesystem APIs. The adapter owns provider-specific upload URL creation, download URL creation, object key handling, and object deletion.

The first implementation supports local development storage. Placeholder adapters exist for future providers such as Amazon S3, Cloudflare R2, Google Cloud Storage, and Azure Blob Storage so the API boundary is stable before provider credentials and infrastructure are finalized.

Storage metadata remains in PostgreSQL through normalized tables for providers, folders, files, file versions, upload sessions, tags, and tag assignments. Object bytes live in the selected storage provider.

## Rationale

A provider abstraction gives VoiceSense portability without weakening the product model. The dashboard, APIs, audit logs, RBAC checks, and metadata lifecycle can stay consistent regardless of where bytes are stored.

This is important for VoiceSense because enterprise customers may require different storage backends, regions, retention policies, or cloud environments. It also keeps local development simple while preserving a path to production-grade object storage.

Separating metadata from object bytes also keeps the database efficient and queryable. PostgreSQL remains the system of record for ownership, hierarchy, lifecycle state, tags, versions, and audit relationships, while storage providers handle binary durability and transfer performance.

## Alternatives Considered

- Store files directly in PostgreSQL: simpler operationally at first, but unsuitable for large audio, archives, recordings, and future enterprise-scale file workloads.
- Hard-code a single cloud provider such as S3: faster initial cloud implementation, but creates vendor lock-in and makes enterprise/regional deployment harder.
- Let the frontend upload directly to a fixed bucket without API-managed upload sessions: low backend complexity, but weaker auditability, policy enforcement, lifecycle tracking, and multi-tenant safety.
- Implement all cloud providers immediately: attractive for completeness, but premature before infrastructure, secrets management, and deployment targets are finalized.

## Consequences

### Positive

- Storage operations are provider-agnostic at the application layer.
- Local development remains lightweight.
- Future cloud providers can be added behind a stable interface.
- File metadata, hierarchy, lifecycle state, and audit events remain consistent across providers.
- Upload sessions create a clear control point for validation, expiration, resumability, and future policy enforcement.

### Negative

- The abstraction adds implementation overhead compared with direct SDK calls.
- Provider-specific features must be normalized or exposed carefully to avoid leaking vendor concepts into product code.
- Placeholder cloud adapters must be replaced before production cloud storage is available.
- Copy and preview behavior may need provider-specific implementations later.

### Follow-Up Work

- Implement production S3 and Cloudflare R2 adapters.
- Add provider credential loading through a secret manager instead of database-stored secrets.
- Add signed URL expiration policies per organization or environment.
- Add upload retry and resumable upload coordination in the dashboard.
- Add retention policies, storage quotas, and provider health checks.
- Add malware scanning and content policy hooks as separate future decisions.

## Related Documents

- `apps/api/docs/STORAGE_ASSET_MANAGEMENT.md`
- `apps/api/docs/STORAGE_API.md`
- `apps/dashboard/docs/FILE_MANAGER.md`
- `apps/api/migrations/versions/0004_storage_asset_management.sql`
- `apps/api/app/storage/providers.py`
- `apps/api/app/storage/router.py`