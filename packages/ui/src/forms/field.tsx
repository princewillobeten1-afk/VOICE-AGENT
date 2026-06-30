import * as React from "react";
import * as LabelPrimitive from "@radix-ui/react-label";
import { cn } from "../utils";

export const Label = React.forwardRef<React.ElementRef<typeof LabelPrimitive.Root>, React.ComponentPropsWithoutRef<typeof LabelPrimitive.Root>>(({ className, ...props }, ref) => <LabelPrimitive.Root ref={ref} className={cn("vs-label", className)} {...props} />);
Label.displayName = "Label";
export function HelperText({ className, ...props }: React.HTMLAttributes<HTMLParagraphElement>) { return <p className={cn("vs-helper", className)} {...props} />; }
export function ErrorMessage({ className, ...props }: React.HTMLAttributes<HTMLParagraphElement>) { return <p className={cn("vs-error", className)} role="alert" {...props} />; }
export function Field({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) { return <div className={cn("vs-field", className)} {...props} />; }