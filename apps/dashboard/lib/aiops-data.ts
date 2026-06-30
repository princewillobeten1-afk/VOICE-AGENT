import { Activity, AlertTriangle, BarChart3, Bot, BrainCircuit, CheckCircle2, Clock3, DatabaseZap, DollarSign, FileSearch, Gauge, GitBranch, HeartPulse, MessageSquareText, RadioTower, ShieldCheck, Sparkles, TrendingUp, Workflow, Wrench } from "lucide-react";

export const aiopsStats = [
  { label: "AI employees", value: "128", detail: "94 active", icon: Bot, tone: "green" },
  { label: "Live conversations", value: "248", detail: "31 escalated", icon: MessageSquareText, tone: "blue" },
  { label: "Success rate", value: "97.8%", detail: "+1.4%", icon: CheckCircle2, tone: "purple" },
  { label: "AI cost", value: "$4.8k", detail: "forecast $19.2k", icon: DollarSign, tone: "amber" },
];

export const liveSignals = [
  { label: "Voice sessions", value: "42", icon: RadioTower, status: "Operational" },
  { label: "Workflow runs", value: "186", icon: Workflow, status: "12 paused" },
  { label: "Tool calls", value: "1.8k", icon: Wrench, status: "98.4% success" },
  { label: "Collaboration", value: "142", icon: GitBranch, status: "31 supervised" },
  { label: "Knowledge queries", value: "8.9k", icon: FileSearch, status: "86 ms avg" },
  { label: "Memory ops", value: "12.4k", icon: BrainCircuit, status: "Healthy" },
];

export const health = [
  { component: "Voice Engine", score: 98, status: "Operational", icon: RadioTower },
  { component: "Conversation Engine", score: 97, status: "Operational", icon: MessageSquareText },
  { component: "Workflow Engine", score: 95, status: "Watch", icon: Workflow },
  { component: "Tool Runtime", score: 99, status: "Operational", icon: Wrench },
  { component: "Knowledge", score: 92, status: "Indexing", icon: DatabaseZap },
  { component: "Memory", score: 96, status: "Operational", icon: BrainCircuit },
];

export const costRows = [
  { type: "LLM", amount: "$2,140", unit: "responses", trend: "+8%" },
  { type: "STT", amount: "$680", unit: "minutes", trend: "+3%" },
  { type: "TTS", amount: "$740", unit: "minutes", trend: "+5%" },
  { type: "Embeddings", amount: "$410", unit: "chunks", trend: "-2%" },
  { type: "Vector DB", amount: "$360", unit: "queries", trend: "+1%" },
  { type: "Tools", amount: "$510", unit: "executions", trend: "+11%" },
];

export const alerts = [
  { title: "Workflow failure spike", detail: "Support Escalation failure rate crossed 4%.", severity: "warning", icon: AlertTriangle },
  { title: "Cost threshold watch", detail: "TTS spend is trending above budget.", severity: "info", icon: DollarSign },
  { title: "Knowledge freshness", detail: "Legal Policies has stale documents.", severity: "warning", icon: FileSearch },
];

export const evaluations = [
  { label: "Goal completion", value: "94%", icon: Sparkles },
  { label: "Instruction following", value: "96%", icon: ShieldCheck },
  { label: "Knowledge accuracy", value: "91%", icon: FileSearch },
  { label: "Human review score", value: "4.7/5", icon: CheckCircle2 },
];

export const auditEvents = [
  { time: "10:42", title: "Tool executed", detail: "Knowledge Retrieval completed for Maya.", icon: Wrench },
  { time: "10:39", title: "Workflow changed", detail: "Lead Qualification published v12.", icon: Workflow },
  { time: "10:31", title: "Permission updated", detail: "HTTP Request denied for Members.", icon: ShieldCheck },
  { time: "10:12", title: "Login event", detail: "Admin signed in from trusted device.", icon: Activity },
];

export const trends = [
  { label: "Response time", value: "642 ms", icon: Clock3 },
  { label: "Error rate", value: "2.2%", icon: Gauge },
  { label: "CSAT", value: "4.6/5", icon: HeartPulse },
  { label: "Optimization", value: "12 ideas", icon: TrendingUp },
];
