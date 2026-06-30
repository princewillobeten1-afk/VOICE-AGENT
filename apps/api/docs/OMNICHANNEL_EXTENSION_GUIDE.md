# Omnichannel Developer Extension Guide

## Add A New Channel

1. Add channel and provider keys to the catalog.
2. Define capability metadata for text, rich messages, attachments, delivery, presence, typing, read receipts, and reactions.
3. Implement webhook verification and inbound normalization.
4. Implement outbound formatting and send behavior.
5. Write delivery event mapping for provider callbacks.
6. Add contract tests with provider payload fixtures.

## Smart Channel Selection

Future channel selection should use customer preference, urgency, availability, cost, content type, business rules, and provider health.

## Observability

Adapters should write delivery events and channel analytics, and publish domain events under `omnichannel.*` for AIOps and workflow subscriptions.