---
title: Dashboard Screen
created: 2026-04-25
updated: 2026-04-25
type: concept
tags: [screen, dashboard, ui-ux, state-management]
sources: [raw/technical-reference.md]
---

# Dashboard Screen

**Route:** `app/(tabs)/index.tsx`  
**Role:** Home tab — greeting, today's stats, upcoming schedules, recent activities, AI banner.

---

## Data Flow

```
User opens app
    ↓
RootLayout checks auth → redirects to (tabs)/index.tsx
    ↓
useFocusEffect fires → loadDashboardData()
    ↓
Parallel Supabase queries:
  getTodayActivities(selectedChild.id)
  getScheduledActivities(selectedChild.id)
    ↓
Filter: scheduled → upcoming (start_time >= today 00:00)
    ↓
calculateStats(todayActivities) → aggregates screen/sleep/meals/education
    ↓
Render: greeting + date + child picker + stats grid + upcoming list + recent activities + AI banner
```

---

## Screen Sections (Top → Bottom)

### 1. Greeting Header
- `getGreeting()` — "Good morning/afternoon/evening"
- Parent's first name from `user.user_metadata.name`
- Current date: "Saturday, April 25"

### 2. Children Horizontal Selector
- Horizontal ScrollView of child chips
- Active chip highlighted with coral border
- `+ Add` link → `/child/wizard`
- **Empty state:** Dashed banner → "Add your first child"
- On tap: `useApp.getState().selectChild(child)` → triggers reload

### 3. Quick Log CTA
- Coral button: "Log an Activity"
- Tap → navigates to `/log` tab

### 4. Today's Overview Stats Grid
- 2×2 grid of `StatCard` components
- **Screen Time:** total mins today as `Xh Ym`
- **Sleep:** last night's sleep duration (most recent `sleep` log)
- **Meals:** `N/3` format
- **Education:** total education minutes today
- Activity colors: screen=#FF7F60, sleep=#10B981, meals=#F59E0B, edu=#8B5CF6

### 5. Upcoming Scheduled Activities
- Pulled from `scheduled_activities`, filtered to `start_time >= today 00:00`
- Sorted ascending by `start_time`, max 3 shown
- **UpcomingItem:** icon + color badge + date label + time range + status badge
- Action buttons: Log (when `now >= start_time`), Update, Cancel
- **Empty state:** "No upcoming activities" + CTA to schedule

### 6. Recent Activity
- `todayActivities` — today's logs
- `RecentItem`: icon + colored dot + human-readable label + time
- Max 5 shown + "+N more activities"
- **Empty state:** "No activities yet"

### 7. AI Insights Banner
- Bottom CTA card: "AI Insights" with sparkles icon
- Tap → navigates to `/ai` tab
- See [[ai-insights-display]] for the recommendations UI.

---

## State Management

| State | Where | How it changes |
|-------|-------|----------------|
| `todayActivities` | Local `useState` | Refetched on tab focus, child switch, pull-to-refresh, mutation |
| `scheduledActivities` | Local `useState` | Same triggers |
| `selectedChild` | Zustand `useApp` | Persisted to AsyncStorage. Changed by child picker. |
| `loading` / `refreshing` / `error` | Local `useState` | Standard async lifecycle |

---

## Key Modals

**UpdateScheduleModal**
- Slide-up sheet: start time steppers, duration range, category/meal selectors
- Save → reschedules notifications → reloads

**LogConfirmModal**
- Pre-fills from scheduled activity
- Save → logs activity + cancels notifications + marks schedule `completed`
- `planned_end_time` stored as `end_time` in activity `value`

---

## Reload Triggers

1. `useFocusEffect` — tab gains focus
2. `selectedChild?.id` useEffect — child switched
3. Pull-to-refresh — manual
4. After any mutation — `await loadDashboardData()`

Mutations originate from [[screen-activities]] (log/schedule) and are reflected in the upcoming list.
