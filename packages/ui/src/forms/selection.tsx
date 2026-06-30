"use client";
import * as React from "react";
import * as CheckboxPrimitive from "@radix-ui/react-checkbox";
import * as RadioGroupPrimitive from "@radix-ui/react-radio-group";
import * as SwitchPrimitive from "@radix-ui/react-switch";
import * as SelectPrimitive from "@radix-ui/react-select";
import * as PopoverPrimitive from "@radix-ui/react-popover";
import { Check, ChevronsUpDown } from "lucide-react";
import { Button } from "../base/button";
import { cn } from "../utils";

export const Checkbox = React.forwardRef<React.ElementRef<typeof CheckboxPrimitive.Root>, React.ComponentPropsWithoutRef<typeof CheckboxPrimitive.Root>>(({ className, ...props }, ref) => <CheckboxPrimitive.Root ref={ref} className={cn("vs-checkbox", className)} {...props}><CheckboxPrimitive.Indicator><Check size={14} /></CheckboxPrimitive.Indicator></CheckboxPrimitive.Root>);
Checkbox.displayName = "Checkbox";
export const RadioGroup = RadioGroupPrimitive.Root;
export const RadioItem = React.forwardRef<React.ElementRef<typeof RadioGroupPrimitive.Item>, React.ComponentPropsWithoutRef<typeof RadioGroupPrimitive.Item>>(({ className, ...props }, ref) => <RadioGroupPrimitive.Item ref={ref} className={cn("vs-radio", className)} {...props}><RadioGroupPrimitive.Indicator className="vs-radio-indicator" /></RadioGroupPrimitive.Item>);
RadioItem.displayName = "RadioItem";
export const Switch = React.forwardRef<React.ElementRef<typeof SwitchPrimitive.Root>, React.ComponentPropsWithoutRef<typeof SwitchPrimitive.Root>>(({ className, ...props }, ref) => <SwitchPrimitive.Root ref={ref} className={cn("vs-switch", className)} {...props}><SwitchPrimitive.Thumb className="vs-switch-thumb" /></SwitchPrimitive.Root>);
Switch.displayName = "Switch";

export interface SelectOption { label: string; value: string; }
export interface SelectProps { value?: string; defaultValue?: string; onValueChange?: (value: string) => void; placeholder?: string; options: SelectOption[]; disabled?: boolean; }
export function Select({ options, placeholder = "Select", ...props }: SelectProps) {
  return <SelectPrimitive.Root {...props}><SelectPrimitive.Trigger className="vs-select"><SelectPrimitive.Value placeholder={placeholder} /><ChevronsUpDown size={16} /></SelectPrimitive.Trigger><SelectPrimitive.Portal><SelectPrimitive.Content className="vs-select-content" position="popper"><SelectPrimitive.Viewport>{options.map((option) => <SelectPrimitive.Item className="vs-select-item" value={option.value} key={option.value}><SelectPrimitive.ItemText>{option.label}</SelectPrimitive.ItemText></SelectPrimitive.Item>)}</SelectPrimitive.Viewport></SelectPrimitive.Content></SelectPrimitive.Portal></SelectPrimitive.Root>;
}
export function MultiSelect({ options, value, onChange, placeholder = "Select options" }: { options: SelectOption[]; value: string[]; onChange: (value: string[]) => void; placeholder?: string; }) {
  const selected = options.filter((option) => value.includes(option.value));
  return <PopoverPrimitive.Root><PopoverPrimitive.Trigger asChild><Button variant="outline" className="vs-combobox-trigger"><span>{selected.length ? selected.map((item) => item.label).join(", ") : placeholder}</span><ChevronsUpDown size={16} /></Button></PopoverPrimitive.Trigger><PopoverPrimitive.Content className="vs-popover-content" align="start"><div className="vs-option-stack">{options.map((option) => { const checked = value.includes(option.value); return <button className="vs-option-row" key={option.value} onClick={() => onChange(checked ? value.filter((item) => item !== option.value) : [...value, option.value])} type="button"><span className={cn("vs-option-check", checked && "is-selected")}>{checked ? <Check size={13} /> : null}</span>{option.label}</button>; })}</div></PopoverPrimitive.Content></PopoverPrimitive.Root>;
}
export function Combobox(props: React.ComponentProps<typeof MultiSelect>) { return <MultiSelect {...props} />; }