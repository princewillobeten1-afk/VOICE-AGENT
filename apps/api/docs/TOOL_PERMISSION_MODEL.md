# Tool Permission Model

Tool permission checks combine platform RBAC with tool-specific allow and deny rules.

## Principles

- Organization and workspace scope are always enforced.
- Deny rules override allow rules.
- If no tool-specific rule exists, the runtime falls back to organization RBAC.
- Secret values are never returned; tools reference credentials through `secret_ref` or connected accounts.

Tool permissions can target users, teams, roles, AI employees, workflows, or future service accounts.
