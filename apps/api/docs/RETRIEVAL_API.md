# Retrieval API

All retrieval endpoints are mounted under `/v1/retrieval` and require authenticated organization access.

## Provider Catalog

`GET /retrieval/providers`

Returns supported provider families and future adapter names.

## Provider Configs

`POST /retrieval/provider-configs`

Creates a workspace-scoped embedding, vector store, or reranker config. Store secrets by reference only.

## Settings

`GET /retrieval/settings?workspace_id={id}`

`POST /retrieval/settings`

Manages chunking, provider references, hybrid weights, token budget, permission mode, and cache policy.

## Indexes

`GET /retrieval/indexes?workspace_id={id}`

`POST /retrieval/indexes`

Creates and lists retrieval indexes for a workspace.

## Indexing

`POST /retrieval/index-content`

`POST /retrieval/reindex`

Creates completed placeholder embedding jobs in this foundation. Production deployments should move heavy indexing into background workers.

## Chunks

`GET /retrieval/chunks?workspace_id={id}`

Lists recent chunks with optional knowledge-base and document filters.

## Search and Context

`POST /retrieval/search`

Returns ranked chunk results.

`POST /retrieval/context`

Returns assembled context, citations, selected chunks, permission summary, and latency.

## Metrics

`GET /retrieval/metrics?workspace_id={id}`

Returns index, chunk, job, request, latency, provider catalog, and observability placeholders.
