# Conversation Context Management Guide

Context snapshots prepare the future model context window without implementing RAG or memory persistence.

Sources can include:

- Current conversation
- Previous messages
- Memory hooks
- Knowledge hooks
- Workflow state
- Integration data
- User profile
- Organization context

Each snapshot records prioritized context, omitted context, token budget, and model limits.