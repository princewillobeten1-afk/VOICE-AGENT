# AI Team Management Guide

AI teams model the way businesses organize work. Teams can represent departments, specialist pods, supervisor groups, or workflow-specific task forces.

## Team Features

- Nested teams through `parent_team_id`.
- Supervisor AI through `supervisor_agent_id`.
- Member assignment through `ai_team_members`.
- Responsibilities as structured text arrays.
- Routing policy and collaboration rules as JSON configuration.
- Department and status fields for filtering.

## Member Types

Supported membership types include member, supervisor, specialist, assistant, manager, and custom values.
