"use client";

import * as React from "react";
import { Alert, Button, Field, HelperText, Label, PasswordInput, TextInput } from "@voicesense/ui";
import { authCopy, type AuthFormState, simulateAuthRequest } from "../../../lib/auth-client";
import { AuthShell } from "../AuthShell";

export default function ResetPasswordPage() {
  const [state, setState] = React.useState<AuthFormState>({ status: "idle" });
  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const token = String(form.get("token") ?? "");
    const password = String(form.get("password") ?? "");
    if (token.length < 32 || password.length < 12) return setState({ status: "error", message: "Token and 12+ character password are required." });
    setState({ status: "loading" });
    setState(await simulateAuthRequest("Password reset. You can now sign in."));
  }
  return <AuthShell title={authCopy.reset.title} description={authCopy.reset.description}><form className="auth-form" onSubmit={onSubmit}>{state.status === "error" ? <Alert variant="danger" title="Could not reset password">{state.message}</Alert> : null}{state.status === "success" ? <Alert variant="success" title="Password updated">{state.message}</Alert> : null}<Field><Label htmlFor="token">Reset token</Label><TextInput id="token" name="token" placeholder="Paste token from email" /></Field><Field><Label htmlFor="password">New password</Label><PasswordInput id="password" name="password" autoComplete="new-password" placeholder="Minimum 12 characters" /><HelperText>All active sessions should be reviewed after a password reset.</HelperText></Field><Button loading={state.status === "loading"} type="submit">Reset password</Button></form></AuthShell>;
}