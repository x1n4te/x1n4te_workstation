---
id: keycloak-fastapi-security-wims-bfp-concept-001
type: concept
created: 2026-04-08
updated: 2026-04-10
last_verified: 2026-04-10
review_after: 2026-05-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - sources/software-dev/keycloak-production-security
  - sources/software-dev/fastapi-keycloak-jwt-rbac
  - sources/cybersecurity/keycloak-cves-2026
  - concepts/postgresql-security-wims-bfp
  - concepts/zero-trust-architecture
  - concepts/docker-security-wims-bfp
status: active
tags:
  - keycloak
  - fastapi
  - jwt
  - rbac
  - authentication
  - wims-bfp
  - security
  - software-dev
related:
  - sources/software-dev/keycloak-production-security
  - sources/software-dev/fastapi-keycloak-jwt-rbac
  - sources/cybersecurity/keycloak-cves-2026
  - concepts/postgresql-security-wims-bfp
  - concepts/docker-security-wims-bfp
  - concepts/secure-coding-practices
  - concepts/zero-trust-architecture
  - mocs/cybersecurity
---

# Keycloak + FastAPI Security for WIMS-BFP

**Synthesis of:** Keycloak hardening, FastAPI JWT RBAC, PostgreSQL RLS, Zero Trust Architecture
**Purpose:** Unified auth security reference for WIMS-BFP's authentication and authorization layer

---

# Keycloak Security — Detailed Reference

Back to overview: [[concepts/keycloak-fastapi-security-wims-bfp]]
## Keycloak Security Configuration

### Master Realm (Admin)

| Setting | Value |
|---|---|
| MFA | TOTP required |
| Password Policy | 12+ chars, special, digits, uppercase |
| Brute Force | 5 failures → 15min lockout |
| Admin IP | localhost + VPN only |
| Session Idle | 30 minutes |
| Session Max | 8 hours |

### Application Realm (WIMS)

| Setting | Value |
|---|---|
| MFA | TOTP required for all users |
| Password Policy | 12+ chars, special, digits, uppercase |
| Brute Force | 10 failures → 30min lockout |
| Token TTL | 10 minutes |
| Refresh Token | Single-use |
| Client Type | Confidential |

---

## FastAPI JWT Validation (5 Checks)

```python
# ALL 5 checks are mandatory — skip none
jwt.decode(
    token,
    signing_key,
    algorithms=["RS256"],
    audience="wims-bfp-backend",     # ← aud
    issuer=ISSUER_URL,               # ← iss
    options={
        "verify_signature": True,    # ← sig
        "verify_aud": True,          # ← aud
        "verify_exp": True,          # ← exp
        "verify_iss": True,          # ← iss
    },
)
# kid is checked implicitly by PyJWKClient
```

---

## RLS Context Wiring

```python
# Every request MUST execute this before any query:
cursor.execute("SET LOCAL wims.current_user_id = %s", (user.user_id,))
cursor.execute("SET LOCAL wims.current_role = %s", (user.role.value,))
if user.region:
    cursor.execute("SET LOCAL wims.current_region = %s", (user.region,))
```

---

## Complete Auth Audit Checklist

### Keycloak Configuration
```
[ ] Master realm: MFA ON, brute force ON, admin IP restricted
[ ] Application realm: MFA ON, password policy enforced
[ ] FRS roles: exactly 5, created as realm roles
[ ] Client scopes: wims:read, wims:write, wims:admin
[ ] Token lifespan: 10 minutes (not default 1 hour)
[ ] Refresh tokens: single-use
[ ] Brute force: 5-10 failures → temporary lockout
[ ] SMTP configured for login alerts
[ ] Admin events enabled, login events enabled
```

### FastAPI Implementation
```
[ ] JWT validation: all 5 checks (kid, iss, aud, sig, exp)
[ ] get_current_wims_user: resolve user, attach to request.state
[ ] require_role: enforce FRS role literals exactly
[ ] get_db: SET LOCAL wims.current_user_id in every transaction
[ ] National Analyst: read-only enforcement (no write endpoints)
[ ] Civilian Reporter: DMZ-only (no internal table access)
[ ] No hardcoded secrets (client secret in secrets file)
[ ] CORS: frontend origin only
[ ] Rate limiting: all endpoints
[ ] Pydantic validation: all external input
```

### PostgreSQL
```
[ ] RLS enabled on all wims.* tables
[ ] FORCE ROW LEVEL SECURITY set
[ ] Policies use OR logic (not multiple AND policies)
[ ] NULL checks in RLS predicates
[ ] Indexes on RLS predicate columns
[ ] Child tables have independent policies
```

### Docker
```
[ ] Keycloak container: non-root, read-only, no-new-privileges
[ ] Network isolation: Keycloak can't reach internet directly
[ ] Database: TLS connection, no port published to host
[ ] Secrets via files, not env vars
```

### CVEs
```
[ ] Keycloak patched: CVE-2026-1529, CVE-2026-4366, CVE-2026-4634
[ ] PostgreSQL patched: CVE-2025-1094, CVE-2025-8714
[ ] runc patched: CVE-2025-31133, CVE-2025-52565, CVE-2025-52881
```

---

## Key Findings from Auth Loop Fix (2026-04-09)

### KEYCLOAK_ISSUER vs KEYCLOAK_REALM_URL

Backend uses two separate URLs:
- `KEYCLOAK_REALM_URL=http://keycloak:8080/auth/realms/bfp` — for JWKS fetching (Docker internal network)
- `KEYCLOAK_ISSUER=http://localhost/auth/realms/bfp` — for JWT `iss` claim validation (browser-visible)

**Why:** Keycloak's `KC_HOSTNAME=localhost` means tokens have `iss: http://localhost/auth/realms/bfp`. But backend can't reach `localhost:8080` from inside Docker (port mapping is host→container only). Split config solves this.

### Audience Mapper (oidc-audience-mapper)

wims-web client needs an audience mapper to put `aud: "wims-web"` in access tokens. Without it, tokens have no audience or wrong audience → "Invalid audience" error.

**Must be in bfp-realm.json** — if added via admin API only, lost on container recreation.

### Realm JSON Persistence

Keycloak uses `--import-realm` with `IGNORE_EXISTING` strategy. Once realm exists, JSON is NOT re-imported. All config (roles, mappers, users) must be in `bfp-realm.json` at first boot.

**What's persisted now:**
- 5 custom realm roles (REGIONAL_ENCODER, SYSTEM_ADMIN, VALIDATOR, ANALYST, NATIONAL_ANALYST)
- Audience mapper on wims-web
- 5 test users (password set via `scripts/seed-dev-users.sh`)

**What still needs scripts:** PostgreSQL user sync (`seed-dev-users.sh`) — realm JSON creates users in Keycloak but doesn't link UUIDs to `wims.users` table.

### MFA Status

TOTP-based MFA is available via self-service enrollment (account page) or manual admin enrollment. `CONFIGURE_TOTP` forced enrollment is BROKEN in Keycloak 24.0.0 — see [[concepts/keycloak-mfa-findings]] for full analysis.

## Related

- [[sources/software-dev/keycloak-production-security]] — Keycloak hardening guide
- [[sources/software-dev/fastapi-keycloak-jwt-rbac]] — FastAPI + Keycloak JWT implementation
- [[sources/cybersecurity/keycloak-cves-2026]] — Keycloak CVEs
- [[concepts/postgresql-security-wims-bfp]] — PostgreSQL RLS security
- [[concepts/docker-security-wims-bfp]] — Docker container security
- [[concepts/secure-coding-practices]] — OWASP/CWE coding standards
- [[concepts/zero-trust-architecture]] — ZTA framework
- [[mocs/cybersecurity]] — Cybersecurity Map of Content
