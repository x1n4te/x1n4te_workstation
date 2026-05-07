# Smart Parenting App — Client Wiki

Standalone project wiki for the Smart Parenting mobile application (Expo SDK 55 + Supabase). This wiki is separate from the main workstation wiki and contains implementation details, architecture decisions, and screen walkthroughs.

---

## Quick Navigation

### Architecture
- [Root Directory & Repo Structure](architecture/root-directory.md) — File layout, navigation architecture, config files
- [Database Schema](architecture/database-schema.md) — Consolidated Supabase schema, RLS policies, indexes, storage
- [Loading Overlay & Auth Guard](architecture/loading-overlay.md) — Root-level auth state machine, redirect delays, z-index overlay

### Screens
- [Dashboard](screens/dashboard.md) — Home tab: greeting, stats grid, scheduled activities, quick log
- [Activities (Log / Schedule)](screens/activities.md) — Core data entry: time inputs, chip selectors, dual-mode form
- [History](screens/history.md) — Read-only activity browser: calendar, filters, stats charts
- [Settings](screens/settings.md) — Profile hub, per-child config, account management, FAQ
- [Login & Register](screens/login-and-register.md) — Auth flows, validation, success states

### Features
- [AI Insights](features/ai-insights.md) — Zero-shot prompting architecture, Edge Function, normalizer, audit trail

---

## Design System Reference

| Token | Value | Usage |
|-------|-------|-------|
| Primary | `#FF7F60` | Buttons, active states, spinners |
| Background | `#FEFBF6` | App background |
| Surface | `#FFFDFF` | Cards, modals |
| Error | `#EF4444` | Validation, destructive actions |
| Screen Time | `#FF7F60` | Activity icon/badge |
| Sleep | `#10B981` | Activity icon/badge |
| Meals | `#F59E0B` | Activity icon/badge |
| Education | `#8B5CF6` | Activity icon/badge |

