# Multi-Agent API

All endpoints are mounted under `/v1/collaboration`.

## Teams

`GET /collaboration/teams?workspace_id={id}` lists AI teams.

`POST /collaboration/teams` creates an AI team.

`POST /collaboration/teams/{team_id}/members` assigns an AI employee to a team.

`GET /collaboration/teams/{team_id}/members` lists team members.

## Policies

`POST /collaboration/policies` creates a collaboration policy.

## Delegation and Sessions

`POST /collaboration/delegate` creates or reuses a collaboration session and assigns a task.

`GET /collaboration/sessions?workspace_id={id}` lists collaboration sessions.

`GET /collaboration/sessions/{session_id}/timeline` returns session logs.

## Analytics

`GET /collaboration/analytics?workspace_id={id}` returns team, member, session, delegation, and routing summary metrics.
