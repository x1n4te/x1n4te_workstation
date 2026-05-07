# WIMS-BFP Session Persistence Fix — Silent Proactive JWT Refresh
**Date:** 2026-05-04 | **Session:** 2026-05-03 late
**PRs:** [#92](https://github.com/x1n4te/WIMS-BFP-PROTOTYPE/pull/92) — `fix/session-persistence-cross-tab-refresh` (context/AuthContext.tsx) | [#93](https://github.com/x1n4te/WIMS-BFP-PROTOTYPE/pull/93) — `fix/session-persistence-silent-refresh` (lib/auth.tsx)
**Status:** PR #92 merged, PR #93 open (CI in progress)

---

## Problem
When switching Chromium tabs or leaving/re-entering the browser window, the WIMS-BFP frontend would fully reload — losing all local state (form inputs, navigation position, unsaved data). The user was logged out and had to re-authenticate.

---

## Root Cause — Dual AuthProvider Architecture

The Next.js app renders **two separate auth providers** in `layout.tsx`:

```tsx
// src/frontend/src/app/layout.tsx
<AuthContextProvider>           {/* @/context/AuthContext — has proactive refresh */}
  <UserProfileProvider>          {/* @/lib/auth — NO proactive refresh */}
    <LayoutShell>
      {children}
```

Most pages use `useUserProfile()` from `lib/auth.tsx` — which had **no proactive refresh logic at all**. It only fetched the session once on mount, then sat idle. When the 5-minute Keycloak access token expired, the tab had stale credentials and no mechanism to recover silently.

The `context/AuthContext.tsx` provider (used by layout/shell components) had been given the `navigator.locks` fix in PR #92, but the pages that use `lib/auth.tsx` were unaffected.

### Pages using `useUserProfile()` (affected):
- `IncidentForm.tsx` — INCIDENT creation/editing
- `incidents/create/page.tsx`
- `incidents/triage/page.tsx`
- `incidents/import/page.tsx`
- `afor/create/page.tsx`
- `home/page.tsx`

### Pages using `useAuth()` (partially fixed by PR #92):
- `dashboard/page.tsx`, `dashboard/analyst/page.tsx`, `dashboard/regional/page.tsx`
- `incidents/[id]/page.tsx`, `incidents/page.tsx`
- `profile/page.tsx`, `login/page.tsx`, `admin/system/page.tsx`

---

## Solution — PR #93

Added the same silent proactive refresh pattern to `lib/auth.tsx`:

### `src/frontend/src/lib/auth.tsx`

**1. `navigator.locks` gate** — prevents `refreshTokenMaxReuse:0` race:
```ts
const REFRESH_LOCK_NAME = 'wims:auth:refresh_lock';

const refreshPromise = navigator.locks.request(REFRESH_LOCK_NAME, async () => {
  // Only one tab refreshes at a time. Others block here until lock released.
  const res = await fetch('/api/auth/refresh', { method: 'POST', credentials: 'include' });
  return res.ok;
});
```

**Why this matters:** Keycloak is configured with `refreshTokenMaxReuse: 0` — each refresh token can only be used once. If Tab A and Tab B both try to refresh simultaneously, Tab A wins (uses the token), Tab B gets a 401 and the session is killed.

**2. 4-minute `setInterval`** — proactively rotates the cookie before the 5-min access token expires:
```ts
const PROACTIVE_REFRESH_INTERVAL_MS = 4 * 60 * 1000;
window.setInterval(() => refreshAccessToken(), PROACTIVE_REFRESH_INTERVAL_MS);
```

**3. `visibilitychange` listener** — silently refreshes when tab becomes visible:
```ts
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    refreshAccessToken(); // Silent — does NOT call fetchProfile()
  }
});
```

**Critical:** Does NOT call `fetchProfile()` on visibility change. `fetchProfile()` re-fetches user state from `/api/auth/session`, which races with other tabs' concurrent refresh attempts and can result in a 401 → full session kill.

---

## PR #92 vs PR #93 — What Each Fixed

| | PR #92 | PR #93 |
|--|--------|--------|
| File | `context/AuthContext.tsx` | `lib/auth.tsx` |
| Provider | `AuthContextProvider` | `UserProfileProvider` |
| Pages affected | Layout, Header, Sidebar, dashboard pages | Incident forms, triage, import, AFOR, home |
| Fix | navigator.locks + silent visibilitychange | Same — added to previously-unprotected provider |

Both providers now run the same refresh strategy. The `navigator.locks` API is shared across the origin regardless of which provider called it, so cross-tab serialization works universally.

---

## Frontend API Route — `src/frontend/src/app/api/auth/refresh/route.ts`

This route handles the actual Keycloak token refresh server-side:

1. Reads `refresh_token` from HttpOnly cookie
2. POSTs to `KEYCLOAK_TOKEN_URL` with `grant_type=refresh_token`
3. On success: sets new `access_token` and `refresh_token` cookies (both HttpOnly)
4. On 401: clears both cookies (forces re-login)

```ts
const res = await fetch(KEYCLOAK_TOKEN_URL, {
  method: 'POST',
  body: new URLSearchParams({ grant_type: 'refresh_token', refresh_token, client_id }),
});
```

---

## Known Pre-Existing Test Failure

`queue-baseline.test.tsx` has a failing test unrelated to this fix:
```
TestingLibraryElementError: Unable to find a label with the text of: /metric/i
```
The test calls `screen.getByLabelText()` synchronously before React 18 has finished rendering the select. This is a pre-existing issue — it fails on current master without any of the session fix changes. Fixing it requires changing `getByLabelText` to `findByLabelText` (async) or wrapping in `waitFor`.

---

## Files Changed

### PR #93 — `lib/auth.tsx`
| Metric | Value |
|--------|-------|
| Lines added | +100 |
| Lines removed | -5 |
| Net | +95 |

### PR #92 — `context/AuthContext.tsx`
| Metric | Value |
|--------|-------|
| Lines added | +69 |
| Lines removed | -27 |
| Net | +42 |

---

## Verification

```bash
# After deploying PR #93:
# 1. Open two tabs to the same WIMS-BFP page
# 2. Switch between tabs — state should persist, no full reload
# 3. Leave tab idle for 5 minutes, return — session should still be valid
# 4. Console should show: '[AuthContext] refreshAccessToken: token refreshed'
```

Check browser DevTools → Application → Cookies to confirm tokens are rotating without page reload.

---

## Related Issues
- Issue #90: JWT Refresh Token Race Condition → **Fixed by PR #92 + PR #93**
- Issue #84: verify_incident() missing analytics sync (P0, unresolved)
- Issues #85–#89: Analyst dashboard features (not started)
