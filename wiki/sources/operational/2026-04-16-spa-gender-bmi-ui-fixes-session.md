---
id: spa-session-2026-04-16-gender-bmi-ui-fixes-001
type: source
created: 2026-04-16
updated: 2026-04-16
last_verified: 2026-04-16
review_after: 2026-05-16
stale_after: 2026-07-16
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
  - sources/operational/2026-04-14-spa-routine-wizard-session
  - sources/operational/2026-04-14-spa-ai-recommendation-flow-session
---

# Smart Parenting App — Gender Column, BMI Fix, UI Fixes + Google Workspace Setup

**Date:** 2026-04-16
**Duration:** ~3 hours
**Branch:** feature/ui-redesign-nestnote
**Connection:** Wireless ADB (phone debug mode)

---

## What Was Built

### 1. Google Workspace Integration (side task)
- Full OAuth 2.0 setup for Gmail, Calendar, Drive, Sheets, Docs, People API
- Fixed `hermes_constants` import path (PYTHONPATH needed for skills/productivity scripts)
- Installed Google API deps into hermes-agent venv (pip via ensurepip)
- Fixed Google Cloud Testing mode (added test user for 403 access_denied)
- Verified: calendar, gmail search, drive search all working
- Created 6 Google Calendar events for SPA TODO queue (3-6PM PH time)
- Verified Canvas LMS: 4 courses enrolled in 3TSY2526 (Third Term)

### 2. IREC Form No. 01 Review (side task)
- Audited `IREC Form No. 01 Application Form for Ethical Review.md`
- Found 7 discrepancies: title mismatch (CRITICAL), Action Research classification, internet data marked No, community-based research, Camama missing info, required docs unchecked, SDG 9 only
- Generated corrected SDG alignment paragraph (added SDG 16 + Explainable AI language)
- Recommended title update to match revised thesis

### 3. SPA Phase 1 — Gender Column + BMI + UI Fixes

#### 3a. Gender Column Migration
- Created `database/migration_gender.sql`
- `ALTER TABLE children ADD COLUMN gender TEXT CHECK (gender IN ('male', 'female'))`

#### 3b. api.ts Changes
- Added `gender: 'male' | 'female' | null` to `Child` interface
- Added `gender: 'male' | 'female' | null` to `RoutineData` interface

#### 3c. Routine Wizard Gender Picker (routine.tsx)
- Added gender state variable
- Added Boy/Girl chip picker UI on Step 4 (Physical)
- BMI `assessBmi()` now uses actual gender instead of hardcoded `'male'`
- Added "Select gender above" hint when gender not set
- Added 5 styles: `genderRow`, `genderChip`, `genderChipActive`, `genderText`, `genderTextActive`

#### 3d. Midnight Edge Case Verification
- `toTimeStr('12', '00', 'AM')` → `'00:00:00'` ✓
- `fromTimeStr('00:00:00')` → `12:00 AM` ✓
- Both `HH:MM` and `HH:MM:SS` formats handled ✓
- Overnight duration (9PM→6AM = 9h) ✓
- No code changes needed — already correct

#### 3e. Keyboard Jump Fix (new.tsx)
- Bug: navigating from child creation (keyboard open) to routine wizard caused KeyboardAvoidingView to oscillate (jump down then up)
- Fix: added `Keyboard.dismiss()` before `router.replace()` to close keyboard before navigation

#### 3f. Calendar Alignment Fix (history.tsx)
- Bug: today's date with `aspectRatio: 1` + `borderWidth: 1.5` caused inconsistent row heights; selecting today misaligned the row
- Fix:
  - Replaced `aspectRatio: 1` with fixed `height: 48`
  - Added `borderWidth: 1.5` + `borderColor: 'transparent'` to ALL cells (reserves border space)
  - Today's cell just changes `borderColor` (no size change)
  - Selected cell adds `backgroundColor` + changes `borderColor` (no size change)

### 4. Expo Build Fixes

#### 4a. @expo/dom-webview SDK 55/52 Incompatibility
- `expo@52.0.49` bundles `@expo/dom-webview@55.0.5` which requires `expo-module-gradle-plugin` (SDK 55 only)
- `npx expo install --fix` did NOT downgrade this package
- Workaround: removed `node_modules/@expo/dom-webview` entirely
- Build successful after removal

#### 4b. Wireless ADB for Device Testing
- User connected phone via wireless ADB for dev build testing
- Dev build installed and tested on device

---

## Files Created/Modified

| File | Action |
|---|---|
| `database/migration_gender.sql` | Created |
| `lib/api.ts` | Modified (Child.gender, RoutineData.gender) |
| `app/child/routine.tsx` | Modified (gender picker, BMI gender fix, styles) |
| `app/child/new.tsx` | Modified (Keyboard.dismiss fix) |
| `app/(tabs)/history.tsx` | Modified (calendar cell dimensions fix) |

## Known Remaining

- Gender migration not yet applied to Supabase
- Supabase types not regenerated
- Notification reschedule on edit not tested on device
- SCOPE.md milestone status not checked
- Edge Function deploy status unknown

## Related
- [[concepts/smart-parenting-app-tech-stack]] — main tech stack page
- [[sources/operational/2026-04-14-spa-routine-wizard-session]] — original routine wizard session
- [[sources/operational/2026-04-14-spa-ai-recommendation-flow-session]] — AI recommendation flow
