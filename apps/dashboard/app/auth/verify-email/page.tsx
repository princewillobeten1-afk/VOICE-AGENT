"use client";

import * as React from "react";
import { Alert, Button, Field, Label, TextInput } from "@voicesense/ui";
import { authCopy, type AuthFormState, simulateAuthRequest } from "../../../lib/auth-client";
import { AuthShell } from "../AuthShell";

export default function VerifyEmailPage() {
  const [state, setState] = React.useState<AuthFormState>({ status: "idle" });
  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const token = String(new FormData(event.currentTarget).get("token") ?? "");
    if (token.length < 32) return setState({ status: "error", message: "Paste the verification token from your email." });
    setState({ status: "loading" });
    setState(await simulateAuthRequest("Email verified. Production workspace access can now continue."));
  }
  return <AuthShell title={authCopy.verify.title} description={authCopy.verify.description}><form className="auth-form" onSubmit={onSubmit}>{state.status === "error" ? <Alert variant="danger" title="Verification failed">{state.message}</Alert> : null}{state.status === "success" ? <Alert variant="success" title="Email verified">{state.message}</Alert> : null}<Field><Label htmlFor="token">Verification token</Label><TextInput id="token" name="token" placeholder="Paste token from email" /></Field><Button loading={state.status === "loading"} type="submit">Verify email</Button></form></AuthShell>;
}