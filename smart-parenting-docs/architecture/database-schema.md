# Database Schema

The app uses **PostgreSQL** via Supabase with **Row-Level Security (RLS)** enabled on every table. This ensures users can only access their own data.

---

## Tables

### `children` — Child Profiles

Stores one row per child.

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID | Primary key, auto-generated |
| `parent_id` | UUID | Links to the parent user; RLS filters by this |
| `name` | Text | Required |
| `date_of_birth` | Date | Optional |
| `avatar_url` | Text | URL or emoji string |
| `gender` | Text | `male` or `female` (optional) |
| `max_screen_time_minutes` | Integer | Parent-set limit (null = unlimited) |
| `min_sleep_minutes` | Integer | Parent-set minimum (null = none) |
| `bedtime`, `wake_time`, etc. | Time | 9 routine time fields (HH:MM:SS) |
| `height_cm` | Numeric | For BMI calculation |
| `weight_kg` | Numeric | For BMI calculation |
| `bmi` | Numeric | Auto-computed by database trigger |
| `notifications` | JSONB | Toggle map: `{ "bedtime": true, "wake_up": false }` |
| `deleted_at` | Timestamp | Soft delete — null means active |

**Soft deletes:** When a child is "deleted," `deleted_at` is set to the current time. The row remains in the database, but RLS policies hide it from all queries. This protects activity history.

**BMI Trigger:** Automatically recalculates BMI whenever height or weight is updated:
```sql
BMI = weight_kg / (height_cm / 100) ^ 2
```

---

### `activities` — Logged Activities

One row per logged activity.

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID | Primary key |
| `child_id` | UUID | Foreign key to `children` |
| `type` | Text | `screen_time`, `sleep`, `nap`, `meal`, `physical_activity`, `education` |
| `value` | JSONB | Flexible payload — see shapes below |
| `recorded_at` | Timestamp | When the activity happened (user-entered) |
| `created_at` | Timestamp | When the database row was created |

**Value shapes:**
- **screen_time:** `{ hours, minutes, category, device }`
- **sleep / nap:** `{ hours, minutes, quality }`
- **meal:** `{ meal_type, start_time, food_groups[], quality }`
- **physical_activity:** `{ hours, minutes, activity }`
- **education:** `{ hours, minutes, subject }`

---

### `recommendations` — AI Insights

One row per AI-generated recommendation.

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID | Primary key |
| `child_id` | UUID | Foreign key to `children` |
| `content` | Text | The recommendation text |
| `category` | Text | `sleep`, `meal`, `education`, `screen_time`, `general` |
| `priority` | Text | `low`, `medium`, `high` |
| `insight_type` | Text | `risk`, `opportunity`, `follow_up`, `positive` |
| `trend` | Text | `worsening`, `stable`, `improving` |
| `based_on` | JSONB | Audit trail — see below |
| `created_at` | Timestamp | Generation date |

**Audit trail (`based_on`):**
```json
{
  "period": "2026-03-28 to 2026-04-25",
  "compact_summary": { "screen_time": {...}, "sleep": {...} },
  "previous_rec_ids": ["uuid1", "uuid2"],
  "child_settings": { "max_screen_time_minutes": 120 },
  "bmi_category": "normal",
  "age_months": 42,
  "model": "inclusionai/ling-2.6-1t:free",
  "confidence": "high"
}
```

This makes every recommendation reproducible.

---

### `alerts` — Health Alerts

Derived alerts from activity data (not AI-generated).

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID | Primary key |
| `child_id` | UUID | Foreign key |
| `type` | Text | Alert category |
| `message` | Text | Human-readable text |
| `severity` | Text | `info`, `warning`, `critical` |
| `acknowledged` | Boolean | Default false |
| `created_at` | Timestamp | |

---

### `scheduled_activities` — Planned Activities

Future activities with reminder notifications.

| Column | Type | Notes |
|--------|------|-------|
| `id` | UUID | Primary key |
| `child_id` | UUID | Foreign key |
| `type` | Text | Same 6 types as `activities` |
| `start_time` | Timestamp | When the activity begins |
| `min_duration_minutes` | Integer | Flexible window start |
| `max_duration_minutes` | Integer | Flexible window end |
| `planned_end_time` | Timestamp | Computed hard end time |
| `category` | Text | For screen time: `leisure` or `educational` |
| `status` | Text | `pending`, `completed`, `skipped` |
| `meal_type` | Text | `breakfast`, `lunch`, `snack`, `dinner` |
| `food_groups` | Text[] | Array of food groups |

---

## Security (RLS)

Every table has **Row-Level Security** enabled. The policies follow two patterns:

**Pattern A — Direct ownership (`children` table):**
```sql
parent_id = auth.uid() AND deleted_at IS NULL
```

**Pattern B — Via child ownership (all other tables):**
```sql
child_id IN (
  SELECT id FROM children
  WHERE parent_id = auth.uid() AND deleted_at IS NULL
)
```

This means:
- A user can only see their own children.
- A user can only see activities, recommendations, alerts, and schedules belonging to their children.
- Soft-deleting a child immediately revokes access to all related data.

---

## Storage

**Bucket:** `avatars` (public read)

Users can upload avatar images. The filename must start with their user ID to pass the ownership check.

---

## Indexes

Key indexes for performance:
- `idx_children_parent` — fast child lookup per parent
- `idx_activities_child_recorded` — history queries, newest first
- `idx_recommendations_child_created` — recent recommendations
- `idx_scheduled_child_status` — pending activities per child
