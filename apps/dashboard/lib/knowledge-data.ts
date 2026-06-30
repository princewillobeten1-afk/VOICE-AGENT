import { Activity, Archive, BookOpen, CheckCircle2, Clock3, Cloud, Database, FileText, FolderOpen, Globe2, History, KeyRound, Layers3, Link2, ListFilter, RefreshCw, Search, ShieldCheck, Tags, UploadCloud } from "lucide-react";

export const knowledgeStats = [
  { label: "Knowledge bases", value: "14", detail: "Sales, Support, Legal", icon: BookOpen, tone: "green" },
  { label: "Documents", value: "42.8k", detail: "+2.1k this month", icon: FileText, tone: "blue" },
  { label: "Storage", value: "1.8 TB", detail: "Versioned assets", icon: Database, tone: "purple" },
  { label: "Freshness", value: "92%", detail: "Healthy content", icon: CheckCircle2, tone: "amber" },
];

export const knowledgeBases = [
  { name: "Customer Support", owner: "CX Team", visibility: "Workspace", status: "Published", docs: "12,420", health: 96 },
  { name: "Sales Enablement", owner: "Revenue", visibility: "Shared", status: "Published", docs: "8,140", health: 91 },
  { name: "Legal Policies", owner: "Legal", visibility: "Restricted", status: "Review", docs: "1,840", health: 88 },
  { name: "Engineering", owner: "Product", visibility: "Workspace", status: "Draft", docs: "6,430", health: 74 },
];

export const sourceTypes = [
  { label: "Documents", detail: "PDF, DOCX, TXT, CSV, Markdown", icon: FileText, status: "Ready" },
  { label: "Websites", detail: "Registered crawl config, no crawler yet", icon: Globe2, status: "Architecture" },
  { label: "Connected services", detail: "Drive, Notion, Confluence, SharePoint", icon: Link2, status: "Prepared" },
  { label: "Databases", detail: "Postgres, MySQL, Supabase, Airtable", icon: Database, status: "Prepared" },
  { label: "Cloud storage", detail: "S3, R2, Azure Blob", icon: Cloud, status: "Prepared" },
];

export const documents = [
  { title: "Refund policy v5.pdf", type: "PDF", base: "Customer Support", status: "Published", freshness: "Fresh", updated: "8 min ago" },
  { title: "Enterprise security FAQ.md", type: "Markdown", base: "Sales Enablement", status: "Draft", freshness: "Review", updated: "34 min ago" },
  { title: "Contract approval SOP.docx", type: "DOCX", base: "Legal Policies", status: "Published", freshness: "Fresh", updated: "Yesterday" },
  { title: "Product limits.csv", type: "CSV", base: "Engineering", status: "Validation", freshness: "Stale", updated: "3 days ago" },
];

export const uploadItems = [
  { name: "support-macros.zip", progress: 82, status: "Uploading" },
  { name: "legal-archive", progress: 44, status: "Folder upload" },
  { name: "duplicate-policy.pdf", progress: 100, status: "Duplicate detected" },
];

export const websiteConfigs = [
  { url: "docs.voicesense.test", schedule: "Daily", status: "Registered", paths: "/docs, /api" },
  { url: "help.acme.test", schedule: "Weekly", status: "Pending", paths: "/articles" },
];

export const activityFeed = [
  { time: "10:42", title: "Document published", detail: "Refund policy v5 moved to published.", icon: CheckCircle2 },
  { time: "10:11", title: "Sync queued", detail: "Notion workspace incremental sync queued.", icon: RefreshCw },
  { time: "09:45", title: "Permission changed", detail: "Legal Policies limited to admin and legal teams.", icon: KeyRound },
  { time: "Yesterday", title: "Duplicate detected", detail: "2 copies of support escalation SOP found.", icon: Archive },
];

export const qualityChecks = [
  { label: "Duplicate detection", value: "32 warnings", icon: Search },
  { label: "Missing content", value: "8 issues", icon: FileText },
  { label: "Freshness", value: "92% healthy", icon: Clock3 },
  { label: "Permissions", value: "No leaks", icon: ShieldCheck },
];

export const categories = ["All", "Sales", "HR", "Customer Support", "Legal", "Finance", "Engineering", "Marketing", "Product"];
export const knowledgeIcons = { ListFilter, Tags, FolderOpen, Layers3, History, UploadCloud, Activity };