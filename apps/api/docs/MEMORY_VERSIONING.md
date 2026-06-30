# Memory Versioning Guide

Every created or updated memory receives a `memory_versions` record.

Tracked fields include:

- Version number
- Title
- Content
- Summary
- Change type
- Change summary
- Evaluation snapshot
- Actor and timestamp

Rollback is architecture-ready through version history, but a dedicated rollback endpoint is reserved for a future task.