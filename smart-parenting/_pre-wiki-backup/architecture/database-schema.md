## Overview

**File:** `database/schema.sql` (527 lines, ~24KB)
**Consolidated:** 2026-04-25 from 14 prior migration files
**Purpose:** Single-file fresh-setup schema for Supabase SQL Editor

---

## Table Architecture

### `children` — Child Profiles

| Column | Type | Notes |
|--------|------|-------|
| `id` | `UUID` | PK, auto-generated |
| `parent_id` | `UUID` | FK → `auth.users(id)`, ON DELETE CASCADE |
| `name` | `TEXT` | Required |
| `date_of_birth` | `DATE` | Optional |
| `avatar_url` | `TEXT` | URL or emoji string |
| `gender` | `TEXT` | `'male'` or `'female'` (NULL allowed) |
| `max_screen_time_minutes` | `INTEGER` | NULL = no limit |
| `min_sleep_minutes` | `INTEGER` | NULL = no minimum |
| 9 × `*_time` | `TIME` | Bedtime, wake, meals, nap, activity, learn — all `HH:MM:SS` |
| `height_cm` | `NUMERIC(5,1)` | e.g. `110.5` |
| `weight_kg` | `NUMERIC(5,1)` | e.g. `18.5` |
| `bmi` | `NUMERIC(4,1)` | Trigger-computed |
| `notifications` | `JSONB` | `{ "bedtime": true, "wake_up": false, ... }` |
| `deleted_at` | `TIMESTAMPTZ` | **Soft delete** — NULL = active |

**Soft delete pattern:** `deleted_at` IS NULL is a mandatory condition in every RLS policy. Deleted children are never returned by any policy.

**BMI Trigger** (lines 246–261):
```sql
NEW.bmi := ROUND((weight_kg / POWER(height_cm / 100.0, 2))::NUMERIC, 1)
```
Fires on INSERT or UPDATE of `height_cm` or `weight_kg`. Converts cm→m automatically.

**`updated_at` Trigger** (lines 233–244):
```sql
NEW.updated_at = NOW()  -- fires on every UPDATE
```

---

### `activities` — Logged Child Activities

| Column | Type | Notes |
|--------|------|-------|
| `id` | `UUID` | PK |
| `child_id` | `UUID` | FK → `children(id)` ON DELETE **RESTRICT** |
| `type` | `TEXT` | Enum: screen_time, sleep, nap, meal, physical_activity, education |
| `value` | `JSONB` | Flexible per-type payload |
| `recorded_at` | `TIMESTAMPTZ` | When the activity happened (user-entered, not server time) |
| `created_at` | `TIMESTAMPTZ` | When the record was created |

**ON DELETE RESTRICT** on `child_id` — prevents deleting a child if activities exist. This is intentional: "protect data" (line 83 comment).

**Type enum:**
```
screen_time | sleep | nap | meal | physical_activity | education
```

**`value` JSONB shape by type** (reconstructed from app code):
```ts
screen_time: { hours, minutes, category, device }
sleep:       { hours, minutes, quality }
nap:         { hours, minutes, quality }  // stored as type 'nap' in DB
meal:        { meal_type, start_time, food_groups[], quality }
physical_activity: { hours, minutes, activity }
education:   { hours, minutes, subject }
```

---

### `recommendations` — AI-Generated Insights

| Column | Type | Notes |
|--------|------|-------|
| `id` | `UUID` | PK |
| `child_id` | `UUID` | FK → `children(id)` ON DELETE RESTRICT |
| `content` | `TEXT` | The insight text |
| `category` | `TEXT` | e.g. "sleep", "nutrition" |
| `priority` | `TEXT` | `'low'` / `'medium'` / `'high'` |
| `insight_type` | `TEXT` | `'risk'` / `'opportunity'` / `'follow_up'` / `'positive'` |
| `trend` | `TEXT` | `'worsening'` / `'stable'` / `'improving'` |
| `based_on` | `JSONB` | Audit trail of what data generated this |
| `created_at` | `TIMESTAMPTZ` | |

**`based_on` JSONB** carries the data provenance — what activities, date range, and comparison period informed the AI's recommendation.

---

### `alerts` — Child Health Alerts

| Column | Type | Notes |
|--------|------|-------|
| `id` | `UUID` | PK |
| `child_id` | `UUID` | FK → `children(id)` ON DELETE RESTRICT |
| `type` | `TEXT` | Alert category (freeform) |
| `message` | `TEXT` | Human-readable alert text |
| `severity` | `TEXT` | `'info'` / `'warning'` / `'critical'` |
| `acknowledged` | `BOOLEAN` | Default FALSE |
| `created_at` | `TIMESTAMPTZ` | |

Unlike `recommendations` (AI-generated), alerts are derived from parent-entered activity data — computed client-side or via Edge Function.

---

### `scheduled_activities` — Planned Routines

| Column | Type | Notes |
|--------|------|-------|
| `id` | `UUID` | PK |
| `child_id` | `UUID` | FK → `children(id)` ON DELETE RESTRICT |
| `type` | `TEXT` | Same 6-type enum as activities |
| `start_time` | `TIMESTAMPTZ` | When the scheduled activity begins |
| `min_duration_minutes` | `INTEGER` | Flexible window start |
| `max_duration_minutes` | `INTEGER` | Flexible window end |
| `planned_end_time` | `TIMESTAMPTZ` | Hard end time |
| `category` | `TEXT` | For screen_time: 'leisure' or 'educational' |
| `status` | `TEXT` | `'pending'` / `'completed'` / `'skipped'` |
| `min_notification_id` | `TEXT` | Expo notif ID for start reminder |
| `max_notification_id` | `TEXT` | Expo notif ID for end-of-window reminder |
| `meal_type` | `TEXT` | For meals: breakfast/lunch/snack/dinner |
| `food_groups` | `TEXT[]` | Array: fruits, vegetables, protein, grains, dairy |

**Flexible duration design:** `min/max_duration_minutes` allows scheduling a range (e.g., "nap 12:00–2:00 PM") rather than a fixed duration. Notifications fire at `start_time` (min) and `planned_end_time` (max).

---

## Compatibility Guards (lines 142–202)

These `ALTER TABLE ADD COLUMN IF NOT EXISTS` statements allow the consolidated schema to **re-run safely** on databases that already have a partial schema from earlier migration files. Fresh projects get columns from `CREATE TABLE`; older databases get them here.

Key pattern — constraints are **dropped and recreated** (not `ADD CONSTRAINT IF NOT EXISTS`, since that doesn't exist in PostgreSQL):
```sql
ALTER TABLE children DROP CONSTRAINT IF EXISTS children_gender_check;
ALTER TABLE children ADD CONSTRAINT children_gender_check
  CHECK (gender IS NULL OR gender IN ('male', 'female'));
```

Also notable: `min_duration_minutes` and `max_duration_minutes` start as NOT NULL in the CREATE but get their NOT NULL constraint **dropped** via ALTER (line 169–170) — meaning they can be NULL in `scheduled_activities`.

---

## Indexes (lines 267–280)

| Index | Columns | Purpose |
|-------|---------|---------|
| `idx_children_parent` | `(parent_id)` | Fast child lookup per parent |
| `idx_activities_child_type` | `(child_id, type)` | Filter activities by child + type |
| `idx_activities_child_recorded` | `(child_id, recorded_at DESC)` | History queries, newest first |
| `idx_recommendations_child` | `(child_id)` | |
| `idx_recommendations_child_created` | `(child_id, created_at DESC)` | Recent recommendations |
| `idx_alerts_child` | `(child_id)` | |
| `idx_scheduled_child` | `(child_id)` | |
| `idx_scheduled_child_status` | `(child_id, status)` | Pending activities per child |
| `idx_scheduled_child_type` | `(child_id, type)` | |
| `idx_scheduled_end_time` | `(planned_end_time)` | **Partial index** — only pending rows |

**Partial index** on `idx_scheduled_end_time` (line 280) — only indexes pending scheduled activities, keeping it lean.

---

## Storage — Avatar Bucket (lines 286–365)

**Bucket:** `'avatars'`, public = true

**Ownership check function** `public.is_owned_avatar_object()` (lines 290–318):
```sql
-- Two paths:
1. bucket = 'avatars' (user avatars)
   filename starts with auth.uid() + '_'

2. bucket = 'child-avatars'
   filename starts with auth.uid() + '_'
   OR filename's first segment is a UUID that belongs to one of the
   authenticated user's non-deleted children
```

This dual-path check allows both parent avatars and child avatars to be uploaded, while restricting uploads to the owning user.

**Policies:**

| Policy                  | Target | Access                                                      |
| ----------------------- | ------ | ----------------------------------------------------------- |
| `avatars_insert_own`    | INSERT | Authenticated, ownership check via `is_owned_avatar_object` |
| `avatars_select_public` | SELECT | **Public** (anyone can view avatars)                        |
| `avatars_update_own`    | UPDATE | Authenticated, ownership check (USING + WITH CHECK)         |
| `avatars_delete_own`    | DELETE | Authenticated, ownership check                              |

All previous policies are explicitly dropped before creating new ones (lines 320–332) — idempotent.

---

## Row Level Security (lines 368–527)

**All 5 tables have RLS enabled.** Every policy follows the same ownership pattern:

### Pattern A — Direct ownership (`children`)
```sql
parent_id = auth.uid() AND deleted_at IS NULL
```
Simple, no subquery needed.

### Pattern B — Via children ownership (all other tables)
```sql
child_id IN (
  SELECT id FROM children
  WHERE parent_id = auth.uid() AND deleted_at IS NULL
)
```
Every non-children table goes through `children` to verify ownership. This means **deleting a child** (soft-delete) immediately revokes access to all their activities, recommendations, alerts, and schedules — no cascade delete needed, data is protected.

### CRUD per table
All 5 tables get 4 policies each: SELECT, INSERT, UPDATE, DELETE — totaling 20 application policies.

**UPDATE policies** use both `USING` (filtering which rows are visible) and `WITH CHECK` (filtering what values can be written):
```sql
FOR UPDATE USING (parent_id = auth.uid() AND deleted_at IS NULL)
WITH CHECK (parent_id = auth.uid())
-- WITH CHECK prevents setting parent_id to someone else during UPDATE
```

**DELETE policy** on `children` is soft-delete-equivalent — since `deleted_at IS NULL` is in the USING clause, the delete would only succeed if `deleted_at` were already NULL (which it is for active children). But the actual delete flow in the app uses `deleteChild()` which likely sets `deleted_at` rather than hard-deleting.

---

## Key Design Decisions

1. **`ON DELETE RESTRICT` on all FKs from activities/recommendations/alerts/scheduled_activities** — data protection: a child cannot be deleted if related records exist. Must delete/revoke those first.

2. **Soft delete on children** — `deleted_at` is the single mechanism. All RLS policies filter it out. No actual DELETE row removal ever needed.

3. **Avatar bucket public read** — `avatars_select_public` is `TO public`, meaning anyone with the URL can view avatars. Only writes require authentication and ownership.

4. **BMI as computed column** — DB-level trigger ensures BMI is always in sync with height/weight. No app-level race condition possible.

5. **`recorded_at` vs `created_at`** — `recorded_at` is when the activity happened (user-provided), `created_at` is when the DB record was created. The app uses `recorded_at` for all date filtering in History tab.

6. **`notifications` as JSONB** — per-routine toggles stored as a single JSONB column. Avoids a separate `child_notifications` table. Schema evolution is easy (add new keys without migrations).

7. **`scheduled_activities` flexible duration** — min/max range design lets parents set "nap between 12–2 PM" rather than "nap exactly 2 hours." Supports notification scheduling at both boundaries.