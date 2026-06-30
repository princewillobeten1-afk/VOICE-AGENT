# VoiceSense Quality Gates

## Required Per Major Task

- ADR for architectural decisions.
- Database schema and ERD updates when models change.
- API docs when endpoints change.
- Dashboard build verification when UI changes.
- API compile/OpenAPI verification when backend changes.
- Migration verification when SQL changes.

## Release Candidate Gates

- `npm run check:dashboard`
- `npm run check:api`
- Migration runner completes.
- Product audit reviewed.
- Accessibility and production checklists reviewed.