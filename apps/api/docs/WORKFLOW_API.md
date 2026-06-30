# Workflow API

All workflow endpoints are mounted under `/v1/workflows`.

## Nodes

`GET /workflows/nodes` returns the node catalog.

## Workflows

`GET /workflows?workspace_id={id}` lists workflows.

`POST /workflows` creates a draft workflow and initial version.

`PATCH /workflows/{workflow_id}` updates a workflow and snapshots a draft version.

`POST /workflows/{workflow_id}/publish` publishes a version.

`GET /workflows/{workflow_id}/versions` lists version history.

## Execution

`POST /workflows/{workflow_id}/execute` creates a simulated durable run.

`POST /workflows/runs/{run_id}/pause` pauses a run.

`POST /workflows/runs/{run_id}/resume` resumes and completes a run in this foundation.

`GET /workflows/runs?workspace_id={id}` lists recent runs.

`GET /workflows/runs/{run_id}/logs` returns node execution logs.

## Monitoring

`GET /workflows/monitoring?workspace_id={id}` returns workflow counts, run status counts, average duration, node catalog size, queue mode, and fault-tolerance metadata.
