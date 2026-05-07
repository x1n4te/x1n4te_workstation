# Changelog

## April 25, 2026 Release

---

### AI Insights Screen Redesign

**What's new:**
- Every recommendation card now shows the date it was generated (e.g., "Apr 25, 2026").
- Only the **3 most recent recommendations per category** are displayed to reduce clutter.
- **Recency badges** show how fresh each recommendation is within its category:
  - **Latest** (green) — most recent
  - **2nd Latest** (amber) — second most recent
  - **Oldest** (gray) — third most recent

**Why:** Parents were overwhelmed by too many recommendations at once. Now they see only the most relevant, recent advice.

---

### Schedule Creation Redirect

**What's changed:**
- After creating a scheduled activity, the app now redirects to the **History tab** instead of staying on the Activities tab.

**Why:** Parents get immediate visual confirmation that their schedule was saved and can see it in their upcoming list right away.

---

### Notification System Overhaul

**What's changed:**
- **New children** are created with **all notifications OFF by default**. Previously, all 10 routine reminders were auto-enabled.
- **Toggle logging:** Every notification switch flip now logs its state for easier debugging.
- **Save summary:** After saving notification settings, the app logs how many reminders are off and which ones.
- **Weekly growth fix:** The "Weekly Growth Check" now properly logs when it's skipped due to being disabled.

**Why:**
- Respects user privacy — no surprise notifications.
- Parents opt-in to the reminders they want rather than disabling unwanted ones.
- Developers get full transparency when debugging notification issues.

---

### No Breaking Changes

Existing children's notification settings are preserved. Only newly created children start with all reminders disabled.
