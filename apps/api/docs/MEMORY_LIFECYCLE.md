# Memory Lifecycle

```mermaid
flowchart LR
  A[Information Created] --> B[Memory Evaluation]
  B --> C[Importance Scoring]
  C --> D[Categorization]
  D --> E[Storage]
  E --> F[Indexing]
  F --> G[Retrieval]
  G --> H[Update]
  H --> I[Expiration]
  I --> J[Archive]
```

Task 015 stores metadata index state only. Embeddings and vector search are future integrations.

## Actions

- Create memory
- Update memory
- Merge memories
- Archive memory
- Restore memory
- Forget memory
- Delete memory
- Pin memory
- Link memories