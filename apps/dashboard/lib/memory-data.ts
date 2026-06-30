import { Activity, Archive, BrainCircuit, CheckCircle2, Clock3, Database, Eye, Filter, Goal, History, Layers3, Link2, LockKeyhole, MemoryStick, Pin, RefreshCw, Search, ShieldCheck, Sparkles, Tags, UserRound } from "lucide-react";

export const memoryStats = [
  { label: "Active memories", value: "18.2k", detail: "+1.4k this month", icon: MemoryStick, tone: "green" },
  { label: "Retrieval latency", value: "31 ms", detail: "Metadata scorer", icon: RefreshCw, tone: "blue" },
  { label: "Pinned facts", value: "428", detail: "High priority", icon: Pin, tone: "purple" },
  { label: "Expiring soon", value: "96", detail: "Policy cleanup", icon: Clock3, tone: "amber" },
];

export const memoryLayers = [
  { name: "Short-term", detail: "Recent messages, active topic, temporary variables", status: "Expiring", icon: Clock3 },
  { name: "Working", detail: "Current objective, active task, collection state", status: "Scoped", icon: Goal },
  { name: "Long-term", detail: "Preferences, contact info, frequently asked topics", status: "Persistent", icon: MemoryStick },
  { name: "Episodic", detail: "Past calls, support tickets, meeting summaries", status: "Summarized", icon: History },
  { name: "Semantic", detail: "Structured facts and relationships", status: "Indexed", icon: Database },
  { name: "Organizational", detail: "Policies, procedures, shared company knowledge", status: "Governed", icon: Layers3 },
  { name: "Shared", detail: "Multi-agent notes, handoff context, shared objectives", status: "Access controlled", icon: Link2 },
];

export const memoryRows = [
  { title: "Ada prefers concise billing updates", type: "long_term", category: "Preferences", privacy: "internal", score: "0.91", updated: "4 min ago", pinned: true },
  { title: "Refund approval requires manager review", type: "organizational", category: "Billing", privacy: "shared", score: "0.88", updated: "18 min ago", pinned: true },
  { title: "Northstar renewal call summary", type: "episodic", category: "Sales", privacy: "restricted", score: "0.74", updated: "Yesterday", pinned: false },
  { title: "Customer timezone is Africa/Lagos", type: "semantic", category: "Personal", privacy: "internal", score: "0.69", updated: "2 days ago", pinned: false },
  { title: "Collect appointment preferences", type: "working", category: "Tasks", privacy: "private", score: "0.62", updated: "2 days ago", pinned: false },
];

export const memoryTimeline = [
  { time: "10:42", event: "Memory retrieved", detail: "3 memories ranked for billing conversation.", icon: Search },
  { time: "10:39", event: "Memory created", detail: "Preference saved from support conversation.", icon: Sparkles },
  { time: "09:21", event: "Policy applied", detail: "Short-term memory expiration scheduled.", icon: ShieldCheck },
  { time: "Yesterday", event: "Memory merged", detail: "Duplicate billing facts merged into canonical memory.", icon: Link2 },
  { time: "Jun 26", event: "Memory archived", detail: "Old appointment detail archived by retention rule.", icon: Archive },
];

export const memoryCategories = ["All", "Personal", "Business", "Preferences", "Tasks", "Contacts", "Support", "Sales", "Billing", "Technical", "Organizational"];

export const memoryPolicies = [
  { name: "Short-term cleanup", scope: "Session", retention: "24 hours", status: "Active" },
  { name: "Customer preference retention", scope: "Workspace", retention: "730 days", status: "Active" },
  { name: "Sensitive support notes", scope: "Restricted", retention: "90 days", status: "Review" },
];

export const relatedMemories = [
  { title: "Billing tone preference", strength: "Strong", type: "semantic" },
  { title: "Refund ticket 4821", strength: "Medium", type: "episodic" },
  { title: "VIP retention playbook", strength: "Medium", type: "organizational" },
];

export const memoryHealth = [
  { label: "Privacy boundaries", state: "Enforced", icon: LockKeyhole },
  { label: "Version history", state: "Enabled", icon: History },
  { label: "Vector search", state: "Future", icon: BrainCircuit },
  { label: "Audit events", state: "Writing", icon: Activity },
  { label: "Access grants", state: "Scoped", icon: Eye },
  { label: "Retention", state: "Policy-ready", icon: ShieldCheck },
];

export const memoryActions = { Filter, Tags, CheckCircle2, UserRound };