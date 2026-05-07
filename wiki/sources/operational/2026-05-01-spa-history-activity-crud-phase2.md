---
id: 2026-05-01-spa-history-activity-crud-phase2
type: source
created: 2026-05-01
updated: 2026-05-01
confidence: high
source_type: operational-session
status: active
tags:
  - smart-parenting-app
  - react-native
  - supabase
  - history
  - crud
---

# Smart Parenting App — History Activity CRUD Phases 1-2

Implemented the first two implementation phases for History activity update/delete CRUD.

## Phase 1 API surface

- Added `ActivityValue = Record<string, unknown>` in `lib/api.ts`.
- Replaced `Activity.value: Record<string, any>` with `ActivityValue`.
- Added `UpdateActivityInput` with narrow update fields only: `type`, `value`, `recorded_at`.
- Added `updateActivity(id, updates)` and `deleteActivity(id)` direct Supabase helpers.
- Typed the Supabase client with generated `Database` types from `lib/database.types.ts`.
- Did not add `child_id` updates, service-role credentials, schema changes, or RLS changes.

## Phase 2 shared activity value utilities

- Added `lib/activity-values.ts` with shared option constants for activity CRUD UI:
  - activity type config
  - quality options
  - device options
  - screen categories
  - meal options
  - food groups
  - physical activity options
  - education subject options
- Added safe helpers for JSONB payload reads:
  - `getDurationMinutes()`
  - `getDurationLabel()`
  - `getFoodGroups()`
  - `getActivityLabel()`
- Added `buildUpdatedActivityValue()` normalizer for edit modal payloads.
- Rewired History labels/stats to use shared helpers and removed the local `getActivityLabel()` duplicate.

## Verification

- `npx tsc --noEmit` passed.
- `git diff --check` passed for changed files.
- No `Alert.alert()` added.
- No new `any` in `lib/activity-values.ts`.
- No RLS or database schema files changed.
