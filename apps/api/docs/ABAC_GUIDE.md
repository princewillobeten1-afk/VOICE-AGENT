# ABAC Guide

ABAC policies supplement RBAC when authorization depends on resource attributes or runtime context.

## Policy Shape

ABAC policies include effect, resource type, action, conditions, priority, status, organization, and optional workspace.

## Evaluation Order

1. Confirm authenticated organization membership.
2. Check RBAC permission for the broad action.
3. Evaluate active ABAC policies by priority.
4. Apply governance policy enforcement mode.
5. Emit audit and risk events when denied or elevated.

The Task 026 implementation stores ABAC policies and exposes management APIs. A full policy evaluation engine is intentionally future work.