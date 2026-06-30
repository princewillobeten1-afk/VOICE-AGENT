# Connector Authentication Guide

Supported authentication methods include OAuth 2.0, OAuth PKCE, API keys, JWT, service accounts, basic auth, bearer tokens, and custom auth.

Raw credentials must not be stored in integration tables. Store `secret_ref`, fingerprints, rotation version, expiry, and redacted metadata only.