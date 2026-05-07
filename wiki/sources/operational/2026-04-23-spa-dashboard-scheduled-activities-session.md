---
id: spa-dashboard-scheduled-activities-2026-04-23
type: source
created: 2026-04-23
updated: 2026-04-23
status: active
tags:
  - smart-parenting-app
  - operational
  - dashboard
  - scheduled-activities
  - hci
source_refs:
  - concepts/smart-parenting-app-tech-stack
  - concepts/smart-parenting-app-client-handover
---

# Smart Parenting App — Dashboard Scheduled Activities Session

**Date:** 2026-04-23
**Focus:** Dashboard "Upcoming" section — instant log, update modal, hard-delete cancel
**Files modified:** `app/(tabs)/index.tsx`, `lib/api.ts`

---

## Changes Summary

### 1. Instant Log (Dashboard → No Navigation)

**Before:** Tapping "Log" on a scheduled activity opened the Log screen with type pre-selected. Parent had to fill the form again and submit.

**After:** Tapping "Log" calls `logActivity()` directly with smart defaults derived from the schedule:

| Scheduled Type | Derived `value` |
|---|---|
| `screen_time` | `{ hours, minutes, category: scheduled.category \|\| 'leisure', device: 'phone' }` |
| `sleep` / `nap` | `{ hours, minutes, quality: 'good' }` |
| `meal` | `{ meal_type: scheduled.meal_type \|\| 'snack', food_groups: [], quality: 'good' }` |
| `physical_activity` | `{ hours, minutes, activity: scheduled.category \|\| 'other' }` |
| `education` | `{ hours, minutes, subject: scheduled.category \|\| 'reading' }` |

**HCI feedback pattern:**
- Idle → "Log" text + pencil icon (coral)
- Loading → spinning sync icon + "Logging…" text
- Success → green checkmark + "Logged!" text (1.8s timeout, then returns to idle)

### 2. Update Schedule Modal

**Trigger:** Tap "Update" on any upcoming scheduled activity card.

**UI:** Slide-up modal sheet (`presentationStyle="overFullScreen"`, `animationType="slide"`) with dark overlay.

**Modal contents:**
- **Activity Type** — 6 color-coded chips (Screen/Sleep/Nap/Meal/Active/Learn)
- **Start Time** — Stepper + RNTextInput + AM/PM toggle (hour/minute/period)
- **End Time** — Same pattern as Start
- **Category / Meal Type** — Single-line text input (switches label based on selected type)
- **Save Changes** — Coral button with loading state

**Time math:**
- Parses existing ISO `start_time` / `planned_end_time` into 12h format on modal open
- Reconstructs new ISO times from edited 12h values on save
- Overnight handled: if newEnd < newStart, adds 24h
- `max_duration_minutes` auto-recalculated from new time delta

### 3. Hard-Delete Cancel

**Before:** "Cancel" button called `updateScheduledActivityStatus(id, 'skipped')` — row persisted with `status='skipped'`.

**After:** "Cancel" button shows inline confirmation row (HCI-compliant, no Alert.alert), then calls `deleteScheduledActivity(id)` which runs `supabase.from('scheduled_activities').delete().eq('id', id)` — row permanently removed.

**Confirmation copy:** "Delete this schedule permanently?" with "Keep" (gray) / "Delete" (red) buttons.

---

## API Additions (`lib/api.ts`)

```ts
export async function deleteScheduledActivity(id: string) {
  const { error } = await (supabase as any)
    .from('scheduled_activities')
    .delete()
    .eq('id', id);
  if (error) throw error;
}

export async function updateScheduledActivity(
  id: string,
  updates: Partial<Omit<ScheduledActivity, 'id' | 'child_id' | 'created_at'>>
) {
  const { data, error } = await (supabase as any)
    .from('scheduled_activities')
    .update(updates)
    .eq('id', id)
    .select()
    .single();
  if (error) throw error;
  return data as ScheduledActivity;
}
```

---

## TypeScript Notes

- `to12h()` helper returns `{ h: string, m: string, p: 'AM' | 'PM' }` — `p` is explicitly cast to the union type to satisfy `useState<'AM' | 'PM'>()`
- No `Alert.alert()` anywhere in the diff (HCI gate passed)
- All async ops followed by `await loadDashboardData()` (refetch gate passed)

---

## Component Signature Changes

`UpcomingItem` props expanded:
```ts
interface UpcomingItemProps {
  scheduled: ScheduledActivity;
  onLog: (s: ScheduledActivity) => Promise<void>;      // NEW
  onUpdate: (s: ScheduledActivity) => void;             // NEW
  onCancel: (id: string) => void;                       // CHANGED: now hard-delete
}
```

---

## Related

- [[concepts/smart-parenting-app-tech-stack]] — updated with new section
- [[concepts/smart-parenting-app-client-handover]] — updated Dashboard section
