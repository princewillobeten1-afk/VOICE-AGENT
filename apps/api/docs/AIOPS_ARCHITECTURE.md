# AIOps Architecture

Task 020 introduces the AI Operations Center for VoiceSense. AIOps is the operational command center for monitoring AI employees, conversations, voice, workflows, tools, knowledge, memory, multi-agent collaboration, cost, health, alerts, audit activity, and evaluation results.

## Scope

AIOps owns operational dashboards, metrics, alert rules, alert events, health reports, cost records, evaluation results, analytics queries, and audit visibility.

It does not implement external billing integrations, automatic self-healing, autonomous optimization, or predictive model recommendations.

## Modules

- `app/analytics/models.py`: metrics, dashboards, alerts, health, costs, evaluations, usage, events, and snapshots.
- `app/analytics/service.py`: cross-platform aggregation and summary logic.
- `app/analytics/router.py`: dashboard, live monitoring, breakdown, alerts, health, cost, evaluation, and audit APIs.
