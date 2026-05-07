---
title: "WIMS-BFP — Earl-Branch Review (PR #91, #93, #84+#66)"
date: 2026-05-04
tags: [wims-bfp, github, pr, analytics, rls, jwt, auth, backend, frontend, postgres]
confidence: high
reviewed: 2026-05-04
source: local-git
author: Ares (Orchestrator)
project: WIMS-BFP
related:
  - "[[sources/operational/2026-05-04-wims-bfp-session-persistence-fix]]"
  - "[[sources/operational/2026-05-04-wims-bfp-admin-onboarding-rls-schema-fix]]"
  - "[[sources/operational/2026-05-04-wims-bfp-session-handoff-archive]]"
---

# WIMS-BFP — Earl-Branch Review (PR #91, #93, #84+#66)

## Branch Identity

| Field | Value |
|-------|-------|
| Branch | `Earl-Branch` |
| Remote | `origin/Earl-Branch` |
| Base | `master` |
| Repo | `x1n4te/WIMS-BFP-PROTOTYPE` |
| Local path | `/home/xynate/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/src/` |
| Status | 3 commits ahead of `master` |

## Commit Summary

```
c5ce2b9 fix(#84,#66): sync analytics on verify + immutable records enforcement (Earl)
7d0ea8a fix(auth): silent proactive JWT refresh for lib/auth.tsx (#93) (Natekatsu)
570eaed fix(admin): admin user onboarding — RLS context fix + missing contact_number column (#91) (Natekatsu)
```

## Files Changed (diff master → Earl-Branch)

| File | Change |
|------|--------|
| `src/backend/api/routes/admin.py` | Admin onboarding fix |
| `src/backend/api/routes/regional.py` | Analytics sync on verify |
| `src/backend/services/keycloak_admin.py` | Keycloak admin client fix |
| `src/backend/tests/test_immutable_records.py` | New integration tests |
| `src/docker-compose.yml` | Keycloak admin password fix |
| `src/frontend/src/context/AuthContext.tsx` | JWT refresh (PR #92) |
| `src/frontend/src/lib/auth.tsx` | JWT refresh (PR #93) |
| `src/postgres-init/03_users.sql` | `contact_number` column added |
| `src/postgres-init/09_rls_helpers.sql` | `exec_as_system_admin()` SECURITY DEFINER function |
| `src/postgres-init/17_immutable_records.sql` | NEW: immutable records + analytics schema expansion |

**Total: 10 files, +644 insertions, -43 deletions**

---

## Commit-by-Commit Breakdown

### Commit `570eaed` — PR #91: Admin User Onboarding RLS Fix

**Author:** Natekatsu
**PR:** #91 (merged)

Root causes fixed (stacked failures):

1. **Wrong Keycloak admin password** — `docker-compose.yml` had password literally set to `***` instead of `admin`, breaking `KeycloakOpenIDConnection` auth.
2. **Broken python-keycloak 7.1.1 client usage** — `KeycloakOpenIDConnection(username/password)` is broken. Fixed: use `KeycloakOpenID.token()` + `KeycloakAdmin(token=)`.
3. **RLS GUC context leak across SQLAlchemy sessions** — `get_db_with_rls()` sets `wims.current_user_id` GUC in one session, but SQLAlchemy pools connections so the actual INSERT ran in a different session lacking the GUC → anonymous session blocked by RLS. Fixed: created `wims.exec_as_system_admin(uid)` SECURITY DEFINER helper in `09_rls_helpers.sql` and switched route to plain `get_db()` + explicit helper call.
4. **Missing `contact_number` column** — ORM included `contact_number` but `03_users.sql` schema was missing it → INSERT failed before RLS was even hit.

Files touched:
- `docker-compose.yml` — correct `KEYCLOAK_ADMIN_PASSWORD`
- `keycloak_admin.py` — `KeycloakOpenID.token()` + `KeycloakAdmin(token=)` pattern
- `admin.py` — plain `get_db()` + `exec_as_system_admin()` call
- `03_users.sql` — add `contact_number` column
- `09_rls_helpers.sql` — add `exec_as_system_admin()` function

### Commit `7d0ea8a` — PR #93: Silent JWT Refresh for lib/auth.tsx

**Author:** Natekatsu
**PR:** #93 (CI in progress per handoff)

Dual-AuthProvider architecture fix:
- `context/AuthContext.tsx` (PR #92) got proactive refresh + `navigator.locks` cross-tab coordination + `visibilitychange` suppression.
- `lib/auth.tsx` (PR #93) had the same fixes applied — `navigator.locks` for cross-tab serialization, silent interval refresh every 4 minutes, `visibilitychange` without triggering full session fetches.

This resolved tab-switch / navigate-away causing full page reloads (state loss).

### Commit `c5ce2b9` — PR #84+#66: Analytics Sync on Verify + Immutable Records

**Author:** Earl

#### Issue #84 — Analytics Sync on verify_incident()

- `verify_incident()` in `regional.py` now calls `sync_incident_to_analytics(db, incident_id)` after a VERIFIED transition.
- ADR-009 comment explicitly records this: "sync verified incident to analytics facts (#84 fix)".
- `sync_incident_to_analytics()` is defined in `services/analytics_read_model.py`:
  - Upserts into `analytics_incident_facts` if VERIFIED and not archived.
  - Removes from facts otherwise.
- `sync_incidents_batch()` calls it for each ID — used after bulk AFOR import commit.
- `backfill_analytics_facts()` backfills all existing VERIFIED non-archived incidents.

#### Issue #66 — Immutable Records (M6-D)

New file: `17_immutable_records.sql`

1. **SHA-256 `data_hash` column** on `wims.fire_incidents` — populated at VERIFIED transition, then immutable.
2. **DB-level UPDATE block** on VERIFIED rows — `CREATE RULE no_update_verified DO INSTEAD NOTHING`.
3. **DB-level DELETE block** on VERIFIED rows — `CREATE RULE no_delete_verified DO INSTEAD NOTHING`.
4. **DB-level DELETE block** on `incident_verification_history` — `CREATE RULE no_delete_ivh DO INSTEAD NOTHING` (append-only audit).
5. **Analytics schema expansion** — adds 8 columns to `analytics_incident_facts` needed by `sync_incident_to_analytics()`:
   - `civilian_injured`, `civilian_deaths`, `firefighter_injured`, `firefighter_deaths`
   - `total_response_time_minutes`, `estimated_damage_php`
   - `fire_station_name`, `barangay_name`

#### New Test File: `test_immutable_records.py`

5 integration tests covering both #66 and #84:
- All 5 tests FAIL before the fix.
- All 5 tests PASS after:
  1. `17_immutable_records.sql` applied to running container
  2. `verify_incident()` patched (data_hash + sync)
- Run: `docker compose run --rm backend pytest tests/test_immutable_records.py -v`

---

## Verification Checklist

Before merging Earl-Branch into master:

- [ ] `17_immutable_records.sql` applied to all environments (`docker compose exec -T postgres psql -U postgres -d wims < src/postgres-init/17_immutable_records.sql`)
- [ ] `09_rls_helpers.sql` applied (exec_as_system_admin function)
- [ ] Keycloak admin password matches between `docker-compose.yml` and actual Keycloak admin credentials
- [ ] `contact_number` column confirmed in `wims.users`
- [ ] PR #93 CI passes (silent refresh for lib/auth.tsx)
- [ ] `test_immutable_records.py` runs green inside Docker
- [ ] `backfill_analytics_facts()` confirmed callable for existing data repair

---

## Relation to Active Issues

| Issue | Title | Addressed By |
|-------|-------|--------------|
| #84 | verify_incident() missing analytics sync | `c5ce2b9` |
| #66 | Immutable records enforcement | `c5ce2b9` (M6-D) |
| #90 | JWT refresh token race condition | `7d0ea8a` (PR #93) |
| #91 | Admin onboarding RLS fix | `570eaed` |

## Notes

- PRs #91, #92, #93 were in flight per 2026-05-04 handoff — PR #91 and #92 merged, #93 CI in progress.
- Earl-Branch is 3 commits ahead of master but NOT yet merged.
- Pre-existing flaky test `queue-baseline.test.tsx` is unrelated to this branch and was not touched.
