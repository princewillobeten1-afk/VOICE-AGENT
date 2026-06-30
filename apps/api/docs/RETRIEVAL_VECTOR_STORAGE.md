# Retrieval Vector Storage

Vector storage is abstracted so VoiceSense can support multiple deployment profiles without rewriting product logic.

## Future Stores

- pgvector for PostgreSQL-native deployments.
- Pinecone for managed vector infrastructure.
- Weaviate and Qdrant for hybrid and metadata-rich search.
- Milvus and Chroma for specialized or self-hosted use cases.
- Elasticsearch or OpenSearch for keyword and hybrid retrieval.

## Current Foundation

Task 016B uses metadata-only vector references. This lets APIs, dashboards, migrations, and observability mature before introducing vendor-specific vector infrastructure.

## Adapter Responsibilities

Adapters should upsert chunks, delete stale vectors, search by vector and metadata filters, return scores, preserve source ids, and expose health checks. Permission filters must be pushed down when the provider supports it and rechecked in application code.
