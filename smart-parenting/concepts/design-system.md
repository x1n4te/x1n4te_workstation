---
title: Design System
created: 2026-04-25
updated: 2026-04-25
type: concept
tags: [ui-ux, design-system, component]
sources: [raw/readme-2026-04-25.md]
---

# Design System

The Smart Parenting app uses a consistent coral-themed design system across all screens.

---

## Color Tokens

| Token | Hex | Usage |
|-------|-----|-------|
| Primary | `#FF7F60` | Buttons, active states, spinners, tab bar tint |
| Background | `#FEFBF6` | App background |
| Surface | `#FFFDFF` | Cards, modals, bottom sheets |
| Error | `#EF4444` | Validation, destructive actions |
| Screen Time | `#FF7F60` | Activity icon/badge |
| Sleep | `#10B981` | Activity icon/badge |
| Meals | `#F59E0B` | Activity icon/badge |
| Education | `#8B5CF6` | Activity icon/badge |

---

## Layout

- **Horizontal padding:** 16px
- **Vertical spacing between sections:** 12px
- **Border radius:** 12px cards, 8px buttons
- **Tab bar height:** 80px Android, 100px iOS
- `tabBarShowLabel: true` on all tabs

---

## Components

- **ScreenHeader** — Reusable across all tab screens: icon + title left, child picker pill right, back-mode for modals
- **DatePicker** — Custom DOB picker using `DateTimePicker`, shows age in months below
- **ChipSelector / MultiChipSelector** — Single and multi-select chips with coral active state
- **TimeRangeInput / SingleTimeInput** — Compact time entry with ± steppers and AM/PM toggle

See [[screen-activities]] for detailed usage of input components. The design system is anchored in [[app-overview]].
