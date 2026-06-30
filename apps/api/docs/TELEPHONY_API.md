# Telephony API

All telephony endpoints require identity middleware and organization-scoped permissions.

## Provider Endpoints

- `GET /api/v1/telephony/providers/catalog`
- `POST /api/v1/telephony/providers`
- `GET /api/v1/telephony/providers?workspace_id=...`

## Number Endpoints

- `POST /api/v1/telephony/numbers`
- `GET /api/v1/telephony/numbers?workspace_id=...`

## Queue Endpoints

- `POST /api/v1/telephony/queues`
- `GET /api/v1/telephony/queues?workspace_id=...`

## Call Endpoints

- `POST /api/v1/telephony/calls`
- `POST /api/v1/telephony/calls/{call_id}/end`
- `GET /api/v1/telephony/calls?workspace_id=...`
- `GET /api/v1/telephony/calls/{call_id}/events`

## Analytics Endpoint

- `GET /api/v1/telephony/analytics?workspace_id=...`

Responses follow the existing VoiceSense API style: JSON objects, UUID IDs, ISO timestamps, and explicit workspace scope.