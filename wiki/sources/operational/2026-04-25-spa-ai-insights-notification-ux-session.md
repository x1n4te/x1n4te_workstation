---
id: spa-ai-insights-notification-ux-2026-04-25
type: source
category: operational
created: 2026-04-25
updated: 2026-04-25
tags:
  - smart-parenting-app
  - operational
  - ai-insights
  - expo-notifications
session_date: 2026-04-25
project: smart-parenting-app
status: completed
---

# Smart Parenting App — AI Insights Redesign + Notification Defaults + UX Redirects

**Session Date:** 2026-04-25  
**Focus Areas:** AI Insights screen UX, schedule creation redirect, notification system privacy defaults, per-child toggle debug logging  
**Agent:** Kimi-K2.6

---

## Summary

Four distinct UX and system improvements shipped in a single session:

1. **AI Insights screen redesign** — capped to 3 recommendations per category, added creation dates, added recency badges (Latest / 2nd Latest / Oldest)
2. **Schedule creation instant redirect** — after creating a schedule, app redirects to History tab instead of staying on Log
3. **Notification privacy-by-default** — new children are created with all 10 notification toggles OFF; parents opt-in individually
4. **Per-child toggle debug logging** — every switch flip and save action now emits detailed `__DEV__` console logs

---

## 1. AI Insights Screen Redesign

### Changes

| Aspect | Before | After |
|--------|--------|-------|
| Category limit | All recommendations shown | Max 3 most recent per category |
| Date display | None | Every card shows `created_at` date |
| Recency indicator | None | Color-coded badge: Latest (🟢), 2nd Latest (🟡), Oldest (⬜) |
| Sort order | Priority-based | Grouped by category → date desc within group |

### Implementation

- `app/(tabs)/ai.tsx`: `filtered` useMemo now groups by `rec.category`, sorts each group by `created_at` desc, slices to top 3, assigns `recencyRank` (0,1,2), then sorts final result by category name → date
- `RecommendationCard` component receives `recencyRank: number` prop
- New style constants: `RECENCY_LABELS`, `RECENCY_COLORS`
- New card footer: `recFooter` flex row with `recencyBadge` (left) + `recDate` (right)
- Pagination (Load More) preserved — works on the post-filtered, post-capped list

### Filter Interaction

Filters (All / Sleep / High Priority / etc.) are applied **before** the 3-per-category cap. So filtering to "Sleep" shows only the 3 most recent Sleep recommendations.

---

## 2. Schedule Creation — Instant History Redirect

### Change

`app/(tabs)/log.tsx` `handleSchedule()` now uses:
```typescript
router.replace('/(tabs)/history');
```

Instead of:
```typescript
router.replace('/(tabs)');  // Dashboard
```

### Rationale

After a parent creates a scheduled activity, the natural next step is to **see and verify** it in the upcoming list. Staying on the Log tab forces manual navigation. Redirecting to History provides instant confirmation and reduces friction.

Uses `router.replace` (not `push`) so the back button won't return to the filled form.

---

## 3. Notification System — Privacy-by-Default

### Problem

Previously, creating a child via the wizard immediately scheduled **all 10 routine notifications** on the device — bedtime, wake-up, breakfast, lunch, snack, dinner, nap, activity, learn, weekly growth. Parents received surprise alerts without having explicitly enabled anything.

### Solution

**Wizard now defaults all toggles to OFF:**

```typescript
// app/child/wizard.tsx
const defaultNotifs: Record<string, boolean> = {
  bedtime: false, wake_up: false,
  breakfast: false, lunch: false, snack: false, dinner: false,
  nap: false, activity: false, learn: false,
  weekly_growth: false,
};
await updateChildSettings(child.id, { notifications: defaultNotifs });
await scheduleChildNotifications(updatedChild, defaultNotifs);
```

- `updateChildSettings()` persists the OFF state to Supabase `children.notifications` JSONB column
- `scheduleChildNotifications()` receives the all-off map → every type is skipped → 0 notifications scheduled

### Existing Children

No migration needed. Existing children retain their saved `notifications` JSONB value. Only newly created children get the all-off default.

---

## 4. Debug Logging — Per-Child Notification Toggles

### Problem

Toggling individual notification types in `app/settings/child/[id].tsx` produced **no visible feedback** in the console. When a toggle was switched OFF, developers couldn't tell if the skip logic in `lib/notifications.ts` was actually executing.

### Solution

**Three layers of logging added:**

#### Layer 1: Toggle Action (immediate)
```
[ChildSettings] snack toggled OFF ❌
[ChildSettings] bedtime toggled ON ✅
```

#### Layer 2: Save Summary (after handleSave)
```
[ChildSettings] Saved with 3 notification(s) OFF for Emma: snack, nap, weekly_growth
[ChildSettings] All notifications ON for Emma
```

#### Layer 3: Scheduler Skip (inside scheduleChildNotifications)
```
[Notifications] snack for Emma — toggle is OFF, skipping
[Notifications] weekly_growth for Emma — toggle is OFF, skipping
```

#### Layer 4: Bulk Cancel/Schedule (master toggle)
```
[Profile] All notifications turned OFF for all children
[Profile] All notifications turned ON for all children
[Notifications] Cancelled 7 OS notifications and removed 7 tracked notifications for child abc-123
[Notifications] Scheduled 5 notifications for Emma
```

All logs are `__DEV__`-guarded and only appear in development builds.

---

## Files Modified

| File | Lines | Nature |
|------|-------|--------|
| `app/(tabs)/ai.tsx` | +45 / -12 | New: date footer, recency badges, 3-per-category filter logic |
| `app/(tabs)/log.tsx` | +1 / -1 | Changed: schedule redirect target from `/(tabs)` to `/(tabs)/history` |
| `app/child/wizard.tsx` | +12 / -2 | New: `updateChildSettings` import; all-off defaultNotifs map; save to DB before scheduling |
| `app/settings/child/[id].tsx` | +12 / -5 | Changed: toggle logging reads current state before setState; save summary logs full ON/OFF state |
| `lib/notifications.ts` | +5 / -1 | New: `weekly_growth` skip log when toggle is OFF (was silently skipped before) |

---

## Verification

- `npx tsc --noEmit --pretty false`: passed (no new errors introduced)
- `git diff --check`: passed (no trailing whitespace issues)
- Forbidden pattern grep (`Alert.alert`, `@expo/dom-webview`, `fetch().blob()` on RN URIs): zero matches in modified files

---

## Related Wiki Pages

- [[concepts/smart-parenting-app-tech-stack]] — updated with AI Insights and notification sections
- [[concepts/smart-parenting-app-tech-stack-details]] — detailed reference for notification architecture
- [[concepts/smart-parenting-app-client-handover]] — client-facing docs updated
- [[concepts/expo-local-notifications]] — notification system concept page
- [[analyses/smart-parenting-app-final-product-qa-plan]] — QA verification context
