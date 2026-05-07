---
id: spa-update-schedule-modal-refactor-2026-04-23
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
  - mobile-dev
source_refs:
  - concepts/smart-parenting-app-tech-stack
  - concepts/react-native-text-input-centering
---

# Smart Parenting App — UpdateScheduleModal Refactor + Range Preview

**Date:** 2026-04-23
**Focus:** Replace End-Time picker with Min/Max duration model; add live calculated range preview; tighten time-input padding
**Files modified:** `app/(tabs)/index.tsx`

---

## Changes Summary

### 1. Duration-Based Scheduling (Replaces End-Time Picker)

**Before:** UpdateScheduleModal used Start Time + End Time. Parent picked absolute start and end times; `max_duration_minutes` was auto-computed from the delta.

**After:** UpdateScheduleModal uses **Start Time + Minimum Duration + Maximum Duration**.

**Why:** Matches the "Log Activity" philosophy — parents think in "allot at least X, at most Y" rather than absolute end times. Also aligns with the new one-off reminder system that needs min/max boundaries.

**Modal sections (non-meal):**
1. **Activity Type** — 6 color-coded chips
2. **Start Time** — CompactTimeBlock: stepper ±, RNTextInput (44×42), AM/PM toggle
3. **Minimum Allotted Duration** — hour/minute inputs with `modalCompactRow` (fixed-width digit columns)
4. **Maximum Allotted Duration** — same pattern as minimum
5. **Category chips** — tailored per activity type:
   - Screen Time: `leisure`, `educational`
   - Physical Activity: `sports`, `playground`, `outdoor`, `other`
   - Education: `reading`, `math`, `science`, `art`, `music`, `other`
   - Meal/Sleep/Nap: no category chips

**Time math:**
- Open: ISO `start_time` → 12h `{h, m, p}` via `to12h()`
- `min_duration_minutes` / `max_duration_minutes` → hour/minute breakdown
- Save: 12h → 24h via `from12h()`, reconstruct ISO on base date
- `planned_end_time` auto-computed from `start_time + max_duration_minutes`

### 2. Live Calculated Range Preview

**New UI element:** Green preview card that updates in real time as parent edits duration fields.

**Display format:**
- `3:00 PM → 3:30 PM – 4:00 PM` (when min ≠ max)
- `3:00 PM → 4:00 PM` (when min = max)

**Helper:** `computeUpdateScheduleRange()` — computes `startDate`, `minEnd`, `maxEnd` from current modal state, formats with `toLocaleTimeString`.

**Styles:**
- `modalRangePreviewCard` — white surface, 1px `#10B981` border, 12px radius, left green accent bar
- `modalRangePreviewTitle` — "Calculated Time Range" in `#059669`
- `modalRangePreviewTime` — bold time string
- `modalRangePreviewSub` — gray helper text explaining the window

### 3. Tightened x:xx Input Padding

**Problem:** The `x : xx` time/duration inputs had too much horizontal spacing because digit columns used wide flex distribution.

**Solution:** Fixed-width digit columns with compact colons.

**New styles:**
- `modalTimeFieldRow` — flex row, items center, gap 4
- `modalCompactRow` — flex row, items center, gap 2
- `modalDigitCol` — fixed 44px width, centered
- `modalTimeColon` — fixed 12px width, centered, 16px font
- `modalTimeInput` — 44×42, `paddingHorizontal: 0`, `paddingVertical: 0`
- `modalPeriodStack` — 32px width, tight vertical AM/PM toggles

**Result:** Time inputs now sit much tighter, e.g. `3:05` instead of `3 : 05`.

### 4. Meal Card Time Label Cleanup

Upcoming meal cards no longer show redundant duration when start and end times are identical (common for meals).

- **Before:** `12:00 PM → 12:00 PM`
- **After:** `12:00 PM`

### 5. Meal Update Clarification

**Meal Type remains in Update Schedule** — it is part of the planning phase.

**Food groups / quality / notes remain in Log Confirm Modal** — they are part of the recording phase.

This separation is intentional:
- **Schedule** = what the parent plans to serve
- **Log** = what the child actually ate

---

## Component Signature Changes

`UpdateScheduleModal` internal state:
```ts
// OLD
const [startH, setStartH] = useState('');
const [startM, setStartM] = useState('');
const [startP, setStartP] = useState<'AM'|'PM'>('AM');
const [endH, setEndH] = useState('');      // REMOVED
const [endM, setEndM] = useState('');      // REMOVED
const [endP, setEndP] = useState<'AM'|'PM'>('AM'); // REMOVED

// NEW
const [minDurationH, setMinDurationH] = useState('');
const [minDurationM, setMinDurationM] = useState('');
const [maxDurationH, setMaxDurationH] = useState('');
const [maxDurationM, setMaxDurationM] = useState('');
```

---

## HCI Compliance

- No `Alert.alert()` anywhere ✅
- Loading state on Save Changes button ✅
- Inline confirmation for Cancel (hard-delete) ✅
- Real-time validation feedback on all inputs ✅
- Empty state with CTA on Dashboard ✅

---

## Related

- [[concepts/smart-parenting-app-tech-stack]] — updated with new UpdateScheduleModal section
- [[concepts/react-native-text-input-centering]] — the View wrapper pattern used for all compact inputs in this modal
