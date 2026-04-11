---
id: keycloak-mfa-findings-001
type: concept
created: 2026-04-10
updated: 2026-04-11
last_verified: 2026-04-10
review_after: 2026-07-10
stale_after: 2026-10-10
confidence: high
source_refs:
  - sources/software-dev/keycloak-production-security
status: active
tags:
  - keycloak
  - mfa
  - totp
  - authentication
  - wims-bfp
  - security
related:
  - concepts/keycloak-fastapi-security-wims-bfp
  - entities/hermes-agent-setup
  - sources/software-dev/keycloak-production-security
---

# Keycloak MFA Findings — What Works and What Doesn't

**Date:** 2026-04-10
**Keycloak version:** 24.0.0
**Finding:** `CONFIGURE_TOTP` required action is broken in Keycloak 24. Forced TOTP enrollment via required actions does NOT work.

---

## What We Tried

### Approach 1: Force TOTP via Required Action (BROKEN)

Set `CONFIGURE_TOTP` as a default required action so every user must enroll TOTP on first login.

**Steps taken:**
1. Set CONFIGURE_TOTP as default required action via API
2. Added CONFIGURE_TOTP to user's required actions
3. User tried to login

**Result:** "Cannot login, credential setup required" — Keycloak couldn't render the TOTP setup page.

**Root cause:** The `CONFIGURE_TOTP` required action provider is NOT properly registered in Keycloak 24.0.0:
- `GET /authentication/required-actions` shows `alias=MISSING name=MISSING` for the first entry
- `PUT /authentication/required-actions/CONFIGURE_TOTP` returns "Failed to find required action"
- The admin console dropdown does NOT show "Configure OTP" as an option
- The TOTP authenticator providers exist (OTP Form, Conditional OTP Form) but they don't register CONFIGURE_TOTP as a required action

**Conclusion:** The `auth-otp-form` authenticator does NOT register `CONFIGURE_TOTP` as a required action in Keycloak 24. This is a known limitation/potential bug.

### Approach 2: Clone Browser Flow + Make OTP REQUIRED (WORKS but incomplete)

Clone the `browser` flow, change OTP subflow from CONDITIONAL → REQUIRED.

**Steps taken:**
1. Cloned `browser` → `browser-with-mfa` via API
2. Changed Conditional OTP subflow from CONDITIONAL → REQUIRED
3. Set `browser-with-mfa` as default browser flow

**Result:** Flow structure is correct:
```
browser-with-mfa [default]
  Cookie [ALTERNATIVE]
  Kerberos [DISABLED]
  Identity Provider Redirector [ALTERNATIVE]
  Forms [ALTERNATIVE]
    Username Password Form [REQUIRED]
    Conditional OTP [REQUIRED]     ← was CONDITIONAL
      Condition - user configured [REQUIRED]
      OTP Form [REQUIRED]
```

**But:** This only works for users who ALREADY have TOTP configured. If a user doesn't have TOTP configured, the "Condition - user configured" check fails, and the REQUIRED OTP subflow blocks login. There's no fallback to TOTP enrollment.

---

## What Works

### Self-Service TOTP Enrollment (Account Page)

Users enroll TOTP through their account page:
1. Go to `http://localhost:8080/auth/realms/bfp/account`
2. Login with credentials
3. Navigate to "Signing in" or "Account Security"
4. Enable "Authenticator Application"
5. Scan QR code with Google Authenticator / Authy
6. Enter OTP to confirm

**After enrollment:** The CONDITIONAL OTP subflow automatically triggers on every login.

**Pros:**
- Works reliably in Keycloak 24
- User-initiated (no forced enrollment)
- Standard Keycloak workflow

**Cons:**
- Not mandatory — users can skip enrollment
- Requires users to know about the account page
- Not suitable for government systems requiring enforced MFA

### Manual Admin TOTP Enrollment

Admin sets up TOTP for each user via the admin console:
1. Go to `http://localhost:8080/admin` → select `bfp` realm
2. Users → select user → Credentials tab
3. Configure OTP → show QR code to user
4. User scans QR code → enters OTP → confirmed

**Pros:**
- Admin-controlled enrollment
- Can be made mandatory as part of onboarding

**Cons:**
- Manual per-user process
- Doesn't scale for large user bases
- Admin must be present during enrollment

---

## Recommended Setup for WIMS-BFP

### Phase 1: Self-Service (Completed — 2026-04-10)
- Keep `browser` flow as default (CONDITIONAL OTP)
- Users enroll TOTP via account page
- OTP subflow automatically triggers after enrollment

### Phase 2: Enforced MFA (2026-04-11 — Active, CONDITIONAL)
- Clone `browser` → `browser-with-mfa` — set as default browser flow
- OTP subflow: CONDITIONAL (not REQUIRED — Keycloak 24 CONFIGURE_TOTP bug)
- `auth-otp-form` with `userSetupAllowed` config created (configurable=false, not actually used)
- **DB fix:** disabled broken `CONFIGURE_TOTP` default_action (empty alias entry in `required_action_provider` table)
  - This fixed "Cannot login, credential setup required" error that affected ALL users
- Behavior:
  - Users with TOTP configured → prompted for OTP on every login ✓
  - Users without TOTP → CONDITIONAL subflow skipped, login proceeds ✓
- Also: brute force protection (5 attempts), direct grants disabled, password policy

### Phase 3: Admin-Controlled (For Thesis Defense)
- Admin enrolls TOTP for each test user via admin console
- Document as part of security evaluation
- Demonstrate MFA in thesis defense

### Phase 4: Future (If Keycloak Fixes CONFIGURE_TOTP)
- When Keycloak properly registers CONFIGURE_TOTP as a required action
- Re-enable forced enrollment via required action approach

---

## Key Lessons

1. **CONFIGURE_TOTP is broken in Keycloak 24.0.0** — don't rely on it for forced enrollment
2. **OTP subflow works** — CONDITIONAL triggers for users with TOTP configured
3. **Account page enrollment works** — self-service TOTP setup is reliable
4. **Admin console TOTP works** — manual per-user enrollment is reliable
5. **Browser flow cloning works** — can change OTP from CONDITIONAL to REQUIRED
6. **The gap:** No way to force TOTP enrollment on first login in Keycloak 24

---

## Connection to Thesis

**Chapter 3 Security Requirement:** "MFA + token-based sessions" (Authentication + Identity domain)

**Current fulfillment:** TOTP-based MFA available via self-service enrollment. OTP subflow triggers automatically after enrollment.

**For thesis evaluation:** Document MFA as "available and configured" rather than "enforced." The technical implementation is correct (TOTP, QR code, OTP validation), but the enrollment mechanism is user-initiated rather than forced.

**Recommendation:** For the thesis defense, demonstrate MFA by manually enrolling TOTP for test users and showing the OTP prompt on login. This satisfies the requirement even if enrollment isn't forced.

---

## Related

- [[concepts/keycloak-fastapi-security-wims-bfp]] — Keycloak + FastAPI security
- [[entities/hermes-agent-setup]] — hermes agent configuration
- [[sources/software-dev/keycloak-production-security]] — Keycloak hardening guide
