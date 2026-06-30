import { AlertTriangle, BarChart3, CheckCircle2, Clock3, DatabaseZap, GitBranch, Headphones, KeyRound, Phone, RadioTower, Route, Server, ShieldCheck, Signal, Timer, Volume2 } from "lucide-react";

export const telephonyStats = [
  { label: "Active calls", value: "42", detail: "8 queued", icon: Phone, tone: "green" },
  { label: "Numbers", value: "218", detail: "14 regions", icon: Phone, tone: "blue" },
  { label: "Avg pickup", value: "4.2s", detail: "p95 9.8s", icon: Timer, tone: "purple" },
  { label: "Provider health", value: "99.9%", detail: "failover ready", icon: Signal, tone: "amber" },
];
export const providers = [
  { name: "Twilio US", provider: "twilio", status: "Enabled", region: "US", latency: "42 ms", health: 99 },
  { name: "Telnyx EU", provider: "telnyx", status: "Enabled", region: "EU", latency: "58 ms", health: 98 },
  { name: "Custom SIP", provider: "custom_sip", status: "Standby", region: "Global", latency: "71 ms", health: 94 },
];

export const numbers = [
  { number: "+1 415 010 2194", label: "Support main", route: "Customer Care", status: "Active", region: "US" },
  { number: "+44 20 8102 3301", label: "UK sales", route: "Revenue Desk", status: "Active", region: "UK" },
  { number: "+1 646 019 8820", label: "Escalations", route: "Manager AI", status: "Testing", region: "US" },
];

export const queues = [
  { name: "Customer Care", waiting: 8, priority: "High", wait: "1m 12s", overflow: "Supervisor AI" },
  { name: "Revenue Desk", waiting: 3, priority: "Normal", wait: "38s", overflow: "Voicemail" },
  { name: "Technical Triage", waiting: 5, priority: "High", wait: "2m 08s", overflow: "Workflow" },
];

export const callTimeline = [
  { time: "10:42:01", title: "Call started", detail: "Inbound PSTN through Twilio US.", icon: Phone },
  { time: "10:42:02", title: "Routing matched", detail: "Business hours + language routed to Customer Care.", icon: Route },
  { time: "10:42:04", title: "Voice session opened", detail: "Full-duplex stream attached to Voice Engine.", icon: RadioTower },
  { time: "10:42:09", title: "Tool executed", detail: "CRM lookup completed in 112 ms.", icon: DatabaseZap },
];

export const callAnalytics = [
  { label: "Call count", value: "18.4k", icon: BarChart3 },
  { label: "AI resolution", value: "82%", icon: CheckCircle2 },
  { label: "Transfer count", value: "1.2k", icon: GitBranch },
  { label: "Queue time", value: "48s avg", icon: Clock3 },
];

export const sipReadiness = [
  { label: "SIP domains", value: "Modeled", icon: Server },
  { label: "SIP auth", value: "Secret refs", icon: KeyRound },
  { label: "Recording policy", value: "Configurable", icon: ShieldCheck },
  { label: "Streaming", value: "Voice Engine", icon: Volume2 },
];

export const telephonyAlerts = [
  { title: "Provider latency watch", detail: "EU Telnyx p95 latency increased above policy.", icon: AlertTriangle },
  { title: "Queue overflow ready", detail: "Customer Care overflow can route to Supervisor AI.", icon: Headphones },
];

