# Metrics Collection Guide

AIOps metrics are stored as high-volume operational telemetry in `ops_metrics`, `usage_records`, `analytics_events`, and `metric_snapshots`.

Metric families include conversations, voice, workflows, tools, retrieval, memory, collaboration, infrastructure, cost, security, and quality.

Collectors should write organization and workspace scoped records with timestamped dimensions. Aggregates should be materialized into snapshots when query volume grows.
