---
title: "WIMS-BFP — Wiki MOC Gap Analysis (2026-05-04)"
date: 2026-05-04
tags: [wims-bfp, wiki, moc, gap-analysis]
confidence: high
reviewed: 2026-05-04
source: wiki-scan
author: Ares (Orchestrator)
project: WIMS-BFP
related:
  - "[[mocs/wims-bfp]]"
  - "[[sources/operational/2026-05-04-wims-bfp-earl-branch-review]]"
  - "[[sources/operational/2026-05-04-wims-bfp-earl-branch-spec-audit]]"
---

# WIMS-BFP — Wiki MOC Gap Analysis

**Scanned:** 2026-05-04
**Scope:** All wiki pages, entities, concepts, analyses, sources, raw/articles
**Baseline:** `mocs/wims-bfp.md` (MOC entry point)

---

## Canonical MOC Sections vs Coverage Status

### MOC Section: "Codebase Reference (Verified 2026-04-21) — Entities"
| Page (MOC name) | Exists? | Populated? | Notes |
|---|---|---|---|
| `entities/wims-bfp-codebase-api-endpoints` | ✅ | ? | — |
| `entities/wims-bfp-codebase-database-schema` | ✅ | ? | — |
| `entities/wims-bfp-codebase-docker-services` | ✅ | ? | — |
| `entities/wims-bfp-codebase-frontend-pages` | ✅ | ? | — |
| `entities/wims-bfp-codebase-init-scripts` | ✅ | ? | — |
| `entities/wims-bfp-codebase-keycloak-config` | ✅ | ? | — |
| `entities/wims-bfp-codebase-rbac-roles` | ✅ | ? | — |

### MOC Section: "Codebase Reference — Concepts"
| Page (MOC name) | Exists? | Populated? | Notes |
|---|---|---|---|
| `concepts/wims-bfp-codebase-afor-import` | ✅ | ? | — |
| `concepts/wims-bfp-codebase-auth-flow` | ✅ | ? | — |
| `concepts/wims-bfp-codebase-data-flow` | ✅ | ? | — |
| `concepts/wims-bfp-codebase-offline-pwa` | ✅ | ? | — |
| `concepts/wims-bfp-codebase-pii-encryption` | ✅ | ✅ | AES-256-GCM, encrypted fields, key management |
| `concepts/wims-bfp-codebase-rls-model` | ✅ | ? | — |
| `concepts/wims-bfp-codebase-spatial-data` | ✅ | ? | — |
| `concepts/wims-bfp-codebase-threat-model` | ✅ | ? | — |
| `concepts/wims-bfp-codebase-xai-pipeline` | ✅ | ? | — |
| `concepts/wims-bfp-ci-cd-pipeline` | ✅ | ? | — |

### MOC Section: "Pending Refactoring"
| Item | Status | Notes |
|---|---|---|
| Split regional.py | Deferred | — |
| Alembic migrations | Pending | No dedicated page |

### MOC Section: "Codebase Audit"
| Page | Status |
|---|---|
| `sources/software-dev/wims-bfp-codebase-ingestion-2026-04-08` | ❌ NOT FOUND — MOC link is dead |
| `sources/software-dev/wims-bfp-codebase-metrics` | ❌ NOT FOUND |
| `sources/software-dev/wims-bfp-regional-encoder-audit-2026-04-08` | ❌ NOT FOUND |
| `sources/software-dev/wims-bfp-thesis-revisions-2026-04-08` | ❌ NOT FOUND |

---

## New Operational Pages (2026-05-04) — Added Today

These were created today and need MOC integration:

| Page | Category | Needs MOC entry? |
|---|---|---|
| `sources/operational/2026-05-04-wims-bfp-earl-branch-review` | operational | ✅ Yes — add to Operational table |
| `sources/operational/2026-05-04-wims-bfp-earl-branch-spec-audit` | operational | ✅ Yes — add to Operational table |

---

## Ghost Links — MOC References Pages That Don't Exist

| MOC link | Referenced from | Status |
|---|---|---|
| `concepts/decisions-and-rationale` | `mocs/wims-bfp.md` (Pending Refactoring) | ❌ File missing |
| `analyses/4-agent-pipeline-postmortem` | `mocs/wims-bfp.md` (Operational) | ❌ File missing |
| `sources/software-dev/wims-bfp-codebase-ingestion-2026-04-08` | `mocs/wims-bfp.md` (Codebase Audit) | ❌ File missing |
| `sources/software-dev/wims-bfp-codebase-metrics` | `mocs/wims-bfp.md` (Codebase Audit) | ❌ File missing |
| `sources/software-dev/wims-bfp-regional-encoder-audit-2026-04-08` | `mocs/wims-bfp.md` (Codebase Audit) | ❌ File missing |
| `sources/software-dev/wims-bfp-thesis-revisions-2026-04-08` | `mocs/wims-bfp.md` (Codebase Audit) | ❌ File missing |

---

## Missing WIMS-BFP Pages — Never Created or Not Yet Linked to MOC

These pages exist in the codebase but have no wiki page, or exist but are not linked in the MOC.

### A. Analytics & Read Model

| Page | Path | Status |
|---|---|---|
| `wims-bfp-codebase-analytics-read-model` | `services/analytics_read_model.py` | ❌ Missing — sync_incident_to_analytics(), backfill_analytics_facts(), analytics_incident_facts table |
| `wims-bfp-codebase-national-analyst` | `routes/analyst.py` + dashboard pages | ❌ Missing — Issue #89 still open |

### B. Immutable Records (M6-D)

| Page | Path | Status |
|---|---|---|
| `wims-bfp-codebase-immutable-records` | `postgres-init/17_immutable_records.sql` | ❌ Missing — data_hash column, DB-level UPDATE/DELETE rules |
| `wims-bfp-codebase-af or-commit-pipeline` | `verify_incident()` in `routes/regional.py` | ❌ Missing — SHA-256 hash at VERIFIED, analytics sync, idempotency guard |

### C. Admin & User Management

| Page | Path | Status |
|---|---|---|
| `wims-bfp-codebase-keycloak-admin-python` | `services/keycloak_admin.py` | ❌ Missing — KeycloakOpenID.token() pattern, broken Connection API |
| `wims-bfp-codebase-admin-onboarding` | `routes/admin.py` | ❌ Missing — 4-layer stacked failure fix (PR #91) |
| `wims-bfp-codebase-user-management-module12` | `routes/admin.py` + `routes/users.py` | ❌ Missing — full CRUD, role assignment, session revocation |

### D. JWT / Session Auth

| Page | Path | Status |
|---|---|---|
| `wims-bfp-codebase-jwt-refresh` | `frontend/src/lib/auth.tsx` + `context/AuthContext.tsx` | ⚠️ Partial — session persistence fix doc exists; navigator.locks + refreshInterval not documented |
| `wims-bfp-codebase-dual-authprovider-trap` | `context/AuthContext.tsx` vs `lib/auth.tsx` | ❌ Missing — Bug 9 from debugging session: pages consume different providers |

### E. Public DMZ & Rate Limiting

| Page | Path | Status |
|---|---|---|
| `wims-bfp-codebase-public-dmz` | `api/public_dmz.py` | ❌ Missing — Module 14, Redis IP rate limiting (3 req/IP/hr), encoder_id=NULL |
| `wims-bfp-codebase-ref-data-service` | `api/ref.py` | ❌ Missing — Module 15, authenticated read-only geographic lookup |

### F. Scheduled & Background Tasks

| Page | Path | Status |
|---|---|---|
| `wims-bfp-codebase-scheduled-reports` | `tasks/` + `routes/reports.py` | ❌ Missing — Issue #88 open, Celery + email scheduling |
| `wims-bfp-codebase-celery-config` | `celery_config.py` | ❌ Missing — broker config, task routing |

### G. Notification System (Module 13 — DEFERRED)

| Page | Path | Status |
|---|---|---|
| `wims-bfp-codebase-notifications-sse` | `routes/notifications.py` | ❌ Missing — SSE, Module 13 deferred |

### H. Testing

| Page | Path | Status |
|---|---|---|
| `wims-bfp-codebase-test-immutable-records` | `tests/test_immutable_records.py` | ❌ Missing — 5 integration tests, red/green state |
| `wims-bfp-codebase-test-suite` | `tests/` directory | ❌ Missing — queue-baseline.test.tsx pre-existing failure |

### I. Infrastructure & Docker

| Page | Path | Status |
|---|---|---|
| `wims-bfp-codebase-nginx-config` | `nginx.conf` or `docker-compose` nginx service | ❌ Missing — reverse proxy, header config |
| `wims-bfp-codebase-docker-volume-backup` | volumes in `docker-compose.yml` | ❌ Missing — incident_attachments_data backup strategy |
| `wims-bfp-codebase-environment-vars` | `.env.example` or `docker-compose.yml` env section | ❌ Missing — all env vars, secrets management |

### J. API Routes Not Yet Documented

From `src/backend/api/routes/` — files with no wiki entry:

| File | Module | Status |
|---|---|---|
| `api/public_dmz.py` | Module 14 | ❌ Missing |
| `api/ref.py` | Module 15 | ❌ Missing |
| `api/reports.py` | Scheduled reports | ❌ Missing |
| `api/notifications.py` | Module 13 | ❌ Missing |
| `api/ai_service.py` | XAI pipeline | ⚠️ Partial — xai-pipeline concept exists, ai_service.py details missing |
| `api/suricata_ingestion.py` | IDS | ⚠️ Partial — xai-pipeline concept exists, route file details missing |

---

## Stray / Unlinked Files in Wiki

These exist in the wiki but are not referenced from the MOC:

| File | Notes |
|---|---|
| `concepts/advisor-strategy.md` | WIMS-BFP advisor strategy — not linked in MOC |
| `concepts/wims-bfp-agentic-workflow.md` | WIMS-BFP agentic workflow — not linked in MOC |
| `concepts/wims-bfp-kanban-integration-plan.md` | Kanban plan — not linked in MOC |
| `concepts/decisions-and-rationale.md` | **Ghost link** — MOC references it but file doesn't exist |

---

## Priority: Missing Pages That Need Creation

Sorted by Earl-Branch relevance and thesis documentation urgency:

### P0 — Must Document (Earl-Branch dependent)

1. **`concepts/wims-bfp-codebase-analytics-read-model`** — analytics_read_model.py, sync_incident_to_analytics(), backfill_analytics_facts(), analytics_incident_facts schema
2. **`concepts/wims-bfp-codebase-immutable-records`** — 17_immutable_records.sql, data_hash, CREATE RULE no_update_verified/no_delete_verified, append-only enforcement
3. **`concepts/wims-bfp-codebase-af or-commit-pipeline`** — verify_incident() full flow: idempotency guard, SHA-256 hash, incident_verification_history insert, log_system_audit, analytics sync

### P1 — High Value (open issues, thesis)

4. **`concepts/wims-bfp-codebase-admin-onboarding`** — 4-layer stacked failure (Keycloak password, python-keycloak API, RLS GUC leak, missing contact_number), exec_as_system_admin(), create_user flow
5. **`concepts/wims-bfp-codebase-keycloak-admin-python`** — KeycloakOpenID.token() + KeycloakAdmin(token=) pattern, vs broken KeycloakOpenIDConnection
6. **`concepts/wims-bfp-codebase-jwt-refresh`** — navigator.locks serialization, setInterval 4-min refresh, visibilitychange suppression, dual-provider trap
7. **`concepts/wims-bfp-codebase-national-analyst`** — analyst.py CRUD, dashboard queries, Issue #89

### P2 — Module Coverage (Modules 13/14/15)

8. **`concepts/wims-bfp-codebase-public-dmz`** — public_dmz.py, Redis rate limiting, encoder_id=NULL, PENDING_VALIDATION
9. **`concepts/wims-bfp-codebase-ref-data-service`** — ref.py, authenticated geographic lookup endpoints
10. **`concepts/wims-bfp-codebase-scheduled-reports`** — Celery tasks, cron, email, Issue #88

### P3 — Cleanup (ghost links, orphaned pages)

11. **Fix or remove ghost links** in `mocs/wims-bfp.md` — `decisions-and-rationale.md`, `wims-bfp-codebase-ingestion-2026-04-08`, `wims-bfp-codebase-metrics`, `wims-bfp-regional-encoder-audit-2026-04-08`, `wims-bfp-thesis-revisions-2026-04-08`
12. **Verify `concepts/advisor-strategy.md`** — determine if still relevant or prune
13. **Verify `concepts/wims-bfp-agentic-workflow.md`** — determine if still relevant or prune

---

## MOC Updates Required

After creating the missing pages above, update `mocs/wims-bfp.md`:

**Operational table additions (today):**
```
|| 2026-05-04 | WIMS-BFP Earl-Branch review + SPEC audit | [[sources/operational/2026-05-04-wims-bfp-earl-branch-spec-audit]] |
```

**Codebase Reference — Concepts additions:**
```
|| [[concepts/wims-bfp-codebase-analytics-read-model]] | analytics_incident_facts, sync functions, National Analyst read model |
|| [[concepts/wims-bfp-codebase-immutable-records]] | SHA-256 data_hash, DB-level UPDATE/DELETE rules, append-only |
|| [[concepts/wims-bfp-codebase-af or-commit-pipeline]] | verify_incident() full flow, idempotency, analytics sync |
|| [[concepts/wims-bfp-codebase-admin-onboarding]] | 4-layer stacked failure, Keycloak auth, RLS fix |
|| [[concepts/wims-bfp-codebase-keycloak-admin-python]] | KeycloakOpenID.token() pattern vs broken API |
|| [[concepts/wims-bfp-codebase-jwt-refresh]] | navigator.locks, refreshInterval, dual-provider trap |
|| [[concepts/wims-bfp-codebase-public-dmz]] | Module 14, Redis rate limiting, public submission |
|| [[concepts/wims-bfp-codebase-ref-data-service]] | Module 15, authenticated geographic lookup |
|| [[concepts/wims-bfp-codebase-scheduled-reports]] | Celery tasks, email reports, Issue #88 |
```

**Pending Refactoring — Alembic:**
```
| Implement Alembic migrations | Not started | Currently manual SQL; versioned schema needed for ISO 27001 compliance |
```

**Ghost links cleanup:**
- Remove or recreate `concepts/decisions-and-rationale.md`
- Remove or recreate `sources/software-dev/wims-bfp-codebase-ingestion-2026-04-08`
- Remove or recreate `sources/software-dev/wims-bfp-codebase-metrics`
- Remove or recreate `sources/software-dev/wims-bfp-regional-encoder-audit-2026-04-08`
- Remove or recreate `sources/software-dev/wims-bfp-thesis-revisions-2026-04-08`
