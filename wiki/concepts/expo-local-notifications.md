---
id: expo-local-notifications-001
type: concept
created: 2026-04-18
updated: 2026-05-05
last_verified: 2026-04-25
review_after: 2026-07-22
stale_after: 2026-10-22
confidence: high
source_refs:
  - raw/articles/smart-parenting-app-codebase-2026-04-18
  - lib/notifications.ts
  - sources/operational/2026-04-23-spa-schedule-reminder-session
  - sources/operational/2026-04-25-spa-ai-insights-notification-ux-session
  - sources/operational/2026-05-05-spa-notification-orphan-fixes
status: active
tags:
  - expo
  - expo-notifications
  - mobile-dev
  - smart-parenting-app
related:
  - concepts/smart-parenting-app-tech-stack
  - concepts/hci-design-principles-mobile
---

# Expo Local Notifications — Child Routine Reminders

Smart Parenting App uses Expo's local notification system to send daily reminders based on each child's configured routine schedule.

## Overview

All notifications are **local** (no server required), **daily or weekly triggers** (OS handles scheduling), and **persist across app restarts**. Triggered from `lib/notifications.ts` (385L as of 2026-04-22).

Two trigger types:
- **Daily** (`SchedulableTriggerInputTypes.DAILY`) — routine reminders
- **Weekly** (`SchedulableTriggerInputTypes.WEEKLY`) — growth check reminder

## Permission Flow

```
requestNotificationPermission()
  → Device.isDevice check (rejects simulators)
  → Notifications.getPermissionsAsync()
  → Notifications.requestPermissionsAsync() if not granted
  → Returns boolean
```

iOS requires explicit user permission; Android auto-grants on first run.

## Notification Trigger Architecture

Each notification uses Expo's `SchedulableTriggerInputTypes.DAILY`:

```typescript
await Notifications.scheduleNotificationAsync({
  content: { title, body, sound: 'default', data: { childId, type } },
  trigger: {
    type: Notifications.SchedulableTriggerInputTypes.DAILY,
    hour,
    minute,
  },
});
```

Daily triggers fire at the specified time every day until cancelled. The OS battery-optimized scheduler handles delivery timing.

## Scheduled Notification Types

### Daily Routine Notifications

| ID prefix | When | Offset | Title | Body |
|---|---|---|---|---|
| `bedtime-{childId}` | bedtime - 30min | -30 | Bedtime for {n} 🌙 | Almost time to wind down |
| `wake_up-{childId}` | wake_up_time | 0 | Good morning {n} ☀️ | How did they sleep? |
| `breakfast-{childId}` | breakfast_time | 0 | Breakfast for {n} 🍳 | Don't forget to log it |
| `lunch-{childId}` | lunch_time | 0 | Lunch for {n} 🍚 | Log what they ate |
| `snack-{childId}` | snack_time | 0 | Snack for {n} 🍎 | Log it after |
| `dinner-{childId}` | dinner_time | 0 | Dinner for {n} 🍲 | Log what they had |
| `nap-{childId}` | nap_time | 0 | Nap time for {n} 😴 | Sweet dreams |
| `activity-{childId}` | activity_time | 0 | Activity for {n} 🏃 | Stay active |
| `learn-{childId}` | learn_time | 0 | Learning for {n} 📚 | Happy studying |

### Scheduled Activity Notifications (One-Off)

As of **2026-04-23**, the app also schedules **one-off notifications** for rows in `scheduled_activities`.

| ID prefix | When | Trigger Type | Purpose |
|---|---|---|---|
| `scheduled-min-{scheduleId}` | `start_time + min_duration_minutes - 5min` | DATE | Warn parent the minimum duration window is almost reached |
| `scheduled-max-{scheduleId}` | `start_time + max_duration_minutes - 5min` | DATE | Warn parent the maximum duration window is almost reached |

**Rules:**
- Only `pending` schedules are considered
- Past triggers are skipped automatically
- If min and max resolve to the same time, only the **max** reminder is scheduled to avoid duplicates
- Notification payload includes `{ childId, type, scheduleId, reminderStage }`

### Weekly Growth Notification

| ID prefix | When | Trigger Type | Title | Body |
|---|---|---|---|---|
| `weekly-growth-{childId}` | Monday 9:00 AM | WEEKLY (weekday: 1) | 📏 Weekly Growth Check for {n}! | Time to record {n}'s weight and height for accurate BMI tracking. |

**Toggle key:** `weekly_growth` — controlled via per-child notification toggles in `app/settings/child/[id].tsx`.

## Key Functions

### `scheduleChildNotifications(child, notifToggles?)`
1. Cancels existing notifications for that child first (idempotent)
2. Iterates all routine times from child record
3. Calls `addNotif()` for each non-null time (skipped if `notifToggles[key]` is `false`)
4. If `notifToggles['weekly_growth']` is `true`, calls `scheduleWeeklyGrowthReminder(child, true)`
5. Fetches pending `scheduled_activities` rows via `getScheduledActivities(child.id, 'pending')`
6. Schedules one-off `scheduled-min-*` / `scheduled-max-*` reminders for each pending schedule
7. Tracks scheduled notifications in `scheduledNotifications[]` array

**`notifToggles` parameter** — `Record<string, boolean>` that controls per-routine notification toggles. All routines default to `true` if not provided.

### `cancelChildNotifications(childId)`
- Queries `Notifications.getAllScheduledNotificationsAsync()` and cancels every scheduled notification whose `content.data.childId` matches
- Covers routine reminders, weekly growth reminder, and one-off scheduled-activity reminders
- Removes matching entries from `scheduledNotifications[]`

### `scheduleWeeklyGrowthReminder(child, enabled)`
- ID: `weekly-growth-{childId}`
- Schedules weekly notification every **Monday at 9:00 AM**
- Uses `SchedulableTriggerInputTypes.WEEKLY` with `weekday: 1`
- Title: `📏 Weekly Growth Check for {name}!`
- Body: `Time to record {name}'s weight and height for accurate BMI tracking.`
- If `enabled` is `false`, cancels instead of scheduling

### `cancelWeeklyGrowthReminder(childId)`
- Finds and cancels the `weekly-growth-{childId}` notification
- Removes from `scheduledNotifications[]`

### `cancelAllNotifications()`
- Calls `Notifications.cancelAllScheduledNotificationsAsync()`
- Resets `scheduledNotifications[]` to empty

### `hasRoutineSet(child)`
- Checks if ANY routine time field is non-null
- Used to determine if notification scheduling is worthwhile

## Time Parsing

Handles both `HH:MM` and `HH:MM:SS` formats via `parseTime()`:
```typescript
const parts = timeStr.split(':');
// returns { hour: number, minute: number }
```

## Offset Logic

Bedtime reminder fires 30 minutes before scheduled bedtime using `offsetTime()`:
```typescript
offsetTime(hour, minute, offsetMinutes)
// Handles overnight wrap-around: 23:30 + 30min → 00:00
```

## NotificationHandler (Foreground)

```typescript
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: false,
  }),
});
```

Notifications show as alerts even when app is in foreground.

## Data Field

Each notification's `data` field carries `{ notificationId, childId, type }` — enables deep-linking back to the relevant screen/action when tapped.
## Integration Points
- `app/child/wizard.tsx` calls `scheduleChildNotifications()` after saving routine
- `app/settings/child/[id].tsx` calls `scheduleChildNotifications()` on save with `notifToggles` to apply per-routine notification settings
- `app/(tabs)/profile.tsx` global notifications toggle: calls `cancelChildNotifications()` for all children when disabled, `scheduleChildNotifications()` for all when re-enabled
- `app/(tabs)/log.tsx` calls `scheduleScheduledActivityNotifications()` immediately after `scheduleActivity()` succeeds
- `app/(tabs)/index.tsx` cancels or reschedules schedule-specific notifications when upcoming cards are logged, updated, or cancelled
- `initNotifications()` called once in root layout for permission setup

## Limitations
- Notifications fire even if the app hasn't been opened that day
- No notification history or read/unread tracking
- No dedicated per-schedule reminder toggle yet — schedule-based reminders follow the app’s overall notification enable/disable flow
- **Requires DB migration** — `notifications` column must be added to `children` table via `database/migration_child_notifications.sql`
- Weekly growth notification uses weekday:1 (Monday 9AM) — fixed day/time, not configurable
