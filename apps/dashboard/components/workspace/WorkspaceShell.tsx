"use client";

import * as React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Bell, ChevronDown, Command, Menu, Moon, PanelLeftClose, PanelLeftOpen, Search, Sun, UserCircle2, X } from "lucide-react";
import { Badge, Button, IconButton } from "@voicesense/ui";
import { breadcrumbs, commandSuggestions, topUtilityItems, workspaceGroups, workspaceOrgs } from "../../lib/workspace-data";
import { drawerNotifications } from "../../lib/notification-data";

export function WorkspaceShell({ children, utilityPanel }: { children: React.ReactNode; utilityPanel?: React.ReactNode }) {
  const [collapsed, setCollapsed] = React.useState(false);
  const [mobileOpen, setMobileOpen] = React.useState(false);
  const [theme, setTheme] = React.useState<"light" | "dark">("light");
  const [notificationOpen, setNotificationOpen] = React.useState(false);
  const pathname = usePathname();

  React.useEffect(() => {
    document.documentElement.dataset.theme = theme;
  }, [theme]);

  return (
    <div className={`ws-shell ${collapsed ? "is-collapsed" : ""}`}>
      <a className="ws-skip" href="#workspace-content">Skip to content</a>
      <aside className={`ws-sidebar ${mobileOpen ? "is-open" : ""}`} aria-label="Workspace navigation">
        <div className="ws-sidebar-head">
          <Link className="ws-brand" href="/" aria-label="VoiceSense dashboard">
            <span>VS</span>
            <strong>VoiceSense</strong>
          </Link>
          <IconButton className="ws-mobile-close" variant="ghost" aria-label="Close navigation" onClick={() => setMobileOpen(false)}><X size={17} /></IconButton>
        </div>

        <button className="ws-org-switcher" type="button" aria-label="Switch organization">
          <span><strong>{workspaceOrgs[0].name}</strong><small>{workspaceOrgs[0].plan} workspace</small></span>
          <ChevronDown size={16} />
        </button>

        <button className="ws-search-shortcut" type="button" aria-label="Open workspace search with Control K">
          <Search size={16} />
          <span>Search workspace</span>
          <kbd aria-label="Control K">Ctrl K</kbd>
        </button>

        <nav className="ws-nav" aria-label="Main modules">
          {workspaceGroups.map((group) => (
            <div className="ws-nav-group" key={group.label}>
              <p>{group.label}</p>
              {group.items.map((item) => (
                <div className="ws-nav-cluster" key={item.label}>
                  <Link className={`ws-nav-item ${(pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href))) ? "is-active" : ""}`} href={item.href} aria-current={(pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href))) ? "page" : undefined}>
                    <item.icon size={18} />
                    <span>{item.label}</span>
                  </Link>
                  {item.children && !collapsed ? <div className="ws-nav-children">{item.children.map((child) => <a href="#" key={child}>{child}</a>)}</div> : null}
                </div>
              ))}
            </div>
          ))}
        </nav>

        <div className="ws-sidebar-footer">
          <button className="ws-collapse" type="button" onClick={() => setCollapsed((value) => !value)} aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}>
            {collapsed ? <PanelLeftOpen size={17} /> : <PanelLeftClose size={17} />}
            <span>{collapsed ? "Expand" : "Collapse"}</span>
          </button>
        </div>
      </aside>

      {mobileOpen ? <button className="ws-scrim" aria-label="Close navigation overlay" onClick={() => setMobileOpen(false)} /> : null}

      <div className="ws-main-area">
        <header className="ws-topbar">
          <div className="ws-topbar-left">
            <IconButton className="ws-mobile-menu" variant="outline" aria-label="Open navigation" onClick={() => setMobileOpen(true)}><Menu size={18} /></IconButton>
            <nav className="ws-breadcrumbs" aria-label="Breadcrumbs">
              {breadcrumbs.map((item, index) => <React.Fragment key={item}>{index > 0 ? <span>/</span> : null}<a href="#">{item}</a></React.Fragment>)}
            </nav>
          </div>

          <div className="ws-global-search" role="search">
            <Search size={16} />
            <input aria-label="Global search" placeholder="Search employees, calls, docs, workflows" />
            <kbd aria-label="Control K">Ctrl K</kbd>
          </div>

          <div className="ws-topbar-actions">
            <Button variant="outline" size="sm" aria-label="Open command palette"><Command size={15} />Command</Button>
            <button className="ws-notification-button" type="button" aria-label="Open notifications" aria-expanded={notificationOpen} onClick={() => setNotificationOpen((value) => !value)}><Bell size={17} /><span>4</span></button>
            <button className="ws-org-pill" type="button"><span>{workspaceOrgs[0].name}</span><ChevronDown size={14} /></button>
            <IconButton variant="outline" aria-label="Toggle theme" onClick={() => setTheme(theme === "light" ? "dark" : "light")}>{theme === "light" ? <Moon size={17} /> : <Sun size={17} />}</IconButton>
            <button className="ws-user-menu" type="button" aria-label="Open user menu"><UserCircle2 size={20} /><span>Ada</span><ChevronDown size={14} /></button>
            {notificationOpen ? <div className="ws-notification-drawer" role="dialog" aria-modal="false" aria-label="Notification preview"><div className="ws-notification-head"><strong>Notifications</strong><Badge>4 unread</Badge></div><div className="ws-notification-list">{drawerNotifications.map((item) => <a href="/notifications" key={item.title}><item.icon size={16} /><span><strong>{item.title}</strong><small>{item.time}</small></span></a>)}</div><div className="ws-notification-foot"><a href="/notifications">Open center</a><a href="/settings/notifications">Preferences</a></div></div> : null}
          </div>
        </header>

        <div className="ws-content-shell">
          <main id="workspace-content" className="ws-content" tabIndex={-1}>{children}</main>
          <aside className="ws-utility-panel" aria-label="Utility panel">
            {utilityPanel ?? <UtilityPanel />}
          </aside>
        </div>
      </div>
    </div>
  );
}

function UtilityPanel() {
  return <div className="ws-utility-stack"><div><p className="ws-kicker">Command suggestions</p>{commandSuggestions.map((item) => <button className="ws-command-suggestion" type="button" key={item}>{item}</button>)}</div><div><p className="ws-kicker">Workspace health</p>{topUtilityItems.map((item) => <div className="ws-utility-row" key={item.label}><item.icon size={16} /><span>{item.label}</span><strong>Ready</strong></div>)}</div></div>;
}