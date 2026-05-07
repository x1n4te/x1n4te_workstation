---
id: wims-bfp-fix-looping-auth-branch-analysis-001
type: source
created: 2026-04-16
updated: 2026-04-16
last_verified: 2026-04-16
review_after: 2026-05-16
stale_after: 2026-07-16
confidence: high
source_refs: []
status: active
tags:
  - wims-bfp
  - keycloak
  - auth
  - security
related:
  - sources/operational/2026-04-14-mfa-auth-debugging-session-continued
  - analyses/keycloak-mfa-pkce-debugging
  - concepts/keycloak-fastapi-security-wims-bfp
---

# WIMS-BFP — `fix/looping-auth` Branch Analysis (G10dero)

**Date:** 2026-04-16
**Branch:** `fix/looping-auth`
**Author:** G10dero (Guinevere Tendero, 202311695@fit.edu.ph)
**Commit:** `2719fb3` — "fix keycloak auth loop"
**Action:** Reviewed for merge readiness

---

## Root Cause Summary

The same root cause we identified independently (Keycloak `--import-realm` regenerating user UUIDs, breaking `wims.users.keycloak_id` references) — but G10dero's fix addresses it at the **source** rather than symptom.

## What Changed (5 files)

### 1. `src/postgres-init/00_keycloak_bootstrap.sql` (NEW — 19 lines)
Idempotent SQL bootstrap replacing `init-db.sh`:
```sql
CREATE ROLE keycloak IF NOT EXISTS;
CREATE DATABASE keycloak IF NOT EXISTS;
GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak;
```
Runs automatically in `docker-entrypoint-initdb.d` on fresh Postgres volumes. Prevents Keycloak startup loop when role/database missing.

### 2. `src/postgres-init/init-db.sh` (DELETED)
Shell-based bootstrap removed — was fragile in container init context.

### 3. `src/backend/auth.py` (MODIFIED — +33 lines)
Added **username fallback lookup** when `keycloak_id = token.sub` fails:
1. Primary: `WHERE keycloak_id = :sub`
2. Fallback: `WHERE username = :preferred_username`
3. Guard: if username row exists with DIFFERENT `keycloak_id` → `403 identity mismatch`

Makes auth resilient when `keycloak_id` is stale but username matches.

### 4. `src/keycloak/bfp-realm.json` (MODIFIED — +27 lines)
- Added `NATIONAL_VALIDATOR` realm role (was missing)
- Added `realmRoles` assignments to all 5 seeded users
- Added **deterministic user `id` values**:
  - `encoder_test` → `11111111-1111-4111-8111-111111111111`
  - `validator_test` → `22222222-2222-4222-8222-222222222222`
  - `analyst_test` → `33333333-3333-4333-8333-333333333333`
  - `analyst1_test` → `44444444-4444-4444-8444-444444444444`
  - `admin_test` → `55555555-5555-4555-8555-555555555555`

### 5. `src/postgres-init/01_wims_initial.sql` (MODIFIED — +52 lines)
Added deterministic seeded users with matching `keycloak_id`:
```sql
INSERT INTO wims.users (user_id, keycloak_id, username, role, ...)
VALUES ('1111...', '1111...', 'encoder_test', 'REGIONAL_ENCODER', ...)
ON CONFLICT (username) DO UPDATE
SET keycloak_id = EXCLUDED.keycloak_id, ...;
```
Self-heals existing broken mappings via `ON CONFLICT` upsert.

---

## Why This Works

**Root cause eliminated:** By hardcoding deterministic IDs in BOTH the realm JSON AND the DB bootstrap, the UUIDs will never drift regardless of `--import-realm` behavior. The `ON CONFLICT` update also retroactively fixes any existing broken mappings.

**Testing approach:** `docker compose down -v` (wipe volumes) → `docker compose up` (fresh Postgres picks up both init scripts) → all users have matching `keycloak_id` from the start.

---

## Hermes Assessment

**Ruling:** Clean, well-documented fix. Addresses root cause (ID drift) not just symptom.

**Verified:** `username` column has `UNIQUE` constraint (`username VARCHAR NOT NULL UNIQUE`) — `ON CONFLICT (username)` is valid.

**Security note:** PR doc explicitly flags that deterministic UUIDs and seeded test credentials should NOT ship to production.

**Merge verdict:** Ready for dev/staging. See PR doc for production hardening checklist.

---

## Contrast With Our Previous Fix (2026-04-14)

Our approach: `UPDATE wims.users SET keycloak_id = '<new-uuid>' WHERE username = 'encoder_test'` (manual SQL fix per user)

G10dero's approach: Deterministic IDs in source code + username fallback in auth.py + idempotent DB bootstrap

**G10dero's approach is superior** — prevents the problem rather than fixing it after the fact.

## Related
- [[analyses/keycloak-mfa-pkce-debugging]] — original MFA debugging session
- [[sources/operational/2026-04-14-mfa-auth-debugging-session-continued]] — 5 stacked bugs resolution
- [[concepts/keycloak-fastapi-security-wims-bfp]] — Keycloak + FastAPI integration
