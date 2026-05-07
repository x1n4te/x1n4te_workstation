---
id: spa-time-input-centering-session-001
type: source
created: 2026-04-18
updated: 2026-04-18
last_verified: 2026-04-18
review_after: 2026-05-18
stale_after: 2026-07-18
confidence: high
source_refs:
  - raw/articles/smart-parenting-app-time-input-fixes-2026-04-18
status: active
tags:
  - smart-parenting-app
  - mobile-dev
  - react-native
  - ui-design
related:
  - concepts/react-native-text-input-centering
  - concepts/smart-parenting-app-tech-stack
  - concepts/hci-design-principles-mobile
---

# Smart Parenting App — Time Input Centering + Preset Grid Session

**Date:** 2026-04-18
**Scope:** UI refinement — sleep step preset layout + time input text centering across all screens
**Files changed:** `app/child/new.tsx`, `app/child/routine.tsx`, `app/settings/child/[id].tsx`

## Changes

### Preset Buttons → 2x2 Grid
Sleep schedule presets (bedtime/wake-up quick-select chips) restructured from vertical list to 2x2 grid:
- `presetGrid`: `flexWrap: 'wrap'`, `width: '46%'` per chip, `gap: 8`
- Applied to both bedtime and wake-up columns in the sleep step

### Time Input Text Centering Fix
**Problem:** Text digits ("12", "00") offset to top-left inside `TextInput` box on Android.
**Root cause:** Paper `TextInput` wrapper adds internal padding that `contentStyle` can't override.
**Fix:** Replace Paper `TextInput` with plain `RNTextInput` + `View` wrapper pattern.
- `timeInputBox`: View with border/background, `justifyContent: 'center', alignItems: 'center'`
- `timeInputRN`: `width: '100%', height: '100%'`, `padding: 0, margin: 0, includeFontPadding: false`

### AM/PM Button Spacing
- `ampmWrap`: `gap: 3→6`, `marginLeft: 4→12`, added `marginTop: 10`
- `ampmBtn`: padding increased to `12×8` for larger tap targets

### Step Hero Title
- Added missing `textAlign: 'center'` to `stepHeroTitle` style

## Technical Details

See [[concepts/react-native-text-input-centering]] for the reusable pattern.
See [[concepts/react-native-textinput-centering]] for full code snippets.
