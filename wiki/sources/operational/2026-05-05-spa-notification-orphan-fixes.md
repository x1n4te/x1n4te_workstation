---
id: 2026-05-05-spa-notification-orphan-fixes
type: source
created: 2026-05-05
updated: 2026-05-05
confidence: high
status: active
tags:
  - smart-parenting-app
  - expo-notifications
  - scheduled-activities
  - supabase
source_refs:
  - /home/xynate/local-projects/smart-parenting-app/app/(tabs)/index.tsx
  - /home/xynate/local-projects/smart-parenting-app/lib/notifications.ts
  - /home/xynate/local-projects/smart-parenting-app/lib/api.ts
  - /home/xynate/local-projects/smart-parenting-app/database/schema.sql
---

# Smart Parenting notification orphan fixes — 2026-05-05

## Changes
- Completed scheduled activities now cancel OS notifications before logging the activity and marking the schedule completed, reducing crash-window orphan notifications.
- Routine pre-reminder skip logging now distinguishes base reminders from `-extra` 15-minute pre-reminders for both disabled toggles and missing routine times.
- `scheduled_activities` now has a `deleted_at` column in the consolidated schema/types, with SELECT/INSERT RLS guarding soft-deleted rows.
- `getScheduledActivities` filters `deleted_at IS NULL` and supports a `fromStartTime` option for restore jobs.
- Scheduled-activity notification restore now queries only future pending schedules.
- Edge Function scheduled-activity summaries filter `deleted_at=is.null`.

## Verification
- `git diff --check` passed.
- `npx tsc --noEmit --skipLibCheck` passed.
- `./gradlew :app:assembleDebug` passed and produced `android/app/build/outputs/apk/debug/app-debug.apk`.
- APK installed successfully to adb device `192.168.1.15:39903` (`23021RAAEG`).

## Note
The deployed Supabase database must have `scheduled_activities.deleted_at` added before app clients that filter this column are used against that environment.
