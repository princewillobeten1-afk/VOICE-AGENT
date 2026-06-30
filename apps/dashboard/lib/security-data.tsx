import { Activity, AlertTriangle, BadgeCheck, Fingerprint, KeyRound, LockKeyhole, Network, Radar, ScanEye, ServerCog, ShieldCheck, UserCog } from "lucide-react";

export const securityStats = [
  { label: "Security score", value: "91", detail: "A- readiness posture", icon: ShieldCheck, tone: "green" },
  { label: "Active policies", value: "38", detail: "12 enforced globally", icon: LockKeyhole, tone: "blue" },
  { label: "Open risks", value: "4", detail: "1 high severity", icon: AlertTriangle, tone: "amber" },
  { label: "Audit events", value: "18.2k", detail: "30 day retention view", icon: Activity, tone: "purple" },
];

export const governancePolicies = [
  { name: "Admin MFA required", scope: "Organization", mode: "Enforce", status: "Active" },
  { name: "AI tool approval gates", scope: "Workspace", mode: "Enforce", status: "Active" },
  { name: "Customer data residency", scope: "Enterprise", mode: "Monitor", status: "Review" },
  { name: "Knowledge access isolation", scope: "Workspace", mode: "Enforce", status: "Active" },
];

export const accessModels = [
  { label: "RBAC", value: "Owner, Admin, Developer, Member", icon: UserCog },
  { label: "ABAC", value: "Resource, action, context, attributes", icon: Fingerprint },
  { label: "AI permissions", value: "Tools, memory, workflows, knowledge", icon: Network },
  { label: "Sessions", value: "Revocation-ready trusted devices", icon: ServerCog },
];

export const complianceFrameworks = [
  { label: "SOC 2", value: "Readiness", progress: 72 },
  { label: "ISO 27001", value: "Control map", progress: 58 },
  { label: "GDPR", value: "Data rights mapped", progress: 81 },
  { label: "HIPAA", value: "Awareness mode", progress: 34 },
];

export const securityEvents = [
  { time: "11:28", title: "High-risk secret rotation overdue", detail: "Production telephony provider key", icon: KeyRound },
  { time: "10:43", title: "Admin session started from trusted device", detail: "Ada Lovelace", icon: BadgeCheck },
  { time: "09:56", title: "ABAC policy matched workflow execution", detail: "Refund approval flow", icon: ScanEye },
  { time: "09:18", title: "SSO connection metadata refreshed", detail: "Acme Okta OIDC", icon: Radar },
];

export const securityReadiness = [
  { label: "SSO/OIDC", value: "Provider model ready", icon: ShieldCheck },
  { label: "Secrets", value: "Versioned references", icon: KeyRound },
  { label: "Compliance", value: "Evidence records", icon: BadgeCheck },
  { label: "Governance graph", value: "Snapshot API", icon: Network },
];

export const riskControls = ["Rate limiting", "Security headers", "Audit logs", "Session inventory", "Data retention policies", "Encryption key registry", "MFA enrollment model", "Risk event timeline"];