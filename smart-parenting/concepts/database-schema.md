---
title: Database Schema
created: 2026-04-25
updated: 2026-04-25
type: concept
tags: [database, architecture, security, rls, supabase]
sources: [raw/technical-reference.md]
---

# Database Schema

**File:** `database/schema.sql` (527 lines, ~24KB)  
**Consolidated:** 2026-04-25 from 14 prior migration files  
**Purpose:** Single-file fresh-setup schema for Supabase SQL Editor

---

## Tables

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
| 9 × `*_time` | `TIME` | Bedtime, wake, meals, nap, activity, learn — `HH:MM:SS` |
| `height_cm` | `NUMERIC(5,1)` | e.g. `110.5` |
| `weight_kg` | `NUMERIC(5,1)` | e.g. `18.5` |
| `bmi` | `NUMERIC(4,1)` | Trigger-computed |
| `notifications` | `JSONB` | `{ "bedtime": true, "wake_up": false, ... }` |
| `deleted_at` | `TIMESTAMPTZ` | **Soft delete** — NULL = active |

**Soft delete pattern:** `deleted_at IS NULL` is mandatory in every RLS policy. Deleted children are never returned.

**BMI Trigger:**
```sql
NEW.bmi := ROUND((weight_kg / POWER(height_cm / 100.0, 2))::NUMERIC, 1)
```
Fires on INSERT/UPDATE of `height_cm` or `weight_kg`.

**`updated_at` Trigger:** Fires on every UPDATE to set `NOW()`.

---

### `activities` — Logged Child Activities

| Column | Type | Notes |
|--------|------|-------|
| `id` | `UUID` | PK |
| `child_id` | `UUID` | FK → `children(id)` ON DELETE **RESTRICT** |
| `type` | `TEXT` | Enum: screen_time, sleep, nap, meal, physical_activity, education |
| `value` | `JSONB` | Flexible per-type payload |
| `recorded_at` | `TIMESTAMPTZ` | User-entered timestamp |
| `created_at` | `TIMESTAMPTZ` | Server timestamp |

**ON DELETE RESTRICT** on `child_id` — prevents deleting a child if activities exist (data protection).

**`value` JSONB shapes:**
```ts
screen_time: { hours, minutes, category, device }
sleep:       { hours, minutes, quality }
nap:         { hours, minutes, quality }
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
| `content` | `TEXT` | Insight text |
| `category` | `TEXT` | e.g. "sleep", "nutrition" |
| `priority` | `TEXT` | `'low'` / `'medium'` / `'high'` |
| `insight_type` | `TEXT` | `'risk'` / `'opportunity'` / `'follow_up'` / `'positive'` |
| `trend` | `TEXT` | `'worsening'` / `'stable'` / `'improving'` |
| `based_on` | `JSONB` | Audit trail — what data generated this |
| `created_at` | `TIMESTAMPTZ` | |

**`based_on` JSONB** carries full data provenance. See [[ai-insights-architecture]] for the audit trail structure.

---

### `alerts` — Child Health Alerts

| Column | Type | Notes |
|--------|------|-------|
| `id` | `UUID` | PK |
| `child_id` | `UUID` | FK → `children(id)` ON DELETE RESTRICT |
| `type` | `TEXT` | Alert category |
| `message` | `TEXT` | Human-readable text |
| `severity` | `TEXT` | `'info'` / `'warning'` / `'critical'` |
| `acknowledged` | `BOOLEAN` | Default FALSE |
| `created_at` | `TIMESTAMPTZ` | |

Unlike `recommendations`, alerts are derived from parent-entered data — computed client-side or via Edge Function.

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

**Flexible duration design:** `min/max_duration_minutes` allows scheduling a range (e.g., "nap 12:00–2:00 PM"). Notifications fire at `start_time` and `planned_end_time`.

See [[screen-activities]] for the scheduling UI and [[screen-dashboard]] for upcoming schedule display.

---

## Compatibility Guards

`ALTER TABLE ADD COLUMN IF NOT EXISTS` statements (lines 142–202) allow the schema to re-run safely on partial databases. Constraints are dropped and recreated — not `ADD CONSTRAINT IF NOT EXISTS` (unsupported in PostgreSQL).

Notable: `min_duration_minutes` and `max_duration_minutes` start as NOT NULL in CREATE but get their NOT NULL constraint dropped via ALTER — meaning they can be NULL in `scheduled_activities`.

---

## Indexes

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

---

## Storage — Avatar Bucket

**Bucket:** `'avatars'`, public = true

**Ownership check function** `public.is_owned_avatar_object()`:
1. `bucket = 'avatars'` → filename starts with `auth.uid() + '_'`
2. `bucket = 'child-avatars'` → filename starts with `auth.uid() + '_'` OR first segment is a UUID belonging to one of the user's non-deleted children

**Policies:**

| Policy | Target | Access |
|--------|--------|--------|
| `avatars_insert_own` | INSERT | Authenticated, ownership check |
| `avatars_select_public` | SELECT | **Public** (anyone can view avatars) |
| `avatars_update_own` | UPDATE | Authenticated, ownership check |
| `avatars_delete_own` | DELETE | Authenticated, ownership check |

---

## Row Level Security

**All 5 tables have RLS enabled.** Every policy follows one of two patterns:

### Pattern A — Direct ownership (`children`)
```sql
parent_id = auth.uid() AND deleted_at IS NULL
```

### Pattern B — Via children ownership (all other tables)
```sql
child_id IN (
  SELECT id FROM children
  WHERE parent_id = auth.uid() AND deleted_at IS NULL
)
```

Soft-deleting a child immediately revokes access to all their activities, recommendations, alerts, and schedules — no cascade delete needed.

**UPDATE policies** use both `USING` and `WITH CHECK`:
```sql
FOR UPDATE USING (parent_id = auth.uid() AND deleted_at IS NULL)
WITH CHECK (parent_id = auth.uid())
```
`WITH CHECK` prevents setting `parent_id` to someone else during UPDATE.

---

## Key Design Decisions

1. **`ON DELETE RESTRICT`** on all FKs from child-related tables — data protection.
2. **Soft delete on children** — `deleted_at` is the single mechanism.
3. **Avatar bucket public read** — only writes require auth + ownership.
4. **BMI as computed column** — DB-level trigger ensures sync.
5. **`recorded_at` vs `created_at`** — user-provided vs server time.
6. **`notifications` as JSONB** — avoids separate table, easy schema evolution.
7. **`scheduled_activities` flexible duration** — min/max range design.
