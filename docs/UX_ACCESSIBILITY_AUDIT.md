# UX and Accessibility Audit

VoiceSense targets WCAG 2.2 AA readiness.

## Release-Candidate Standards

- Every page has semantic landmarks through the workspace shell.
- Keyboard users can skip to content.
- Active routes expose `aria-current`.
- Icon-only buttons require accessible labels.
- Motion respects `prefers-reduced-motion`.
- Touch targets expand on coarse pointers.
- Focus states are visible across dashboard and UI components.
- Empty, loading, and error states preserve layout stability.

## UX Principles

- Keep primary actions visible and secondary actions quiet.
- Prefer progressive disclosure over dense first-run pages.
- Use the right panel for command suggestions and workspace health.
- Use onboarding cues to reduce first-time setup uncertainty.
- Keep tables scannable, with clear status badges and recovery actions.