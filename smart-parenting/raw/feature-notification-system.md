---
ingested: 2026-04-25
source_type: feature-spec
---

# Notification System Overhaul

**Status:** ✅ Completed  
**Date:** April 25, 2026  
**Files Modified:**
- `app/settings/child/[id].tsx`
- `app/child/wizard.tsx`
- `lib/notifications.ts`

---

## Overview

The notification system was rebuilt to give parents **full control** over which reminders they receive, with **transparent logging** for debugging and a **privacy-first default** of all notifications OFF for new children.

---

## Part 1: Per-Child Notification Toggles

### What Changed

Every child now has **10 individually toggleable notification types** in their Settings screen. Previously, toggling these off worked silently — now every action is logged.

### Notification Types

| # | Type | Description | Default |
|---|------|-------------|---------|
| 1 | 🌙 Bedtime Reminder | 30 min before bedtime | OFF |
| 2 | ☀️ Wake-Up Reminder | At wake-up time | OFF |
| 3 | 🍳 Breakfast Reminder | At breakfast time | OFF |
| 4 | 🍚 Lunch Reminder | At lunch time | OFF |
| 5 | 🍎 Snack Reminder | At snack time | OFF |
| 6 | 🍲 Dinner Reminder | At dinner time | OFF |
| 7 | 😴 Nap Reminder | At nap time | OFF |
| 8 | 🏊 Activity Reminder | At physical activity time | OFF |
| 9 | 📚 Learning Reminder | At learning time | OFF |
| 10 | 📊 Weekly Growth Check | Every Monday at 9 AM | OFF |

### Where to Find It
```
Settings Tab → Tap Child Card → Scroll to "Notifications" Section
```

### Toggle Behavior

**Before:**
- Toggle OFF → No log, no confirmation, unclear if it worked

**After:**
- Toggle OFF → Immediate log: `[ChildSettings] snack toggled OFF ❌`
- Toggle ON → Immediate log: `[ChildSettings] breakfast toggled ON ✅`
- Save → Summary log: `[ChildSettings] Saved with 3 OFF for Emma: snack, nap, weekly_growth`

---

## Part 2: Child Creation Wizard — Notifications Default OFF

### The Problem

Previously, creating a new child through the wizard would **automatically schedule all 10 routine notifications** on the device. Parents had no choice — they'd start receiving bedtime, wake-up, meal, and activity reminders immediately, even if they didn't want them.

### The Solution

**All notifications now default to OFF** when a child is created.

#### New Child Flow
```
Create Child Wizard
    ↓
Child Profile Created
    ↓
All 10 Notifications = OFF (saved in database)
    ↓
0 notifications scheduled on device
    ↓
Parent goes to Settings → Child → Notifications
    ↓
Parent manually enables only desired reminders
    ↓
Only enabled reminders get scheduled
```

### Why This Is Better

| Before | After |
|--------|-------|
| 10 notifications auto-enabled | 0 notifications auto-enabled |
| Parents had to manually disable unwanted ones | Parents opt-in to wanted ones |
| Surprise alerts on first use | Silent, respectful onboarding |
| No record of preferences until changed | Explicit `false` saved for each type |

### What Parents See

When they open a newly created child's notification settings:
```
┌──────────────────────────────────────┐
│ Notifications — Emma                │
│                                     │
│ 🌙 Bedtime Reminder          [OFF]  │
│ ☀️ Wake-Up Reminder          [OFF]  │
│ 🍳 Breakfast Reminder        [OFF]  │
│ 🍚 Lunch Reminder            [OFF]  │
│ 🍎 Snack Reminder            [OFF]  │
│ 🍲 Dinner Reminder           [OFF]  │
│ 😴 Nap Reminder              [OFF]  │
│ 🏊 Activity Reminder         [OFF]  │
│ 📚 Learning Reminder         [OFF]  │
│ 📊 Weekly Growth Check       [OFF]  │
└──────────────────────────────────────┘
```

Parents toggle ON only what they need.

---

## Part 3: Debug Logging for Developers

All notification actions now emit detailed console logs (visible only in development builds) for debugging and verification.

### Log Reference Table

| Action | Log Output | File |
|--------|------------|------|
| Toggle turned ON | `[ChildSettings] {name} toggled ON ✅` | `settings/child/[id].tsx` |
| Toggle turned OFF | `[ChildSettings] {name} toggled OFF ❌` | `settings/child/[id].tsx` |
| Save (mixed state) | `[ChildSettings] Saved with N OFF for {child}: {list}` | `settings/child/[id].tsx` |
| Save (all ON) | `[ChildSettings] All notifications ON for {child}` | `settings/child/[id].tsx` |
| Schedule skipped | `[Notifications] {type} for {child} — toggle is OFF, skipping` | `lib/notifications.ts` |
| Bulk cancel | `[Notifications] Cancelled N OS notifications for child {id}` | `lib/notifications.ts` |
| Wizard creation | `[Wizard] Child created with all notifications OFF by default` | `child/wizard.tsx` |

### Example Debug Session
```
[ChildSettings] snack toggled OFF ❌
[ChildSettings] nap toggled OFF ❌
[ChildSettings] weekly_growth toggled OFF ❌
[ChildSettings] Saved with 3 notification(s) OFF for Emma: snack, nap, weekly_growth
[Notifications] Cancelled 7 OS notifications and removed 7 tracked notifications for child abc-123
[Notifications] Scheduled 7 notifications for Emma
[Notifications] snack for Emma — toggle is OFF, skipping
[Notifications] nap for Emma — toggle is OFF, skipping
[Notifications] weekly_growth for Emma — toggle is OFF, skipping
```

---

## Part 4: Master "All Notifications" Toggle

### Location
```
Settings Tab → "All Notifications" Switch
```

### Behavior
- **Turning ON**: Schedules notifications for ALL children, respecting each child's individual toggle preferences
- **Turning OFF**: Cancels ALL notifications for ALL children

### Important
The master toggle does **not** override individual child settings. When turned back ON:
- Child A (3 reminders ON) → Those 3 are rescheduled
- Child B (all OFF) → Nothing is scheduled
- Child C (all ON) → All 10 are scheduled

---

## Client FAQ

**Q: Will existing children lose their notification settings?**  
A: No. Existing children's saved preferences are preserved. Only newly created children start with all OFF.

**Q: Can a parent enable all notifications at once for a child?**  
A: Currently, each type must be toggled individually. This is intentional to encourage mindful selection.

**Q: What happens if a child has no routine times set?**  
A: Even if a notification type is toggled ON, it won't schedule if the corresponding routine time is empty (e.g., no bedtime set → no bedtime reminder, even if enabled).

**Q: Are scheduled activity reminders (the 5-minute alerts) affected by these toggles?**  
A: No. Scheduled activity reminders ("Screen time ends in 5 minutes") are separate from routine daily reminders and are always scheduled for pending activities.

**Q: Do debug logs appear in production builds?**  
A: No. All logs are wrapped in `__DEV__` checks and only appear during development.

---

**Related Files:**
- `app/settings/child/[id].tsx`
- `app/child/wizard.tsx`
- `lib/notifications.ts`
- `app/(tabs)/profile.tsx`
