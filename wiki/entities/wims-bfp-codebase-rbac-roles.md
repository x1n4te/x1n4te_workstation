---
id: wims-bfp-codebase-rbac-roles-001
type: entity
created: 2026-04-21
updated: 2026-04-21
last_verified: 2026-04-21
review_after: 2026-06-21
stale_after: 2026-10-21
confidence: high
source_refs:
  - raw/sources/wims-bfp-codebase/docs/SECURITY.md
status: active
tags:
  - wims-bfp
  - auth
  - security
  - rbac
related:
  - concepts/wims-bfp-codebase-auth-flow
  - entities/wims-bfp-codebase-keycloak-config
  - concepts/wims-bfp-codebase-rls-model
---

# RBAC Roles

5 system roles defined in FRS. Enforced at JWT + RLS layer.

## Role Definitions

| Role | Scope | Can Do | Cannot Do |
|------|-------|--------|-----------|
| `CIVILIAN_REPORTER` | Public | Submit fire reports, view own submissions | Access internal dashboards |
| `REGIONAL_ENCODER` | Regional (1 region) | Import AFORs, create/edit incidents in assigned region | View other regions, verify incidents |
| `NATIONAL_VALIDATOR` | National | Verify/reject incidents, approve data commits | Manage users, view analytics |
| `NATIONAL_ANALYST` | National | View all analytics, heatmaps, trends | Modify incidents, manage users |
| `SYSTEM_ADMIN` | National | Manage users, view security logs, system health | — (full access) |

## Guard Implementation

```python
# src/backend/main.py
WIMS_ROLES_FROM_KEYCLOAK = (
    "CIVILIAN_REPORTER",
    "REGIONAL_ENCODER",
    "NATIONAL_VALIDATOR",
    "NATIONAL_ANALYST",
    "SYSTEM_ADMIN",
)

# Route-level enforcement
@app.get("/api/admin/users")
async def list_users(
    user=Depends(require_role(["SYSTEM_ADMIN"]))
):
    ...
```

## Role Resolution

From JWT `realm_access.roles` + `resource_access.bfp-client.roles`:
```python
def _resolve_role_from_token(token: dict) -> str:
    # Priority: resource_access > realm_access
    resource_roles = token.get("resource_access", {}).get("bfp-client", {}).get("roles", [])
    realm_roles = token.get("realm_access", {}).get("roles", [])
    for role in WIMS_ROLES_FROM_KEYCLOAK:
        if role in resource_roles or role in realm_roles:
            return role
    raise HTTPException(403, "No valid role found")
```

## MFA Requirements

| Role | MFA Required | Method |
|------|-------------|--------|
| CIVILIAN_REPORTER | No | — |
| REGIONAL_ENCODER | No | — |
| NATIONAL_VALIDATOR | Yes | TOTP (7-day trusted device) |
| NATIONAL_ANALYST | No | — |
| SYSTEM_ADMIN | Yes | TOTP (7-day trusted device) |

## Related

- [[concepts/wims-bfp-codebase-auth-flow]] — full authentication pipeline
- [[entities/wims-bfp-codebase-keycloak-config]] — realm JSON structure
- [[concepts/wims-bfp-codebase-rls-model]] — database-level role enforcement
