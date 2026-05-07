# Repository Structure

This page describes how the codebase is organized.

---

## Root Files

| File | Purpose |
|------|---------|
| `app.json` | Expo configuration — app name, bundle ID, EAS updates, deep-link scheme |
| `App.tsx` | Entry point — delegates everything to Expo Router |
| `tsconfig.json` | Strict TypeScript with path aliases |
| `eas.json` | Cloud build and OTA update configuration |
| `.env` | Runtime secrets (Supabase URL and anon key) |
| `package.json` | Dependencies — Expo SDK 55, React Native, Paper, Zustand, Supabase |

---

## `app/` — Screens

The app uses **Expo Router** for file-based routing. Every file in `app/` automatically becomes a screen.

```
app/
├── _layout.tsx              # Root layout — auth guard, theme provider, notifications
├── (auth)/                  # Auth screens (accessible when logged out)
│   ├── login.tsx
│   └── signup.tsx
├── (tabs)/                  # Main app tabs (guarded — requires login)
│   ├── _layout.tsx         # Tab bar configuration
│   ├── index.tsx          # Dashboard
│   ├── log.tsx            # Activities (Log/Schedule)
│   ├── history.tsx        # History
│   ├── ai.tsx             # AI Insights
│   └── profile.tsx        # Settings hub
├── child/
│   └── wizard.tsx        # Multi-step child creation
└── settings/
    ├── [id].tsx          # Per-child settings
    ├── edit-profile.tsx
    ├── change-email.tsx
    ├── change-password.tsx
    ├── help.tsx
    └── privacy.tsx
```

Route groups like `(auth)` and `(tabs)` don't appear in URLs — they exist only for organization.

---

## `components/` — Shared UI

| File | Purpose |
|------|---------|
| `ScreenHeader.tsx` | Reusable header with inline child picker modal |
| `DatePicker.tsx` | Custom date-of-birth picker with age display |

---

## `lib/` — Business Logic

| File | Purpose |
|------|---------|
| `api.ts` | All Supabase CRUD operations, age helpers, TypeScript types |
| `supabase.ts` | Supabase client initialization |
| `bmi.ts` | WHO BMI-for-age calculator (ages 2–5) |
| `notifications.ts` | Notification scheduling, cancellation, and permissions |
| `sleep-calculator.ts` | Sleep duration recommendations based on WHO guidelines |
| `image.ts` | Avatar image picking and Supabase Storage upload |
| `database.types.ts` | Auto-generated TypeScript types from the database schema |

---

## `stores/` — State Management

| File | Purpose |
|------|---------|
| `auth.ts` | Two Zustand stores: `useAuth` (user/session) and `useApp` (selected child, children list) |

`useApp` persists only `selectedChildId` to AsyncStorage. On app launch, the store restores the last selected child.

---

## `supabase/` — Backend

```
supabase/
├── config.toml              # CLI project configuration
└── functions/
    └── analyze-child/
        ├── index.ts                     # Edge Function entry point
        ├── recommendation-normalizer.ts # Post-processing AI output
        └── recommendation-normalizer.test.ts
```

---

## `database/` — Schema

| File | Purpose |
|------|---------|
| `schema.sql` | Consolidated 527-line schema. Replaces 14 prior migration files. |

This single file can be pasted directly into the Supabase SQL Editor to set up a fresh project.
