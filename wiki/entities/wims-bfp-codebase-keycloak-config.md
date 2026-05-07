---
id: wims-bfp-codebase-keycloak-config-001
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
  - keycloak
  - auth
  - security
related:
  - entities/wims-bfp-codebase-rbac-roles
  - concepts/wims-bfp-codebase-auth-flow
  - entities/wims-bfp-codebase-docker-services
---

# Keycloak Configuration

Identity provider for WIMS-BFP. Runs on `wims_internal` network at port 8080.

## Realm: `bfp`

| Setting | Value |
|---------|-------|
| Realm name | `bfp` |
| SSL required | `external` (none for local dev) |
| Login theme | Custom (BFP-branded FTL template) |
| Brute force detection | Enabled (`failureFactor: 5`, `waitIncrementSeconds: 60`) |

## Clients

| Client ID | Type | Auth | Purpose |
|-----------|------|------|---------|
| `bfp-client` | Public | PKCE | Frontend OIDC login |
| `bfp-admin-cli` | Confidential | Client Secret | Backend admin operations (user mgmt, session control) |

## Roles (Realm)

| Role | MFA | Description |
|------|-----|-------------|
| `CIVILIAN_REPORTER` | No | Public report submission |
| `REGIONAL_ENCODER` | No | Regional data entry |
| `NATIONAL_VALIDATOR` | Yes | Incident verification |
| `NATIONAL_ANALYST` | No | Analytics viewing |
| `SYSTEM_ADMIN` | Yes | Full admin access |

## Session Settings

| Setting | Value | FRS Requirement |
|---------|-------|-----------------|
| `ssoSessionIdleTimeout` | 1800 (30min) | 30min inactivity ✅ |
| `ssoSessionMaxLifespan` | 36000 (10h) | 8h max ⚠️ (needs 28800) |
| Access token lifespan | 300 (5min) | — |
| Access token lifespan (SSO) | 1800 (30min) | — |

## Password Policy

```
length(12) and upperCase(1) and lowerCase(1) and digits(1) and specialChars(1) and notUsername(undefined)
```

## Environment Variables

```bash
KEYCLOAK_REALM_URL=http://localhost:8080/auth/realms/bfp
KEYCLOAK_CLIENT_ID=bfp-client
KEYCLOAK_AUDIENCE=bfp-client
KEYCLOAK_ISSUER=http://localhost:8080/auth/realms/bfp/
```

## Related

- [[entities/wims-bfp-codebase-rbac-roles]] — role definitions and guard implementation
- [[concepts/wims-bfp-codebase-auth-flow]] — full authentication pipeline
- [[entities/wims-bfp-codebase-docker-services]] — Keycloak container details
