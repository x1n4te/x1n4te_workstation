---
id: fastapi-security-wims-bfp-concept-001
type: concept
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - sources/software-dev/fastapi-security-best-practices
  - sources/software-dev/fastapi-cves-2025-2026
  - sources/software-dev/celery-redis-security
  - sources/software-dev/fastapi-keycloak-jwt-rbac
  - sources/software-dev/keycloak-production-security
  - concepts/postgresql-security-wims-bfp
  - concepts/docker-security-wims-bfp
  - concepts/zero-trust-architecture
status: active
tags:
  - fastapi
  - celery
  - redis
  - api-security
  - task-queue
  - wims-bfp
  - software-dev
related:
  - sources/software-dev/fastapi-security-best-practices
  - sources/software-dev/fastapi-cves-2025-2026
  - sources/software-dev/celery-redis-security
  - sources/software-dev/fastapi-keycloak-jwt-rbac
  - concepts/postgresql-security-wims-bfp
  - concepts/docker-security-wims-bfp
  - concepts/secure-coding-practices
  - concepts/zero-trust-architecture
  - mocs/cybersecurity
---

# FastAPI + Celery/Redis Security for WIMS-BFP

**Synthesis of:** FastAPI API security, Celery task queue, Redis broker, Keycloak JWT, PostgreSQL RLS
**Purpose:** Unified backend security reference for WIMS-BFP's API layer

---

## WIMS-BFP Backend Architecture

```
Internet → Next.js (PWA)
  → FastAPI (JWT validation, rate limiting, input validation)
    → PostgreSQL (RLS enforced per user_id/region/role)
    → Redis (TLS, password-protected)
      → Celery (JSON-only, time-limited tasks)
        → Suricata Eve ingestion (10s beat)
```

---

## ZTA Mapping

| Component | ZTA Tenet | Implementation |
|---|---|---|
| FastAPI JWT | Tenet 6: Dynamic auth | 5-check JWT validation |
| Rate limiting | Tenet 4: Dynamic policy | Per-endpoint limits |
| RLS context | Tenet 3: Per-session access | SET LOCAL wims.current_user_id |
| TLS everywhere | Tenet 2: Security regardless of network | HTTPS + Redis TLS |
| Security headers | Tenet 7: Improve posture | HSTS, CSP, nosniff |
| Audit logging | Tenet 7: Improve posture | Security event logging |

---

## Security Stack (Layered)

```
Layer 1: Transport Security
  - HTTPS (TLS 1.3)
  - Redis TLS (rediss://)
  - PostgreSQL TLS

Layer 2: Authentication
  - Keycloak JWT (RS256, 10min TTL)
  - MFA required for all users
  - 5-check validation (kid, iss, aud, sig, exp)

Layer 3: Authorization
  - FRS role enforcement (require_role dependency)
  - RLS per-user/region isolation
  - Object-level ownership checks (BOLA prevention)

Layer 4: Input Validation
  - Pydantic models on all route inputs
  - Field validators (length, pattern, sanitization)
  - Max request body size (1MB)

Layer 5: Rate Limiting
  - Read: 100 requests/minute
  - Write: 10 requests/minute
  - Auth: 5 requests/minute

Layer 6: Output Security
  - Security headers (HSTS, CSP, nosniff, DENY)
  - Error responses without stack traces
  - CORS: only wims-bfp.example.com

Layer 7: Task Security
  - Celery JSON-only serialization (no pickle)
  - Time limits on all tasks (soft + hard)
  - Worker resource limits (memory, max tasks)

Layer 8: Monitoring
  - Security event logging
  - Failed auth alerting
  - Rate limit breach alerting
```

---

## Related Sections
*Detailed content split into sub-pages for readability. See [[concepts/fastapi-security-wims-bfp-details]] for the full reference.*

---

*This page is scannable in 30 seconds. Full reference content moved to sub-pages.*
