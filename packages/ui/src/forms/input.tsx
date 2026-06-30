import * as React from "react";
import { Search } from "lucide-react";
import { cn } from "../utils";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> { invalid?: boolean; leadingIcon?: React.ReactNode; }
export const Input = React.forwardRef<HTMLInputElement, InputProps>(({ className, invalid, leadingIcon, type = "text", ...props }, ref) => (
  <span className={cn("vs-input-wrap", invalid && "is-invalid", className)}>{leadingIcon ? <span className="vs-input-icon">{leadingIcon}</span> : null}<input className="vs-input" data-invalid={invalid ? "true" : undefined} ref={ref} type={type} {...props} /></span>
));
Input.displayName = "Input";
export const TextInput = Input;
export const PasswordInput = React.forwardRef<HTMLInputElement, Omit<InputProps, "type">>((props, ref) => <Input ref={ref} type="password" {...props} />);
PasswordInput.displayName = "PasswordInput";
export const EmailInput = React.forwardRef<HTMLInputElement, Omit<InputProps, "type">>((props, ref) => <Input ref={ref} type="email" {...props} />);
EmailInput.displayName = "EmailInput";
export const NumberInput = React.forwardRef<HTMLInputElement, Omit<InputProps, "type">>((props, ref) => <Input ref={ref} type="number" {...props} />);
NumberInput.displayName = "NumberInput";
export const PhoneInput = React.forwardRef<HTMLInputElement, Omit<InputProps, "type">>((props, ref) => <Input ref={ref} type="tel" {...props} />);
PhoneInput.displayName = "PhoneInput";
export const SearchInput = React.forwardRef<HTMLInputElement, Omit<InputProps, "type" | "leadingIcon">>((props, ref) => <Input ref={ref} type="search" leadingIcon={<Search size={16} />} {...props} />);
SearchInput.displayName = "SearchInput";