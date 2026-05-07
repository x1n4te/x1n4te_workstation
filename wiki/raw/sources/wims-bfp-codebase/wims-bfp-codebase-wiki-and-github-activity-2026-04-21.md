# WIMS-BFP Codebase Wiki & GitHub Activity — 2026-04-21

> Raw capture of in-repo codebase wiki evolution and GitHub repository activity.
> Source: `~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/wiki/` + `gh` CLI + `git log`

---

## Codebase Wiki Status (in-repo)

**Location:** `~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/wiki/`
**Total pages:** 22 (codebase-local wiki, Karpathy LLM Wiki pattern)
**Initialized:** 2026-04-21
**SCHEMA:** Follows Karpathy pattern — YAML frontmatter, wikilinks, index backbone, append-only log

### Directory Structure
```
wiki/
├── SCHEMA.md, index.md, log.md
├── analyst-dashboard-queue.md (290 lines, 14 features, 4 phases)
├── module6-crypto-queue.md (12 features, 4+2 phases)
├── sprint-timeline.md, sprint-gantt.md
├── frs-modules.md, ci-cd-pipeline.md
├── development-setup.md, project-conventions.md
├── architecture-summary.md
├── raw/ (FRS modules 1-13, docs, specs, misc — 15+ files)
├── entities/ (7 pages: database-schema, api-endpoints, etc.)
├── concepts/ (9 pages: auth-flow, rls-model, spatial-data, etc.)
```

### Wiki Log Entries (chronological, all 2026-04-21)

1. **create** — Wiki initialized: 20 pages from existing docs/ files
2. **ingest** — FRS modules copied to raw/: 15 files, frs-modules.md tracking page
3. **plan** — Sprint timeline: 7→6 sprints (Apr 22–May 5), all 13 modules mapped
4. **audit** — Codebase verification of FRS modules: M1 90%, M2 30%, M5 HALF, M6 HALF, M7 HALF, M12 DONE, rest NOT STARTED
5. **plan** — Mermaid Gantt chart: 16 task sections across 6 sprints
6. **audit** — Module 2 deep audit: queue buffer (not DB mirror), offline encryption missing
7. **fix** — PostGIS location pin: backend query + frontend map component
8. **feature** — Wildland fire indicator + regional dashboard: is_wildland detection, 8 fire type counters
9. **test** — Analyst dashboard TDD suite: 80 tests, Red State 5% pass rate
10. **implementation** — Analyst dashboard all phases: 54/54 backend green (100%)
11. **implementation** — Analyst dashboard frontend: 87/87 full stack green (100%)
12. **skill** — karpathy-guidelines + analyst-dashboard-queue created
13. **planning** — Validated needs added: 31 team-validated features mapped to modules
14. **refactor** — CI/CD pipeline overhaul: ci.yml (6 jobs) + cd.yml (GHCR build)
15. **create** — Module 6 crypto queue: 12 features, 4 phases, 28 baseline tests

---

## GitHub Repository Activity

### Branch State (as of 2026-04-22 01:44)

**Local is AHEAD of origin/master by 5 commits** (not yet pushed):

| # | Commit | Description |
|---|--------|-------------|
| 1 | 309f300 | fix(CI): apply 05_analytics_facts_expand.sql + handle missing .env in docker build |
| 2 | 76a23e6 | fix(CI): resolve 5 backend test failures + update crypto queue plan |
| 3 | e5b7978 | chore: overhaul CI/CD pipeline, fix lint errors, pass frontend design tests |
| 4 | c3d2391 | feat(analyst): full analyst dashboard — filters, charts, exports, top-N, scheduled reports |
| 5 | 446bd06 | fix/incident-location-map |

**Untracked file:** `.wims-bfp-context.md` (project context isolation)

### Key Commit Details

**309f300 — CI fix (latest)**
- Added `05_analytics_facts_expand.sql` to backend test DB init
- Made `docker compose config --quiet` fail gracefully when .env missing
- Files: `.github/workflows/ci.yml` (1 file, +3/-1)

**76a23e6 — Backend test fixes + crypto queue expansion**
- Fixed 5 backend test failures: Keycloak resetPasswordAllowed, analytics test overrides, AFOR import ValueError propagation, PENDING_VALIDATION constraint
- Expanded module6-crypto-queue.md: Phase 5 (blob versioning, rollback) + Phase 6 (internal TLS, PII audit log)
- 197 tests passed, 15 skipped (environmental)
- Files: 18 changed, +454/-136 (regional.py, analytics.py, keycloak_admin.py, keycloak realm JSON, etc.)

**e5b7978 — CI/CD pipeline overhaul**
- Split monolithic CI into 6 jobs: security-audit, migrations, frontend, backend, docker-build, merge-gate
- Created cd.yml: GHCR image build (backend + frontend matrix)
- Added concurrency groups, pytest-cov 30% threshold, vitest to frontend job

**c3d2391 — Analyst dashboard (full feature)**
- Phase 1: 4 materialized views, schema expansion (8 new columns), Celery refresh task
- Phase 2: Casualty severity filter, damage range filter, type-distribution, top-barangays, response-time endpoints
- Phase 3: PDF + Excel export Celery tasks, analytics_export_log table with RLS
- Phase 4: Multi-region select, compare-regions, top-N configurable, scheduled reports CRUD
- Test results: 87/87 passing (100%) from 5% baseline

**446bd06 — PostGIS location pin fix**
- Backend: added ST_Y/ST_X query for latitude/longitude from PostGIS location column
- Frontend: added Leaflet map component on incident detail page

### Pull Requests (all 27)

| # | Title | Branch | Status | Date |
|---|-------|--------|--------|------|
| 27 | feat: Module 12 — system admin, user profiles, Suricata seeding | feature/sync-fixes | MERGED | 2026-04-21 |
| 26 | feature/module-4-import-and-validator-dashboard | feature/module-4-import-spreadsheet | MERGED | 2026-04-19 |
| 25 | fix(keycloak): restore deterministic realm users and roles | fix/auth-looping-keycloak-realm | CLOSED | 2026-04-16 |
| 24 | Fix/mfa login redirect loop issuer UUID | fix/mfa-login-redirect-loop-issuer-uuid | MERGED | 2026-04-16 |
| 23 | fix keycloak auth loop | fix/looping-auth | MERGED | 2026-04-16 |
| 22 | Feat/keycloak custom theme | feat/keycloak-custom-theme | MERGED | 2026-04-10 |
| 21 | Fix/auth loop database refactor | fix/auth-loop-database-refactor | MERGED | 2026-04-09 |
| 20 | Fix/audit remediation cr1 cr2 | fix/audit-remediation-cr1-cr2 | MERGED | 2026-04-04 |
| 1-8 | Earlier: schema validation, CI setup, RLS enforcement, linting | various | MERGED | 2026-03-14 to 2026-04-03 |

### Open Security Issues (8 OPEN)

| Severity | ID | Title |
|----------|-----|-------|
| HIGH | #15 | system_audit_trails: wims_app blanket INSERT grant breaks chain-of-custody |
| HIGH | #14 | incident_sensitive_details allows plaintext PII in legacy fields |
| HIGH | #12 | security_threat_logs: GUC unset path allows unattributed INSERT |
| MEDIUM | #16 | ref_* geography tables lack RLS — enables reconnaissance |
| MEDIUM | #13 | citizen_reports: WITH CHECK re-validates incident_id region, NULL transition unhandled |
| LOW | #18 | system_audit_trails ip_address and user_agent lack length constraints |
| LOW | #17 | wims_app granted unnecessary DELETE on all tables |

### Closed Critical Issues

| ID | Title | Closed |
|----|-------|--------|
| #11 | [CRITICAL-2] Duplicate 'SYSTEM_ADMIN' in every IN clause | 2026-04-04 |
| #10 | [CRITICAL-1] RLS bypass: wims.current_user_role() returns NULL | 2026-04-04 |
| #9 | [CRITICAL-1] RLS bypass (duplicate) | 2026-04-04 |

### Remote Branches (16)

Active local branches: `feature/analyst-CRUD` (current), `master`, plus 13 fix/feat/infra branches
Remote: `origin` → `https://github.com/x1n4te/WIMS-BFP-PROTOTYPE.git`

---

## FRS Module Status Update

| Module | Previous Status | Current Status | Change |
|--------|----------------|----------------|--------|
| 5 — Analytics | HALF | **DONE** | Analyst dashboard 87/87 tests green |
| 6 — Crypto | HALF | HALF (expanded) | Queue now has 6 phases, 17 features |

All other modules unchanged from previous audit.

---

## Diff Summary (local vs origin/master)

- **130 files changed**, +3,038 insertions, -15,928 deletions
- Major additions: analytics materialized views, export tasks, scheduled reports, CI/CD overhaul
- Major deletions: likely cleanup of old/unused code
