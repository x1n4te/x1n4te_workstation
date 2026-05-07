# Smart Parenting App Changelog

## April 25, 2026 Release

---

### ✅ AI Insights Screen Redesign

**Added:**
- Date display on every recommendation card (e.g., "Apr 25, 2026")
- 3-per-category limit — only the 3 most recent recommendations shown per category
- Recency badges: "Latest" (🟢), "2nd Latest" (🟡), "Oldest" (⬜)
- Category grouping with consistent sort order

**Why:** Reduces information overload and helps parents focus on the freshest AI advice.

---

### ✅ Schedule Creation Redirect

**Changed:**
- After creating a scheduled activity, app now redirects to History tab instead of staying on Log tab

**Why:** Parents get immediate visual confirmation that their schedule was saved.

---

### ✅ Notification System Overhaul

**Changed:**
- **Child Creation Wizard**: All 10 notification types now default to OFF
- **Per-Child Settings**: Every toggle logs its state change (ON/OFF) for debugging
- **Save Action**: Full notification state summary logged after saving
- **Weekly Growth**: Now properly logs when skipped due to toggle being OFF

**Why:**
- Respects user privacy — no surprise notifications
- Full transparency for developers debugging notification issues
- Parents opt-in to reminders rather than opting out

---

### Files Modified

| File | Lines Changed | Description |
|------|---------------|-------------|
| `app/(tabs)/ai.tsx` | +45 / -12 | Date footer, recency badges, 3-per-category filter |
| `app/(tabs)/log.tsx` | +1 / -1 | Redirect to History after schedule creation |
| `app/child/wizard.tsx` | +12 / -2 | Default notifications OFF; `updateChildSettings` call |
| `app/settings/child/[id].tsx` | +12 / -5 | Improved toggle logging; save summary logging |
| `lib/notifications.ts` | +5 / -1 | Weekly growth skip log when toggle is OFF |

---

### No Breaking Changes

All existing children retain their current notification settings. Only newly created children start with notifications disabled.
