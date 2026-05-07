---
title: History Screen
created: 2026-04-25
updated: 2026-04-25
type: concept
tags: [screen, history, ui-ux, component]
sources: [raw/technical-reference.md]
---

# History Screen

**Route:** `app/(tabs)/history.tsx`  
**Role:** Read-only activity browser — calendar picker, filter chips, expandable stats with bar/pie charts.

---

## State Architecture

| State | Type | Purpose |
|-------|------|---------|
| `viewYear`, `viewMonth` | `number` | Calendar navigation |
| `selectedDate` | `Date` | Currently viewed day |
| `monthActivities` | `Activity[]` | All activities for child (fetched fresh, filtered client-side) |
| `loading` | `boolean` | Initial load spinner |
| `refreshing` | `boolean` | Pull-to-refresh spinner |
| `error` | `string` | Error message |
| `activeFilter` | `string` | `'all'` or specific activity type |
| `statsExpanded` | `boolean` | Collapsible stats module |
| `statsPeriod` | `'weekly' \| 'monthly'` | Stats granularity |

---

## Data Flow

### Load
```
useFocusEffect → loadActivities()
  → getActivities(selectedChild.id)  [ALL activities for child]
  → setMonthActivities(data)
```

**Key design:** All activities fetched at once, then filtered **client-side** by `selectedDate` and `activeFilter`. No per-day API calls. See [[database-schema]] for the underlying `activities` table structure.

### Filtering
- **`selectedDayActivities`** — filtered by `selectedDate` + `activeFilter`, sorted newest-first.
- **`filteredMonthActivities`** — filtered by `activeFilter` only. Used for stats.

### Calendar dots
`activityDateKeys` is a `Set<string>` of ISO date strings derived from all loaded activities. Passed into `buildCalendarGrid`-derived `calendarDays` to show activity indicator dots.

---

## Calendar System

### `buildCalendarGrid`
Fixed **42-cell grid** (6 rows × 7 columns):
1. Prev month padding — fills from Sunday of current month backward
2. Current month — all days
3. Next month padding — fills remaining cells

**Week starts on Monday** (`getWeekStart` rolls Sunday back 6 days). Sunday column gets red text styling.

### `getWeekStart`
```
day = getDay()  // 0=Sunday
offset = day === 0 ? 6 : day - 1  // Monday=0, ..., Sunday=6
setDate(getDate() - offset)
```

---

## Filter System

`FILTER_OPTIONS`: `['all', ...ACTIVITY_TYPES.map(...)]` — 7 options: All, Screen, Sleep, Nap, Meals, Active, Learn.

`visibleChartTypes`: determines which bar charts render:
- `'all'` → all 5 time-based types
- Specific type → only that type
- `'meal'` → no bar chart (only pie)

---

## Stats Computation

### `weeklyStats`
1. Compute Mon–Sun week containing `selectedDate`
2. Build 7 weekday labels
3. For each of 5 `TIME_BASED_TYPES`, produce 7 values (hours/day, minutes ÷ 60)
4. Pie chart: count all food groups from meals in that week

### `monthlyStats`
1. Build ~7-day chunks covering full month (`1–7`, `8–14`, ...)
2. Sum hours across days in each chunk
3. Same pie chart logic for meals in viewed month

---

## Rendering Paths

```
FlatList data={selectedDayActivities}
  ListHeaderComponent:
    renderCalendar()      ← always shown
    renderFilterBar()     ← always shown
    daySectionHeader      ← only if activities exist for day
  ListEmptyComponent:
    renderEmpty()         ← "No activities this day"
  ListFooterComponent:
    renderStatsSection()  ← always at bottom
```

### `renderStatsSection`
- **Collapsed:** header with chevron
- **Expanded:** weekly/monthly toggle, then per-type bar charts + food groups pie chart

---

## Activity Card

Each card shows:
- Colored icon (from `getTypeConfig`)
- Human-readable label via `getActivityLabel(type, value)`
- Formatted time (`formatTime` — e.g., `3:45 PM`)

### `getActivityLabel` examples
- `screen_time` → `"Screen time (leisure) — 1h 30m on phone"`
- `sleep` → `"Sleep — 9h 0m (good)"`
- `meal` → `"Breakfast @ 7:30 AM — good · fruits, protein"`

---

## Key Design Decisions

1. **Client-side month filtering** — all activities fetched once, filtered in-memory.
2. **No activity deletion/edit** — History is read-only. Scheduled activities that have been logged are handled via [[schedule-redirect]].
3. **Week starts Monday** — ISO week convention.
4. **Stats at bottom** — always rendered (collapsed), predictable scroll depth.
5. **Food groups pie only** — nutrition shown as pie, not duration bars.
6. **`fromZero` on BarChart** — Y-axis starts at 0, no misleading truncation.
