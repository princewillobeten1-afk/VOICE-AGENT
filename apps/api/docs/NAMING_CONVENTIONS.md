# Naming Conventions

## Tables

- Use plural snake_case names: `agents`, `workflow_runs`, `api_keys`.
- Join tables use both entity names: `team_members`.
- Placeholder tables include the suffix only when intentionally non-final: `subscription_placeholders`.

## Columns

- Primary key: `id`.
- Foreign keys: `<entity>_id`.
- Tenant scope: `organization_id`.
- Workspace scope: `workspace_id`.
- Soft delete: `deleted_at`.
- Actor fields: `created_by_user_id`, `updated_by_user_id`.
- JSON payload columns: `metadata_json`, `settings`, `payload`, or explicit domain name.

## API

- Paths use kebab-case for URL segments only when needed.
- JSON fields use snake_case to match Python and database conventions.
- Event names use dot notation: `conversation.started`.

## Code

- Domain folders use singular conceptual names when appropriate: `workflow`, `storage`, `analytics`.
- SQLAlchemy models use PascalCase singular names.
- Pydantic schemas use suffixes such as `Create`, `Update`, `Out`, `Response`.