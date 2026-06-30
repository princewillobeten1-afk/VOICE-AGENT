import { Activity, Bot, BrainCircuit, Building2, CheckCircle2, Clock3, GitBranch, KeyRound, Layers3, MessageSquareText, Network, Route, ShieldCheck, Sparkles, UsersRound, Workflow } from "lucide-react";

export const teamStats = [
  { label: "AI teams", value: "18", detail: "6 departments", icon: Building2, tone: "green" },
  { label: "Active sessions", value: "142", detail: "31 supervised", icon: Network, tone: "blue" },
  { label: "Delegations", value: "4.8k", detail: "last 7 days", icon: GitBranch, tone: "purple" },
  { label: "Resolution rate", value: "96.1%", detail: "+2.4%", icon: CheckCircle2, tone: "amber" },
];

export const teams = [
  { name: "Revenue Desk", department: "Sales", supervisor: "Morgan", members: 8, status: "Active", load: 74 },
  { name: "Customer Care", department: "Support", supervisor: "Maya", members: 12, status: "Active", load: 82 },
  { name: "Technical Triage", department: "Support", supervisor: "Riley", members: 6, status: "Review", load: 61 },
  { name: "Operations Hub", department: "Operations", supervisor: "Avery", members: 5, status: "Active", load: 48 },
];

export const orgNodes = [
  { label: "VoiceSense AI Org", role: "Organization", icon: Building2 },
  { label: "Revenue", role: "Department", icon: UsersRound },
  { label: "Sales AI", role: "Specialist", icon: Bot },
  { label: "Pricing AI", role: "Specialist", icon: Sparkles },
  { label: "Manager AI", role: "Supervisor", icon: ShieldCheck },
];

export const delegations = [
  { task: "Qualify enterprise lead", route: "Receptionist -> Sales -> Pricing", confidence: "0.91", status: "Assigned" },
  { task: "Resolve refund exception", route: "Support -> Manager -> CRM", confidence: "0.86", status: "In review" },
  { task: "Book technical onboarding", route: "Sales -> Technical Support -> Calendar", confidence: "0.78", status: "Completed" },
];

export const timeline = [
  { time: "10:42", title: "Task delegated", detail: "Receptionist AI routed lead qualification to Sales AI.", icon: GitBranch },
  { time: "10:40", title: "Shared context updated", detail: "Customer intent, budget, and timeline added to team context.", icon: BrainCircuit },
  { time: "10:37", title: "Supervisor approved", detail: "Manager AI approved pricing recommendation.", icon: ShieldCheck },
  { time: "10:34", title: "Workflow progressed", detail: "Follow-up automation moved to email step.", icon: Workflow },
];

export const policies = [
  { name: "Max delegation depth", value: "4 levels", icon: Layers3 },
  { name: "Cross-department approval", value: "Required", icon: KeyRound },
  { name: "Escalation timeout", value: "15 min", icon: Clock3 },
  { name: "Allowed routing", value: "Role + workload", icon: Route },
];

export const analytics = [
  { label: "Avg resolution", value: "3m 18s", icon: Activity },
  { label: "Utilization", value: "71%", icon: Bot },
  { label: "Escalation rate", value: "6.2%", icon: ShieldCheck },
  { label: "Shared context hits", value: "18.9k", icon: MessageSquareText },
];
