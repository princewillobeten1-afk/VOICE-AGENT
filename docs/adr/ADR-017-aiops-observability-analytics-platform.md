# ADR-017: AI Operations Center Observability and Analytics Platform

## Status

Accepted

## Context

VoiceSense needs a central operations layer for monitoring AI employees, conversations, voice sessions, workflows, tool executions, knowledge usage, memory usage, multi-agent collaboration, costs, health, alerts, audit events, and evaluation results.

## Decision

VoiceSense will extend the analytics foundation into an AI Operations Center. AIOps introduces operational dashboards, metrics, alert rules, alert events, health reports, cost records, evaluation results, analytics APIs, audit visibility, and an executive dashboard UI.

AIOps aggregates across existing platform modules instead of duplicating their domain records. It stores operational telemetry separately from transactional source tables.

## Consequences

This creates a single operational command center for enterprise customers. It also establishes a scalable path for real-time monitoring, cost intelligence, compliance reporting, quality evaluation, and health dashboards.

The trade-off is that Task 020 provides frameworks and aggregation surfaces, not autonomous optimization, self-healing, or trained predictive recommendations.

## Follow-Ups

- Add streaming event ingestion and WebSocket live dashboards.
- Add materialized rollups for high-volume metrics.
- Add notification delivery for alert events.
- Add provider-level cost ingestion adapters.
- Add evaluation runners and human review workflows.
