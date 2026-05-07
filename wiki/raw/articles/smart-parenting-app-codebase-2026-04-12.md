# Smart Parenting App — Codebase Ingestion (2026-04-12)

**Source:** ~/local-projects/smart-parenting-app/ (live codebase)
**Date:** 2026-04-12
**Branch:** feature/ui-redesign-nestnote

## Project Overview

AI-based child activity monitoring mobile application. Freelance commission (₱12K). React Native + Expo + Supabase + OpenRouter.

## Tech Stack (from package.json)

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
│   ├── _layout.tsx          # Root: PaperProvider + Stack + auth guard
│   ├── (auth)/
│   │   ├── _layout.tsx      # Auth stack
│   │   ├── login.tsx        # Login screen (animated welcome)
│   │   └── signup.tsx       # Signup screen
│   ├── (tabs)/
│   │   ├── _layout.tsx      # Tab navigator (Home, Log, Insights, Settings)
│   │   ├── index.tsx        # Dashboard (785L — stats, today's activities, child picker)
│   │   ├── log.tsx          # Activity logger (692L — 6 types, stepper+text duration)
│   │   ├── ai.tsx           # AI recommendations (589L — filter bar, priority sorting)
│   │   └── profile.tsx      # Profile/Settings (532L — child cards, settings items)
│   └── child/
│       └── new.tsx          # Add child screen (385L — quick age selectors)
├── lib/
│   ├── supabase.ts          # Supabase client (lazy-load, SSR-safe)
│   └── api.ts               # CRUD: children, activities, recommendations
├── stores/
│   └── auth.ts              # Zustand: useAuth + useApp stores
├── database/
│   ├── schema.sql           # Full schema (4 tables, RLS, triggers, indexes)
│   └── migration_add_activity_types.sql  # Add nap + physical_activity
├── assets/                  # Icons, splash
└── dist/                    # Web export (HTML files)
```

## Database Schema (from schema.sql)

### Tables
1. **children** — parent_id (FK auth.users), name, date_of_birth, soft-delete (deleted_at)
2. **activities** — child_id (FK children), type (6 types), value (JSONB), recorded_at
3. **recommendations** — child_id, content, category, priority (low/medium/high), based_on (JSONB)
4. **alerts** — child_id, type, message, severity (info/warning/critical), acknowledged

### Activity Types (after migration)
screen_time, sleep, nap, meal, physical_activity, education

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

### Auth Flow
- Root layout checks auth state → redirects to /(auth)/login if unauthenticated
- Welcome animation on login (opacity + scale, 1.8s delay before redirect)
- signUp does NOT auto-login (prevents email confirmation issues)
- onAuthStateChange listener for session persistence

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

### UI Theme (from _layout.tsx)
- Primary: #3B82F6 (blue)
- Background: #F8FAFC
- Activity-specific colors: screen_time=#3B82F6, sleep=#10B981, meals=#F59E0B, education=#8B5CF6
- Custom colors added to MD3LightTheme: screenTime, sleep, meals, education + bg variants

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
- CLAUDE.md says Firebase Auth — actual code uses Supabase Auth exclusively
- createChild passes userId from Zustand store, not from getUser()
- signUp intentionally does NOT set user state (email confirmation flow)
