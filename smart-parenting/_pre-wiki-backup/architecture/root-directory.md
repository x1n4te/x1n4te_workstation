## Smart Parenting App — Repository Structure Reference

### Root Configuration Files

| File            | Purpose                                                                                                                                                         |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `app.json`      | Expo SDK 55 config — app name, bundle ID (`com.smartparenting.app`), EAS update URL, deep-link scheme (`smart-parenting-app`), `typedRoutes` experiment enabled |
| `App.tsx`       | Entry point — just renders `<Slot />` from `expo-router`, all routing delegated to `app/`                                                                       |
| `tsconfig.json` | Strict TypeScript — paths point to `app/` as base URL                                                                                                           |
| `eas.json`      | EAS Build/Submit config for OTA updates                                                                                                                         |
| `.env`          | Runtime secrets — `EXPO_PUBLIC_SUPABASE_URL`, `EXPO_PUBLIC_SUPABASE_ANON_KEY`                                                                                   |
| `deno.lock`     | Lockfile for Supabase Edge Functions (Deno runtime)                                                                                                             |
| `package.json`  | Deps: Expo SDK 55, React Native 0.83.6, `@react-native-async-storage/async-storage`, `expo-router`, `react-native-paper`, `zustand`, Supabase JS SDK `^2.49.0`  |

---

### `app/` — All Screens (Expo Router file-based routing)

```
app/
├── _layout.tsx              # Root layout: PaperProvider theme, auth guard, notification handler
├── (auth)/                  # Auth group — always accessible, redirect if logged in
│   ├── _layout.tsx
│   ├── login.tsx            # Email/password login + "Welcome back!" animation
│   └── signup.tsx          # Email/password signup (auto sign-out after, no auto-login)
├── (tabs)/                  # Main app group — guarded by auth (redirects to login if unauthed)
│   ├── _layout.tsx         # Tab navigator: 5 tabs (Home, Activities, History, Insights, Settings)
│   ├── index.tsx          # Dashboard: greeting, today's activities, scheduled activities, quick-log
│   ├── log.tsx            # Activity logger: segmented control → type-specific form
│   ├── history.tsx        # SectionList with date grouping + filter pills
│   ├── ai.tsx            # AI Insights: 28-day analysis, recommendation cards
│   └── profile.tsx       # Per-child settings, screen time/sleep limits, notification toggles
├── child/
│   └── wizard.tsx        # Multi-step child creation (name/DOB → routine → BMI → avatar)
├── settings/
│   ├── [id].tsx          # Per-child settings (limits, notifications, routine, delete)
│   ├── edit-profile.tsx  # Change name/avatar
│   ├── change-email.tsx
│   ├── change-password.tsx
│   ├── help.tsx
│   └── privacy.tsx
```

**Navigation Architecture:**
- `(auth)` / `(tabs)` are route groups — parentheses don't affect URLs, only grouping
- Auth guard lives in `_layout.tsx` — checks `useAuth().user` + `segments[0]`, redirects with 1800ms delay on login
- `isMounted` ref pattern prevents "Attempted to navigate before mounting" errors from synchronous `onAuthStateChange`
- Deep-link notification handling: polls auth readiness every 100ms (max 1s), then routes to tab based on notification `type`

---

### `components/` — Shared UI Components

| File | Purpose |
|------|---------|
| `ScreenHeader.tsx` | Reusable header: icon+title left, child picker pill right, back-mode for modals. Contains inline child picker Modal. |
| `DatePicker.tsx` | Custom DOB picker using `DateTimePicker` — shows age in months below picker |

---

### `lib/` — Business Logic & Utilities

| File | Purpose |
|------|---------|
| `api.ts` | **Main data layer** — all Supabase CRUD for `children`, `activities`, `recommendations`, `scheduled_activities`. Also exports `getAgeYears()`, `getAgeMonths()`, `formatDateLocal()`, `getAgeGroup()`, types `Activity`, `Child`, `Recommendation`, `ScheduledActivity` |
| `supabase.ts` | Supabase client init — `createClient(EXPO_PUBLIC_SUPABASE_URL, EXPO_PUBLIC_SUPABASE_ANON_KEY)` |
| `bmi.ts` | WHO BMI-for-age assessment for 2–5 year olds (toddlers) — returns z-score, percentile, category |
| `notifications.ts` | Expo Notifications setup, per-child daily scheduled notifications (9 types: bedtime, wake, meals, nap, activity, learn, growth, weekly, reminder), cancellation |
| `sleep-calculator.ts` | Sleep duration recommendation based on WHO age guidelines + child age |
| `image.ts` | Avatar image picking + Supabase Storage upload (`pickAndUploadImage`) |
| `database.types.ts` | Supabase-generated TypeScript types for all DB tables (generated from `supabase config`) |

---

### `stores/` — Zustand State

| File | Purpose |
|------|---------|
| `auth.ts` | **Two stores**: `useAuth` (user, signIn, signUp, signOut, loadSession) + `useApp` (selectedChild, selectedChildId, children[], loadChildren, selectChild). `useApp` persisted to AsyncStorage (`smartparenting-app-state`) — only `selectedChildId` is persisted. |

---

### `supabase/` — Backend

```
supabase/
├── config.toml              # Supabase CLI project config
├── functions/
│   └── analyze-child/       # Edge Function: aggregates 28-day activities → OpenRouter → recommendations
│       ├── index.ts         # Entry point, calls recommendation-normalizer
│       ├── recommendation-normalizer.ts   # Transforms LLM raw output → DB-ready recommendation
│       └── recommendation-normalizer.test.ts
```

---

### `database/` — Schema & Migrations

|| File | Purpose |
|------|---------|
| `schema.sql` | **Consolidated schema** (527 lines, 2026-04-25) — single-file fresh-setup for Supabase SQL Editor. Contains: `children`, `activities`, `recommendations`, `alerts`, `scheduled_activities`, RLS policies, indexes, triggers, avatar storage bucket, and compatibility guards for older partial databases. Replaces 14 prior migration files. No separate `migrations/` directory. |
| `seed_test_account.sql` | Does not exist in current repo |

---

### Other Root Files

| File                            | Purpose                                                                                             |
| ------------------------------- | --------------------------------------------------------------------------------------------------- |
| `index.js`                      | Expo entry — imports `expo-router/hook` and `polyfills.js`                                          |
| `polyfills.js`                  | React Native polyfills for `fetch`, `AbortController`                                               |
| `metro.config.js`               | Metro bundler config                                                                                |
| `scripts/create_test_user.js`   | Dev script to create a test account                                                                 |
| `scripts/remove-dom-webview.js` | Cleanup script — removes `@expo/dom-webview` that breaks Android builds                             |

