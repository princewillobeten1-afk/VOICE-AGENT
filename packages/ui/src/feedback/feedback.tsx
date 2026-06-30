import * as React from "react";
import * as ProgressPrimitive from "@radix-ui/react-progress";
import { AlertCircle, CheckCircle2, Inbox, Loader2 } from "lucide-react";
import { Button } from "../base/button";
import { cn } from "../utils";
export function Badge({ className, variant = "neutral", ...props }: React.HTMLAttributes<HTMLSpanElement> & { variant?: "neutral" | "success" | "warning" | "danger" | "info" }) { return <span className={cn("vs-badge", `vs-badge-${variant}`, className)} {...props} />; }
export function Alert({ className, variant = "info", title, children }: React.HTMLAttributes<HTMLDivElement> & { variant?: "info" | "success" | "warning" | "danger"; title: string }) { const Icon = variant === "success" ? CheckCircle2 : AlertCircle; return <div className={cn("vs-alert", `vs-alert-${variant}`, className)} role="status"><Icon size={18} /><div><strong>{title}</strong><p>{children}</p></div></div>; }
export function Progress({ value = 0 }: { value?: number }) { return <ProgressPrimitive.Root className="vs-progress" value={value}><ProgressPrimitive.Indicator className="vs-progress-bar" style={{ transform: `translateX(-${100 - value}%)` }} /></ProgressPrimitive.Root>; }
export function Skeleton({ className }: { className?: string }) { return <div className={cn("vs-skeleton", className)} aria-hidden="true" />; }
export function LoadingState({ label = "Loading" }: { label?: string }) { return <div className="vs-state"><Loader2 className="vs-spin" size={22} /><strong>{label}</strong></div>; }
export function EmptyState({ title, description, action }: { title: string; description: string; action?: React.ReactNode }) { return <div className="vs-state"><Inbox size={28} /><strong>{title}</strong><p>{description}</p>{action}</div>; }
export function ErrorState({ title, description, onRetry }: { title: string; description: string; onRetry?: () => void }) { return <div className="vs-state vs-state-error"><AlertCircle size={28} /><strong>{title}</strong><p>{description}</p>{onRetry ? <Button variant="outline" onClick={onRetry}>Retry</Button> : null}</div>; }
export function Toast({ title, description }: { title: string; description?: string }) { return <div className="vs-toast" role="status"><strong>{title}</strong>{description ? <p>{description}</p> : null}</div>; }