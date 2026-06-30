# Audit Guide

VoiceSense auditability starts with identity audit logs and expands through security risk events.

## Captured Events

Security APIs emit audit events for major policy creation. Future updates should audit role changes, SSO changes, MFA enrollment, session revocation, secret rotation, compliance evidence changes, and data-governance changes.

## Retention

Retention is controlled through data governance policies. Export, archival, and external SIEM delivery are future integrations.