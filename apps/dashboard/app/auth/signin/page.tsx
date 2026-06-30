"use client";

import * as React from "react";
import Link from "next/link";
import { Alert, Button, EmailInput, ErrorMessage, Field, HelperText, Label, PasswordInput } from "@voicesense/ui";
import { authCopy, type AuthFormState, simulateAuthRequest, validateEmail } from "../../../lib/auth-client";
import { AuthShell } from "../AuthShell";

export default function SignInPage() {
  const [state, setState] = React.useState<AuthFormState>({ status: "idle" });

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const email = String(form.get("email") ?? "");
    const password = String(form.get("password") ?? "");
    if (!validateEmail(email) || !password) {
      setState({ status: "error", message: "Enter a valid email and password." });
      return;
    }
    setState({ status: "loading" });
    setState(await simulateAuthRequest("Signed in. The API endpoint is /v1/auth/signin."));
  }

  return (
    <AuthShell title={authCopy.signin.title} description={authCopy.signin.description} footer={<p>New to VoiceSense? <Link href="/auth/signup">Create a workspace</Link></p>}>
      <form className="auth-form" onSubmit={onSubmit}>
        {state.status === "error" ? <Alert variant="danger" title="Could not sign in">{state.message}</Alert> : null}
        {state.status === "success" ? <Alert variant="success" title="Ready for API wiring">{state.message}</Alert> : null}
        <Button variant="outline" type="button" className="auth-google">Continue with Google</Button>
        <div className="auth-divider"><span>or</span></div>
        <Field><Label htmlFor="email">Email</Label><EmailInput id="email" name="email" autoComplete="email" placeholder="you@company.com" /></Field>
        <Field><Label htmlFor="password">Password</Label><PasswordInput id="password" name="password" autoComplete="current-password" placeholder="Enter your password" /><HelperText><Link href="/auth/forgot-password">Forgot password?</Link></HelperText></Field>
        <Button loading={state.status === "loading"} type="submit">Sign in</Button>
        <ErrorMessage>Protected routes will require a valid access token and active session.</ErrorMessage>
      </form>
    </AuthShell>
  );
}