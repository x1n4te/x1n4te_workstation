# WIMS-BFP Codebase Audit — 2026-04-08

**Orchestrator audit of existing prototype before redo.**

---

## Overview

| Metric | Value |
|---|---|
| Total source files | ~3,800 (mostly node_modules) |
| SQL tables | 22 |
| RLS-enabled tables | 17 |
| FORCE RLS tables | 17 |
| CREATE POLICY statements | 65 |
| Backend route files | 8 |
| Backend model files | 7 |
| Celery task files | 2 |
| JWT validation checks | 5 (kid, iss, aud, exp, iat) |

---

## What's GOOD (Don't Redo These)

### SQL Schema
- 22 tables with proper foreign keys and constraints ✅
- `wims.users` has CHECK constraint on FRS role literals ✅
- `FORCE ROW LEVEL SECURITY` on all 17 operational tables ✅
- 65 RLS policies using `wims.current_user_uuid()` and `wims.current_user_role()` ✅
- PostGIS geography types with GIST indexes ✅
- Soft-delete patterns (`is_archived`, not hard deletes) ✅

### Auth (auth.py)
- All 5 JWT checks: kid, iss, aud, exp, iat ✅
- azp client verification ✅
- JWKS cache (60s TTL) with key rotation fallback ✅
- HttpOnly cookie token transport (XSS protection) ✅
- `get_current_wims_user` resolves user from JWT → wims.users ✅

### Database Layer (database.py)
- `set_rls_context()` correctly uses `SET LOCAL` (transaction-scoped) ✅
- `get_db()` dependency pattern with RLS context ✅

### PII Protection
- AES-256-GCM encryption for sensitive details (`pii_blob_enc`) ✅
- `encryption_iv` stored separately ✅
- Legacy plaintext fields marked for null-out on new writes ✅

### Security
- Redis Lua sliding window rate limiter ✅
- HttpOnly cookies for auth tokens ✅
- Role precedence defined in main.py ✅

---

## ISSUES FOUND (Redo Candidates)

### CRITICAL — RLS Context Dependency Cycle

**File:** `backend/database.py` + `backend/auth.py`

**Problem:**
```python
# database.py
def get_db(request):
    wims_user = getattr(request.state, "wims_user", None)
    if wims_user is not None:
        set_rls_context(db, wims_user["user_id"])
    yield db

# auth.py
async def get_current_wims_user(request, token_payload, db: Depends(get_db)):
    # db already yielded — RLS context NOT set because request.state.wims_user isn't set yet
    row = db.execute(text("SELECT ... FROM wims.users WHERE ..."))
```

`get_current_wims_user` depends on `get_db`, but `get_db` needs `request.state.wims_user` to set RLS context. The user isn't resolved yet, so RLS context is NOT set for the user lookup query.

**Impact:** The user lookup query runs without RLS context. If RLS policies on `wims.users` are restrictive, this could fail silently.

**Fix:** Set RLS context in a separate middleware after user resolution, not in `get_db`.

---

### CRITICAL — Incidents Route Has No Role Checks

**File:** `backend/api/routes/incidents.py` (5KB, 2 routes)

**Problem:** 0 role references, 0 RLS calls. The route file relies entirely on database-level RLS. No API-level authorization checks.

**Impact:** If RLS is misconfigured, anyone can upload attachments to any incident.

**Fix:** Add `require_role()` dependency to incident routes.

---

### HIGH — File Upload Missing Region Ownership Check

**File:** `backend/api/routes/incidents.py` line 36-38

```python
# Current: checks incident exists but not region ownership
incident = db.execute(
    text("SELECT incident_id FROM wims.fire_incidents WHERE incident_id = :iid"),
    {"iid": incident_id},
).fetchone()
```

**Problem:** Doesn't verify the user's region matches the incident's region.

**Fix:** Add region_id to the query and verify ownership.

---

### HIGH — Regional Routes Massive Review Needed

**File:** `backend/api/routes/regional.py` (71KB, 5 routes)

**Problem:** 71KB file with only 1 role reference. This is the largest route file and needs thorough review for:
- AFOR import logic
- Region isolation
- Input validation
- File handling

**Fix:** Decompose into smaller route files and add explicit role + region checks.

---

### MEDIUM — Missing Security Headers Middleware

**Problem:** No security headers in main.py.

**Missing:**
- `Strict-Transport-Security`
- `Content-Security-Policy`
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: strict-origin-when-cross-origin`

**Fix:** Add middleware to main.py.

---

### MEDIUM — JWKS Cache Too Short

**File:** `backend/auth.py` line 31

```python
JWKS_CACHE_TTL_SECONDS = 60  # 60 seconds
```

**Problem:** 60 seconds means every minute there's a network call to Keycloak. In production with many requests, this adds latency.

**Fix:** Increase to 300 seconds (5 minutes). Keycloak key rotation is typically hourly/daily.

---

### MEDIUM — No Explicit Token Expiry Verification

**File:** `backend/auth.py` line 155-158

```python
options={
    "verify_at_hash": False,
    "require": ["exp", "iat", "iss", "aud"],
}
```

**Problem:** `require` only requires the CLAIM EXISTS. It doesn't enforce `verify_exp: True` explicitly. The `jose` library defaults to `True` but this should be explicit.

**Fix:** Add `"verify_exp": True, "verify_signature": True, "verify_iss": True, "verify_aud": True` to options.

---

### LOW — Celery Tasks Use svc_suricata Account

**Files:** `tasks/suricata.py`, `tasks/exports.py`

**Status:** Both tasks set RLS context with svc_suricata user_id ✅

**Verification needed:** Confirm `00000000-0000-0000-0000-000000000001` exists in wims.users with role `NATIONAL_ANALYST`.

---

## Redo Plan Recommendation

Based on this audit, here's the recommended redo order:

| Step | Task | Why |
|---|---|---|
| 1 | Fix RLS context dependency cycle | Foundation — everything depends on this |
| 2 | Add security headers middleware | Low effort, high impact |
| 3 | Add role checks to incidents.py | Quick fix for route security |
| 4 | Review + refactor regional.py (71KB) | Largest risk surface |
| 5 | Add explicit JWT verification options | Defense-in-depth |
| 6 | Increase JWKS cache to 300s | Performance |
| 7 | Run full pytest suite | Validate all fixes |

Each step should go through: **Builder → Tester → Critic** pipeline.

---

## FRS Compliance Status

| FRS Role | Checked in SQL? | Checked in Routes? | RLS Policies? |
|---|---|---|---|
| CIVILIAN_REPORTER | ✅ | Partial | ✅ |
| REGIONAL_ENCODER | ✅ | Partial | ✅ |
| NATIONAL_VALIDATOR | ✅ | Partial | ✅ |
| NATIONAL_ANALYST | ✅ | Partial | ✅ |
| SYSTEM_ADMIN | ✅ | Partial | ✅ |
