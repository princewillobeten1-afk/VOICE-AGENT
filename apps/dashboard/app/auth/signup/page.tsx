"use client";

import { useState, type FormEvent } from "react";
import Link from "next/link";
import { Alert, Button, EmailInput, Field, HelperText, Label, PasswordInput, TextInput } from "@voicesense/ui";
import { authCopy, realSignUp, type AuthFormState, validateEmail } from "../../../lib/auth-client";
import { AuthShell } from "../AuthShell";

export default function SignUpPage() {
  const [state, setState] = useState<AuthFormState>({ status: "idle" });

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const email = String(form.get("email") ?? "");
    const password = String(form.get("password") ?? "");
    const name = String(form.get("name") ?? "");
    const organization = String(form.get("organization") ?? "");
    if (!name || !organization || !validateEmail(email) || password.length < 12) {
      setState({ status: "error", message: "Provide your name, organization, valid email, and a 12+ character password." });
      return;
    }
    setState({ status: "loading" });
    const result = await realSignUp(name, email, password, organization);
    setState(result);
    if (result.status === "success") window.location.href = "/employees";
  }

  return (
    <AuthShell title={authCopy.signup.title} description={authCopy.signup.description} footer={<p>Already have an account? <Link href="/auth/signin">Sign in</Link></p>}>
      <form className="auth-form" onSubmit={onSubmit}>
        {state.status === "error" ? <Alert variant="danger" title="Check the form">{state.message}</Alert> : null}
        {state.status === "success" ? <Alert variant="success" title="Workspace ready">{state.message}</Alert> : null}
        <Button variant="outline" type="button" className="auth-google">Sign up with Google</Button>
        <div className="auth-divider"><span>or</span></div>
        <Field><Label htmlFor="name">Name</Label><TextInput id="name" name="name" autoComplete="name" placeholder="Ada Lovelace" /></Field>
        <Field><Label htmlFor="organization">Organization</Label><TextInput id="organization" name="organization" placeholder="Acme Co." /></Field>
        <Field><Label htmlFor="email">Work email</Label><EmailInput id="email" name="email" autoComplete="email" placeholder="you@company.com" /></Field>
        <Field><Label htmlFor="password">Password</Label><PasswordInput id="password" name="password" autoComplete="new-password" placeholder="Minimum 12 characters" /><HelperText>Use a strong password. VoiceSense stores only secure password hashes.</HelperText></Field>
        <Button loading={state.status === "loading"} type="submit">Create workspace</Button>
      </form>
    </AuthShell>
  );
}
