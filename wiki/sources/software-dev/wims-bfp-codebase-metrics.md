---
id: wims-bfp-codebase-metrics-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-07-08
confidence: high
source_refs:
  - ~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/src/
status: active
tags:
  - wims-bfp
  - codebase
  - metrics
  - refactoring
  - loc
  - pygount
related:
  - analyses/wims-bfp-thesis-codebase-gaps
  - sources/software-dev/wims-bfp-codebase-ingestion
---

# WIMS-BFP Codebase Metrics (Pre-Refactor Baseline)

**Date:** 2026-04-08
**Tool:** pygount 3.2.0
**Scope:** ~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/src/
**State:** Post-cleanup (3 venvs + caches + stale files removed)

---

## Summary

| Metric | Value |
|---|---|
| Total source files (.py/.ts/.tsx/.sql) | 118 |
| Total lines (code files) | 19,879 |
| Files over 500 lines | 6 |
| Files over 200 lines | 26 |
| Project size (cleaned) | 1.4 GB |

---

## Language Breakdown

| Language | Files | Lines | % |
|---|---|---|---|
| Python | 58 | 8,977 | 45.2% |
| TSX (React) | 38 | 7,387 | 37.2% |
| TypeScript | 18 | 1,992 | 10.0% |
| SQL | 4 | 1,523 | 7.7% |
| **TOTAL** | **118** | **19,879** | **100%** |

Code-to-comment ratio: 81.3% code / 5.5% comments

---

## Refactoring Priority

### CRITICAL (>1000 lines) — MUST split

| Lines | File | Issue |
|---|---|---|
| 1,876 | `backend/api/routes/regional.py` | Monolithic route file. Contains AFOR import, manual entry, regional CRUD, data sync — all in one file. Thesis calls this "microservices" but it's a monolith. |
| 1,468 | `postgres-init/01_wims_initial.sql` | Single init SQL with schema + RLS + indexes + seeds. No migration versioning. |

### HIGH (501-1000 lines) — SHOULD split

| Lines | File | Issue |
|---|---|---|
| 927 | `frontend/src/components/WildlandAforManualForm.tsx` | Massive form component. Should extract sub-components + hooks. |
| 772 | `frontend/src/components/IncidentForm.tsx` | Large form component. Same issue. |
| 515 | `backend/tests/integration/test_regional_afor_unified_import.py` | Long test file — OK for integration tests but could be split by feature. |
| 507 | `frontend/src/lib/api.ts` | API client with all endpoints in one file. Should split by domain. |

### MEDIUM (301-500 lines) — Consider splitting

| Lines | File |
|---|---|
| 492 | `frontend/src/app/dashboard/analyst/page.tsx` |
| 485 | `frontend/src/app/dashboard/page.tsx` |
| 478 | `frontend/src/lib/api.test.ts` |
| 474 | `frontend/src/app/admin/system/page.tsx` |
| 419 | `frontend/src/app/incidents/import/page.tsx` |
| 405 | `frontend/src/app/afor/import/page.tsx` |
| 384 | `backend/tests/integration/test_analytics_api.py` |
| 383 | `backend/main.py` |
| 376 | `frontend/src/app/dashboard/regional/page.tsx` |
| 364 | `backend/tests/integration/test_analytics_security.py` |
| 353 | `backend/auth.py` |
| 350 | `backend/services/analytics_read_model.py` |

---

## Refactoring Plan

### Phase 1: Backend (2 files)

**regional.py (1,876 lines) → split into:**
- `routes/regional_afor.py` — AFOR import/export (~400 lines)
- `routes/regional_manual.py` — manual entry forms (~300 lines)
- `routes/regional_crud.py` — CRUD operations (~300 lines)
- `routes/regional_sync.py` — data sync logic (~200 lines)
- `routes/regional.py` — router aggregation (~100 lines)

**01_wims_initial.sql (1,468 lines) → split into:**
- `01_schema.sql` — table definitions (~500 lines)
- `02_rls.sql` — RLS policies (~400 lines)
- `03_indexes.sql` — indexes + constraints (~200 lines)
- `04_seeds.sql` — reference data (~200 lines)
- `01_init.sql` — master script that calls the above

### Phase 2: Frontend (4 files)

**WildlandAforManualForm.tsx (927 lines) → extract:**
- Sub-components for each form section
- Custom hooks for form logic
- Shared validation utilities

**IncidentForm.tsx (772 lines) → extract:**
- Sub-components (location picker, evidence upload, etc.)
- Form state management hook

**api.ts (507 lines) → split by domain:**
- `api/incidents.ts`
- `api/auth.ts`
- `api/analytics.ts`
- `api/admin.ts`
- `api/regional.ts`

---

## Cross-References

- [[analyses/wims-bfp-thesis-codebase-gaps]] — Thesis vs codebase discrepancies
- [[sources/software-dev/wims-bfp-codebase-ingestion-2026-04-08]] — Pre-refactor ingestion
