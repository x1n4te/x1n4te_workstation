---
id: smart-parenting-app-tech-stack-details-001
type: concept
created: 2026-04-10
updated: 2026-05-05
last_verified: 2026-04-25
review_after: 2026-07-23
stale_after: 2026-10-23
confidence: high
source_refs:
  - sources/operational/2026-04-10-smart-parenting-ui-redesign
  - raw/articles/smart-parenting-app-codebase-2026-04-12
  - raw/articles/smart-parenting-app-codebase-2026-04-13
  - sources/operational/2026-04-14-smart-parenting-feature-session
  - sources/operational/2026-04-23-spa-hci-alert-fix-session
  - sources/operational/2026-04-24-spa-sdk55-schema-migration-session
  - sources/operational/2026-04-25-spa-consolidated-database-schema
  - sources/operational/2026-04-25-spa-ai-insights-notification-ux-session
  - sources/operational/2026-05-01-spa-history-activity-crud-phase2
  - sources/operational/2026-05-01-spa-history-activity-crud-ui
  - sources/operational/2026-05-05-spa-notification-orphan-fixes
status: active
tags:
  - react-native
  - expo
  - supabase
  - openrouter
  - mobile-dev
  - smart-parenting-app
related:
  - concepts/smart-parenting-app-tech-stack
  - concepts/hci-design-principles-mobile
---

# Smart Parenting Tech — Detailed Reference

Back to overview: [[concepts/smart-parenting-app-tech-stack]]

## Supabase (Auth + Database)

**What:** Open-source Firebase alternative. PostgreSQL database with auth, realtime, storage, and edge functions. Used for BOTH auth and database in this project (Firebase removed).

**Actual implementation:**
- `lib/supabase.ts` — Lazy-loaded client with SSR-safe AsyncStorage
- `stores/auth.ts` — useAuth store wraps signIn/signUp/signOut
- `database/schema.sql` — single consolidated bootstrap file containing base tables, all former migrations, RLS policies, avatar storage setup, triggers, and indexes
- RLS on all 5 app tables — `parent_id = auth.uid()` directly or through child ownership subqueries

**Auth flow (verified from code):**
- signUp does NOT auto-login (email confirmation compat)
- signIn with email/password
- onAuthStateChange listener for session persistence
- Root layout auth guard: unauthenticated → /(auth)/login

**Why Supabase Auth over Firebase:**
- Single provider (auth + DB + RLS — no split brain)
- PostgreSQL RLS you already know from WIMS-BFP
- Open source, no vendor lock-in
- Simpler setup (one SDK, not two)

**Free tier:** 500MB database, 50K monthly active users.

**Key docs:**
- Supabase docs: https://supabase.com/docs/
- React Native quickstart: https://supabase.com/docs/guides/auth/quickstarts/react-native
- Supabase JS SDK: https://supabase.com/docs/reference/javascript/start
- Database guide: https://supabase.com/docs/guides/database

**Key features for this project:**
- PostgreSQL database (activity logs, child profiles, recommendations)
- Row Level Security (parents only see their children's data)
- Auth (email/password — no Firebase needed)
- Edge Functions (AI analysis endpoint)

**Database (verified from consolidated schema.sql):**
- 5 app tables: children (soft-delete), activities (6 types, JSONB value), recommendations, alerts, scheduled_activities
- Storage setup: public `avatars` bucket plus owner-aware storage.object policies for profile/child avatar paths
- RLS on all app tables — separate SELECT/INSERT/UPDATE/DELETE policies
- children: direct parent_id = auth.uid() ownership with soft-delete scoping
- activities/recommendations/alerts/scheduled_activities: child_id subquery through active children
- Composite indexes: activity child/type + recorded_at, scheduled child/status/type + pending end-time
- Triggers: auto-update `children.updated_at`; calculate `children.bmi` from height/weight
- Optional development seed data lives in `database/seed_test_account.sql.template`; `database/schema.sql` is the only `.sql` file under `database/`

---

## OpenRouter API

**What:** Unified API for 400+ AI models. One API key, access to GPT-4, Claude, Gemini, Llama, Qwen, and more. Pay-per-use, free tier available.

**Key docs:**
- OpenRouter docs: https://openrouter.ai/docs/quickstart
- API reference: https://openrouter.ai/docs/api/reference/overview
- Models list: https://openrouter.ai/models
- React Native integration: https://openrouter.ai/docs/guides/community/frameworks-and-integrations-overview

**Quick start:**
```javascript
const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + OPENROUTER_API_KEY,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'google/gemma-4-26b-a4b-it:free',  // free model
    messages: [{role: 'user', content: prompt}],
  }),
});
```

**Key features for this project:**
- Free models available (Gemma, Llama, Qwen)
- Structured output support (JSON mode)
- Same API as OpenAI (drop-in compatible)
- Pay-per-token (no subscription needed)
- Auto-fallback (if one provider is down, routes to another)

**Why OpenRouter over direct providers:**
- One API key for all models
- Free tier covers development + testing
- You already use it for WIMS-BFP (Nous Portal)
- Easy to switch models without code changes

---

## Expo EAS Build

**What:** Cloud build service for Expo/React Native apps. Builds APK (Android) and IPA (iOS) without local native build tools.

**Key docs:**
- EAS Build docs: https://docs.expo.dev/build/introduction/
- Build profiles: https://docs.expo.dev/build/eas-json/
- Android build: https://docs.expo.dev/build/setup/
- iOS build: https://docs.expo.dev/build-reference/ios-build/
- Submit to stores: https://docs.expo.dev/submit/introduction/

**Quick start:**
```bash
# 1. Install EAS CLI
npm install -g eas-cli

# 2. Login
eas login

# 3. Configure
eas build:configure

# 4. Build Android APK
eas build --platform android --profile preview

# 5. Build iOS IPA (requires Apple Developer account)
eas build --platform ios --profile preview
```

**Build profiles (eas.json):**
```json
{
  "build": {
    "development": { "developmentClient": true, "distribution": "internal" },
    "preview": { "distribution": "internal" },
    "production": {}
  }
}
```

**Key features:**
- Cloud builds (no local Android Studio / Xcode needed)
- Automatic credential management (keystores, provisioning profiles)
- Parallel builds (Android + iOS simultaneously)
- Build caching (faster subsequent builds)
- Free tier: 30 builds/month

---

## React Native Paper (UI Library)

**What:** Material Design components for React Native. Pre-built buttons, forms, cards, navigation.

**Docs:** https://callstack.github.io/react-native-paper/

**Install:**
```bash
npx expo install react-native-paper react-native-safe-area-context
```

**Why:** Pre-built Material Design components. Saves time on UI development. Accessible by default.

---

## react-native-chart-kit (Charts)

**What:** Pre-built chart components for React Native. Line, bar, pie charts.

**Docs:** https://github.com/indiespirit/react-native-chart-kit

**Install:**
```bash
npx expo install react-native-chart-kit react-native-svg
```

**Why:** Pre-built charts for activity reports. Minimal config, good enough for a prototype.

---

## Architecture (Verified)

```
┌─────────────────────────────────────────┐
│   React Native App (Expo SDK 55)        │
│                                         │
│   ┌───────────┐  ┌───────────────────┐  │
│   │  Zustand  │  │  Expo Router      │  │
│   │ useAuth   │  │  file-based       │  │
│   │ useApp    │  │  (auth)/(tabs)    │  │
│   └─────┬─────┘  └────────┬──────────┘  │
│         │                 │              │
│   ┌─────┴─────────────────┴──────────┐  │
│   │  lib/supabase.ts                 │  │
│   │  (lazy client, SSR-safe)         │  │
│   └─────┬────────────────────────────┘  │
│         │                               │
│   ┌─────┴────────────────────────────┐  │
│   │  Supabase Cloud                  │  │
│   │  ┌──────────┐ ┌───────────────┐  │  │
│   │  │ Auth     │ │ PostgreSQL    │  │  │
│   │  │ (email/  │ │ + RLS         │  │  │
│   │  │  pass)   │ │ 4 tables      │  │  │
│   │  └──────────┘ └───────────────┘  │  │
│   │  ┌──────────────────────────┐    │  │
│   │  │ Edge Function            │    │  │
│   │  │ analyze-child → OpenRouter│    │  │
│   │  └──────────────────────────┘    │  │
│   └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## Screen Architecture

```
app/
├── _layout.tsx          # Root: PaperProvider + Stack + auth guard
├── (auth)/              # Auth group (shown when unauthenticated)
│   ├── login.tsx        # Animated welcome, inline validation
│   └── signup.tsx       # No auto-login (email confirm compat)
├── (tabs)/              # Main app (shown when authenticated)
│   ├── index.tsx        # Dashboard: stats, today's activities, child picker
│   ├── log.tsx          # Activity logger: 6 types, duration stepper
│   ├── history.tsx      # History browser: SectionList, date grouping, filters (NEW)
│   ├── ai.tsx           # AI recommendations: filter bar, priority
│   └── profile.tsx      # Settings: child management, sign out
└── child/
    └── new.tsx          # Add child: quick age selectors, inline validation
```

**Tab order:** Dashboard → Log → History → AI Insights → Settings

## Zustand Stores

```typescript
// stores/auth.ts — two stores in one file

useAuth: {
  user: User | null,
  loading: boolean,
  signIn(email, password),
  signUp(email, password, name),  // no auto-login
  signOut(),
  loadSession(),                  // getSession + onAuthStateChange
}

useApp: {
  selectedChild: Child | null,
  children: Child[],
  setChildren(children),
  selectChild(child),
  loadChildren(),                  // preserves selection if valid
}
```

## API Layer (lib/api.ts)

```typescript
// Children
getChildren()              // ordered by created_at DESC
createChild(name, dob, userId)  // userId from Zustand, NOT getUser()
updateChildSettings(childId, { name, date_of_birth, avatar_url, notifications })  // notifications: Record<string,boolean>|null

// Activities
logActivity(childId, type, value)  // auto-sets recorded_at
getActivities(childId, type?)      // 100 limit, optional filter
getActivitySummary(childId)        // last 7 days
getTodayActivities(childId)        // today only

// AI
getRecommendations(childId)        // 20 limit
analyzeChild(childId)              // calls Edge Function
```

---

## Current Versions (SDK 55)

| Package | Version | Documentation |
|---|---|---|
| Expo | ~55.0.0 | https://docs.expo.dev/versions/v55.0.0/ |
| React Native | 0.83.6 | https://reactnative.dev/docs/getting-started |
| Expo Router | ~55.0.13 | https://docs.expo.dev/router/introduction/ |
| React Native Paper | ^5.12.0 | https://callstack.github.io/react-native-paper/docs/guides/getting-started/ |
| Supabase JS | ^2.49.0 | https://supabase.com/docs/reference/javascript/start |

### SDK 55 Migration Notes

- `lib/image.ts` uses `expo-file-system/legacy` for the existing base64 upload path.
- `lib/notifications.ts` uses `shouldShowBanner` + `shouldShowList` for foreground notification display.
- `expo-system-ui` is installed because `userInterfaceStyle` is configured.
- `android/` and `ios/` are generated/native folders; rerun prebuild after native config edits.

### Key Documentation Links (Exact Versions)

| Technology | Link | What |
|---|---|---|
| Expo SDK 55 docs | https://docs.expo.dev/versions/v55.0.0/ | SDK 55 package APIs |
| Expo Router docs | https://docs.expo.dev/router/introduction/ | API reference, hooks, navigation |
| Expo Router intro | https://docs.expo.dev/router/introduction/ | File-based routing concepts |
| Expo Router tutorial | https://www.youtube.com/watch?v=FWYiG6OIEJw | Login → Dashboard → Profile flow |
| React Native docs | https://reactnative.dev/docs/getting-started | Getting started guide |
| React Native releases | https://reactnative.dev/blog | Release notes and architecture updates |
| React Native Paper v5 | https://callstack.github.io/react-native-paper/docs/guides/getting-started/ | Setup, PaperProvider, components |
| React Native Paper v5 guide | https://callstack.github.io/react-native-paper/docs/guides/migration-guide-to-5.0/ | Material You design |
| Supabase React Native | https://supabase.com/docs/guides/auth/quickstarts/react-native | Quickstart guide |
| Expo tutorial | https://docs.expo.dev/tutorial/introduction/ | Official step-by-step tutorial |
| Expo EAS Build | https://docs.expo.dev/build/introduction/ | Cloud build for Android/iOS |

---

## Development Resources

### React Native + Expo Tutorials

| Resource | Type | Link |
|---|---|---|
| Expo Tutorial (official) | Docs | https://docs.expo.dev/tutorial/introduction/ |
| React Native Full Course 2026 (Expo) | Video | https://www.youtube.com/watch?v=RdJhqaOIWn0 |
| React Native Full Course 2026 (publish + monetize) | Video | https://www.youtube.com/watch?v=4nVoLX2taFg |
| React Native Tutorial: Build 1st App in 3 Hours | Guide | https://tech-insider.org/react-native-tutorial-mobile-app-complete-guide-2026/ |
| Expo SDK 55 docs | Docs | https://docs.expo.dev/versions/v55.0.0/ |

### Supabase + React Native

| Resource | Type | Link |
|---|---|---|
| Supabase React Native quickstart (official) | Docs | https://supabase.com/docs/guides/auth/quickstarts/react-native |
| Supabase Setup in React Native Expo 2026 | Video | https://www.youtube.com/watch?v=o5C6cEEAKkI |
| Pocket Backend: React Native CRUD with Supabase | Blog | https://weblianz.com/blog/pocket-backend-react-native-crud-with-supabase |
| Build CRUD App with React + Supabase | Guide | https://adevait.com/react/building-crud-app-with-react-js-supabase |

### EAS Build + Deployment

| Resource | Type | Link |
|---|---|---|
| EAS Build docs (official) | Docs | https://docs.expo.dev/build/introduction/ |
| Build profiles config | Docs | https://docs.expo.dev/build/eas-json/ |
| Submit to app stores | Docs | https://docs.expo.dev/submit/introduction/ |
| Expo dev workflow 2026 | Blog | https://irfanqutab.dev/blog/expo-developer-workflow-2026 |

### Mobile App Architecture

| Resource | Type | Link |
|---|---|---|
| 9 Mobile App Architecture Best Practices | Guide | https://nextnative.dev/blog/mobile-app-architecture-best-practices |
| React Native Architecture (2026) | Blog | https://medium.com/@silverskytechnology/react-native-architecture-explained-2026-edition |
| React Design Patterns 2025 | Guide | https://www.telerik.com/blogs/react-design-patterns-best-practices |

### AI Integration

| Resource | Type | Link |
|---|---|---|
| OpenRouter quickstart | Docs | https://openrouter.ai/docs/quickstart |
| OpenRouter API reference | Docs | https://openrouter.ai/docs/api/reference/overview |
| OpenRouter models catalog | List | https://openrouter.ai/models |
| OpenRouter React Native integration | Guide | https://openrouter.ai/docs/guides/community/frameworks-and-integrations-overview |

---

## Notification System — Privacy-by-Default Details (2026-04-25)

### Default State

When a child is created via the 5-step wizard, the `notifications` JSONB column is initialized with all 10 toggles set to `false`:

```json
{
  "bedtime": false, "wake_up": false,
  "breakfast": false, "lunch": false, "snack": false, "dinner": false,
  "nap": false, "activity": false, "learn": false,
  "weekly_growth": false
}
```

### Schedule Flow

1. Wizard saves child profile
2. Wizard calls `updateChildSettings(child.id, { notifications: defaultNotifs })`
3. Wizard calls `scheduleChildNotifications(updatedChild, defaultNotifs)`
4. `scheduleChildNotifications()` iterates routine keys; each is skipped because `notifToggles[key] === false`
5. Result: **0 notifications scheduled** on device

### Existing Children (No Migration)

Children created before this change retain their existing `notifications` JSONB value. If they were created before the `notifications` column existed, the column is `null` and `scheduleChildNotifications()` treats all routines as enabled (legacy fallback). No data migration is required.

### Debug Log Levels

| Level | When | Example |
|-------|------|---------|
| Toggle | Immediate on switch | `[ChildSettings] snack toggled OFF ❌` |
| Save | After handleSave | `[ChildSettings] Saved with 3 OFF for Emma: snack, nap, weekly_growth` |
| Skip | Inside scheduler | `[Notifications] snack for Emma — toggle OFF, skipping` |
| Bulk | Master toggle | `[Profile] All notifications OFF for all children` |
| OS | After cancelAll | `[Notifications] Cancelled 7 OS + 7 tracked for child abc-123` |

All logs are `__DEV__`-guarded (`if (__DEV__) console.log(...)`).

---

## AI Insights — Recency Rank Algorithm (2026-04-25)

### Filtering Pipeline

```
raw recommendations
  → apply active filter (category/priority)
  → group by rec.category
  → sort each group by created_at desc
  → slice each group to top 3
  → assign recencyRank: 0=Latest, 1=2nd, 2=Oldest
  → flatten back to single array
  → sort by category name → created_at desc
  → apply pagination (show 5, load more +5)
```

### Recency Badge Rendering

```typescript
const RECENCY_LABELS = ['Latest', '2nd Latest', 'Oldest'];
const RECENCY_COLORS = ['#22C55E', '#F59E0B', '#94A3B8']; // green, amber, slate
```

Badge appears in card footer, left-aligned, alongside the creation date (right-aligned).

---

## Related

- [[concepts/smart-parenting-app-tech-stack]] — Tech stack overview
- [[concepts/hci-design-principles-mobile]] — HCI design principles applied to this app
- [[sources/operational/2026-04-12-smart-parenting-session]] — First codebase ingestion
- [[sources/operational/2026-04-12b-smart-parenting-codebase-reingestion]] — Post-settings re-ingestion
- [[sources/operational/2026-04-10-smart-parenting-ui-redesign]] — UI redesign session
- [[sources/operational/2026-04-14-smart-parenting-feature-session]] — Feature dev session (child picker, settings, time range)
- [[sources/operational/2026-04-25-spa-ai-insights-notification-ux-session]] — This session
