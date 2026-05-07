---
id: wims-bfp-codebase-auth-flow-001
type: concept
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
  - keycloak
  - security
related:
  - entities/wims-bfp-codebase-rbac-roles
  - entities/wims-bfp-codebase-keycloak-config
  - concepts/wims-bfp-codebase-rls-model
---

# Auth Flow

Keycloak OIDC → JWT → HttpOnly cookie → RLS context. Zero-Trust: every request authenticated.

## Login Flow

1. Frontend redirects to Keycloak `/auth/realms/bfp/protocol/openid-connect/auth`
2. Keycloak shows login page (BFP-branded FTL template)
3. If MFA required (SYSTEM_ADMIN, NATIONAL_VALIDATOR): TOTP challenge
4. Keycloak returns auth code → frontend exchanges via PKCE (`/api/auth/callback`)
5. Backend validates auth code, receives tokens (access + refresh + ID)
6. Backend stores tokens in HttpOnly Secure SameSite cookies
7. Frontend receives user profile from JWT claims

## Token Validation (Per-Request)

```python
# src/backend/auth.py
async def validate_token(token: str) -> dict:
    # 1. Fetch JWKS from Keycloak (cached)
    jwks = await fetch_jwks(KEYCLOAK_REALM_URL)
    # 2. Decode + verify signature (RS256)
    # 3. Validate: iss, aud, exp, nbf
    # 4. Return decoded claims
```

## Role Resolution

From JWT claims:
- `realm_access.roles` — realm-level roles
- `resource_access.bfp-client.roles` — client-level roles

Backend resolves to one of: `CIVILIAN_REPORTER`, `REGIONAL_ENCODER`, `NATIONAL_VALIDATOR`, `NATIONAL_ANALYST`, `SYSTEM_ADMIN`

## RLS Context Injection

Before each DB query, backend sets PostgreSQL session variables:
```python
async def set_rls_context(db: AsyncSession, user: User):
    await db.execute(text(f"SET LOCAL wims.current_user_id = '{user.user_id}'"))
    await db.execute(text(f"SET LOCAL wims.current_user_role = '{user.role}'"))
    await db.execute(text(f"SET LOCAL wims.current_user_region_id = '{user.region_id}'"))
```

## Related

- [[entities/wims-bfp-codebase-rbac-roles]] — role definitions
- [[entities/wims-bfp-codebase-keycloak-config]] — realm configuration
- [[concepts/wims-bfp-codebase-rls-model]] — database-level enforcement
