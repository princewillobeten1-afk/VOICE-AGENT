"use client";
import * as React from "react";
import * as DialogPrimitive from "@radix-ui/react-dialog";
import * as PopoverPrimitive from "@radix-ui/react-popover";
import * as TooltipPrimitive from "@radix-ui/react-tooltip";
import * as ContextMenuPrimitive from "@radix-ui/react-context-menu";
import { X } from "lucide-react";
import { IconButton } from "../base/button";
import { cn } from "../utils";

export const Dialog = DialogPrimitive.Root;
export const DialogTrigger = DialogPrimitive.Trigger;
export function DialogContent({ title, children }: { title: string; children: React.ReactNode }) { return <DialogPrimitive.Portal><DialogPrimitive.Overlay className="vs-overlay" /><DialogPrimitive.Content className="vs-dialog"><div className="vs-dialog-header"><DialogPrimitive.Title>{title}</DialogPrimitive.Title><DialogPrimitive.Close asChild><IconButton variant="ghost" aria-label="Close dialog"><X size={16} /></IconButton></DialogPrimitive.Close></div>{children}</DialogPrimitive.Content></DialogPrimitive.Portal>; }
export const Drawer = Dialog;
export const DrawerTrigger = DialogTrigger;
export function DrawerContent({ title, children }: { title: string; children: React.ReactNode }) { return <DialogPrimitive.Portal><DialogPrimitive.Overlay className="vs-overlay" /><DialogPrimitive.Content className="vs-drawer"><div className="vs-dialog-header"><DialogPrimitive.Title>{title}</DialogPrimitive.Title><DialogPrimitive.Close asChild><IconButton variant="ghost" aria-label="Close drawer"><X size={16} /></IconButton></DialogPrimitive.Close></div>{children}</DialogPrimitive.Content></DialogPrimitive.Portal>; }
export const Popover = PopoverPrimitive.Root;
export const PopoverTrigger = PopoverPrimitive.Trigger;
export function PopoverContent({ className, ...props }: React.ComponentPropsWithoutRef<typeof PopoverPrimitive.Content>) { return <PopoverPrimitive.Portal><PopoverPrimitive.Content className={cn("vs-popover-content", className)} {...props} /></PopoverPrimitive.Portal>; }
export const TooltipProvider = TooltipPrimitive.Provider;
export const Tooltip = TooltipPrimitive.Root;
export const TooltipTrigger = TooltipPrimitive.Trigger;
export function TooltipContent({ className, ...props }: React.ComponentPropsWithoutRef<typeof TooltipPrimitive.Content>) { return <TooltipPrimitive.Portal><TooltipPrimitive.Content className={cn("vs-tooltip", className)} {...props} /></TooltipPrimitive.Portal>; }
export const ContextMenu = ContextMenuPrimitive.Root;
export const ContextMenuTrigger = ContextMenuPrimitive.Trigger;
export function ContextMenuContent({ className, ...props }: React.ComponentPropsWithoutRef<typeof ContextMenuPrimitive.Content>) { return <ContextMenuPrimitive.Portal><ContextMenuPrimitive.Content className={cn("vs-menu-content", className)} {...props} /></ContextMenuPrimitive.Portal>; }
export function ContextMenuItem({ className, ...props }: React.ComponentPropsWithoutRef<typeof ContextMenuPrimitive.Item>) { return <ContextMenuPrimitive.Item className={cn("vs-menu-item", className)} {...props} />; }