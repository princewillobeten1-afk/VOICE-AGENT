# Tool API

All endpoints are mounted under `/v1/tools`.

## Registry

`GET /tools?workspace_id={id}` lists tools.

`POST /tools` registers a tool.

`PATCH /tools/{tool_id}` updates a tool.

`POST /tools/{tool_id}/enable` enables a tool.

`POST /tools/{tool_id}/disable` disables a tool.

`GET /tools/{tool_id}/versions` lists tool versions.

## Runtime

`POST /tools/{tool_id}/validate` validates a payload.

`POST /tools/{tool_id}/execute` executes through the guarded simulated runtime.

`GET /tools/executions/history?workspace_id={id}` lists execution history.

`GET /tools/executions/{execution_id}/logs` lists execution logs.

## Analytics and MCP

`GET /tools/analytics/summary?workspace_id={id}` returns usage and health summary.

`POST /tools/mcp-servers` registers a placeholder MCP server.

`GET /tools/mcp-servers?workspace_id={id}` lists MCP server definitions.
