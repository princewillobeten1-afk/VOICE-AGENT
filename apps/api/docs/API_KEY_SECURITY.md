# API Key Security

API keys are high-risk credentials and must be handled with strict rules.

## Rules

- Generate keys with cryptographically secure randomness.
- Show secrets only once.
- Store only SHA-256 hashes and short prefixes.
- Scope every key by organization and workspace.
- Require explicit scopes.
- Support expiration and revocation.
- Track last-used metadata.
- Audit create, rename, regenerate, and revoke events.

## Prefixes

Use readable prefixes for environment identification:

- `vsk_dev_...`
- `vsk_prod_...`

The prefix is not secret and may be shown in logs and UI.