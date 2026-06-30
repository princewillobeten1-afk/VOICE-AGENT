# Identity and Access Guide

VoiceSense uses identity records for authentication and membership, then layers enterprise access governance through Task 026 security models.

## Access Layers

1. Organization membership defines tenant access.
2. Role assignments provide coarse RBAC permissions.
3. Custom roles add organization-specific permission bundles.
4. ABAC policies evaluate resource, action, subject, and context attributes.
5. Governance policies set organization or workspace enforcement behavior.

## Administration

Administrators should manage users, groups, departments, policies, sessions, SSO connections, MFA factors, trusted devices, and audit review from the Security workspace.