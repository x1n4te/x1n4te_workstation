# Authentication Flow

The app uses **Supabase Auth** with email and password. This page explains how login, signup, and session management work.

---

## Login

1. Enter your email and password on the login screen.
2. Tap **Login**.
3. The app validates that both fields are filled.
4. It calls Supabase Auth to verify credentials.
5. On success, a **"Welcome back!"** animation plays.
6. After the animation, the root layout detects the active session and redirects to the Dashboard.

**Error messages:**
- Wrong password → "Invalid email or password"
- Unconfirmed email → "Please confirm your email"
- Network issue → "Network error — check your connection"

---

## Signup

1. Enter your **name**, **email**, **password**, and **confirm password**.
2. The app validates:
   - Name is required
   - Email format is valid
   - Password is at least 6 characters
   - Passwords match
3. Validation errors appear inline under each field.
4. On submit, the app creates the account.
5. A success screen replaces the form: "Account Created."
6. After 2.5 seconds, you are redirected to the login screen.

> **Important:** After signup, you are **not** automatically logged in. You must confirm your email first, then log in manually.

---

## Session Management

- Sessions are handled by Supabase Auth and stored securely.
- The app checks for an existing session on launch.
- If a session exists, you go straight to the Dashboard.
- If not, you see the login screen.

---

## The Loading Overlay

While the app checks your session on startup, a full-screen overlay appears with:
- A coral spinner
- The text "Smart Parenting"

If you're logged in but land on an auth screen (like after reinstalling the app), the overlay changes to "Setting things up…" for 1.8 seconds while the app prepares the main tabs.

This overlay sits above everything (z-index: 999) so you never see half-loaded screens.

---

## Sign Out

1. Go to Settings and tap **Sign Out**.
2. A confirmation modal appears.
3. A "Goodbye" animation plays for 1.2 seconds.
4. The session is cleared and you return to the login screen.

---

## Changing Credentials

**Email:**
- Requires your current password for security.
- A confirmation email is sent to the new address.
- You must click the link to complete the change.

**Password:**
- Requires your current password.
- New password must be at least 6 characters.
- You stay logged in on the current device.

---

## Deep Links

The app handles notification deep links:
- When you tap a notification, the app opens.
- It polls for auth readiness (up to 1 second).
- Once ready, it routes to the appropriate tab based on the notification type.
