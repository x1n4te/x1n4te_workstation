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

# FastAPI Security — Detailed Reference

Back to overview: [[concepts/fastapi-security-wims-bfp]]
## Complete WIMS-BFP Backend Security Checklist

### FastAPI
```
[ ] JWT validation: 5 checks (kid, iss, aud, sig, exp)
[ ] FRS role enforcement: require_role on all protected endpoints
[ ] RLS context: SET LOCAL in every transaction
[ ] Pydantic: all inputs validated with strict models
[ ] Rate limiting: 100/min read, 10/min write, 5/min auth
[ ] CORS: wims-bfp.example.com only
[ ] Security headers: HSTS, CSP, nosniff, DENY, referrer-policy
[ ] Debug: disabled in production
[ ] API docs: hidden or auth-gated
[ ] Error responses: no stack traces
[ ] Max body size: 1MB
[ ] HTTPS only: no HTTP
[ ] BOLA prevention: ownership checks + RLS
```

### Celery
```
[ ] JSON serializer only (no pickle)
[ ] Time limits: soft 240s, hard 300s globally
[ ] max_memory_per_child: 200MB
[ ] max_tasks_per_child: 1000
[ ] Result expiry: 24 hours
[ ] Beat on trusted host only
[ ] Suricata task: svc_suricata account, 10s interval
```

### Redis
```
[ ] requirepass enabled
[ ] TLS connection (rediss://)
[ ] Internal network only (no ports published)
[ ] Dangerous commands renamed: FLUSHALL, FLUSHDB, DEBUG
[ ] maxmemory configured
[ ] maxmemory-policy: allkeys-lru
```

### PostgreSQL (linked)
```
[ ] See concepts/postgresql-security-wims-bfp for full checklist
```

### Docker (linked)
```
[ ] See concepts/docker-security-wims-bfp for full checklist
```

### CVEs
```
[ ] python-multipart ≥0.0.20 (CVE-2026-24486 ReDoS)
[ ] fastapi-users ≥15.0.2 (CVE-2025-68481 OAuth injection)
[ ] fastapi-guard ≥2.0.0 (CVE-2025-46814 header spoofing)
[ ] PostgreSQL patched (CVE-2025-1094, CVE-2025-8714)
[ ] Keycloak patched (CVE-2026-1529, CVE-2026-4366, CVE-2026-4634)
[ ] runc patched (CVE-2025-31133, CVE-2025-52565, CVE-2025-52881)
```

---

## Related

- [[concepts/keycloak-fastapi-security-wims-bfp]] — Auth layer (Keycloak + JWT)
- [[concepts/postgresql-security-wims-bfp]] — Database layer (RLS + CVEs)
- [[concepts/docker-security-wims-bfp]] — Container layer (Compose + runc)
- [[concepts/secure-coding-practices]] — OWASP/CWE standards
- [[concepts/zero-trust-architecture]] — ZTA framework
- [[sources/software-dev/fastapi-security-best-practices]] — FastAPI security reference
- [[sources/software-dev/fastapi-cves-2025-2026]] — FastAPI CVEs
- [[sources/software-dev/celery-redis-security]] — Celery + Redis security
- [[mocs/cybersecurity]] — Cybersecurity Map of Content
