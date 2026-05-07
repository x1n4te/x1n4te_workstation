---
id: keycloak-forgot-password-test-001
type: concept
created: 2026-04-14
updated: 2026-04-14
last_verified: 2026-04-14
review_after: 2026-06-14
stale_after: 2026-10-14
confidence: high
source_refs:
  - sources/software-dev/keycloak-production-security
  - raw/articles/keycloak-26-mfa-debugging-session-2026-04-13.md
status: active
tags:
  - keycloak
  - auth
  - security
  - testing
  - wims-bfp
related:
  - concepts/keycloak-mfa-findings
  - analyses/keycloak-mfa-pkce-debugging
  - concepts/keycloak-fastapi-security-wims-bfp
---

# Keycloak Forgot Password Flow — Test Coverage & Configuration

**Date:** 2026-04-14
**Keycloak version:** 26.6.0
**Test file:** `src/backend/tests/integration/test_keycloak_password_reset.py`

---

## Overview

End-to-end test for the Keycloak "Forgot Password" flow: user clicks "Forgot Password?", receives a one-time token via email, clicks the link, sets a new password, and logs in.

---

## Keycloak Reset Credentials Flow

Keycloak 26.6.0 ships a built-in `reset credentials` flow with 3 REQUIRED executions:

```
reset credentials [built-in]
  1. reset-credentials-choose-user [REQUIRED]  — collects username/email
  2. reset-credential-email [REQUIRED]         — sends one-time token email
  3. reset-password [REQUIRED]                 — user enters new password
```

This flow is built-in and cannot be deleted, but SMTP and `resetPasswordAllowed` must be configured.

---

## Prerequisites

### 1. Enable `resetPasswordAllowed`

Without this, the "Forgot Password?" link won't appear on the login page.

```bash
# Via Admin API
curl -X PUT "http://localhost:8080/auth/admin/realms/bfp" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"resetPasswordAllowed": true}'
```

Or in `bfp-realm.json`:
```json
"resetPasswordAllowed": true
```

### 2. Configure SMTP

The `smtpServer` must be set for email delivery. For Docker dev, use MailHog:

```bash
# Via Admin API
curl -X PUT "http://localhost:8080/auth/admin/realms/bfp" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "smtpServer": {
      "host": "mailhog",
      "port": "1025",
      "from": "noreply@wims-bfp.local",
      "fromDisplayName": "WIMS-BFP",
      "starttls": "false",
      "auth": "false"
    }
  }'
```

### 3. Add MailHog to docker-compose.yml

```yaml
mailhog:
  image: mailhog/mailhog:latest
  container_name: wims-mailhog
  ports:
    - "1025:1025"   # SMTP
    - "8025:8025"   # Web UI
  networks:
    - wims_internal
```

---

## Test Structure

```
test_keycloak_password_reset.py
├── TestForgotPasswordConfiguration (pre-flight checks)
│   ├── test_reset_credentials_flow_exists
│   ├── test_reset_credentials_has_correct_executions
│   ├── test_realm_smtp_configured
│   ├── test_reset_password_allowed_in_realm
│   └── test_forgot_password_link_visible_on_login_page
└── TestForgotPasswordFlow (end-to-end)
    ├── test_reset_password_via_admin_api (baseline)
    ├── test_forgot_password_sends_reset_email
    ├── test_full_forgot_password_e2e
    ├── test_reset_token_is_one_time_use
    └── test_nonexistent_user_does_not_leak_information
```

---

## Security Considerations

### Token One-Time Use
The action token (`/login-actions/action-token?token=...`) must be consumed after use. Reusing the same link should fail with an error or redirect. Test: `test_reset_token_is_one_time_use`.

### User Enumeration Prevention
OWASP ASVS requires that forgot-password responses don't reveal whether a user exists. Keycloak shows the same "email sent" confirmation for both valid and invalid usernames. Test: `test_nonexistent_user_does_not_leak_information`.

### Email Link Security
- Token is a signed JWT with short expiry (configurable via `accessCodeLifespanUserAction`, default 5 minutes)
- Link uses HTTPS in production
- Token is bound to the client_id in the flow

---

## Key Lessons from [[concepts/keycloak-mfa-findings]]

1. **Keycloak 26 CONFIGURE_TOTP fix** — the same upgrade that fixed MFA required actions also ensures `reset credentials` works correctly
2. **Browser flow vs reset flow** — these are separate flows; MFA enforcement on the browser flow doesn't affect password reset
3. **Docker networking** — SMTP host must be reachable from the Keycloak container (use Docker service name, not `localhost`)

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| No "Forgot Password?" link | `resetPasswordAllowed: false` | Enable in realm config |
| Email never arrives | SMTP not configured or unreachable | Check `smtpServer` config, verify MailHog |
| Token link 404s | Wrong `frontendUrl` | Set `KC_HOSTNAME_STRICT_HTTP_HEADERS` or configure `frontendUrl` |
| Token expired | User took too long | Increase `accessCodeLifespanUserAction` |
| Form action URL fails | Keycloak rewrite rules | Check nginx proxy config |

---

## Related

- [[concepts/keycloak-mfa-findings]] — MFA setup and Keycloak 24→26 upgrade findings
- [[analyses/keycloak-mfa-pkce-debugging]] — Auth flow debugging session
- [[concepts/keycloak-fastapi-security-wims-bfp]] — Keycloak + FastAPI integration
