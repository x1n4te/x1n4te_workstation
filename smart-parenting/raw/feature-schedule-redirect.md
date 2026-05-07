---
ingested: 2026-04-25
source_type: feature-spec
---

# Schedule Creation — Instant History Redirect

**Status:** ✅ Completed  
**Date:** April 25, 2026  
**File Modified:** `app/(tabs)/log.tsx`

---

## Overview

When parents create a scheduled activity, the app now **instantly redirects to the History tab** so they can immediately see and verify their new schedule.

---

## User Flow Comparison

### Before (Old Behavior)
```
1. Parent taps "Log" tab
2. Switches to "Schedule" mode
3. Fills in activity type, time, duration
4. Taps "Schedule Activity" button
5. App stays on the Log tab
6. Parent manually navigates to History to verify
```

### After (New Behavior)
```
1. Parent taps "Log" tab
2. Switches to "Schedule" mode
3. Fills in activity type, time, duration
4. Taps "Schedule Activity" button
5. App automatically redirects to History tab
6. Parent immediately sees the scheduled activity in the list
```

---

## Why This Change?

| Problem | Solution |
|---------|----------|
| No immediate confirmation | Parent sees the schedule appear right away |
| Extra manual navigation | Zero extra taps required |
| Uncertainty if schedule saved | Visual confirmation in the history list |
| Broken workflow | Natural flow: create → review |

---

## What Activities Are Affected?

All scheduled activities redirect to History after creation:

- 📱 Screen Time
- 🌙 Sleep
- 😴 Nap
- 🍳 Meals
- 🏊 Physical Activity
- 📚 Education

> **Note:** This only applies to **scheduling** (future activities). Logging past activities still shows the success state on the Log tab.

---

## Visual Example

```
Step 1: Parent fills schedule form
┌──────────────────────────────────────┐
│  [Log]  [Schedule]                     │
│                                     │
│  Activity: Screen Time ▼             │
│  Date: April 25, 2026               │
│  Time: 3:00 PM                      │
│  Duration: 30-60 min                │
│                                     │
│  [  Schedule Activity  ]            │
└──────────────────────────────────────┘

Step 2: Tap button → Instant redirect

Step 3: History tab shows new schedule
┌──────────────────────────────────────┐
│  History                    [Today]│
│                                     │
│  ┌────────────────────────┐        │
│  │ Screen Time                     │ ← NEW!  │
│  │ Scheduled: 3:00 PM - 4:00 PM   │        │
│  │ Status: 🔴 Upcoming             │        │
│  └────────────────────────┘        │
│                                     │
└──────────────────────────────────────┘
```

---

## Technical Details

### Code Change
```typescript
// In app/(tabs)/log.tsx, handleSchedule function

// Before:
await scheduleScheduledActivityNotifications(scheduled, selectedChild.name);
resetForm();
router.replace('/(tabs)');  // Redirects to Dashboard

// After:
await scheduleScheduledActivityNotifications(scheduled, selectedChild.name);
resetForm();
router.replace('/(tabs)/history');  // Redirects to History tab
```

### Why `router.replace` Instead of `router.push`?
- `replace` removes the Log screen from the navigation stack
- Pressing the device back button won't return to the filled form
- Creates a cleaner navigation experience

---

## Client FAQ

**Q: Does this affect logging past activities?**  
A: No. Logging completed activities (the "Log" mode) still shows a success message on the same screen. Only the "Schedule" mode redirects.

**Q: Can parents still navigate to other tabs after scheduling?**  
A: Yes. The redirect is just the initial landing. Parents can freely switch between all tabs.

**Q: What happens if scheduling fails?**  
A: The error is shown inline on the Log tab, and no redirect occurs. The form stays filled so parents can retry.

---

**Related Files:** `app/(tabs)/log.tsx`
