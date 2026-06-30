# Retrieval Chunking Guide

Chunking turns long documents into reusable retrieval units. VoiceSense stores every chunk with source document, index, language, strategy, metadata, checksum, token estimate, and embedding state.

## Strategies

- `paragraph_aware`: preserves paragraph boundaries when content has clear breaks.
- `section_aware`: intended for headings, chapters, policies, and product docs.
- `semantic`: reserved for future semantic boundary detection.
- `fixed_window`: uses configured character windows and overlap.

## Defaults

- Chunk size: `900`
- Overlap: `120`
- Language: stored per chunk for future language-aware retrieval.
- Token count: approximate in this foundation, provider-specific later.

## Guidance

Use smaller chunks for FAQs, policy exceptions, and high-precision support answers. Use larger chunks for long procedural context where losing surrounding steps would reduce answer quality. Overlap should be high enough to preserve continuity but low enough to avoid duplicate citations.

## Reindexing

Reindexing creates an `embedding_jobs` record and new chunk records. Production workers should deduplicate by checksum and replace stale chunk sets atomically.
