---
id: smart-parenting-app-tech-stack-001
type: concept
created: 2026-04-10
updated: 2026-05-07
last_verified: 2026-05-07
review_after: 2026-07-06
stale_after: 2026-09-04
confidence: high
source_refs:
  - raw/articles/smart-parenting-app-codebase-2026-04-18
  - sources/operational/2026-04-16-spa-gender-bmi-ui-fixes-session
  - sources/operational/2026-04-18-spa-time-input-centering-session
  - sources/operational/2026-04-19-spa-add-child-hci-validation-session
  - sources/operational/2026-04-23-spa-dashboard-scheduled-activities-session
  - sources/operational/2026-04-23-spa-hci-alert-fix-session
  - sources/operational/2026-04-23-spa-qa-baseline-session
  - sources/operational/2026-04-23-spa-schedule-reminder-session
  - sources/operational/2026-04-23-spa-update-schedule-modal-refactor
  - sources/operational/2026-04-23-spa-final-product-dual-agent-qa-plan
  - sources/operational/2026-04-23-spa-hci-alert-fix-session
  - sources/operational/2026-04-24-spa-meal-time-logging-session
  - sources/operational/2026-04-24-spa-sdk55-schema-migration-session
  - sources/operational/2026-04-25-spa-ai-recommendation-category-normalization
  - sources/operational/2026-04-25-spa-consolidated-database-schema
  - sources/operational/2026-04-25-spa-ai-insights-notification-ux-session
  - sources/operational/2026-05-01-spa-history-activity-crud-phase2
  - sources/operational/2026-05-01-spa-history-activity-crud-ui
  - sources/operational/2026-05-05-spa-notification-orphan-fixes
  - sources/operational/2026-05-07-spa-rls-stale-cache-bypass
status: active
tags:
  - react-native
  - expo
  - supabase
  - openrouter
  - mobile-dev
  - smart-parenting-app
  - expo-notifications
  - bmi-calculator
related:
  - concepts/llm-applied-learning-path
  - concepts/hci-design-principles-mobile
  - concepts/react-native-text-input-centering
  - analyses/smart-parenting-app-final-product-qa-plan
  - sources/operational/2026-04-12-smart-parenting-session
  - sources/operational/2026-04-12b-smart-parenting-codebase-reingestion
  - concepts/who-bmi-calculator
  - sources/operational/2026-05-07-spa-rls-stale-cache-bypass
---

# Smart Parenting App — Tech Stack

**Project:** Smart Parenting App (NestNote) — AI-Based Child Activity Monitoring
**Platforms:** Android + iOS (Expo EAS)
**Repo:** ~/local-projects/smart-parenting-app/
**Branch:** feature/ui-redesign-nestnote (5 tabs, coral theme finalized)

---

## Tech Stack (Verified from package.json)

| Layer | Technology | Version | Role |
|---|---|---|---|
| Framework | React Native | 0.83.6 | Cross-platform mobile |
| Platform | Expo SDK | ~55.0.0 | Tooling, builds, modules |
| Routing | Expo Router | ~55.0.13 | File-based routing |
| Auth + DB | Supabase | ^2.49.0 | Auth, PostgreSQL, RLS |
| State | Zustand | ^5.0.0 | Client state management |
| UI | React Native Paper | ^5.12.0 | Material Design 3 components |
| Forms | react-hook-form + zod | ^7.54.0 / ^3.24.0 | Form validation |
| Charts | react-native-chart-kit | ^6.12.0 | Activity charts |
| AI | OpenRouter API | env-driven model | Child activity analysis via Supabase Edge Function |

---

## React Native + Expo

**What:** Framework for building native mobile apps with JavaScript/TypeScript. Expo adds tooling, cloud builds, and pre-built modules.

**Key docs:**
- Expo docs: https://docs.expo.dev/
- Expo Router (file-based routing): https://docs.expo.dev/router/introduction/
- Expo SDK 55 docs: https://docs.expo.dev/versions/v55.0.0/
- React Native Directory (library search): https://reactnative.directory/

**Quick start:**
```bash
npx create-expo-app@latest smart-parenting-app
cd smart-parenting-app
npx expo install expo-router expo-dev-client
npx expo start
```

**Key concepts:**
- File-based routing (like Next.js App Router)
- Expo Go for development (phone simulator)
- EAS Build for production APKs
- OTA updates (push code changes without app store)

**Why Expo over bare React Native:**
- No Android Studio / Xcode setup for development
- Cloud builds via EAS
- Pre-built modules (camera, notifications, storage)
- Faster iteration cycle

- `lib/database.types.ts` now includes `scheduled_activities.food_groups` from the linked Supabase schema (regenerated 2026-04-24 after applying the additive v3 migration).
- `database/schema.sql` is now the single consolidated database bootstrap file (2026-04-25); former incremental migration SQL files were folded into it, and optional seed data was renamed to `seed_test_account.sql.template` so `schema.sql` is the only `.sql` under `database/`.
- SDK 55 compatibility: current upload code imports legacy base64 APIs from `expo-file-system/legacy`; notification foreground behavior uses `shouldShowBanner` + `shouldShowList`.

---

## UI Patterns (Verified from Codebase)

### Coral Theme Tokens (applied 2026-04-12)

```
Primary:        #FF7F60  (coral/salmon)
PrimaryContainer: #FFE5E0
Background:     #FEFBF6  (cream)
Surface:        #FFFDFF  (near-white)
Error:          #EF4444
OnSurface:      #0F172A
Outline:        #E2E8F0
```

Activity category colors preserved: screenTime=#FF7F60, sleep=#10B981, meals=#F59E0B, education=#8B5CF6.

### Welcome/Goodbye Animation Pattern

Used on login (welcome) and sign-out (goodbye). Pattern:
```tsx
// Parallel animation: fade in + spring scale
Animated.parallel([
  Animated.timing(opacity, { toValue: 1, duration: 400, useNativeDriver: true }),
  Animated.spring(scale, { toValue: 1, friction: 6, useNativeDriver: true }),
]).start(() => {
  // Show for 1.2s, then fade out
  setTimeout(() => {
    Animated.timing(opacity, { toValue: 0, duration: 300, useNativeDriver: true }).start();
  }, 1200);
});
```

Auth guard in `_layout.tsx` delays redirect by 1.8s to let the animation play.

### Sign-Out Confirmation Modal

Modal (transparent, fade animationType) with centered card. Pattern:
- Overlay: `rgba(0,0,0,0.4)`, dismissible on background tap
- Card: white, 24px borderRadius, icon + title + text + Cancel/Sign Out buttons
- Cancel: `#F1F5F9` background, gray text
- Sign Out: `#EF4444` background, white text

### Settings Screen Architecture (profile.tsx — 532L)

Reusable components: `Section` (title + card wrapper), `Item` (icon + label + description + trailing), `ChildCard` (avatar + name + age). Sections: Account, Children, Notifications (Switch toggles), Privacy & Security, Support.

### History Screen (history.tsx — 564L, NEW 2026-04-13)

SectionList with date-grouped sections (Today, Yesterday, full weekday date). Filter pills horizontal scroll (All + 6 types). Child picker cycles via avatar tap. Activity cards show type icon + formatted label + time. States: loading spinner, error with retry button, empty state with CTA. Pull-to-refresh with coral tint. Uses `useFocusEffect` to reload on tab focus.

Key helpers:
- `groupByDate()` — groups activities by ISO date key, sorts newest-first
- `getActivityLabel()` — formats each type with duration, quality, device/food/subject
- `getSectionTitle()` — Today/Yesterday/locale date string

### Tab Navigation (5 tabs — updated 2026-04-13)

```
Dashboard → Log → History → AI Insights → Settings
home      → add  → time    → bulb        → settings
```

Tab bar: 80px Android, 100px iOS. `tabBarShowLabel: true`. Coral active tint (#FF7F60).

---

## New Features (2026-04-14)

### Screen Time Category
- Screen time logs now have a `category` field: `leisure` or `educational`
- Log screen shows Category selector (Leisure / Educational) before Device selector
- Display: `Screen time (leisure) — 1h 30m on phone`

### Time Range Input (Sleep/Nap/Education/Physical)
- Replaced manual hours/minutes stepper with Start → End time picker
- Vertical layout (Start ↓ End) to fit mobile screens
- Auto-calculates duration from start/end times
- Supports overnight (e.g., 9PM → 6AM = 9h)
- Screen time still uses manual hours/minutes

### Meal Time Logging (updated 2026-04-24)
- Manual meal logs capture a single `start_time` in the activity `value` JSONB payload.
- Meal time uses the compact `RNTextInput` + wrapper View pattern for Android-safe vertical centering.
- Dashboard and History labels display saved meal time as `Meal @ H:MM AM/PM` when present.

### Per-Child Settings
- DB: `max_screen_time_minutes` and `min_sleep_minutes` columns on `children` table
- Settings modal on tap of child card in Settings screen
- Presets: Screen time (30m/1h/1.5h/2h/3h/none), Sleep (8-12h/none)
- Saved to Supabase via `updateChildSettings()` API

### Child Picker Modal (History)
- History screen child selector now opens a modal listing all children
- Previously cycled round-robin on tap

---

## AI Recommendation Flow (2026-04-25, verified 2026-05-07)

**Pattern:** Stateless zero-shot prompting with context injection plus deterministic post-model validation.

**Flow:**
1. Parent taps "Run AI Insights" on AI tab
2. `analyzeChild()` fetches in parallel: 28-day activity summary, last 3 recommendations, child profile
3. Edge Function aggregates raw activities into structured stats (sleep avg, screen time breakdown, meal frequency, etc.)
4. Builds zero-shot prompt: system role + child profile + activity summary + previous recommendations
5. Calls OpenRouter API via the `OPENROUTER_MODEL` environment variable; live repo default is `inclusionai/ling-2.6-1t:free`
6. Parses AI JSON response, normalizes recommendation categories/metadata, then inserts into `recommendations` table with `based_on` audit trail
7. App reloads recommendations from DB, displays with category badges + priority colors

**Category hardening (2026-04-25):** The Edge Function no longer trusts raw model category output. Allowed categories are exactly `screen_time`, `sleep`, `meal`, `education`, `physical_activity`, and `general`. Legacy/ambiguous outputs are normalized deterministically: `nutrition` → `meal`, `activity` → inferred from cited content, and generic scheduled/routine activity advice → `general`. `physical_activity` is only used when movement evidence is explicit.

**Caching:** Recommendations cached until next day. `isToday()` check skips API call if recs already generated today.

**Audit trail (`based_on` JSONB):**
```json
{
  "period": "2026-03-17 to 2026-04-14",
  "activity_summary": { "sleep": {...}, "screen_time": {...}, "meals": {...} },
  "previous_rec_ids": ["uuid-1", "uuid-2"],
  "child_settings": { "max_screen_time_minutes": 120, "min_sleep_minutes": 540 },
  "model": "inclusionai/ling-2.6-1t:free"
}
```

**Edge Function:** `supabase/functions/analyze-child/index.ts` (329 lines)
- Activity aggregation (group by type, compute stats)
- Prompt engineering (child development advisor role)
- OpenRouter API call with env-driven model selection; current code default is `inclusionai/ling-2.6-1t:free`
- Supabase REST insert with service role key (bypasses RLS)

**Model drift note (2026-05-07):** a user handoff reported a switch to `baidu/cobuddy:free`, but live code still defaults to `inclusionai/ling-2.6-1t:free`. Treat the provider path as operationally mutable until runtime config or a code diff confirms the switch.

## Child soft-delete RPC bypass (2026-05-07)

Direct `children` updates for soft-delete were replaced with `supabase.rpc('soft_delete_child', { child_id })` after the APK kept hitting a stale PostgREST view of the `children_update` policy. The consolidated schema now documents the fix in two layers:
- `children_update` allows `WITH CHECK (parent_id = auth.uid())` without a `deleted_at IS NULL` self-contradiction on the new row.
- `soft_delete_child(child_id UUID)` is a `SECURITY DEFINER` RPC that re-checks ownership internally before setting `deleted_at = NOW()`.

This keeps authorization anchored in the database while bypassing a temporarily untrustworthy REST policy cache path. See [[sources/operational/2026-05-07-spa-rls-stale-cache-bypass]].

## Uniform Headers (2026-04-14)

**Component:** `components/ScreenHeader.tsx` — shared across Log, History, AI Insights screens.

**Layout:** Icon + title on left, child picker pill (avatar + name + chevron) on right.

**Child picker:** Tap → modal with all children → select → updates globally via Zustand.

**HCI principles applied:** Consistency & Standards (#4), Recognition over Recall (#6), User Control (#3), Visibility of System Status (#1).

---

## Related Sections
*Detailed content split into sub-pages for readability. See [[concepts/smart-parenting-app-tech-stack-details]] for the full reference.*
*Client-facing handover documentation: [[concepts/smart-parenting-app-client-handover]]*
*System architecture overview: [[concepts/smart-parenting-app-system-architecture]]*

Session documentation: [[sources/operational/2026-04-12-smart-parenting-session]], [[sources/operational/2026-04-12b-smart-parenting-codebase-reingestion]], [[sources/operational/2026-04-10-smart-parenting-ui-redesign]], [[sources/operational/2026-04-14-smart-parenting-feature-session]], [[sources/operational/2026-04-23-spa-dashboard-scheduled-activities-session]]

---

## Dashboard Scheduled Activities (2026-04-23)

The Dashboard "Upcoming" section displays pending `scheduled_activities` rows. Each card shows type icon, date label ("Today" or short date), time range, and up to 3 action buttons.

### UpcomingItem Card Layout

```
├───────────────────────────────────────────────────┐
│  📱 Screen        [Today]                  │  ← top row (icon + meta + badge)
│  3:00 PM → 5:00 PM  · up to 2h             │
│                                         │
│  Log    Update    Cancel                │  ← action row (3 buttons)
└───────────────────────────────────────────────────┘
```

Card container: `flexDirection: 'column'` (default), white surface, 14px radius, 1px `#E2E8F0` border.

### Three Actions

| Button | Behavior | API Call |
|---|---|---|
| **Log** | Opens `LogConfirmModal` (meal: quality + food groups + meal type + notes; others: notes only). Log button only appears once `start_time <= now`. | `logActivity()` + cancel schedule-specific reminders |
| **Update** | Opens `UpdateScheduleModal` slide-up sheet | `updateScheduledActivity()` + reschedule one-off reminders |
| **Cancel** | Inline confirmation: "Delete this schedule permanently?" → Keep / Delete | `deleteScheduledActivity()` + cancel one-off reminders |

### Log — Confirmation Modal Mapping

Duration is still taken from `max_duration_minutes`, but the log flow is now user-confirmed before insertion.

- **meal**: parent chooses `meal_type`, `quality`, `food_groups`, optional `notes`
- **screen_time / sleep / nap / physical_activity / education**: optional `notes` only
- After successful log, schedule-specific one-off reminders for that schedule are cancelled

### UpdateScheduleModal

Slide-up modal with 3 sections:
1. **Type picker** — 6 chips, color-coded border on active
2. **Start Time** — CompactTimeBlock pattern: stepper ±, RNTextInput, AM/PM toggles
3. **Min / Max Allotted Duration** — hour/minute inputs with fixed-width digit columns (`modalCompactRow`)
4. **Category or Meal Type** — tailored chip sets per activity type:
   - Screen Time: `leisure`, `educational`
   - Physical Activity: `sports`, `playground`, `outdoor`, `other`
   - Education: `reading`, `math`, `science`, `art`, `music`, `other`

**Time conversion:**
- Open: ISO `start_time` → 12h `{h, m, p}` via `to12h()`; `min_duration_minutes` / `max_duration_minutes` → hour/minute breakdown
- Save: 12h → 24h via `from12h()`, reconstruct ISO on base date. `planned_end_time` auto-computed from `start_time + max_duration_minutes`.

**Live range preview:** Green card shows calculated loggable window in real time:
- `3:00 PM → 3:30 PM – 4:00 PM` (when min ≠ max)
- `3:00 PM → 4:00 PM` (when min = max)

### Hard-Delete Cancel

Old behavior: `updateScheduledActivityStatus(id, 'skipped')` — row persisted.
New behavior: `deleteScheduledActivity(id)` — `DELETE FROM scheduled_activities WHERE id = $1`. Row gone permanently. Inline confirmation prevents accidents.

### One-Off Schedule Reminders (2026-04-23)

Each pending `scheduled_activities` row now schedules up to **2 local notifications**:
- `scheduled-min-{scheduleId}` → `start_time + min_duration_minutes - 5 minutes`
- `scheduled-max-{scheduleId}` → `start_time + max_duration_minutes - 5 minutes`

Rules:
- Past triggers are skipped
- If min/max resolve to the same time, only the max reminder is scheduled
- Updating a schedule cancels and rebuilds its reminders
- Cancelling or logging from the card cancels remaining schedule-specific reminders

## Final Product QA Strategy (2026-04-23)

Smart Parenting QA now has two layers:

1. **Baseline QA** — static audit + severity-ranked fixes
2. **Final Product QA** — release-candidate validation focused on runtime correctness, end-to-end parent flows, failure handling, data integrity, performance, and codebase bloat

The final-product track is designed for **two concurrent agents**:
- **MiniMax-M2.7** → compliance auditor for checklist validation, data integrity, security assumptions, release gating, and bloat review
- **Kimi-K2.6** → product dogfooder for end-to-end flow testing, HCI friction detection, runtime behavior checks, and edge-case reproduction

Phases 3–9 cover:
- runtime product validation
- core flow certification
- failure and edge-case behavior
- data integrity and security validation
- performance and bloat audit
- release-candidate readiness
- final ship/no-ship sign-off

Hard ship gate:
- 0 known Critical issues
- 0 known High issues
- 0 dead primary actions
- 0 unresolved console/runtime errors in certified flows
- 0 must-fix bloat findings

See [[analyses/smart-parenting-app-final-product-qa-plan]] for the detailed dual-agent execution design.

---

## AI Insights Screen — UX Redesign (2026-04-25)

### Category Capping + Recency Badges

The AI Insights screen now limits each category to **3 most recent recommendations** and surfaces **recency** to help parents identify what changed:

- **Max 3 per category** — `screen_time`, `sleep`, `meal`, `education`, `physical_activity`, and `general` each show their 3 newest recommendations
- **Creation date** on every card footer (`MMM D, YYYY`)
- **Recency badge:**
  - 🟢 **Latest** — newest in that category (today or most recent run)
  - 🟡 **2nd Latest** — second most recent
  - ⬜ **Oldest** — third most recent (still within the 3-cap)
- **Sort order:** Grouped by category name alphabetically, then date descending within each group
- **Filter interaction:** Active filters apply before the cap. Filtering to "Sleep" shows only the 3 most recent Sleep recommendations.
- **Pagination:** "Load More" works on the post-capped list (shows next 5 items regardless of category)

This prevents information overload when the AI generates many recommendations across categories while preserving the ability to see full history via Load More or filter.

---

## Notification System — Privacy-by-Default (2026-04-25)

### Problem

Previously, creating a child immediately scheduled **all 10 routine notifications** on the device. Parents received surprise alerts without having explicitly opted in.

### Solution

New children are created with all notification toggles **OFF by default**. Parents must explicitly enable each routine notification they want:

| Routine | Default | Opt-In Location |
|---------|---------|-----------------|
| Bedtime | OFF | Settings → Child → Bedtime toggle |
| Wake Up | OFF | Settings → Child → Wake Up toggle |
| Breakfast | OFF | Settings → Child → Breakfast toggle |
| Lunch | OFF | Settings → Child → Lunch toggle |
| Snack | OFF | Settings → Child → Snack toggle |
| Dinner | OFF | Settings → Child → Dinner toggle |
| Nap | OFF | Settings → Child → Nap toggle |
| Activity | OFF | Settings → Child → Activity toggle |
| Learn | OFF | Settings → Child → Learn toggle |
| Weekly Growth | OFF | Settings → Child → Weekly Growth toggle |

### Implementation

- Wizard (`app/child/wizard.tsx`) saves `defaultNotifs` (all `false`) to Supabase via `updateChildSettings()` before calling `scheduleChildNotifications()`
- `scheduleChildNotifications()` skips any type whose toggle is `false`
- Existing children retain their saved `notifications` JSONB value — no migration needed
- Master toggle in Settings → Notifications still works globally (cancels all / re-enables all)

### Debug Logging

Every toggle flip and save action now emits `__DEV__`-guarded console logs:
- Toggle action: `[ChildSettings] snack toggled OFF ❌`
- Save summary: `[ChildSettings] Saved with 3 notification(s) OFF for Emma: snack, nap, weekly_growth`
- Scheduler skip: `[Notifications] snack for Emma — toggle is OFF, skipping`
- Master toggle: `[Profile] All notifications turned OFF for all children`

See [[concepts/expo-local-notifications]] for full notification architecture details.

---

## Schedule Creation Redirect (2026-04-25)

After creating a scheduled activity from the Log tab, the app now **instantly redirects to the History tab** instead of staying on the Log form:

```typescript
// app/(tabs)/log.tsx
router.replace('/(tabs)/history');  // was: '/(tabs)' (Dashboard)
```

Rationale: after scheduling, the parent's next need is to **verify and manage** upcoming activities. The History tab (now "Schedule" tab) shows all pending scheduled activities with Log / Update / Cancel actions. Using `replace` (not `push`) prevents back-navigation to the filled form.

---

## Related Sections
