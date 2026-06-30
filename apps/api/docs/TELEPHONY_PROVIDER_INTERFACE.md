# Telephony Provider Interface

Provider adapters should expose a stable capability interface rather than leaking vendor SDK details into product code.

## Required Capabilities

- Normalize inbound call webhooks.
- Start outbound calls.
- Attach media streams to the Voice Engine.
- Verify provider signatures.
- Handle call status callbacks.
- Emit recording lifecycle callbacks.
- Send and receive DTMF events.
- Hang up, hold, resume, and transfer calls where supported.

## Configuration

`telephony_provider_configs` stores provider, region, priority, health, capabilities, failover policy, provider config, and a secret reference. Secrets remain outside the database.

## Failover

Provider selection is priority-based and can be region-filtered. Future runtime adapters should support fallback on provider outage, latency threshold, account quota, or destination country.

## Out of Scope For Task 021

Task 021 does not create provider accounts, buy numbers, configure production webhooks, or charge for telephony usage.