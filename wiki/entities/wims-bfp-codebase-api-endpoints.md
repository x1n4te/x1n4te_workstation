---
id: wims-bfp-codebase-api-endpoints-001
type: entity
created: 2026-04-21
updated: 2026-04-21
last_verified: 2026-04-21
review_after: 2026-06-21
stale_after: 2026-10-21
confidence: high
source_refs:
  - raw/sources/wims-bfp-codebase/docs/API_AND_FUNCTIONS.md
  - raw/sources/wims-bfp-codebase/docs/ARCHITECTURE.md
status: active
tags:
  - wims-bfp
  - api
  - fastapi
  - endpoint
related:
  - entities/wims-bfp-codebase-database-schema
  - entities/wims-bfp-codebase-rbac-roles
  - concepts/wims-bfp-codebase-auth-flow
---

# API Endpoints

All backend + frontend API routes. Backend prefix: `/api`. Auth: Keycloak JWT bearer token.

## Public (No Auth)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/public/report` | Civilian fire incident report (DMZ) |

## Auth

| Method | Path | Role | Description |
|--------|------|------|-------------|
| POST | `/api/auth/callback` | — | Keycloak OIDC callback with PKCE |
| GET | `/api/auth/me` | Any | Current user profile from JWT |

## Civilian

| Method | Path | Role | Description |
|--------|------|------|-------------|
| POST | `/api/civilian/reports` | CIVILIAN_REPORTER | Submit fire report |
| GET | `/api/civilian/reports` | CIVILIAN_REPORTER | List own reports |

## Regional

| Method | Path | Role | Description |
|--------|------|------|-------------|
| GET | `/api/regional/incidents` | REGIONAL_ENCODER | List incidents in region |
| POST | `/api/regional/incidents` | REGIONAL_ENCODER | Create incident |
| GET | `/api/regional/incidents/{id}` | REGIONAL_ENCODER | Incident detail (with PostGIS coords) |
| PUT | `/api/regional/incidents/{id}` | REGIONAL_ENCODER | Update incident |
| POST | `/api/regional/afor/import` | REGIONAL_ENCODER | Import AFOR XLSX/CSV |
| POST | `/api/regional/incidents/{id}/attachments` | REGIONAL_ENCODER | Upload attachment |

## Triage / Validation

| Method | Path | Role | Description |
|--------|------|------|-------------|
| GET | `/api/triage/pending` | NATIONAL_VALIDATOR | Pending incidents queue |
| POST | `/api/triage/{id}/promote` | NATIONAL_VALIDATOR | Verify/reject incident |

## Analytics

| Method | Path | Role | Description |
|--------|------|------|-------------|
| GET | `/api/analytics/heatmap` | NATIONAL_ANALYST | PostGIS heatmap data |
| GET | `/api/analytics/trends` | NATIONAL_ANALYST | Incident trends |
| GET | `/api/analytics/comparative` | NATIONAL_ANALYST | Comparative analysis |
| GET | `/api/analytics/export` | NATIONAL_ANALYST | CSV export |

## Admin

| Method | Path | Role | Description |
|--------|------|------|-------------|
| GET | `/api/admin/users` | SYSTEM_ADMIN | List users |
| POST | `/api/admin/users` | SYSTEM_ADMIN | Create user (via Keycloak) |
| PUT | `/api/admin/users/{id}` | SYSTEM_ADMIN | Update user |
| GET | `/api/admin/security-logs` | SYSTEM_ADMIN | Security threat logs |
| POST | `/api/admin/security-logs/{id}/analyze` | SYSTEM_ADMIN | Trigger XAI analysis |
| GET | `/api/admin/audit-logs` | SYSTEM_ADMIN | Audit trail |

## User (Self-Service)

| Method | Path | Role | Description |
|--------|------|------|-------------|
| GET | `/api/user/me` | Any | Own profile |
| PATCH | `/api/user/me` | Any | Update own profile |
| PATCH | `/api/user/me/password` | Any | Change own password |

## Reference

| Method | Path | Role | Description |
|--------|------|------|-------------|
| GET | `/api/ref/regions` | Any | Philippine regions list |

## Related

- [[entities/wims-bfp-codebase-database-schema]] — tables backing these endpoints
- [[entities/wims-bfp-codebase-rbac-roles]] — role-based access control
- [[concepts/wims-bfp-codebase-auth-flow]] — authentication pipeline
