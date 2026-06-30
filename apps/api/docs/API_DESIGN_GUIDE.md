# API Design Guide

VoiceSense APIs should use predictable resource names, stable version prefixes, consistent JSON envelopes where needed, cursor pagination for lists, explicit filtering/sorting parameters, idempotency keys for mutation retries, and standard error objects.

Every dashboard capability should eventually have an equivalent API endpoint.