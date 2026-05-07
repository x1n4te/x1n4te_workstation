---
id: smart-parenting-session-2026-04-12b-001
type: source
created: 2026-04-12b
updated: 2026-04-12b
last_verified: 2026-04-12b
review_after: 2026-05-12
stale_after: 2026-07-12
confidence: high
source_refs:
  - raw/articles/smart-parenting-app-codebase-2026-04-12b
status: active
tags:
  - smart-parenting-app
  - mobile-dev
  - operational
related:
  - concepts/smart-parenting-app-tech-stack
  - sources/operational/2026-04-12-smart-parenting-session
---

# Smart Parenting App — Codebase Re-Ingestion (2026-04-12b)

**Trigger:** New feature to add — re-ingest codebase to capture changes since last wiki update.

---

## Changes Since Last Ingestion (Apr 12)

5 commits on branch `feature/ui-redesign-nestnote`. Package.json, schema, and API layer unchanged.

### 1. Settings Screen Redesign (profile.tsx — 510 lines changed)
- **Before:** Simple list of settings items
- **After:** Full redesign with:
  - Parent Profile Card (avatar initials, name, email, edit button)
  - 5 grouped sections: Account, Children, Notifications, Privacy & Security, Support
  - Reusable components: `Section`, `Item`, `ChildCard`
  - Notification toggles (Push Notifications, Weekly Summary) — local state only
  - Placeholder items: Edit Profile, Change Password, Privacy Settings, Biometric Login, Help & FAQ
  - Removed: Contact Support, Rate NestNote

### 2. Sign-Out Confirmation Modal + Goodbye Animation
- Modal: transparent overlay, centered card with icon, title, text, Cancel/Sign Out buttons
- Goodbye animation: Animated.parallel (opacity + spring scale), shows 1.2s, fades out
- After animation: signOut() → reset scale → navigate to /(auth)/login
- Pattern mirrors welcome animation (same timing/friction)

### 3. Login Welcome Animation + Auth Guard Delay
- Welcome overlay: Animated.parallel (opacity + spring scale), shows 1.2s, fades out
- _layout.tsx: Auth guard delays redirect to /(tabs) by 1.8s via useRef timer
- Timer cleared on unmount to prevent stale redirects

### 4. Theme Already Documented (Apr 12 session)
- Coral #FF7F60 primary, cream #FEFBF6 background, surface #FFFDFF
- Applied across all files in earlier session — this ingestion confirms it's still current

---

## Wiki Updates
- Created: `wiki/raw/articles/smart-parenting-app-codebase-2026-04-12b.md` — full codebase snapshot
- Updated: `wiki/concepts/smart-parenting-app-tech-stack.md`
  - Added source_ref to new raw file
  - Added UI Patterns section: Coral theme tokens, welcome/goodbye animation pattern, sign-out modal pattern, settings screen architecture
  - Bumped updated date

---

## Key Observations
- **Schema drift:** `schema.sql` CHECK constraint has 4 activity types; `migration_add_activity_types.sql` adds nap + physical_activity but schema.sql NOT updated. Code references all 6 types.
- **State-only toggles:** Notification switches (notifEnabled, weeklyReport) are useState — not persisted to Supabase or AsyncStorage. User preference will be lost on app restart.
- **CLAUDE.md still wrong:** Claims Firebase Auth and SDK 54. Actual: Supabase Auth + SDK ~52.0.0.
- **Placeholder items:** 5 settings items have no onPress handlers (Edit Profile, Change Password, Privacy Settings, Biometric Login, Help & FAQ).
- **Social login placeholders:** Google and Apple buttons on login screen are non-functional (no OAuth providers configured).

---

## Feature Readiness for New Addition
Codebase is well-structured for new feature work:
- Auth flow stable (welcome/goodbye animations working)
- Settings screen has clean component architecture (Section/Item pattern)
- API layer has clear CRUD patterns to follow
- RLS policies enforce parent_id ownership on all tables
- Zustand stores handle state cleanly
