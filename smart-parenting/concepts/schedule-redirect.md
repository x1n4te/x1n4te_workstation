---
title: Schedule Creation — Instant History Redirect
created: 2026-04-25
updated: 2026-04-25
type: concept
tags: [schedule, feature, navigation]
sources: [raw/feature-schedule-redirect.md, raw/changelog-2026-04-25.md]
---

# Schedule Creation — Instant History Redirect

**Route:** `app/(tabs)/log.tsx`  
**Role:** Redirect user to History tab immediately after scheduling a future activity.

See [[screen-activities]] for the scheduling form and [[screen-history]] for the History tab.

---

## User Flow

### Before
```
Log Tab → Fill Schedule Form → Submit → Stays on Log Tab
(User must manually navigate to verify)
```

### After
```
Log Tab → Fill Schedule Form → Submit → Redirects to History Tab
(User immediately sees their scheduled activity)
```

---

## Why This Change?

| Problem | Solution |
|---------|----------|
| No immediate confirmation | Parent sees the schedule appear right away |
| Extra manual navigation | Zero extra taps required |
| Uncertainty if schedule saved | Visual confirmation in the history list |

---

## Scope

Applies to **scheduling** (future activities) only. Logging past activities still shows the success state on the Log tab.

All activity types affected:
- 📱 Screen Time
- 🌙 Sleep
- 😴 Nap
- 🍳 Meals
- 🏊 Physical Activity
- 📚 Education

---

## Technical Details

### Code Change
```typescript
// Before:
await scheduleScheduledActivityNotifications(scheduled, selectedChild.name);
resetForm();
router.replace('/(tabs)');  // Redirects to Dashboard

// After:
await scheduleScheduledActivityNotifications(scheduled, selectedChild.name);
resetForm();
router.replace('/(tabs)/history');  // Redirects to History tab
```

### Why `router.replace`?
- Removes the Log screen from the navigation stack
- Pressing the device back button won't return to the filled form
- Creates a cleaner navigation experience

### Error Handling
If scheduling fails, the error is shown inline on the Log tab and **no redirect occurs**. The form stays filled for retry.
