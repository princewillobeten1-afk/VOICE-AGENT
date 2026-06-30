# VoiceSense Design Language

VoiceSense is a premium AI Employee Platform for businesses, developers, agencies, and enterprise teams. The design language must support a product that feels calm, intelligent, reliable, and powerful without becoming visually loud or trend-dependent.

This document defines the brand identity and visual system that should guide every future VoiceSense interface, design system component, product flow, marketing asset, and developer experience surface.

## Brand Identity

### Brand Personality

VoiceSense should feel like a composed expert sitting beside the business: intelligent, precise, calm under pressure, and deeply capable. The brand should communicate technical excellence without becoming cold, and sophistication without becoming decorative.

VoiceSense is:

- Premium, but not flashy.
- Intelligent, but not mysterious.
- Enterprise-ready, but not bureaucratic.
- Developer-friendly, but not overly technical in customer-facing surfaces.
- Calm, but not passive.
- Fast, but not frantic.

### Mission

VoiceSense helps organizations create, deploy, and manage AI employees that can communicate, reason, act, remember, and collaborate across business workflows.

### Vision

VoiceSense aims to become the operating system for AI employees: a trusted platform where businesses can build reliable AI workers for voice, chat, email, messaging, scheduling, knowledge work, tool usage, and workflow automation.

### Tone of Voice

The VoiceSense tone should be clear, confident, concise, and helpful. It should avoid hype and vague AI language. Use practical language that explains what is happening, what the user can do next, and why it matters.

Use:

- Direct, plain explanations.
- Confident but measured claims.
- Product language that emphasizes outcomes, reliability, and control.
- Human wording for complex technical states.

Avoid:

- Overpromising autonomy or perfection.
- Buzzwords without product meaning.
- Cute system messages in serious workflows.
- Fear-based enterprise language.

### Core Values

- Trust: Users should always understand what an AI employee is doing and why.
- Clarity: Every interface should reduce ambiguity.
- Control: Humans define boundaries, approvals, tools, and escalation paths.
- Reliability: VoiceSense must make quality, latency, failures, and outcomes observable.
- Extensibility: The platform should welcome APIs, providers, workflows, and integrations.
- Craft: Every detail should feel intentionally designed and engineered.

## Visual Direction

### Design Philosophy

VoiceSense should look like a serious work platform with exceptional taste. The interface should prioritize clarity, density, speed, and confidence. It should be beautiful because it is composed, not because it is decorative.

The product should feel suitable for daily operational use by teams who manage real customer interactions, sensitive business data, and production AI systems.

### Overall Aesthetic

The aesthetic should be:

- Clean and restrained.
- Warm-neutral rather than sterile.
- Structured and highly scannable.
- Low-noise, with strong hierarchy.
- Precise in spacing, typography, and alignment.
- Premium through material quality, not visual effects.

### Inspiration Sources

Use these products as directional references, not templates to copy:

- Stripe: clarity, developer trust, documentation quality.
- Linear: speed, focus, refined interaction patterns.
- Notion: approachable structure and information organization.
- Figma: collaborative product density and tool confidence.
- Vercel: developer-first polish and technical credibility.
- Apple: restraint, hierarchy, and material discipline.

### Do's

- Use whitespace to create calm and comprehension.
- Make dashboards dense enough for real operators.
- Use clear section hierarchy and consistent alignment.
- Prefer useful visual distinction over decoration.
- Make system state, latency, quality, and risk visible.
- Use short, specific labels.
- Design every empty, loading, error, and permission state.

### Don'ts

- Do not use loud gradients as the core identity.
- Do not rely on glassmorphism, glowing orbs, or trendy visual effects.
- Do not build marketing-style layouts inside the product dashboard.
- Do not use excessive rounded corners.
- Do not hide critical AI behavior behind vague labels.
- Do not make the product feel like a toy chatbot UI.
- Do not use one-note color palettes dominated by a single hue.

## Color System

The VoiceSense palette should balance warmth, trust, precision, and technical depth. Colors should support enterprise workflows, observability, and long reading sessions.

### Primary Palette

| Token | Hex | Usage | Rationale |
| --- | --- | --- | --- |
| `primary.900` | `#10201E` | Primary dark text on light surfaces, high-emphasis UI | Deep green-black gives authority and subtle brand distinction without feeling blue-corporate. |
| `primary.700` | `#0B5F56` | Primary actions, active states | Teal-green suggests signal, clarity, and communication while remaining professional. |
| `primary.600` | `#0F766E` | Buttons, selected navigation, key metrics | Balanced saturation for strong affordance without visual noise. |
| `primary.100` | `#DDF4EF` | Soft active backgrounds, badges | Supports calm highlighting and AI/voice states without neon effects. |
| `primary.50` | `#EEF9F6` | Very subtle section tinting | Useful for low-emphasis brand presence on large surfaces. |

### Secondary Palette

| Token | Hex | Usage | Rationale |
| --- | --- | --- | --- |
| `signal.blue` | `#2F6EEA` | Developer, API, integration, link states | Communicates technical trust and familiar interactive affordance. |
| `signal.amber` | `#B86B16` | Pending, review, human approval, warnings | Warm but controlled; useful for workflow states requiring attention. |
| `signal.violet` | `#6D55D9` | Intelligence, orchestration, advanced AI features | Adds depth and product range without making purple the dominant identity. |
| `signal.coral` | `#D45F4C` | Escalation, risk, destructive actions | Softer than pure red while still clear for important states. |
| `signal.cyan` | `#0E7490` | Streaming, realtime, voice transport | Supports technical runtime surfaces and live states. |

### Neutral Palette

| Token | Hex | Usage | Rationale |
| --- | --- | --- | --- |
| `neutral.950` | `#141615` | Primary text, dark surfaces | Near-black with slight warmth for long-term readability. |
| `neutral.800` | `#2B2E2C` | Secondary dark text, sidebar surfaces | Strong but less harsh than pure black. |
| `neutral.600` | `#5F625E` | Secondary text | Maintains readability while supporting hierarchy. |
| `neutral.400` | `#9A9D97` | Placeholder, low-emphasis labels | Useful for secondary metadata. |
| `neutral.200` | `#E4E1DA` | Borders, dividers | Warm line color that avoids sterile gray. |
| `neutral.100` | `#F0EEE8` | Subtle surfaces | Supports calm app backgrounds. |
| `neutral.50` | `#F7F6F2` | Main app background | Warm off-white creates premium comfort without beige dominance. |
| `white` | `#FFFFFF` | Primary cards and content surfaces | Maintains crisp information areas. |

### Semantic Colors

| Token | Hex | Usage | Rationale |
| --- | --- | --- | --- |
| `success` | `#16825D` | Successful runs, resolved conversations, healthy systems | Calm green aligned with reliability. |
| `success.bg` | `#E3F6ED` | Success backgrounds | Keeps success states visible but quiet. |
| `warning` | `#B86B16` | Pending approvals, latency drift, configuration warnings | Human attention without alarm. |
| `warning.bg` | `#FAECD2` | Warning backgrounds | Warm review state. |
| `danger` | `#C74637` | Failed calls, blocked tools, destructive actions | Clear risk signal without harsh red saturation. |
| `danger.bg` | `#FBE5E1` | Error backgrounds | Readable and accessible for error panels. |
| `info` | `#2F6EEA` | Informational messages, docs, developer links | Familiar and trustworthy information color. |
| `info.bg` | `#E8EFFD` | Info backgrounds | Supports product guidance and API docs. |

### Backgrounds

- `app.background`: `#F7F6F2` for the main product workspace.
- `app.background.dark`: `#141615` for dark navigation and command surfaces.
- `section.subtle`: `#F0EEE8` for secondary page bands.
- `runtime.dark`: `#101312` for voice runtime and live monitoring panels.

### Surface Colors

- `surface.base`: `#FFFFFF` for primary content panels.
- `surface.subtle`: `#FDFBF7` for nested controls and low-emphasis rows.
- `surface.raised`: `#FFFFFF` with border and shadow for popovers, menus, and modals.
- `surface.inverse`: `#141615` for dark command surfaces.

### Border Colors

- `border.subtle`: `#E8E5DE` for default dividers.
- `border.default`: `#DDD8CE` for cards, tables, and controls.
- `border.strong`: `#C8C1B5` for selected or high-contrast boundaries.
- `border.inverse`: `rgba(255,255,255,0.12)` for dark surfaces.

## Typography

### Font Selection

Primary interface font: `Inter`.

Rationale: Inter is highly legible for dashboards, supports dense enterprise interfaces, performs well across operating systems, and has excellent numeric rendering for analytics-heavy screens.

Future optional display font: `Suisse Intl`, `Geist`, or `SF Pro` where licensing and platform constraints permit. Do not introduce a display font until there is a clear brand need.

### Heading Scale

| Token | Size | Line Height | Weight | Usage |
| --- | --- | --- | --- | --- |
| `display.lg` | 56px | 60px | 750 | Rare hero-level product moments. |
| `display.md` | 44px | 50px | 750 | Main dashboard or page titles. |
| `heading.xl` | 32px | 40px | 700 | Major product sections. |
| `heading.lg` | 24px | 32px | 700 | Panels and page subsections. |
| `heading.md` | 20px | 28px | 700 | Card titles and dialogs. |
| `heading.sm` | 16px | 24px | 700 | Compact headings and table groups. |

### Body Scale

| Token | Size | Line Height | Weight | Usage |
| --- | --- | --- | --- | --- |
| `body.lg` | 18px | 30px | 400 | Explanatory page copy. |
| `body.md` | 16px | 26px | 400 | Default reading text. |
| `body.sm` | 14px | 22px | 400 | UI descriptions, table content. |
| `body.xs` | 12px | 18px | 500 | Metadata, timestamps, badges. |

### Font Weights

- `400`: default body text.
- `500`: labels, navigation, compact metadata.
- `600`: buttons, tabs, active controls.
- `700`: headings and strong emphasis.
- `750` or `800`: rare brand or display emphasis.

### Line Heights

- Display text: tight but readable, approximately 1.05 to 1.15.
- Headings: approximately 1.2 to 1.3.
- Body text: approximately 1.55 to 1.65.
- Compact UI labels: approximately 1.35 to 1.5.

### Letter Spacing

- Default letter spacing should be `0`.
- Avoid negative letter spacing.
- Uppercase metadata labels may use `0` letter spacing and rely on size, weight, and color for hierarchy.

## Spacing System

Use a 4px-based spacing scale. This keeps layout decisions consistent and works well across responsive screens.

### Base Scale

| Token | Value |
| --- | --- |
| `space.0` | 0px |
| `space.1` | 4px |
| `space.2` | 8px |
| `space.3` | 12px |
| `space.4` | 16px |
| `space.5` | 20px |
| `space.6` | 24px |
| `space.8` | 32px |
| `space.10` | 40px |
| `space.12` | 48px |
| `space.16` | 64px |
| `space.20` | 80px |

### Layout Spacing

- Product shell padding: 24px to 32px desktop, 16px to 20px mobile.
- Panel padding: 16px to 24px depending on density.
- Form field vertical gap: 12px to 16px.
- Section gap: 24px to 40px.
- Dense table row height: 44px to 52px.
- Comfortable card row height: 64px to 88px.

### Container Widths

- Full product workspace should use available width after navigation.
- Reading documents and settings pages: max width 880px to 1040px.
- Forms and configuration flows: max width 720px to 960px.
- Analytics dashboards: max width none, use responsive grid constraints.
- Developer docs: max width 1120px with a stable side navigation.

### Grid Recommendations

- Desktop dashboard: 12-column grid with 24px gutters.
- Tablet: 8-column grid with 20px gutters.
- Mobile: 4-column grid with 16px gutters.
- Use CSS grid for page layout and flexbox for small local alignment.
- Prefer predictable grid spans over masonry-like layouts.

## Elevation

### Shadows

VoiceSense should use shadows sparingly. Most hierarchy should come from spacing, borders, surface color, and typography.

| Token | Value | Usage |
| --- | --- | --- |
| `shadow.none` | none | Default panels and sections. |
| `shadow.sm` | `0 1px 2px rgba(20,22,21,0.06)` | Inputs, small controls. |
| `shadow.md` | `0 8px 24px rgba(20,22,21,0.08)` | Dropdowns, popovers. |
| `shadow.lg` | `0 24px 70px rgba(20,22,21,0.12)` | Modals and command surfaces. |

### Border Radius

Use restrained radius to keep the product precise and enterprise-ready.

- `radius.xs`: 4px for small badges and compact controls.
- `radius.sm`: 6px for inputs and buttons.
- `radius.md`: 8px for cards, panels, menus, and modals.
- `radius.lg`: 12px only for large modal surfaces or special product moments.
- Avoid pill shapes except for badges, status labels, and compact tags.

### Surface Hierarchy

1. App background: warm neutral, no shadow.
2. Page sections: unframed or lightly tinted.
3. Panels and cards: white surface with subtle border.
4. Interactive controls: border, hover state, and focus ring.
5. Overlays: elevated with shadow and strong separation.
6. Critical runtime panels: dark inverse surface for live operational focus.

## Motion

### Animation Philosophy

Motion should make the product feel fast, responsive, and intelligent. It should clarify state changes, not decorate the interface.

Use motion for:

- Hover and pressed feedback.
- Opening menus, drawers, and modals.
- Loading and streaming states.
- Voice activity and realtime status.
- Confirming successful actions.

Avoid motion that:

- Slows down operational workflows.
- Distracts during live calls.
- Loops indefinitely without communicating state.
- Makes dense dashboards feel unstable.

### Transition Durations

- Micro interactions: 120ms to 160ms.
- Menus and popovers: 140ms to 180ms.
- Panels and drawers: 180ms to 240ms.
- Page-level transitions: 220ms to 320ms only when useful.
- Loading skeleton shimmer: 1000ms to 1400ms.

### Easing

- Default: `cubic-bezier(0.2, 0, 0, 1)`.
- Exit: `cubic-bezier(0.4, 0, 1, 1)`.
- Emphasized entrance: `cubic-bezier(0.16, 1, 0.3, 1)`.

### Hover Behavior

- Buttons should shift surface, border, or text color; avoid large movement.
- Table rows may use subtle background change.
- Cards should not jump or resize on hover.
- Icon buttons should expose tooltips for unfamiliar actions.

### Loading Animations

- Use skeletons for content regions.
- Use progress indicators for long-running setup tasks.
- Use streaming indicators for live AI responses.
- Use voice waveform activity only when audio is actually active or simulated in a clearly labeled test state.

### Micro-interactions

- Successful save: subtle inline confirmation.
- Tool call started: event appears in runtime trace.
- Tool call failed: clear error row with retry or inspect action.
- AI employee listening: calm realtime indicator, not a flashy animation.
- Human approval required: persistent state until resolved.

## Iconography

### Recommended Icon Library

Use `lucide-react` for product UI icons.

Rationale: Lucide provides a broad, consistent, readable outline icon set that works well in SaaS dashboards, developer tools, and operational interfaces.

### Icon Sizing Rules

- Navigation icons: 18px to 20px.
- Button icons: 16px to 18px.
- Metric icons: 18px to 22px.
- Empty state icons: 32px to 48px.
- Product illustration icons: use sparingly and keep consistent stroke width.

### Usage Guidelines

- Icons should support recognition, not replace unclear labels in important workflows.
- Use icon-only buttons only for familiar actions or when tooltips are provided.
- Keep stroke width visually consistent.
- Do not mix filled, 3D, emoji, and outline icon styles in product UI.
- Use icons for tools, channels, statuses, and navigation categories.

## Accessibility

### Contrast Goals

- Body text should meet WCAG AA at minimum.
- Critical operational text should aim for WCAG AAA where practical.
- Do not rely on color alone for status; pair color with text or iconography.
- Disabled states must remain readable enough to understand what is unavailable.

### Focus States

- Every interactive element must have a visible keyboard focus state.
- Default focus ring: 2px solid `#0F766E` with 2px offset.
- Dark surfaces may use `#83DCC9` for focus rings.
- Focus states should not be removed for aesthetic reasons.

### Keyboard Navigation Principles

- All controls must be reachable by keyboard.
- Navigation order should match visual order.
- Modals and drawers must trap focus while open.
- Escape should close dismissible overlays.
- Command menus should support keyboard-first workflows.
- Destructive actions should require clear confirmation.

### Responsive Design Principles

- Design mobile layouts intentionally, not as compressed desktop screens.
- Product navigation should collapse predictably.
- Data tables need mobile alternatives such as cards, pinned columns, or horizontal scroll with clear affordance.
- Text must never overlap containers or controls.
- Fixed-format UI elements should have stable dimensions to avoid layout shift.

## Design Principles

### Premium

Premium comes from restraint, consistency, spacing, and thoughtful details. Avoid decorative excess.

### Calm

The product should help users feel in control, especially when AI employees are handling live customer interactions.

### Minimal

Minimal does not mean empty. It means every visible element earns its place.

### Fast

The interface should communicate immediacy through fast response, clear feedback, and low-friction flows.

### Intelligent

AI behavior should be observable, explainable, and configurable. Intelligence should feel like assistance, not mystery.

### Trustworthy

Users should see system health, conversation history, tool usage, approvals, failures, and audit trails clearly.

### Enterprise-ready

The product should support roles, permissions, compliance posture, auditability, and operational reliability from the beginning.

## Product Surface Guidance

### Dashboard

Dashboards should be dense, scannable, and operational. Use metrics, traces, employee status, latency, channel activity, and system health as first-class information.

### Builder

The AI employee builder should feel guided but powerful. Break configuration into understandable stages: identity, instructions, voice, model, tools, knowledge, memory, channels, guardrails, testing, deployment, and monitoring.

### Conversation Playground

The playground should make model behavior, tool calls, memory use, latency, and evaluation visible. It should support text testing first and voice testing as the runtime matures.

### Developer Platform

Developer surfaces should be precise, documentation-rich, and practical. API keys, webhooks, logs, SDK examples, and request traces should be easy to inspect and copy.

### Observability

Observability UI should emphasize causality: user input, AI reasoning boundary, tool calls, provider latency, policy checks, responses, outcomes, and failures.

## Implementation Notes

- Translate this document into design tokens before expanding the component library.
- Keep color, spacing, typography, radius, and shadow tokens centralized.
- Components should use semantic tokens rather than hard-coded color values.
- Future dark mode should be token-driven, not a separate visual system.
- Accessibility checks should be part of component review.
- Screens should be reviewed at desktop, tablet, and mobile widths before completion.