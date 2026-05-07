## Login Screen (`login.tsx`)

**Purpose:** Authenticate existing users.

**State:**

| State | Type | Purpose |
|-------|------|---------|
| `email` | `string` | Email input |
| `password` | `string` | Password input |
| `showPassword` | `boolean` | Toggle password visibility |
| `loading` | `boolean` | Spinner in button |
| `error` | `string` | Banner error message |
| `showWelcome` | `boolean` | Triggers welcome overlay |
| `welcomeOpacity` | `Animated.Value` | Fade animation ref |
| `welcomeScale` | `Animated.Value` | Spring scale ref |

**Flow:**
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

**Redirect mechanism:** The auth guard in `_layout.tsx` (not this screen) watches the auth session and redirects to `/(tabs)` once the session is active. The welcome animation gives the guard time to initialize.

**Error categories (line 56-63):**
- Invalid credentials → "Invalid email or password"
- Email not confirmed → "Please confirm your email"
- Network → "Network error — check your connection"
- Catch-all → raw Supabase message

**Sign Up link:** `router.push('/(auth)/signup')` — pushes onto history stack (can go back).

---

## Signup Screen (`signup.tsx`)

**Purpose:** Register new parent accounts.

**State:**

| State | Type | Purpose |
|-------|------|---------|
| `name` | `string` | Full name input |
| `email` | `string` | Email input |
| `password` | `string` | Password input |
| `confirmPassword` | `string` | Password confirmation |
| `showPassword` | `boolean` | Toggle password visibility |
| `showConfirm` | `boolean` | Toggle confirm visibility |
| `loading` | `boolean` | Spinner in button |
| `errors` | `FieldError[]` | Per-field error objects |
| `success` | `boolean` | Triggers success component swap |

**Flow:**
```
User fills form → taps Sign Up
  → validate() runs all field checks
    → fail: setErrors([{ field, message }]) — per-field inline errors
    → pass: setLoading(true), call signUp(email, password, name)
      → fail: categorize Supabase error (already registered, password policy, network)
      → pass: setSuccess(true)
          → Component SWAPS entire form for success UI (checkmark + message)
          → After 2500ms: router.replace('/(auth)/login')
```

**Validation (per-field, on change and on submit):**
- `name`: required
- `email`: required + regex format check
- `password`: required + min 6 chars + strength indicator (6/8/10 char bars)
- `confirmPassword`: required + must match password + "Passwords match" green indicator

**Success state:** Not an overlay — entire form is replaced by a `success` component (lines 86-98). Shows checkmark icon + "Account Created" + "You can now sign in with your credentials."

**Sign In link (line 291):** `router.back()` — goes to previous screen. More fragile than `router.replace` since it depends on navigation history.

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
| **Sign In/Up link** | `router.push` (can go back) | `router.back()` (depends on history) |

Both are intentionally different patterns — login uses overlay animation (short delay, auth guard handles routing), while signup uses component swap with longer delay (user needs to read confirmation before going to login).