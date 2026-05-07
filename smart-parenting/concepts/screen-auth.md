---
title: Login & Register Screens
created: 2026-04-25
updated: 2026-04-25
type: concept
tags: [screen, auth, ui-ux]
sources: [raw/technical-reference.md]
---

# Login & Register Screens

---

## Login Screen (`login.tsx`)

**Purpose:** Authenticate existing users.

### State
| State | Type | Purpose |
|-------|------|---------|
| `email` | `string` | Email input |
| `password` | `string` | Password input |
| `showPassword` | `boolean` | Toggle visibility |
| `loading` | `boolean` | Spinner in button |
| `error` | `string` | Banner error message |
| `showWelcome` | `boolean` | Triggers welcome overlay |
| `welcomeOpacity` / `welcomeScale` | `Animated.Value` | Fade + spring refs |

### Flow
```
User fills form → taps Login
  → validate: both fields non-empty
    → fail: setError('Please enter your email and password.')
    → pass: setLoading(true), call signIn()
      → fail: categorize error (invalid creds, email not confirmed, network)
      → pass: setShowWelcome(true)
          → Animated: opacity 0→1 (400ms) + scale 0.8→1 spring
          → After 1200ms: opacity 1→0 (300ms fade out)
          → Auth guard in _layout.tsx handles redirect to tabs
```

**Redirect mechanism:** The auth guard (see [[auth-loading-overlay]]) watches the auth session and redirects to `/(tabs)` once active. The welcome animation gives the guard time to initialize.

### Error Categories
- Invalid credentials → "Invalid email or password"
- Email not confirmed → "Please confirm your email"
- Network → "Network error — check your connection"
- Catch-all → raw Supabase message

---

## Signup Screen (`signup.tsx`)

**Purpose:** Register new parent accounts.

### State
| State | Type | Purpose |
|-------|------|---------|
| `name` | `string` | Full name input |
| `email` | `string` | Email input |
| `password` | `string` | Password input |
| `confirmPassword` | `string` | Password confirmation |
| `showPassword` / `showConfirm` | `boolean` | Toggle visibility |
| `loading` | `boolean` | Spinner in button |
| `errors` | `FieldError[]` | Per-field error objects |
| `success` | `boolean` | Triggers success component swap |

### Flow
```
User fills form → taps Sign Up
  → validate() runs all field checks
    → fail: setErrors([{ field, message }]) — per-field inline errors
    → pass: setLoading(true), call signUp(email, password, name)
      → fail: categorize Supabase error
      → pass: setSuccess(true)
          → Component SWAPS entire form for success UI
          → After 2500ms: router.replace('/(auth)/login')
```

### Validation (per-field, on change and on submit)
- `name`: required
- `email`: required + regex format check
- `password`: required + min 6 chars + strength indicator (6/8/10 char bars)
- `confirmPassword`: required + must match password + "Passwords match" green indicator

### Success State
Not an overlay — entire form is replaced by a `success` component. Shows checkmark icon + "Account Created" + "You can now sign in with your credentials."

---

## Key Differences

| Aspect | Login | Signup |
|--------|-------|--------|
| **Success feedback** | `Animated.View` overlay (fade + spring) | Component swap (entire form replaced) |
| **Animation duration** | ~1900ms total (400 + 1200 + 300) | 2500ms delay then redirect |
| **Error handling** | Single `error` string (banner) | `errors[]` array (per-field inline) |
| **Redirect after success** | Auth guard redirects to tabs | Manual `router.replace('/(auth)/login')` |
| **Password strength** | None | 3-bar strength indicator |
| **Confirm password** | None | Yes, with match indicator |

Both are intentionally different patterns — login uses overlay animation (short delay, auth guard handles routing), while signup uses component swap with longer delay (user needs to read confirmation before going to login). Auth state is managed via [[auth-loading-overlay]].
