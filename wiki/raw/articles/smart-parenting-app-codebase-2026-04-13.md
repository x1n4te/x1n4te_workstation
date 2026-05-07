# Smart Parenting App — Codebase Ingestion (2026-04-13)

**Source:** ~/local-projects/smart-parenting-app/ (live codebase)
**Date:** 2026-04-13
**Branch:** feature/ui-redesign-nestnote
**Commits since last ingestion:** 0 (last commit: 7ef4e79)
**Uncommitted changes:** 9 modified files + 3 new files (history.tsx, SCOPE.md, excalidraw)

## Project Overview

AI-based child activity monitoring mobile application. Freelance commission (₱12K). React Native + Expo + Supabase + OpenRouter. Brand: NestNote.

## Tech Stack (from package.json — unchanged since Apr 12)

| Layer | Technology | Version |
|---|---|---|
| Framework | React Native | 0.76.3 |
| Platform | Expo SDK | ~52.0.0 |
| Routing | Expo Router | ~4.0.0 |
| Database/Auth | Supabase JS | ^2.49.0 |
| State | Zustand | ^5.0.0 |
| UI | React Native Paper | ^5.12.0 |
| Forms | react-hook-form + zod | ^7.54.0 / ^3.24.0 |
| Charts | react-native-chart-kit | ^6.12.0 |
| Icons | @expo/vector-icons (Ionicons) | — |
| Storage | AsyncStorage | ^2.1.0 |
| Build | Expo EAS | (eas.json present) |

## Directory Structure

```
smart-parenting-app/
├── app/
│   ├── _layout.tsx          # Root: PaperProvider + Stack + auth guard (85L)
│   ├── (auth)/
│   │   ├── _layout.tsx      # Auth stack (10L)
│   │   ├── login.tsx        # Login screen (472L — welcome animation, social buttons)
│   │   └── signup.tsx       # Signup screen (593L — strength meter, confirm password)
│   ├── (tabs)/
│   │   ├── _layout.tsx      # Tab navigator (82L — 5 tabs)
│   │   ├── index.tsx        # Dashboard (785L — stats, today's activities, child picker)
│   │   ├── log.tsx          # Activity logger (692L — 6 types, stepper+text duration)
│   │   ├── history.tsx      # History browser (564L — NEW: SectionList, date grouping, filters)
│   │   ├── ai.tsx           # AI recommendations (589L — filter bar, priority sorting)
│   │   └── profile.tsx      # Settings (532L — profile card, sections, sign-out modal)
│   └── child/
│       └── new.tsx          # Add child screen (385L — quick age selectors)
├── lib/
│   ├── supabase.ts          # Supabase client (lazy-load, SSR-safe) (41L)
│   └── api.ts               # CRUD: children, activities, recommendations (121L)
├── stores/
│   └── auth.ts              # Zustand: useAuth + useApp stores (70L)
├── database/
│   ├── schema.sql           # Full schema (4 tables, RLS, triggers, indexes) (200L)
│   └── migration_add_activity_types.sql  # Add nap + physical_activity (9L)
├── assets/                  # Icons, splash
├── dist/                    # Web export (HTML files)
├── CLAUDE.md                # AI coding guidance (claims SDK 54 — actual is 52)
├── SCOPE.md                 # Project scope, milestones, payment terms
└── smart-parenting-app-flow.excalidraw  # Architecture diagram
```

## Color Theme (Coral — applied 2026-04-12, finalized 2026-04-13)

```
Primary:        #FF7F60 (coral/salmon)
PrimaryContainer: #FFE5E0
Secondary:      #F1F5F9
Background:     #FEFBF6 (cream)
Surface:        #FFFDFF (near-white)
Error:          #EF4444
OnSurface:      #0F172A
Outline:        #E2E8F0

Activity Colors:
  screenTime:   #FF7F60  bg: #FFF0ED
  sleep:        #10B981  bg: #ECFDF5
  nap:          #8B5CF6  bg: #F5F3FF
  meals:        #F59E0B  bg: #FFFBEB
  physical:     #EF4444  bg: #FEF2F2
  education:    #6366F1  bg: #EEF2FF
```

## Database Schema (from schema.sql)

### Tables
1. **children** — parent_id (FK auth.users), name, date_of_birth, soft-delete (deleted_at)
2. **activities** — child_id (FK children), type (4 base types in schema), value (JSONB), recorded_at
3. **recommendations** — child_id, content, category, priority (low/medium/high), based_on (JSONB)
4. **alerts** — child_id, type, message, severity (info/warning/critical), acknowledged

### Activity Types
- **Schema constraint:** screen_time, sleep, meal, education (4 types)
- **Migration file adds:** nap, physical_activity (6 types total — migration NOT yet applied to schema.sql CHECK constraint)
- **Code uses all 6 types** regardless

### RLS Policies
All 4 tables have separate SELECT/INSERT/UPDATE/DELETE policies. Pattern:
- children: direct parent_id = auth.uid()
- activities/recommendations/alerts: child_id IN (SELECT id FROM children WHERE parent_id = auth.uid() AND deleted_at IS NULL)

### Indexes
- idx_activities_child_type (child_id, type) composite
- idx_activities_child_recorded (child_id, recorded_at DESC) composite
- Single-column: idx_recommendations_child, idx_alerts_child, idx_children_parent

### Triggers
- children_updated_at: auto-update updated_at on children row update

## Key Implementation Details

### Tab Navigation (5 tabs — updated 2026-04-13)
```
Tabs: Dashboard (Home) → Log → History → AI Insights → Settings
Icons: home/outline → add-circle/outline → time/outline → bulb/outline → settings/outline
```
Tab bar: 80px Android, 100px iOS. Coral active tint (#FF7F60), gray inactive (#94A3B8).

### History Screen (NEW — app/(tabs)/history.tsx, 564L)
- **SectionList** with date-grouped sections (Today, Yesterday, full date)
- **Filter pills** — All + 6 activity types, horizontal scroll
- **Child picker** — tap avatar to cycle children (multi-child support)
- **Activity cards** — type icon + label + time, coral theme
- **States:** loading spinner, error with retry button, empty state with CTA
- **Pull-to-refresh** with coral tint
- Uses `useFocusEffect` to reload on tab focus
- `groupByDate()` helper sorts sections newest-first, items within section newest-first
- `getActivityLabel()` formats each type with duration, quality, device, food groups, subject

### Auth Flow (with animations)
- Root layout checks auth state → redirects to /(auth)/login if unauthenticated
- **Welcome animation on login:** Animated.parallel (opacity 0→1, spring scale 0.8→1), shows 1.2s, then fades out
- **Auth guard delay:** _layout.tsx delays redirect to /(tabs) by 1.8s after login to let welcome animation complete (uses useRef timer, clears on unmount)
- signUp does NOT auto-login (prevents email confirmation issues)
- onAuthStateChange listener for session persistence

### Sign-Out Flow
- **Confirmation modal:** Modal (transparent, fade) with icon, title, description, Cancel/Sign Out buttons
- **Goodbye animation:** Animated.parallel (opacity 0→1, spring scale 0.8→1), shows 1.2s, then fades out
- After animation: calls signOut(), resets scale, navigates to /(auth)/login

### Settings Screen (profile.tsx — 532L)
Structure: Header → Parent Profile Card → Account → Children → Notifications (Switch toggles) → Privacy & Security → Support → Sign Out button → Version "NestNote v1.0.0"

### Supabase Client
- Lazy-loaded to avoid SSR "window is not defined"
- Proxy export pattern for convenient access
- AsyncStorage for session persistence
- autoRefreshToken + persistSession enabled

### Data Layer (api.ts)
- getChildren: ordered by created_at DESC
- createChild: requires userId from auth store (NOT getUser())
- logActivity: auto-sets recorded_at
- getActivities: 100 limit, optional type filter
- getActivitySummary: last 7 days
- getTodayActivities: today's activities only
- analyzeChild: calls Supabase Edge Function (analyze-child)

### State Management (stores/auth.ts)
- useAuth: user, loading, signIn, signUp, signOut, loadSession
- useApp: selectedChild, children, setChildren, selectChild, loadChildren
- loadChildren preserves current selection if it still exists

### Activity Logger (log.tsx — 692L)
- 6 activity types with icons, colors, backgrounds
- Duration input: both stepper (+/-) and text input
- Quality selector: poor/fair/good with emojis
- Device selector for screen_time (phone/tablet/tv/pc)
- Meal type + food groups for meal
- Physical activity type selector
- Education subject selector

## Known Issues / Notes
- CLAUDE.md says SDK 54 — actual package.json shows ~52.0.0
- CLAUDE.md says Firebase Auth — FIXED (now says Supabase)
- createChild passes userId from Zustand store, not from getUser()
- signUp intentionally does NOT set user state (email confirmation flow)
- migration_add_activity_types.sql adds nap + physical_activity but schema.sql CHECK constraint NOT updated
- Notification toggles (notifEnabled, weeklyReport) are local state only — not persisted to DB or user prefs
- Edit Profile, Change Password, Privacy Settings, Biometric Login, Help & FAQ are all placeholder items (no onPress handlers)
- Social login buttons (Google/Apple) on login screen are placeholders (no auth providers configured)

## SCOPE.md Milestone Status
- **Milestone 1 (₱5,000):** Core app — auth, dashboard, logging, 6 activity types, child management
- **Milestone 2 (₱4,000):** Pending — AI recommendations finalization, settings polish, Edge Function
- **Milestone 3 (₱3,000):** Pending — APK build, Supabase transfer, handover docs, walkthrough

## Uncommitted Changes (2026-04-13)
- **New:** `app/(tabs)/history.tsx` (564L) — Activity history browser with SectionList
- **New:** `SCOPE.md` — Project scope and agreement document
- **New:** `smart-parenting-app-flow.excalidraw` — Architecture diagram
- **Modified:** 9 files — theme completion (remaining #3B82F6 → #FF7F60 coral), tab bar adjustments

## Git History (last 15 commits)
```
7ef4e79 fix: add fade out to welcome and goodbye animations
d16be13 fix: login animation — delay auth guard redirect by 1.8s
f45e2f3 feat: sign out confirmation modal + welcome/goodbye animations
4204d1a fix: remove Contact Support and Rate NestNote from settings
9b2b833 redesign: settings screen with parent profile card + HCI principles
873016c fix: child selection resets on focus — preserve selected child across reloads
c5f869e fix: remove active pill from tab bar — use filled icon + color only
37bd024 fix: multi-child display on dashboard + nav bar sizing for iPhone 14 Pro Max
9ca6929 feat: child picker on log screen — tap to switch who you're logging for
553d143 redesign: nav bar regular tabs, log screen with 6 types, text input, meal details
64a25e8 fix: data loading race condition — useApp.getState() instead of stale closure
a773017 fix: dashboard shows real activity data + AI insights generate local recommendations
5b41fe4 redesign: Log Activity screen with HCI — fixed button, stepper inputs, visual type selector
35082b2 redesign: dashboard + nav bar with HCI principles
14bd1e1 redesign: HCI feedback — inline validation, visual states, success screens
```
