---
id: smart-parenting-ui-redesign-2026-04-10
type: source
created: 2026-04-11
updated: 2026-04-11
last_verified: 2026-04-11
review_after: 2026-05-11
stale_after: 2026-07-11
confidence: high
status: active
source_refs:
  - ~/local-projects/v0.app/
  - ~/local-projects/smart-parenting-app/
tags:
  - smart-parenting-app
  - react-native
  - expo
  - ui-redesign
  - hci
  - commission
related:
  - concepts/smart-parenting-app-tech-stack
  - concepts/mldc-mobile-development-lifecycle
  - concepts/hci-design-principles-mobile
---

Related: [[sources/operational/2026-04-10-android-build-debugging]], [[concepts/hci-design-principles-mobile]]
# Smart Parenting App — UI Redesign Session (2026-04-10/11)

**Session:** 2026-04-10 23:37 → 2026-04-11 ~02:00
**Branch:** `feature/ui-redesign-nestnote` (14 commits)
**Source:** v0.app design ("NestNote") in `~/local-projects/v0.app/`
**Target:** `~/local-projects/smart-parenting-app/`

---

## What Happened

Ported a v0.app-generated Next.js/Tailwind design ("NestNote") to the existing React Native + Expo Smart Parenting App. Applied HCI principles throughout. Fixed multiple runtime bugs discovered during testing.

---

## Commits (14 total)

| # | Hash | Description |
|---|---|---|
| 1 | `b9436e5` | Port Login + Signup screens from v0 design |
| 2 | `c1a5e4b` | Port Dashboard + Tabs layout |
| 3 | `da0b5fc` | Port Log Activity screen |
| 4 | `8b7c024` | Port AI Insights screen |
| 5 | `4056a47` | Port Profile/Settings screen |
| 6 | `94a7321` | Redesign Add Child screen with HCI |
| 7 | `20c1984` | Fix createChild — add parent_id to insert |
| 8 | `4e83bc1` | Fix auth flow — login as root, confirm password, email confirmation |
| 9 | `a773017` | Dashboard shows real activity data + local AI analysis |
| 10 | `64a25e8` | Fix data loading race condition |
| 11 | `14bd1e1` | HCI feedback — inline validation, success screens |
| 12 | `553d143` | Log screen overhaul — 6 types, text input, meal details |
| 13 | `37bd024` | Multi-child display + nav bar sizing |
| 14 | `f45e2f3` → `7ef4e79` | Welcome/goodbye animations + fade out |

---

## Key Bugs Fixed

### 1. RLS parent_id Missing on Insert
- **Symptom:** Create child did nothing, silent failure
- **Root cause:** `createChild()` didn't pass `parent_id`. RLS `WITH CHECK (parent_id = auth.uid())` rejected NULL.
- **Fix:** Fetch `user.id` from Zustand auth store, pass directly.

### 2. Auth Guard Catches Stale Closure
- **Symptom:** Dashboard showed no data until logout/login
- **Root cause:** `loadChildren()` updated Zustand store, but `loadTodayData()` ran with stale `selectedChild` from closure.
- **Fix:** Use `useApp.getState().selectedChild.id` to read fresh state.

### 3. Child Selection Resets on Focus
- **Symptom:** Tapping a child chip highlights briefly, then reverts
- **Root cause:** `loadChildren()` always set `selectedChild = children[0]`.
- **Fix:** Check if current selection still exists in fetched list before overwriting.

### 4. signUp Auto-Login Without Email Confirmation
- **Symptom:** Signup → dashboard → logout → can't login
- **Root cause:** Supabase requires email confirmation by default. `signUp` set `user` in store, auth guard redirected to dashboard, but login failed because email wasn't confirmed.
- **Fix:** `signUp` no longer auto-logs-in. Shows "Account Created" alert → redirect to login.

### 5. Alert.alert Doesn't Work on Web
- **Symptom:** Sign out button did nothing
- **Root cause:** `Alert.alert` doesn't render in Expo web.
- **Fix:** Custom Modal component for sign out confirmation.

### 6. Login Animation Killed by Auth Guard
- **Symptom:** "Welcome back!" never showed
- **Root cause:** Auth guard called `router.replace('/(tabs)')` immediately when `user` was set.
- **Fix:** 1.8s delay on auth-to-tabs redirect.

---

## UI Architecture After Redesign

```
app/
├── (auth)/
│   ├── login.tsx      — NestNote branding, gradient-style button, social login
│   └── signup.tsx     — Confirm password, strength meter, inline validation
├── (tabs)/
│   ├── _layout.tsx    — 4 tabs: Home, Log, Insights, Settings
│   ├── index.tsx      — Dashboard: children selector, stats, activity feed
│   ├── log.tsx        — 6 activity types, child picker, stepper + text input
│   ├── ai.tsx         — Local analysis from activity data, filters
│   └── profile.tsx    — Parent profile, settings sections, sign out animation
├── child/
│   └── new.tsx        — HCI form: quick age, validation, privacy note
└── _layout.tsx        — Auth guard with animation delay
```

---

## Design Tokens

| Token | Value |
|---|---|
| Primary | `#3B82F6` |
| Text | `#0F172A` |
| Muted | `#64748B` |
| Surface | `#F8FAFC` |
| Card | `#FFFFFF` |
| Border | `#E2E8F0` |
| Screen Time | `#3B82F6` / `#EFF6FF` |
| Sleep | `#10B981` / `#ECFDF5` |
| Nap | `#8B5CF6` / `#F5F3FF` |
| Meals | `#F59E0B` / `#FFFBEB` |
| Physical | `#EF4444` / `#FEF2F2` |
| Education | `#6366F1` / `#EEF2FF` |
| Border radius | 14-20px (cards), 12px (inputs), 16px (buttons) |

---

## Database Migration Needed

```sql
ALTER TABLE activities DROP CONSTRAINT IF EXISTS activities_type_check;
ALTER TABLE activities ADD CONSTRAINT activities_type_check
  CHECK (type IN ('screen_time', 'sleep', 'nap', 'meal', 'physical_activity', 'education'));
```

Until migration is run, app maps: `nap → sleep`, `physical_activity → education` with original type in JSON value.

---

## Related
- [[concepts/smart-parenting-app-tech-stack]] — tech stack reference
- [[concepts/mldc-mobile-development-lifecycle]] — development methodology
- [[concepts/hci-design-principles-mobile]] — HCI principles applied
