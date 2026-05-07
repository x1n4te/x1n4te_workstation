---
title: Activities (Log / Schedule) Screen
created: 2026-04-25
updated: 2026-04-25
type: concept
tags: [screen, activities, ui-ux, component]
sources: [raw/technical-reference.md]
---

# Activities (Log / Schedule) Screen

**Route:** `app/(tabs)/log.tsx`  
**Role:** Dual-mode form — **Log** (record past) and **Schedule** (set future reminders). Core data-entry screen.

---

## State Architecture

### Top-level state
| State | Type | Purpose |
|-------|------|---------|
| `mode` | `'log' \| 'schedule'` | Toggle between Log and Schedule |
| `activityType` | `ActivityTypeExtended` | Selected activity category |
| `loading` | `boolean` | Submit spinner |
| `success` | `boolean` | Full-screen success component swap |
| `submitError` | `string` | Banner error |

### Time input state (per activity)
Each type using a time range has its own `H/M/period` pairs:
- `sleep` → `sleepStartH/M/P`, `sleepEndH/M/P`
- `nap` → `napStartH/M/P`, `napEndH/M/P`
- `learn` → `learnStartH/M/P`, `learnEndH/M/P`
- `active` → `activeStartH/M/P`, `activeEndH/M/P`
- `screen` → `screenStartH/M/P`, `screenEndH/M/P`
- `meal` → `mealTimeH/M/P` (single time)

### Activity-specific sub-state
| Activity | Sub-state |
|----------|-----------|
| `screen_time` | `device`, `screenCategory` |
| `sleep` | `sleepQuality` |
| `nap` | `napQuality` |
| `meal` | `mealType`, `mealQuality`, `foodGroups[]` |
| `physical_activity` | `physicalType` |
| `education` | `subject` |

### Schedule-only state
`scheduleDate`, `schedHour/Minute/Period`, `minDurationH/M`, `maxDurationH/M`, `schedMealType`, `schedCategory`

---

## Reusable Components

### `SingleTimeInput`
For meal timestamp. `+`/`−` steppers on hour (±1) and minute (±5), AM/PM toggle. Tap digit box focuses `TextInput` for direct typing. `sanitizeHour` clamps 1–12, `sanitizeMinute` pads to 2 digits.

### `TimeRangeInput`
For sleep, nap, screen, active, education. Two labeled `TimeBlock`s with `↓` arrow. Auto-calculates duration:
- Converts both times to 24h
- Handles overnight crossing (`endTotal += 24*60` if `endTotal < startTotal`)
- Displays `= Xh Ym`

### `ChipSelector` / `MultiChipSelector`
Single and multi-select chips. Active gets coral border + background tint. `foodGroups` uses `MultiChipSelector`.

---

## Core Handlers

### `calcDuration`
Converts 12h + AM/PM → 24h minutes, handles overnight, returns `{hours, minutes}`.

### `handleLog`
1. Builds `value` object based on `activityType`
2. `nap` stored as `sleep` in DB (type mapping)
3. Calls `logActivity(selectedChild.id, dbType, value)`
4. Success: `resetForm()` → `setSuccess(true)` → `router.back()` after 1800ms

### `handleSchedule`
1. Computes start ISO timestamp from `scheduleDate` + time
2. Stores `minMins`/`maxMins` duration range; validates `minMins <= maxMins`
3. Calls `scheduleActivity(...)` then `scheduleScheduledActivityNotifications(...)`
4. Success: redirects to History tab (see [[schedule-redirect]])

### `resetForm`
Resets ALL form state to defaults — called after successful submit and on schedule mode activation.

---

## UI Structure

```
ScreenHeader: "Activities" + create-outline icon
  ↓
Error Banner (if submitError)
  ↓
Mode Toggle [Log | Schedule] — pill toggle
  ↓
Activity Type Grid (6 cards: Screen, Sleep, Nap, Meals, Active, Learn)
  ↓
── LOG MODE ──
  Date Navigator (← Today, Dec 25 →) — day picker, resets to today via ↩ pill
  Time Range inputs (sleep, nap, education, physical, screen_time)
  Category / device / quality chips per type
  Notes field (optional)
  Submit → `logActivity(childId, type, value, logDate)`
  ↓
── SCHEDULE MODE ──
  Date Navigator (← Today, Dec 25 →)
  Start Time stepper (H:M + AM/PM)
  Duration Range (min/max H:M) — hidden for meals
  Computed preview card (green)
  Screen category chip / Meal type chip
── LOG MODE ──
  TimeRangeInput
  [Activity-specific chips]
  ↓
Notes (multiline TextInput)
  ↓
Submit Button — disabled if !selectedChild
```

---

## Success State
Full-screen component swap — green checkmark + dynamic message (`"Logged!"` or `"Scheduled!"`) + child name. Auto-navigates back after 1800ms.

---

## Key Design Decisions

1. **`nap` → `sleep` type mapping** — DB stores nap as `sleep` until proper migration exists.
2. **No validation on time ranges in log mode** — `calcDuration` handles overnight crossing but doesn't warn.
3. **Schedule duration is a range** — `minMins`/`maxMins` with reminder at both boundaries.
4. **Log mode has a date picker** — users can log past activities. `logDate` is passed as `recorded_at` to `logActivity()`, defaulting to `new Date()` if not set.
5. **No per-field inline errors** — single `submitError` banner for whole form.
6. **Food groups are multi-select** — presence/absence only, no quantity.
7. **`router.back()` on log success** — goes back to previous tab. Scheduled activities link to [[screen-history]] for viewing after creation.
