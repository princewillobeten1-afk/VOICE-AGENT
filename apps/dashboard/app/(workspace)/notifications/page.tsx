"use client";

import { Archive, CheckCheck, ChevronLeft, ChevronRight, Search, SlidersHorizontal, Trash2 } from "lucide-react";
import { Badge, Button, EmptyState, ErrorState, IconButton, SearchInput, Skeleton } from "@voicesense/ui";
import { eventLogs, notificationFilters, notifications, notificationStats } from "../../../lib/notification-data";

export default function NotificationsPage() {
  return (
    <div className="notify-page">
      <header className="notify-hero">
        <div><p className="ws-kicker">Notification center</p><h1>Track important workspace updates, event deliveries, and actions that need attention.</h1><p>Notifications are generated from platform events, keeping business modules loosely coupled from delivery channels.</p></div>
        <div className="notify-actions"><Button><CheckCheck size={16} />Mark all read</Button><Button variant="outline"><SlidersHorizontal size={16} />Filters</Button></div>
      </header>

      <section className="notify-stat-grid" aria-label="Notification summary">{notificationStats.map((stat) => <article className={`notify-card notify-stat ${stat.tone}`} key={stat.label}><stat.icon size={18} /><p>{stat.label}</p><strong>{stat.value}</strong><span>{stat.detail}</span></article>)}</section>

      <section className="notify-toolbar"><div className="notify-filter-row">{notificationFilters.map((filter) => <button className={filter === "All" ? "is-active" : ""} type="button" key={filter}>{filter}</button>)}</div><div className="notify-search"><SearchInput placeholder="Search notifications" /><Button variant="outline" size="sm"><Search size={15} />Search</Button></div></section>

      <section className="notify-main-grid">
        <article className="notify-card"><div className="notify-panel-head"><h2>Notifications</h2><Badge>{notifications.filter((item) => item.status === "Unread").length} unread</Badge></div><div className="notify-list">{notifications.map((item) => <div className={`notify-row ${item.status === "Unread" ? "is-unread" : ""}`} key={item.title}><span className="notify-row-icon"><item.icon size={18} /></span><div><div className="notify-row-title"><strong>{item.title}</strong><Badge variant={item.severity === "Success" ? "success" : item.severity === "Warning" ? "warning" : item.severity === "Error" ? "danger" : "info"}>{item.severity}</Badge></div><p>{item.body}</p><small>{item.category} - {item.time}</small></div><div className="notify-row-actions"><IconButton variant="ghost" size="sm" aria-label="Archive notification"><Archive size={15} /></IconButton><IconButton variant="ghost" size="sm" aria-label="Delete notification"><Trash2 size={15} /></IconButton></div></div>)}</div><div className="notify-pagination"><Button variant="outline" size="sm"><ChevronLeft size={15} />Previous</Button><span>Page 1 of 8</span><Button variant="outline" size="sm">Next<ChevronRight size={15} /></Button></div></article>

        <aside className="notify-side-stack"><article className="notify-card"><div className="notify-panel-head"><h2>Event processing</h2><Badge variant="success">Healthy</Badge></div><div className="notify-event-list">{eventLogs.map((log) => <div className="notify-event-row" key={log.event}><div><strong>{log.event}</strong><p>{log.subscriber}</p></div><Badge variant={log.status === "Processed" ? "success" : "warning"}>{log.status}</Badge><small>{log.latency} - {log.retries} retries</small></div>)}</div></article><EmptyState title="No archived notifications" description="Archived notifications remain searchable without crowding active work." action={<Button variant="outline" size="sm"><Archive size={15} />Open archive</Button>} /><div className="notify-card"><Skeleton className="notify-skeleton" /><Skeleton className="notify-skeleton-line" /><Skeleton className="notify-skeleton-line" /></div><ErrorState title="Delivery queue delayed" description="Queue health states keep operators informed without hiding the rest of the notification center." onRetry={() => undefined} /></aside>
      </section>
    </div>
  );
}