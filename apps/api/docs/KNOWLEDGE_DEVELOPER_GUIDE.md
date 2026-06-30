# Knowledge Developer Guide

Future integrations should create data sources and sync jobs rather than writing directly into retrieval systems.

## Connector Flow

1. Register source.
2. Queue sync job.
3. Validate file or metadata.
4. Create or update documents.
5. Create document versions.
6. Record activity and quality checks.

## RAG Integration

The future RAG engine should consume published documents and version metadata from this platform. It should not own knowledge governance.