---
id: 2026-05-03-wims-bfp-pr78-pr83-integration-details
type: source
created: 2026-05-03
updated: 2026-05-03
last_verified: 2026-05-03
review_after: 2026-06-02
stale_after: 2026-08-01
confidence: high
source_refs:
  - sources/operational/2026-05-03-wims-bfp-pr78-pr83-integration-closeout
  - sources/operational/2026-05-03-wims-bfp-session-handoff-archive
status: active
tags:
  - wims-bfp
  - operational
  - ci-cd
  - auth
  - jwt
  - keycloak
  - nextjs
  - postgresql
  - testing
  - github
related:
  - mocs/wims-bfp
  - concepts/wims-bfp-ci-cd-pipeline
  - concepts/wims-bfp-codebase-auth-flow
  - concepts/wims-bfp-frs-modules
---

# WIMS-BFP PR #78–#83 Integration Details — May 3, 2026

Detailed record for [[sources/operational/2026-05-03-wims-bfp-pr78-pr83-integration-closeout]]. Archive snapshot: [[sources/operational/2026-05-03-wims-bfp-session-handoff-archive]]. Navigation: [[mocs/wims-bfp]], [[concepts/wims-bfp-ci-cd-pipeline]], [[concepts/wims-bfp-codebase-auth-flow]].

---

## Session Governance / PR #82

- PR: https://github.com/x1n4te/WIMS-BFP-PROTOTYPE/pull/82
- Author: ShibaTheShiba
- Branch: `sessionManagement/red`
- Merge commit: `ced6381dcd294a48a6dda76a72ca70710307c7aa`
- CI at merge: all green
- Merged by x1n4te using admin squash merge

### Conflict Resolution Summary

- Merged `master` (`d054d59`) into `sessionManagement/red`.
- Resolved conflicts in:
  - `src/backend/main.py`
  - `src/backend/services/keycloak_admin.py`
  - `src/frontend/src/lib/api.ts`
- Rejected PR #82's 60-minute `accessTokenLifespan` workaround.
- Kept 5-minute access tokens (300s) with proactive refresh via `/api/auth/refresh`.
- Added ruff format fix (`53a6d76`) to pass CI format gate.

### Key Files

- `src/frontend/src/app/api/auth/refresh/route.ts`
- `src/frontend/src/context/AuthContext.tsx`
- `src/frontend/src/app/api/auth/sync/route.ts`
- `src/frontend/src/app/callback/page.tsx`
- `src/backend/main.py`
- `src/keycloak/bfp-realm.json` — 300s access token / 28800s session

### Preserved Features

- Backchannel logout after password change.
- Backchannel logout after admin role change.
- Admin sessions API: `/api/admin/sessions/...`.
- Admin System Hub active-session metric/modal/terminate-all UI.

### QA Flag

PR #82 uses master admin credentials (`KEYCLOAK_ADMIN_USER` / `KEYCLOAK_ADMIN_PASSWORD`) for the Keycloak admin service. This was accepted as a dev/local operational expedient. Long-term secure alternative: least-privileged service account.

---

## Master Schema State After PR #78

PR #78 introduced modular SQL initialization and became the schema foundation for later PRs. Deterministic lexical init order:

| File | Role |
|------|------|
| `00_keycloak_bootstrap.sql` | Fresh Keycloak database creation |
| `01_extensions_roles.sql` | PostGIS + pgcrypto + 6 FRS roles + `wims_app` |
| `02_ref_geography.sql` | Province/city/barangay FK cascade |
| `03_users.sql` | User model |
| `04_import_incidents.sql` | fire_incidents + nonsensitive FK |
| `04a_fire_incidents_composite_index.sql` | Composite index |
| `05_citizen_reports.sql` | Citizen report table |
| `06_incident_details.sql` | Sensitive + nonsensitive details |
| `07_wildland_afor.sql` | Wildland AFOR tables |
| `08_security_audit.sql` | Security + audit tables |
| `09_rls_helpers.sql` | GUC helpers |
| `10_rls_policies.sql` | Comprehensive RLS policies |
| `11_analytics_facts.sql` | `analytics_incident_facts` table |
| `12_analytics_mvs.sql` | 4 materialized views |
| `13_export_reports.sql` | Export audit log + scheduled reports |
| `14_seed_ncr.sql` | NCR region seed |
| `15_validator_workflow.sql` | Validators + RLS UPDATE policy |
| `16_fix_ivh_legacy.sql` | Legacy IVH compatibility |

The schema is intended to be idempotent and lexically ordered. Later overlays from PR #79 had to be renamed to avoid stale pre-PR-78 ordering assumptions.

---

## PR #79 — Module 2 Incident Workflow Checkpoint

- PR: `feat/module-2-incident-workflow`
- Author: laqqui / Guinevere T. Tendero
- Merge commit on master: `d054d5988b6dab6df31ff021c3c3a6f217194f05`
- GitHub final state: `MERGED`
- Merged at: 2026-05-02T12:13:26Z

### Source-of-Truth Findings

- PR #79 was a checkpoint PR, not full M4 completion.
- Implemented:
  - encoder create/edit/drafts
  - validator queue/approve/reject
  - incident detail UI
  - AFOR import path
  - auth/JWKS improvements
- Intentionally still open/deferred:
  - duplicate detection
  - diff view
  - true regional RBAC enforcement
  - civilian/encoder merge model
  - wildland workflow depth
  - regional `region_id` enforcement
- The alleged `nd.barangay` critical bug was not present in the live branch. It was stale or already fixed.

### Conflict Resolution Applied

Merge base: `origin/master` at `edd2394` after PR #78 and PR #81 landed.
Conflict-resolution commit pushed as `5eeddf4`.

Resolved decisions:

- `src/backend/api/routes/regional.py`
  - Kept PR #79 `get_current_wims_user` import required by incident detail route.
  - Combined rejection-history response fields with master wildland AFOR indicator fields.
  - Kept `nonsensitive` enrichment (`city_municipality`, `province_district`).
  - Added `is_wildland`, `wildland_fire_type`, `wildland_area_hectares`, `wildland_area_display`.
  - Fixed merged wildland stats query to scope by `encoder_id`, not undefined `region_id`.
  - Kept unpend behavior: set `verification_status='DRAFT'` plus `updated_at=now()`.
- `src/backend/api/routes/user.py`
  - Security winner: kept master CRIT-0 restriction; self-service profile update cannot modify government email.
- `src/backend/services/keycloak_admin.py`
  - Kept admin email-update capability, but preserved comment that self-service routes must never pass email.
- Analytics tests
  - Removed stale `get_db` imports.
  - Tests override `get_db_with_rls` only.
- Frontend regional pages
  - Combined detail/edit flow with master wildland badge and wildland detail rows.
  - Combined rejected-incident alert with master 5-card wildland stats layout.
- SQL init conflicts
  - Kept PR #78 modular schema as authoritative.
  - Deleted stale `03_seed_reference.sql` reintroduction.
  - Renamed stale PR #79 SQL overlays for correct lexical order:
    - `07_m4_incident_scope.sql` → `10a_m4_incident_scope.sql`
    - `08_assign_ncr_to_test_users.sql` → `14a_assign_ncr_to_test_users.sql`
  - Fixed invalid PostgreSQL syntax: use `DROP POLICY IF EXISTS <policy> ON <table>`, not `ALTER TABLE <table> DROP POLICY`.

### PR #79 Verification

Commands/results:

- `python -m py_compile src/backend/api/routes/regional.py src/backend/api/routes/user.py src/backend/services/keycloak_admin.py src/backend/tests/integration/test_analytics_security.py` — PASS
- Targeted regression tests:
  - `test_analytics_heatmap_uses_read_model` — PASS
  - `test_heatmap_incident_type_and_alarm_level_passed_as_bound_parameters_not_sql_concat` — PASS
  - `test_regional_import_ambiguous_returns_400` — PASS
- Full analytics API/security tests: `41 passed` — PASS
- Ruff on touched backend files — PASS
- Frontend `npx tsc --noEmit` reported pre-existing unrelated TS errors only.

### Test Fixes Applied

- Commit `673f4a2` — `fix(regional): propagate ValueError detail in AFOR import`
  - `regional.py:1382`: changed generic `Unrecognized AFOR file format` to `str(e)`.
  - Fixed `test_regional_import_ambiguous_returns_400`.
- Commit `4afd994` — `fix(tests): override get_db_with_rls in analytics tests`
  - Root cause: Analytics routes use `get_db_with_rls`, but tests overrode `get_db`; FastAPI dependency overrides require the exact dependency object.
  - Fixed imports and override keys in `test_analytics_api.py` and `test_analytics_security.py`.

### Remaining PR #79 Deferred Items

1. Duplicate detection on import — pending.
2. Diff view — pending.
3. Regional RBAC enforcement — encoders can encode outside assigned region.
4. Civilian + encoder incident merging — pending.
5. Wildland workflow depth — pending.
6. Incident creation does not enforce `region_id` matches encoder's assigned region.

---

## PR #81 — CI/CD OIDC Build Args

- Branch: `fix/cd-oidc-build-args`
- Purpose: unblock frontend Docker/CD build by passing required OIDC/Next.js public env vars to `docker/build-push-action@v5`.
- Result: merged before PR #79.
- Commit on master: `edd2394 fix(cd): pass OIDC build args to docker buildx with localhost defaults (#81)`.

### Root Cause

Frontend build failed during static prerender with an undefined OIDC authority URL because build-time `NEXT_PUBLIC_*` variables were not passed into Docker buildx.

### Fix Pattern

Add placeholder/default localhost build args for:

- `NEXT_PUBLIC_AUTH_API_URL`
- `NEXT_PUBLIC_BASE_URL`
- `NEXT_PUBLIC_OIDC_CLIENT_ID`

Production values remain tracked separately and should not be hard-coded into the workflow.

---

## Earl/Admin System Merge Before Hotfix

By the time the proactive refresh hotfix was applied, master already included Earl/admin-system work:

- `445a587 Merge branch 'Earl-Branch' into master — admin onboarding fix, audit logging, session management, health dashboard, RBAC region isolation`
- `3354f4a fix(lint): resolve ruff + eslint errors post PR #83 merge`
- `7cc3651 style: ruff format on PR #83 backend files`

Operationally this means the old handoff claim that `Earl-Branch` still needed a PR was superseded.

---

## Pre-Existing Test / Type Issues Not Caused by PR #79 or Proactive Refresh

Known unrelated frontend TypeScript errors observed in full `npx tsc --noEmit`:

- `src/app/admin/system/page.tsx`
- `src/app/incidents/triage/page.tsx`
- `src/app/login/login.test.tsx`
- `src/lib/__tests__/useAutoSync.test.ts`
- `src/lib/syncEngine.ts`
- `src/lib/useAutoSync.ts`
- `src/lib/useNetworkStatus.ts`

Earlier backend full-suite failures also included environment-level issues:

- `test_keycloak_password_reset` — SMTP/flow config missing in test env.
- `test_rate_limiting` — Redis/config not configured in test env.
- `test_bootstrap_creates_v2_and_afor_objects` — schema idempotency issue around existing role `civilian_reporter`.

Do not attribute these to PR #79 or the JWT refresh hotfix without re-verifying live code.

---

## Team Mapping

| Real Name | GitHub | Role |
|-----------|--------|------|
| Natekatsu / x1n4te | x1n4te | Lead Architect, DevSecOps |
| Guinevere T. Tendero | G10dero + laqqui | Module 2 Incident Workflow |
| Earl Justin P. Camama | orljorstin | Admin/User Management, Health Dashboard, Audit Log, Sessions |
| Red Gabrielle A. Dela Cruz | ShibaTheShiba | Auth / Session Management |

---
