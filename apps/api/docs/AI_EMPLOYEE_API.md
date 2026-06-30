# AI Employee API

Base path: `/v1/ai-employees`

## Employees

- `GET /ai-employees?workspace_id=` lists employees.
- `POST /ai-employees` creates an employee and initial draft version.
- `GET /ai-employees/{agent_id}` retrieves detail with versions and publishing history.
- `PATCH /ai-employees/{agent_id}` updates identity/configuration metadata.
- `DELETE /ai-employees/{agent_id}` soft deletes an employee.

## Versions

- `GET /ai-employees/{agent_id}/versions` lists versions.
- `POST /ai-employees/{agent_id}/versions` creates a new draft version.
- `POST /ai-employees/{agent_id}/publish` publishes the current version.

## Management

- `POST /ai-employees/{agent_id}/archive` archives an employee.
- `POST /ai-employees/{agent_id}/duplicate` duplicates an employee into a new draft.
- `PUT /ai-employees/{agent_id}/builder-state` saves builder progress.
- `POST /ai-employees/{agent_id}/playground` returns a placeholder test result.
- `GET /ai-employees/templates` lists reusable templates.