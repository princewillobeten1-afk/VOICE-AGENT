import * as React from "react";
import { cn } from "../utils";
export function Avatar({ name, className }: { name: string; className?: string }) { return <span className={cn("vs-avatar", className)} aria-label={name}>{name.slice(0, 2).toUpperCase()}</span>; }
export function Separator() { return <hr className="vs-separator" />; }