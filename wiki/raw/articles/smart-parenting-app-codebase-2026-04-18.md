# Smart Parenting App — Codebase Ingestion (2026-04-18)

**Source:** ~/local-projects/smart-parenting-app/ (live codebase)
**Date:** 2026-04-18
**Branch:** feature/ui-redesign-nestnote
**Commit:** 20373a7 (docs: mark Milestone 2 complete in SCOPE.md)
**Commits since last ingestion (2026-04-12b):** 9 commits

## Project Overview

AI-based child activity monitoring mobile application. Freelance commission (₱12K total). React Native + Expo + Supabase + OpenRouter.

---

## Tech Stack (from package.json — UPDATED 2026-04-18)

| Layer | Technology | Version | Notes |
|---|---|---|---|
| Framework | React Native | **0.76.9** | Was 0.76.3 |
| Platform | Expo SDK | ~52.0.0 | |
| Routing | Expo Router | ~4.0.0 | |
| Database/Auth | Supabase JS | ^2.49.0 | |
| State | Zustand | ^5.0.0 | |
| UI | React Native Paper | ^5.12.0 | |
| Forms | react-hook-form + zod | ^7.54.0 / ^3.24.0 | |
| Charts | react-native-chart-kit | ^6.12.0 | |
| Storage | AsyncStorage | ^2.1.0 | |
| Build | Expo EAS | (eas.json present) | |
| **NEW** | expo-keep-awake | ~14.0.3 | Prevent screen sleep during activities |
| **NEW** | expo-secure-store | ~14.0.1 | Secure credential storage |
| **NEW** | expo-font | ~13.0.4 | Custom fonts |
| **NEW** | expo-asset | ~11.0.5 | Asset bundling |
| **NEW** | expo-device | ~7.0.3 | Device info for notifications |
| **NEW** | date-fns | ^4.1.0 | Date manipulation |

---

## Directory Structure

```
smart-parenting-app/
├── app/
│   ├── _layout.tsx              # Root: PaperProvider + Stack + auth guard (86L)
│   ├── (auth)/
│   │   ├── _layout.tsx
│   │   ├── login.tsx            # 473L — welcome animation, social placeholders
│   │   └── signup.tsx          # 593L
│   ├── (tabs)/
│   │   ├── _layout.tsx          # 82L — 5-tab navigator
│   │   ├── index.tsx           # 785L — Dashboard
│   │   ├── log.tsx             # 880L — Activity logger (6 types)
│   │   ├── history.tsx         # 770L — History with calendar + filters
│   │   ├── ai.tsx              # 457L — AI recommendations
│   │   └── profile.tsx          # 765L — Settings
│   └── child/
│       ├── new.tsx             # 388L — Add child
│       └── routine.tsx         # 719L — 4-step routine wizard
├── lib/
│   ├── supabase.ts             # Lazy-load Supabase client (41L)
│   ├── api.ts                  # Full CRUD + AI analysis (209L) — UPDATED
│   ├── bmi.ts                  # WHO BMI-for-age calculator (201L) — NEW
│   ├── notifications.ts        # Local scheduled notifications (243L) — NEW
│   └── database.types.ts       # Supabase generated types (340L)
├── stores/
│   └── auth.ts                 # Zustand auth + app state (71L)
├── database/
│   ├── schema.sql              # Full schema, 4 tables, RLS (201L)
│   ├── migration_add_activity_types.sql
│   ├── migration_child_routine.sql
│   ├── migration_child_settings.sql
│   └── migration_gender.sql
├── supabase/
│   └── functions/
│       └── analyze-child/
│           └── index.ts        # Edge Function (328L) — AI analysis
├── assets/
├── SCOPE.md                    # Project scope — ₱12K, M2 Done (212L)
└── package.json
```

---

## Database Schema (schema.sql — VERIFIED)

### Tables

1. **children** — parent_id (FK auth.users), name, date_of_birth, soft-delete (deleted_at), routine schedule (bedtime/wake_up/meal times/activity times), per-child limits (max_screen_time, min_sleep), physical (height_cm, weight_kg, bmi), gender
2. **activities** — child_id, type, value (JSONB), recorded_at
3. **recommendations** — child_id, content, category, priority, based_on (JSONB audit trail)
4. **alerts** — child_id, type, message, severity, acknowledged

### CHECK Constraint Discrepancy (KNOWN ISSUE)
Schema CHECK constraint: `type IN ('screen_time', 'sleep', 'meal', 'education')` — **nap and physical_activity NOT in constraint** despite migrations. Migration files exist but constraint gap means:
- `nap` and `physical_activity` activities are being logged via the app but would fail if inserted via direct SQL that validates the constraint.

### RLS Policies
All 4 tables: separate SELECT/INSERT/UPDATE/DELETE policies using subquery pattern:
- children: `parent_id = auth.uid() AND deleted_at IS NULL`
- activities/recommendations/alerts: `child_id IN (SELECT id FROM children WHERE parent_id = auth.uid() AND deleted_at IS NULL)`

### Indexes
- `idx_activities_child_type` (child_id, type)
- `idx_activities_child_recorded` (child_id, recorded_at DESC)
- Single-column: recommendations_child, alerts_child, children_parent

---

## New Libraries (since Apr 12)

### lib/bmi.ts (201L)
WHO BMI-for-age percentile calculator using LMS method.

**Key functions:**
- `calculateBmi(heightCm, weightKg)` → raw BMI
- `assessBmi(heightCm, weightKg, ageMonths, gender)` → `{ bmi, zScore, percentile, category, label }`

**Implementation:**
- WHO LMS tables for boys/girls ages 24-60 months (2-5 years)
- Z-score calculation: `z = ((BMI/M)^L - 1) / (L * S)`
- Percentile: Abramowitz-Stegun normal CDF approximation
- Categories: underweight (<5th), normal (5-85th), overweight (85-95th), obese (>95th)
- Returns null if age < 24 or > 60 months

### lib/notifications.ts (243L)
Local Expo notifications based on child routine schedule.

**Key functions:**
- `requestNotificationPermission()` — handles iOS/Android permissions
- `scheduleChildNotifications(child)` — schedules daily reminders for all routine times
- `cancelChildNotifications(childId)` — cancels all for one child
- `cancelAllNotifications()` — global cancel
- `hasRoutineSet(child)` — checks if child has any routine time set

**Notification triggers (daily):**
- Bedtime reminder: 30 min before scheduled bedtime
- Wake-up check-in: at wake_up_time
- Breakfast/Lunch/Snack/Dinner: at meal times
- Nap/Activity/Learn: at scheduled times

**Pattern:** Expo `Notifications.scheduleNotificationAsync` with `SchedulableTriggerInputTypes.DAILY`. Uses `expo-device` for permission checks. `parseTime()` handles both `HH:MM` and `HH:MM:SS` formats.

### app/child/routine.tsx (719L — UPDATED)
4-step wizard: Sleep → Meals → Activities → Physical.

**Step 4 (Physical) changes since Apr 12:**
- Added gender chip picker (Boy/Girl) — writes to `children.gender`
- BMI calculation now uses actual gender (was hardcoded 'male')
- Added height/weight inputs with unit labels

---

## SCOPE.md — Key Updates (2026-04-18)

- **Total cost:** ₱12,000 (clarified from earlier ambiguous figure)
- **Milestone 1:** Marked complete
- **Milestone 2:** Marked **Done**
- **Milestone 3:** Pending — APK build, Supabase transfer, handover docs, walkthrough

---

## AI Edge Function (analyze-child/index.ts — 328L)

**Flow:**
1. `analyzeChild()` in api.ts fetches 28-day activity summary + last 3 recs + child profile in parallel
2. Edge Function aggregates: screen time (total/avg/leisure/educational breakdown), sleep (avg/min/max/consistency), naps (avg/frequency), meals (avg per day/unique foods), education (total/subjects), physical activity (total/types)
3. Builds zero-shot prompt with child profile, activity summary, previous recommendations
4. Calls `openrouter/elephant-alpha` (free, stateless), temperature 0.7, max_tokens 1024
5. Parses JSON from markdown code block or raw response
6. Inserts recommendations via Supabase REST with service role key (bypasses RLS)
7. Returns saved recommendations with full `based_on` audit trail (period, activity_summary, previous_rec_ids, child_settings, model)

**Caching:** App checks `isToday()` before calling — skips API if recs already generated today.

---

## Known Issues (current as of 2026-04-18)

1. **schema.sql CHECK constraint gap:** `activities.type` only allows `screen_time|sleep|meal|attendance|education` — nap and physical_activity NOT included, despite app-level support and migration files
2. **CLAUDE.md outdated:** Still says SDK 54 and Firebase Auth (actual: SDK ~52.0.0, Supabase Auth)
3. **Notification toggles in Settings:** `notifEnabled` and `weeklyReport` are local state only — not persisted to DB
4. **Placeholder items:** Edit Profile, Change Password, Privacy Settings, Biometric Login, Help & FAQ have no handlers
5. **Social login buttons:** Google/Apple placeholders, no auth providers configured
6. **Gender migration:** Migration file exists but may not have been applied to production Supabase yet

---

## Git History (last 9 commits from 20373a7)

```
20373a7 docs: mark Milestone 2 complete in SCOPE.md
c29949e wip: gender migration, routine screen, history tab, BMI, notifications,
             AI edge function, child settings
7ef4e79 fix: add fade out to welcome and goodbye animations
d16be13 fix: login animation — delay auth guard redirect by 1.8s
f45e2f3 feat: sign out confirmation modal + welcome/goodbye animations
4204d1a fix: remove Contact Support and Rate NestNote from settings
9b2b833 redesign: settings screen with parent profile card + HCI principles
873016c fix: child selection resets on focus — preserve selected child
c5f869e fix: remove active pill from tab bar
```

---

## Milestone Status

| Milestone | Amount | Status |
|---|---|---|
| M1 — Core App | ₱5,000 | Complete |
| M2 — AI & Polish | ₱4,000 | **Done** |
| M3 — Delivery & Handover | ₱3,000 | Pending |
