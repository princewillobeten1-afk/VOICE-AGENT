"use client";
import * as React from "react";
import * as TabsPrimitive from "@radix-ui/react-tabs";
import * as DropdownMenuPrimitive from "@radix-ui/react-dropdown-menu";
import { Command as CommandPrimitive } from "cmdk";
import { ChevronRight, Search } from "lucide-react";
import { Button } from "../base/button";
import { cn } from "../utils";

export interface NavItem { label: string; href?: string; icon?: React.ComponentType<{ size?: number }>; active?: boolean; }
export function Sidebar({ brand, items }: { brand: React.ReactNode; items: NavItem[] }) { return <aside className="vs-sidebar"><div className="vs-sidebar-brand">{brand}</div><nav className="vs-sidebar-nav">{items.map((item) => { const Icon = item.icon; return <a className={cn("vs-sidebar-item", item.active && "is-active")} href={item.href ?? "#"} key={item.label}>{Icon ? <Icon size={18} /> : null}<span>{item.label}</span></a>; })}</nav></aside>; }
export function TopNav({ title, actions }: { title: string; actions?: React.ReactNode }) { return <header className="vs-topnav"><h1>{title}</h1><div className="vs-topnav-actions">{actions}</div></header>; }
export function Breadcrumb({ items }: { items: { label: string; href?: string }[] }) { return <nav className="vs-breadcrumb" aria-label="Breadcrumb">{items.map((item, index) => <React.Fragment key={item.label}>{index > 0 ? <ChevronRight size={14} /> : null}{item.href ? <a href={item.href}>{item.label}</a> : <span>{item.label}</span>}</React.Fragment>)}</nav>; }
export const Tabs = TabsPrimitive.Root;
export const TabsList = React.forwardRef<React.ElementRef<typeof TabsPrimitive.List>, React.ComponentPropsWithoutRef<typeof TabsPrimitive.List>>(({ className, ...props }, ref) => <TabsPrimitive.List ref={ref} className={cn("vs-tabs-list", className)} {...props} />);
TabsList.displayName = "TabsList";
export const TabsTrigger = React.forwardRef<React.ElementRef<typeof TabsPrimitive.Trigger>, React.ComponentPropsWithoutRef<typeof TabsPrimitive.Trigger>>(({ className, ...props }, ref) => <TabsPrimitive.Trigger ref={ref} className={cn("vs-tabs-trigger", className)} {...props} />);
TabsTrigger.displayName = "TabsTrigger";
export const TabsContent = TabsPrimitive.Content;
export function Pagination({ page, pages, onPageChange }: { page: number; pages: number; onPageChange?: (page: number) => void }) { return <div className="vs-pagination"><Button variant="outline" size="sm" disabled={page <= 1} onClick={() => onPageChange?.(page - 1)}>Previous</Button><span>Page {page} of {pages}</span><Button variant="outline" size="sm" disabled={page >= pages} onClick={() => onPageChange?.(page + 1)}>Next</Button></div>; }
export const DropdownMenu = DropdownMenuPrimitive.Root;
export const DropdownMenuTrigger = DropdownMenuPrimitive.Trigger;
export function DropdownMenuContent({ className, ...props }: React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Content>) { return <DropdownMenuPrimitive.Portal><DropdownMenuPrimitive.Content className={cn("vs-menu-content", className)} {...props} /></DropdownMenuPrimitive.Portal>; }
export function DropdownMenuItem({ className, ...props }: React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Item>) { return <DropdownMenuPrimitive.Item className={cn("vs-menu-item", className)} {...props} />; }
export function CommandPalette({ items }: { items: { label: string; value: string }[] }) { return <CommandPrimitive className="vs-command"><div className="vs-command-search"><Search size={16} /><CommandPrimitive.Input placeholder="Search commands" /></div><CommandPrimitive.List>{items.map((item) => <CommandPrimitive.Item className="vs-command-item" key={item.value} value={item.value}>{item.label}</CommandPrimitive.Item>)}</CommandPrimitive.List></CommandPrimitive>; }