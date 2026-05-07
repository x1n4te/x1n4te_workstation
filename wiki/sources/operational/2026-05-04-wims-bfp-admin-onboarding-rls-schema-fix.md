# WIMS-BFP Admin Onboarding RLS + Schema Fix
**Date:** 2026-05-04 | **Session:** ~23:00 PST
**PR:** [#91](https://github.com/x1n4te/WIMS-BFP-PROTOTYPE/pull/91) — `fix/admin-onboarding-rls-and-schema`
**Status:** Merged to master

---

## Problem
Admin user creation in the UI: "User created in Keycloak but database sync failed. Contact system administrator."

Two users reported the issue after the password fix was applied (docker-compose KEYCLOAK_ADMIN_PASSWORD `***` → `admin`).

---

## Root Causes (3 stacked bugs)

### 1. Keycloak password (partial fix only — applied in earlier session)
- `docker-compose.yml` `KEYCLOAK_ADMIN_PASSWORD=***` (literal asterisks)
- `keycloak_admin.py` used `KeycloakOpenIDConnection` (broken in python-keycloak 7.1.1)
- **Status:** Fixed earlier this session

### 2. RLS context not propagating to service-account session (NEWLY IDENTIFIED)
- `wims.users` has `FORCE ROW LEVEL SECURITY` — applies to ALL sessions including the postgres service account
- `create_user` route used `get_db_with_rls()` — this reads `wims.current_user_id` from `request.state.wims_user`
- Problem: `request.state.wims_user` is set by `get_current_wims_user` in a **different SQLAlchemy session** (a different DB connection from the auth layer → FastAPI dependency resolution chain)
- The service-account session doing the actual INSERT had `NULL` GUC
- `current_user_role()` → `COALESCE(role, 'ANONYMOUS')` with `WHERE user_id = NULL` → returns 0 rows → `'ANONYMOUS'`
- Policy check: `'ANONYMOUS' IN ('SYSTEM_ADMIN')` → `NULL`/false → **INSERT BLOCKED**
- **NOT visible in error logs** — the actual schema error (bug #3) fired first

### 3. Missing `contact_number` column (BLOCKING — the actual error)
- The Pydantic `UserCreate` model included `contact_number`
- The INSERT statement referenced `contact_number`
- But `03_users.sql` **never defined** the column in the schema
- Error: `ProgrammingError: column "contact_number" of relation "users" does not exist`
- This fired **before** RLS was ever evaluated

---

## Fix

### `src/postgres-init/09_rls_helpers.sql`
Added `wims.exec_as_system_admin(uid)` — a `SECURITY DEFINER` helper that bypasses RLS for the session to set the GUC:

```sql
CREATE OR REPLACE FUNCTION wims.exec_as_system_admin(uid uuid)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  PERFORM set_config('wims.current_user_id', uid::text, true);
END;
$$;
```

`SECURITY DEFINER` ensures the function executes with the owner's (postgres) privileges, bypassing `FORCE ROW LEVEL SECURITY` for this call.

### `src/backend/api/routes/admin.py`
```python
# Before (broken):
db: Annotated[Session, Depends(get_db_with_rls)]

# After (fixed):
db: Annotated[Session, Depends(get_db)]

# Before INSERT:
db.execute(text("SELECT wims.exec_as_system_admin(:uid)"), {"uid": _admin["user_id"]})
```

`get_db()` has no RLS context set on the session. The explicit `exec_as_system_admin()` call sets the GUC within the same transaction before the INSERT.

### `src/postgres-init/03_users.sql`
```sql
assigned_region_id INTEGER REFERENCES wims.ref_regions(region_id),
contact_number    VARCHAR(20),   -- ← added
is_active BOOLEAN DEFAULT TRUE,
```

### `src/docker-compose.yml`
```yaml
KEYCLOAK_ADMIN_PASSWORD: admin  # was: "***"
```

### `src/backend/services/keycloak_admin.py`
```python
# Before (broken — KeycloakOpenIDConnection):
kc = KeycloakOpenIDConnection(
    server_url=..., realm_name="master",
    username=_KC_ADMIN_USER, password=_KC_ADMIN_PASSWORD,
    client_id=_KC_CLIENT_ID, client_secret=_KC_CLIENT_SECRET,
)
# KeycloakAdmin(realm_name="bfp")  ← uses wrong auth flow

# After (fixed):
oidc = KeycloakOpenID(server_url=_KC_BASE_URL, realm_name="master", client_id="admin-cli")
token = oidc.token(_KC_ADMIN_USER, _KC_ADMIN_PASSWORD)
KeycloakAdmin(server_url=_KC_BASE_URL, realm_name=_KC_REALM, token=token)
```

---

## Verification
```bash
# Verify exec_as_system_admin exists
docker compose exec -T postgres psql -U postgres -d wims -c \
  "SELECT proname FROM pg_proc WHERE pronname = 'exec_as_system_admin';"

# Verify contact_number column
docker compose exec -T postgres psql -U postgres -d wims -c "\d wims.users"

# Test function directly
docker compose exec -T postgres psql -U postgres -d wims -c \
  "SELECT wims.exec_as_system_admin('44444444-4444-4444-8444-444444444444'::uuid);"
```

---

## Related Issues
- Issue #90: JWT Refresh Token Race Condition (P0, unresolved)
- Issue #84: verify_incident() missing analytics sync (P0, unresolved)

---

## Files Changed
| File | Lines |
|------|-------|
| `src/postgres-init/09_rls_helpers.sql` | +29 |
| `src/backend/api/routes/admin.py` | +9 −1 |
| `src/postgres-init/03_users.sql` | +1 |
| `src/docker-compose.yml` | +1 −1 |
| `src/backend/services/keycloak_admin.py` | +8 −7 |

**Total:** +47 insertions, 9 deletions across 5 files.
