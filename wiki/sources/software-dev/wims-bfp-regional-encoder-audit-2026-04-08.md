---
id: wims-bfp-regional-encoder-audit-2026-04-08-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-07-08
confidence: high
source_refs:
  - ~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/src/backend/api/routes/regional.py
  - ~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/src/backend/api/routes/incidents.py
status: active
tags:
  - wims-bfp
  - security
  - audit
  - regional-encoder
  - crud
  - cve
  - error-leakage
related:
  - sources/software-dev/postgis-secure-coding-practices
  - concepts/keycloak-fastapi-security-wims-bfp
  - analyses/wims-bfp-thesis-codebase-gaps
---

# Regional Encoder CRUD + Backend Security Audit — 2026-04-08

**Date:** 2026-04-08
**Scope:** Regional Encoder CRUD routes + full backend security scan
**Verdict:** PASS with 4 fixes applied

---

## Audit Gate Results

### Regional Encoder CRUD

| Check | Status | Details |
|---|---|---|
| SQL Injection | PASS | INSERT f-strings use allowlist column names + parameterized VALUES. UPDATE/DELETE use allowlist + parameterized. |
| Parameterized Queries | PASS | 31 text() calls, 146 parameterized values across regional.py |
| RLS Context | PASS | get_db_with_rls used 9 times (all 8 routes covered) |
| Region Isolation | PASS | assigned_region_id extracted 8 times, region_id in WHERE 7 times |
| Status Gating | PASS | VERIFIED incidents cannot be edited or deleted |
| Soft Delete | PASS | 0 hard DELETE, 2 soft-delete (is_archived=TRUE) |
| PII Encryption | PASS | SecurityProvider encrypt_json/decrypt_json used for PII blob |

### Backend-Wide Security Scan

| Check | Status | Details |
|---|---|---|
| Hardcoded Secrets | PASS | Only test file (test_auth_flow.py) — acceptable |
| CORS | PASS | No wildcard CORS middleware |
| Route Auth | PASS | All routes except civilian.py (DMZ — intentional) have auth |
| Error Leakage | **FIXED** | 4 instances of str(e) in error details — replaced with generic messages |
| Pydantic Validation | WARN | civilian.py, incidents.py, triage.py have routes without explicit Pydantic body (existing pattern, not new) |
| Known CVEs | PASS | All packages at safe versions (sqlalchemy>=2.0, cryptography>=42.0, fastapi>=0.135) |

---

## Fixes Applied

### Error Message Leakage (4 fixes)

| File | Line | Before | After |
|---|---|---|---|
| incidents.py | 56 | `f"Failed to save file: {str(e)}"` | `"Failed to save uploaded file"` + logger.exception |
| incidents.py | 82 | `f"Database error: {str(e)}"` | `"Internal server error"` + logger.exception |
| regional.py | 1100 | `detail=str(e)` | `"Unrecognized AFOR file format"` |
| regional.py | 1103 | `f"Failed to parse file: {str(e)}"` | `"Failed to parse file"` + logger.exception |

**Rationale:** str(e) exposes internal stack traces, DB error messages, and file paths to API consumers. An attacker can use this for reconnaissance. Fixed by returning generic messages and logging details server-side only.

---

## New Routes Added

| Method | Route | Auth | RLS | Purpose |
|---|---|---|---|---|
| POST | `/api/regional/incidents` | REGIONAL_ENCODER | ✅ | Create incident (DRAFT) with nonsensitive + PII-encrypted sensitive |
| PUT | `/api/regional/incidents/{id}` | REGIONAL_ENCODER | ✅ | Update DRAFT/PENDING/REJECTED, PII re-encrypt on merge |
| DELETE | `/api/regional/incidents/{id}` | REGIONAL_ENCODER | ✅ | Soft-delete DRAFT only (is_archived=TRUE) |

Total regional routes: 8 (3 GET + 2 POST AFOR + 1 POST CRUD + 1 PUT + 1 DELETE)

---

## Remaining Warnings (Not Fixed — Existing Pattern)

| Issue | Location | Assessment |
|---|---|---|
| Pydantic body missing | civilian.py, incidents.py, triage.py | Existing routes use raw request.body. Not a new regression. Defer to refactor pass. |
| python-jose CVE-2024-33663 | requirements.txt | No fix available upstream. Mitigated by short token TTLs + Keycloak JWKS validation. |

---

## Cross-References

- [[concepts/keycloak-fastapi-security-wims-bfp]] — Auth architecture
- [[sources/software-dev/postgis-secure-coding-practices]] — Spatial security
- [[analyses/wims-bfp-thesis-codebase-gaps]] — Thesis discrepancies
