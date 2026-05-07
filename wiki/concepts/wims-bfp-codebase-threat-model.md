---
id: wims-bfp-codebase-threat-model-001
type: concept
created: 2026-04-21
updated: 2026-04-21
last_verified: 2026-04-21
review_after: 2026-06-21
stale_after: 2026-10-21
confidence: high
source_refs:
  - raw/sources/wims-bfp-codebase/docs/SECURITY.md
status: active
tags:
  - wims-bfp
  - security
  - owasp
  - threat-model
related:
  - concepts/wims-bfp-codebase-auth-flow
  - concepts/wims-bfp-codebase-rls-model
  - entities/wims-bfp-codebase-rbac-roles
---

# Threat Model

OWASP-aligned threat assessment for WIMS-BFP. Defense-in-depth across all layers.

## STRIDE Mapping

| Threat | Category | Mitigation |
|--------|----------|------------|
| Spoofing | Authentication | Keycloak OIDC + MFA, JWT validation |
| Tampering | Integrity | RLS, soft-delete, audit trail, AES-256-GCM |
| Repudiation | Non-repudiation | `audit_log` table, `incident_verification_history` |
| Information Disclosure | Confidentiality | PII encryption, RLS scoping, TLS 1.3 |
| Denial of Service | Availability | Rate limiting, Celery offloading, Nginx |
| Elevation of Privilege | Authorization | RBAC (5 roles), route guards, RLS |

## Attack Surface

| Surface | Entry Point | Controls |
|---------|------------|----------|
| Public API | `/api/v1/public/report` | Input validation, rate limit |
| Auth | Keycloak endpoints | MFA, brute force detection, PKCE |
| File Upload | `/api/regional/incidents/{id}/attachments` | Type whitelist, 10MB limit, 5/file |
| Database | PostgreSQL | RLS, encrypted PII, no hard deletes |
| Internal Network | Docker `wims_internal` | Suricata IDS, network segmentation |
| AI Inference | Ollama API | On-demand only, no autonomous actions |

## OWASP Top 10 (2025) Coverage

| # | Vulnerability | WIMS Mitigation |
|---|--------------|-----------------|
| A01 | Broken Access Control | RBAC + RLS + route guards |
| A02 | Cryptographic Failures | AES-256-GCM, TLS 1.3, WIMS_MASTER_KEY |
| A03 | Injection | SQLAlchemy ORM, parameterized queries |
| A04 | Insecure Design | Constitution mandates, threat model |
| A05 | Security Misconfiguration | Docker hardening, Nginx security headers |
| A06 | Vulnerable Components | Dependabot, CVE tracking |
| A07 | Auth Failures | Keycloak MFA, brute force, session timeout |
| A08 | Data Integrity Failures | Audit trail, soft-delete, version tracking |
| A09 | Logging Failures | `audit_log`, `security_threat_log`, Suricata |
| A10 | SSRF | Internal network segmentation |

## Related

- [[concepts/wims-bfp-codebase-auth-flow]] — authentication controls
- [[concepts/wims-bfp-codebase-rls-model]] — database-level controls
- [[entities/wims-bfp-codebase-rbac-roles]] — authorization model
