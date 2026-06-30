import Link from "next/link";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@voicesense/ui";

export function AuthShell({ title, description, children, footer }: { title: string; description: string; children: React.ReactNode; footer?: React.ReactNode }) {
  return (
    <main className="auth-page">
      <section className="auth-brand-panel" aria-label="VoiceSense identity">
        <Link className="auth-brand" href="/">
          <span>VS</span>
          <strong>VoiceSense</strong>
        </Link>
        <div>
          <p className="auth-kicker">Identity foundation</p>
          <h1>Secure access for multi-tenant AI employee workspaces.</h1>
          <p>Built for organizations, teams, roles, sessions, and future enterprise controls from the beginning.</p>
        </div>
      </section>
      <section className="auth-form-panel">
        <Card className="auth-card">
          <CardHeader>
            <CardTitle>{title}</CardTitle>
            <CardDescription>{description}</CardDescription>
          </CardHeader>
          <CardContent>{children}</CardContent>
        </Card>
        {footer ? <div className="auth-footer">{footer}</div> : null}
      </section>
    </main>
  );
}