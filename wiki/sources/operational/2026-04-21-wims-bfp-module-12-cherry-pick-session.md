---
id: wims-bfp-module-12-cherry-pick-2026-04-21
type: source
created: 2026-04-21
updated: 2026-04-21
last_verified: 2026-04-21
review_after: 2026-05-21
stale_after: 2026-07-21
confidence: high
source_refs:
  - ~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/src/backend/api/routes/user.py
  - ~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/src/backend/services/keycloak_admin.py
  - ~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/src/backend/api/routes/admin.py
  - ~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/src/frontend/src/app/admin/system/page.tsx
  - ~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/src/frontend/src/app/profile/page.tsx
status: active
tags:
  - wims-bfp
  - thesis
  - operational
  - module-12
  - user-management
related:
  - analyses/wims-bfp-frs-implementation-tracker
  - mocs/wims-bfp
  - concepts/keycloak-admin-rest-api
  - concepts/keycloak-authentication-flows
---

# WIMS-BFP — Module 12 Cherry-Pick Session — 2026-04-21

## What Happened

### Goal
Restore Module 12 (User Management and Administration) from Earl's commit `9e0d657` into the local repository at `~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/`, then force-push to `origin/master`.

### Background Context
- **Earl's commit** `9e0d657` — implemented Module 12 by orljorstin on a branch that was NOT in the main lineage
- Module 12 was subsequently REMOVED from the main branch (commit `82016ab` or earlier)
- Local repo HEAD was `0ed1a0a` (Module 4 validator dashboard)
- Remote `origin/master` was ahead with 12K+ extra lines — user confirmed local is canonical source of truth

### Step-by-Step

1. **Identified** Earl's Module 12 commit `9e0d6579877845facf99cf0686248c553f1797ef`
2. **Cherry-picked** `9e0d657` onto local HEAD `0ed1a0a` — committed as `8d42f3f`
3. **Resolved conflict** in `src/frontend/src/lib/api.ts`:
   - Conflict: HEAD used `ApiRequestError` class vs 9e0d657's plain `Error`
   - Resolution: kept HEAD's `ApiRequestError` pattern (newer/more correct)
4. **Installed missing dependency** `email-validator` — was required by new Pydantic models but missing from requirements.txt
5. **Restarted backend** on port 8000 — uvicorn reloaded, process confirmed up
6. **Verified** no `/health` endpoint exists (returns 404 — not an error, no health endpoint was ever defined)
7. **Force-pushed** `8d42f3f` to `origin/master` — remote now matches local

### Key Decisions Made

| Decision | Rationale |
|---|---|
| Cherry-pick instead of merge | Main lineage (0ed1a0a) was correct base; only Module 12 was missing |
| Keep `ApiRequestError` over plain `Error` | HEAD is newer; `ApiRequestError` has better structured error handling |
| Force push | User confirmed local is canonical source of truth; remote had unrelated history |
| No Keycloak password reset | Direct KC admin writes were blocked by existing auth constraints; user instructed to reset via Admin Console |

---

## What Module 12 Actually Is

### Source: FRS Chapter — User Management and Administration

Module 12 implements the User Management and Administration requirement from the FRS (Chapter 3a). It adds:

### Backend — `src/backend/api/routes/user.py`
Self-service profile routes for ALL authenticated users (not just admins):

| Endpoint | Method | What |
|---|---|---|
| `/api/user/me/profile` | GET | Get current user's profile (first name, last name, contact number) |
| `/api/user/me` | PATCH | Update own profile (first name, last name, email, contact number) |
| `/api/user/me/password` | PATCH | Change own password (requires current password + optional OTP) |

**Validation:**
- `ProfileUpdate`: name cannot be blank, contact_number must be 7+ digits
- `PasswordChange`: min 8 chars, requires uppercase + digit + special character

**Key design:** JWT bearer token confirms identity — no password re-entry needed for profile updates. Password change verifies current password via Keycloak's `bfp-client` (public, `directAccessGrantsEnabled=true`).

### Backend — `src/backend/services/keycloak_admin.py`
Keycloak Admin SDK service using **client credentials grant** (service account `wims-admin-service`):

| Function | What |
|---|---|
| `create_keycloak_user()` | Create user + set temp password (must change on first login) + assign realm role |
| `generate_temp_password()` | 14-char cryptographically secure password |
| `set_user_enabled()` | Enable/disable user + revoke all sessions |
| `update_user_profile()` | Update firstName, lastName, email, contact_number |
| `change_user_password()` | Set new non-temporary password |
| `get_user_profile()` | Fetch profile from Keycloak |

**Auth:** Uses `KEYCLOAK_ADMIN_CLIENT_ID` / `KEYCLOAK_ADMIN_CLIENT_SECRET` env vars — never stores human admin passwords.

### Backend — `src/backend/api/routes/admin.py` (updated)
`POST /api/admin/users` — System Admin only:
- Creates user in Keycloak (temp password, must-change-on-login)
- Inserts row into `wims.users` table
- Returns plaintext temp password for admin to distribute
- Validates region FK exists before inserting
- 409 Conflict if email already exists in Keycloak

`VALID_ROLES` in admin.py: `CIVILIAN_REPORTER`, `REGIONAL_ENCODER`, `NATIONAL_VALIDATOR`, `NATIONAL_ANALYST`, `SYSTEM_ADMIN`
Note: `ENCODER`, `VALIDATOR`, `ANALYST`, `ADMIN` (old names) are NOT in this list — they are the old role literals that were replaced.

### Frontend — `src/frontend/src/app/profile/page.tsx`
Self-service profile page — users can update their own name, email, contact number, and change password.

### Frontend — `src/frontend/src/app/admin/system/page.tsx`
Admin user management UI — create users, enable/disable, assign roles and regions.

---

## Files Changed (8d42f3f)

| File | Change |
|---|---|
| `src/backend/api/routes/user.py` | RESTORED — self-service profile endpoints |
| `src/backend/services/keycloak_admin.py` | RESTORED — Keycloak Admin SDK wrappers |
| `src/backend/api/routes/admin.py` | UPDATED — create_user() endpoint restored |
| `src/backend/auth.py` | UPDATED — new route registrations |
| `src/backend/requirements.txt` | UPDATED — python-keycloak>=4.0.0 added |
| `src/backend/main.py` | (changes from Module 4 + cherry-pick) |
| `src/frontend/src/app/profile/page.tsx` | RESTORED — self-service profile UI |
| `src/frontend/src/app/admin/system/page.tsx` | RESTORED — admin user management UI |
| `src/frontend/src/lib/api.ts` | CONFLICT RESOLVED — kept ApiRequestError |
| `src/frontend/src/components/Sidebar.tsx` | (updated route links) |

---

## Verification Commands

```bash
# Cherry-pick confirmation
git log --oneline 0ed1a0a..8d42f3f

# Force push
git push origin master --force

# Backend is running
curl -s http://localhost:8000/api/user/me/profile | head -c 200

# Missing dep check
pip show email-validator
```

---

## Outstanding Issues

1. **Keycloak test user passwords are stale** — `admin_test`, `encoder_test`, `validator_test`, `analyst_test` passwords are unknown. User was instructed to reset via Keycloak Admin Console at `http://localhost:8080/auth/` using `admin`/`admin`.

2. **No `/health` endpoint on backend** — returns 404. Not an actual error; health endpoint was never defined in the requirements.

3. **Remote reset was necessary** — the force push replaced ~12K lines of unrelated remote history with the correct local canonical state.

---

## Relationship to FRS Tracker

Module 12 maps to the "User Management and Administration" section of Chapter 3a (FR-4 Access Control extension). The FRS tracker at [[analyses/wims-bfp-frs-implementation-tracker]] should be updated to reflect:
- FR-4 is now COMPLETE (was already marked complete but Module 12 adds the self-service profile layer)
- A new row may be needed for User Administration requirements

---

*Session end. Remote `origin/master` now at commit `8d42f3f` — force-pushed, canonical state confirmed.*
