---
id: spa-routine-wizard-session-2026-04-14-001
type: source
created: 2026-04-14
updated: 2026-04-14
last_verified: 2026-04-14
review_after: 2026-05-14
stale_after: 2026-07-14
confidence: high
source_refs: []
status: active
tags:
  - smart-parenting-app
  - mobile-dev
  - expo
  - supabase
related:
  - concepts/smart-parenting-app-tech-stack
  - sources/operational/2026-04-14-smart-parenting-feature-session
---

# Smart Parenting App — Routine Wizard + Notifications Session Log

**Date:** 2026-04-14 (late night)
**Duration:** ~1 hour
**Feature:** Child routine setup wizard, local scheduled notifications, BMI assessment

---

## What Was Built

### 1. Database Migration (`database/migration_child_routine.sql`)
Added 11 columns to `children` table:
- **Sleep:** `bedtime` (TIME), `wake_up_time` (TIME)
- **Meals:** `breakfast_time`, `lunch_time`, `snack_time`, `dinner_time` (all TIME)
- **Activities:** `nap_time`, `activity_time`, `learn_time` (all TIME, nullable for 6+)
- **Physical:** `height_cm` (NUMERIC), `weight_kg` (NUMERIC), `bmi` (auto-calculated by trigger)

BMI trigger: `weight(kg) / (height(cm)/100)²` — fires on INSERT/UPDATE of height/weight.

### 2. TypeScript Types (`lib/api.ts`)
- `Child` interface expanded with 13 new fields
- `AgeGroup` type: `'toddler'` (2-5) vs `'child'` (6+)
- `getAgeGroup(dob)` — returns age group from DOB
- `getAgeMonths(dob)` — returns age in months
- `RoutineData` interface for wizard form data
- `updateChildRoutine(childId, routine)` — saves routine to Supabase

### 3. BMI Calculator (`lib/bmi.ts`)
- WHO LMS parameters for BMI-for-age (boys + girls, 24-60 months)
- `calculateBmi(height, weight)` — raw BMI
- `assessBmi(height, weight, ageMonths, gender)` — full assessment:
  - z-score via LMS method: `((BMI/M)^L - 1) / (L*S)`
  - percentile via normal CDF approximation
  - category: underweight (<5th), normal (5-85th), overweight (85-95th), obese (>95th)
- Returns null if age <24 or >60 months (outside WHO reference)

### 4. Notifications Service (`lib/notifications.ts`)
- `expo-notifications` + `expo-device` — daily triggers, no server
- 9 notification types per child:
  - Bedtime (-30 min before), wake-up, breakfast, lunch, snack, dinner, nap, activity, learn
- `scheduleChildNotifications(child)` — schedules all for one child
- `cancelChildNotifications(childId)` — cancels all for one child
- `hasRoutineSet(child)` — check if any routine time is set
- `initNotifications()` — request permission, call in root layout

### 5. Routine Wizard (`app/child/routine.tsx`)
4-step wizard triggered after child creation:

| Step | Content | Age logic |
|---|---|---|
| 1. Sleep | Bedtime + wake-up time | Required all ages |
| 2. Meals | Breakfast, lunch, snack, dinner | Required all ages |
| 3. Activities | Nap, activity, learn | Required 2-5, optional 6+ |
| 4. Physical | Height (cm) + weight (kg) → BMI preview | Required all ages |

- Quick-set chips for common times (e.g., 7:30PM, 8:00PM for bedtime)
- Manual AM/PM input
- Live BMI preview with WHO percentile + color-coded category card
- "Skip" button to bypass wizard entirely
- "Required" / "Optional" badges based on age group

### 6. Flow Integration
- `app/child/new.tsx` — after create, navigates to `/child/routine?childId=...` instead of `router.back()`
- `app/_layout.tsx` — `initNotifications()` on mount, notification tap listener, routine screen in Stack

---

## Known Issues (TO DEBUG)

### Issue 1: Notifications require dev build
`expo-notifications` doesn't work in Expo Go on SDK 52+. Need `eas build --profile development` or `npx expo run:android`.

### Issue 2: BMI gender not captured
The `children` table has no `gender` column. BMI assessment uses `'male'` as default. Need to add gender field or ask during wizard.

### Issue 3: Notification reschedule on edit
When routine is edited from settings, `scheduleChildNotifications` should cancel old + schedule new. Currently works (cancels by childId then reschedules) but needs testing.

### Issue 4: Time format edge cases
- TIME columns in DB are `HH:MM:SS` but wizard outputs `HH:MM:00`
- `fromTimeStr()` handles both `HH:MM` and `HH:MM:SS`
- Quick-set chips may set hour=12 for noon (12PM → 12:00) correctly, but midnight (12AM → 00:00) needs verification

### Issue 5: Supabase types untyped
All `.update()` and `.insert()` calls cast to `(supabase as any)` because the project doesn't have generated Supabase types. After running the migration, should regenerate types with `npx supabase gen types typescript`.

---

## Files Created/Modified

| File | Action |
|---|---|
| `database/migration_child_routine.sql` | Created |
| `lib/api.ts` | Modified (Child interface, RoutineData, updateChildRoutine) |
| `lib/bmi.ts` | Created |
| `lib/notifications.ts` | Created |
| `app/child/routine.tsx` | Created |
| `app/child/new.tsx` | Modified (navigate to wizard) |
| `app/_layout.tsx` | Modified (notif init + routine screen) |
| `package.json` | Modified (expo-notifications, expo-device) |

## Related
- [[concepts/smart-parenting-app-tech-stack]] — main tech stack page
- [[concepts/hci-design-principles-mobile]] — HCI patterns used in wizard
