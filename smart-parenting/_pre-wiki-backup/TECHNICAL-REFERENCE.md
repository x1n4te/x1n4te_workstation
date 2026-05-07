# Technical Reference

**For:** Development team  
**Purpose:** Implementation details and code patterns for recent updates

---

## 1. AI Insights Filter Logic

### File: `app/(tabs)/ai.tsx`

The `filtered` useMemo now returns an array of objects containing both the recommendation and its recency rank:

```typescript
const filtered = useMemo(() => {
  let base = recommendations;
  if (activeFilter !== 'all') {
    // Apply category/priority/insight_type filter
  }

  // Group by category
  const grouped = new Map<string, Recommendation[]>();
  for (const rec of base) {
    const cat = rec.category || 'general';
    if (!grouped.has(cat)) grouped.set(cat, []);
    grouped.get(cat)!.push(rec);
  }

  // Keep top 3 per category, assign recency rank
  const result: { rec: Recommendation; recencyRank: number }[] = [];
  for (const [cat, list] of grouped) {
    const sorted = [...list].sort(
      (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    );
    const top3 = sorted.slice(0, 3);
    for (let i = 0; i < top3.length; i++) {
      result.push({ rec: top3[i], recencyRank: i });
    }
  }

  // Sort by category name, then date desc
  result.sort((a, b) => {
    const catA = a.rec.category || 'general';
    const catB = b.rec.category || 'general';
    if (catA !== catB) return catA.localeCompare(catB);
    return new Date(b.rec.created_at).getTime() - new Date(a.rec.created_at).getTime();
  });

  return result;
}, [recommendations, activeFilter]);
```

### Rendering
```tsx
{paginated.map(({ rec, recencyRank }, i) => (
  <RecommendationCard key={rec.id || i} rec={rec} recencyRank={recencyRank} />
))}
```

---

## 2. Notification Default State

### File: `app/child/wizard.tsx`

New children are created with an explicit all-off notification map:

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

### File: `lib/notifications.ts`

The `isEnabled` helper checks the toggle map:

```typescript
const isEnabled = (key: string): boolean => {
  if (notifToggles === undefined) return true;
  return notifToggles[key] ?? true;
};
```

When `notifToggles` is provided (which it always is after the wizard update), it uses the saved preference. When `undefined` (legacy calls), it defaults to `true` for backward compatibility.

---

## 3. Debug Log Patterns

### Standard Prefixes
- `[ChildSettings]` — Per-child notification toggle UI
- `[Notifications]` — Core scheduling/cancellation engine
- `[Wizard]` — Child creation flow
- `[Profile]` — Master notification toggle

### All Log Messages
```
[ChildSettings] {key} toggled ON ✅
[ChildSettings] {key} toggled OFF ❌
[ChildSettings] Saved with {n} notification(s) OFF for {name}: {list}
[ChildSettings] All notifications ON for {name}
[Notifications] Cancelled {n} OS notifications and removed {m} tracked notifications for child {id}
[Notifications] Scheduled {n} notifications for {name}
[Notifications] {type} for {name} — toggle is OFF, skipping
[Notifications] Cancelled {n} existing notifications for {name} before rescheduling
[Wizard] Child created with all notifications OFF by default
[Profile] All notifications turned ON for all children
[Profile] All notifications turned OFF for all children
```

---

## 4. Routing

### Schedule Redirect
```typescript
// app/(tabs)/log.tsx
router.replace('/(tabs)/history');
```

Uses `replace` (not `push`) to prevent back-button from returning to the filled form.

---

## 5. State Management Notes

### Zustand Fresh State Access
When accessing `selectedChild` inside callbacks or effects, always use:
```typescript
const cid = useApp.getState().selectedChild?.id;
```

Never destructure from the hook in async contexts — it goes stale.

### useFocusEffect Pattern
```typescript
useFocusEffect(
  useCallback(() => {
    const cid = useApp.getState().selectedChild?.id;
    if (cid) {
      // Load data
    }
  }, [/* deps */])
);
```

---

## 6. Testing Checklist

### AI Insights
- [ ] Create 5+ recommendations in the same category → verify only 3 show
- [ ] Verify "Latest" badge on newest, "Oldest" on 3rd newest
- [ ] Change filter → verify 3-limit applies within filter
- [ ] Verify date displays correctly

### Schedule Redirect
- [ ] Create a schedule → verify redirect to History tab
- [ ] Verify schedule appears in history list
- [ ] Verify error state does NOT redirect (stays on Log tab)

### Notifications
- [ ] Create new child → verify all toggles are OFF in settings
- [ ] Verify no notifications scheduled (check logs)
- [ ] Toggle one ON → save → verify it schedules
- [ ] Toggle one OFF → save → verify log shows skip
- [ ] Master toggle OFF → verify all cancelled
- [ ] Master toggle ON → verify only enabled types reschedule
