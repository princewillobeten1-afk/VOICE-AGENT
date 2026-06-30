# Secrets Management Guide

Task 026 models secrets as references, not plaintext values.

## Rules

- Store `secret_ref`, never raw secret material.
- Use `secret_versions` for rotation history.
- Use `rotation_policy`, `last_rotated_at`, and `expires_at` for compliance checks.
- Use provider-specific vault adapters in future runtime services.

## Providers

The initial model supports internal references and future external providers such as AWS Secrets Manager, GCP Secret Manager, Azure Key Vault, HashiCorp Vault, or enterprise-managed KMS.