"use client";

import * as React from "react";
import Link from "next/link";
import { Alert, Button, EmailInput, Field, Label } from "@voicesense/ui";
import { authCopy, type AuthFormState, simulateAuthRequest, validateEmail } from "../../../lib/auth-client";
import { AuthShell } from "../AuthShell";

export default function ForgotPasswordPage() {
  const [state, setState] = React.useState<AuthFormState>({ status: "idle" });
  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const email = String(new FormData(event.currentTarget).get("email") ?? "");
    if (!validateEmail(email)) return setState({ status: "error", message: "Enter a valid email." });
    setState({ status: "loading" });
    setState(await simulateAuthRequest("If this account exists, reset instructions will be sent."));
  }
  return <AuthShell title={authCopy.forgot.title} description={authCopy.forgot.description} footer={<p><Link href="/auth/signin">Back to sign in</Link></p>}><form className="auth-form" onSubmit={onSubmit}>{state.status === "error" ? <Alert variant="danger" title="Invalid email">{state.message}</Alert> : null}{state.status === "success" ? <Alert variant="success" title="Check your email">{state.message}</Alert> : null}<Field><Label htmlFor="email">Email</Label><EmailInput id="email" name="email" autoComplete="email" placeholder="you@company.com" /></Field><Button loading={state.status === "loading"} type="submit">Send reset link</Button></form></AuthShell>;
}