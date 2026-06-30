# Customer Identity Resolution Guide

Identity resolution matches customers using phone number, email address, provider user ID, CRM ID, external ID, and workspace identity.

## Rules

The initial implementation supports deterministic matching by `workspace_id`, `identity_type`, and `identity_value`. Future configurable rules can score multiple signals, merge identities, flag conflicts, and preserve audit history.

## Security

Identity values may contain personal data. Access must remain organization-scoped, and future encryption or tokenization should be applied for sensitive identifiers.