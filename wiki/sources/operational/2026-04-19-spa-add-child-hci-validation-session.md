---
id: spa-add-child-hci-validation-session-001
type: source
created: 2026-04-19
updated: 2026-04-19
last_verified: 2026-04-19
review_after: 2026-05-19
stale_after: 2026-07-19
confidence: high
source_refs: []
status: active
tags:
  - smart-parenting-app
  - mobile-dev
  - react-native
  - hci
related:
  - concepts/smart-parenting-app-tech-stack
  - concepts/hci-design-principles-mobile
  - concepts/react-native-text-input-centering
---

# Smart Parenting App — Add Child HCI + Validation + Test Seed

**Date:** 2026-04-19
**Scope:** Add child flow hardening — conditional skip button, field validation, Alert.alert removal, test account seeding
**Files changed:** `app/child/new.tsx`, `app/child/routine.tsx`, `database/seed_test_account.sql`, `scripts/create_test_user.js`

---

## Changes

### 1. Skip Button Conditional on Age

**Problem:** Skip button always visible in Add Child and Set Routine screens, even for ages 1-5 where routines are required.

**Fix:** Hide Skip button when child is 1-5 years old, show placeholder View to keep header title centered.

- `new.tsx`: `isRequired = ageYears >= 1 && ageYears <= 5` gates Skip visibility
- `routine.tsx`: Added `ageYears` and `routineRequired` computed from child DOB
- Both screens: `{isRequired ? <View style={{ width: 40, height: 40 }} /> : <TouchableOpacity>...</TouchableOpacity>}`

**HCI principle:** Error Prevention (#5) — remove escape routes that would skip required data.

### 2. Header Title Centering

**Problem:** "Add Child" / "Set Routine" title shifted right when Skip button hidden (space-between layout).

**Root cause:** `flexDirection: 'row', justifyContent: 'space-between'` needs items on both sides to center the middle element.

**Fix:** Placeholder `View` with `width: 40, height: 40` (matching back button dimensions) replaces Skip when hidden.

### 3. canProceed Field Validation (new.tsx)

**Problem:** Next button always clickable except step 0 name check. For ages 1-5, all routine fields should be required before proceeding.

**Before:** `const canProceed = step === 0 ? !!name.trim() : true;`

**After:**
```typescript
const canProceed = () => {
  if (step === 0) return !!name.trim();
  if (!isRequired) return true;
  if (step === 1) return !!gender && !!height && !!weight; // physical
  if (step === 2) return bedH && bedM && wakeH && wakeM; // sleep
  if (step === 3) return bfH && bfM && luH && luM && snH && snM && diH && diM; // meals
  if (step === 4) return napH && napM && actH && actM && lrnH && lrnM; // activities
  return true;
};
```

- Button dims (`nextBtnDisabled`) and disables when `canProceed()` returns false
- Ages <1 and >5 remain fully optional (skip all fields)

**HCI principle:** Visibility of System Status (#1) — user sees disabled state when fields incomplete.

### 4. Alert.alert() Removal (HCI Compliance)

All `Alert.alert()` calls removed from both files — zero remaining.

**Replacements:**
- Name validation → inline error text below field + red border (`inputError` style)
- Upload failure → dismissible error banner at top of scroll
- Submit error → dismissible error banner
- Routine save error → dismissible error banner

**Error banner pattern:**
```tsx
{saveError ? (
  <View style={styles.errorBanner}>
    <Ionicons name="alert-circle" size={18} color="#EF4444" />
    <Text style={styles.errorBannerText}>{saveError}</Text>
    <TouchableOpacity onPress={() => setSaveError('')}>
      <Ionicons name="close" size={16} color="#EF4444" />
    </TouchableOpacity>
  </View>
) : null}
```

**Imports cleaned:** `Alert` removed from both RN imports.

**HCI principles:** Error Prevention (#5), Help Users Recognize/Recover (#9), Aesthetic/Minimalist (#8).

### 5. Test Account Seed Script

Created `database/seed_test_account.sql` — comprehensive seed data for testing all features:

**Test parent:** test@nestnote.dev / Test1234!

**Child 1 — Emma** (3y4mo, female):
- Full routine (bed 8PM, wake 7AM, all meals, nap, activity, learn)
- 96.5cm, 14.2kg, gender set for BMI
- 28 days of all 7 activity types (screen_time, sleep, nap, meal×3, education, physical_activity)
- 3 AI recommendations (sleep, education, activity)
- 2 alerts (screen time exceeded, low sleep)

**Child 2 — Noah** (1y8mo, male):
- Full routine (bed 7:30PM, wake 6:30AM, all meals, nap, activity, learn)
- 82.3cm, 11.5kg
- 28 days of age-appropriate activities (minimal screen time, longer naps)
- 2 AI recommendations (sleep, activity)
- 2 alerts (skipped meal, late bedtime)

**Helper:** `scripts/create_test_user.js` — creates auth user via Supabase Admin API using service role key.

---

## Verification

| Check | Status |
|---|---|
| No Alert.alert() in new.tsx | ✅ |
| No Alert.alert() in routine.tsx | ✅ |
| Skip hidden for ages 1-5 | ✅ |
| Header title centered (both states) | ✅ |
| Next disabled when required fields empty | ✅ |
| Next enabled for optional (age <1, >5) | ✅ |
| Inline name error + red border | ✅ |
| Error banners dismissible | ✅ |
| Seed script covers 2 children | ✅ |
| Seed script has 28 days of data | ✅ |
