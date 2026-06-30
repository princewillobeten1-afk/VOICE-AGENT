"use client";

import { Bell, Clock, Mail, Moon, Save } from "lucide-react";
import { Badge, Button, Switch } from "@voicesense/ui";
import { categoryPreferences, preferenceChannels } from "../../../../lib/notification-data";

export default function NotificationPreferencesPage() {
  return (
    <div className="notify-page">
      <header className="notify-hero">
        <div><p className="ws-kicker">Notification preferences</p><h1>Control how VoiceSense communicates workspace events, alerts, and team activity.</h1><p>Preferences are channel-aware and category-aware so future email, SMS, push, Slack, Discord, WhatsApp, and webhook delivery can reuse the same policy model.</p></div>
        <div className="notify-actions"><Button><Save size={16} />Save preferences</Button></div>
      </header>

      <section className="notify-pref-grid">
        <article className="notify-card"><div className="notify-panel-head"><h2>Channels</h2><Badge>5 configured</Badge></div><div className="notify-pref-list">{preferenceChannels.map((channel) => <div className="notify-pref-row" key={channel.label}><div><strong>{channel.label}</strong><p>{channel.description}</p><Badge variant={channel.status === "Implemented" ? "success" : channel.status === "Architecture ready" ? "info" : "neutral"}>{channel.status}</Badge></div><Switch checked={channel.enabled} /></div>)}</div></article>

        <article className="notify-card"><div className="notify-panel-head"><h2>Frequency and quiet hours</h2><Clock size={18} /></div><div className="notify-form-grid"><label><span>Default frequency</span><select defaultValue="instant"><option value="instant">Instant</option><option value="hourly">Hourly digest</option><option value="daily">Daily digest</option><option value="weekly">Weekly digest</option></select></label><label><span>Quiet hours start</span><input defaultValue="22:00" /></label><label><span>Quiet hours end</span><input defaultValue="07:00" /></label><label><span>Timezone</span><input defaultValue="Africa/Lagos" /></label></div><div className="notify-pref-note"><Moon size={18} /><p>Critical security and billing events can bypass quiet hours when policy requires immediate delivery.</p></div></article>
      </section>

      <section className="notify-pref-grid two"><article className="notify-card"><div className="notify-panel-head"><h2>Categories</h2><Bell size={18} /></div><div className="notify-pref-list">{categoryPreferences.map((item) => <div className="notify-pref-row" key={item.label}><div><strong>{item.label}</strong><p>{item.description}</p></div><Badge>{item.value}</Badge></div>)}</div></article><article className="notify-card"><div className="notify-panel-head"><h2>Template readiness</h2><Mail size={18} /></div><div className="notify-template-box"><strong>Reusable templates</strong><p>Templates support variables like user name, organization name, agent name, timestamp, and action details. Channel-specific renderers can reuse the same event payload contract.</p><pre>{`{{user_name}} created {{action_details}} in {{organization_name}} at {{timestamp}}.`}</pre></div></article></section>
    </div>
  );
}