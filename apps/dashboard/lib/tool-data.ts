import { Activity, AlertTriangle, Braces, CheckCircle2, Clock3, Code2, Database, FileSearch, Gauge, GitBranch, Globe2, KeyRound, Layers3, LockKeyhole, Network, Play, Search, Server, ShieldCheck, Sparkles, Terminal, Wrench, Zap } from "lucide-react";

export const toolStats = [
  { label: "Registered tools", value: "86", detail: "24 enabled", icon: Wrench, tone: "green" },
  { label: "Executions", value: "42.1k", detail: "last 7 days", icon: Activity, tone: "blue" },
  { label: "Success rate", value: "98.4%", detail: "guarded runtime", icon: CheckCircle2, tone: "purple" },
  { label: "Avg latency", value: "112 ms", detail: "simulated adapters", icon: Gauge, tone: "amber" },
];

export const tools = [
  { name: "Knowledge Retrieval", category: "AI", status: "Enabled", runtime: "Internal", auth: "Workspace", executions: "12.4k", health: 99 },
  { name: "Memory Access", category: "AI", status: "Enabled", runtime: "Internal", auth: "Policy", executions: "8.1k", health: 97 },
  { name: "Workflow Execution", category: "Automation", status: "Enabled", runtime: "Internal", auth: "RBAC", executions: "6.8k", health: 96 },
  { name: "HTTP Request", category: "Developer", status: "Disabled", runtime: "Sandbox", auth: "Secret ref", executions: "2.2k", health: 82 },
];

export const runtimeStages = [
  { label: "Request", detail: "Normalize context and payload", icon: Braces },
  { label: "Permission", detail: "RBAC and tool policy check", icon: ShieldCheck },
  { label: "Validation", detail: "Schema, required fields, constraints", icon: CheckCircle2 },
  { label: "Authentication", detail: "Secret refs and connected accounts", icon: LockKeyhole },
  { label: "Execution", detail: "Provider-agnostic runtime adapter", icon: Zap },
  { label: "Logging", detail: "Trace, latency, result, analytics", icon: Activity },
];

export const executions = [
  { id: "tool_exec_82A", tool: "Knowledge Retrieval", status: "Completed", latency: "88 ms", retries: 0, source: "Maya" },
  { id: "tool_exec_81F", tool: "Workflow Execution", status: "Completed", latency: "124 ms", retries: 0, source: "Support Agent" },
  { id: "tool_exec_80C", tool: "HTTP Request", status: "Rejected", latency: "4 ms", retries: 0, source: "Sales Agent" },
  { id: "tool_exec_7FF", tool: "Memory Access", status: "Completed", latency: "52 ms", retries: 1, source: "Supervisor" },
];

export const categories = [
  { label: "AI", detail: "Prompt, memory, retrieval", icon: Sparkles },
  { label: "Communication", detail: "Email, SMS, WhatsApp, Slack", icon: Globe2 },
  { label: "Business", detail: "CRM, ERP, calendar", icon: Database },
  { label: "Automation", detail: "Workflows, events, jobs", icon: GitBranch },
  { label: "Developer", detail: "HTTP, GraphQL, REST, webhooks", icon: Code2 },
  { label: "Custom", detail: "SDK plugins and org tools", icon: Terminal },
];

export const mcpServers = [
  { name: "Internal Docs MCP", status: "Placeholder", transport: "stdio", tools: 0, resources: "modeled" },
  { name: "Enterprise Services MCP", status: "Disabled", transport: "http", tools: 0, resources: "future" },
  { name: "Developer Sandbox MCP", status: "Draft", transport: "websocket", tools: 0, resources: "future" },
];

export const permissionRules = [
  { principal: "AI employees", action: "discover", effect: "allow", condition: "workspace + category" },
  { principal: "Developers", action: "execute", effect: "allow", condition: "non-secret tools" },
  { principal: "Members", action: "execute", effect: "deny", condition: "external APIs" },
  { principal: "Admins", action: "manage", effect: "allow", condition: "organization" },
];

export const toolLogs = [
  { time: "10:42", title: "Execution completed", detail: "Knowledge Retrieval returned structured context.", icon: CheckCircle2 },
  { time: "10:39", title: "Request rejected", detail: "HTTP Request missing required endpoint field.", icon: AlertTriangle },
  { time: "10:31", title: "Tool enabled", detail: "Workflow Execution moved to enabled status.", icon: Wrench },
  { time: "10:12", title: "MCP server registered", detail: "Internal Docs MCP placeholder created.", icon: Server },
];

export const toolIcons = { FileSearch, Network, Search, Clock3, KeyRound, Layers3 };
