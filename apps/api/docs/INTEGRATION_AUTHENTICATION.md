# Integration Authentication and Credentials

Task 010 creates the credential lifecycle model without integrating provider-specific OAuth or secret-manager clients.

## Supported Auth Methods

The framework is prepared for:

- OAuth 2.0
- OAuth PKCE
- API keys
- Bearer tokens
- Basic authentication
- JWT
- Custom headers

## Credential Storage Boundary

VoiceSense does not store raw provider secrets in application tables. `integration_credentials` stores:

- `secret_ref`: pointer to a future secret manager or KMS-backed vault.
- `secret_fingerprint`: one-way fingerprint for validation and rotation comparison.
- `secret_provider`: provider name for the secret backend.
- `rotation_version`, `expires_at`, `last_rotated_at`, and `status`.

This avoids normalizing insecure local secret storage into the platform architecture.

## Rotation Lifecycle

1. User submits replacement credentials.
2. API stores a new `secret_ref` and fingerprint.
3. Existing active credentials are marked rotated.
4. `integration.credentials.rotated` event is emitted.
5. Health check validates connection readiness.