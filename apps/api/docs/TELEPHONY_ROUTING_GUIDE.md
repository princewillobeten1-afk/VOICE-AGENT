# Telephony Routing Guide

Routing rules decide where a call should go before the Voice Engine or Conversation Engine takes over.

## Inputs

- Workspace and organization.
- Dialed number or SIP endpoint.
- Direction and call type.
- Region and provider health.
- Customer metadata.
- Business hours and compliance metadata.

## Destinations

Supported destination types are data-modeled as `agent`, `queue`, `workflow`, `voicemail`, `external_number`, and future `human_team`.

## Priority

Rules are evaluated by ascending priority. Number-specific rules can override workspace defaults. When no rule matches, the number default route is used.

## Future Conditions

Condition payloads should support language, country, customer tier, previous sentiment, account owner, business hours, holiday calendar, compliance region, and AIOps health signals.