# Security API

All endpoints are mounted under `/api/security` and require organization-scoped authentication.

## Endpoints

- `POST /security/policies`
- `GET /security/policies`
- `POST /security/abac-policies`
- `GET /security/abac-policies`
- `POST /security/sso`
- `GET /security/sso`
- `POST /security/secrets`
- `GET /security/secrets`
- `POST /security/compliance/frameworks`
- `GET /security/compliance/frameworks`
- `POST /security/data-governance`
- `POST /security/risk-events`
- `GET /security/risk-events`
- `GET /security/sessions`
- `GET /security/audit`
- `GET /security/governance-graph`
- `GET /security/analytics`

## Notes

The APIs store governance records and expose administrative views. Live SSO provisioning, SCIM, MFA challenge flows, SIEM export, HSM operations, and certification automation are future implementation layers.