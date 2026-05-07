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
  - analyses/keycloak-mfa-pkce-debugging
---

# Keycloak + FastAPI Security for WIMS-BFP

**Synthesis of:** Keycloak hardening, FastAPI JWT RBAC, PostgreSQL RLS, Zero Trust Architecture
**Purpose:** Unified auth security reference for WIMS-BFP's authentication and authorization layer

---

## Auth Flow (WIMS-BFP)

```
User → Keycloak (authenticate, MFA)
  → JWT token (RS256, 10min TTL)
    → FastAPI endpoint
      → validate_token() — 5 checks (kid, iss, aud, sig, exp)
      → get_current_wims_user() — resolve user from JWT
      → require_role() — check FRS role
      → get_db() — SET LOCAL wims.current_user_id + role + region
      → RLS policy evaluates — per-user/region access control
      → Query executes — data filtered by RLS
```

---

## ZTA Mapping

| Component | ZTA Tenet | Implementation |
|---|---|---|
| Keycloak MFA | Tenet 6: Dynamic auth | TOTP required for all users |
| JWT 5-check validation | Tenet 4: Dynamic policy | kid, iss, aud, signature, expiry |
| FRS role enforcement | Tenet 3: Per-session access | require_role() on every endpoint |
| RLS context | Tenet 3: Per-session access | SET LOCAL wims.current_user_id |
| Token TTL 10min | Tenet 4: Dynamic policy | Short-lived credentials |
| Audit logging | Tenet 7: Improve posture | Login events, admin events, RLS denials |

---

## FRS Role Matrix

| Role | JWT Claim | API Access | RLS Scope | MFA | Description |
|---|---|---|---|---|---|
| CIVILIAN_REPORTER | realm_access.roles | DMZ only | None (air-locked) | Optional | External incident submission |
| REGIONAL_ENCODER | realm_access.roles | CRUD | Region-scoped | Required | Regional data entry |
| NATIONAL_VALIDATOR | realm_access.roles | CRUD | Region-scoped | Required | Regional validation |
| NATIONAL_ANALYST | realm_access.roles | Read-only | Global | Required | Analytics, reporting |
| SYSTEM_ADMIN | realm_access.roles | Full CRUD | Global | Required | Infrastructure management |

---

## Related Sections
*Detailed content split into sub-pages for readability. See [[concepts/keycloak-fastapi-security-wims-bfp-details]] for the full reference.*

---

*This page is scannable in 30 seconds. Full reference content moved to sub-pages.*
