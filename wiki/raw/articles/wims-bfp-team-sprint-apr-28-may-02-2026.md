# WIMS-BFP Team Sprint — Apr 28 – May 2, 2026

**Source:** GitHub API (`x1n4te/WIMS-BFP-PROTOTYPE`)  
**Date:** 2026-05-02  
**Type:** operational  
**Confidence:** high  

---

## Team Composition & Contributions

| Member | GitHub Handle(s) | Role | Commits (Recent Sprint) |
|--------|----------------|------|------------------------|
| Natekatsu / x1n4te | x1n4te | Lead Architect, DevSecOps | 41 (total repo) |
| Guinevere T. Tendero | G10dero, laqqui | Module 2 (Incident Workflow) | 3 |
| Earl Justin P. Camama | orljorstin | Module 4 (Import + Validator Dashboard) | 3 |
| Red Gabrielle A. Dela Cruz | ShibaTheShiba | Auth / Session Management | 1 (recent) |

**Total contributors:** 4 (+ Earl from INB-Nathan fork, x1n4te is xynate)

---

## Open PRs

### PR #78 — `feature/analyst-CRUD` — National Analyst CRUD *(OPEN, mergeable)*
**Author:** x1n4te  
**Size:** +5258 / -2036 lines, 60 files  
**Description:** National Analyst role: dashboard, PostGIS heatmaps, CSV/Excel/PDF exports, Celery beat scheduled reports, self-service profile. Rebased on master post-PR-77.  
**Status:** CI green, draft-ready for review.

---

### PR #79 — `feat/module-2-incident-workflow` — M4 Incident Workflow Checkpoint *(OPEN, mergeable)*
**Author:** laqqui  
**Size:** +4558 / -1329 lines, 29 files  
**Description:** Checkpoint PR documenting the currently implemented slice of M4 (incident creation, edit, draft save, validator verification queue) and listing 10 intentionally deferred items.

**What works:**
| M4 Item | Status |
|---------|--------|
| M4-A Incident creation with PostGIS location | ✅ Met |
| M4-B Incident edit for own non-verified incidents | ✅ Mostly met |
| M4-E Draft save | ✅ Met |
| M4-F Validator verification queue | ✅ Mostly met |

**Intentionally deferred (10 items):**
1. Edit audit trail entry
2. Duplicate detection on import
3. Diff view
4. Bulk approve
5. Validator audit trail viewer
6. Regional RBAC enforcement (encoders can encode outside assigned region)
7. AFOR accuracy updates
8. Civilian + encoder incident merging
9. Wildland workflow
10. Incident creation does not enforce `region_id` matches assigned region

**Notable gap:** Backend verification history helper exists but create/edit/draft actions don't write history rows yet.

---

### PR #77 — `fix/init-auth-fix-no-loop` *(MERGED — Apr 28, 2026)*
**Author:** G10dero  
**Sprint impact:** Fixed init auth no-loop, incident location map.

---

## Key Architectural Decisions (Recent)

### 1. Strict FRS Role Enforcement (Post-PR #20/#21)
- All RLS policies now use only the 5 strict FRS role literals: `CIVILIAN_REPORTER`, `REGIONAL_ENCODER`, `NATIONAL_VALIDATOR`, `NATIONAL_ANALYST`, `SYSTEM_ADMIN`
- Deprecated aliases (`ADMIN`, `ANALYST`, `ENCODER`, `VALIDATOR`) removed from all policies and application code
- `users_role_check` CHECK constraint enforces the 5-role set at DB level
- `wims.current_region_id()` added as alias for `wims.current_user_region_id()`

### 2. MFA Auth Flow (Keycloak 26, Conditional OTP)
- KC 26.6.0 upgrade — fresh install fixes CONFIGURE_TOTP alias (null in KC 24)
- `browser-with-mfa` flow: Cookie [ALT] → Username/Password [REQ] → OTP Form [REQ]
- `CONFIGURE_TOTP` set as defaultAction — forces TOTP enrollment on first login
- 5 stacked bugs fixed in MFA login loop (issuer port, theme JS, stale UUIDs, session race, JWKS key rotation)

### 3. Keycloak Custom Theme — `wims-bfp`
- BFP maroon/white branding
- `loginTheme=wims-bfp` persisted in `bfp-realm.json`
- Volume mount: `./keycloak/themes/wims-bfp:/opt/keycloak/themes/wims-bfp:ro`

### 4. Session Management — Backchannel Logout *(branch: `sessionManagement/red`)*
**Author:** ShibaTheShiba  
- `feat(auth): implement session management — backchannel logout and admin session governance`
- Implements OIDC backchannel logout + admin session governance controls

### 5. RLS Wired on All Protected Routes
- `get_db()` → `get_db_with_rls()` on all protected endpoints
- Auth dependency resolves BEFORE `get_db_with_rls` so `request.state.wims_user` is populated
- 21 endpoints across: ref.py, incidents.py, regional.py, triage.py, admin.py, analytics.py

### 6. Regional Encoder CRUD (Module)
- `POST /api/regional/incidents` — create DRAFT with PII-encrypted sensitive details
- `PUT /api/regional/incidents/{id}` — update DRAFT/PENDING/REJECTED, PII re-encryption on merge
- `DELETE /api/regional/incidents/{id}` — soft-delete (is_archived=TRUE)

---

## Active Branches

| Branch | Owner | Description |
|--------|-------|-------------|
| `feat/module-2-incident-workflow` | laqqui (Guinevere T. Tendero) | M4 incident workflow (PR #79) |
| `feature/analyst-CRUD` | x1n4te | National Analyst CRUD (PR #78) |
| `fix/init-auth-fix-no-loop` | laqqui (Guinevere T. Tendero) | Auth fix (merged PR #77) |
| `fix/module-2-import-module-accuracy` | laqqui (Guinevere T. Tendero) | AFOR accuracy improvements |
| `sessionManagement/red` | ShibaTheShiba (Red Gabrielle A. Dela Cruz) | Backchannel logout + session governance |

---

## Schema Changes Summary (Recent Commits)

### `postgres-init/01_wims_initial.sql` — Critical Fixes
1. FRS roles moved to line ~13 (before any `CREATE POLICY ... TO <role>`)
2. `wims.current_region_id()` added at line ~460 (after `current_user_region_id()`)
3. All deprecated role literals replaced with strict FRS names
4. `pgcrypto` extension added (`gen_random_uuid()`)
5. Child table RLS split into per-operation policies (SELECT / INSERT / UPDATE / DELETE)
6. `wims_app` role created before GRANT statements

### `postgres-init/04_wims_auth_indexes.sql`
- `idx_wims_users_keycloak_id` — single column
- Composite `idx_wims_users_keycloak_id_active` — covers `is_active=TRUE` filter
- FK indexes on all child tables (eliminates seq scans)

---

## Related Wiki Entries

- [[entities/WIMS-BFP]] — project entity
- [[concepts/WIMS-BFP-RBAC-Model]] — current FRS role model
- [[concepts/WIMS-BFP-Auth-Flow]] — Keycloak MFA + JWT flow
- [[concepts/WIMS-BFP-RLS-Model]] — RLS enforcement architecture
- [[concepts/WIMS-BFP-FRS-Modules]] — 13-module tracker
- [[analyses/wims-bfp-thesis-codebase-gaps]] — thesis vs codebase discrepancy
- [[sources/wims-bfp-codebase]] — codebase ingestion (Apr 21)
