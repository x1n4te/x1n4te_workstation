---
id: hci-design-principles-mobile-001
type: concept
created: 2026-04-11
updated: 2026-04-19
last_verified: 2026-04-19
review_after: 2026-07-11
stale_after: 2026-10-11
confidence: high
source_refs:
  - sources/operational/2026-04-10-smart-parenting-ui-redesign
  - sources/operational/2026-04-19-spa-add-child-hci-validation-session
status: active
tags:
  - hci
  - ui-ux
  - mobile
  - design
  - react-native
related:
  - concepts/vercel-web-interface-guidelines
  - concepts/smart-parenting-app-tech-stack
  - sources/operational/2026-04-10-smart-parenting-ui-redesign
  - sources/operational/2026-04-19-spa-add-child-hci-validation-session
---

# HCI Design Principles — Mobile App Implementation

**Context:** Applied during Smart Parenting App UI redesign (2026-04-11) and History screen (2026-04-13)
**Reference:** Nielsen's 10 Usability Heuristics, iOS Human Interface Guidelines, Material Design

---

## Principles Applied

### 1. Visibility of System Status
**What:** The system should always keep users informed about what's happening.

| Implementation | Example |
|---|---|
| Loading states | Button shows spinner + "Signing in…" text |
| Disabled states | Grayed button when form invalid |
| Success feedback | Green checkmark screen after logging activity |
| Error feedback | Inline red error below field, not hidden in Alert |
| Progress indicators | Password strength bar (3 segments) |

### 2. Match Between System and Real World
**What:** Use language and concepts familiar to users.

| Implementation | Example |
|---|---|
| Friendly greetings | "Good morning, Alex" (time-aware) |
| Natural language | "Who's joining NestNote?" instead of "Create Child Record" |
| Emoji for quality | 😟😐😊 instead of numeric ratings |
| Food groups | 🍎🥦🍗🍚 with recognizable icons |

### 3. User Control and Freedom
**What:** Users need exits, undo, and clear navigation.

| Implementation | Example |
|---|---|
| Cancel/back on all screens | Close (×) on modal screens, back arrow on others |
| Dismissible errors | × button on error banners |
| Confirmation on destructive | "Sign Out" shows modal, not immediate action |
| Clear fields | × button to clear date input |

### 4. Consistency and Standards
**What:** Don't make users guess whether different words mean the same thing.

| Implementation | Example |
|---|---|
| Design tokens | Same colors, border-radius, spacing everywhere |
| Card pattern | Same card style on dashboard, log, settings |
| Input pattern | All inputs: icon prefix, rounded, same height (52pt) |
| Button pattern | All CTAs: rounded-16, same height, shadow |
| Section headers | Same uppercase label + card pattern |

### 5. Error Prevention
**What:** Prevent errors before they happen.

| Implementation | Example |
|---|---|
| Confirm password | Must match before submit allowed |
| Date validation | Inline error if format wrong, clear button |
| Disabled button | Can't submit with empty required fields |
| Type constraints | Numeric keyboard for duration, max length |
| Email format check | Green checkmark when valid |

### 6. Recognition Rather Than Recall
**What:** Make options visible rather than requiring users to remember.

| Implementation | Example |
|---|---|
| Visual type selector | 6 large cards with icons, not a hidden dropdown |
| Quick age chips | Tap "5 yrs" instead of calculating a date |
| Chip selectors | Visible options (Phone/Tablet/TV/PC) not text input |
| Recent activity | Shows what was logged, not just counts |
| Color-coded sections | Blue=account, amber=notifications, green=privacy |

### 7. Flexibility and Efficiency of Use
**What:** Accelerators for expert users, shortcuts for everyone.

| Implementation | Example |
|---|---|
| Duration input | Both stepper (+/-) AND editable text field |
| Child picker | Tap avatar on log screen to switch children |
| Stat card shortcuts | Tap stat card → pre-fills activity type on log screen |
| Pull-to-refresh | Manual data refresh without navigating away |

### 8. Aesthetic and Minimalist Design
**What:** Show only what's relevant.

| Implementation | Example |
|---|---|
| Progressive disclosure | Show nap quality only when nap is selected |
| Optional fields | "Notes (optional)" with placeholder hint |
| Clean hierarchy | Section headers, cards, consistent spacing |
| No clutter | 6 activity types fit in 2×3 grid, not a long list |

### 9. Help Users Recognize and Recover from Errors
**What:** Error messages should be clear and suggest fixes.

| Implementation | Example |
|---|---|
| Field-specific errors | "This email is already registered" on email field |
| Error categorization | Different messages for: invalid creds, not confirmed, network |
| Errors clear on edit | Typing clears the error on that field |
| Inline hints | "Use format YYYY-MM-DD (e.g. 2020-01-15)" |

### 10. Help and Documentation
**What:** Provide contextual help without being intrusive.

| Implementation | Example |
|---|---|
| Empty states | "No activities yet. Tap + to get started" |
| Hints | "Optional — helps us provide age-appropriate recommendations" |
| Privacy note | Lock icon + "Your child's data is private" |
| Guided CTAs | "Add a child profile to start logging" with link |

---

## Anti-Patterns Avoided

| Anti-Pattern | How Avoided |
|---|---|
| Alert.alert for errors | Inline error banners (Alert doesn't work on web in Expo) |
| Silent failures | Every action has visible feedback |
| Reset on reload | `useApp.getState()` reads fresh state, not stale closure |
| Generic error messages | Categorized: credentials, network, confirmation |
| Hidden actions | All options visible (chips, cards) not buried in menus |
| Fixed-position buttons | In scroll flow, not absolute positioned |

---

## Metrics

| Metric | Before Redesign | After Redesign |
|---|---|---|
| Activity types | 4 | 6 (+nap, +physical) |
| Input methods (duration) | Text only | Stepper + text |
| Feedback on signup | None (silent) | Inline errors, strength bar, success screen |
| Child switching | None (single child) | Dashboard chips + log screen picker |
| Meal detail | Type + quality | Type + quality + 7 food groups |
| Animation | None | Welcome/goodbye with fade in/out |
| History browsing | None | SectionList with date grouping, filter pills (NEW 2026-04-13) |

---

## Related
- [[concepts/vercel-web-interface-guidelines]] — Web-specific HCI checklist
- [[sources/operational/2026-04-10-smart-parenting-ui-redesign]] — Session documentation
- [[concepts/smart-parenting-app-tech-stack]] — Tech stack
