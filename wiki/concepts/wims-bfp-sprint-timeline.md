---
id: wims-bfp-sprint-timeline-001
type: concept
created: 2026-04-21
updated: 2026-04-21
last_verified: 2026-04-21
review_after: 2026-05-21
stale_after: 2026-07-21
confidence: high
source_refs:
  - raw/sources/wims-bfp-codebase/frs-modules.md (codebase wiki)
status: active
tags:
  - wims-bfp
  - design
  - operational
related:
  - concepts/wims-bfp-frs-modules
  - concepts/wims-bfp-sprint-gantt
  - analyses/wims-bfp-frs-implementation-tracker
  - mocs/wims-bfp
---

# Sprint Timeline — April 22 to May 5, 2026

14 days. 6 sprints. Based on ACTUAL codebase audit (2026-04-21).
Modules 1 and 12 are DONE. Module 2 is IN PROGRESS (laqqui). Everything else needs work.

## Codebase Audit Summary (Verified 2026-04-21)

| Module | Status | Verified |
|--------|--------|----------|
| 1 — Auth & Access Control | DONE | JWT, MFA, brute force, session timeouts all in `auth.py` + realm JSON |
| 2 — Offline-First Incidents | IN PROGRESS | `offlineStore.ts` (idb), `sw.js` (Background Sync), AFOR import UI exists. Laqqui working on AFOR/wildland. |
| 3 — Conflict Detection | NOT STARTED | Frontend `runConflictDetection()` calls non-existent backend. No RapidFuzz. No background tasks. |
| 4 — Immutable Storage | NOT STARTED | DB schema has soft-delete. No append-only GRANT/REVOKE. No version tracking. |
| 5 — Analytics | HALF | `analytics.py` routes, `analytics_read_model.py`, HeatmapViewer + TrendCharts components exist. No materialized views. |
| 6 — Crypto | HALF | `crypto.py` AES-256-GCM working. No key rotation. No TLS enforcement config. |
| 7 — IDS | HALF | Suricata container + ingestion service running. No AF_PACKET tuning. No app-layer parser config. |
| 8 — XAI | NOT STARTED | `ai_service.py` exists but empty/stub. No prompt templates. No Qwen2.5 integration. |
| 9 — Monitoring | NOT STARTED | Nothing. |
| 10 — Compliance | NOT STARTED | Nothing. |
| 11 — PenTesting | NOT STARTED | Nothing. |
| 12 — User Management | DONE | `keycloak_admin.py` with create/disable/update. Admin CRUD routes. Tests. |
| 13 — Notifications | NOT STARTED | Nothing. |

## Gantt Overview

```
Apr 22 Wed ─┤ S1: Module 2 Offline/Sync (3d)     Module 2 B+C (laqqui handles AFOR)
Apr 25 Fri ─┤ S2: Conflict Detection (2d)         Module 3
Apr 27 Sun ─┤ S3: Immutable Storage (2d)          Module 4
Apr 29 Tue ─┤ S4: Analytics Completion (2d)       Module 5
May  01 Thu ─┤ S5: Crypto + IDS + XAI (3d)        Modules 6,7,8
May  04 Sun ─┤ S6: Mon+Compliance+PenTest+Notif (2d)  Modules 1.D,9,10,11,13 + E2E
             ╰ DONE
```

**NOTE:** Module 1 is 90% done — missing D.3 (session max 8h), D.4 (force logout on password/role change), D.5 (concurrent session detection). Scheduled in S6.
**NOTE:** Module 2 is 30% — skeleton exists (offlineStore, SW, NetworkStatusIndicator). Laqqui handles AFOR import. Offline CRUD + encryption + sync scheduled S1.
**NOTE:** Module 12 (User Mgmt) is DONE via cherry-pick.

---

## Sprint 1: Module 2 — Offline CRUD + Encryption + Sync
**Duration:** 3 days (Apr 22–24)
**Modules:** [[concepts/wims-bfp-frs-modules#Module 2|Module 2]] (B.3, B.5, C.2–C.5, D.1)
**Status:** 30% — skeleton exists, most offline/sync features missing

### Scope
| # | Task | FRS Ref | Est |
|---|------|---------|-----|
| 1.1 | Encrypt queued payloads — Web Crypto API AES-256-GCM before IndexedDB write | Module 2.B.3 | 3h |
| 1.2 | Queue management — view/edit/delete queued incidents before sync | Module 2.B.5 | 3h |
| 1.3 | Integrity verification — AES-GCM tag check before upload in SW | Module 2.C.3 | 2h |
| 1.4 | Atomic sync — wrap each incident upload in backend transaction | Module 2.C.5 | 2h |
| 1.5 | Exponential backoff retry (max 5) with counter in SW sync handler | Module 2.C.6 | 2h |
| 1.6 | Frontend toast handler for `sync-complete` postMessage from SW | Module 2.C.7 | 2h |
| 1.7 | Add "Flagged" status to verification_status enum if needed | Module 2.D.1 | 1h |
| 1.8 | Verify IncidentForm field completeness + client-side validation | Module 2.A.1, A.3 | 3h |
| 1.9 | Integration tests — queue create, encrypt, sync, integrity check | — | 3h |

### Deliverables
- Queued payloads encrypted with AES-256-GCM before IndexedDB storage
- Queue management UI (view/edit/delete pending offline incidents)
- Background Sync with integrity verification + exponential backoff
- Toast notification on sync success/failure
- Form validation verified against FRS requirements

### Depends On
- Existing: `offlineStore.ts` (64 lines), `sw.js` (141 lines), `IncidentForm.tsx` (60KB)
- No dependency on other sprints

---

## Sprint 2: Conflict Detection & Manual Verification
**Duration:** 2 days (Apr 25–26)
**Modules:** [[concepts/wims-bfp-frs-modules#Module 3|Module 3]]
**Status:** NOT STARTED — backend endpoint doesn't exist, no fuzzy matching

### Scope
| # | Task | FRS Ref | Est |
|---|------|---------|-----|
| 2.1 | Backend: conflict detection endpoint `POST /api/incidents/{id}/detect-conflicts` | Module 3.A.1 | 3h |
| 2.2 | Add `rapidfuzz>=3.0` to requirements.txt | Module 3.A.2 | 0.5h |
| 2.3 | Exact match: location + date/time within 30-min window (SQL query) | Module 3.A.2 | 3h |
| 2.4 | Fuzzy match: incident narrative similarity (RapidFuzz, threshold 80%) | Module 3.A.2 | 3h |
| 2.5 | Casualty count matching logic | Module 3.A.2 | 2h |
| 2.6 | FastAPI Background Task — auto-trigger on new incident create | Module 3.A.1 | 2h |
| 2.7 | Fix frontend `runConflictDetection()` — wire to real backend | Module 3.B | 2h |
| 2.8 | National Validator review UI — side-by-side comparison, accept/reject/merge | Module 3.B | 4h |
| 2.9 | Integration tests — duplicate detection, validator decision flow | — | 2h |

### Deliverables
- Backend conflict detection endpoint returning matched incidents
- RapidFuzz narrative comparison working
- Auto-trigger on incident creation (background task)
- Frontend wired to real backend (not stub)
- Validator sees flagged conflicts in triage queue

### Depends On
- Existing: `frontend/src/lib/edgeFunctions.ts` (stub), `src/backend/api/routes/triage.py` (queue exists)

---

## Sprint 3: Immutable Storage & Data Commit
**Duration:** 2 days (Apr 27–28)
**Modules:** [[concepts/wims-bfp-frs-modules#Module 4|Module 4]]
**Status:** NOT STARTED — soft-delete exists but no append-only or versioning

### Scope
| # | Task | FRS Ref | Est |
|---|------|---------|-----|
| 3.1 | PostgreSQL: REVOKE UPDATE/DELETE on committed records (append-only) | Module 4.A.2 | 3h |
| 3.2 | Add `version_id` and `original_record_id` columns to `fire_incidents` | Module 4.A.3 | 2h |
| 3.3 | Version creation on modification — new row references original | Module 4.A.3 | 3h |
| 3.4 | Commit verification — validator approves → immutable record + status gate | Module 4.A.1 | 3h |
| 3.5 | Write migration SQL: `05_append_only_enforcement.sql` | Module 4.A.2 | 2h |
| 3.6 | Integration tests — append-only constraint, version chain, commit flow | — | 3h |

### Deliverables
- Committed records cannot be modified at DB level (GRANT/REVOKE)
- Every modification creates a version entry linked to original
- Status transitions enforce immutability post-VERIFIED
- Migration script for schema changes

### Depends On
- Existing: [[entities/wims-bfp-codebase-database-schema]], concepts/wims-bfp-codebase-rls-model, `src/postgres-init/01_wims_initial.sql`
- Sprint 1 preferred (conflict detection feeds into verification)

---

## Sprint 4: Analytics Completion
**Duration:** 2 days (Apr 29–30)
**Modules:** [[concepts/wims-bfp-frs-modules#Module 5|Module 5]]
**Status:** HALF — routes and components exist, materialized views missing

### Scope
| # | Task | FRS Ref | Est |
|---|------|---------|-----|
| 4.1 | PostgreSQL materialized views — incident counts, trends, aggregations | Module 5.A.1 | 4h |
| 4.2 | Filter engine — date range, incident type, location, casualty severity, damage range | Module 5.A.2 | 3h |
| 4.3 | Materialized view refresh — Celery beat schedule (hourly) | Module 5.A.1 | 2h |
| 4.4 | Analytics views implementation — total incidents, daily/weekly/monthly trends | Module 5.A.3 | 3h |
| 4.5 | CSV export — async Celery task for large datasets | Module 5.B | 2h |
| 4.6 | Analyst dashboard UI polish — filters, charts, export button | Module 5.C | 3h |
| 4.7 | Integration tests — materialized view refresh, filter correctness | — | 2h |

### Deliverables
- Materialized views auto-refresh via Celery beat
- Analyst can filter by date, type, location, severity, damage
- Trend charts render real data
- CSV export working for large result sets

---

## Sprint 5: Crypto + IDS + XAI
**Duration:** 3 days (May 1–3)
**Modules:** [[concepts/wims-bfp-frs-modules#Module 6|Module 6]], [[concepts/wims-bfp-frs-modules#Module 7|Module 7]], [[concepts/wims-bfp-frs-modules#Module 8|Module 8]]
**Status:** Modules 6+7 HALF, Module 8 NOT STARTED

### Scope
| # | Task | FRS Ref | Est |
|---|------|---------|-----|
| 5.1 | Key rotation mechanism — OpenBao integration or manual rotation script | Module 6.A.4 | 4h |
| 5.2 | Expand PII encryption — narratives, casualty details, property damage, attachments | Module 6.A.1–2 | 3h |
| 5.3 | TLS enforcement — Nginx SSL termination, internal Docker TLS | Module 6.B | 2h |
| 5.4 | Suricata AF_PACKET — monitor all Docker network traffic | Module 7.A.1–2 | 3h |
| 5.5 | App-layer parsers — HTTP, DB queries, file uploads, auth flows | Module 7.A.3 | 2h |
| 5.6 | XAI: prompt template — "Sovereign Forensic Template" with alert fields | Module 8.A–B | 4h |
| 5.7 | XAI: Qwen2.5-3B integration via Ollama — inference pipeline | Module 8.A | 4h |
| 5.8 | XAI: on-demand mode — admin triggers analysis, sync response | Module 8.A.3 | 2h |
| 5.9 | Integration tests — encryption roundtrip, Suricata ingestion, XAI output | — | 4h |

---

## Sprint 6: PenTest + Notifications + E2E Polish
**Duration:** 2 days (May 4–5)
**Modules:** [[concepts/wims-bfp-frs-modules#Module 11|Module 11]], [[concepts/wims-bfp-frs-modules#Module 13|Module 13]], Integration

### Scope
| # | Task | FRS Ref | Est |
|---|------|---------|-----|
| 6.1 | Module 1.D.3: Adjust `ssoSessionMaxLifespan` to 28800 (8h per FRS) | Module 1.D.3 | 0.5h |
| 6.2 | Module 1.D.4: Backchannel logout on `PATCH /api/user/me/password` | Module 1.D.4 | 2h |
| 6.3 | Module 1.D.4: Backchannel logout on `PATCH /api/admin/users/{id}` (role change) | Module 1.D.4 | 1h |
| 6.4 | Module 1.D.5: Backend `GET /api/admin/sessions/{user_id}` | Module 1.D.5 | 2h |
| 6.5 | Module 1.D.5: Backend `DELETE /api/admin/sessions/{user_id}/{session_id}` | Module 1.D.5 | 1h |
| 6.6 | Module 1.D.5: Frontend — replace `'—'` with active sessions view + terminate button | Module 1.D.5 | 2h |
| 6.7 | Nmap scan — network discovery + port scanning on staging | Module 11.A.1 | 2h |
| 6.8 | OWASP ZAP scan — web app vulnerability scanning | Module 11.A.2 | 3h |
| 6.9 | sqlmap test — SQL injection validation on all endpoints | Module 11.A.3 | 2h |
| 6.10 | PenTest report — findings + remediation plan | Module 11.B | 3h |
| 6.11 | SSE endpoint — `/api/notifications/stream` | Module 13.A.1 | 3h |
| 6.12 | Notification events: status updates, duplicate alerts, verification decisions, security alerts, sync status | Module 13.A.1 | 2h |
| 6.13 | Toast UI — react-hot-toast integration, top-right non-intrusive | Module 13.A.2 | 2h |
| 6.14 | Notification history page | Module 13.A.3 | 2h |
| 6.15 | E2E integration test — full flow: create → conflict → verify → commit → analytics → notify | — | 4h |
| 6.16 | Final lint + test pass across entire stack | — | 3h |

---

## Summary Matrix (Post-Audit)

| Sprint | Dates | Days | Modules | Status |
|--------|-------|------|---------|--------|
| S1 | Apr 22–24 | 3 | 2 (Offline CRUD + Sync) | pending |
| S2 | Apr 25–26 | 2 | 3 (Conflict Detection) | pending |
| S3 | Apr 27–28 | 2 | 4 (Immutable Storage) | pending |
| S4 | Apr 29–30 | 2 | 5 (Analytics) | pending |
| S5 | May 1–3 | 3 | 6, 7, 8 (Crypto + IDS + XAI) | pending |
| S6 | May 4–5 | 2 | 1.D, 9, 10, 11, 13 + E2E | pending |

**Done:** Module 12
**90%:** Module 1 (auth done, session mgmt D.3/D.4/D.5 missing — scheduled S6)
**30%:** Module 2 (skeleton exists, laqqui on AFOR, offline/sync scheduled S1)
**Remaining:** Modules 2 (offline), 3, 4, 5, 6, 7, 8, 9, 10, 11, 13 + Module 1 session mgmt
**Total remaining:** ~120 estimated hours across 14 working days

## Related

- [[concepts/wims-bfp-frs-modules]] — full FRS module details
- [[concepts/wims-bfp-sprint-gantt]] — visual Gantt chart
- [[analyses/wims-bfp-frs-implementation-tracker]] — older FRS tracker (6-area format)
- [[mocs/wims-bfp]] — project map of content
