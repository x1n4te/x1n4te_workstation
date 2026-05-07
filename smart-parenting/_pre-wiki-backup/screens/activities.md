## Overview

The Activities tab is a dual-mode form — **Log** (record past activities) and **Schedule** (set future reminders) — both tied to a selected child. It's the core data-entry screen of the app.

---

## State Architecture

### Top-level state (lines 458–567)
| State | Type | Purpose |
|-------|------|---------|
| `mode` | `'log' \| 'schedule'` | Toggle between Log and Schedule |
| `activityType` | `ActivityTypeExtended` | Selected activity category |
| `loading` | `boolean` | Submit spinner |
| `success` | `boolean` | Full-screen success component swap |
| `submitError` | `string` | Banner error |
| `selectedChild`, `children`, `selectChild`, `loadChildren` | from `useApp()` | Child context |

### Time input state (per activity, lines 498–554)
Each activity type that uses a time range has its own `H/M/period` pairs:
- `sleep` → `sleepStartH/M/P`, `sleepEndH/M/P`
- `nap` → `napStartH/M/P`, `napEndH/M/P`
- `learn` (education) → `learnStartH/M/P`, `learnEndH/M/P`
- `active` (physical) → `activeStartH/M/P`, `activeEndH/M/P`
- `screen` → `screenStartH/M/P`, `screenEndH/M/P`
- `meal` → `mealTimeH/M/P` (single time, not range)

### Activity-specific sub-state (lines 534–554)
| Activity | Sub-state |
|----------|-----------|
| `screen_time` | `device`, `screenCategory` |
| `sleep` | `sleepQuality` |
| `nap` | `napQuality` |
| `meal` | `mealType`, `mealQuality`, `foodGroups[]`, meal time |
| `physical_activity` | `physicalType` |
| `education` | `subject` |

### Schedule-only state (lines 559–569)
`scheduleDate`, `schedHour/Minute/Period`, `minDurationH/M`, `maxDurationH/M`, `schedMealType`, `schedCategory`

---

## Reusable Components

### `SingleTimeInput` (lines 102–196)
For meal timestamp. Has `+`/`−` steppers on hour (±1) and minute (±5), and AM/PM toggle. Tap on the digit box focuses the `TextInput` for direct typing. `sanitizeHour` clamps 1–12, `sanitizeMinute` pads to 2 digits.

### `TimeRangeInput` (lines 198–376)
For sleep, nap, screen, active, education. Renders two labeled `TimeBlock`s (Start/End) vertically with a `↓` arrow between. **Auto-calculates duration** in real-time:
- Converts both times to 24h
- Handles overnight crossing (`endTotal += 24*60` if `endTotal < startTotal`)
- Displays `= Xh Ym` below

### `ChipSelector` (lines 378–421)
Single-select chips. Pass `showIcon` or `showEmoji` for icons/emojis. Active chip gets coral border + background tint.

### `MultiChipSelector` (lines 423–454)
Multi-select chips with checkmark overlay on active items. `foodGroups` uses this.

---

## Core Handlers

### `calcDuration` (lines 605–617)
```ts
// Converts 12h + AM/PM → 24h minutes, handles overnight, returns {hours, minutes}
```
Used in `handleLog` to build the `value` payload.

### `handleLog` (lines 735–808)
1. Builds `value` object based on `activityType` — includes hours/minutes from `calcDuration`, plus type-specific fields
2. `nap` is stored as `sleep` in DB (line 789 — type mapping)
3. Calls `logActivity(selectedChild.id, dbType, value)`
4. On success: `resetForm()` → `setSuccess(true)` → `router.back()` after 1800ms

### `handleSchedule` (lines 680–733)
1. Computes start ISO timestamp from `scheduleDate` + `schedHour/Minute/Period`
2. For meals: only stores `mealType` (single reminder time)
3. For others: stores `minMins`/`maxMins` duration range; validates `minMins <= maxMins`
4. For screen_time: includes `schedCategory`
5. Calls `scheduleActivity(...)` then `scheduleScheduledActivityNotifications(...)` for push reminders
6. Success flow same as `handleLog`

### `resetForm` (lines 573–602)
Resets ALL form state to defaults — called after both successful submit and on schedule mode activation.

### `refreshChildren` + `onRefresh` + `useFocusEffect` (lines 468–495)
Pull-to-refresh reloads child list. `useFocusEffect` re-fetches on every tab focus (with async safety via `.catch(())`).

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
── SCHEDULE MODE ──
  Date Navigator (← Today, Dec 25 →)
  Start Time stepper (H:M + AM/PM)
  Duration Range (min/max H:M) — hidden for meals
  Computed preview card (green, shows start → end range)
  Screen category chip (if screen_time)
  Meal type chip (if meal) + hint text
── LOG MODE ──
  TimeRangeInput (for range-based: sleep/nap/screen/active/learn)
  [Activity-specific chips: device/category, quality, food groups, subject, etc.]
  ↓
Notes (multiline TextInput)
  ↓
Submit Button [Log/Schedule X] — disabled if !selectedChild
No-child hint → navigates to wizard
```

---

## Success State (lines 811–825)
Full-screen component swap — green checkmark + dynamic message (`"Logged!"` or `"Scheduled!"`) + child name. Auto-navigates back after 1800ms.

---

## Key Design Decisions

1. **`nap` → `sleep` type mapping**: Nap is semantically a `sleep` type in the DB until a proper nap migration exists (line 789)
2. **No validation on time ranges in log mode**: `calcDuration` handles overnight crossing but doesn't warn if start > end — user can log any range
3. **Schedule duration is a range, not fixed**: Stores `minMins`/`maxMins` — the reminder fires at `startTime` and tracks whether activity happened within the window
4. **No per-field inline errors**: Single `submitError` banner for the whole form
5. **Food groups are multi-select**: No quantity — just presence/absence per group
6. **`router.back()` on success**: Goes back to previous tab, not a specific route