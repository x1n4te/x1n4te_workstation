---
id: wims-bfp-frs-implementation-tracker-001
type: analysis
created: 2026-04-12
updated: 2026-04-12
last_verified: 2026-04-21
review_after: 2026-05-12
stale_after: 2026-07-12
confidence: high
source_refs:
  - sources/software-dev/wims-bfp-ch3a-research-design
  - analyses/wims-bfp-thesis-codebase-gaps
  - ~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/src/
status: active
tags:
  - wims-bfp
  - thesis
  - frs
  - implementation-tracker
  - design
related:
  - sources/software-dev/wims-bfp-ch3a-research-design
  - analyses/wims-bfp-thesis-codebase-gaps
  - mocs/wims-bfp
  - concepts/secure-coding-practices
  - concepts/wims-bfp-frs-modules
---

# WIMS-BFP FRS Implementation Tracker (Legacy — 6-Area Format)

**Superseded by:** [[concepts/wims-bfp-frs-modules]] (13-module format, codebase-verified 2026-04-21)
**This page:** Retained for cross-reference to thesis Chapter 3a FR-1 through FR-6 areas.

**Source:** Chapter 3a Functional Requirements (6 areas)
**Method:** Cross-referenced against codebase routes, models, and services (2026-04-12)
**Status:** 2/6 complete, 3/6 partial, 1/6 not started

---

## Legend

| Symbol | Meaning |
|---|---|
| ✅ | Implemented and verified in codebase |
| ⚠️ | Partially implemented — gaps exist |
| ❌ | Not implemented or not started |
| 🔧 | In progress / recently touched |

---

## FR-1: Crowdsourced Reporting ✅

**Thesis claim:** Public VPS portal for civilian incident submission; internal users encode/update/track

| Component | Status | Evidence |
|---|---|---|
| Public incident submission (no-auth DMZ) | ✅ | `public_dmz.py` — POST `/api/v1/public/report` |
| Civilian report route | ✅ | `civilian.py` — POST `/reports` with Pydantic validation |
| Regional encoder CRUD | ✅ | `regional.py` — full CRUD (2,217 lines) |
| Incident creation | ✅ | `incidents.py` — POST `/incidents` |
| Attachment upload | ✅ | `incidents.py` — POST `/incidents/{id}/attachments` |
| Frontend incident form | ✅ | `src/app/incidents/create/`, `src/app/report/` |

**Verdict:** Complete. All submission paths exist.

---

## FR-2: Geospatial Mapping ⚠️

**Thesis claim:** PostGIS interactive heatmaps; centralized validation workflow

| Component | Status | Evidence |
|---|---|---|
| PostGIS column (geometry) | ✅ | `fire_incident.py` model has `GeoAlchemy2` geometry |
| Geometry validation service | ✅ | `geometry_validation.py` model exists |
| Heatmap API endpoint | ⚠️ | `analytics.py` — GET `/heatmap` exists but needs load testing |
| Interactive map frontend | ❌ | No `Map/` or `Heatmap/` component found in `src/components/` |
| PostGIS spatial queries (clustering) | ⚠️ | Backend has PostGIS support but clustering is Celery-deferred |
| Province/city drill-down | ⚠️ | `ref.py` — GET `/regions` only, no `/provinces` or `/cities` |

**Gaps:**
- [ ] Frontend interactive map component (Leaflet/Mapbox integration)
- [ ] Expand `/api/ref/` to include provinces and cities endpoints
- [ ] PostGIS heatmap rendering performance validation (Locust)
- [ ] Spatial clustering Celery task confirmation

---

## FR-3: Data Synchronization ❌

**Thesis claim:** Auto-detect network restoration; sync offline bundles without data loss

| Component | Status | Evidence |
|---|---|---|
| IndexedDB local storage | ✅ | `offlineStore.ts` — `idb` package, `wims-bfp-db` |
| Incident queue (offline) | ✅ | `queueIncident`, `getPendingIncidents`, `markSynced` |
| Service Worker | ❌ | `public/sw.js` exists but no background sync logic |
| TanStack Query (sync state) | ❌ | Not in `package.json` |
| Auto-detect network restoration | ❌ | No `navigator.onLine` listener or `online` event handler |
| Conflict resolution | ❌ | No merge/retry logic for failed syncs |
| Background sync registration | ❌ | No `sync.register()` API usage |

**Gaps (CRITICAL — thesis defense blocker per C-1 discrepancy):**
- [ ] Implement Service Worker with `sync` event handler
- [ ] Add TanStack Query for sync state management (or equivalent)
- [ ] Network detection (`online`/`offline` event listeners)
- [ ] Conflict resolution strategy (last-write-wins or manual merge)
- [ ] Background sync registration on connectivity restore
- [ ] Update thesis language if not implementing full offline-first

---

## FR-4: Access Control ✅

**Thesis claim:** Strict RBAC via Keycloak across 5 roles

| Component | Status | Evidence |
|---|---|---|
| Keycloak OIDC integration | ✅ | `auth.py` — JWT validation, JWKS fetch |
| 5 FRS roles (exact literals) | ✅ | `main.py` — `WIMS_ROLES_FROM_KEYCLOAK` tuple |
| Role resolution from JWT | ✅ | `_resolve_role_from_token()` — realm_access + resource_access |
| `require_role()` dependency | ✅ | Route-level enforcement on all protected endpoints |
| RLS (Row-Level Security) | ✅ | `01_wims_initial.sql` — policies for region-scoped access |
| MFA (TOTP) | ✅ | Keycloak realm config — `bfp-realm.json` |
| PKCE auth flow | ✅ | `main.py` — `/api/auth/callback` with code_verifier |
| JWT `kid`, `iss`, `aud`, expiry validation | ✅ | `auth.py` — full validation chain |

**Verdict:** Complete. 5 FRS roles enforced at JWT + RLS layer.

### FR-4 Extension: Self-Service Profile (Module 12) ✅
**Added 2026-04-21 via cherry-pick of commit `9e0d657`**

|| Component | Status | Evidence |
|---|---|---|---|
| Self-service profile view | ✅ | `user.py` — GET `/api/user/me/profile` |
| Self-service profile update | ✅ | `user.py` — PATCH `/api/user/me` |
| Self-service password change | ✅ | `user.py` — PATCH `/api/user/me/password` (requires current PW + optional OTP) |
| Admin user onboarding | ✅ | `admin.py` — POST `/api/admin/users` (System Admin only) |
| Keycloak Admin SDK service | ✅ | `keycloak_admin.py` — client credentials grant |
| Frontend profile page | ✅ | `src/frontend/src/app/profile/page.tsx` |
| Frontend admin user management | ✅ | `src/frontend/src/app/admin/system/page.tsx` |
| Self-service role constraints | ✅ | Users cannot change their own role — enforced at API level |

**Note:** Self-service profile endpoints validate current password via Keycloak `bfp-client` before allowing password change. JWT bearer token confirms identity for profile updates — no password re-entry needed.

**Outstanding:** Test user passwords (`admin_test`, `encoder_test`, etc.) need to be reset in Keycloak Admin Console — current passwords unknown.

---

## FR-5: Threat Detection ⚠️

**Thesis claim:** Suricata IDS alerts consumed by Qwen2.5-3B XAI; human-readable forensic narratives

| Component | Status | Evidence |
|---|---|---|
| Suricata IDS | ✅ | `suricata/` — rules, logs, eve.json output |
| Suricata log ingestion | ✅ | `suricata_ingestion.py` — parses eve.json |
| Suricata Celery task | ✅ | `tasks/suricata.py` — periodic ingestion |
| AI service (Ollama) | ✅ | `ai_service.py` — calls Ollama API |
| Qwen2.5-3B model | ✅ | Docker `ollama` service, CLAUDE.md confirms |
| XAI narrative generation | ⚠️ | `ai_service.py` exists but narrative output pipeline unclear |
| Security threat log model | ✅ | `security_threat_log.py` — stores alerts + narratives |
| Admin threat analysis endpoint | ✅ | `admin.py` — POST `/security-logs/{id}/analyze` |
| Forensic narrative frontend | ❌ | No dedicated threat/XAI dashboard component found |

**Gaps:**
- [ ] Verify XAI narrative quality (MOS evaluation per NFR)
- [ ] Frontend threat analysis dashboard / narrative viewer
- [ ] End-to-end test: Suricata alert → Celery → Ollama → narrative → DB → API → frontend
- [ ] Inference latency profiling (NFR: <5s mean)

---

## FR-6: Forensic Reporting ⚠️

**Thesis claim:** Immutable timestamped audit logs; chain of custody; ISO 27001 + RA 10173 compliance

| Component | Status | Evidence |
|---|---|---|
| Audit log table | ✅ | `01_wims_initial.sql` — `wims.audit_log` table |
| Admin audit log endpoint | ✅ | `admin.py` — GET `/audit-logs` |
| Soft-delete (no hard deletes) | ✅ | Constitution rule, `deleted_at` columns |
| Timestamps (created_at, updated_at) | ✅ | All models have timestamp columns |
| AES-256-GCM encryption | ✅ | `utils/crypto.py` — encryption utilities |
| Chain of custody tracking | ⚠️ | `incident_verification_history.py` model exists but workflow unclear |
| Digital signatures | ❌ | No signing logic found in codebase |
| Export/report generation | ⚠️ | `tasks/exports.py` — CSV export exists, PDF/format unclear |
| Compliance documentation | ❌ | No ISO 27001 or RA 10173 mapping document in codebase |

**Gaps:**
- [ ] Digital signature implementation for critical records
- [ ] Chain of custody workflow validation (who verified what, when)
- [ ] Export format expansion (PDF reports for auditors)
- [ ] ISO 27001 control mapping document
- [ ] RA 10173 PII handling audit (encrypted fields verified)

---

## Summary Dashboard

| FR# | Requirement | Status | Blocker? |
|---|---|---|---|
| FR-1 | Crowdsourced Reporting | ✅ Complete | No |
| FR-2 | Geospatial Mapping | ⚠️ Partial | No (frontend map needed) |
| FR-3 | Data Synchronization | ❌ Not Started | **YES — C-1 thesis discrepancy** |
| FR-4 | Access Control | ✅ Complete | No |
| FR-5 | Threat Detection | ⚠️ Partial | No (end-to-end test needed) |
| FR-6 | Forensic Reporting | ⚠️ Partial | No (digital sigs + compliance docs) |

---

## Priority Queue (Defense-Ordered)

### P0 — CRITICAL (thesis defense blocker)
1. **FR-3: Offline Sync** — Decide: implement Service Worker + background sync OR reframe thesis language to "local queuing with manual sync"

### P1 — HIGH (defense expected)
2. **FR-2: Interactive Map** — Leaflet/Mapbox frontend component for PostGIS heatmaps
3. **FR-5: XAI E2E Test** — Validate full Suricata → Ollama → narrative → frontend pipeline
4. **FR-5: Inference Latency** — Profile and confirm <5s mean (NFR requirement)

### P2 — MEDIUM (defense nice-to-have)
5. **FR-6: Digital Signatures** — Implement signing for critical audit records
6. **FR-6: Compliance Mapping** — ISO 27001 + RA 10173 control matrix
7. **FR-2: Ref Endpoints** — Add `/api/ref/provinces` and `/api/ref/cities`

### P3 — LOW (post-defense)
8. **FR-6: PDF Export** — Auditor-ready report generation
9. **FR-5: Threat Dashboard** — Dedicated XAI narrative viewer UI

---

*This tracker should be updated as implementation progresses. Cross-reference with [[analyses/wims-bfp-thesis-codebase-gaps]] for discrepancy details.*
