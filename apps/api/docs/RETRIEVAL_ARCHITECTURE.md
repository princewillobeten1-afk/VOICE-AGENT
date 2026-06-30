# Retrieval Architecture

Task 016B introduces the Enterprise RAG and Intelligent Retrieval Engine for VoiceSense. The engine converts governed Knowledge Platform content into permission-aware chunks, indexes, search traces, and assembled context.

## Scope

The retrieval layer owns document chunk preparation, embedding provider abstraction, vector store abstraction, hybrid retrieval, reranking interfaces, context assembly, citation metadata, and retrieval observability.

It does not own LLM reasoning, response generation, conversation state, workflow execution, or tool calling.

## Pipeline

1. Knowledge documents are selected from approved workspace content.
2. Text is normalized and chunked by the configured strategy.
3. Chunks are stored with token counts, metadata, checksums, permission scope, and vector references.
4. Embedding jobs track indexing and reindexing activity.
5. Search requests apply tenant scope, workspace scope, optional knowledge-base filters, metadata filters, and permission mode.
6. Candidate chunks are scored using hybrid weights.
7. Optional reranking adjusts the final ordering.
8. Context assembly enforces token budgets and returns citations.
9. Search logs and retrieval requests preserve traceability.

## Modules

- `app/retrieval/models.py`: SQLAlchemy persistence models.
- `app/retrieval/providers.py`: embedding, vector store, and reranker interfaces.
- `app/retrieval/service.py`: indexing, scoring, search, and context assembly services.
- `app/retrieval/router.py`: REST API endpoints.
- `migrations/versions/0012_enterprise_retrieval_engine.sql`: database foundation.

## Security Boundary

Retrieval always begins from `organization_id` and `workspace_id`. Knowledge base, document, agent, and conversation filters narrow access further. Future document and team grants should be enforced before vector candidate expansion and again before context assembly.

## Provider Strategy

The local foundation uses placeholder embedding, metadata-only vector references, and heuristic reranking. Real providers are configured through provider configs and should be added as adapters behind the existing interfaces.
