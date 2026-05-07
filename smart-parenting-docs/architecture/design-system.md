# Design System

The app uses a consistent coral-themed design system to ensure a cohesive look and feel across all screens.

---

## Colors

| Name           | Hex       | Usage                                                 |
| -------------- | --------- | ----------------------------------------------------- |
| **Primary**    | `#FF7F60` | Buttons, active states, spinners, tab bar active tint |
| **Background** | `#FEFBF6` | App background                                        |
| **Surface**    | `#FFFDFF` | Cards, modals, bottom sheets                          |
| **Error**      | `#EF4444` | Validation messages, destructive actions              |

### Activity Colors

| Activity | Color | Hex |
|----------|-------|-----|
| Screen Time | Coral | `#FF7F60` |
| Sleep | Green | `#10B981` |
| Meals | Amber | `#F59E0B` |
| Education | Purple | `#8B5CF6` |

These colors appear on icons, badges, chart bars, and activity dots throughout the app.

---

## Layout

- **Horizontal padding:** 16px on all screens
- **Vertical section spacing:** 12px between sections
- **Card border radius:** 12px
- **Button border radius:** 8px

---

## Typography

- Uses React Native Paper's default type scale.
- Headers are bold; labels are medium weight.
- Error text uses the Error color (`#EF4444`).

---

## Components

### Screen Header

Used on every tab screen:
- Icon + title on the left
- Child picker pill on the right
- In modal mode, shows a back arrow instead

### Time Inputs

All time inputs use a custom component with:
- Hour and minute steppers (±1 for hours, ±5 for minutes)
- AM/PM toggle buttons
- Direct text entry for fast input

**Important:** Time inputs use plain React Native `TextInput` inside `View` wrappers, not Paper's `TextInput`, to ensure reliable vertical centering on Android.

### Chip Selectors

- **Single-select:** Circular chips with coral border when active
- **Multi-select:** Same style with a checkmark overlay

Used for activity types, food groups, meal types, and quality ratings.

### Cards

All cards use:
- White surface background (`#FFFDFF`)
- 12px border radius
- Subtle shadow on iOS, elevation on Android

---

## Tab Bar

- **5 tabs:** Dashboard, Activities, History, AI Insights, Settings
- **Height:** 80px (Android), 100px (iOS)
- **Active tint:** Coral (`#FF7F60`)
- **Labels always visible**

---

## Animation

- **Welcome back:** Fade-in + spring scale (login success)
- **Goodbye:** Fade + spring scale (sign out)
- **Success screen:** Green checkmark with brief hold before navigation
- **Redirect delay:** 1.8 seconds to let animations finish before switching tabs
