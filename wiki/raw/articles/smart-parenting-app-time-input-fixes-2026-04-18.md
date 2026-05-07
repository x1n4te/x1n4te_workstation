# Smart Parenting App — Time Input Centering + Preset Grid Session (2026-04-18)

## Session Summary
UI refinement session focused on two areas: (1) preset button layout in the child creation wizard sleep step, and (2) fixing text centering in time input boxes across the entire app.

## What Changed

### 1. Preset Buttons → 2x2 Grid
- Sleep schedule step (child creation wizard) had preset buttons (bedtime/wake-up) stacked vertically
- Restructured as a 2x2 grid using `flexWrap: 'wrap'` with `width: '46%'` per chip
- Added `presetGrid`, `presetChip`, `presetChipActive`, `presetChipText`, `presetChipTextActive` styles
- Proper `View` closure for the grid container after the `.map()`

### 2. Time Input Text Centering — Root Cause + Fix
**Problem:** Text inside `TextInput` (e.g., "12", "00") appeared offset to the top-left of the input box instead of being vertically centered.

**Root cause:** React Native Paper's `TextInput` component wraps the native `TextInput` internally. The `contentStyle` prop controls inner content styling but cannot reliably force vertical centering on Android. Internal padding offsets and `includeFontPadding` add invisible space at the top.

**Fix pattern:** Replace Paper `TextInput` with plain `RNTextInput` (imported from `react-native`) wrapped in a `View` container:
- `timeInputBox` — View with border/background, `justifyContent: 'center', alignItems: 'center'`
- `timeInputRN` — `width: '100%', height: '100%'` fills the box, `padding: 0, margin: 0, includeFontPadding: false`

**Files changed:**
- `app/child/new.tsx` — TimeField component (line ~93) + bedtime/wake-up inputs (lines ~450, ~492)
- `app/child/routine.tsx` — `timeInput` helper function (line ~221)
- `app/settings/child/[id].tsx` — `timeInput` helper function (line ~269)

### 3. AM/PM Button Spacing
- Added `marginTop: 10` to `ampmWrap` for vertical separation from time inputs
- Increased `gap: 3→6`, `marginLeft: 4→12` for horizontal separation
- Increased `ampmBtn` padding from `8×6` to `12×8` for larger tap targets

### 4. Step Hero Title Centering
- Added `textAlign: 'center'` to `stepHeroTitle` style — was missing despite parent having `alignItems: 'center'`
- Subtitle (`stepHeroSub`) already had it

## Technical Details

### Style: `timeInputBox`
```typescript
timeInputBox: {
  width: 48, height: 44,
  backgroundColor: '#FEFBF6',
  borderRadius: 10, borderWidth: 1.5, borderColor: '#E2E8F0',
  justifyContent: 'center', alignItems: 'center'
}
```

### Style: `timeInputRN`
```typescript
timeInputRN: {
  width: '100%', height: '100%',
  fontSize: 18, fontWeight: '700', color: '#0F172A',
  textAlign: 'center', textAlignVertical: 'center',
  padding: 0, margin: 0, includeFontPadding: false
}
```

### Style: `presetGrid`
```typescript
presetGrid: {
  flexDirection: 'row', flexWrap: 'wrap',
  gap: 8, marginBottom: 10, justifyContent: 'center'
}
```

### Style: `presetChip`
```typescript
presetChip: {
  width: '46%', paddingVertical: 10,
  borderRadius: 10, backgroundColor: '#F1F5F9',
  alignItems: 'center', borderWidth: 1.5, borderColor: 'transparent'
}
```

## Import Change
Added `TextInput as RNTextInput` to `react-native` import in all three files to distinguish from Paper's `TextInput`.

## Lesson Learned
Paper's `TextInput` is fine for text fields where vertical centering isn't pixel-critical, but for compact time input boxes where the digit must be dead center, plain `RNTextInput` + View wrapper is the reliable pattern.
