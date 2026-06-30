# Security Architecture

Task 026 establishes the VoiceSense enterprise security, administration, compliance, and governance foundation. It does not implement live IdP provisioning, formal certifications, HSM-backed key custody, or SOC/SIEM integrations.

## Architecture

The `app/security` module owns governance policy records, ABAC rules, SSO connection metadata, MFA/trusted-device state, secret references, compliance readiness, data governance, encryption-key references, risk events, health scoring, and governance graph snapshots.

Authentication and base membership remain in `app/identity`. Security extends that foundation instead of replacing it.

## Boundaries

- Identity: users, organizations, teams, memberships, sessions, roles, invitations, audit logs.
- Security: enterprise policy, ABAC, SSO configuration, MFA factors, trusted devices, secrets, compliance, data governance, encryption key records, risk events.
- Audit: user-visible security events are queried from identity audit logs and future audit/security event stores.

## Multi-Tenant Rules

Every security record is organization-scoped. Workspace-scoped records are used where policy, secret, data governance, or risk scope may vary by workspace.

## Future Runtime Services

Future workers can evaluate ABAC rules, rotate secrets, collect compliance evidence, publish SIEM events, and build governance graph snapshots without changing the API contracts introduced here.