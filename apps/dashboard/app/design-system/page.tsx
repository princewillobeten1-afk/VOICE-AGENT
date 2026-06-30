"use client";

import * as React from "react";
import { Bot, Boxes, ChartSpline, Code2, Database, Home, MoreHorizontal, PhoneCall, Settings, ShieldCheck, Sparkles } from "lucide-react";
import {
  Alert,
  AreaChartCard,
  Avatar,
  Badge,
  BarChartCard,
  Breadcrumb,
  Button,
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  Checkbox,
  Combobox,
  CommandPalette,
  ContextMenu,
  ContextMenuContent,
  ContextMenuItem,
  ContextMenuTrigger,
  DataTable,
  Dialog,
  DialogContent,
  DialogTrigger,
  Drawer,
  DrawerContent,
  DrawerTrigger,
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  EmailInput,
  EmptyState,
  ErrorMessage,
  ErrorState,
  Field,
  HelperText,
  IconButton,
  KpiCard,
  Label,
  LineChartCard,
  LoadingState,
  MultiSelect,
  NumberInput,
  Pagination,
  PasswordInput,
  PhoneInput,
  PieChartCard,
  Popover,
  PopoverContent,
  PopoverTrigger,
  Progress,
  RadioGroup,
  RadioItem,
  SearchInput,
  Select,
  Separator,
  Sidebar,
  Skeleton,
  Switch,
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
  TextInput,
  Toast,
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
  TopNav,
} from "@voicesense/ui";

type AgentRow = { id: string; name: string; role: string; status: string; latency: string };

const selectOptions = [
  { label: "Voice runtime", value: "voice" },
  { label: "Knowledge search", value: "knowledge" },
  { label: "Workflow tools", value: "workflow" },
];

const tableRows: AgentRow[] = [
  { id: "agent-1", name: "Maya", role: "Customer Success", status: "Live", latency: "612 ms" },
  { id: "agent-2", name: "Atlas", role: "Sales Development", status: "Testing", latency: "708 ms" },
  { id: "agent-3", name: "Nova", role: "Support Triage", status: "Draft", latency: "--" },
  { id: "agent-4", name: "Orion", role: "Billing Ops", status: "Paused", latency: "841 ms" },
];

const chartData = [
  { day: "Mon", calls: 82, success: 61 },
  { day: "Tue", calls: 104, success: 79 },
  { day: "Wed", calls: 96, success: 72 },
  { day: "Thu", calls: 132, success: 101 },
  { day: "Fri", calls: 118, success: 94 },
];

export default function DesignSystemPage() {
  const [selected, setSelected] = React.useState(["voice", "knowledge"]);

  return (
    <main className="ds-page">
      <section className="ds-hero">
        <div>
          <p className="ds-kicker">VoiceSense design system</p>
          <h1>Reusable UI infrastructure for every VoiceSense surface.</h1>
          <p>Production-ready foundations for dashboard, developer, enterprise, and operational workflows.</p>
        </div>
        <Button><Sparkles size={16} />New component</Button>
      </section>

      <DesignSection title="Base actions" description="Buttons use shadcn-style variants with VoiceSense tokens.">
        <div className="ds-row">
          <Button>Primary</Button>
          <Button variant="secondary">Secondary</Button>
          <Button variant="outline">Outline</Button>
          <Button variant="ghost">Ghost</Button>
          <Button variant="destructive">Destructive</Button>
          <Button variant="success">Success</Button>
          <Button loading>Loading</Button>
          <IconButton variant="outline" aria-label="More options"><MoreHorizontal size={16} /></IconButton>
        </div>
      </DesignSection>

      <DesignSection title="Forms" description="Inputs, labels, validation, and selection controls share consistent focus and error states.">
        <div className="ds-grid three">
          <Field><Label>Text input</Label><TextInput placeholder="Employee name" /><HelperText>Use short human-readable names.</HelperText></Field>
          <Field><Label>Email</Label><EmailInput placeholder="team@company.com" /></Field>
          <Field><Label>Password</Label><PasswordInput placeholder="••••••••" /></Field>
          <Field><Label>Search</Label><SearchInput placeholder="Search knowledge" /></Field>
          <Field><Label>Number</Label><NumberInput placeholder="650" /></Field>
          <Field><Label>Phone</Label><PhoneInput placeholder="+1 555 0100" /></Field>
          <Field><Label>Error state</Label><TextInput invalid placeholder="Missing value" /><ErrorMessage>Instructions are required.</ErrorMessage></Field>
          <Field><Label>Select</Label><Select options={selectOptions} placeholder="Choose capability" /></Field>
          <Field><Label>Multi select</Label><MultiSelect options={selectOptions} value={selected} onChange={setSelected} /></Field>
        </div>
        <div className="ds-row">
          <label className="ds-inline"><Checkbox defaultChecked /> Allow recording</label>
          <RadioGroup className="ds-row" defaultValue="manual"><label className="ds-inline"><RadioItem value="manual" /> Manual approval</label><label className="ds-inline"><RadioItem value="auto" /> Auto approve</label></RadioGroup>
          <label className="ds-inline"><Switch defaultChecked /> Runtime enabled</label>
          <Combobox options={selectOptions} value={selected} onChange={setSelected} placeholder="Combobox" />
        </div>
      </DesignSection>

      <DesignSection title="Cards and feedback" description="Reusable display and status patterns for operational product surfaces.">
        <div className="ds-grid three">
          <Card variant="dashboard"><CardHeader><CardTitle>Dashboard card</CardTitle></CardHeader><CardContent><CardDescription>Primary dashboard surface with calm hierarchy.</CardDescription></CardContent></Card>
          <Card variant="agent"><CardHeader><CardTitle>AI agent card</CardTitle></CardHeader><CardContent><Badge variant="success">Live</Badge></CardContent></Card>
          <Card variant="knowledge"><CardHeader><CardTitle>Knowledge card</CardTitle></CardHeader><CardContent><Progress value={72} /></CardContent></Card>
          <Alert title="Provider connected">OpenAI adapter is available for testing.</Alert>
          <Alert variant="warning" title="Approval required">Refund workflow needs human review.</Alert>
          <Toast title="Saved" description="Design token changes were synced." />
        </div>
        <div className="ds-grid three">
          <EmptyState title="No tools connected" description="Connect a tool before enabling workflow automation." action={<Button variant="outline">Connect tool</Button>} />
          <LoadingState label="Loading components" />
          <ErrorState title="Could not load trace" description="The runtime trace request failed." onRetry={() => undefined} />
          <Skeleton className="ds-skeleton" />
        </div>
      </DesignSection>

      <DesignSection title="Navigation and overlays" description="Radix-backed primitives for keyboard-first platform workflows.">
        <div className="ds-grid two">
          <Sidebar brand="VoiceSense" items={[{ label: "Home", icon: Home, active: true }, { label: "Agents", icon: Bot }, { label: "Developers", icon: Code2 }, { label: "Security", icon: ShieldCheck }]} />
          <Card><CardContent><TopNav title="Workspace" actions={<Button variant="outline">Invite</Button>} /><Breadcrumb items={[{ label: "VoiceSense" }, { label: "Design system" }]} /><Separator /><Tabs defaultValue="one"><TabsList><TabsTrigger value="one">Overview</TabsTrigger><TabsTrigger value="two">Usage</TabsTrigger></TabsList><TabsContent value="one"><p className="ds-copy">Tabs organize related settings without changing page context.</p></TabsContent><TabsContent value="two"><p className="ds-copy">Use tabs for peer-level views.</p></TabsContent></Tabs><Separator /><Pagination page={1} pages={5} /></CardContent></Card>
        </div>
        <div className="ds-row">
          <DropdownMenu><DropdownMenuTrigger asChild><Button variant="outline">Dropdown</Button></DropdownMenuTrigger><DropdownMenuContent><DropdownMenuItem>View logs</DropdownMenuItem><DropdownMenuItem>Export</DropdownMenuItem></DropdownMenuContent></DropdownMenu>
          <Dialog><DialogTrigger asChild><Button variant="outline">Dialog</Button></DialogTrigger><DialogContent title="Dialog example"><p className="ds-copy">Use dialogs for focused confirmation or configuration.</p></DialogContent></Dialog>
          <Drawer><DrawerTrigger asChild><Button variant="outline">Drawer</Button></DrawerTrigger><DrawerContent title="Drawer example"><p className="ds-copy">Use drawers for contextual editing without losing page state.</p></DrawerContent></Drawer>
          <Popover><PopoverTrigger asChild><Button variant="outline">Popover</Button></PopoverTrigger><PopoverContent><p className="ds-copy">Compact contextual information.</p></PopoverContent></Popover>
          <TooltipProvider><Tooltip><TooltipTrigger asChild><Button variant="outline">Tooltip</Button></TooltipTrigger><TooltipContent>Helpful detail</TooltipContent></Tooltip></TooltipProvider>
          <ContextMenu><ContextMenuTrigger asChild><Button variant="outline">Context menu</Button></ContextMenuTrigger><ContextMenuContent><ContextMenuItem>Inspect</ContextMenuItem><ContextMenuItem>Duplicate</ContextMenuItem></ContextMenuContent></ContextMenu>
        </div>
        <CommandPalette items={[{ label: "Create employee", value: "create" }, { label: "Open runtime logs", value: "logs" }, { label: "Manage API keys", value: "api" }]} />
      </DesignSection>

      <DesignSection title="Enterprise data table" description="Search, sort, pagination, selection, and bulk action slots are built in.">
        <DataTable<AgentRow>
          data={tableRows}
          bulkActions={<Button variant="outline" size="sm">Archive</Button>}
          columns={[
            { key: "name", header: "Name", sortable: true, render: (row) => <span className="ds-person"><Avatar name={row.name} />{row.name}</span> },
            { key: "role", header: "Role", sortable: true },
            { key: "status", header: "Status", sortable: true, render: (row) => <Badge variant={row.status === "Live" ? "success" : row.status === "Testing" ? "warning" : "neutral"}>{row.status}</Badge> },
            { key: "latency", header: "Latency", sortable: true },
          ]}
        />
      </DesignSection>

      <DesignSection title="Charts" description="Standardized wrappers for VoiceSense analytics and observability surfaces.">
        <div className="ds-grid two">
          <KpiCard label="Resolved conversations" value="79.4%" delta="+6.1%" />
          <KpiCard label="Avg latency" value="642 ms" delta="-18%" />
          <LineChartCard title="Voice sessions" data={chartData} xKey="day" yKey="calls" />
          <AreaChartCard title="Successful outcomes" data={chartData} xKey="day" yKey="success" />
          <BarChartCard title="Daily calls" data={chartData} xKey="day" yKey="calls" />
          <PieChartCard title="Channel mix" data={[{ name: "Phone", value: 46 }, { name: "Chat", value: 32 }, { name: "Email", value: 22 }]} nameKey="name" dataKey="value" />
        </div>
      </DesignSection>

      <DesignSection title="Layouts" description="Composable layout primitives keep product surfaces consistent.">
        <div className="ds-grid three">
          <Card><CardContent><Boxes size={22} /><CardTitle>Page layout</CardTitle><CardDescription>Default constrained page rhythm.</CardDescription></CardContent></Card>
          <Card><CardContent><Settings size={22} /><CardTitle>Settings layout</CardTitle><CardDescription>Side navigation plus focused content.</CardDescription></CardContent></Card>
          <Card><CardContent><PhoneCall size={22} /><CardTitle>Dashboard layout</CardTitle><CardDescription>Navigation plus operational workspace.</CardDescription></CardContent></Card>
          <Card><CardContent><Database size={22} /><CardTitle>Auth layout</CardTitle><CardDescription>Centered authentication and onboarding.</CardDescription></CardContent></Card>
          <Card><CardContent><ChartSpline size={22} /><CardTitle>Centered layout</CardTitle><CardDescription>Empty, loading, and focused utility views.</CardDescription></CardContent></Card>
        </div>
      </DesignSection>
    </main>
  );
}

function DesignSection({ title, description, children }: { title: string; description: string; children: React.ReactNode }) {
  return <section className="ds-section"><div className="ds-section-head"><h2>{title}</h2><p>{description}</p></div>{children}</section>;
}