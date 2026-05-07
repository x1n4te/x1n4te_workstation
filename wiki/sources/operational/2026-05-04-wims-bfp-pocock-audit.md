---
title: "WIMS-BFP — Pocock Architecture Audit PRD (2026-05-04)"
date: 2026-05-04
tags: [wims-bfp, pocock, architecture, refactor, prd, deep-module, outsterhout]
confidence: high
reviewed: 2026-05-04
source: local-codebase + matt-pocock-improve-codebase-architecture transcript
author: Ares (Orchestrator)
project: WIMS-BFP
related:
  - "[[sources/operational/2026-05-04-wims-bfp-earl-branch-spec-audit]]"
  - "[[sources/operational/2026-05-04-wims-bfp-earl-branch-review]]"
  - "[[concepts/improve-codebase-architecture-skill]]"
  - "[[raw/transcripts/matt-pocock-improve-codebase-architecture-2026]]"
---

# WIMS-BFP — Pocock Architecture Audit PRD

**Audit Standard:** John Ousterhout *A Philosophy of Software Design* (2nd Ed.) + Matt Pocock `improve-codebase-architecture` skill
**Phase:** Phase 1 (Explore) complete → Phase 2 (PRD) delivered, awaiting implementation
**Scan scope:** 3,158 source files (backend + frontend, excluding venv/node_modules)
**User philosophy:** "Make it work → then refactor." Simple, straight-to-point implementation.

---

## Codebase Structure (Pre-Split)

```
Backend Routes (10 files, 4,759 LOC)
├── regional.py      3,326 LOC  ← LARGEST SHALLOW MODULE
├── admin.py           723 LOC
├── incidents.py       525 LOC
├── analytics.py        373 LOC
├── user.py            231 LOC
├── triage.py          226 LOC
├── public_dmz.py      204 LOC
├── ref.py              97 LOC
├── civilian.py         93 LOC
└── sessions.py         60 LOC

Backend Services (4 files, 1,135 LOC)
├── analytics_read_model.py   649 LOC
├── keycloak_admin.py         272 LOC
├── suricata_ingestion.py      116 LOC
└── ai_service.py              98 LOC

Frontend lib/ (7 files, 1,434 LOC)
├── api.ts              809 LOC  (entire backend surface)
├── api.test.ts         520 LOC
├── afor-utils.ts       219 LOC
├── syncEngine.ts       154 LOC  (offline sync + LWW conflict)
├── edgeFunctions.ts    172 LOC
├── validator-api.ts    124 LOC
└── auth.tsx             73 LOC

Frontend components (8 files, 3,518 LOC)
├── IncidentForm.tsx          1,646 LOC
├── WildlandAforManualForm      927 LOC
├── MapPickerInner               275 LOC
└── [Sidebar, Header, SyncStatusBar, LayoutShell, NetworkStatusIndicator]

Dual Auth Providers
├── context/AuthContext.tsx     214 LOC  (OIDC userManager + proactive JWT refresh)
└── lib/auth.tsx                73 LOC  (UserProfileProvider, /api/auth/session fetch)
```

---

## Candidates — Ranked by Leverage

| Rank | Candidate | Problem | Files | Effort | Priority |
|------|-----------|---------|-------|--------|----------|
| **A** | `regional.py` split | 3,326-line shallow module, 71 fns/classes, impossible to navigate | 1 file | High | **SELECTED** |
| **B** | Analytics logging + batch | `except: pass` silent failure; N+1 batch queries | 1 file | Low | **CRITICAL** |
| **C** | Dual AuthProvider seam | Two providers, no shared interface, tab-switch state loss risk | 2 files | Medium | Deferred |
| **D** | `api.ts` OpenAPI contract | No automated type contract between frontend/backend | 1 file | Medium | Deferred |
| **E** | `audit.py` verification | Called by routes but existence not confirmed | 1 file | Low | Quick check |

---

## Candidate A (SELECTED): `regional.py` Split

### Problem

`backend/api/routes/regional.py` (3,326 LOC) contains **71 discrete functions/classes** in a single file:

- **AFOR Parsing (3 parsers):** `BfpXlsxParser`, `WildlandXlsxParser`, `CsvWorksheetAdapter`
- **Utility helpers:** `_wgs84_pair_from_raw`, `_safe_int`, `_safe_float`, `_safe_dt`, `_normalize_general_category`, `_column_letters_to_index`
- **Compatibility shims:** `_incident_verification_history_uses_target_columns`, `_incident_verification_history_has_column`
- **Business logic:** `_insert_incident_verification_history`, `_commit_wildland_afor_row`
- **AFOR pipeline:** `detect_afor_template_kind`, `_pick_structural_worksheet`, `_pick_wildland_worksheet`, `parse_wildland_afor_report_data`, `parse_afor_report_data`, `parse_csv_content`, `parse_xlsx_content`
- **HTTP handlers (10 endpoints):** `import_afor_file`, `commit_afor_import`, `get_regional_incidents`, `get_regional_incident_detail`, `get_validator_stats`, `get_regional_stats`, `create_incident`, `update_incident`, `unpend_incident`, `delete_incident`, `submit_incident_for_review`, `get_validator_incident_queue`, `verify_incident`
- **All Pydantic schemas:** Inline with no separation

**Friction signals:**
- Change `verify_incident()` → must read 3,326 lines
- AFOR parsers deeply interleaved with HTTP handlers — no clean seam
- The file is the module — no interface surface to test against
- Ousterhout's 3 causes of complexity all present: change amplification (touch one, fear all), cognitive load (71 things to hold), unknown unknowns (who calls what)

### Confirmed Designs

| Design | Approach | Pros | Cons |
|--------|----------|------|------|
| **A — Minimum** | 4 files: `afor_parsers.py`, `incident_crud.py`, `schemas/regional.py`, `routes/regional.py` | Maximum depth, 1-3 entry points | Less flexibility for callers |
| **B — Flexibility** | Same split but typed functions per operation | More entry points, more control | Shallow interfaces if over-extracted |
| **C — Practical Efficiency** (RECOMMENDED) | `afor_pipeline.py` = parse+commit in one; `verify_incident` gets own deep module | Matches AFOR import flow, matches "make it work → refactor" | Slightly more surface area |
| **D — Ports & Adapters** | Abstract `afor_port.py` + `xlsx/csv` adapters | Most testable | Most verbose, over-engineered for thesis |

**User selected:** Design C — Practical Efficiency (2026-05-04)
**Implementation status:** SPLIT COMPLETE (2026-05-04)

### Target Architecture (Design C — Implemented)

```
backend/
├── api/routes/regional.py          # Thin HTTP layer — 283 LOC (was 3,326)
├── schemas/
│   ├── __init__.py                  # Re-exports
│   └── regional.py                  # All Pydantic models — 192 LOC
├── services/
│   ├── afor_parsers.py              # Pure parse logic — 1,185 LOC
│   ├── afor_pipeline.py             # Parse+commit orchestration — 540 LOC
│   ├── incident_crud.py             # Business logic — 1,592 LOC
│   └── analytics_read_model.py      # [N+1 batch fix applied]
```

### Implementation Order

1. Extract `schemas/regional.py` first (most independent, no business logic) ✅
2. Extract `afor_parsers.py` (pure functions, no FastAPI) ✅
3. Extract `incident_crud.py` (needs schemas + afor_parsers) ✅
4. Extract `afor_pipeline.py` (parse+commit orchestration) ✅
5. Thin `routes/regional.py` to HTTP handlers only ✅

---

## Candidate B: Analytics Read Model — Silent Failure + N+1

### Problem 1 — Silent Sync Failure

**File:** `backend/services/analytics_read_model.py`
**Location:** `sync_incident_to_analytics()` called from `verify_incident()` in `regional.py`

```python
# CURRENT (line ~17-113):
try:
    # ... sync logic ...
except:  # ← silently swallows all errors
    pass
```

**Risk:** If analytics sync fails post-incident verification, National Analyst dashboard shows stale/missing data with zero indication. This is the `except: pass` pattern identified in the SPEC audit.

**Fix:**
```python
except Exception as e:
    logger.warning("Analytics sync failed for incident %s: %s", incident_id, e)
    # Verification commit already succeeded — this is non-blocking
```

### Problem 2 — N+1 Batch Queries

**File:** `backend/services/analytics_read_model.py`
**Location:** `sync_incidents_batch()` lines 116-119

```python
# CURRENT:
def sync_incidents_batch(db: Session, incident_ids: list[int]) -> None:
    for iid in incident_ids:
        sync_incident_to_analytics(db, iid)  # N round-trips
```

**Risk:** For a 100-row AFOR bulk import, this generates 100 separate DB queries + commits instead of 1.

**Fix (straight to point — single INSERT ... ON CONFLICT with unnest):**
```python
def sync_incidents_batch(db: Session, incident_ids: list[int]) -> None:
    if not incident_ids:
        return
    # Single query: upsert all VERIFIED incidents via unnest
    db.execute(
        text("""
            INSERT INTO wims.analytics_incident_facts
                (incident_id, region_id, location, notification_dt, notification_date,
                 alarm_level, general_category,
                 civilian_injured, civilian_deaths, firefighter_injured, firefighter_deaths,
                 total_response_time_minutes, estimated_damage_php,
                 fire_station_name, barangay_name)
            SELECT
                fi.incident_id, fi.region_id, fi.location,
                nd.notification_dt, nd.notification_dt::date,
                nd.alarm_level, nd.general_category,
                COALESCE(nd.civilian_injured, 0), COALESCE(nd.civilian_deaths, 0),
                COALESCE(nd.firefighter_injured, 0), COALESCE(nd.firefighter_deaths, 0),
                nd.total_response_time_minutes, nd.estimated_damage_php,
                nd.fire_station_name, rb.barangay_name
            FROM wims.fire_incidents fi
            LEFT JOIN wims.incident_nonsensitive_details nd ON nd.incident_id = fi.incident_id
            LEFT JOIN wims.ref_barangays rb ON rb.barangay_id = nd.barangay_id
            WHERE fi.incident_id = ANY(:ids)
              AND fi.verification_status = 'VERIFIED'
              AND fi.is_archived = FALSE
            ON CONFLICT (incident_id) DO UPDATE SET
                region_id = EXCLUDED.region_id,
                location = EXCLUDED.location,
                notification_dt = EXCLUDED.notification_dt,
                notification_date = EXCLUDED.notification_date,
                alarm_level = EXCLUDED.alarm_level,
                general_category = EXCLUDED.general_category,
                civilian_injured = EXCLUDED.civilian_injured,
                civilian_deaths = EXCLUDED.civilian_deaths,
                firefighter_injured = EXCLUDED.firefighter_injured,
                firefighter_deaths = EXCLUDED.firefighter_deaths,
                total_response_time_minutes = EXCLUDED.total_response_time_minutes,
                estimated_damage_php = EXCLUDED.estimated_damage_php,
                fire_station_name = EXCLUDED.fire_station_name,
                barangay_name = EXCLUDED.barangay_name,
                synced_at = now()
        """),
        {"ids": incident_ids}
    )
    db.commit()
```

---

## Candidate C: Dual AuthProvider Seam (DEFERRED)

**Files:** `frontend/src/context/AuthContext.tsx` + `frontend/src/lib/auth.tsx`

Both providers received JWT refresh fixes in PRs #92/#93 but there is no shared interface contract. Pages using the wrong provider lose session silently.

**Fix:** `hooks/useAuth.ts` wrapping both providers behind one interface. Pages import from `useAuth` — they don't know which provider is underneath.

**Status:** Deferred past thesis defense.

---

## Candidate D: `api.ts` OpenAPI Contract (DEFERRED)

**File:** `frontend/src/lib/api.ts` (809 LOC)

Backend has Pydantic schemas in `backend/schemas/`. Frontend has TypeScript types in `frontend/src/types/api.ts`. No automated enforcement that they stay in sync.

**Fix:** Add build step that generates TypeScript from FastAPI `openapi.json` at build time.

**Status:** Deferred.

---

## Candidate E: `utils/audit.py` Verification

**File:** `backend/utils/audit.py`

`log_system_audit` is imported in `regional.py` and `admin.py` but actual implementation not verified during audit.

**Status:** Quick check — does file exist with correct interface?

---

## Implementation Priority

| Order | Candidate | Effort | Dependency | Blocked by |
|-------|-----------|--------|------------|------------|
| 1 | Candidate B (analytics logging + batch) | 1 session | None | No |
| 2 | Candidate A (`regional.py` split) | Multi-session | Design decision | User choice A/B/C |
| 3 | Candidate C (AuthProvider seam) | 2-3 sessions | None | Can run parallel to A |
| 4 | Candidate D (OpenAPI contract) | 2 sessions | None | Deferred |
| 5 | Candidate E (`audit.py` check) | 10 min | None | No |

---

## Verification Checklist (Post-Implementation)

After each candidate:
- [ ] Deletion test: deleting the new module recreates complexity across N callers → deep ✅
- [ ] All existing tests still pass
- [ ] No `except: pass` remaining in refactored modules
- [ ] Wiki pages updated with new module names and interface signatures
