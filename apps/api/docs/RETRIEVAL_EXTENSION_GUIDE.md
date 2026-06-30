# Retrieval Developer Extension Guide

Use this guide when adding production retrieval providers or improving ranking quality.

## Add an Embedding Provider

1. Implement `EmbeddingProvider` in `app/retrieval/providers.py` or a provider-specific module.
2. Read credentials through `secret_ref`, never raw config values.
3. Return model, dimensions, token count, and vector reference.
4. Add health checks and capability metadata.

## Add a Vector Store

1. Implement `VectorStoreProvider`.
2. Support metadata filters for organization, workspace, knowledge base, document, language, and access scope.
3. Return stable chunk ids and scores.
4. Recheck permissions in application code before context assembly.

## Add Reranking

1. Implement `RerankerProvider`.
2. Keep input payloads small and avoid sending unauthorized text to third-party providers.
3. Return chunk ids, scores, and reasons for traceability.

## Testing Expectations

Provider adapters should include unit tests for config validation, retry behavior, timeout handling, filter translation, and degraded-provider fallback.
