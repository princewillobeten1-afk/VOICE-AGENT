# Retrieval Context Assembly

Context assembly converts ranked chunks into a compact, citation-ready payload for downstream AI systems.

## Inputs

- Query
- Search mode
- Workspace and optional knowledge-base scope
- Metadata filters
- Hybrid weights
- Token budget
- Rerank flag
- Optional agent and conversation references

## Output

The `/retrieval/context` endpoint returns selected chunks, context text, citations, token usage, permission summary, and retrieval latency.

## Rules

Context assembly must never exceed the token budget. It should preserve citation ordering, omit low-value chunks when budget is exhausted, and expose omission reasons in future versions.

## Non-Goals

The assembly layer does not write final answers, call LLMs, execute tools, update conversation state, or decide business actions.
