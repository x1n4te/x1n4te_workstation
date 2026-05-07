---
id: smart-parenting-app-system-architecture-001
type: concept
created: 2026-04-23
updated: 2026-05-07
last_verified: 2026-05-07
review_after: 2026-07-06
stale_after: 2026-09-04
confidence: high
source_refs:
  - concepts/smart-parenting-app-client-handover
  - concepts/smart-parenting-app-tech-stack
  - concepts/expo-local-notifications
  - sources/operational/2026-04-23-spa-dashboard-scheduled-activities-session
  - sources/operational/2026-05-07-spa-rls-stale-cache-bypass
  - /home/xynate/local-projects/smart-parenting-app/wiki/components/dashboard-screen.md
  - /home/xynate/local-projects/smart-parenting-app/wiki/components/log-screen.md
  - /home/xynate/local-projects/smart-parenting-app/wiki/components/history-screen.md
  - /home/xynate/local-projects/smart-parenting-app/wiki/components/ai-insights-screen.md
  - /home/xynate/local-projects/smart-parenting-app/wiki/components/settings-screen.md
  - /home/xynate/local-projects/smart-parenting-app/wiki/components/5step-add-child-wizard.md
  - /home/xynate/local-projects/smart-parenting-app/wiki/lib/api.md
  - /home/xynate/local-projects/smart-parenting-app/wiki/lib/supabase.md
  - /home/xynate/local-projects/smart-parenting-app/wiki/database/schema-overview.md
  - /home/xynate/local-projects/smart-parenting-app/wiki/stores/auth.md
  - /home/xynate/local-projects/smart-parenting-app/wiki/concepts/child-picker-state-propagation.md
  - /home/xynate/local-projects/smart-parenting-app/wiki/supabase/edge-function-analyze-child.md
status: active
tags:
  - smart-parenting-app
  - mobile-dev
  - software-dev
  - design
related:
  - concepts/smart-parenting-app-client-handover
  - concepts/smart-parenting-app-tech-stack
  - concepts/expo-local-notifications
  - concepts/hci-design-principles-mobile
  - sources/operational/2026-05-07-spa-rls-stale-cache-bypass
---

# Smart Parenting App — System Architecture

## Purpose
This page explains how Smart Parenting is divided between frontend and backend responsibilities. Use [[concepts/smart-parenting-app-client-handover]] for a user-facing walkthrough and [[concepts/smart-parenting-app-tech-stack]] for stack/version history.

## Executive Summary
Smart Parenting uses a mobile-first client plus backend-as-a-service architecture.

- Frontend: React Native + Expo owns presentation, routing, local validation, screen state, child-context switching, and device-native services such as local notifications.
- Backend: Supabase owns authentication, PostgreSQL storage, Row Level Security, Storage for media, and an Edge Function for AI recommendation generation.
- Standard CRUD does not go through a custom always-on app server. The mobile app talks directly to Supabase through `lib/api.ts` and depends on RLS for parent-scoped authorization.
- The only privileged compute path is the AI analysis Edge Function, which runs with service-role access and writes recommendation rows back into the database.

## High-Level Topology
```text
┌───────────────────────────────────────────────────────────────┐
│                       Mobile Device                           │
│  React Native + Expo app                                     │
│  ├─ Expo Router screens                                      │
│  ├─ Zustand auth/child context store                         │
│  ├─ Local validation + form state                            │
│  ├─ AsyncStorage session persistence                         │
│  └─ Expo local notifications                                 │
└──────────────────────────────┬────────────────────────────────┘
                               │
                               ▼
┌───────────────────────────────────────────────────────────────┐
│                    Supabase Project                           │
│  Auth → session + identity                                   │
│  Postgres → children, activities, recommendations, alerts    │
│  RLS → parent-owned data isolation                           │
│  Storage → child photos                                      │
│  Edge Function → analyze-child                               │
└──────────────────────────────┬────────────────────────────────┘
                               │
                               ▼
┌───────────────────────────────────────────────────────────────┐
│                Configured External AI Provider                │
│            Called only by the analyze-child function         │
└───────────────────────────────────────────────────────────────┘
```

## Frontend Architecture

### App shell and navigation
The app is organized around Expo Router. Primary route groups are `(auth)` for login/signup, `(tabs)` for Dashboard/Log/History/AI/Settings, `child/wizard.tsx` for the 5-step Add Child flow, and `settings/*` for account/per-child management. The shell gates unauthenticated users, waits for store hydration, and keeps navigation mobile-first.

### State management boundary
Global state is intentionally small. `stores/auth.ts` holds the authenticated session, current user, `selectedChildId`, and hydration status. This store is the coordination point for Dashboard, Log, History, and AI Insights: when the parent switches child once, all subscribed screens re-render against the same active child. This propagation model is described in the repo wiki's child-picker-state-propagation page.

### Frontend service layer
The frontend uses two key modules:

- `lib/supabase.ts` → lazy singleton client initialization so the app can restore session state from AsyncStorage without blocking startup.
- `lib/api.ts` → app-facing CRUD and Edge Function wrappers such as `getChildren()`, `createChild()`, `updateChild()`, `createActivity()`, `getActivitiesByDateRange()`, `getRecommendations()`, and `runAiAnalysis()`.

This keeps screens focused on interaction logic instead of low-level transport code.

### Screen responsibilities
| Surface | Main responsibility | Writes performed |
|---|---|---|
| Dashboard | Daily summary, child switching, upcoming schedule actions | Instant schedule logging, schedule update, schedule delete |
| Log | Activity entry UI per type | Creates activity rows |
| History | Historical browsing and filtering | None |
| AI Insights | Recommendation display and AI trigger | Calls Edge Function path |
| Settings | Account, child edits, notification preferences | Updates child profile/routine/settings |
| Add Child Wizard | Progressive onboarding | Creates child, saves routine/settings, triggers notifications |

### Validation and interaction model
The frontend owns most user-facing validation. Activity forms validate by type before `createActivity()`. Wizard steps validate incrementally before advancing. Inline feedback is preferred over popups, and loading/success states are shown close to the triggering action. This aligns with [[concepts/hci-design-principles-mobile]].

### Device-local capabilities
Some important behavior is frontend-only: session persistence in AsyncStorage, local notification scheduling through Expo Notifications, transient UI state, and immediate BMI preview calculation during onboarding. Routine reminders are local device notifications derived from child settings, not server push notifications. See [[concepts/expo-local-notifications]].

## Backend Architecture

### Core pattern: direct-to-Supabase BaaS
The backend is not a traditional custom REST server for normal app operations. The mobile client authenticates with Supabase Auth, uses anon-key access with the authenticated session, calls named operations in `lib/api.ts`, and relies on PostgreSQL + RLS to enforce ownership rules. The real security boundary for standard CRUD is the database policy layer, not button logic.

### Data model
The repo wiki currently documents 4 core user-facing tables:

- `children`
- `activities`
- `recommendations`
- `alerts`

Relationship chain:
```text
auth.users
   └─ children (parent_id)
        ├─ activities (child_id)
        ├─ recommendations (child_id)
        └─ alerts (child_id)
```

Operationally, newer Smart Parenting documentation also references `scheduled_activities` for Dashboard upcoming items. That feature is present in the current system narrative, but it is not yet represented consistently across all repo wiki schema pages.

### Access control model
The backend security model is parent-scoped ownership via RLS.

- `children` rows are visible only when `parent_id = auth.uid()`.
- Child-owned tables use subqueries against the caller's allowed children.
- Soft-deleted children are filtered from normal access paths.

This is the most important backend design choice in the app: the client can hold an anon key and still remain safe because the database checks ownership on every query.

### Soft-delete exception path (2026-05-07)
One path now intentionally avoids the normal PostgREST table-update route: child soft-delete. The app hit a stale cached version of the `children_update` RLS policy on the REST API even after PostgreSQL had the corrected policy definition. To fail closed without waiting for cache convergence, `deleteChild()` now calls `soft_delete_child(child_id UUID)` as a `SECURITY DEFINER` RPC.

The function does not grant broad bypass power. It still performs an internal ownership check against `children` using `parent_id = auth.uid()` and `deleted_at IS NULL`, then updates only the authorized row. This is a surgical reliability workaround, not an authorization relaxation. See [[sources/operational/2026-05-07-spa-rls-stale-cache-bypass]].

### Storage and media
Child photos are stored separately from relational rows, with the child profile holding the resulting URL/reference. Architecturally: media is selected on-device, uploaded through the Supabase path, and then attached to the child record.

### AI compute boundary
AI recommendation generation is intentionally separated from normal CRUD.

- Standard reads/writes happen directly from the mobile app to Supabase through `lib/api.ts`.
- The privileged AI path triggers `analyze-child`, which fetches child profile + activity context, aggregates the data, prepares a structured prompt payload, calls the configured upstream model provider, and inserts rows into `recommendations`.

Only the Edge Function should ever use service-role capabilities. The client never receives service-role access.

### Backend responsibilities by layer
| Backend layer | Responsibility |
|---|---|
| Supabase Auth | Sign-in, session identity, auth context |
| PostgreSQL | Durable storage for app entities |
| RLS policies | Authorization enforcement |
| Storage | Child photo persistence |
| Edge Function | AI analysis and recommendation insertion |
| External model provider | Text generation only, behind the Edge Function |

## End-to-End Flows

### Flow 1: Login
```text
Login screen
  → Supabase Auth sign-in
  → auth state stored in Zustand + AsyncStorage
  → hydration completes
  → protected tabs render
```
Frontend owns the UX and state transition; backend owns identity proof and session issuance.

### Flow 2: Add Child
```text
5-step wizard
  → create child profile
  → compute BMI preview/client-side values
  → save routine/settings
  → upload photo if present
  → schedule local notifications
  → child becomes selectable across app
```
This feels like one flow to the parent, but it spans UI state, storage, table writes, and device-local scheduling.

### Flow 3: Log Activity
```text
Log screen
  → validate by activity type
  → createActivity() in lib/api.ts
  → INSERT into activities
  → RLS checks child ownership
  → Dashboard/History refresh against new state
```
This is the clearest example of the direct-to-Supabase architecture: no custom server is required for the happy path.

### Flow 4: Run AI Insights
```text
AI Insights screen
  → runAiAnalysis()
  → Edge Function fetches child + recent activity context
  → summary/prompt assembly
  → external model call via configured provider
  → INSERT recommendations
  → UI reloads stored recommendation batch
```
This is the only flow where the architecture switches from direct CRUD to privileged server-side compute.

## Trust Boundaries
| Zone | Trusted for | Not trusted for |
|---|---|---|
| Mobile UI | Presentation, local interaction state | Enforcing data ownership |
| Client app with anon key | Authenticated CRUD requests | Bypassing authorization |
| PostgreSQL + RLS | Row ownership checks, durable storage | Rich UX behavior |
| Edge Function | Privileged aggregation + AI writeback | Direct user interaction |
| External AI provider | Generating recommendation text | Acting as source of truth for authorization |

Key rule: authorization lives at the Supabase policy layer, not in screen logic.

## Architecture Strengths
1. Simple operational model: no always-on custom app server for standard CRUD.
2. Strong ownership boundary: RLS protects parent-owned data at the database layer.
3. Clean frontend responsibility split: screens handle UX; service modules handle transport.
4. Good mobile fit: AsyncStorage and local notifications are naturally device-centric.
5. AI isolation: privileged model calls are separated behind one Edge Function.

## Known Documentation Gaps and Drift

### AI provider drift
The sources agree that AI runs through `analyze-child`, but they disagree on the exact upstream provider/model.
- Older main wiki pages describe OpenRouter / `openrouter/elephant-alpha`.
- Live code currently defaults to OpenRouter with `inclusionai/ling-2.6-1t:free` via `OPENROUTER_MODEL`.
- The 2026-05-07 operational handoff claims the model was changed to `baidu/cobuddy:free`, but that switch is not visible in the current repo code.

Conclusion: treat the AI layer as provider-pluggable and distinguish verified code defaults from user-reported runtime or deployment changes.

### Notification scope drift
The sources agree that routine reminders are local notifications, but they do not fully agree on the exact toggle model.
- Some pages describe global + per-routine/per-child controls.
- Some repo wiki pages still describe a simpler global-toggle flow.

Conclusion: the stable architectural fact is that notification scheduling is frontend/device-local and derived from child routine settings.

### Scheduled activities coverage gap
Dashboard upcoming items and AI scheduled-activity summaries are documented in recent operational notes, but `scheduled_activities` does not yet have full first-class coverage in the repo wiki schema documentation.

### Deprecated route references remain in navigation docs
Some repo wiki navigation pages still reference the older two-screen child flow (`new.tsx` + `routine.tsx`) even though the current canonical onboarding flow is the unified 5-step wizard.

## Reading Path
Start here for architecture, then branch by need:

1. [[concepts/smart-parenting-app-client-handover]] — best for explaining what users do.
2. [[concepts/smart-parenting-app-tech-stack]] — best for version and feature-history context.
3. `~/local-projects/smart-parenting-app/wiki/components/*.md` — best for per-screen implementation detail.
4. `~/local-projects/smart-parenting-app/wiki/lib/api.md` — best for frontend/backend call boundaries.
5. `~/local-projects/smart-parenting-app/wiki/database/schema-overview.md` — best for persistence and RLS structure.
6. `~/local-projects/smart-parenting-app/wiki/supabase/edge-function-analyze-child.md` — best for AI backend flow.

## Related
- [[concepts/smart-parenting-app-client-handover]] — client-facing walkthrough
- [[concepts/smart-parenting-app-tech-stack]] — stack and feature evolution
- [[concepts/expo-local-notifications]] — device-local reminder subsystem
- [[concepts/hci-design-principles-mobile]] — UX principles applied across the frontend
