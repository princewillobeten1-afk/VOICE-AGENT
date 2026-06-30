# ADR-013: Enterprise RAG Retrieval Engine

## Status

Accepted

## Context

VoiceSense needs a retrieval foundation that can turn governed enterprise knowledge into fast, permission-aware context for AI employees. The system must support future embedding providers, vector stores, rerankers, search modes, observability, and enterprise security requirements without locking the platform into one vendor.

Task 016B follows the Knowledge Management Platform from Task 016A. Knowledge owns content governance. Retrieval owns chunking, indexing metadata, candidate search, reranking interfaces, context assembly, citations, and analytics.

## Decision

VoiceSense will implement retrieval as a modular platform layer with:

- Workspace-scoped provider configs for embeddings, vector stores, and rerankers.
- Retrieval settings per workspace or knowledge base.
- Retrieval indexes and chunks stored in PostgreSQL metadata tables.
- Embedding jobs to track indexing and reindexing operations.
- Retrieval requests and search logs for traceability.
- Retrieval metrics for future analytics and cost monitoring.
- Provider interfaces for embeddings, vector storage, and reranking.
- Placeholder providers in local development until production adapters are added.

The initial implementation stores vector references rather than raw vectors. Real vector storage will be added behind adapters.

## Consequences

This keeps product APIs, dashboard surfaces, database relationships, and observability stable while allowing provider choices to evolve. It also avoids premature vector infrastructure coupling.

The trade-off is that early retrieval quality is intentionally limited. The foundation produces metadata-aware placeholder search and context assembly, but production semantic quality requires real embedding, vector, and reranking adapters.

## Alternatives Considered

- Direct pgvector-first implementation: faster to make semantic search real, but creates an early storage assumption.
- Managed vector provider first: strong scale path, but introduces vendor lock-in too early.
- Embed retrieval inside conversation runtime: simpler short term, but mixes knowledge retrieval with reasoning and conversation state.

## Follow-Ups

- Add production embedding adapters.
- Add pgvector and managed vector-store adapters.
- Move indexing into background workers.
- Enforce document/team permissions before vector expansion and before context assembly.
- Add retrieval evaluation datasets and quality scoring.
