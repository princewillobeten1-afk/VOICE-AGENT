# Telephony SIP Guide

SIP support is modeled through `sip_endpoints` so VoiceSense can later support enterprise trunks, BYOC, office PBX integrations, and custom carrier connectivity.

## Endpoint Types

- `trunk`: carrier or enterprise SIP trunk.
- `domain`: hosted SIP domain for registration.
- `peer`: static endpoint with allowed IPs.

## Security

SIP credentials are referenced through `secret_ref`. Allowed IPs, headers, and routing config are metadata records. Runtime enforcement belongs in the future SIP gateway or provider adapter.

## Routing

SIP endpoint routing should resolve to the same destination model as PSTN numbers: AI agent, queue, workflow, voicemail, or external transfer target.