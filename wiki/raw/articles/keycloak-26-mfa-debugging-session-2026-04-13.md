# Keycloak 26 MFA + PKCE Debugging Session — 2026-04-13

## Session Summary
Debugged MFA login failure on WIMS-BFP. After TOTP code entry, Keycloak redirects to `/login` instead of `/callback`. Root cause not resolved.

## Investigation Steps
1. Checked callback page (`/app/callback/page.tsx`) — calls `signinCallback()` then `/api/auth/sync` — both exist and work
2. Checked OIDC config (`lib/oidc.ts`) — PKCE with `response_type: 'code'`, correct redirect_uri
3. Checked realm JSON flows — found `browser-with-mfa` missing from JSON (red herring: it's a custom flow in DB, not from export)
4. Found duplicate `forms` flow in realm JSON (broken, removed)
5. Checked Keycloak logs — `invalid_user_credentials` with `selected_credential_id` = OTP validation failing
6. Checked Docker time — synced (22s drift, within TOTP window)
7. Found missing `pkce.code.challenge.method: S256` on wims-web client — added to JSON
8. Provided Admin API curl to apply fix — user reported "still didn't work"

## Key Evidence
- Keycloak logs: `error="invalid_user_credentials", selected_credential_id="b26a2119-f724-4e15-9141-40cd62a2644a"` — OTP credential validation failing
- Same `code_id` across multiple attempts — auth flow restarting
- Flow structure verified correct: cookie (ALT) + idp-redirector (ALT) + username-password (REQ) + otp-form (REQ)
- OTP policy: totp, HmacSHA1, 6 digits, 30s period — correct

## Hypotheses
A. PKCE code_verifier lost across MFA redirect (sessionStorage cleared?)
B. Keycloak 26 PKCE + MFA compatibility bug
C. accessCodeLifespan (60s) too short — code expires during MFA entry
D. oidc-client-ts v3.5.0 + Keycloak 26 incompatibility
E. PKCE attribute not actually applied to running Keycloak instance

## Files Checked
- `src/frontend/src/app/callback/page.tsx` — callback handler
- `src/frontend/src/lib/oidc.ts` — OIDC config
- `src/frontend/src/context/AuthContext.tsx` — auth provider
- `src/frontend/src/app/api/auth/sync/route.ts` — sync proxy
- `src/keycloak/bfp-realm.json` — realm config
- Keycloak container logs via `docker compose logs keycloak`
