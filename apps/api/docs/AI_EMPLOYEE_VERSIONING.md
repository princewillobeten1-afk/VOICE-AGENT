# AI Employee Versioning

AI employees are versioned so teams can safely draft, review, publish, roll back, and audit changes.

## Version Rules

- Every new employee receives an initial draft version.
- Publishing marks the current version as published.
- Historical versions remain available for review and future rollback.
- Publishing actions are recorded in `agent_publishing_history`.

## Future Rollback

Rollback should create a new draft from an older version rather than mutating historical records.