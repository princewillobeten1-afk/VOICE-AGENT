# ADR-012: Enterprise Knowledge Management Platform

## Status

Accepted

## Date

2026-06-28

## Related Task

Task 016A - Enterprise Knowledge Management Platform

## Context

VoiceSense needs a governed content management platform for knowledge assets before building RAG. Organizations must be able to upload, organize, version, secure, synchronize, and maintain knowledge that AI employees will later consume.

## Decision

VoiceSense will expand the existing knowledge base, data source, and document tables into a full Knowledge Management Platform. The platform will model knowledge bases, categories, folders, collections, tags, website sources, document versions, permissions, sync jobs, activity logs, and quality checks.

The platform intentionally excludes embeddings, vector databases, semantic search, crawling execution, RAG retrieval, and AI reasoning.

## Rationale

RAG quality depends on governed, fresh, well-permissioned source content. Building retrieval before content management would create brittle pipelines and weak enterprise controls.

## Alternatives Considered

- Build RAG first: faster demo value, but poor governance foundation.
- Store all knowledge as files only: too weak for websites, external sources, permissions, versions, and freshness.
- Build separate CMS per source type: creates inconsistent governance and UX.

## Consequences

### Positive

- Organizations can manage knowledge assets independently of AI retrieval.
- Versioning, permissions, sync jobs, activity, and quality checks are first-class.
- Future RAG can consume clean published documents.

### Negative

- No semantic search or embeddings yet.
- Website crawling and connector execution are queued only.
- Rollback is modeled but not exposed as a dedicated endpoint yet.

## Follow-Up Work

- Implement connector sync workers.
- Implement website crawler.
- Add rollback endpoint.
- Add RAG ingestion pipeline for published documents.
- Add deeper quality dashboards.

## Related Documents

- `apps/api/docs/KNOWLEDGE_ARCHITECTURE.md`
- `apps/api/docs/KNOWLEDGE_CONTENT_LIFECYCLE.md`
- `apps/api/docs/KNOWLEDGE_VERSION_MANAGEMENT.md`
- `apps/api/docs/KNOWLEDGE_PERMISSION_MODEL.md`
- `apps/api/docs/KNOWLEDGE_SYNC_ARCHITECTURE.md`
- `apps/api/docs/KNOWLEDGE_API.md`
- `apps/api/docs/KNOWLEDGE_DEVELOPER_GUIDE.md`
- `apps/api/migrations/versions/0011_enterprise_knowledge_management.sql`