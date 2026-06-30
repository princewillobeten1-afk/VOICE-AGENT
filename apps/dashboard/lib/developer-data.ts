import { Activity, BarChart3, BookOpen, Braces, Code2, FileClock, Gauge, Globe2, KeyRound, LockKeyhole, RadioTower, RotateCcw, ScrollText, Settings, ShieldCheck, Webhook } from "lucide-react";

export const developerNav = [
  { label: "Overview", icon: Activity },
  { label: "API Keys", icon: KeyRound },
  { label: "Webhooks", icon: Webhook },
  { label: "API Playground", icon: Braces },
  { label: "Documentation", icon: BookOpen },
  { label: "SDKs", icon: Code2 },
  { label: "OAuth Apps", icon: Globe2 },
  { label: "API Logs", icon: FileClock },
  { label: "Usage Analytics", icon: BarChart3 },
  { label: "Rate Limits", icon: Gauge },
  { label: "Settings", icon: Settings },
];

export const apiKeys = [
  { name: "Development key", prefix: "vsk_dev_c5f8...", environment: "Development", scopes: ["read", "write"], lastUsed: "4 minutes ago", expires: "Never", requests: "12.8k" },
  { name: "Production backend", prefix: "vsk_prod_92aa...", environment: "Production", scopes: ["read", "write", "webhooks"], lastUsed: "1 hour ago", expires: "Dec 31, 2026", requests: "184.2k" },
];

export const webhooks = [
  { url: "https://api.acme.com/voicesense/webhooks", events: ["conversation.started", "call.finished"], status: "Active", deliveries: "99.7%" },
  { url: "https://dev.acme.com/hooks", events: ["agent.created"], status: "Paused", deliveries: "--" },
];

export const playgroundEndpoints = [
  { method: "GET", path: "/v1/users/me", status: 200, latency: "124 ms" },
  { method: "POST", path: "/v1/developer/api-keys", status: 201, latency: "186 ms" },
  { method: "GET", path: "/v1/conversations", status: 200, latency: "142 ms" },
  { method: "POST", path: "/v1/webhooks/test", status: 202, latency: "211 ms" },
];

export const docsSections = [
  "Authentication Guide",
  "Quick Start",
  "API Reference",
  "SDK Guides",
  "Code Examples",
  "Webhook Guide",
  "Error Codes",
  "Rate Limits",
  "Changelog",
  "CLI Guide",
  "Sandbox Guide",
  "Migration Guides",
];

export const sdks = [
  { language: "TypeScript", package: "@voicesense/sdk", status: "Planned", icon: Code2 },
  { language: "JavaScript", package: "voicesense", status: "Planned", icon: Code2 },
  { language: "Python", package: "voicesense", status: "Planned", icon: Code2 },
  { language: "Go", package: "github.com/voicesense/voicesense-go", status: "Planned", icon: Code2 },
  { language: "Java", package: "com.voicesense", status: "Planned", icon: Code2 },
  { language: "C#", package: "VoiceSense", status: "Planned", icon: Code2 },
  { language: "PHP", package: "voicesense/voicesense-php", status: "Planned", icon: Code2 },
];

export const apiLogs = [
  { time: "11:42:18", method: "GET", endpoint: "/v1/users/me", status: 200, latency: "88 ms", requestId: "req_8f31" },
  { time: "11:41:02", method: "POST", endpoint: "/v1/developer/webhooks", status: 201, latency: "141 ms", requestId: "req_71ac" },
  { time: "11:39:44", method: "GET", endpoint: "/v1/conversations", status: 403, latency: "63 ms", requestId: "req_d22b" },
];

export const usageMetrics = [
  { label: "API requests", value: "184.2k", detail: "+18.4%", icon: RadioTower },
  { label: "Success rate", value: "99.2%", detail: "+0.3%", icon: ShieldCheck },
  { label: "Error rate", value: "0.8%", detail: "-0.2%", icon: LockKeyhole },
  { label: "Explorer runs", value: "3.8k", detail: "48 ms avg", icon: RotateCcw },
];

export const rateLimits = [
  { label: "Development", limit: "600 requests/min", used: "18%" },
  { label: "Production", limit: "6,000 requests/min", used: "42%" },
  { label: "Webhook deliveries", limit: "1,000 deliveries/min", used: "9%" },
];

export const oauthApps = [
  { name: "Acme internal portal", clientId: "vso_7da4...", environment: "Development", status: "Active" },
  { name: "Partner sandbox", clientId: "vso_91af...", environment: "Sandbox", status: "PKCE ready" },
];

export const developerIcons = { ScrollText };