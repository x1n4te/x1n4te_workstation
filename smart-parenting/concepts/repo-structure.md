---
title: Repository Structure
created: 2026-04-25
updated: 2026-04-25
type: concept
tags: [architecture, repo-structure, navigation, expo]
sources: [raw/technical-reference.md]
---

# Repository Structure

## Root Configuration Files

| File | Purpose |
|------|---------|
| `app.json` | Expo SDK 55 config — bundle ID, EAS updates, deep-link scheme, `typedRoutes` |
| `App.tsx` | Entry point — renders `<Slot />` from `expo-router` |
| `tsconfig.json` | Strict TypeScript with `app/` as base URL |
| `eas.json` | EAS Build/Submit config for OTA updates |
| `.env` | Runtime secrets — `EXPO_PUBLIC_SUPABASE_URL`, `EXPO_PUBLIC_SUPABASE_ANON_KEY` |
| `deno.lock` | Lockfile for Supabase Edge Functions (Deno runtime) |
| `package.json` | Expo SDK 55, RN 0.83.6, Paper, Zustand, Supabase JS SDK `^2.49.0` |

---

## `app/` — Expo Router File-Based Routing

```
app/
├── _layout.tsx              # Root layout: PaperProvider, auth guard, notification handler
├── (auth)/                  # Auth group — always accessible, redirects if logged in
│   ├── _layout.tsx
│   ├── login.tsx            # Email/password login + "Welcome back!" animation
│   └── signup.tsx          # Signup (auto sign-out after, no auto-login)
├── (tabs)/                  # Main app group — guarded by auth
│   ├── _layout.tsx         # Tab navigator: 5 tabs (Home, Activities, History, Insights, Settings)
│   ├── index.tsx          # Dashboard
│   ├── log.tsx            # Activity logger
│   ├── history.tsx        # SectionList with date grouping + filter pills
│   ├── ai.tsx            # AI Insights
│   └── profile.tsx       # Per-child settings, limits, toggles
├── child/
│   └── wizard.tsx        # Multi-step child creation
└── settings/
    ├── [id].tsx          # Per-child settings
    ├── edit-profile.tsx  # Change name/avatar
    ├── change-email.tsx
    ├── change-password.tsx
    ├── help.tsx
    └── privacy.tsx
```

**Navigation notes:**
- `(auth)` / `(tabs)` are route groups — parentheses don't affect URLs
- Auth guard in `_layout.tsx` checks `useAuth().user` + `segments[0]`, redirects with 1800ms delay
- `isMounted` ref pattern prevents "Attempted to navigate before mounting" errors
- Deep-link notification handling: polls auth readiness every 100ms up to 1s max

See [[auth-loading-overlay]] for the full auth state machine.

---

## `components/` — Shared UI

| File | Purpose |
|------|---------|
| `ScreenHeader.tsx` | Reusable header with inline child picker Modal |
| `DatePicker.tsx` | Custom DOB picker with age display |

See [[design-system]] for component conventions.

---

## `lib/` — Business Logic

| File | Purpose |
|------|---------|
| `api.ts` | Main data layer — all Supabase CRUD, `getAgeYears()`, types |
| `supabase.ts` | Supabase client init |
| `bmi.ts` | WHO BMI-for-age assessment for 2–5 year olds |
| `notifications.ts` | Expo Notifications setup, per-child scheduling, cancellation |
| `sleep-calculator.ts` | Sleep duration recommendations based on WHO guidelines |
| `image.ts` | Avatar picking + Supabase Storage upload |
| `database.types.ts` | Supabase-generated TypeScript types |

---

## `stores/` — Zustand State

| File | Purpose |
|------|---------|
| `auth.ts` | Two stores: `useAuth` (user/session) + `useApp` (selectedChild, children[]) |

`useApp` is persisted to AsyncStorage (`smartparenting-app-state`) — only `selectedChildId` is persisted.

---

## `supabase/` — Backend

```
supabase/
├── config.toml
└── functions/
    └── analyze-child/
        ├── index.ts
        ├── recommendation-normalizer.ts
        └── recommendation-normalizer.test.ts
```

See [[ai-insights-architecture]] for the Edge Function flow.

---

## `database/` — Schema

| File | Purpose |
|------|---------|
| `schema.sql` | Consolidated 527-line schema (replaces 14 prior migrations) |

See [[database-schema]] for full table documentation.
