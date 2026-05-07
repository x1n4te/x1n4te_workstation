---
title: Notification System
created: 2026-04-25
updated: 2026-04-25
type: concept
tags: [notification, feature, ui-ux]
sources: [raw/feature-notification-system.md, raw/changelog-2026-04-25.md]
---

# Notification System

The notification system was rebuilt to give parents **full control** over which reminders they receive, with **transparent logging** for debugging and a **privacy-first default** of all notifications OFF for new children.

See [[screen-settings]] for the per-child toggle UI and [[screen-dashboard]] for scheduled activity display.

---

## Per-Child Notification Toggles

Every child has **10 individually toggleable notification types** in their Settings screen.

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

**Location:** Settings Tab → Tap Child Card → "Notifications" Section

### Toggle Behavior
- Toggle OFF → Immediate log: `[ChildSettings] snack toggled OFF ❌`
- Toggle ON → Immediate log: `[ChildSettings] breakfast toggled ON ✅`
- Save → Summary log: `[ChildSettings] Saved with 3 OFF for Emma: snack, nap, weekly_growth`

---

## Child Creation Wizard — Notifications Default OFF

Previously, creating a child auto-scheduled all 10 routine notifications. Now:

- **All notifications default to OFF** when a child is created
- System explicitly saves `{ bedtime: false, wake_up: false, ... }` to the database
- **0 notifications scheduled** until the parent manually enables them

### New Child Flow
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
Parent manually enables desired reminders
    ↓
Only enabled reminders get scheduled
```

---

## Master "All Notifications" Toggle

**Location:** Settings Tab → "All Notifications" Switch

- **Turning ON:** Schedules notifications for ALL children, respecting each child's individual toggle preferences
- **Turning OFF:** Cancels ALL notifications for ALL children

The master toggle does **not** override individual child settings. When turned back ON:
- Child A (3 reminders ON) → Those 3 are rescheduled
- Child B (all OFF) → Nothing is scheduled
- Child C (all ON) → All 10 are scheduled

---

## Debug Logging

All notification actions emit `__DEV__`-guarded console logs:

| Action | Log Output |
|--------|------------|
| Toggle ON | `[ChildSettings] {key} toggled ON ✅` |
| Toggle OFF | `[ChildSettings] {key} toggled OFF ❌` |
| Save (mixed) | `[ChildSettings] Saved with {n} OFF for {name}: {list}` |
| Save (all ON) | `[ChildSettings] All notifications ON for {name}` |
| Schedule skipped | `[Notifications] {type} for {name} — toggle is OFF, skipping` |
| Bulk cancel | `[Notifications] Cancelled {n} OS notifications for child {id}` |
| Wizard creation | `[Wizard] Child created with all notifications OFF by default` |

---

## Technical Reference

### Default State in Wizard
```typescript
const defaultNotifs: Record<string, boolean> = {
  bedtime: false, wake_up: false,
  breakfast: false, lunch: false, snack: false, dinner: false,
  nap: false, activity: false, learn: false,
  weekly_growth: false,
};
await updateChildSettings(child.id, { notifications: defaultNotifs });
await scheduleChildNotifications(updatedChild, defaultNotifs);
```

### `isEnabled` Helper
```typescript
const isEnabled = (key: string): boolean => {
  if (notifToggles === undefined) return true;
  return notifToggles[key] ?? true;
};
```
When `notifToggles` is provided, uses saved preference. When `undefined` (legacy), defaults to `true` for backward compatibility.

---

## FAQ

**Q: Will existing children lose their notification settings?**  
A: No. Existing children's saved preferences are preserved. Only newly created children start with all OFF.

**Q: What happens if a child has no routine times set?**  
A: Even if a notification type is toggled ON, it won't schedule if the corresponding routine time is empty.

**Q: Are scheduled activity reminders (5-minute alerts) affected by these toggles?**  
A: No. Scheduled activity reminders are separate from routine daily reminders and are always scheduled for pending activities.

**Q: Do debug logs appear in production builds?**  
A: No. All logs are wrapped in `__DEV__` checks.
