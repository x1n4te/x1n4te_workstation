---
id: keycloak-authentication-flows-001
type: concept
created: 2026-04-17
updated: 2026-04-17
last_verified: 2026-04-17
review_after: 2026-07-17
stale_after: 2026-10-17
confidence: high
source_refs:
  - https://www.keycloak.org/docs/latest/server_admin/index.html#_authentication-flows
  - https://docs.redhat.com/en/documentation/red_hat_build_of_keycloak/26.0/html/server_developer_guide/admin_rest_api
status: active
tags:
  - keycloak
  - authentication
  - mfa
  - security
related:
  - concepts/keycloak-mfa-findings
  - concepts/keycloak-fastapi-security-wims-bfp
  - analyses/keycloak-mfa-pkce-debugging
  - concepts/keycloak-26-upgrading-guide
  - concepts/keycloak-forgot-password-test
---

# Keycloak Authentication Flows

Official Keycloak documentation on how authentication flows, executions, and conditional logic work. Critical for understanding the `browser` vs `browser-with-mfa` flow configuration in WIMS-BFP.

---

## What is an Authentication Flow?

An authentication flow is a container for an ordered list of executions. Each execution is a single action or check during the authentication process. Flows can be nested (a flow can contain sub-flows).

**Key properties:**
- **Alias** — unique name of the flow (e.g., `browser`, `forms`)
- **Top-level** — whether the flow can be bound as a realm's browser/registration/direct-grant flow
- **Provider ID** — `basic-flow` for standard flows

---

## Execution Requirements

Each execution in a flow has a **requirement** setting:

| Requirement | Meaning |
|-------------|---------|
| **REQUIRED** | Must succeed for the overall flow to succeed |
| **ALTERNATIVE** | At least one ALTERNATIVE in a sub-flow must succeed |
| **CONDITIONAL** | Only executed if conditions evaluate to true |
| **DISABLED** | Not executed |

**Key rule:** In a sub-flow with multiple ALTERNATIVE executions, only ONE needs to succeed. In a sub-flow with REQUIRED, ALL must succeed.

---

## Default Browser Flow (Keycloak 24+)

The standard `browser` flow structure:

```
browser (topLevel=True, basic-flow)
├── auth-cookie (ALTERNATIVE)                    ← priority 10
│   └── Returns success if valid session cookie exists
├── auth-spnego (DISABLED)                       ← priority 20
│   └── Kerberos/SPNEGO (disabled by default)
├── identity-provider-redirector (ALTERNATIVE)   ← priority 25
│   └── Redirects to configured IdP if present
└── forms (ALTERNATIVE, sub-flow)                ← priority 30
    ├── auth-username-password-form (REQUIRED)   ← priority 10
    │   └── Shows username/password form
    └── Browser - Conditional OTP (REQUIRED, sub-flow) ← priority 20
        ├── conditional-user-configured (ALTERNATIVE) ← priority 10
        │   └── Checks if user has OTP credential configured
        ├── conditional-user-role (ALTERNATIVE)        ← priority 20
        │   └── Condition based on user role
        ├── conditional-user-role (ALTERNATIVE)        ← priority 30
        │   └── Condition based on user role
        └── auth-otp-form (REQUIRED)                   ← priority 40
            └── Shows OTP input form
```

**Critical insight:** The default `browser` flow ALREADY includes MFA via the `Browser - Conditional OTP` sub-flow. The `conditional-user-configured` authenticator gates OTP — it only triggers if the user has TOTP configured. Users without TOTP never see the OTP form.

---

## Why `browser-with-mfa` is Problematic

If `browser-with-mfa` is set as `browserFlow` in `bfp-realm.json` but NO authentication flow with alias `browser-with-mfa` exists in the realm:

1. **Keycloak cannot resolve the flow reference** at startup
2. **Behavior varies by version:**
   - Some versions fall back to `browser` silently
   - Some versions throw an error
   - Some versions enter a redirect loop (auth → look up flow → fail → redirect → repeat)

**WIMS-BFP finding:** On Windows, `browser-with-mfa` (undefined flow) caused a redirect loop. Changing to `browser` (standard flow) fixed the loop while preserving MFA enforcement through the nested `Browser - Conditional OTP` sub-flow.

---

## Creating Custom Auth Flows

To create a custom flow that explicitly adds MFA:

1. **Copy the default browser flow** in Admin Console → Authentication → Browser flow → Actions → Copy
2. **Name it** `browser-with-mfa` (or any alias)
3. **Add executions** under the `forms` sub-flow:
   - `OTP Form` — set to REQUIRED (always show OTP) or CONDITIONAL
4. **Set as realm browser flow:** Realm Settings → Authentication → Browser Flow → select your custom flow

### Via Admin REST API:

```bash
# Get admin token
TOKEN=$(curl -s -X POST \
  "http://keycloak:8080/realms/bfp/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "grant_type=client_credentials" \
  --data-urlencode "client_id=wims-admin-service" \
  --data-urlencode "client_secret=$CLIENT_SECRET" | jq -r '.access_token')

# List flows
curl -s -H "Authorization: Bearer $TOKEN" \
  "http://keycloak:8080/admin/realms/bfp/authentication/flows" | jq '.[].alias'

# Create a copy of browser flow
curl -s -X POST \
  "http://keycloak:8080/admin/realms/bfp/authentication/flows/browser/copy" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"newName": "browser-with-mfa"}'
```

---

## Realm Configuration: `browserFlow` Field

In `bfp-realm.json`:

```json
{
  "browserFlow": "browser"
}
```

- Must match the `alias` of a **top-level** flow defined in `authenticationFlows`
- The `browser` flow is always present (default Keycloak flow)
- Custom flows must be explicitly defined in the realm JSON or created via API

---

## Conditional OTP Sub-Flow Details

### `conditional-user-configured`
- Authenticator: `conditional-user-configured`
- Checks if the user has an OTP credential registered
- If YES → proceeds to OTP form
- If NO → skips OTP step
- This is why MFA works "on by default" for configured users

### `conditional-user-role`
- Authenticator: `conditional-user-role`
- Can enforce OTP only for specific roles
- WIMS-BFP: Could use this to require MFA for `SYSTEM_ADMIN` and `NATIONAL_VALIDATOR` but not `CIVILIAN_REPORTER`

### `auth-otp-form`
- Authenticator: `auth-otp-form`
- Renders the OTP input page
- Uses template: `login-config-totp.ftl` (if TOTP not configured) or `login-otp.ftl` (if configured)

---

## Recovery Authentication Codes (Keycloak 26.3+)

New 2FA recovery feature:
- Users can generate backup codes via Account Console → Account Security → Signing in
- Recovery codes are an ALTERNATIVE to OTP in the `Browser - Conditional OTP` sub-flow
- Admin enables by setting `Recovery Authentication Code Form` to *Alternative*
- Available in realm JSON under `authenticationFlows` with `Recovery Authentication Code Form` execution

**WIMS-BFP consideration:** Enable recovery codes as backup for users who lose their OTP device.

---

## Troubleshooting Common Flow Issues

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Redirect loop after login | `browserFlow` points to non-existent flow | Set to `"browser"` or create the custom flow |
| MFA not showing | No OTP credential on user | Force `CONFIGURE_TOTP` required action |
| MFA always showing | OTP Form set to REQUIRED (not CONDITIONAL) | Set to CONDITIONAL with `conditional-user-configured` |
| Windows-specific loop | Platform-specific redirect handling + broken flow ref | Use standard `browser` flow |
| "Flow not found" error | `browserFlow` alias doesn't match any flow alias | Check `authenticationFlows` in realm JSON |

---

*Source: Official Keycloak Server Administration Guide (latest)*
*Extracted: 2026-04-17*
