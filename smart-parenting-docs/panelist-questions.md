# Likely Panelist Questions — Implementation Defense

This document catalogs anticipated panelist questions organized by the wiki structure. Each section lists questions a thesis/capstone panel typically asks about implementation decisions, trade-offs, and edge cases.

---

## 1. Architecture & Repository Structure

### File-Based Routing (Expo Router)
- Why did you choose Expo Router over React Navigation? What are the trade-offs?
- How does the `(auth)` / `(tabs)` route group pattern work? Why parentheses?
- What happens if a user manually types a deep link to a protected route while logged out?
- How do you prevent the "Attempted to navigate before mounting" error?

### Auth Guard & Root Layout
- Why is the auth guard in `_layout.tsx` instead of per-screen?
- What happens if `loadSession()` takes longer than 1800ms?
- Is the `isMounted` ref pattern sufficient? What about concurrent auth state changes?
- Why keep the root Stack mounted and use an overlay instead of conditional routing?

### Project Structure
- Why co-locate screens under `app/` instead of a separate `src/screens/` directory?
- The `lib/` folder mixes API calls, utilities, and business logic. Isn't that a violation of separation of concerns?
- Where are your unit tests? Why is there no `__tests__/` or `*.test.ts` outside the normalizer?

---

## 2. Database Schema & Backend

### Row Level Security (RLS)
- Walk me through exactly how RLS prevents one parent from reading another child's data.
- What happens if a parent knows another child's UUID? Can they query it directly?
- Why `ON DELETE RESTRICT` instead of `CASCADE`? Isn't that dangerous for orphaned data?
- The `children` table uses soft delete. What if someone bypasses the app and runs `DELETE FROM children` directly?

### Schema Design
- Why `JSONB` for `value` instead of normalized columns per activity type?
- How do you ensure data integrity when `value` JSONB has no schema constraint at the DB level?
- Why store `recorded_at` separately from `created_at`? What's the practical difference?
- The `notifications` column is JSONB with 10 toggles. How do you add an 11th notification type without a migration?

### Performance
- You fetch ALL activities for a child in the History tab. What's the performance impact at 1,000 records? 10,000?
- `getActivities()` has a `limit(100)`. Why 100? What happens when a child has more than 100 logged activities?
- The partial index on `idx_scheduled_end_time` — prove to me it improves query performance.

### Storage & Avatars
- Your avatar bucket is public-read. What's stopping someone from scraping all avatar URLs?
- The `is_owned_avatar_object` function checks filename prefixes. What if a user uploads `other-user-uuid_filename.jpg`?

---

## 3. Loading Overlay & Auth UX

### State Machine
- The overlay has three states but only two booleans (`loading`, `redirecting`). What about the transition where both are true?
- Why 1800ms specifically? How did you determine that value?
- If the network is slow and session fetch hangs, the user sees "Smart Parenting" indefinitely. Where's the timeout?

### UX Decisions
- Why not show a skeleton screen instead of a blank overlay?
- The background color matches the app theme to prevent flash. What if the user's system theme is dark?
- On cold start, the overlay shows for ~2 seconds. Have you measured user perception of this delay?

---

## 4. Dashboard

### Data Flow
- You run parallel Supabase queries on every `useFocusEffect`. How many round trips is that per tab switch?
- `todayActivities` and `scheduledActivities` are separate state variables. What if they get out of sync?
- The stats are computed client-side. Why not use a Supabase RPC or view?

### Child Selection
- What happens if `selectedChild` is in AsyncStorage but the child was deleted on another device?
- You store `selectedChildId` in Zustand + AsyncStorage. Why both? Isn't that a cache invalidation risk?
- If a parent has 10 children, the horizontal selector becomes unwieldy. Did you consider a dropdown?

### Scheduled Activities
- "Upcoming" shows max 3 items. How does the user see the rest?
- The Log button only appears when `now >= start_time`. What if the user's device clock is wrong?
- Canceling a schedule shows an inline confirmation. Why not a modal?

---

## 5. Activities Screen (Log / Schedule)

### Form Complexity
- This file has 800+ lines with 50+ state variables. How do you maintain this?
- Why not split Log and Schedule into separate screens or sub-components?
- Each activity type has its own H/M/P state. That's 30+ variables for time alone. Why not a single `times` object?

### Time Input
- Your `TimeRangeInput` auto-calculates duration but doesn't validate start < end. Why?
- Overnight crossing adds 24 hours. What if a nap legitimately crosses midnight? Is that handled?
- The steppers increment by 1 hour / 5 minutes. What if a parent needs 2:37 PM specifically?

### Data Mapping
- `nap` is stored as `sleep` in the database. When will you migrate this properly?
- Food groups are multi-select with no quantities. How does the AI distinguish "1 bite of fruit" from "a full serving"?

### Validation
- There's no per-field inline validation — only a single `submitError` banner. Why?
- Schedule mode validates `minMins <= maxMins`. What about negative values? Zero?

---

## 6. History Screen

### Calendar
- The calendar builds a fixed 42-cell grid. Why not use a library like `react-native-calendars`?
- Week starts on Monday. What if the user expects Sunday (common in the Philippines)?
- You fetch all activities then filter client-side by date string prefix. Is string comparison reliable across timezones?

### Charts
- `react-native-chart-kit` is deprecated. Why not `victory-native` or Skia charts?
- Charts are in `ListFooterComponent` which means they render after scrolling through all activities. Why not at the top?
- The pie chart shows food groups for the selected week/month. What if no meals were logged? Does it hide or show empty?

### Read-Only Design
- History is read-only with no edit or delete. What if a parent logs the wrong time? Must they re-log?
- No search functionality. How does a parent find "that swimming lesson from 3 weeks ago"?

---

## 7. Settings

### Profile & Account
- `updateUser()` only updates metadata. Where is the actual user profile table?
- Changing email requires re-authentication. What if the parent forgot their current password?
- Password minimum is 6 characters. That's below NIST recommendations. Why?

### Child Settings
- BMI assessment only works for ages 24–60 months. What about infants under 2? School-age over 5?
- The BMI trigger computes at the DB level, but `assessBmi()` also runs client-side. Which one is authoritative?
- You have 9 routine time fields, each split into H/M/P. That's 27 state variables. Why not a `routine` object?

### Notifications
- The master toggle `useEffect` has a stale closure bug you documented. Why hasn't it been fixed?
- Notifications are scheduled locally. What if the user changes time zones?
- You schedule 9 notification types per child. With 5 children, that's 45 notifications. Any performance issues?

### Deletion
- Deleting a child soft-deletes the profile but activities remain via `ON DELETE RESTRICT`. How does the parent access orphaned activity data?

---

## 8. Login & Register

### Auth Flow
- Signup auto-signs out after creation. Why not auto-login?
- The welcome animation on login is 1900ms. Is that empirically tested or arbitrary?
- `router.back()` from signup is fragile. What if the user deep-linked directly to signup?

### Validation
- Email regex check on signup — what's the pattern? Does it reject valid emails like `user+tag@domain.com`?
- Password strength is just length bars (6/8/10). No complexity requirements. Why?

### Security
- Login errors distinguish "invalid credentials" from "email not confirmed". Doesn't that enable user enumeration attacks?
- No rate limiting on login attempts. How do you prevent brute force?

---

## 9. AI Insights

### Architecture
- Why an Edge Function instead of a direct API call from the client?
- The Edge Function uses the service role key. What prevents a malicious client from calling it directly?
- Why zero-shot prompting instead of fine-tuning or RAG?

### Model Choice
- `inclusionai/ling-2.6-1t:free` is a free-tier model. What happens if OpenRouter removes it or starts charging?
- You said quality is "dependent on the free model." If this were a real product, what's the migration path?
- Temperature 0.4 with a +0.15 retry bump. How did you arrive at those values?

### Prompt Engineering
- The prompt is 686 lines. How do you version control and test it?
- What prevents prompt injection if a parent names their child "Ignore previous instructions and..."?
- The prompt includes WHO guidelines as hardcoded text. How do you update them when WHO revises recommendations?

### Safety & Normalization
- The normalizer uses regex patterns. What if the model outputs a recommendation in Tagalog or mixes languages?
- Max 3 recommendations with deterministic slicing. What if all 3 are about screen time and none about nutrition?
- How do you know the normalizer isn't silently dropping valid but unusual recommendations?

### Data Privacy
- Child name, age, and activity stats are sent to OpenRouter. Have you verified their data retention policy?
- You acknowledge no PDPA consent checkbox exists. Is this app legally deployable in the Philippines?
- The `based_on` audit trail allows reproduction. But the model is non-deterministic. Can you truly reproduce outputs?

### Cost & Scaling
- One API call per tap per day per child. With 1,000 users, what's the monthly cost if you upgrade to GPT-4o?
- The client-side `isToday()` cache prevents redundant calls. What if the user clears app data or switches devices?

### Edge Cases
- What does the AI recommend when there are exactly 0 logged activities? Show me the actual prompt output.
- Network failure during analysis: the user sees an error banner. What happens to the partial data?
- The timeout is 30 seconds. On a 3G connection in rural Philippines, is that sufficient?

---

## 10. Cross-Cutting Concerns

### State Management
- Zustand for client state, Supabase for server state. Where do you draw the line?
- `useFocusEffect` refetches on every tab switch. That's a lot of network traffic. Why not use Supabase Realtime?

### Error Handling
- Async errors are caught and set to state. Are they also logged? Sent to a crash reporter?
- You have `console.warn` in some catch blocks. Is that acceptable for production?

### Testing
- No E2E tests. How do you verify the full login → add child → log activity → view history flow?
- The normalizer has a test file. Why doesn't the BMI calculator or time input logic?

### Accessibility
- Are the time steppers accessible to screen readers?
- Color-coded activity badges — how does a colorblind parent distinguish screen time from sleep?

### Offline Support
- What happens when a parent logs an activity with no internet connection?
- Supabase client queues mutations locally. Do you handle sync conflicts?

---

## Question Difficulty Matrix

| Difficulty | Count | Examples |
|------------|-------|----------|
| **Basic** (what/why) | ~25 | "Why Expo Router?", "What is RLS?" |
| **Intermediate** (how/trade-off) | ~35 | "How does the normalizer handle edge cases?", "Why client-side filtering?" |
| **Advanced** (prove/justify/fix) | ~20 | "Prove the partial index improves performance", "Fix the stale closure bug", "Is this PDPA-compliant?" |

**Total: ~80 questions** covering all implementation areas.
