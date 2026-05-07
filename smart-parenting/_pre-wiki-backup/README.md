# Smart Parenting App — Recent Updates Wiki

**Last Updated:** April 25, 2026  
**Purpose:** Client-facing documentation of all recent feature updates, UX improvements, and bug fixes.

---

## 📋 Table of Contents

1. [AI Insights Screen Improvements](#1-ai-insights-screen-improvements)
2. [Schedule Creation — Instant History Redirect](#2-schedule-creation--instant-history-redirect)
3. [Notification System Overhaul](#3-notification-system-overhaul)
   - 3.1 [Per-Child Notification Toggles](#31-per-child-notification-toggles)
   - 3.2 [Child Creation Wizard — Notifications Default OFF](#32-child-creation-wizard--notifications-default-off)
   - 3.3 [Debug Logging for Developers](#33-debug-logging-for-developers)
4. [Files Modified](#files-modified)

---

## 1. AI Insights Screen Improvements

### What Changed
The AI Insights recommendations screen has been completely upgraded for better readability and focus.

### Key Improvements

| Feature | Before | After |
|---------|--------|-------|
| **Date Display** | No date shown on recommendations | Every card shows creation date (e.g., "Apr 25, 2026") |
| **Category Limit** | All recommendations shown, creating clutter | Only **3 most recent** per category displayed |
| **Recency Labels** | No visual distinction between old/new | Color-coded badges: **Latest** (green), **2nd Latest** (amber), **Oldest** (gray) |
| **Grouping** | Mixed priority sort | Grouped by category, sorted by date within each group |

### Visual Result
```
┌─────────────────────────────────────┐
│ Sleep              [HIGH]           │
│ "Consider an earlier bedtime..."    │
│                                     │
│ [Latest 🟢]          Apr 25, 2026   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Meals              [MEDIUM]         │
│ "Try adding more vegetables..."     │
│                                     │
│ [2nd Latest 🟡]      Apr 24, 2026   │
└─────────────────────────────────────┘
```

### Why This Helps
- **Reduces overwhelm** — Parents see only the most relevant 3 recommendations per category
- **Contextual dates** — Know exactly when each insight was generated
- **Instant priority** — "Latest" badge tells parents which advice is freshest

---

## 2. Schedule Creation — Instant History Redirect

### What Changed
When parents create a scheduled activity (e.g., "Screen time at 3 PM"), the app now instantly redirects to the **History tab** instead of staying on the Log tab.

### User Flow
```
Before:
  Log Tab → Fill Schedule Form → Submit → Stays on Log Tab
  (User has to manually navigate to see the schedule)

After:
  Log Tab → Fill Schedule Form → Submit → Redirects to History Tab
  (User immediately sees their scheduled activity in the list)
```

### Why This Helps
- **Immediate confirmation** — Parents see their schedule appear right away
- **Fewer taps** — No need to manually switch tabs to verify
- **Natural workflow** — After scheduling, the next logical step is reviewing the schedule

---

## 3. Notification System Overhaul

### 3.1 Per-Child Notification Toggles

#### Problem
Previously, when toggling individual notification types OFF for a child (e.g., turning off "Snack Reminder"), the system would silently skip scheduling it but provided no feedback in debug logs.

#### Solution
- **Instant toggle logging** — Every switch flip now logs:  
  `[ChildSettings] {notification_name} toggled OFF ❌` or `ON ✅`
- **Save summary logging** — After saving settings, the full state is logged:  
  `[ChildSettings] Saved with 3 notification(s) OFF for Emma: snack, nap, weekly_growth`
- **Weekly growth fix** — The "Weekly Growth Check" reminder now properly logs when skipped due to being toggled off

#### Visual Example
In Settings → Child → Notifications:
```
┌─────────────────────────────────────┐
│ 🌙 Bedtime Reminder          [ON]   │
│ ☀️ Wake-Up Reminder          [OFF]  │  ← Logs: "wake_up toggled OFF ❌"
│ 🍳 Breakfast Reminder        [ON]   │
│ 🍚 Lunch Reminder            [ON]   │
│ ...                                 │
└─────────────────────────────────────┘
```

---

### 3.2 Child Creation Wizard — Notifications Default OFF

#### Problem
Previously, when creating a new child through the wizard, **all 10 routine notifications were automatically scheduled** (bedtime, wake-up, breakfast, lunch, snack, dinner, nap, activity, learn, weekly growth). This happened without the parent's explicit consent and flooded the device with reminders.

#### Solution
- **All notifications now default to OFF** when creating a child
- The system explicitly saves `{ bedtime: false, wake_up: false, ... }` to the database
- **0 notifications are scheduled** until the parent manually enables them in Settings
- A debug log confirms: `[Wizard] Child created with all notifications OFF by default`

#### Parent Control Flow
```
Create Child Wizard
    ↓
Child Profile Created
    ↓
Notifications = ALL OFF (saved in database)
    ↓
Parent goes to Settings → Child → Notifications
    ↓
Parent manually enables desired reminders only
    ↓
Only enabled reminders get scheduled
```

#### Why This Helps
- **Opt-in, not opt-out** — Parents choose which reminders they want
- **No surprise notifications** — The app doesn't bombard new users with alerts
- **Respects preferences** — Each child's notification map is persisted and honored

---

### 3.3 Debug Logging for Developers

All notification actions now emit detailed `__DEV__`-guarded console logs for debugging:

| Action | Log Output |
|--------|------------|
| Toggle ON | `[ChildSettings] bedtime toggled ON ✅` |
| Toggle OFF | `[ChildSettings] nap toggled OFF ❌` |
| Save (some off) | `[ChildSettings] Saved with 3 notification(s) OFF for Emma: snack, nap, weekly_growth` |
| Save (all on) | `[ChildSettings] All notifications ON for Emma` |
| Schedule skipped | `[Notifications] snack for Emma — toggle is OFF, skipping` |
| Bulk cancel | `[Notifications] Cancelled 5 OS notifications and removed 5 tracked notifications for child abc-123` |
| Wizard creation | `[Wizard] Child created with all notifications OFF by default` |

---

## Files Modified

| File | Change Summary |
|------|----------------|
| `app/(tabs)/ai.tsx` | Added date footer, recency badges, 3-per-category filter logic |
| `app/(tabs)/log.tsx` | Schedule submit now redirects to `/(tabs)/history` |
| `app/child/wizard.tsx` | Added `updateChildSettings` import; defaults all notifications to OFF |
| `app/settings/child/[id].tsx` | Improved toggle logging; added save-state summary logging |
| `lib/notifications.ts` | Added weekly_growth skip logging when toggle is OFF |

---

## Questions?

For technical details on implementation, see the individual feature pages in this wiki directory.
