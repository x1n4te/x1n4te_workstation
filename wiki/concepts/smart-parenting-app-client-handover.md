---
id: smart-parenting-app-client-handover-001
type: concept
created: 2026-04-22
updated: 2026-04-23
last_verified: 2026-04-23
review_after: 2026-06-22
stale_after: 2026-10-22
confidence: high
source_refs:
  - raw/articles/smart-parenting-app-codebase-2026-04-18
  - concepts/smart-parenting-app-tech-stack
  - concepts/hci-design-principles-mobile
  - sources/operational/2026-04-23-spa-dashboard-scheduled-activities-session
  - sources/operational/2026-04-23-spa-hci-alert-fix-session
status: active
tags:
  - smart-parenting-app
  - mobile-dev
  - react-native
  - expo
  - supabase
related:
  - concepts/smart-parenting-app-tech-stack
  - concepts/smart-parenting-app-tech-stack-details
  - concepts/hci-design-principles-mobile
---

# Smart Parenting App — Client Handover Documentation

**Project:** Smart Parenting App — AI-Based Child Activity Monitoring
**Platforms:** Android (primary), iOS (compatible)
**Tech Stack:** React Native + Expo SDK 52 | Supabase | Ollama Cloud API

---

## Table of Contents

1. [What This App Does](#what-this-app-does)
2. [How the App is Built — Simple Explanation](#how-the-app-is-built)
3. [Screen-by-Screen Walkthrough](#screen-by-screen-walkthrough)
4. [Add Child — 5-Step Wizard](#add-child-5-step-wizard)
5. [Data Flow — How Data Moves](#data-flow)
6. [AI Recommendations — How It Works](#ai-recommendations)
7. [Security — How Your Data is Protected](#security)
8. [Notifications — How They Work](#notifications)
9. [File Structure — Where Everything Lives](#file-structure)
10. [Database — What We Store](#database)

---

## What This App Does

Smart Parenting is a mobile app that helps parents track their children's daily activities and get personalized parenting tips powered by AI.

**Core capabilities:**
- 👤 **Track multiple children** — each parent can manage profiles for all their kids
- 📊 **Log 6 activity types** — screen time, sleep, naps, meals, physical activity, education
- 🤖 **AI recommendations** — analyzes activity patterns and suggests improvements
- 🔔 **Smart reminders** — local notifications based on your child's routine schedule
- 📈 **History & trends** — browse past activities with date grouping and filters

---

## How the App is Built

Think of the app as three layers stacked on top of each other:

```
┌─────────────────────────────────────────────┐
│  📱 Phone Screen (what you see)             │
│  Dashboard, Log Activity, AI Insights...    │
├─────────────────────────────────────────────┤
│  🧠 App Logic (how it works)                │
│  Stores data locally, talks to internet     │
├─────────────────────────────────────────────┤
│  ☁️  Cloud (where data lives)               │
│  Supabase = Database + Login + Security     │
│  Ollama Cloud = AI Brain                    │
└─────────────────────────────────────────────┘
```

**What each piece does:**

| Piece        | Simple Explanation                               | Real Name                |
| ------------ | ------------------------------------------------ | ------------------------ |
| Phone Screen | The buttons, forms, and lists you tap on         | React Native + Expo      |
| App Logic    | Remembers your login, holds temporary data       | Zustand (state manager)  |
| Database     | Stores children, activities, recommendations     | Supabase PostgreSQL      |
| Login System | Email + password, keeps you signed in            | Supabase Auth            |
| AI Brain     | Reads activity patterns, writes tips             | Ollama Cloud API         |
| Security     | Makes sure parents only see their own kids' data | Row Level Security (RLS) |

---

## Screen-by-Screen Walkthrough

### 🔐 Login / Signup

**What it does:** Lets parents create an account or sign in.

**Signup flow:**
1. Parent enters name, email, password
2. Password must be 8+ characters with strength indicator (3-segment bar)
3. Account is created — but NOT auto-logged in (requires email confirmation)
4. After confirming email, parent can log in

**Login flow:**
1. Parent enters email + password
2. App checks credentials with Supabase
3. On success → welcome animation plays (1.8 seconds)
4. Redirects to Dashboard

**Key design choices:**
- Password strength bar (red → yellow → green) prevents weak passwords
- Email format is validated inline (green checkmark when valid)
- Errors appear directly on the field, not as popup alerts

---

### 🏠 Dashboard

**What it does:** Shows today's activity summary, upcoming scheduled activities, and recent activity for the selected child.

**Layout:**
- **Top:** "Good morning/afternoon/evening, [Name]" greeting
- **Child picker:** Tap child avatar pill to switch between children
- **Quick log card:** One-tap entry to the Log screen
- **Stat cards:** Screen Time, Sleep, Meals, Education — each with today's total
- **Upcoming scheduled:** Cards for pending scheduled activities (max 3 shown, "+N more" link)
- **Recent activities:** List of what was logged today, newest first

**Upcoming Scheduled Cards:**
Each scheduled activity shows its type icon, time, duration, and 3 action buttons:
- **Log** — Instantly logs the activity without opening another screen. Shows a brief "Logging…" → "Logged!" checkmark.
- **Update** — Opens a slide-up editor to change the activity type, start/end time, or category.
- **Cancel** — Shows an inline confirmation ("Delete this schedule permanently?"), then permanently removes the schedule.

**Interactions:**
- Tap a stat card → jumps to Log screen with that activity type pre-selected
- Pull down to refresh data
- Child picker opens a modal listing all children

---

### ➕ Log Activity

**What it does:** Lets parents record an activity for the selected child.

**6 activity types (tap to select):**

| Type | What You Log | Extra Fields |
|---|---|---|
| 📱 Screen Time | Duration + device type | Category (leisure/educational), Phone/Tablet/TV/PC |
| 😴 Sleep | Duration or time range | Quality (😟😐😊) |
| 🌙 Nap | Duration | Quality |
| 🍽️ Meals | Meal type + food groups | Breakfast/Lunch/Snack/Dinner, food group chips |
| ⚡ Physical Activity | Duration + activity type | Running/Swimming/Dancing/Cycling/etc. |
| 📚 Education | Duration + subject | Reading/Writing/Math/Art/Music |

**How it works:**
1. Select child (tap avatar pill at top)
2. Tap activity type card (large icons, 2×3 grid)
3. Fill in duration (stepper +/- or type directly)
4. Pick optional details (quality, device, food groups)
5. Tap "Log Activity" → saves to database
6. Success screen with checkmark appears

**Key HCI principles applied:**
- Visual type selector (large cards with icons, not hidden dropdown)
- Duration input supports both stepper AND editable text
- Optional fields clearly labeled "(optional)"
- Inline validation prevents logging 0-minute activities

---

### 📅 History

**What it does:** Browse all past activities organized by date.

**Layout:**
- SectionList grouped by date (Today, Yesterday, full weekday date)
- Filter pills: All, Screen Time, Sleep, Nap, Meals, Physical, Education
- Activity cards: type icon + formatted label + time

**Key helpers:**
- `groupByDate()` — groups activities by date key
- `getActivityLabel()` — formats each type with duration, quality, device/food/subject
- `getSectionTitle()` — Today/Yesterday/locale date string

**Interactions:**
- Tap child picker → opens modal to switch child
- Tap filter pill → filters to that activity type
- Pull to refresh
- Reloads on tab focus (if new activity was just logged)

---

### 🤖 AI Insights

**What it does:** Shows AI-generated parenting recommendations based on activity patterns.

**How it works:**
1. Parent taps "Run AI Insights" button
2. App fetches 28-day activity history for the selected child
3. Sends data to AI (via Supabase Edge Function → Ollama Cloud)
4. AI analyzes patterns and writes recommendations
5. Recommendations saved to database with full audit trail
6. Displayed with category badges (Sleep, Screen Time, Meals, etc.) and priority colors

**Caching:** Recommendations are cached until the next day. If recs were already generated today, the app skips the API call.

**Categories:**
- 💤 Sleep — bedtime consistency, sleep duration
- 📱 Screen Time — limits, educational vs leisure balance
- 🍽️ Meals — nutrition, meal timing, food variety
- 📚 Education — learning activity recommendations
- ⚡ Physical — exercise frequency and type
- 🏥 General — overall wellness tips

**Priority colors:**
- 🔴 High — needs immediate attention
- 🟡 Medium — suggested improvement
- 🟢 Low — optional enhancement

---

### ⚙️ Settings

**What it does:** Manage account, children, notifications, and app preferences.

**Sections:**

| Section | What's There |
|---|---|
| 👤 Account | Edit Profile, Change Email, Change Password |
| 👶 Children | List of child profiles, tap to edit each |
| 🔔 Notifications | Toggle switches for reminders |
| 🔒 Privacy & Security | Privacy settings, biometric login (placeholder) |
| ❓ Support | Help & FAQ, Contact info |
| 🚪 Sign Out | Confirmation modal (not immediate) |

**Per-Child Settings (tap a child):**
- Edit name, date of birth, gender
- Adjust height/weight (BMI preview)
- Set routine times (bedtime, wake-up, meals, nap, activity, learning)
- Configure screen time limits and minimum sleep targets
- Upload/change profile photo

---

## Add Child — 5-Step Wizard

When adding a new child, parents go through a guided 5-step wizard:

```
Step 1: Profile → Step 2: Body → Step 3: Sleep → Step 4: Meals → Step 5: Active
  👤               📏              🌙              🍽️              ⚡
```

### Step 1: Profile 👤
- **Child's name** (required) — text input
- **Date of birth** (required) — calendar date picker
- **Avatar icon** — choose from 8 emoji options (👶🧒👧👦🦁🐰🐻⭐)
- **Photo upload** (optional) — pick from gallery or take photo
- Photo is uploaded to Supabase Storage immediately on selection

### Step 2: Body 📏
- **Gender** — Boy/Girl chip selector
- **Height** (cm) — numeric input
- **Weight** (kg) — numeric input
- **BMI preview** — calculated in real-time using WHO pediatric standards
  - Shows: BMI value, percentile, category (underweight/normal/overweight/obese)
  - Age 24-60 months only (WHO data range)

### Step 3: Sleep 🌙
- **Bedtime** — quick time chips (7:30 PM, 8:00 PM, 8:30 PM, 9:00 PM, 9:30 PM) + custom picker
- **Wake-up time** — quick time chips (5:30 AM – 7:30 AM) + custom picker
- **Sleep recommendation** — shows age-appropriate sleep duration guideline
- **Minimum sleep toggle** — set a daily sleep target with age-guided default

### Step 4: Meals 🍽️
- **Breakfast time** — quick chips + custom picker
- **Lunch time** — quick chips + custom picker
- **Snack time** — quick chips + custom picker
- **Dinner time** — quick chips + custom picker

### Step 5: Active ⚡
- **Nap time** (optional for ages 1-5, hidden for older) — quick chips + custom picker
- **Activity time** (optional for ages 5+) — quick chips + custom picker
- **Learning time** (optional for ages 5+) — quick chips + custom picker

### After Completion
1. All data submitted to database in one transaction
2. Profile photo uploaded to Supabase Storage
3. BMI computed locally (saved with child record)
4. Routine notifications scheduled automatically
5. Child appears in Dashboard child picker
6. Navigates to Dashboard

---

## Data Flow

Here's how data moves when you log an activity:

```
┌──────────┐    ┌──────────────┐    ┌──────────────┐
│ Parent   │───▶│ Log Screen   │───▶│ api.ts       │
│ taps Log │    │ (fills form) │    │ logActivity()│
└──────────┘    └──────────────┘    └──────┬───────┘
                                           │
                                    ┌──────▼───────┐
                                    │ Supabase     │
                                    │ INSERT into  │
                                    │ activities   │
                                    └──────┬───────┘
                                           │
              ┌──────────────┐    ┌────────▼────────┐
              │ Dashboard    │◀───│ RLS Check:      │
              │ shows updated│    │ Does child      │
              │ stats        │    │ belong to this  │
              └──────────────┘    │ parent? Yes → OK│
                                  └─────────────────┘
```

**Security layer (RLS):** Every database operation checks: "Does this child belong to the logged-in parent?" If not, the request is blocked. This happens automatically at the database level — the app can't accidentally show someone else's data.

---

## AI Recommendations

### How the AI "Thinks"

```
┌─────────────────────────────────────────────────┐
│  Input: 28 days of activity data for one child  │
│  ┌──────────────────────────────────────────┐   │
│  │ Sleep: avg 8.2h, range 6-10h, 3 poor     │   │
│  │ Screen: avg 2.1h, 60% leisure            │   │
│  │ Meals: avg 3.2/day, mostly carbs         │   │
│  │ Physical: 4 sessions, 45min avg          │   │
│  └──────────────────────────────────────────┘   │
│                      ▼                          │
│  AI Prompt: "You are a child development        │
│  advisor. Given this child's activity data,     │
│  provide 3-5 recommendations..."                │
│                      ▼                          │
│  Output: Structured recommendations with        │
│  categories, priorities, and explanations       │
└─────────────────────────────────────────────────┘
```

### What the AI Sees
The AI receives ONLY activity summaries — not raw individual records. It sees:
- Sleep: average, min, max, consistency score
- Screen time: total, average, leisure vs educational breakdown
- Meals: average per day, food groups, unique foods
- Education: total hours, subjects covered
- Physical activity: total hours, types

### What the AI Does NOT See
- Child's name or photo
- Parent's email or account info
- Exact timestamps of activities
- Any information about other children

### Audit Trail
Every AI recommendation is saved with a `based_on` field that records exactly what data was used:
```json
{
  "period": "2026-03-17 to 2026-04-14",
  "activity_summary": { "sleep": {...}, "screen_time": {...} },
  "model": "qwen/qwen3.5",
  "previous_rec_ids": ["uuid-1", "uuid-2"]
}
```

---

## Security

### How Your Data is Protected

**Layer 1: Login (Supabase Auth)**
- Email + password authentication
- Passwords are hashed (never stored as plain text)
- Session tokens expire after inactivity

**Layer 2: Database Security (Row Level Security)**
- Every database query checks: "Is this parent allowed to see this data?"
- Parents can ONLY see their own children's data
- This happens at the database level — even if the app has a bug, the database won't leak data

**Layer 3: Storage Security**
- Profile photos stored in Supabase Storage with parent-scoped access
- Each parent's photos are in their own folder — no cross-access

**What RLS policies enforce:**

| Table | Who Can See | Who Can Edit |
|---|---|---|
| Children | Only their own parent | Only their own parent |
| Activities | Only for their own children | Only for their own children |
| Recommendations | Only for their own children | Read-only (written by AI) |
| Alerts | Only for their own children | Only their own parent (acknowledge) |

## Notifications
### How Local Notifications Work

When you set a routine schedule for a child, the app schedules daily reminders:

| Reminder | When |
|---|---|
| 🌙 Bedtime | 30 minutes before scheduled bedtime |
| ☀️ Wake-up check-in | At wake-up time |
| 🍳 Breakfast | At breakfast time |
| 🍱 Lunch | At lunch time |
| 🍪 Snack | At snack time |
| 🍽️ Dinner | At dinner time |
| 😴 Nap | At nap time (if set) |
| ⚡ Activity | At activity time (if set) |
| 📚 Learning | At learning time (if set) |
| 📏 Weekly Growth Check | Every Monday at 9:00 AM |

**Per-routine notification toggles:** Each child has individual notification toggles in their settings screen (`app/settings/child/[id].tsx`). Parents can independently enable/disable each routine reminder plus the weekly growth check. These toggles are stored in the `children.notifications` JSONB column.

**Global toggle:** The Settings tab has a single "All Notifications" toggle that turns all notifications on/off for all children. When re-enabled, all notifications are rescheduled.

**Important notes:**
- Notifications are LOCAL (on your phone only) — no server push
- They repeat daily (or weekly for growth check) until you cancel them
- You can cancel all notifications from Settings
- Changing routine times automatically reschedules notifications

---

## File Structure

```
smart-parenting-app/
├── app/                          ← All screens
│   ├── _layout.tsx               ← Root: login guard + theme
│   ├── (auth)/
│   │   ├── login.tsx             ← Login screen
│   │   └── signup.tsx            ← Signup screen
│   ├── (tabs)/
│   │   ├── index.tsx             ← Dashboard
│   │   ├── log.tsx               ← Log Activity
│   │   ├── history.tsx           ← History browser
│   │   ├── ai.tsx                ← AI Insights
│   │   └── profile.tsx           ← Settings
│   ├── child/
│   │   └── wizard.tsx            ← 5-step Add Child wizard
│   └── settings/
│       ├── edit-profile.tsx      ← Edit parent profile
│       ├── change-email.tsx      ← Change email
│       ├── change-password.tsx   ← Change password
│       ├── child/[id].tsx        ← Per-child settings
│       ├── help.tsx              ← Help & FAQ
│       └── privacy.tsx           ← Privacy settings
├── lib/                          ← Shared logic
│   ├── supabase.ts               ← Database connection
│   ├── api.ts                    ← All data operations
│   ├── bmi.ts                    ← BMI calculator (WHO standards)
│   ├── image.ts                  ← Photo upload
│   ├── notifications.ts          ← Notification scheduling
│   ├── sleep-calculator.ts       ← Sleep recommendations
│   └── database.types.ts         ← TypeScript types
├── stores/
│   └── auth.ts                   ← Login state + child selection
├── components/
│   ├── DatePicker.tsx            ← Calendar date picker
│   └── ScreenHeader.tsx          ← Shared header with child picker
├── database/
│   ├── schema.sql                ← Main database schema
│   ├── migration_*.sql           ← Schema updates
│   └── seed_test_account.sql     ← Test data
├── supabase/functions/
│   └── analyze-child/index.ts    ← AI recommendation engine
├── SCOPE.md                      ← Project agreement
└── package.json                  ← Dependencies
```

---

## Database

### Tables

**1. children** — Child profiles

| Column | Type | Purpose |
|---|---|---|
| id | UUID | Unique identifier |
| parent_id | UUID | Links to parent account |
| name | TEXT | Child's name |
| date_of_birth | DATE | For age calculations |
| gender | TEXT | Boy/Girl (for BMI) |
| avatar_url | TEXT | Profile photo URL |
| height_cm | NUMERIC | Height for BMI |
| weight_kg | NUMERIC | Weight for BMI |
| bmi | NUMERIC | Computed BMI value |
| bedtime | TIME | Routine bedtime |
| wake_up_time | TIME | Routine wake-up |
| breakfast_time | TIME | Meal schedule |
| lunch_time | TIME | Meal schedule |
| snack_time | TIME | Meal schedule |
| dinner_time | TIME | Meal schedule |
| nap_time | TIME | Routine nap |
| activity_time | TIME | Routine activity |
| learn_time | TIME | Routine learning |
| max_screen_time_minutes | INT | Screen time limit |
| min_sleep_minutes | INT | Minimum sleep target |
| notifications | JSONB | Per-routine notification toggles |
| deleted_at | TIMESTAMPTZ | Soft-delete flag |

---

**2. activities** — Activity logs

| Column | Type | Purpose |
|---|---|---|
| id | UUID | Unique identifier |
| child_id | UUID | Links to child |
| type | TEXT | Activity type (6 types) |
| value | JSONB | Activity details (duration, quality, etc.) |
| recorded_at | TIMESTAMPTZ | When activity happened |

**3. recommendations** — AI tips

| Column | Type | Purpose |
|---|---|---|
| id | UUID | Unique identifier |
| child_id | UUID | Links to child |
| content | TEXT | The recommendation text |
| category | TEXT | Sleep, Screen Time, etc. |
| priority | TEXT | High, Medium, Low |
| based_on | JSONB | Audit trail of what data was used |

**4. alerts** — System alerts

| Column | Type | Purpose |
|---|---|---|
| id | UUID | Unique identifier |
| child_id | UUID | Links to child |
| type | TEXT | Alert type |
| message | TEXT | Alert content |
| severity | TEXT | Info, Warning, Critical |
| acknowledged | BOOLEAN | Has parent seen this? |

---

## Related

- [[concepts/smart-parenting-app-system-architecture]] — Frontend/backend architecture overview
- [[concepts/smart-parenting-app-tech-stack]] — Technical stack details
- [[concepts/smart-parenting-app-tech-stack-details]] — Detailed reference with docs links
- [[concepts/hci-design-principles-mobile]] — Design principles applied
- [[sources/operational/2026-04-19-spa-add-child-hci-validation-session]] — Wizard implementation session
