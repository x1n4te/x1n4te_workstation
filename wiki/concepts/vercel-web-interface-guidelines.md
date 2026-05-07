---
id: vercel-web-interface-guidelines-001
type: concept
created: 2026-04-10
updated: 2026-04-10
last_verified: 2026-04-10
review_after: 2026-07-10
stale_after: 2026-10-10
confidence: high
source_refs:
  - sources/operational/2026-04-10-smart-parenting-ui-redesign
status: active
tags:
  - web-development
  - ui
  - accessibility
  - frontend
  - review-checklist
related:
  - concepts/signs-of-ai-writing
  - entities/hermes-agent-v2-reference
---

# Vercel Web Interface Guidelines — Review Checklist

**Purpose:** Review UI code for compliance with modern web interface best practices.
**Format:** Concise rules for code review. High signal-to-noise.
**Use with:** Claude Code, Hermes, or manual review.

---

## Accessibility

- Icon-only buttons need `aria-label`
- Form controls need `<label>` or `aria-label`
- Interactive elements need keyboard handlers (`onKeyDown`/`onKeyUp`)
- `<button>` for actions, `<a>`/`<Link>` for navigation (not `<div onClick>`)
- Images need `alt` (or `alt=""` if decorative)
- Decorative icons need `aria-hidden="true"`
- Async updates (toasts, validation) need `aria-live="polite"`
- Use semantic HTML (`<button>`, `<a>`, `<label>`, `<table>`) before ARIA
- Headings hierarchical `<h1>`–`<h6>`; include skip link for main content
- `scroll-margin-top` on heading anchors

## Focus States

- Interactive elements need visible focus: `focus-visible:ring-*` or equivalent
- Never `outline-none` / `outline: none` without focus replacement
- Use `:focus-visible` over `:focus` (avoid focus ring on click)
- Group focus with `:focus-within` for compound controls

## Forms

- Inputs need `autocomplete` and meaningful `name`
- Use correct `type` (`email`, `tel`, `url`, `number`) and `inputmode`
- Never block paste (`onPaste` + `preventDefault`)
- Labels clickable (`htmlFor` or wrapping control)
- Disable spellcheck on emails, codes, usernames (`spellCheck={false}`)
- Checkboxes/radios: label + control share single hit target (no dead zones)
- Submit button stays enabled until request starts; spinner during request
- Errors inline next to fields; focus first error on submit
- Placeholders end with `…` and show example pattern
- `autocomplete="off"` on non-auth fields to avoid password manager triggers
- Warn before navigation with unsaved changes (`beforeunload` or router guard)

## Related Sections
*Detailed content split into sub-pages for readability. See [[concepts/vercel-web-interface-guidelines-details]] for the full reference.*

---

*This page is scannable in 30 seconds. Full reference content moved to sub-pages.*
