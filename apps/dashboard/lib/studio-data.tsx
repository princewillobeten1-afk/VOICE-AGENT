import { Activity, BarChart3, Beaker, Bot, Boxes, Braces, BrainCircuit, CheckCircle2, GitCompare, GitPullRequest, History, MessageSquareText, Play, Rocket, ScrollText, ShieldCheck, Sparkles, TestTube2, Workflow } from "lucide-react";

export const studioStats = [
  { label: "Prompt versions", value: "184", detail: "+18 this week", icon: ScrollText, tone: "green" },
  { label: "Eval pass rate", value: "92.4%", detail: "+4.8% vs baseline", icon: CheckCircle2, tone: "blue" },
  { label: "Simulator runs", value: "3.2k", detail: "412 edge cases", icon: MessageSquareText, tone: "amber" },
  { label: "Avg latency", value: "712 ms", detail: "voice path excluded", icon: Activity, tone: "purple" },
];

export const studioLifecycle = [
  { label: "Prompt", value: "System instructions and variables", icon: Braces },
  { label: "Context", value: "Knowledge, memory, customer state", icon: BrainCircuit },
  { label: "Action", value: "Tools, workflows, approvals", icon: Workflow },
  { label: "Evaluate", value: "Tests, benchmarks, regressions", icon: TestTube2 },
  { label: "Deploy", value: "QA, staging, production, rollback", icon: Rocket },
];

export const promptVersions = [
  { version: "v18", status: "Draft", score: "94.1", cost: "$0.014", latency: "692 ms" },
  { version: "v17", status: "Production", score: "91.3", cost: "$0.016", latency: "741 ms" },
  { version: "v16", status: "Archived", score: "87.9", cost: "$0.019", latency: "814 ms" },
];

export const templates = ["Customer Support", "Sales", "Healthcare", "Finance", "Recruiting", "Scheduling", "Education", "Ecommerce", "Hospitality", "Custom"];

export const evaluationMetrics = [
  { label: "Goal completion", value: "96%", progress: 96 },
  { label: "Instruction following", value: "94%", progress: 94 },
  { label: "Tool accuracy", value: "91%", progress: 91 },
  { label: "Knowledge grounding", value: "89%", progress: 89 },
];

export const aiTimeline = [
  { step: "Prompt execution", detail: "System, developer, and dynamic sections assembled", icon: ScrollText },
  { step: "Memory retrieval", detail: "3 long-term memories selected", icon: BrainCircuit },
  { step: "Knowledge retrieval", detail: "5 chunks reranked from support index", icon: Boxes },
  { step: "Tool call", detail: "CRM lookup authorized by policy", icon: Workflow },
  { step: "LLM response", detail: "Response streamed with guardrail checks", icon: Sparkles },
];

export const experiments = [
  { name: "Prompt A vs B", target: "Billing deflection", lift: "+6.2%", status: "Running" },
  { name: "Model latency test", target: "Support triage", lift: "-122 ms", status: "Ready" },
  { name: "Knowledge variant", target: "Refund accuracy", lift: "+4.1%", status: "Review" },
];

export const collaboration = [
  { time: "12:20", title: "QA approved v17 for staging", detail: "Deployment gate passed", icon: GitPullRequest },
  { time: "11:48", title: "Prompt diff reviewed", detail: "Guardrail section tightened", icon: GitCompare },
  { time: "10:15", title: "Regression suite completed", detail: "48 passed, 2 require review", icon: TestTube2 },
];

export const studioReadiness = ["Prompt Builder", "Version Control", "Playground", "Simulator", "Evaluation", "Regression", "A/B Testing", "Benchmarks", "Deployment", "Replay Studio", "AI Timeline", "Analytics"];
export const studioIcons = { Bot, BarChart3, Beaker, History, Play, ShieldCheck };