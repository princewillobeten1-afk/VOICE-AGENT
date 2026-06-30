# Developer Webhook Guide

Webhook endpoints support event registration, signing secret verification, retry policies, delivery logs, replay, signature validation, and test deliveries.

Webhook delivery should integrate with the event bus and expose enough metadata for debugging failures safely.