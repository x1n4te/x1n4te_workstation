---
id: fastapi-keycloak-jwt-rbac-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - github.com/fastapi/fastapi/discussions/9066
  - kubeblogs.com/implement-role-based-access-control-rbac-in-fastapi-using-keycloak
  - medium.com/@buffetbenjamin/securing-fastapi-with-keycloak-the-adventure-begins-part-1
status: active
tags:
  - fastapi
  - keycloak
  - jwt
  - rbac
  - oauth2
  - authentication
  - software-dev
related:
  - sources/software-dev/keycloak-production-security
  - concepts/keycloak-fastapi-security-wims-bfp
  - concepts/secure-coding-practices
  - mocs/cybersecurity
---

# FastAPI + Keycloak JWT RBAC Integration (Source Summary)

**Sources:** FastAPI GitHub Discussions, KubeBlogs, Medium tutorials
**Type:** Implementation guide for FastAPI + Keycloak JWT auth
**Confidence:** High — official FastAPI patterns + community best practices

---

## Architecture

```
Client → Keycloak (authenticate) → JWT token
  → FastAPI (validate JWT) → RLS context set → Query executes
```

### Components

| Component | Role |
|---|---|
| Keycloak | Token issuer, user management, RBAC |
| FastAPI | Token validator, API gateway |
| PostgreSQL | Data storage with RLS enforcement |

---

## Keycloak Client Configuration

### For WIMS-BFP Backend

```
Client ID: wims-bfp-backend
Client Protocol: openid-connect
Access Type: confidential
Standard Flow: enabled
Direct Access Grants: enabled
Valid Redirect URIs: https://wims-bfp.example.com/callback
```

### FRS Roles (Realm Roles)

```
CIVILIAN_REPORTER      — DMZ intake only
REGIONAL_ENCODER       — Regional CRUD with RLS
NATIONAL_VALIDATOR     — Regional CRUD with RLS
NATIONAL_ANALYST       — Global read-only
SYSTEM_ADMIN           — Full CRUD everywhere
```

### Client Scopes

| Scope | Purpose | Token Claim |
|---|---|---|
| `wims:read` | Read access | `realm_access.roles` |
| `wims:write` | Write access | `realm_access.roles` |
| `wims:admin` | Admin access | `realm_access.roles` |
| `wims:region` | Region binding | `wims_region` custom attribute |

---

## FastAPI JWT Validation

### Token Validation Flow

```python
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2AuthorizationCodeBearer
from jwt import PyJWKClient
import jwt

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl="https://keycloak.example.com/realms/wims/protocol/openid-connect/token",
    authorizationUrl="https://keycloak.example.com/realms/wims/protocol/openid-connect/auth",
)

async def validate_token(
    access_token: str = Depends(oauth2_scheme),
) -> dict:
    """Validate JWT token from Keycloak."""
    url = "https://keycloak.example.com/realms/wims/protocol/openid-connect/certs"
    jwks_client = PyJWKClient(url)
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(access_token)
        data = jwt.decode(
            access_token,
            signing_key.key,
            algorithms=["RS256"],
            audience="wims-bfp-backend",
            issuer="https://keycloak.example.com/realms/wims",
            options={
                "verify_signature": True,
                "verify_aud": True,
                "verify_exp": True,
                "verify_iss": True,
            },
        )
        return data
    except jwt.exceptions.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=str(e))
```

### 5 JWT Validation Checks (Mandatory)

| Check | Purpose | WIMS-BFP Status |
|---|---|---|
| `kid` | Correct signing key | ✅ Implemented |
| `iss` | Token from trusted issuer | ✅ Implemented |
| `aud` | Token for this API | ✅ Implemented |
| `signature` | Token not tampered | ✅ Implemented |
| `exp` | Token not expired | ✅ Implemented |

---

## RBAC Implementation

### WIMS-BFP User Model

```python
from pydantic import BaseModel
from enum import Enum

class FRSEnum(str, Enum):
    CIVILIAN_REPORTER = "CIVILIAN_REPORTER"
    REGIONAL_ENCODER = "REGIONAL_ENCODER"
    NATIONAL_VALIDATOR = "NATIONAL_VALIDATOR"
    NATIONAL_ANALYST = "NATIONAL_ANALYST"
    SYSTEM_ADMIN = "SYSTEM_ADMIN"

class WimsUser(BaseModel):
    sub: str  # Keycloak user ID
    email: str
    role: FRSEnum
    region: str | None = None
    user_id: str  # Internal wims.users.user_id

    def can_write(self) -> bool:
        return self.role in (
            FRSEnum.SYSTEM_ADMIN,
            FRSEnum.REGIONAL_ENCODER,
            FRSEnum.NATIONAL_VALIDATOR,
        )

    def is_read_only(self) -> bool:
        return self.role == FRSEnum.NATIONAL_ANALYST

    def is_regional(self) -> bool:
        return self.role in (
            FRSEnum.REGIONAL_ENCODER,
            FRSEnum.NATIONAL_VALIDATOR,
        )
```

### Role-Based Dependencies

```python
from fastapi import Depends, HTTPException

def require_role(allowed_roles: list[FRSEnum]):
    """Dependency that requires specific FRS roles."""
    async def check_role(user: WimsUser = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Role {user.role} not in {allowed_roles}"
            )
        return user
    return check_role

# Usage in endpoints:
@router.post("/incidents", dependencies=[Depends(require_role([
    FRSEnum.SYSTEM_ADMIN,
    FRSEnum.REGIONAL_ENCODER,
    FRSEnum.NATIONAL_VALIDATOR,
]))])
async def create_incident(...):
    ...
```

---

## RLS Context Wiring

### FastAPI Middleware Pattern

```python
from contextlib import asynccontextmanager
import psycopg2

@asynccontextmanager
async def get_db(request: Request):
    """Database session with RLS context."""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    try:
        # Set RLS context from authenticated user
        user: WimsUser = request.state.wims_user
        cursor.execute("SET LOCAL wims.current_user_id = %s", (user.user_id,))
        cursor.execute("SET LOCAL wims.current_role = %s", (user.role.value,))
        if user.region:
            cursor.execute("SET LOCAL wims.current_region = %s", (user.region,))
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
```

### get_current_wims_user Dependency

```python
async def get_current_wims_user(
    request: Request,
    token_data: dict = Depends(validate_token),
) -> WimsUser:
    """Extract WIMS user from JWT token and attach to request."""
    # Lookup user in wims.users table by keycloak_id
    user = await lookup_user_by_keycloak_id(token_data["sub"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Attach to request state for DB middleware
    request.state.wims_user = user
    return user
```

---

## Token Introspection (Optional)

For real-time token verification (catches revocations):

```python
async def introspect_token(token: str) -> bool:
    """Verify token is still active with Keycloak."""
    response = httpx.post(
        "https://keycloak.example.com/realms/wims/protocol/openid-connect/token/introspect",
        data={
            "token": token,
            "client_id": "wims-bfp-backend",
            "client_secret": CLIENT_SECRET,
        },
    )
    return response.json().get("active", False)
```

**Note:** Token introspection adds ~50ms latency. Use selectively:
- Critical endpoints (admin actions, financial operations)
- Session-sensitive operations (password changes)
- Not on every request (fallback to JWT validation)

---

## WIMS-BFP Security Checklist

### Keycloak Configuration
```
[ ] FRS roles created as realm roles (exact 5 literals)
[ ] Client scopes configured: wims:read, wims:write, wims:admin
[ ] Token lifespan: 10 minutes
[ ] Refresh token: single-use
[ ] MFA required for all users
```

### FastAPI Implementation
```
[ ] JWT validation with all 5 checks (kid, iss, aud, sig, exp)
[ ] get_current_wims_user dependency on all protected routes
[ ] require_role dependency for role-specific endpoints
[ ] get_db middleware sets RLS context (wims.current_user_id)
[ ] Role literals match FRS exactly (no aliases)
[ ] National Analyst enforced as read-only (no write endpoints)
[ ] Civilian Reporter limited to DMZ endpoints only
```

### Security
```
[ ] Client secret stored in secrets file (not env var)
[ ] JWKS endpoint cached (not fetched on every request)
[ ] Token not stored in localStorage (XSS risk)
[ ] CORS configured for frontend origin only
[ ] Rate limiting on token endpoint
```

---

## Related Pages

- [[sources/software-dev/keycloak-production-security]] — Keycloak hardening guide
- [[concepts/keycloak-fastapi-security-wims-bfp]] — WIMS-BFP security synthesis
- [[sources/cybersecurity/keycloak-cves-2026]] — Keycloak CVEs
- [[concepts/secure-coding-practices]] — OWASP/CWE coding standards
- [[mocs/cybersecurity]] — Cybersecurity Map of Content
