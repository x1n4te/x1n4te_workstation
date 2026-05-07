---
id: react-native-text-input-centering-001
type: concept
created: 2026-04-18
updated: 2026-04-18
last_verified: 2026-04-18
review_after: 2026-06-18
stale_after: 2026-10-18
confidence: high
source_refs:
  - raw/articles/smart-parenting-app-time-input-fixes-2026-04-18
status: active
tags:
  - react-native
  - mobile-dev
  - ui-design
  - smart-parenting-app
related:
  - sources/operational/2026-04-18-spa-time-input-centering-session
  - concepts/smart-parenting-app-tech-stack
  - concepts/hci-design-principles-mobile
---

# React Native TextInput Centering — View Wrapper Pattern

## Problem
React Native Paper's `TextInput` component adds internal padding offsets that `contentStyle` cannot reliably override on Android. Text rendered inside compact input boxes (e.g., time pickers showing "12", "00") appears offset to the top-left instead of being centered.

## Root Cause
Paper's `TextInput` wraps the native `TextInput` internally. On Android:
- `includeFontPadding` adds extra space above text
- Internal wrapper padding shifts content
- `textAlignVertical: 'center'` on `contentStyle` doesn't reach the native renderer reliably
- `padding: 0` on the outer style doesn't affect inner content offset

## Solution: RNTextInput + View Wrapper

Replace Paper `TextInput` with plain `RNTextInput` (from `react-native`) inside a `View` container:

### Step 1: Import
```typescript
import { TextInput as RNTextInput } from 'react-native';
// Keep Paper TextInput for non-centering-critical fields
import { TextInput } from 'react-native-paper';
```

### Step 2: Wrapper View Style
```typescript
timeInputBox: {
  width: 48,        // matches your desired input width
  height: 44,       // matches your desired input height
  backgroundColor: '#FEFBF6',
  borderRadius: 10,
  borderWidth: 1.5,
  borderColor: '#E2E8F0',
  justifyContent: 'center',  // vertical centering
  alignItems: 'center',      // horizontal centering
}
```

### Step 3: TextInput Style
```typescript
timeInputRN: {
  width: '100%',        // fills wrapper completely
  height: '100%',       // fills wrapper completely
  fontSize: 18,
  fontWeight: '700',
  color: '#0F172A',
  textAlign: 'center',        // horizontal text centering
  textAlignVertical: 'center', // vertical text centering
  padding: 0,                  // no internal padding
  margin: 0,                   // no external margin
  includeFontPadding: false,   // eliminates Android font padding
}
```

### Step 4: JSX
```tsx
<View style={s.timeInputBox}>
  <RNTextInput
    value={value}
    onChangeText={onChange}
    placeholder="12"
    keyboardType="number-pad"
    maxLength={2}
    style={s.timeInputRN}
    placeholderTextColor="#CBD5E1"
    textAlign="center"
    textAlignVertical="center"
  />
</View>
```

## When to Use This Pattern
- Compact input boxes where text must be dead center (time pickers, number pads, OTP inputs)
- Any `TextInput` where Paper's internal padding causes visual offset
- Inputs with fixed height where pixel-perfect centering matters

## When NOT to Use
- Standard text fields (name, email, notes) — Paper's `TextInput` is fine and provides Material Design features (label, outline, helper text)
- Multiline inputs where vertical centering isn't expected

## Applied In
- [[sources/operational/2026-04-18-spa-time-input-centering-session]] — Smart Parenting App sleep step, routine wizard, child settings
- `app/child/new.tsx` — TimeField component, bedtime/wake-up inputs
- `app/child/routine.tsx` — timeInput helper function
- `app/settings/child/[id].tsx` — timeInput helper function

## Related
- [[concepts/smart-parenting-app-tech-stack]] — project that uses this pattern
- [[concepts/hci-design-principles-mobile]] — UI consistency principles
