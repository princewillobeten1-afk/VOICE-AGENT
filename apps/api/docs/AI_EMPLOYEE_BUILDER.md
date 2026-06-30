# AI Employee Builder Architecture

The builder is a guided 10-step workflow:

1. Identity
2. Personality
3. Instructions
4. Voice
5. Knowledge
6. Tools
7. Memory
8. Channels
9. Review
10. Publish

Each step maps to a versioned configuration area on `agent_versions`. Builder state and readiness checks live in `agent_configurations` so users can save progress without publishing.

## UX Principle

The experience should feel like hiring and training a real employee. Beginner users get a guided path. Advanced users can configure prompts, memory policy, tools, channels, and version history.

## Safety Principle

Publishing is separate from saving drafts. Real execution remains unavailable until future runtime systems are implemented.