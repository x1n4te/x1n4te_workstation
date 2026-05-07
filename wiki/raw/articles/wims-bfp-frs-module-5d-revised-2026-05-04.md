# FRS Module 5d — Public Anonymous Incident Submission (REVISED)

> **Status:** REVISED — removed citizen authentication requirement
> **Based on:** User decision 2026-05-04
> **Implementation:** `api/public_dmz.py`
> **Supersedes:** Previous Module 5d (Citizen Auth Portal / Citizen Dashboard)

---

## Module 5d: Public Anonymous Incident Submission

### 1. Module Overview

| Field | Value |
|-------|-------|
| Module ID | 5d |
| Module Name | Public Anonymous Incident Submission |
| Category | Public-Facing Ingestion |
| Implementation | `api/public_dmz.py` (`POST /api/v1/public/report`) |
| Authentication | None (zero-trust architecture) |
| Rate Limiting | Redis — 3 requests per IP per hour |

### 2. Purpose

The system shall provide a publicly accessible incident submission portal that allows any civilian to report fire incidents without requiring account creation, login, or any form of authentication. This design decision prioritizes **reporting frictionlessness** — requiring authentication before submitting a fire report creates a barrier that directly conflicts with the urgency of emergency reporting. Abuse prevention is handled exclusively through rate limiting rather than access control.

### 3. Functional Requirements

#### 5d.1 Anonymous Submission Endpoint

- [ ] `POST /api/v1/public/report` shall accept incident reports without requiring any authentication token, cookie, or session
- [ ] The endpoint shall accept the following fields:
  - `latitude` (float, required) — WGS84 decimal degrees
  - `longitude` (float, required) — WGS84 decimal degrees
  - `description` (string, required) — free-text incident narrative
  - `incident_type` (enum, required) — one of: `STRUCTURE_FIRE`, `VEHICULAR_FIRE`, `GRASS_FIRE`, `OTHER`
  - `occurred_at` (ISO 8601 datetime, optional) — timestamp of incident; defaults to server time
- [ ] The endpoint shall return a structured response containing:
  - `incident_id` (UUID) — assigned by the central database
  - `verification_status` — always `PENDING_VALIDATION`
  - `created_at` (datetime) — server-side commit timestamp
  - `latitude`, `longitude` — confirmed coordinates

#### 5d.2 Rate Limiting

- [ ] Each unique source IP address shall be limited to a maximum of **3 submissions per rolling 1-hour window**
- [ ] Rate limit state shall be stored in Redis with TTL of 3600 seconds
- [ ] Exceeding the rate limit shall return HTTP 429 (Too Many Requests) with header `Retry-After`
- [ ] Rate limiting shall be applied **before** any database write operation

#### 5d.3 Data Routing and Region Resolution

- [ ] Submitted incidents shall be automatically assigned to the appropriate region based on geographic coordinates
- [ ] Region resolution shall use a nearest-centroid heuristic against `wims.ref_regions` geometry
- [ ] If no region geometry intersects the submitted coordinates, the system shall assign the incident to the first seeded region (fail-safe; prevents hard failure)
- [ ] The `encoder_id` field shall be set to `NULL` for all anonymous submissions (distinguishes anonymous records from authenticated records)

#### 5d.4 Verification Status Routing

- [ ] All anonymously submitted incidents shall be assigned `verification_status = 'PENDING_VALIDATION'`
- [ ] These records shall enter the same triage queue as authenticated submissions from Regional Encoders
- [ ] National Validators shall review and promote/reject anonymous submissions through the same workflow defined in Module 3

### 4. Security Requirements

| ID | Requirement | Threat Mitigated |
|----|-------------|-----------------|
| SEC-5d-1 | No JWT, session cookie, or credential exchange shall occur on the public endpoint | Information Disclosure |
| SEC-5d-2 | Redis rate limiting shall be enforced at the application layer before database connection acquisition | Denial of Service / Spam |
| SEC-5d-3 | All submitted data shall be treated as untrusted and subject to input validation (Pydantic schema) | Injection attacks |
| SEC-5d-4 | encoder_id shall be NULL — no authenticated user context shall be set on this request | Spoofing prevention |

### 5. Data Handling

- [ ] Anonymous submissions shall be stored in the same `wims.fire_incidents` table as authenticated submissions
- [ ] Anonymous records shall be visually distinguishable in the National Validator triage queue by `encoder_id = NULL`
- [ ] No personally identifiable information (PII) shall be collected beyond what is operationally necessary
- [ ] Data retention for anonymous submissions follows the same policy as Module 4 (append-only, indefinite retention post-validation)

### 6. Constraints and Design Decisions

| Decision | Rationale |
|----------|-----------|
| No CAPTCHA | Adds friction incompatible with emergency reporting; rate limiting is the abuse vector control |
| No IP-based geographic blocking | BFP coverage is national; geographic restrictions would block legitimate reporters near jurisdictional boundaries |
| NULL encoder_id | Ensures anonymous records are never mistaken for authenticated encoder submissions; enables audit distinction |
| PENDING_VALIDATION routing | All public submissions require National Validator review before entering the canonical dataset — prevents bogus data from polluting analytics without review |

### 7. Out of Scope

- Citizen authentication and login — removed per revision
- Citizen dashboard for tracking submission status — future Phase 2
- Email or SMS confirmation to submitter — no PII collected
- Attachment upload for anonymous submissions — attachments require authenticated session (Module 2)
- Rate limit exemption for verified BFP personnel — BFP personnel use authenticated Module 2 portal
