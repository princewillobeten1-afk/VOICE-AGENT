# Developer Platform Foundation

VoiceSense is API-first. The developer platform provides secure access to APIs, credential management, webhooks, logs, usage analytics, SDK foundations, and documentation structure.

## Backend Structure

```text
app/developer/
  models.py
  schemas.py
  router.py
  README.md
```

Developer APIs are mounted under:

```text
/v1/developer
```

## Database Objects

- `api_keys`: workspace-scoped machine credentials. Secrets are generated once and stored as hashes.
- `personal_access_tokens`: user-scoped tokens for developer workflows.
- `oauth_applications`: future OAuth application registry.
- `webhook_endpoints`: configured outbound webhook endpoints.
- `webhook_deliveries`: delivery attempts and retry records.
- `api_request_logs`: request viewer foundation.
- `api_usage_buckets`: analytics and rate-limit reporting foundation.
- `sdk_metadata`: official SDK registry and release metadata.
- `developer_settings`: per-workspace developer defaults.

## API Key Lifecycle

1. Create key with name, workspace, environment, scopes, and optional expiration.
2. Return secret once in the create response.
3. Store only `key_hash` and `key_prefix`.
4. Allow rename without changing secret.
5. Allow regenerate, returning the new secret once.
6. Allow revoke by setting `revoked_at`.
7. Log each mutation to audit logs.

## Webhook Lifecycle

1. Create endpoint with URL, events, environment, and retry policy.
2. Return signing secret once.
3. Store only a secret hash/reference.
4. Record delivery attempts in `webhook_deliveries`.
5. Support retries through policy metadata.
6. Delete via soft delete.

## Security Model

- Never expose stored secrets.
- Hash API keys, PATs, webhook secrets, and OAuth client secrets.
- Scope credentials by organization and workspace.
- Enforce RBAC permissions for developer operations.
- Track credential changes through audit logs.
- Keep API logs free of raw authorization headers and secrets.

## SDK Strategy

Official SDKs should share generated types and consistent behavior:

- TypeScript / Node.js
- Python
- Go
- Java
- PHP

SDKs should support retries, request IDs, typed errors, pagination helpers, webhook signature verification, and environment-aware configuration.