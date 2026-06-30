# Memory Retrieval Strategy

The initial retrieval engine is provider-neutral.

## Ranking Inputs

- Text match against title, content, summary, and tags.
- Importance score.
- Confidence score.
- Recency score.
- Pinned state.
- Category and memory type filters.
- User, agent, and visibility filters.

## Future Expansion

A future RAG/vector task can add embedding generation and vector similarity behind the same `/v1/memory/search` contract. The current `index_state` field is intentionally ready for that provider state.