# Tool Developer Guide

Use this guide to create custom tools safely.

## Requirements

- Define a stable slug.
- Provide input and output schemas.
- Declare auth requirements and permission requirements.
- Set timeout and retry policy.
- Store secrets by reference only.
- Return structured results.
- Emit logs for each runtime stage.

## Adapter Boundary

Provider-specific execution belongs in adapters. Core Tool Runtime remains responsible for guardrails, logs, permission checks, analytics, and standardized result envelopes.
