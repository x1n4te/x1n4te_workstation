---
id: fastapi-security-best-practices-2026-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - oneuptime.com/blog/post/2026-02-20-api-security-best-practices
  - peerlist.io/pravinkunnure9/articles/fastapi-security-made-easy
  - medium.com/@connect.hashblock/7-fastapi-security-patterns-that-actually-ship
status: active
tags:
  - fastapi
  - api-security
  - python
  - owasp-api
  - software-dev
related:
  - sources/software-dev/fastapi-cves-2025-2026
  - sources/software-dev/celery-redis-security
  - sources/software-dev/fastapi-keycloak-jwt-rbac
  - concepts/fastapi-security-wims-bfp
  - concepts/secure-coding-practices
  - mocs/cybersecurity
---

# FastAPI Security Best Practices (Source Summary)

**Sources:** OneUptime, Peerlist, Medium
**Type:** API security reference for Python/FastAPI
**Confidence:** High — based on OWASP API Security Top 10

---

## OWASP API Security Top 10 (2023)

| Rank | Category | WIMS-BFP Mitigation |
|---|---|---|
| API1 | Broken Object Level Auth | RLS (wims.current_user_id) |
| API2 | Broken Authentication | Keycloak JWT + MFA |
| API3 | Broken Object Property Auth | Pydantic validation, response filtering |
| API4 | Unrestricted Resource Consumption | Rate limiting, max payload sizes |
| API5 | Broken Function Level Auth | FRS role checks on every endpoint |
| API6 | Server Side Request Forgery | URL validation, restricted outbound |
| API7 | Security Misconfiguration | Hardened Docker, no defaults |
| API8 | Lack of Protection from Automated Threats | Rate limiting, CAPTCHA on auth |
| API9 | Improper Inventory Management | API docs hidden, no debug endpoints |
| API10 | Unsafe Consumption of APIs | Input validation on external API responses |

---

## 7 Security Patterns for FastAPI

### 1. JWT Validation (All 5 Checks)

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jwt import PyJWKClient
import jwt

security = HTTPBearer()

async def validate_token(credentials = Depends(security)) -> dict:
    """Validate JWT from Keycloak with all 5 checks."""
    token = credentials.credentials
    try:
        jwks = PyJWKClient("https://keycloak.example.com/realms/wims/protocol/openid-connect/certs")
        signing_key = jwks.get_signing_key_from_jwt(token)
        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience="wims-bfp-backend",
            issuer="https://keycloak.example.com/realms/wims",
            options={"require": ["exp", "iss", "aud", "sub"]},
        )
        return claims
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### 2. Object-Level Authorization (BOLA Prevention)

```python
@router.get("/incidents/{incident_id}")
async def get_incident(incident_id: str, user: WimsUser = Depends(get_current_user)):
    """Always filter by user context to prevent unauthorized access."""
    # RLS handles this at DB level, but double-check at API level too
    cursor = await get_db_cursor()
    cursor.execute(
        "SELECT * FROM wims.incidents WHERE id = %s", (incident_id,)
    )
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Not found")  # 404 not 403
    return result
```

### 3. Input Validation (Pydantic)

```python
from pydantic import BaseModel, Field, field_validator
import re

class IncidentCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(max_length=5000)
    severity: str = Field(pattern=r"^(LOW|MEDIUM|HIGH|CRITICAL)$")
    region: str = Field(min_length=2, max_length=50)
    
    @field_validator("title")
    @classmethod
    def no_script_tags(cls, v):
        if re.search(r"<script|javascript:", v, re.IGNORECASE):
            raise ValueError("Invalid characters in title")
        return v
```

### 4. Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/v1/incidents")
@limiter.limit("100/minute")
async def list_incidents(request: Request):
    ...

@app.post("/api/v1/incidents")
@limiter.limit("10/minute")
async def create_incident(request: Request):
    ...
```

### 5. CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://wims-bfp.example.com"],  # Only specific domain
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

### 6. Security Headers

```python
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response
```

### 7. Audit Logging

```python
import logging
logger = logging.getLogger("security")

async def log_security_event(event_type: str, user_id: str, resource: str, action: str, result: str):
    logger.info(f"SECURITY: {event_type} | user={user_id} | resource={resource} | action={action} | result={result}")
```

---

## WIMS-BFP FastAPI Audit Checklist

```
[ ] JWT validation: all 5 checks (kid, iss, aud, sig, exp)
[ ] BOLA prevention: RLS + API-level ownership checks
[ ] Pydantic: all route inputs validated with strict models
[ ] Rate limiting: per-endpoint limits (100/min read, 10/min write)
[ ] CORS: only wims-bfp.example.com allowed
[ ] Security headers: nosniff, DENY, HSTS, CSP
[ ] Debug endpoints: disabled in production
[ ] API docs: hidden or behind auth
[ ] Error responses: no stack traces or internal details
[ ] Audit logging: auth failures, RLS denials, admin actions
[ ] Request body size: limited (max 1MB)
[ ] Timeout: all external calls have timeouts
[ ] HTTPS only: no HTTP in production
```

---

## Related Pages

- [[sources/software-dev/fastapi-cves-2025-2026]] — FastAPI CVEs
- [[sources/software-dev/celery-redis-security]] — Celery + Redis security
- [[sources/software-dev/fastapi-keycloak-jwt-rbac]] — Keycloak JWT RBAC
- [[concepts/fastapi-security-wims-bfp]] — WIMS-BFP FastAPI security synthesis
- [[concepts/secure-coding-practices]] — OWASP/CWE coding standards
- [[mocs/cybersecurity]] — Cybersecurity Map of Content
