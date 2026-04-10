---
id: wims-bfp-knowledge-graph-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-07-08
confidence: medium
source_refs:
  - raw/misc/KNOWLEDGE_GRAPH.md
  - raw/misc/BACKEND_HEALTH_REPORT.md
status: active
tags:
  - wims-bfp
  - knowledge-graph
  - code-map
  - health-report
  - audit
related:
  - sources/software-dev/wims-bfp-codebase-ingestion
  - analyses/wims-bfp-thesis-codebase-gaps
---

# WIMS-BFP Knowledge Graph + Backend Health Report

**Source:** raw/misc/KNOWLEDGE_GRAPH.md, raw/misc/BACKEND_HEALTH_REPORT.md
**Generated:** 2026-03-28
**Note:** Snapshot from pre-refactor baseline. May not reflect latest codebase state.

---

## Architecture Alignment (Thesis ↔ Prototype)

### Thesis Architecture (Ch 3.4)
```
User → Next.js (PWA) → FastAPI → PostgreSQL/PostGIS
                         ↓
                    Suricata IDS (EVE JSON)
                         ↓
              AI Service (Qwen2.5-3B via Ollama)
                         ↓
              XAI Narrative → Dashboard
```

### Actual Codebase (2026-03-28 snapshot)
```
frontend/next.js (App Router) → nginx (:80) → backend/fastapi
                                               ↓
                         ┌──────────────────────┴──────────────────────┐
                    PostgreSQL + PostGIS        Redis           Ollama (qwen2.5:3b)
                    (fire_incidents,            (broker)        (SLM inference)
                     citizen_reports,
                     security_threat_logs,
                     ref_* tables)
                                               Celery worker
                                               (suricata.py)
                                               reads EVE JSON
                                               → security_threat_logs
```

**Status:** Aligned with thesis architecture. Discrepancies documented in [[analyses/wims-bfp-thesis-codebase-gaps]].

---

## Backend Health Report Findings (2026-03-28)

### CRITICAL (at time of report)

| ID | Finding | Status (Apr 2026) |
|---|---|---|
| C-01 | AES-256-GCM NOT implemented — no crypto library in requirements.txt | NOW IMPLEMENTED (crypto.py exists) |
| C-02 | RLS policies incomplete — multiple tables unprotected | PARTIALLY FIXED (01_wims_initial.sql has policies) |
| C-03 | Hardcoded secrets in .env | NEEDS VERIFICATION |

### Key Metrics (at time of report)

| Metric | Value |
|---|---|
| Branch | master — clean |
| Last 10 commits | Active development (auth hardening, AFOR import, analytics) |
| Audit scope | Auth boundaries, crypto/secrets, ingestion endpoints |
| Audit standard | OWASP ASVS Level 2 + STRIDE |

### Evolution Since Health Report

The health report was generated 2026-03-28. Since then:
- `feat(auth): enforce role-based OTP for admin/validator with 7-day trusted device`
- `feat(regional-afor): add wildland workbook import, manual entry, and commit source`
- `feat(analytics): add national analyst dashboard and backend support`
- `feat: UI overhaul, AFOR parser implementation, PWA features, and final cleanup`

This indicates active remediation of the health report findings.

---

## Purpose in Wiki

This document serves as:
1. **Historical baseline** — snapshot of codebase state at thesis draft time
2. **Cross-reference anchor** — links thesis claims to actual code at a point in time
3. **Audit trail** — documents what was found broken and when it was fixed

For current codebase state, see [[sources/software-dev/wims-bfp-codebase-ingestion-2026-04-08]].
For discrepancy analysis, see [[analyses/wims-bfp-thesis-codebase-gaps]].
