# RBAC Guide

RBAC remains the first authorization gate in VoiceSense.

## Principles

- Keep built-in roles stable for product defaults.
- Use custom roles for enterprise-specific bundles.
- Evaluate RBAC before ABAC for predictable denial behavior.
- Audit role and permission changes.

## Built-In Direction

Owner, Admin, Manager, Developer, Member, and Billing roles remain the baseline. Task 026 adds `custom_roles`, `user_groups`, and `admin_departments` so enterprise tenants can model internal administration without code changes.