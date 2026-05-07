# FRS Module 14 — Public Anonymous Incident Submission

> **Status:** NEW MODULE
> **Implementation:** `api/public_dmz.py`
> **Rationale:** Unauthenticated public portal with Redis IP-based rate limiting. Distinct from the authenticated civilian submission flow. Enforces no-auth design decision — reporting fire incidents must not require login.

---

## Module 14: Public Anonymous Incident Submission

### 14.1 Overview

| Attribute | Detail |
|-----------|--------|
| Module ID | 14 |
| Category | Public-Facing / Zero-Trust Ingestion |
| Auth Required | None |
| Rate Limit | 3 requests per IP per hour (Redis) |
| Implementation | `src/backend/api/routes/public_dmz.py` |
| Endpoint | `POST /api/v1/public/report` |
| Verification Status | `PENDING_VALIDATION` (requires National Validator review) |

### 14.2 Purpose

The system provides a frictionless, publicly accessible incident reporting channel requiring no account creation or authentication. This ensures that civilians can report fire incidents without delay. Abuse is controlled exclusively through Redis-based IP rate limiting rather than authentication gates.

### 14.3 Functional Specification

**14.3.1 Anonymous Submission**

- Public unauthenticated endpoint `POST /api/v1/public/report`
- Accepts: `latitude`, `longitude`, `description`, `incident_type`
- Inserts directly into `wims.fire_incidents` with `encoder_id = NULL`
- All records receive `verification_status = 'PENDING_VALIDATION'`

**14.3.2 Rate Limiting**

- Redis-backed sliding window: max 3 submissions per IP per 3600-second window
- HTTP 429 returned with `Retry-After` header on violation
- Enforcement occurs before any database write

**14.3.3 Geographic Routing**

- `region_id` auto-resolved via nearest-centroid query against `wims.ref_regions`
- Fallback to first seeded region if no geometry intersection found
- Prevents hard failure from invalid coordinates

### 14.4 Security Posture

| Property | Value |
|----------|-------|
| Authentication | None (zero-trust) |
| RLS Context | None set (`encoder_id = NULL`) |
| Abuse Control | Rate limiting only |
| Trust Score | 0 (unauthenticated) |
| Audit Trail | Logs IP address at web server level only |

### 14.5 Out of Scope

- Attachment uploads (requires authenticated session — Module 2)
- Submission status tracking (Phase 2)
- Email/SMS confirmations
- CAPTCHA (friction incompatible with emergency reporting)
