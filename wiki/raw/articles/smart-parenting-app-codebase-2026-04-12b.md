# Smart Parenting App — Codebase Ingestion (2026-04-12b)

**Source:** ~/local-projects/smart-parenting-app/ (live codebase)
**Date:** 2026-04-12 (post-settings-redesign)
**Branch:** feature/ui-redesign-nestnote
**Commits since last ingestion:** 5 (settings redesign, sign-out modal, welcome/goodbye animations)

## Project Overview

AI-based child activity monitoring mobile application. Freelance commission (₱12K). React Native + Expo + Supabase + OpenRouter.

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
| Storage | AsyncStorage | ^2.1.0 |
| Build | Expo EAS | (eas.json present) |

## Directory Structure

```
smart-parenting-app/
├── app/
│   ├── _layout.tsx          # Root: PaperProvider + Stack + auth guard (86L)
│   ├── (auth)/
│   │   ├── _layout.tsx      # Auth stack (11L)
│   │   ├── login.tsx        # Login screen (473L — welcome animation, social buttons)
│   │   └── signup.tsx       # Signup screen (594L)
│   ├── (tabs)/
│   │   ├── _layout.tsx      # Tab navigator (74L)
│   │   ├── index.tsx        # Dashboard (786L — stats, today's activities, child picker)
│   │   ├── log.tsx          # Activity logger (693L — 6 types, stepper+text duration)
│   │   ├── ai.tsx           # AI recommendations (590L — filter bar, priority sorting)
│   │   └── profile.tsx      # Settings (533L — profile card, sections, sign-out modal)
│   └── child/
│       └── new.tsx          # Add child screen (386L — quick age selectors)
├── lib/
│   ├── supabase.ts          # Supabase client (lazy-load, SSR-safe) (42L)
│   └── api.ts               # CRUD: children, activities, recommendations (122L)
├── stores/
│   └── auth.ts              # Zustand: useAuth + useApp stores (71L)
├── database/
│   ├── schema.sql           # Full schema (4 tables, RLS, triggers, indexes) (201L)
│   └── migration_add_activity_types.sql  # Add nap + physical_activity (10L)
├── assets/                  # Icons, splash
├── dist/                    # Web export (HTML files)
├── CLAUDE.md                # AI coding guidance
├── SCOPE.md                 # Project scope, milestones, payment terms (212L)
└── smart-parenting-app-flow.excalidraw  # Architecture diagram
```

## Color Theme (Coral — applied 2026-04-12)

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
  meals:        #F59E0B  bg: #FFFBEB
  education:    #8B5CF6  bg: #F5F3FF
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

### Auth Flow (with animations)
- Root layout checks auth state → redirects to /(auth)/login if unauthenticated
- **Welcome animation on login:** Animated.parallel (opacity 0→1, spring scale 0.8→1), shows 1.2s, then fades out
- **Auth guard delay:** _layout.tsx delays redirect to /(tabs) by 1.8s after login to let welcome animation complete (uses useRef timer, clears on unmount)
- signUp does NOT auto-login (prevents email confirmation issues)
- onAuthStateChange listener for session persistence

### Sign-Out Flow (NEW — post-Apr 12)
- **Confirmation modal:** Modal (transparent, fade) with icon, title, description, Cancel/Sign Out buttons
- **Goodbye animation:** Animated.parallel (opacity 0→1, spring scale 0.8→1), shows 1.2s, then fades out
- After animation: calls signOut(), resets scale, navigates to /(auth)/login
- Pattern mirrors welcome animation (same timing, spring config)

### Settings Screen (profile.tsx — redesigned 2026-04-12)
Structure (top to bottom):
1. **Header** — "Settings" title
2. **Parent Profile Card** — avatar (initials), name, email, edit button
3. **Account section** — Edit Profile, Email, Change Password (all placeholders)
4. **Children section** — ChildCard per child (avatar, name, age), Add Child button
5. **Notifications section** — Push Notifications toggle, Weekly Summary toggle (local state only)
6. **Privacy & Security section** — Privacy Settings, Biometric Login (placeholders)
7. **Support section** — Help & FAQ (placeholder)
8. **Sign Out button** — triggers confirmation modal
9. **Version** — "NestNote v1.0.0"

Reusable components: `Section`, `Item`, `ChildCard`

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

### Activity Logger (log.tsx)
- 6 activity types with icons, colors, backgrounds
- Duration input: both stepper (+/-) and text input
- Quality selector: poor/fair/good with emojis
- Device selector for screen_time (phone/tablet/tv/pc)
- Meal type + food groups for meal
- Physical activity type selector
- Education subject selector

## Known Issues / Notes
- README says SDK 52, CLAUDE.md says SDK 54 — actual package.json shows ~52.0.0
- CLAUDE.md says Firebase Auth — actual code uses Supabase Auth exclusively (fixed in wiki, NOT in CLAUDE.md)
- createChild passes userId from Zustand store, not from getUser()
- signUp intentionally does NOT set user state (email confirmation flow)
- migration_add_activity_types.sql adds nap + physical_activity but schema.sql CHECK constraint NOT updated
- Notification toggles (notifEnabled, weeklyReport) are local state only — not persisted to DB or user prefs
- Edit Profile, Change Password, Privacy Settings, Biometric Login, Help & FAQ are all placeholder items (no onPress handlers)
- Social login buttons (Google/Apple) on login screen are placeholders (no auth providers configured)

## SCOPE.md Milestone Status
- **Milestone 1 (₱5,000):** All items checked — core app complete
- **Milestone 2 (₱4,000):** Pending — AI recommendations, Edge Function, settings finalization, UI polish
- **Milestone 3 (₱3,000):** Pending — APK build, Supabase transfer, handover docs, walkthrough

## Recent Git History (last 5 commits)
```
7ef4e79 fix: add fade out to welcome and goodbye animations
d16be13 fix: login animation — delay auth guard redirect by 1.8s
f45e2f3 feat: sign out confirmation modal + welcome/goodbye animations
4204d1a fix: remove Contact Support and Rate NestNote from settings
9b2b833 redesign: settings screen with parent profile card + HCI principles
```
