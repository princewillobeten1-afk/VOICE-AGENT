import * as React from "react";
import { cn } from "../utils";
export function PageLayout({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) { return <main className={cn("vs-page-layout", className)} {...props} />; }
export function DashboardLayout({ sidebar, children }: { sidebar: React.ReactNode; children: React.ReactNode }) { return <div className="vs-dashboard-layout">{sidebar}<main>{children}</main></div>; }
export function SettingsLayout({ nav, children }: { nav: React.ReactNode; children: React.ReactNode }) { return <div className="vs-settings-layout"><aside>{nav}</aside><section>{children}</section></div>; }
export function AuthLayout({ children }: { children: React.ReactNode }) { return <main className="vs-auth-layout">{children}</main>; }
export function CenteredLayout({ children }: { children: React.ReactNode }) { return <main className="vs-centered-layout">{children}</main>; }