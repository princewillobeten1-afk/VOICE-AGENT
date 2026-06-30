import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { Loader2 } from "lucide-react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "../utils";

export const buttonVariants = cva("vs-button", {
  variants: {
    variant: { primary: "vs-button-primary", secondary: "vs-button-secondary", ghost: "vs-button-ghost", outline: "vs-button-outline", destructive: "vs-button-destructive", success: "vs-button-success" },
    size: { sm: "vs-button-sm", md: "vs-button-md", lg: "vs-button-lg", icon: "vs-button-icon" }
  },
  defaultVariants: { variant: "primary", size: "md" }
});

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>, VariantProps<typeof buttonVariants> { asChild?: boolean; loading?: boolean; }

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(({ className, variant, size, asChild = false, loading = false, disabled, children, ...props }, ref) => {
  const Comp = asChild ? Slot : "button";
  return <Comp className={cn(buttonVariants({ variant, size }), className)} ref={ref} disabled={disabled || loading} {...props}>{loading ? <Loader2 className="vs-spin" size={16} aria-hidden="true" /> : null}{children}</Comp>;
});
Button.displayName = "Button";

export function IconButton({ children, "aria-label": ariaLabel, ...props }: ButtonProps) {
  return <Button size="icon" aria-label={ariaLabel} {...props}>{children}</Button>;
}