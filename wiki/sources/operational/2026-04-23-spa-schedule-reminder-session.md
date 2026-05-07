---
id: 2026-04-23-spa-schedule-reminder-session
type: source
created: 2026-04-23
updated: 2026-04-23
last_verified: 2026-04-23
confidence: high
source_type: operational
project: smart-parenting-app
tags:
  - smart-parenting-app
  - expo-notifications
  - scheduled-activities
  - react-native
  - operational
---

# Smart Parenting App — Scheduled Activity Reminder Session

## Summary

Implemented one-off local notifications for `scheduled_activities` so parents receive reminders **5 minutes before the minimum duration** and **5 minutes before the maximum duration** of a scheduled activity.

## Files Modified

- `lib/notifications.ts`
- `app/(tabs)/log.tsx`
- `app/(tabs)/index.tsx`

## Key Changes

### `lib/notifications.ts`
- Added `scheduleScheduledActivityNotifications(activity, childName)`
- Added `cancelScheduledActivityNotifications(scheduleId)`
- Added one-time `Date` trigger scheduling via Expo Notifications
- Added child-level notification cancellation using `Notifications.getAllScheduledNotificationsAsync()` so cancellation works even after app restarts
- Extended `scheduleChildNotifications()` to also resync pending scheduled-activity reminders after routine reminders are rebuilt

### `app/(tabs)/log.tsx`
- After `scheduleActivity(...)` returns the inserted row, immediately schedules one-off reminders for that schedule

### `app/(tabs)/index.tsx`
- On schedule update: reschedules reminders using the updated `ScheduledActivity` row
- On schedule cancel: cancels schedule-specific reminders before deleting the DB row
- On log-from-upcoming confirm: cancels schedule-specific reminders to avoid stale follow-up reminders after the activity is manually logged

## Reminder Logic

For each pending `ScheduledActivity`:
- `min_duration_minutes` → notification at `start_time + min_duration - 5 minutes`
- `max_duration_minutes` → notification at `start_time + max_duration - 5 minutes`
- If min/max resolve to the same trigger time, only one **max** reminder is scheduled to avoid duplicate notifications
- Past reminders are skipped automatically

## Notification Payload

Each schedule reminder carries:

```json
{
  "notificationId": "scheduled-min-<scheduleId>" | "scheduled-max-<scheduleId>",
  "childId": "<child-id>",
  "type": "<activity-type>",
  "scheduleId": "<schedule-id>",
  "reminderStage": "min" | "max"
}
```

This preserves compatibility with existing notification tap routing because `type` still uses the activity type (`meal`, `nap`, `education`, etc.).

## User-Facing Behavior

- Scheduling a future activity now also schedules its min/max reminder notifications
- Editing the schedule updates the notification times
- Cancelling the schedule removes its notifications
- Logging the activity from Dashboard upcoming cards removes any remaining schedule-specific reminders

## Verification

Targeted TypeScript check confirmed **no new errors** in:
- `lib/notifications.ts`
- `app/(tabs)/log.tsx`
- `app/(tabs)/index.tsx`

Pre-existing TypeScript issues remain elsewhere (`history.tsx`, `lib/api.ts`, Deno edge function typings).
