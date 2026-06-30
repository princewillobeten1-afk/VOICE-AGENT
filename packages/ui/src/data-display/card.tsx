import * as React from "react";
import { cn } from "../utils";
export interface CardProps extends React.HTMLAttributes<HTMLDivElement> { variant?: "default" | "dashboard" | "stat" | "agent" | "knowledge" | "settings"; }
export function Card({ className, variant = "default", ...props }: CardProps) { return <div className={cn("vs-card", `vs-card-${variant}`, className)} {...props} />; }
export function CardHeader({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) { return <div className={cn("vs-card-header", className)} {...props} />; }
export function CardTitle({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) { return <h3 className={cn("vs-card-title", className)} {...props} />; }
export function CardDescription({ className, ...props }: React.HTMLAttributes<HTMLParagraphElement>) { return <p className={cn("vs-card-description", className)} {...props} />; }
export function CardContent({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) { return <div className={cn("vs-card-content", className)} {...props} />; }