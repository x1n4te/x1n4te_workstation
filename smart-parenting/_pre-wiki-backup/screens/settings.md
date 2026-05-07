## Architecture Overview

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

### State Architecture

| State | Type | Purpose |
|-------|------|---------|
| `loading` | `boolean` | Initial async load guard |
| `error` | `string` | Error message display |
| `refreshing` | `boolean` | Pull-to-refresh spinner |
| `notificationsEnabled` | `boolean` | Global notification master toggle |
| `showSignOutConfirm` | `boolean` | Sign-out modal |
| `showGoodbye` | `boolean` | Animated goodbye overlay |
| `goodbyeOpacity` | `Animated.Value` | Fade-in for goodbye |
| `goodbyeScale` | `Animated.Value` | Spring scale for goodbye |

### Data Loading (lines 116–135)
```
useEffect (mount) → loadChildren()
useFocusEffect (tab focus) → loadChildren() again  // ensures fresh data on return
```

### Global Notifications Toggle (lines 151–165)
When the master switch changes:
- `true` → `scheduleChildNotifications()` for **all** children
- `false` → `cancelChildNotifications()` for **all** children

⚠️ **Bug (known):** The `useEffect` has `notificationsEnabled` in its dependency array but NOT `children`. When `loadChildren()` replaces the children array, the effect does NOT re-run, so the new children don't get their notification schedules updated until the next toggle. The fix is moving `children` into the dependency array and wrapping `apply()` in a useCallback, or restructuring to fire on both state changes independently.

### Sign-Out Flow (lines 171–200)
```
showSignOutConfirm modal (fade in)
  → handleSignOut()
    → showGoodbye overlay (Animated fade + spring scale)
      → 1200ms delay
        → signOut() → router.replace('/(auth)/login')
```

The goodbye animation uses `Animated.parallel` (fade + spring simultaneously), then after 1200ms, fades out before calling `signOut()`.

### Child Card Rendering (lines 311–325)
Children are rendered with a rotating palette:
```js
childColors[i % childColors.length]  // cycles through 5 colors
```
If no children exist → empty state with CTA to `/child/wizard`.

---

## Edit Profile (`/settings/edit-profile.tsx`)

### State

| State | Type | Purpose |
|-------|------|---------|
| `name` | `string` | Form field |
| `avatarUrl` | `string` | Uploaded image URL |
| `uploading` | `boolean` | Image upload spinner |
| `saving` | `boolean` | Save spinner |
| `nameError`, `submitError`, `uploadError` | `string` | Validation errors |
| `submitSuccess` | `string` | Success message |

### Save Flow (lines 46–67)
```
validate() → supabase.auth.updateUser({
  data: { name: name.trim(), avatar_url: avatarUrl }
})
→ success: "Profile updated!" → router.back() after 2000ms
```

**Key behavior:** `supabase.auth.updateUser()` only updates metadata. Email is deliberately **not editable here** — routed to `/settings/change-email` instead. This is correct separation of concerns.

### Avatar Initials (lines 69–74)
```js
name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
```
First letter of each word, max 2 chars. Empty name → empty string (no crash, just blank avatar).

---

## Change Email (`/settings/change-email.tsx`)

### Security Pattern
**Requires current password** before allowing email change (lines 49–56):
```js
supabase.auth.signInWithPassword({ email: user.email, password })
→ success → supabase.auth.updateUser({ email: newEmail })
```

This re-authentication prevents session hijacking (someone who left a browser logged in can't change the email without knowing the password).

### Validation (lines 27–43)
- New email: required + regex format check
- Current password: required

### Success Message (line 60)
> "Confirmation sent! Check your new email for a confirmation link."

Supabase sends a confirmation email to the **new** address — user must click it to complete the change.

---

## Change Password (`/settings/change-password.tsx`)

### Validation Rules (lines 29–47)
| Field | Rule |
|-------|------|
| Current password | Required |
| New password | Min 6 characters |
| Confirm password | Must match new password |

Same re-authentication pattern as change-email.

### `PasswordField` Sub-component (lines 73–112)
Reusable component rendering a label + password input + show/hide toggle (eye icon). Extracted to avoid repetition for 3 identical fields.

### Info Card (lines 146–151)
```jsx
<View style={styles.infoCard}>
  <Ionicons name="information-circle" size={20} color="#6366F1" />
  <Text>Your new password must be at least 6 characters. 
        You'll stay logged in on this device.</Text>
</View>
```
Warns user they won't get logged out — `updateUser({ password })` preserves the current session.

---

## Privacy Policy (`/settings/privacy.tsx`)

**Read-only display screen.** Renders static content with sections:

| Section | Key Content |
|---------|-------------|
| RA 10173 (Data Privacy Act) | Transparency, legitimate purpose, proportionality |
| Children's Data Protection | Minors as sensitive personal information |
| Secure-by-Design | E2E encryption, RLS, JWT, no third-party sharing |
| User Rights | Access, correction, erasure, portability, objection, NPC complaint |

No state, no API calls, no forms. Static compliance display.

---

## Help & FAQ (`/settings/help.tsx`)

### Data Architecture
All FAQ content is **hardcoded** in `FAQ_ITEMS` array (lines 23–366). No API, no CMS.

### Categories
`['Tracking', 'Screen Time', 'Sleep', 'Nutrition', 'Physical Activity', 'Growth', 'AI Features', 'Behavior', 'Philippine Context', 'Digital Parenting']`

### FAQ Item Structure
```ts
interface FAQItem {
  id: string;
  category: string;
  question: string;
  answer: string;        // multi-paragraph with citations
  citations: string[];    // formatted academic references
  icon: Ionicons key;
}
```

### Research Stats Banner (lines 397–405)
```js
RESEARCH_STATS = [
  { label: 'Studies Cited', value: '40+' },
  { label: 'Guidelines', value: 'WHO · AAP · CDC' },
  { label: 'Countries', value: 'Global + PH' },
]
```

### Expand/Collapse Logic (lines 376–378)
```ts
toggle(id) → setExpandedId(id === expandedId ? null : id)
// One item open at a time
```

### Category Filter (lines 380–382)
```ts
activeCategory: string | null  // null = show all
filtered = activeCategory ? FAQ_ITEMS.filter(...) : FAQ_ITEMS
```

### Citations Box (lines 469–479)
Rendered only when item is expanded. Shows numbered sources in a purple-tinted box (`#F5F3FF`).

---

## Child Settings (`/settings/child/[id].tsx`)

### Most Complex Settings Screen

This is the **per-child configuration hub**. Route param `id` identifies which child.

### State Groups

**Profile (lines 89–94):**
`name`, `dob` (Date | null), `avatarUrl`, `selectedIcon` (emoji), `showIconPicker`, `uploading`

**Body (lines 97–100):**
`gender` ('male'|'female'|null), `height`, `weight`, `bmiResult` (live computed)

**Routines — 9 time fields (lines 103–111):**
Each split into H/M/P (hour string, minute string, AM/PM):
`bedH/M/P`, `wakeH/M/P`, `bfH/M/P` (breakfast), `luH/M/P` (lunch), `snH/M/P` (snack), `diH/M/P` (dinner), `napH/M/P`, `actH/M/P`, `lrnH/M/P`

**Notifications (lines 114–116):**
```ts
notifToggles: Record<string, boolean>  // 10 keys, all default true
```

### Data Loading (lines 129–171)

**`loadChildren()` on mount** (lines 130–137):
```
useEffect → loadChildren() → setLoadingData(false)
```
Ensures latest child data before populating form.

**Populate form from child** (lines 140–171):
```ts
setName(child.name)
setAvatarUrl(child.avatar_url || '')
setDob(new Date(child.date_of_birth + 'T00:00:00'))  // date fix
setGender(child.gender)
setHeight(String(child.height_cm))
setWeight(String(child.weight_kg))
// Each time field split into H/M/P via fromTimeStr()
```

### Live BMI Preview (lines 173–191)
```ts
ageMonths = dob ? getAgeMonths(formatDateLocal(dob)) : 0
// Guard: age must be 24-60 months (2-5 years)
assessBmi(height, weight, ageMonths, gender) → BmiResult
```
Updates on every height/weight/gender/dob change. Only available for ages 2–5 (the WHO BMI-for-age reference range).

### Save Flow (lines 224–302)

**Step 1:** `updateChildSettings(child.id, { name, date_of_birth, avatar_url, notifications })`

**Step 2:** Compute BMI if `ageMonths >= 24 && ageMonths <= 60 && height && weight && gender`

**Step 3:** `updateChildRoutine(child.id, routine)` with all 9 times + height/weight/gender/bmi

**Step 4:** `scheduleChildNotifications(updatedChild, notifToggles)` — reschedules all notifs based on toggles

**Step 5:** `loadChildren()` to refresh store

### Time Input System

**Quick Pick Chips** (lines 336–344):
```ts
QUICK_TIMES = {
  bedtime: [{h:'7', m:'30', p:'PM'}, {h:'8', m:'00', p:'PM'}, ...],
  wake: [...], breakfast: [...], lunch: [...], snack: [...],
  dinner: [...], nap: [...], activity: [...], learn: [...]
}
```
Tap a chip → auto-fills H/M/P. Highlights currently selected time.

**Manual Input** (lines 346–367):
- H: 2-digit number pad input, maxLength 2, strips non-digits
- M: same
- AM/PM: toggle buttons

**`toTimeStr`** (lines 51–56): converts H/M/P → `"HH:MM:SS"` (24-hour format for DB)
```ts
if (p === 'PM' && hour !== 12) hour += 12
if (p === 'AM' && hour === 12) hour = 0
return `${hour}:${m}:00`
```

**`fromTimeStr`** (lines 58–67): converts `"HH:MM:SS"` → `{h, m, p}` for display

### Notification Toggles (lines 602–615)
10 notification types each with colored icon + toggle switch:
`bedtime`, `wake_up`, `breakfast`, `lunch`, `snack`, `dinner`, `nap`, `activity`, `learn`, `weekly_growth`

### Delete Flow (lines 304–316, 658–697)
```ts
handleDelete() → deleteChild(child.id) → loadChildren() → router.replace('/(tabs)/profile')
```
Modal warns: **"All activity records will remain, but profile and reminders will be removed."** This is correct — `deleteChild` likely only deletes the child profile record, not the activity history (preserving data integrity).

### Rules of Hooks Compliance
Lines 80–125 declare ALL hooks before line 126. The early `if (!child)` return at line 198 is **after** all hooks — correct.

---

## Key Design Patterns Across Settings

1. **Success timeout**: `setTimeout(() => router.back(), 2000)` after save success — gives user time to read confirmation
2. **Error dismissal**: Every error banner has an X button to close it
3. **Loading guards**: `disabled={saving}` on save buttons prevents double-submit
4. **Consistent header**: Back button + title + Save button (or spacer) across all settings screens
5. **Supabase RLS**: All settings changes go through RLS-protected database operations — user can only modify their own data