## Dashboard — `app/(tabs)/index.tsx` Walkthrough

### Data Flow

```
User opens app
    ↓
_RootLayout checks auth → redirects to (tabs)/index.tsx
    ↓
useFocusEffect fires → loadDashboardData()
    ↓
Parallel Supabase queries:
  getTodayActivities(selectedChild.id)  ← today's logs for selected child
  getScheduledActivities(selectedChild.id)  ← ALL scheduled (pending/completed/skipped)
    ↓
Filter: scheduled → upcoming (start_time >= today 00:00)
    ↓
calculateStats(todayActivities) → aggregates screen/sleep/meals/education
    ↓
Render: greeting + date + child picker + stats grid + upcoming list + recent activities + AI banner
```

---

### Screen Sections (Top → Bottom)

**1. Greeting Header**
- `getGreeting()` → "Good morning/afternoon/evening"
- Parent's first name from `user.user_metadata.name`
- Current date formatted: "Saturday, April 25"

**2. Children Horizontal Selector**
- Horizontal ScrollView of child chips
- Each chip: avatar initial + name + age in years
- Active chip highlighted with coral border
- `+ Add` link → `/child/wizard`
- **Empty state:** Dashed banner → "Add your first child"
- On tap child: `useApp.getState().selectChild(child)` → triggers `useEffect` → `loadDashboardData(child.id)`

**3. Quick Log CTA**
- Coral button: "Log an Activity"
- Subtitle: "For [childName]" or "Screen time, sleep, meals, education"
- Tap → navigates to `/log` tab

**4. Today's Overview Stats Grid**
- 2×2 grid of `StatCard` components
- Each card: icon + label + value + subtitle
- **Screen Time:** total mins logged today as `Xh Ym` or `Xm`
- **Sleep:** last night's sleep duration (looks at most recent `sleep` type log)
- **Meals:** `N/3` format (meals tracked today out of 3 typical meals)
- **Education:** total education minutes today
- Stats computed client-side by `calculateStats(todayActivities)`
- Cards show activity colors: screen=#FF7F60, sleep=#10B981, meals=#F59E0B, edu=#8B5CF6

**5. Upcoming Scheduled Activities**
- Pulled from `scheduled_activities` table, filtered to `start_time >= today 00:00`
- Sorted ascending by `start_time`
- Max 3 shown + "+N more scheduled" if overflow
- **UpcomingItem component** shows:
  - Activity type icon + color badge
  - Date label ("Today" or "Sat, Apr 25")
  - Time range ("7:00 AM → 8:00 AM · up to 1h 30m")
  - Category / meal_type / food_groups if present
  - **⏳ Upcoming** badge if `now < start_time` (hasn't started yet)
  - **Log / Update / Cancel** action buttons
    - Log only appears when `now >= start_time` (can only log past/current activities)
    - Update → opens `UpdateScheduleModal`
    - Cancel → inline confirmation ("Delete this schedule permanently?")
- **Empty state:** "No upcoming activities" + CTA to schedule

**6. Recent Activity**
- `todayActivities` — today's logs from `activities` table
- `RecentItem` component: activity type icon + colored dot + label (human-readable via `getActivityLabel()`) + time
- Max 5 shown + "+N more activities"
- **Empty state:** "No activities yet" / "Add a child profile first" with icon

**7. AI Insights Banner**
- Bottom CTA card: "AI Insights" with sparkles icon
- Subtitle contextual: "Get personalized recommendations for [childName]"
- Tap → navigates to `/ai` tab

---

### State Management

| State | Where it lives | How it changes |
|-------|---------------|----------------|
| `todayActivities` | Local `useState` | Refetched on tab focus, child switch, pull-to-refresh, any log/cancel/update action |
| `scheduledActivities` | Local `useState` | Same triggers — refetched fully each time |
| `selectedChild` | Zustand `useApp` store | Persisted to AsyncStorage. Restored on app open. Changed by child picker tap. |
| `loading` | Local `useState` | True during `loadDashboardData()` |
| `refreshing` | Local `useState` | True during pull-to-refresh operation |
| `error` | Local `useState` | Set on catch, cleared on retry |

---

### Loading / Error / Empty States

- **Loading:** Full-screen spinner (ActivityIndicator coral) during initial data fetch
- **Error:** Top banner with message + close button. Pull-to-refresh recovers.
- **Pull-to-refresh:** `RefreshControl` with coral tint — calls `loadDashboardData()` again
- **Empty child:** Shows dashed "Add your first child" banner — both child picker AND upcoming/recent sections adapt
- **Empty activities:** "No activities yet" with CTA to log

---

### Key Modals

**UpdateScheduleModal**
- Slide-up sheet from bottom
- Fields: Start time (hour/minute/AM-PM steppers), Duration allotment (min/max hours+minutes)
- Live "Calculated Time Range" preview card
- Category/meal_type/food_groups selectors
- Save → `handleUpdateSchedule(id, updates)` → reschedules notifications → reloads

**LogConfirmModal**
- Pre-fills from a scheduled activity (`setLogModalSchedule(scheduled)`)
- Shows duration range, category chips, food groups, notes
- Save → `handleLogScheduleConfirm(scheduled, value)` → logs activity + cancels notifications + marks schedule `completed`
- The logged activity value includes `end_time` (from `scheduled.planned_end_time`) so the history shows when the activity ended

---

### Reload Triggers

1. **`useFocusEffect`** — fires when tab gains focus (handles tab switch)
2. **`selectedChild?.id` useEffect** — fires when user picks a different child
3. **Pull-to-refresh** — manual
4. **After any mutation** (cancel, update, log) — `await loadDashboardData()`

---

### Likely Panelist Questions

**"How does the dashboard know which child's data to show?"**
The `selectedChild` is stored in Zustand + persisted to AsyncStorage. On app open, it's restored from storage and `useEffect` triggers `loadDashboardData(selectedChild.id)`. All queries filter by `child_id = selectedChild.id`.

**"What happens when there's no child selected?"**
Empty state shown for child picker. Stats grid, upcoming, and recent all show contextual empty states ("Add a child profile first"). Quick Log shows generic subtitle.

**"How is today's sleep determined?"**
The `calculateStats()` function iterates over `todayActivities` and sums all `sleep` type logs. It aggregates `hours + minutes` from the JSONB `value` field. The "last night" subtitle is misleading — it shows total sleep logged today, not specifically last night.

**"Why do scheduled activities show ALL statuses?"**
The query fetches everything then filters client-side to `start_time >= today 00:00`. The `UpcomingItem` shows status implicitly via the `⏳ Upcoming` badge (not started yet). Completed/skipped activities from today that already passed would also appear if they were scheduled.

**"How does the Log action work on a scheduled activity?"**
Tapping Log pre-opens `LogConfirmModal` with the scheduled activity's data pre-filled. Saving calls `logActivity()` to create a real activity log, `cancelScheduledActivityNotifications()` to remove the now-redundant notification, then `updateScheduledActivityStatus(id, 'completed')` to mark the schedule as done. The `completed` status causes it to disappear from the dashboard's upcoming list. The `planned_end_time` is stored as `end_time` in the logged activity's `value` field, so the History tab shows when the activity ended.