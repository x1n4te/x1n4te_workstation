---
title: Settings Screen
created: 2026-04-25
updated: 2026-04-25
type: concept
tags: [screen, settings, ui-ux, auth, notification]
sources: [raw/technical-reference.md]
---

# Settings Screen

The Settings system is split across two locations:

| Screen | Route | Role |
|--------|-------|------|
| `profile.tsx` | `/(tabs)/profile` | **Main settings hub** — parent profile, children list, notifications, sign out |
| `edit-profile.tsx` | `/settings/edit-profile` | Edit name + avatar |
| `change-email.tsx` | `/settings/change-email` | Change email address |
| `change-password.tsx` | `/settings/change-password` | Change password |
| `privacy.tsx` | `/settings/privacy` | Privacy policy display |
| `help.tsx` | `/settings/help` | FAQ with research citations |
| `child/[id].tsx` | `/settings/child/[id]` | Per-child profile, routines, notifications |

There is **no dedicated `settings/index` route** — the Profile tab IS the settings entry point.

---

## Profile Tab (`/(tabs)/profile.tsx`)

### State
| State | Type | Purpose |
|-------|------|---------|
| `loading` | `boolean` | Initial async load guard |
| `error` | `string` | Error message display |
| `refreshing` | `boolean` | Pull-to-refresh spinner |
| `notificationsEnabled` | `boolean` | Global notification master toggle |
| `showSignOutConfirm` | `boolean` | Sign-out modal |
| `showGoodbye` | `boolean` | Animated goodbye overlay |
| `goodbyeOpacity` / `goodbyeScale` | `Animated.Value` | Fade + spring animation |

### Data Loading
```
useEffect (mount) → loadChildren()
useFocusEffect (tab focus) → loadChildren() again
```

### Global Notifications Toggle
- `true` → `scheduleChildNotifications()` for **all** children
- `false` → `cancelChildNotifications()` for **all** children

⚠️ **Known issue:** The `useEffect` has `notificationsEnabled` in deps but NOT `children`. When `loadChildren()` replaces the array, the effect does NOT re-run. See [[notification-system]] for details.

### Sign-Out Flow
```
showSignOutConfirm modal
  → handleSignOut()
    → showGoodbye overlay (Animated fade + spring scale)
      → 1200ms delay
        → signOut() → router.replace('/(auth)/login')
```

### Child Card Rendering
Rotating palette: `childColors[i % childColors.length]` cycles through 5 colors. Empty state → CTA to `/child/wizard`.

---

## Edit Profile (`/settings/edit-profile.tsx`)

### Save Flow
```
validate() → supabase.auth.updateUser({
  data: { name: name.trim(), avatar_url: avatarUrl }
})
→ success: "Profile updated!" → router.back() after 2000ms
```

`updateUser()` only updates metadata. Email is **not editable here** — routed to `/settings/change-email`.

### Avatar Initials
```js
name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
```

---

## Change Email (`/settings/change-email.tsx`)

**Requires current password** before allowing email change:
```js
supabase.auth.signInWithPassword({ email: user.email, password })
→ success → supabase.auth.updateUser({ email: newEmail })
```

Re-authentication prevents session hijacking.

Success: "Confirmation sent! Check your new email for a confirmation link."

---

## Change Password (`/settings/change-password.tsx`)

### Validation Rules
| Field | Rule |
|-------|------|
| Current password | Required |
| New password | Min 6 characters |
| Confirm password | Must match new password |

Same re-authentication pattern as change-email. `updateUser({ password })` preserves the current session.

---

## Privacy Policy (`/settings/privacy.tsx`)

Read-only static compliance display:
- RA 10173 (Data Privacy Act)
- Children's Data Protection
- Secure-by-Design (E2E encryption, RLS, JWT)
- User Rights (access, correction, erasure, portability, objection)

---

## Help & FAQ (`/settings/help.tsx`)

All FAQ content is **hardcoded** in `FAQ_ITEMS` array (lines 23–366). No API, no CMS.

### Categories
`['Tracking', 'Screen Time', 'Sleep', 'Nutrition', 'Physical Activity', 'Growth', 'AI Features', 'Behavior', 'Philippine Context', 'Digital Parenting']`

### Expand/Collapse
```ts
toggle(id) → setExpandedId(id === expandedId ? null : id)
// One item open at a time
```

### Citations Box
Rendered only when expanded. Shows numbered sources in a purple-tinted box (`#F5F3FF`).

---

## Child Settings (`/settings/child/[id].tsx`)

**Most complex settings screen.** Per-child configuration hub.

### State Groups

**Profile:** `name`, `dob`, `avatarUrl`, `selectedIcon`, `showIconPicker`, `uploading`

**Body:** `gender`, `height`, `weight`, `bmiResult` (live computed)

**Routines — 9 time fields:** Each split into H/M/P. `bedH/M/P`, `wakeH/M/P`, `bfH/M/P`, `luH/M/P`, `snH/M/P`, `diH/M/P`, `napH/M/P`, `actH/M/P`, `lrnH/M/P`

**Notifications:** `notifToggles: Record<string, boolean>` — 10 keys. See [[notification-system]].

### Live BMI Preview
```ts
ageMonths = dob ? getAgeMonths(formatDateLocal(dob)) : 0
// Guard: 24-60 months (2-5 years)
assessBmi(height, weight, ageMonths, gender) → BmiResult
```
Updates on every height/weight/gender/dob change.

### Save Flow
1. `updateChildSettings(child.id, { name, date_of_birth, avatar_url, notifications })`
2. Compute BMI if age 2–5 and data complete
3. `updateChildRoutine(child.id, routine)` with all 9 times + body metrics
4. `scheduleChildNotifications(updatedChild, notifToggles)` — reschedules
5. `loadChildren()` to refresh store

### Time Input System
- **Quick Pick Chips:** `QUICK_TIMES` per routine type — tap to auto-fill
- **Manual Input:** 2-digit H/M + AM/PM toggle
- **`toTimeStr`:** H/M/P → `"HH:MM:SS"` (24h)
- **`fromTimeStr`:** `"HH:MM:SS"` → `{h, m, p}`

### Delete Flow
```ts
handleDelete() → deleteChild(child.id) → loadChildren() → router.replace('/(tabs)/profile')
```
Modal warns: "All activity records will remain, but profile and reminders will be removed."

---

## Key Design Patterns Across Settings

1. **Success timeout:** `setTimeout(() => router.back(), 2000)` after save
2. **Error dismissal:** Every error banner has an X button
3. **Loading guards:** `disabled={saving}` prevents double-submit
4. **Consistent header:** Back + title + Save button
5. **RLS:** All changes go through RLS-protected operations
