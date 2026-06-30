import { Archive, AudioLines, FileArchive, FileText, Folder, Image, MoreHorizontal, ShieldCheck, UploadCloud } from "lucide-react";

export const storageStats = [
  { label: "Total assets", value: "18,420", detail: "+842 this month", icon: Archive, tone: "green" },
  { label: "Storage used", value: "1.84 TB", detail: "46% of allocation", icon: UploadCloud, tone: "blue" },
  { label: "Protected files", value: "99.98%", detail: "Encrypted at rest", icon: ShieldCheck, tone: "purple" },
  { label: "Active uploads", value: "12", detail: "4 resumable", icon: MoreHorizontal, tone: "amber" },
];

export const folders = [
  { name: "Knowledge sources", count: 482, size: "84.2 GB", owner: "Ops", updated: "8 min ago" },
  { name: "Call recordings", count: 1204, size: "612 GB", owner: "Voice", updated: "24 min ago" },
  { name: "Reports", count: 97, size: "9.8 GB", owner: "Analytics", updated: "1 hr ago" },
  { name: "Legal and compliance", count: 68, size: "4.1 GB", owner: "Admin", updated: "Yesterday" },
];

export const files = [
  { name: "Support policy handbook.pdf", type: "PDF", icon: FileText, size: "8.4 MB", owner: "Ada", status: "Ready", updated: "4 min ago", tags: ["knowledge", "approved"] },
  { name: "Q2 customer success calls.zip", type: "Archive", icon: FileArchive, size: "2.1 GB", owner: "Maya", status: "Uploading", updated: "12 min ago", tags: ["calls"] },
  { name: "Onboarding voice sample.wav", type: "Audio", icon: AudioLines, size: "42 MB", owner: "Noah", status: "Ready", updated: "38 min ago", tags: ["voice", "training"] },
  { name: "Brand response examples.png", type: "Image", icon: Image, size: "1.8 MB", owner: "Iris", status: "Ready", updated: "Today", tags: ["brand"] },
  { name: "Enterprise security questionnaire.docx", type: "Document", icon: FileText, size: "612 KB", owner: "Ada", status: "Review", updated: "Yesterday", tags: ["security", "sales"] },
];

export const uploads = [
  { name: "call-recordings-june.zip", progress: 72, speed: "18 MB/s", status: "Uploading" },
  { name: "kb-refresh-batch-04.pdf", progress: 100, speed: "Complete", status: "Ready" },
  { name: "training-audio-pack.wav", progress: 36, speed: "8 MB/s", status: "Resumable" },
];

export const activity = [
  { title: "Folder created", detail: "Knowledge sources / Returns", time: "10:48" },
  { title: "File restored", detail: "pricing-faq.pdf moved out of trash", time: "10:22" },
  { title: "Bulk move completed", detail: "42 files moved to Reports", time: "09:58" },
  { title: "Provider health check", detail: "Local storage adapter is operational", time: "09:30" },
];

export const emptyStorageStates = [
  { title: "No files in this folder", description: "Upload assets, drag in folders, or move files here from another workspace location.", action: "Upload files", icon: UploadCloud },
  { title: "No active uploads", description: "Resumable uploads will appear here with progress, retry, and cancellation controls.", action: "Start upload", icon: Archive },
  { title: "No archived files", description: "Deleted assets stay recoverable until permanent deletion policies remove them.", action: "Open trash", icon: Folder },
];