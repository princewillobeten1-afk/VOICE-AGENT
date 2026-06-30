# Authentication and Identity API

Base path: `/v1`

All responses use JSON. Protected endpoints require `Authorization: Bearer <access_token>`.

## Authentication

- `POST /auth/signup`
- `POST /auth/signin`
- `POST /auth/signout`
- `POST /auth/forgot-password`
- `POST /auth/reset-password`
- `POST /auth/verify-email`
- `POST /auth/change-password`
- `POST /auth/update-email`
- `DELETE /auth/account`

## Users

- `GET /users/me`
- `PATCH /users/me`

## Sessions

- `GET /sessions`
- `DELETE /sessions/{session_id}`

## Organizations

- `POST /organizations`
- `GET /organizations`
- `PATCH /organizations/{organization_id}`
- `DELETE /organizations/{organization_id}`

## Teams

- `POST /organizations/{organization_id}/teams`
- `GET /organizations/{organization_id}/teams`

## Invitations

- `POST /organizations/{organization_id}/invitations`

## OAuth Providers

The identity model supports OAuth accounts through `oauth_accounts`. Google is the first planned provider using:

- `GOOGLE_OAUTH_CLIENT_ID`
- `GOOGLE_OAUTH_CLIENT_SECRET`
- `GOOGLE_OAUTH_REDIRECT_URI`

Additional providers should implement the same provider adapter contract: build authorization URL, exchange code, normalize profile, link or create user.

## Security Controls

- Passwords are hashed with Argon2 through `pwdlib`.
- Access tokens are short-lived JWTs.
- Refresh tokens are opaque and stored as SHA-256 hashes.
- Sessions can be listed and revoked.
- Authentication events are written to `audit_logs`.
- RBAC permissions are centralized in `identity/rbac.py`.
- API responses do not reveal whether an email exists during password reset.
- Security headers and rate limiting middleware are installed by default.

## Response Shape

Successful auth responses return:

```json
{
  "user": {},
  "organization": {},
  "tokens": {
    "access_token": "...",
    "refresh_token": "...",
    "token_type": "bearer",
    "expires_in": 900
  }
}
```

Simple mutations return:

```json
{
  "ok": true,
  "message": "Done"
}
```