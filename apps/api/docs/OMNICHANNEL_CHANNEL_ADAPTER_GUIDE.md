# Omnichannel Channel Adapter Guide

Adapters should expose one stable interface for receive, send, typing, attachments, reactions, read receipts, delivery status, presence, and conversation metadata.

## Adapter Responsibilities

- Verify provider webhook signatures.
- Normalize provider payloads into `omnichannel_messages`.
- Resolve or create customer identities.
- Attach the correct channel session and conversation reference.
- Format outbound responses using capability metadata.
- Emit delivery events for sent, delivered, read, failed, retried, and expired states.

## Provider Isolation

Provider credentials are referenced by `secret_ref`. Runtime code should never store plaintext provider secrets in application tables.