# VoiceSense UI Components

The VoiceSense UI package is the official reusable interface layer for product, admin, developer, and internal tools. It follows the brand rules in `DESIGN_LANGUAGE.md` and exposes typed React components built with Radix primitives, shadcn-style variants, and tokenized CSS.

## Package Structure

- `src/base`: Buttons and primitive actions.
- `src/forms`: Inputs, labels, helper text, validation messages, and selection controls.
- `src/navigation`: Sidebar, top navigation, breadcrumbs, tabs, pagination, dropdowns, and command palette.
- `src/data-display`: Cards and enterprise data table.
- `src/feedback`: Toast, alert, badge, progress, skeleton, empty, loading, and error states.
- `src/overlays`: Dialog, drawer, popover, tooltip, and context menu.
- `src/layout`: Page, dashboard, settings, auth, and centered layouts.
- `src/charts`: Line, bar, pie, area, and KPI chart wrappers.
- `src/utility`: Avatar, separator, and small helpers.

## Component Standards

Every component should support keyboard access, visible focus states, disabled states where applicable, responsive sizing, and dark-mode tokens. Components should accept `className` for layout-level composition while keeping visual defaults centralized in `src/styles.css`.

## Usage

```tsx
import { Button, Card, CardContent, Field, Label, TextInput } from "@voicesense/ui";
import "@voicesense/ui/src/styles.css";
```

## Accessibility Notes

- Radix primitives provide accessible behavior for dialogs, menus, selects, tabs, switches, checkboxes, radio groups, popovers, tooltips, and progress.
- Icon-only buttons must include `aria-label`.
- Inputs with validation should pair `Label`, `HelperText`, and `ErrorMessage`.
- Tables include row-selection labels and keyboard focusable controls.
- Color is never the only state indicator; badges, labels, and text must accompany color states.

## Variants

### Buttons

Variants: `primary`, `secondary`, `ghost`, `outline`, `destructive`, `success`.

Sizes: `sm`, `md`, `lg`, `icon`.

Use primary for the main action, outline for secondary commands, ghost for low-emphasis actions, destructive for risky actions, and success for explicit positive confirmations.

### Inputs

Inputs support text, password, search, number, email, and phone types. Use `invalid` to expose error styling and pair it with `ErrorMessage`.

### Cards

Variants: `default`, `dashboard`, `stat`, `agent`, `knowledge`, `settings`.

Use dashboard cards for primary operational panels, stat cards for KPI summaries, agent cards for AI employee objects, knowledge cards for source/index surfaces, and settings cards for configuration groups.

### Feedback

Use alerts for persistent inline messages, toasts for transient confirmations, skeletons for content loading, progress for measurable completion, and empty/error/loading states for full-region status.

### Tables

`DataTable` supports search, sorting, pagination, row selection, and bulk action slots. Keep business-specific cell rendering outside the table through the `render` column function.

### Charts

Chart wrappers are intentionally thin and standardized. They provide consistent container, sizing, and palette defaults while preserving Recharts flexibility.
## Release-Candidate Component Checklist

Before a component is used in production screens, verify:

- Keyboard focus is visible.
- Reduced-motion preferences are respected.
- Touch targets meet mobile ergonomics.
- Disabled and loading states are present where applicable.
- Icon-only controls have accessible labels.
- Text does not overflow at mobile widths.
- Empty, loading, and error states preserve layout stability.