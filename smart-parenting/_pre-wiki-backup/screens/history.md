## Overview

The History tab is a **read-only activity browser** — it shows logged activities from the selected child, organized by date with a calendar picker, filter chips, and an expandable stats module with bar/pie charts.

---

## State Architecture

| State | Type | Purpose |
|-------|------|---------|
| `viewYear`, `viewMonth` | `number` | Calendar navigation |
| `selectedDate` | `Date` | Currently viewed day |
| `monthActivities` | `Activity[]` | All activities for child (loaded fresh, filtered client-side) |
| `loading` | `boolean` | Initial load spinner |
| `refreshing` | `boolean` | Pull-to-refresh spinner |
| `error` | `string` | Error message |
| `activeFilter` | `string` | `'all'` or specific activity type |
| `statsExpanded` | `boolean` | Collapsible stats module |
| `statsPeriod` | `'weekly' \| 'monthly'` | Stats granularity |

---

## Data Flow

### Load (lines 239–263)
```
useFocusEffect → loadActivities()
  → getActivities(selectedChild.id)  [fetches ALL activities for child]
  → setMonthActivities(data)
```
**Key design:** All activities are fetched at once, then filtered **client-side** by `selectedDate` and `activeFilter`. No per-day API calls.

### Filtering (lines 275–291)
- **`selectedDayActivities`** — `monthActivities` filtered by `selectedDate` (ISO date string prefix match) + `activeFilter`. Sorted newest-first.
- **`filteredMonthActivities`** — `monthActivities` filtered by `activeFilter` only. Used for stats computation (weekly/monthly charts).

### Calendar dots (lines 266–272)
`activityDateKeys` is a `Set<string>` of ISO date strings (`'2026-04-25'`) derived from all loaded activities. Passed into `buildCalendarGrid`-derived `calendarDays` to show activity indicator dots.

---

## Calendar System

### `buildCalendarGrid` (lines 162–213)
Builds a **fixed 42-cell grid** (6 rows × 7 columns):
1. **Prev month padding** — fills from Sunday of current month backward
2. **Current month** — all days of the viewed month
3. **Next month padding** — fills remaining cells to complete 42

**Note:** Week starts on **Monday** (`getWeekStart` rolls Sunday back 6 days). Sunday column gets red text styling.

### `getWeekStart` (lines 143–151)
```
day = getDay()  // 0=Sunday
offset = day === 0 ? 6 : day - 1  // Monday=0, Tuesday=1, ..., Sunday=6
setDate(getDate() - offset)         // roll back to Monday
```

### Calendar navigation (lines 442–465)
- `goToPrevMonth` / `goToNextMonth` — month arithmetic with year rollover
- `goToToday` — resets year, month, AND selected date to now

---

## Filter System

### `FILTER_OPTIONS` (lines 39–42)
```ts
['all', ...ACTIVITY_TYPES.map(t => ({ key: t.key, label: t.label }))]
```
7 options: All, Screen, Sleep, Nap, Meals, Active, Learn.

### `visibleChartTypes` (lines 293–298)
Determines which bar charts render:
- `'all'` → all 5 time-based types (screen, sleep, nap, education, physical)
- Specific type → only that type's chart
- `'meal'` → no bar chart (only pie)

---

## Stats Computation

### `weeklyStats` (lines 330–381)
1. Compute the **Mon–Sun week** containing `selectedDate`
2. Build 7 labels (weekday abbreviations)
3. For each of the 5 `TIME_BASED_TYPES`, produce a dataset of 7 values (hours/day, converted from minutes ÷ 60)
4. **Pie chart**: count all food groups from meals in that week, map to `foodCounts`

### `monthlyStats` (lines 383–439)
1. Build ~7-day chunks covering the full month (e.g., `1–7`, `8–14`, ...)
2. For each chunk, sum hours across all days in that chunk
3. Same pie chart logic for meals in the viewed month

### `hexToRgba` (lines 129–134)
Converts hex to `rgba(r, g, b, opacity)` for chart gradient compatibility with `react-native-chart-kit`.

---

## Key Rendering Paths

```
FlatList data={selectedDayActivities}
  ListHeaderComponent:
    renderCalendar()      ← always shown
    renderFilterBar()     ← always shown
    daySectionHeader      ← only if activities exist for day
  ListEmptyComponent:
    renderEmpty()         ← "No activities this day — tap Log to record"
  ListFooterComponent:
    renderStatsSection()  ← always at bottom
```

### `renderStatsSection` (lines 648–759)
- **Collapsed**: just header with chevron
- **Expanded**: weekly/monthly toggle, then:
  - Empty state if no data
  - **Per-type bar charts** (`BarChart`) — one per `visibleChartTypes`
  - **Food groups pie chart** (`PieChart`) — only if `hasMeals`

---

## Activity Card (lines 586–607)
Each card shows:
- Colored icon (from `getTypeConfig`)
- Activity description via `getActivityLabel(type, value)`
- Formatted time (`formatTime` — e.g., `3:45 PM`)

### `getActivityLabel` (lines 86–111)
Human-readable labels:
- `screen_time` → `"Screen time (leisure) — 1h 30m on phone"`
- `sleep` → `"Sleep — 9h 0m (good)"`
- `meal` → `"Breakfast @ 7:30 AM — good · fruits, protein"`
- `physical_activity` → `"Physical — 1h 0m (swimming)"`
- `education` → `"Learning — 45m (reading)"`

---

## Screen States

| State | What renders |
|-------|-------------|
| `!selectedChild` | `renderEmpty()` (no child hint) |
| `loading` | `renderLoading()` spinner |
| `error` | `renderError()` with retry button |
| No activities for day | `renderEmpty()` with "tap Log tab" hint |
| Activities exist | FlatList with cards + stats at bottom |

---

## Key Design Decisions

1. **Client-side month filtering**: All activities for the child are fetched once and filtered in-memory. This avoids N API calls for N days but means the full month's data must fit in memory.
2. **No activity deletion/edit**: History is read-only — no edit or delete affordances exist.
3. **Week starts Monday**: ISO week convention, not Sunday.
4. **Overnight handling in calendar**: Calendar grid always 42 cells regardless of month — previous/next month padding handles the visual overflow.
5. **Stats at bottom**: Stats section is always rendered (just collapsed), so the scroll depth is predictable.
6. **Food groups pie only**: Nutrition data (food groups) is shown as a pie, not as duration bars, since meals don't have a duration comparable to activities.
7. **`fromZero` on BarChart**: Y-axis always starts at 0 — no misleading truncated bars.