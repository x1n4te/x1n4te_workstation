---
id: wims-bfp-codebase-wiki-github-activity-2026-04-21
type: source
created: 2026-04-22
updated: 2026-04-22
last_verified: 2026-04-22
review_after: 2026-06-22
stale_after: 2026-10-22
confidence: high
source_refs:
  - raw/sources/wims-bfp-codebase/wims-bfp-codebase-wiki-and-github-activity-2026-04-21.md
status: active
tags:
  - wims-bfp
  - devops
  - operational
  - analysis
related:
  - concepts/wims-bfp-frs-modules
  - concepts/wims-bfp-ci-cd-pipeline
  - concepts/wims-bfp-sprint-timeline
  - analyses/wims-bfp-frs-implementation-tracker
  - entities/wims-bfp-codebase-database-schema
---

# WIMS-BFP Codebase Wiki & GitHub Activity — 2026-04-21/22

Comprehensive capture of in-repo codebase wiki evolution and GitHub repository activity during the sprint planning and analyst dashboard implementation phase.

## Codebase Wiki (in-repo)

**Location:** `~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/wiki/`
**Pattern:** Karpathy LLM Wiki — 22 pages, YAML frontmatter, wikilinks, append-only log
**Initialized:** 2026-04-21 (same day as main LLM wiki integration)

### Wiki Structure

The in-repo wiki mirrors the codebase architecture:
- **Entity pages** (7): database-schema, api-endpoints, docker-services, frontend-pages, init-scripts, keycloak-config, rbac-roles
- **Concept pages** (9): auth-flow, rls-model, spatial-data, data-flow, xai-pipeline, pii-encryption, threat-model, offline-pwa, afor-import
- **Reference pages** (6): frs-modules, sprint-timeline, sprint-gantt, ci-cd-pipeline, development-setup, project-conventions
- **Task queues** (2): analyst-dashboard-queue (14 features), module6-crypto-queue (12 features)

### Key Wiki Events (all 2026-04-21)

1. **Wiki initialized** — 20 pages from existing docs/ files, Karpathy pattern applied
2. **FRS audit** — all 13 modules verified against actual codebase: M1 90%, M2 30%, M5 HALF, M6 HALF, M7 HALF, M12 DONE, 7 modules NOT STARTED
3. **Module 2 deep audit** — clarified offline store is queue buffer (not DB mirror), corrected architecture interpretation across sprint docs
4. **PostGIS location pin fix** — backend added ST_Y/ST_X query, frontend added Leaflet map component
5. **Wildland fire indicator** — is_wildland detection via incident_wildland_afor join, 8 fire type counters in regional dashboard
6. **Analyst dashboard TDD** — 80 baseline tests (54 backend + 26 frontend), Red State at 5% pass rate
7. **Analyst dashboard COMPLETE** — all 4 phases implemented: 87/87 tests green (100%)
8. **CI/CD pipeline overhaul** — ci.yml split into 6 jobs, cd.yml created for GHCR builds
9. **Module 6 crypto queue** — 12 features in 4 phases, later expanded to 6 phases (17 features)
10. **Team validated needs** — 31 features mapped across 5 roles (GWEN, RED, EARL, NATHAN)

## GitHub Repository

**Repo:** `x1n4te/WIMS-BFP-PROTOTYPE` (origin/master)
**Local state:** 5 commits ahead of origin/master (analyst dashboard + CI fixes not pushed yet)

### Unpushed Commits

1. `309f300` — fix(CI): apply analytics facts expansion SQL + handle missing .env
2. `76a23e6` — fix(CI): resolve 5 backend test failures + expand crypto queue
3. `e5b7978` — chore: CI/CD pipeline overhaul (6 jobs + CD)
4. `c3d2391` — feat(analyst): full analyst dashboard (87/87 tests green)
5. `446bd06` — fix/incident-location-map (PostGIS + Leaflet)

### Pull Request Activity

- **27 total PRs**, 20 MERGED, 4 CLOSED, 3 not listed as open
- Recent merges: PR #27 (Module 12 user mgmt), PR #26 (Module 4 import), PR #24 (MFA redirect fix), PR #23 (Keycloak auth loop), PR #22 (custom theme)
- All critical auth/RLS issues resolved (PRs #20-#24)

### Open Security Issues (8)

- **HIGH (3):** #15 audit_trails INSERT grant, #14 plaintext PII in legacy fields, #12 security_threat_logs GUC bypass
- **MEDIUM (2):** #16 ref_* geography tables lack RLS, #13 citizen_reports NULL transition
- **LOW (2):** #18 audit_trails length constraints, #17 wims_app unnecessary DELETE grants
- **Critical resolved:** #9, #10, #11 all CLOSED (RLS bypass + duplicate SYSTEM_ADMIN)

### Diff vs Remote

- **130 files changed**, +3,038 / -15,928 lines
- Major: analytics materialized views, export tasks, scheduled reports, CI/CD, regional.py expansion

## Module Status Changes

| Module | Before | After | Evidence |
|--------|--------|-------|----------|
| 5 — Analytics | HALF | **DONE** | 87/87 tests, materialized views, 5 chart types, PDF/Excel export, scheduled reports |
| 6 — Crypto | HALF | HALF+ | Queue expanded from 4→6 phases (added blob versioning, TLS, PII audit) |

## Architectural Clarifications Recorded

1. **Module 2 offline store** = queue buffer, NOT database mirror. Encoders queue incidents offline → IndexedDB → flush on reconnect → backend is source of truth.
2. **"Offline CRUD"** = queue management (view/edit/delete queued items), not full offline database operations.
3. **Wildland fire AFOR** = distinct from standard structural AFOR, stored in `incident_wildland_afor` table, classified by 8 fire types.

## Related

- [[concepts/wims-bfp-frs-modules]] — updated module tracker
- [[concepts/wims-bfp-ci-cd-pipeline]] — new CI/CD documentation
- [[concepts/wims-bfp-sprint-timeline]] — sprint plan (Apr 22–May 5)
- [[analyses/wims-bfp-frs-implementation-tracker]] — FRS tracker (needs Module 5 update)
- [[mocs/wims-bfp]] — master entry point
