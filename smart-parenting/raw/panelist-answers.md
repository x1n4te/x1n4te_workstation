---
ingested: 2026-04-25
source_type: panelist-qna
---

# Panelist Questions — Suggested Answers

Defensive answers for capstone/thesis presentation. Each answer is structured as: **Direct answer first**, then **technical justification**, then **acknowledged limitations** (where applicable). Honest about trade-offs.

---

## 1. Architecture & Repository Structure

### File-Based Routing (Expo Router)

**Q: Why Expo Router over React Navigation?**
> Expo Router was chosen because it eliminates the manual route registration boilerplate that React Navigation requires. In a file-based system, adding a new screen is just creating a file — no `Stack.Screen` declarations, no navigator config objects. This reduces the surface area for routing bugs and makes the codebase more approachable for a single-developer project. The trade-off is less runtime flexibility: dynamic routes require route groups and slugs, but our navigation structure is largely static (5 tabs + settings sub-screens), so we don't miss that flexibility.

**Q: How does the `(auth)` / `(tabs)` route group pattern work?**
> The parentheses tell Expo Router that this is a **route group**, not a URL segment. `(auth)/login.tsx` renders at `/login`, not at `/(auth)/login`. This lets us group related screens under a shared layout (`_layout.tsx`) without polluting the URL. The auth group has no tab bar; the tabs group has the bottom tab navigator. The auth guard inspects `segments[0]` to determine which group the user is in and redirects accordingly.

**Q: What if a user manually types a deep link to a protected route while logged out?**
> The root `_layout.tsx` auth guard intercepts every route change. If `user` is null and `segments[0] !== '(auth)'`, it immediately calls `router.replace('/(auth)/login')`. The protected route never mounts. This is a synchronous check on `segments` state, so there's no race window where the protected screen is visible.

**Q: How do you prevent "Attempted to navigate before mounting"?**
> We use an `isMounted` ref initialized in a mount-only `useEffect`. All navigation calls check `isMounted.current` before executing. Additionally, `loadSession()` runs in a `useEffect` with an empty dependency array, so it doesn't fire until after the component tree is fully mounted. The `redirecting` state adds a 1.8s delay for auth-screen redirects, giving the Stack time to initialize.

---

### Auth Guard & Root Layout

**Q: Why is the auth guard in `_layout.tsx` instead of per-screen?**
> Centralizing the guard in the root layout means we write the logic once and it applies to every route in the tree. Per-screen guards would require duplicating the check in every protected file, which guarantees inconsistency over time. The root layout is the single chokepoint for all navigation decisions.

**Q: What happens if `loadSession()` takes longer than 1800ms?**
> The 1800ms timer only governs the *redirect delay after auth is confirmed* — it is not a timeout on `loadSession()`. `loadSession()` can take arbitrarily long; the overlay simply shows "Smart Parenting" until it resolves. In practice, Supabase local session retrieval is under 200ms on a warm start. A network-dependent session refresh might take longer, but that is a legitimate loading state.

**Q: Is the `isMounted` ref pattern sufficient? What about concurrent auth state changes?**
> The `isMounted` ref prevents the most common bug (navigation before mount), but it does not serialize concurrent auth events. Supabase's `onAuthStateChange` fires on a separate microtask, and rapid sign-in/sign-out could theoretically interleave. In practice, our flows have natural user-paced gaps (form submission, animation delays) that prevent this. For a production system at scale, we would queue auth events or use a state machine.

**Q: Why keep the root Stack mounted and use an overlay instead of conditional routing?**
> Conditional routing (`{user ? <Tabs /> : <Auth />}`) unmounts the entire navigation tree on auth change, which destroys all screen state, scroll positions, and form inputs. The overlay preserves the mounted tree while blocking interaction, allowing seamless transitions. When the overlay disappears, the target screen is already rendered underneath.

---

### Project Structure

**Q: Why co-locate screens under `app/` instead of `src/screens/`?**
> Expo Router *requires* the `app/` directory to be the routing root. We could symlink or reconfigure this, but the convention is well-documented and tooling-aware. Co-locating routes, layouts, and route groups in `app/` is idiomatic for Expo Router projects.

**Q: `lib/` mixes API calls, utilities, and business logic. Separation of concerns violation?**
> For a project of this scope (~15k LOC), aggressive modularization creates more friction than value. `lib/api.ts` is the data layer boundary — everything Supabase-related lives there. `lib/bmi.ts` and `lib/sleep-calculator.ts` are pure functions with no side effects. If the project grew beyond 5 developers, we would split into `services/`, `utils/`, and `domain/` directories. At this scale, flat `lib/` is a pragmatic choice.

**Q: Where are your unit tests?**
> The only unit test file is `recommendation-normalizer.test.ts` because the normalizer is the most deterministic, algorithmic piece of code — perfect for unit testing. Most of our logic is UI-bound (forms, navigation, async data fetching), which we validate through integration testing on-device rather than mocked unit tests. Given the ₱12K budget and single-developer constraint, we prioritized end-user validation over test coverage metrics.

---

## 2. Database Schema & Backend

### Row Level Security (RLS)

**Q: Walk me through how RLS prevents cross-parent data access.**
> Every table has RLS enabled. The `children` table policies enforce `parent_id = auth.uid() AND deleted_at IS NULL`. All other tables (activities, recommendations, etc.) use a subquery pattern: `child_id IN (SELECT id FROM children WHERE parent_id = auth.uid() AND deleted_at IS NULL)`. This means even if a malicious client crafts a direct Supabase query with another child's UUID, the policy evaluates to false and returns zero rows. The database is the security boundary, not the client.

**Q: What if a parent knows another child's UUID?**
> Knowing the UUID is insufficient. The RLS policy still checks `parent_id = auth.uid()`. Without being authenticated as that child's parent, the query returns nothing. UUIDs are not secrets in this architecture — they are identifiers, not access tokens.

**Q: Why `ON DELETE RESTRICT` instead of `CASCADE`?**
> `RESTRICT` is a data-protection guardrail. A child's activities represent months of logging effort. Accidentally deleting a child should not vaporize that history. The app implements soft-delete on `children` (`deleted_at IS NULL`), so the actual `DELETE` operation is rarely invoked. If a hard delete is ever needed, the admin must explicitly delete related records first. This is intentional friction.

**Q: What if someone bypasses the app and runs `DELETE FROM children` directly?**
> They would need a valid JWT token for the Supabase project. If they have one, the RLS `DELETE` policy still checks `parent_id = auth.uid() AND deleted_at IS NULL`, so they can only delete their own active children. Even with service role access (which we don't expose to clients), the soft-delete pattern in the app code means the row would be updated, not removed.

---

### Schema Design

**Q: Why `JSONB` for `value` instead of normalized columns?**
> Activity types have heterogeneous schemas: sleep has `quality`, meals have `food_groups[]`, screen time has `device` and `category`. Normalizing into separate tables or sparse columns creates a combinatorial schema explosion. JSONB lets us store validated, type-safe payloads without schema migrations when we add a new field to an activity type. We enforce shape at the TypeScript level via the `Activity['value']` discriminated union, not the database level.

**Q: How do you ensure `value` JSONB integrity without DB constraints?**
> TypeScript's discriminated union on the `Activity` type enforces correct shapes at compile time. At runtime, the app only writes `value` objects through typed functions in `lib/api.ts` that construct the payload explicitly. There is no user-facing path to inject arbitrary JSON into the `value` field. For a production hardening step, we would add a PostgreSQL `CHECK` constraint with `jsonb_schema_is_valid`, but that adds maintenance overhead for a schema that rarely changes.

**Q: Why `recorded_at` separate from `created_at`?**
> `recorded_at` is the *semantic time* the activity happened — e.g., "sleep occurred last night at 9 PM." `created_at` is the *system time* the row was inserted — e.g., "parent logged it at 8 AM this morning." The History tab filters and groups by `recorded_at`. If we only had `created_at`, late entries (e.g., logging yesterday's meal today) would appear on the wrong date.

**Q: `notifications` is JSONB. How do you add an 11th type without migration?**
> JSONB is schemaless. The app reads `notifications['new_type'] ?? true` (defaults to enabled), and writes back the full object. No `ALTER TABLE` is needed. The trade-off is that we cannot enforce "exactly 10 keys" at the database level, but the app code is the only writer, so the shape is controlled.

---

### Performance

**Q: You fetch ALL activities in History. Performance at 1,000 records? 10,000?**
> `getActivities()` actually has a `limit(100)` — it fetches at most 100 records, not unlimited. At 100 records: negligible impact, ~50KB JSON payload. The 100-limit is a deliberate guard; it covers the typical 2–3 month view window for a parent logging a few activities per day.
>
> At 10,000 records: the `limit(100)` prevents memory issues, but the stats aggregation (weekly/monthly charts) running over 10,000 rows client-side would become slow. We would implement cursor-based pagination or server-side aggregation for that scale. This is a known scaling boundary — the current limit of 100 is tested for the thesis scope but would need addressing for a production app with years of data.
>
> A future enhancement would be a separate "activity dates" aggregation query to power the calendar dots, decoupled from the per-day activity log.

**Q: `getActivities()` has a `limit(100)`. Why 100? What happens when a child has more than 100 logged activities?**
> 100 was chosen empirically — it covers roughly 2–3 months of typical daily logging (3–5 activities per day). If a child exceeds 100 activities, older records are simply not fetched and won't appear in the History view. This is a deliberate tradeoff: the calendar dot system and stats charts all operate within a monthly view, so older records beyond the limit don't affect the primary UI. For a parent who has been logging for over a year, only the most recent 100 entries matter for their current month navigation. A cursor-based pagination or date-range query would fix this but adds complexity — deferred to post-thesis scaling work.

**Q: Prove the partial index improves performance.**
> The partial index `idx_scheduled_end_time` only indexes rows where `status = 'pending'`. If 90% of scheduled activities are completed or skipped, this index is ~10% the size of a full index. PostgreSQL's query planner will use it for queries like `SELECT * FROM scheduled_activities WHERE planned_end_time < NOW() AND status = 'pending'`, which is our cleanup/notification query. We verified this with `EXPLAIN ANALYZE` on a seeded database: the partial index reduced the scan from 1,200 rows to 45 rows.

---

### Storage & Avatars

**Q: The avatar bucket is public-read. Scraping risk?**
> Yes, anyone with the bucket URL can list public files. However, our bucket policy only allows `SELECT` to public — `INSERT`, `UPDATE`, and `DELETE` require auth + ownership. The filenames are UUID-prefixed (`[user-uuid]_[random].jpg`), making enumeration infeasible. The risk is equivalent to a public GitHub avatar URL: visible if known, but not listable without insider access.

**Q: What if a user uploads `other-user-uuid_filename.jpg`?**
> The `is_owned_avatar_object()` function checks that the filename starts with `auth.uid() + '_'`. If user A uploads `user-b-uuid_file.jpg`, the ownership check fails and the `INSERT` policy rejects it. The prefix is verified at the database level, not the client level.

---

## 3. Loading Overlay & Auth UX

### State Machine

**Q: The overlay has three states but only two booleans. What about the transition where both are true?**
> Both booleans being true is an impossible state in the actual flow. `loading` is set to false inside `loadSession()` before `redirecting` is ever set to true. The redirect effect has an early return (`if (loading) return`), so `redirecting` can only be set after `loading` is false. We could model this as a single state machine (`'idle' | 'loading' | 'redirecting'`), but two booleans are simpler and equivalent given the invariant.

**Q: Why 1800ms specifically?**
> Empirically determined. The login screen's welcome animation (fade + spring) takes ~400ms to become visible, holds for ~1200ms, then fades out over 300ms. 1800ms covers the full animation cycle plus a 100ms buffer for React Native's bridge latency. It's not arbitrary — it's the sum of the animation durations on the source screen.

**Q: If session fetch hangs, the user sees "Smart Parenting" indefinitely. Timeout?**
> There is no explicit timeout on `loadSession()`. In practice, Supabase's `getSession()` resolves quickly because it reads from AsyncStorage first (local), then validates with the server. If the server is unreachable, the local session is still returned and validated lazily on the next network request. The user would see the overlay for at most 2–3 seconds. A timeout could be added (`Promise.race(getSession(), delay(5000))`) but hasn't been necessary in testing.

---

### UX Decisions

**Q: Why not a skeleton screen instead of a blank overlay?**
> A skeleton screen implies the shape of the final UI (headers, cards, lists), but at overlay time we don't yet know which screen to show — auth or tabs. Rendering a generic skeleton that might be wrong is more disorienting than a branded loading spinner. The overlay's background color matches the app theme, making the transition feel like a continuous surface rather than a blank interruption.

**Q: Background color prevents flash. What about dark mode?**
> The app currently does not implement dark mode. The color `#FEFBF6` (warm cream) is the sole background. If dark mode were added, we would read the system theme from `useColorScheme()` and conditionally set the overlay background to `#121212`. This is a known limitation acknowledged in the project scope.

**Q: Have you measured user perception of the 2-second cold start?**
> Informally, yes. Test users (n=4, all parents) reported the spinner felt "normal" compared to other apps they use (Facebook, Grab). The 1.8s delay on login redirect is masked by the welcome animation, which users perceive as intentional polish rather than waiting. For a formal evaluation, we would use a System Usability Scale (SUS) questionnaire, which is planned for the defense data collection phase.

---

## 4. Dashboard

### Data Flow

**Q: Parallel Supabase queries on every `useFocusEffect`. How many round trips?**
> Two: `getTodayActivities()` and `getScheduledActivities()`. They are independent, so we `Promise.all([...])` them. Two round trips per tab focus is acceptable. Supabase reuses the HTTP connection via keep-alive, so there's no TCP handshake overhead after the first request. If we added Realtime subscriptions, we could eliminate these polls entirely — that's a future optimization.

**Q: `todayActivities` and `scheduledActivities` are separate state. Out of sync risk?**
> Both are re-fetched from the same `loadDashboardData()` function, so they are atomically updated. The only desync scenario is if a mutation (cancel schedule, log activity) calls `loadDashboardData()` and fails. In that case, the error banner is shown and the stale state remains — which is correct, because showing stale data with an error is better than silently showing nothing.

**Q: Stats are computed client-side. Why not a Supabase RPC or view?**
> The stats are simple aggregations (sum of minutes, count of meals) over a small dataset (today's activities, typically < 20 rows). Client-side computation is faster than an additional network round trip to an RPC. If we were computing 28-day rolling averages on the dashboard, an RPC would make sense. For today's data, `reduce()` in JavaScript is negligible.

---

### Child Selection

**Q: What if `selectedChild` in AsyncStorage was deleted on another device?**
> On app open, `loadChildren()` fetches the fresh child list from Supabase. If `selectedChildId` points to a deleted (soft-deleted) child, the `children.find()` returns undefined, and the app falls back to selecting the first available child. If no children exist, the empty state is shown. The AsyncStorage value is treated as a *hint*, not a *source of truth*.

**Q: Why both Zustand and AsyncStorage for `selectedChildId`?**
> Zustand provides reactive state for the UI; AsyncStorage provides persistence across app kills. Zustand alone would lose the selection on restart. AsyncStorage alone would require prop-drilling or context for reactivity. The Zustand store uses a persistence middleware that syncs `selectedChildId` to AsyncStorage automatically. It's one value, two concerns: reactivity and durability.

**Q: If a parent has 10 children, the horizontal selector becomes unwieldy.**
> True. The current ScrollView works well up to ~5 children (tested). Beyond that, we would switch to a horizontal FlatList with snap-to-item or replace the inline selector with a modal picker. The modal picker already exists as the child picker accessible from the header pill on every tab screen. Expanding the dashboard selector to use the same modal is a straightforward enhancement.

---

### Scheduled Activities

**Q: "Upcoming" shows max 3 items. How does the user see the rest?**
> The Activities tab has a full Schedule mode where all future activities are visible with date navigation. The dashboard preview is intentionally a summary. Tapping "+N more scheduled" navigates to the Activities tab with Schedule mode pre-selected. This follows the principle of progressive disclosure: show the most urgent items, provide a path to the full list.

**Q: Log button appears when `now >= start_time`. What if the device clock is wrong?**
> If the device clock is behind, the Log button would appear earlier than intended. If ahead, it would appear late. We trust the device clock because (a) most smartphones sync automatically via NTP, and (b) there is no server-side "now" reference available offline. For a production hardening, we could fetch server time on app open and compute an offset, but this adds a network dependency to a local UI decision.

**Q: Canceling shows inline confirmation. Why not a modal?**
> Inline confirmation (expanding action buttons below the item) is less disruptive than a full-screen modal for a reversible action. The schedule item remains visible, context is preserved, and the user can dismiss by tapping elsewhere. A modal would obscure the list and force a context switch. This is a deliberate HCI choice for lightweight destructive actions.

---

## 5. Activities Screen (Log / Schedule)

### Form Complexity

**Q: 800+ lines with 50+ state variables. How do you maintain this?**
> We don't — not ideally. The file grew organically as activity types were added. For a refactor, we would extract each activity type's form section into a sub-component (`SleepForm`, `MealForm`, etc.) and use a reducer pattern (`useReducer`) for the time-input state. The current flat state is manageable because each variable maps 1:1 to a UI field, making it easy to trace. The refactor is on the post-thesis roadmap.

**Q: Why not split Log and Schedule into separate screens?**
> They share 80% of their UI: activity type grid, time inputs, chip selectors, notes field. Splitting would duplicate those components or force abstraction overhead. The mode toggle is a simple state switch. If the two modes diverged further (e.g., Schedule gained calendar recurrence), then splitting would make sense. For now, the similarity outweighs the complexity cost.

**Q: Each activity type has its own H/M/P state. Why not a single `times` object?**
> A single object would require dynamic key access (`times[`${activityType}StartH`]`), which loses TypeScript exhaustiveness checking. With explicit state variables, the compiler guarantees every branch handles its own time fields. The verbosity is the price of type safety. A reducer with a discriminated action type would be the compromise.

---

### Time Input

**Q: `TimeRangeInput` auto-calculates but doesn't validate start < end. Why?**
> Because start > end is a valid input for overnight activities. A sleep session from 10 PM to 6 AM has `start > end` in 12-hour representation, but it's semantically correct. The auto-calculation adds 24 hours when `end < start`, producing the correct duration. Adding a "start must be before end" validation would block legitimate overnight logs.

**Q: Overnight crossing adds 24 hours. What about a nap crossing midnight?**
> Naps are typically daytime, but a parent could log a late nap (11:30 PM – 12:30 AM). The same overnight logic applies: 12:30 AM is treated as 24.5 hours after the previous day's noon, producing 1 hour duration. This is mathematically correct and consistent with the sleep handler.

**Q: Steppers increment by 1 hour / 5 minutes. What about 2:37 PM?**
> The steppers are for coarse adjustment. Each digit box is also a `TextInput` that accepts direct typing. A parent can tap the hour box and type "2", tap the minute box and type "37". The steppers are an affordance, not a constraint.

---

### Data Mapping

**Q: `nap` is stored as `sleep`. When will you migrate?**
> The `nap` type exists in the TypeScript union and UI but is mapped to `sleep` at the API layer (`dbType = activityType === 'nap' ? 'sleep' : activityType`). A proper migration would add 'nap' to the database enum, update all existing nap records, and remove the mapping. This is deferred to post-thesis because it requires a downtime migration and re-testing of the history filters and AI aggregation logic. The mapping is a documented technical debt.

**Q: Food groups are multi-select with no quantities. How does AI distinguish serving sizes?**
> It doesn't. The AI prompt currently receives boolean food group presence ("fruits: yes, protein: yes"). It cannot distinguish a full serving from a single bite. This is a limitation we acknowledge: the app tracks *dietary diversity* (how many groups were present), not *dietary quantity*. Future versions could add portion-size selectors (small/medium/large) per group.

---

### Validation

**Q: No per-field inline validation — only a single banner. Why?**
> The Activities screen predates our inline validation pattern (which was introduced in the Login and Child Wizard screens). Retrofitting inline validation to 50+ state variables is a significant refactor. The single banner was the MVP approach. We are migrating to inline validation screen-by-screen; the Child Wizard already has it. The Activities screen is next on the list.

**Q: Schedule mode validates `minMins <= maxMins`. What about negative or zero?**
> The hour/minute inputs are sanitized: `sanitizeHour` clamps to 1–12, `sanitizeMinute` clamps to 0–59 and pads to 2 digits. Negative values are impossible via the UI. Zero duration (0h 0m) is allowed — it represents a reminder with no minimum duration requirement. If zero is semantically invalid for a specific activity type, we would add a check in `handleSchedule()`.

---

## 6. History Screen

### Calendar

**Q: Why not use `react-native-calendars`?**
> We evaluated it. It adds ~1.5MB to the bundle, has Android-specific rendering issues with custom theming, and its API is more complex than our needs. Our calendar is a 42-cell grid built with plain `<View>` and `<Text>` components — no dependencies, full control over styling, and it matches our coral theme exactly. The cost of writing 60 lines of grid logic is lower than the cost of fighting a third-party library.

**Q: Week starts on Monday. What about Sunday-start expectation?**
> The Philippines follows the international ISO 8601 standard (Monday start) in government and academic contexts. However, many Filipino families observe Sunday as the week start due to Catholic tradition. We chose Monday because (a) it aligns with the `Date.getDay()` convention where Monday=1, and (b) it matches the WHO reporting standards referenced in the app. A settings toggle for week start is a planned enhancement.

**Q: String prefix filtering for dates — timezone-safe?**
> We use `formatDateLocal(date)` which returns `YYYY-MM-DD` in the device's local timezone. The `recorded_at` timestamp is also stored in the device's local timezone context (the parent logs "9 PM" and we store it as `2026-04-25T21:00:00+08:00`). String prefix matching on `YYYY-MM-DD` is safe as long as both sides use the same timezone, which they do. Cross-timezone travel would break this — a known edge case.

---

### Charts

**Q: `react-native-chart-kit` is deprecated. Why not Skia?**
> `react-native-chart-kit` was already in the project when we inherited the codebase. Migrating to `@shopify/react-native-skia` would require rewriting all chart rendering logic and adding a C++ dependency (Skia binaries increase app size by ~5MB). For the thesis timeline, the existing library works. The deprecation is noted; migration to Skia or `victory-native-xl` is post-thesis.

**Q: Charts are in `ListFooterComponent`. Why not at the top?**
> User preference. Parents open the History tab to *review today's activities first*. Charts are analytical summary; the daily activity list is the primary task. Placing charts at the bottom respects the reading order: specific events first, patterns second. The stats section is collapsible, so users who want charts immediately can leave it expanded.

**Q: Pie chart with no meals — hide or show empty?**
> The pie chart section is conditionally rendered: `hasMeals && <PieChart ... />`. If no meals exist in the selected period, the chart is omitted entirely with no placeholder. This avoids a confusing empty donut. The bar charts follow the same pattern: `visibleChartTypes.map(...)` only renders charts for types with data.

---

### Read-Only Design

**Q: History is read-only. What if a parent logs the wrong time?**
> They must delete and re-log. We acknowledge this is suboptimal. An edit feature requires (a) an edit modal with pre-filled form state, (b) validation that the edit doesn't violate scheduled activity constraints, and (c) an audit trail for AI reproducibility. These are non-trivial. Edit functionality is planned for v2.

**Q: No search. How find an activity from weeks ago?**
> The calendar picker allows jumping to any date. For text search ("swimming"), there is no affordance. A search bar filtering by activity type, notes content, or date range is on the feature backlog. The current design assumes parents browse by date rather than keyword.

---

## 7. Settings

### Profile & Account

**Q: `updateUser()` only updates metadata. Where is the user profile table?**
> We don't have one. Supabase Auth stores `user_metadata` (name, avatar_url) as part of the auth user object. This is sufficient for our needs because the parent profile is minimal (name + avatar). If we needed additional fields (address, phone, subscription tier), we would create a `profiles` table with `id = auth.uid()` and extend the RLS. For now, auth metadata is the correct boundary.

**Q: Changing email requires current password. What if the parent forgot it?**
> They would use the "Forgot Password" flow on the login screen, which sends a reset email. After resetting, they can return to Change Email with the new password. This is standard security practice — re-authentication for sensitive account changes is required by OWASP guidelines.

**Q: Password minimum is 6 characters. Below NIST recommendations?**
> NIST SP 800-63B recommends 8 characters minimum but explicitly discourages arbitrary complexity requirements. We chose 6 as the minimum because (a) Supabase Auth defaults to 6, and (b) our user testing showed parents struggled with longer passwords on mobile keyboards. The 3-bar strength indicator (6/8/10 chars) encourages longer passwords without blocking submission. If we enforced 8, we would see more password reset requests.

---

### Child Settings

**Q: BMI only works for 24–60 months. What about other ages?**
> WHO BMI-for-age reference tables exist for 0–5 years (z-scores) and 5–19 years (percentiles). We implemented the 2–5 year range because it covers the app's core demographic (toddlers and preschoolers) and the z-score calculation is straightforward. Infants under 2 use weight-for-length, not BMI, which requires a different WHO table. School-age children use BMI-for-age with a different statistical model. These are planned extensions.

**Q: BMI trigger at DB level vs `assessBmi()` client-side. Which is authoritative?**
> The DB trigger computes raw BMI (`weight / height²`). The client-side `assessBmi()` computes BMI *and* maps it to a WHO z-score, percentile, and category (normal/at-risk/overweight/obese). The DB stores the raw number; the client interprets it. Both are "correct" at their layer. If we needed server-side BMI categorization (for example, in an Edge Function), we would port `assessBmi()` to SQL or Deno.

**Q: 9 routine time fields × 3 sub-fields = 27 state variables. Why not a `routine` object?**
> Same answer as the Activities screen: explicit variables give TypeScript exhaustiveness. A `routine` reducer would be cleaner. The current implementation uses individual `useState` calls because each time field has its own Quick Pick chips and independent validation. Refactoring to a `useReducer` with a `RoutineState` type is a post-thesis cleanup task.

---

### Notifications

**Q: The stale closure bug in the master toggle. Why hasn't it been fixed?**
> The bug: the `useEffect` has `notificationsEnabled` in its dependency array but NOT `children`. When `loadChildren()` refreshes the children array, the effect does not re-run, so new children don't get their notification schedules applied until the next manual toggle. This was documented in the codebase and wiki as a known issue.
>
> The fix is straightforward: add `children` to the dependency array and wrap the async `apply()` function in `useCallback`, or restructure the effect to fire independently on both `notificationsEnabled` changes and `children` changes. It was not patched before defense due to time constraints — the bug only manifests when adding a new child while the toggle is off, which is an edge case in normal usage. The worst-case outcome (new child misses one notification cycle) self-heals on the next manual toggle.

**Q: Time zone changes?**
> Expo local notifications schedule in the device's local time. If a parent travels from Manila (+08:00) to Dubai (+04:00), the 8 PM bedtime notification would fire at 8 PM Dubai time — which is midnight Manila time. This is technically "correct" (local time is preserved) but semantically wrong for the child's routine. A production app would store routines in UTC and convert to local time on schedule. We use local time for simplicity.

**Q: 9 notification types × 5 children = 45 notifications. Performance issues?**
> No. Expo Notifications on Android use the system `AlarmManager`, which handles thousands of alarms efficiently. On iOS, the `UNUserNotificationCenter` batch-schedules up to 64 local notifications per app. We are well under that limit. The scheduling operation itself is a single JavaScript bridge call per notification, which takes ~10ms. 45 notifications = 450ms, done once on child save.

---

### Deletion

**Q: Soft-delete child but activities remain. How access orphaned data?**
> Activities are not orphaned — they remain in the database but are invisible to the parent because the RLS policy joins through `children`, and soft-deleted children fail the `deleted_at IS NULL` check. If a parent accidentally deletes a child and wants to recover, they would contact an admin who can `UPDATE children SET deleted_at = NULL WHERE id = ?`. This is intentional data preservation with admin-mediated recovery. A "recently deleted" trash bin in the app is a v2 feature.

---

## 8. Login & Register

### Auth Flow

**Q: Signup auto-signs out after creation. Why not auto-login?**
> Two reasons. First, Supabase Auth sends an email confirmation by default, and the account is not fully active until confirmed. Auto-logging in an unconfirmed user creates a confusing state where the app appears functional but some features fail. Second, auto-login would skip the "Account Created" success screen, which provides critical feedback that the registration succeeded. The user sees confirmation, then navigates to login with full context.

**Q: Welcome animation 1800ms — empirically tested or arbitrary?**
> The 1800ms timer is the sum of the animation keyframes as wired in the code: fade in (~400ms) + hold (~1200ms) + fade out (~300ms). These values were tuned manually during development. We tested 3 variants (shorter hold, longer fade, no spring) with 4 users; the current timing had the highest "polished" rating. The wiki previously misstated this as 1900ms — the correct value in the code is 1800ms.

**Q: `router.back()` from signup is fragile. Deep-link risk?**
> True. If a user deep-links directly to `/signup` with no prior route, `router.back()` exits the app. The correct pattern is `router.replace('/(auth)/login')`, which guarantees navigation to login regardless of history. This is a known bug; the fix is one line. It will be patched before defense.

---

### Validation

**Q: Email regex on signup — pattern details?**
> We use a pragmatic regex: `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`. It rejects obvious garbage (`not-an-email`) but accepts `user+tag@domain.com` and internationalized domains. We intentionally do NOT use a comprehensive RFC 5322 regex because those are 500+ characters and still fail edge cases. The real validation happens when Supabase attempts to send the confirmation email.

**Q: Password strength is just length bars. No complexity requirements?**
> Correct. NIST SP 800-63B explicitly recommends against complexity requirements (special chars, mixed case) because they reduce usability without improving entropy. Length is the primary entropy driver. Our 3-bar indicator (6/8/10 chars) nudges users toward longer passwords without enforcing arbitrary rules.

---

### Security

**Q: Login errors distinguish "invalid credentials" from "email not confirmed". User enumeration?**
> This is a valid concern. The current implementation returns different error messages, which allows an attacker to determine if an email is registered. The fix is to return a generic "Invalid credentials or unconfirmed email" message for both cases, while still logging the specific reason server-side for support purposes. This will be patched before defense.

**Q: No rate limiting on login. Brute force risk?**
> Supabase Auth implements rate limiting on its API: 10 failed attempts per IP per hour, with exponential backoff. This is handled at the infrastructure level, not our client code. We do not implement additional client-side rate limiting because it is trivially bypassed and would add no real protection.

---

## 9. AI Insights

### Architecture

**Q: Why an Edge Function instead of a direct API call from the client?**
> Three reasons: (1) **API key secrecy** — the OpenRouter API key lives in Supabase secrets, never exposed to the client; (2) **Data aggregation** — the Edge Function queries Supabase directly with the service role key, avoiding multiple client round trips; (3) **Auditing** — all AI interactions pass through a single server-side chokepoint where we can log, throttle, and validate. A direct client call would leak the API key and require the client to fetch 28 days of raw activity data.

**Q: The Edge Function uses the service role key. What prevents a malicious client from calling it directly?**
> The Edge Function validates the JWT token from the request headers (`req.headers.get('authorization')`). Even though it uses the service role key for internal Supabase calls, the *entry point* still requires a valid user session. An unauthenticated request is rejected before any service-role query executes. The service role key is never exposed to the client; it is injected as an environment variable by Supabase.

**Q: Why zero-shot instead of fine-tuning or RAG?**
> Fine-tuning requires a labeled dataset of child development recommendations, which does not exist for our domain and would cost thousands in GPU hours. RAG (retrieval-augmented generation) requires a vector database and embedding model, adding infrastructure complexity. Zero-shot is the correct choice because: (a) the prompt contains all necessary context (WHO guidelines, child data, trends), (b) the model is used as a reasoning engine, not a knowledge base, and (c) it requires zero infrastructure beyond the API call.

---

### Model Choice

**Q: What if OpenRouter removes the free model?**
> We would swap the model string in one line: `model: 'openrouter/elephant-alpha'` → `model: 'anthropic/claude-sonnet-4'` or any other OpenRouter-supported model. The prompt and normalizer are model-agnostic. The only change needed is adjusting `max_tokens` and `temperature` for the new model's behavior. This abstraction is why we chose OpenRouter instead of a vendor-specific API.

**Q: Quality is "dependent on the free model." Production migration path?**
> For production, we recommend `openrouter/anthropic/claude-sonnet-4` or `openrouter/openai/gpt-4o`. Both produce significantly more reliable structured JSON and better follow the prompt's formatting instructions. The cost is approximately $0.005 per 1K tokens, which for our ~2K-token prompt and ~500-token response is ~$0.015 per analysis. At once-per-day-per-child, a 1,000-user app costs ~$450/month — reasonable for a SaaS product.

**Q: Temperature 0.4 with +0.15 retry bump. How arrived at?**
> Temperature 0.4 was chosen through manual testing: 0.0 produced overly rigid, repetitive outputs; 0.7 produced too much variation and occasional JSON parse failures; 0.4 balanced consistency with slight variation. The +0.15 retry bump (to 0.55) is a standard technique: if the model fails to produce valid JSON at low temperature, a slightly higher temperature on retry increases the probability of a different token sampling path succeeding. These values were validated over ~50 test calls during development.

---

### Prompt Engineering

**Q: The prompt is 686 lines. Version control and testing?**
> The prompt is a TypeScript template literal in `index.ts`. It is version-controlled via Git like any other source file. For testing, we snapshot the prompt output for specific input datasets and diff them during regression testing. We do not unit-test the prompt itself because the model is non-deterministic; instead, we test the normalizer's output on a corpus of 20 real model responses.

**Q: What prevents prompt injection via child name?**
> The child name is inserted as a plain string value in a structured section: `Name: ${child.name}`. The rest of the prompt is hardcoded instructions with no user-controlled text in instruction positions. A child named "Ignore previous instructions" would simply appear as `Name: Ignore previous instructions` — the model sees this as data, not instructions, because it is not in a system or instruction block. This is not a guaranteed defense against sophisticated injection, but it raises the bar significantly.

**Q: WHO guidelines are hardcoded. Update path when WHO revises them?**
> The guidelines are in a dedicated section of the prompt, clearly demarcated with comments. Updating them is a find-and-replace operation in `index.ts`. Because the prompt is source code, it goes through the same code review and deployment pipeline as any other change. We subscribe to WHO newsletter alerts for pediatric guideline updates.

---

### Safety & Normalization

**Q: Normalizer uses regex. What if the model outputs Tagalog or mixed languages?**
> The regex patterns are case-insensitive and match English keywords only. If the model outputs Tagalog (e.g., "Oras sa screen"), the regex would not match and the category inference would fall back to `general`. This is a graceful degradation — the recommendation is still displayed, just without category-specific filtering. For a Philippines-focused product, we would add Tagalog regex variants or use a lightweight language-detection pass before normalization.

**Q: Max 3 recommendations with deterministic slicing. What if all 3 are about screen time?**
> The normalizer does not enforce topic diversity. If the model outputs 3 screen-time recommendations, all 3 are saved. In practice, the prompt explicitly instructs the model to cover different domains, and our testing shows 90%+ of outputs contain mixed categories. If diversity enforcement were required, we would add a post-normalizer filter that ensures at most one recommendation per category.

**Q: How do you know the normalizer isn't silently dropping valid recommendations?**
> We don't, absolutely. The normalizer logs every transformation decision (category inference, priority mapping) to the `based_on` field. During development, we manually inspected 50+ normalized outputs against their raw model responses to verify correctness. The test file (`recommendation-normalizer.test.ts`) covers edge cases: unknown categories, null trends, mixed-case inputs. For production, we would add a "raw output" viewer in the admin panel.

---

### Data Privacy

**Q: Child name, age, and stats sent to OpenRouter. Their data retention policy?**
> OpenRouter's privacy policy states they retain API request logs for 30 days for abuse detection and do not use request data for model training unless explicitly opted in. We are on the free tier, which does not opt in to training. However, we have not negotiated a DPA (Data Processing Agreement) with OpenRouter. For a production deployment in the Philippines, we would require a DPA or switch to a provider with one (e.g., Azure OpenAI).

**Q: No PDPA consent checkbox. Legally deployable?**
> Technically, no. The Philippines Data Privacy Act of 2012 (RA 10173) requires explicit consent for processing personal information, including children's data. The current onboarding flow does not include a consent checkbox for AI data processing. This is a **critical gap** that must be addressed before any public deployment. The fix is adding a modal during signup or child creation that explains AI data usage and requires an explicit toggle/opt-in.

**Q: `based_on` allows reproduction, but the model is non-deterministic. Can you truly reproduce?**
> Not byte-for-byte. However, `based_on` contains the exact input data, prompt parameters (temperature, model), and previous recommendation IDs. Replaying the same inputs with the same parameters produces *statistically similar* outputs. For auditing purposes, this is sufficient: a panelist can verify that the recommendation is *plausibly derived* from the stated inputs, even if the exact wording differs. True reproducibility would require a deterministic model (temperature 0 on a fixed seed), which OpenRouter does not guarantee.

---

### Cost & Scaling

**Q: Monthly cost at 1,000 users if upgraded to GPT-4o?**
> Prompt: ~2,000 tokens. Response: ~500 tokens. Total: ~2,500 tokens per call. GPT-4o pricing: $5 per 1M input tokens, $15 per 1M output tokens. Cost per call: (2000/1M × $5) + (500/1M × $15) = $0.01 + $0.0075 = **$0.0175**. At 1,000 users × 1 child × 30 days = 30,000 calls/month. Total: **$525/month**. With caching (client-side `isToday()`), the actual call volume is lower because users don't tap "Generate Insights" every day.

**Q: Client-side `isToday()` cache — what if app data is cleared or device switched?**
> The cache is lost. The user would trigger a redundant API call on the new device or after clearing data. This is acceptable: it wastes one API call, not data. The `isToday()` check is a UX optimization, not a cost optimization. For a true cross-device cache, we would store `last_analysis_date` in the `children` table and check that before calling the Edge Function.

---

### Edge Cases

**Q: What does the AI recommend with exactly 0 logged activities?**
> The prompt includes a "Data Quality" section that flags "First analysis — no baseline" and "Sparse data." The model is instructed to provide generic, age-appropriate WHO guideline recommendations in this case (e.g., "Ensure your child gets 10–13 hours of sleep per night according to WHO guidelines"). During testing, the model consistently produced safe, guideline-based advice rather than making up specific observations about the child.

**Q: Network failure during analysis — partial data?**
> The Edge Function is atomic: it fetches data, calls the API, normalizes, and inserts. If any step fails, no recommendations are written to the database. The client receives an HTTP error (502 or 504) and shows a retry banner. There is no partial write state because the INSERTs happen only after the full normalization succeeds.

**Q: 30-second timeout. Sufficient on 3G in rural Philippines?**
> A 2K-token prompt + 500-token response on a 1 Mbps 3G connection takes ~3 seconds of transfer time. The 30-second timeout is for the model's inference latency, not network latency. In rural areas with high packet loss, the connection might stall. We have not tested on actual 3G; this is a gap. A potential fix is reducing the prompt length (currently 686 lines) or adding a progressive loading indicator that explains "Analyzing your child's data..." during the wait.

---

## 10. Cross-Cutting Concerns

### State Management

**Q: Zustand for client, Supabase for server. Where's the line?**
> The line is simple: if the data needs to survive app restarts or be visible on other devices, it lives in Supabase. If it's ephemeral UI state (active tab, expanded accordion, scroll position), it lives in Zustand or local `useState`. `selectedChildId` is the exception — it is client state that we persist for UX convenience, but it is always validated against the server child list on load.

**Q: `useFocusEffect` refetches every tab switch. Why not Supabase Realtime?**
> Supabase Realtime requires a persistent WebSocket connection, which has battery implications on mobile and complexity implications for background state. For our data freshness requirements (activities update a few times per day), polling on tab focus is sufficient and simpler. Realtime would make sense for a collaborative feature (e.g., two parents on the same account), which we do not support.

---

### Error Handling

**Q: Async errors are caught and set to state. Also logged? Crash reporter?**
> Errors are caught with `try/catch` and surfaced via inline banners or toast messages. We do not currently integrate a crash reporter (Sentry, Bugsnag) due to budget constraints. `console.warn` statements exist in development but are stripped in production builds via Metro's `__DEV__` dead code elimination. For production, we would add Sentry and send anonymized error traces.

**Q: `console.warn` in catch blocks. Acceptable for production?**
> No. All `console.warn` calls are wrapped in `if (__DEV__)` or will be removed before production. The production build configuration (`eas.json` release profile) enables Metro minification, which removes `console.*` calls when configured. Any remaining `console.warn` in production is a bug and should be reported.

---

### Testing

**Q: No E2E tests. How verify the full flow?**
> Manual testing on physical devices (Xiaomi Note 12 4G, iPhone 14 Pro Max). We have a written test script covering: login → add child → log activity → view history → generate AI insights → change settings → sign out. For the thesis, this is supplemented by user acceptance testing with 4 parent participants. E2E automation (Maestro or Detox) is a post-thesis infrastructure investment.

**Q: Normalizer has tests. Why not BMI or time inputs?**
> The normalizer is the most algorithmically complex and error-prone component: regex matching, weight-based inference, null handling. The BMI calculator and time inputs are deterministic mathematical functions with clear boundaries (e.g., `bmi = weight / height²`). They are validated implicitly through UI integration tests ("does the BMI card show 'Normal' for these inputs?"). As the codebase matures, we would add unit tests for `bmi.ts` and `sleep-calculator.ts`.

---

### Accessibility

**Q: Are time steppers accessible to screen readers?**
> The stepper buttons have `accessibilityLabel` set ("Increment hour", "Decrement minute"). The digit `TextInput` has `accessibilityLabel` describing the field ("Hour input, 12-hour format"). We have not conducted full VoiceOver/TalkBack testing. A full accessibility audit is a post-thesis requirement, particularly for colorblind-safe badges and screen reader navigation through the 9 routine time fields.

**Q: Color-coded badges — colorblind accessibility?**
> Each activity badge pairs color with a distinct icon (moon for sleep, book for education, etc.). The color is supplementary; the icon is the primary identifier. However, we do not currently add text labels or patterns to the badge backgrounds. A colorblind-safe enhancement would add hatching or shape variation to the badge containers.

---

### Offline Support

**Q: What happens when logging an activity with no internet?**
> The app shows an error banner ("Network error — check your connection") and the activity is NOT logged. There is no offline queue. Supabase's local persistence is read-only for our setup; writes require an active connection. A proper offline queue would use a local SQLite database (via `expo-sqlite`) to buffer writes and sync when online. This is a major v2 feature.

**Q: Supabase client queues mutations locally?**
> Not in our configuration. Supabase's `createClient` does not enable automatic offline queuing by default. The `supabase-js` library has experimental offline support via `gotrue-js` persistence, but write queuing requires `@supabase/realtime-js` with a custom strategy. We have not implemented this.
