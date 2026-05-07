---
id: wims-bfp-frs-modules-003
type: analysis
created: 2026-04-21
updated: 2026-05-04
last_verified: 2026-05-04
review_after: 2026-06-04
stale_after: 2026-08-04
confidence: high
source_refs:
  - raw/sources/wims-bfp-codebase/module1.md
  - raw/sources/wims-bfp-codebase/module2.md
  - raw/sources/wims-bfp-codebase/module3.md
  - raw/sources/wims-bfp-codebase/module4.md
  - raw/sources/wims-bfp-codebase/module5.md
  - raw/sources/wims-bfp-codebase/module6.md
  - raw/sources/wims-bfp-codebase/module7.md
  - raw/sources/wims-bfp-codebase/module8.md
  - raw/sources/wims-bfp-codebase/module9.md
  - raw/sources/wims-bfp-codebase/module10.md
  - raw/sources/wims-bfp-codebase/module11.md
  - raw/sources/wims-bfp-codebase/module12.md
  - raw/sources/wims-bfp-codebase/module13.md
  - raw/articles/wims-bfp-frs-consolidated-2026-05-04.md
status: active
tags:
  - wims-bfp
  - frs
  - design
  - implementation-tracker
related:
  - analyses/wims-bfp-frs-implementation-tracker
  - concepts/wims-bfp-sprint-timeline
  - concepts/wims-bfp-sprint-gantt
  - mocs/wims-bfp
  - sources/articles/wims-bfp-frs-consolidated-2026-05-04
---

# FRS Modules — Implementation Tracker (Codebase-Verified)

Functional Requirements Specification for WIMS-BFP. **15 modules** covering the full system scope. Source files in `raw/sources/wims-bfp-codebase/module{N}.md` and the consolidated specification in [[sources/articles/wims-bfp-frs-consolidated-2026-05-04]].

**Supersedes:** The older [[analyses/wims-bfp-frs-implementation-tracker]] which used a 6-area (FR-1 through FR-6) format from thesis Chapter 3a. This page uses the 15-module FRS format which maps more directly to sprint tasks.

## Module Overview

| # | Module | Key Tech | Status |
|---|--------|----------|--------|
| 1 | Authentication & Access Control | Keycloak Browser Flow + OTP | 90% (session mgmt missing) |
| 2 | Offline-First Incident Management | idb + Service Worker, AFOR import | 30% (skeleton, laqqui on AFOR) |
| 3 | Conflict Detection & Manual Verification | RapidFuzz + SQL Intervals | NOT STARTED |
| 4 | Data Commit and Immutable Storage | PostgreSQL append-only, GRANT/REVOKE | NOT STARTED |
| 5 | Analytics and Reporting | Materialized Views, SQLAlchemy + Pandas | **DONE** (87/87 tests green) |
| 5d | Public Anonymous Incident Submission | Redis rate limiting, Pydantic | **DONE** (endpoint + rate limit) |
| 6 | Cryptographic Security | AES-256-GCM, OpenBao | HALF (queue expanded: 6 phases, 17 features) |
| 7 | Intrusion Detection & Network Monitoring | Suricata AF_PACKET | HALF |
| 8 | Threat Detection with Explanation AI (XAI) | Qwen2.5-3B, Llama.cpp | NOT STARTED |
| 9 | System Monitoring and Health Dashboard | psutil, Docker API | NOT STARTED |
| 10 | Compliance and Data Privacy | RA 10173, Data Minimization | NOT STARTED |
| 11 | Penetration Testing and Security Validation | Nmap, OWASP ZAP, sqlmap | Procedure |
| 12 | User Management and Administration | python-keycloak Admin Client | **DONE** |
| 13 | Notification System | SSE, react-hot-toast | DEFERRED |
| 14 | Public Anonymous Incident Submission | Zero-trust endpoint, Redis rate limit | **DONE** (new module) |
| 15 | Reference Data Service | Read-only API, RLS | NOT STARTED |

## Module 1: Authentication & Access Control

**Source:** `raw/sources/wims-bfp-codebase/module1.md`  
**Wiki pages:** concepts/wims-bfp-codebase-auth-flow, entities/wims-bfp-codebase-rbac-roles, entities/wims-bfp-codebase-keycloak-config  
**Status:** 90% — auth works, session management incomplete

### A. User Authentication — DONE
- Login with username/password (min 8 chars: upper, lower, digit, special) — Keycloak Browser Flow
- MFA for SYSTEM_ADMIN + NATIONAL_VALIDATOR — TOTP, 7-day trusted device — Keycloak OTP Policy
- Account lockout after 5 failed attempts — Keycloak Brute Force Detection (`bruteForceProtected: true`, `failureFactor: 5`)
- Auto session timeout after 30min inactivity — `ssoSessionIdleTimeout: 1800`

### B. Password Management — DONE
- Reset via secure email link (15min expiry) — Keycloak "Forgot Password"
- Change password for authenticated users — requires current password verification
- Strong password policy — `length(12) and upperCase(1) and lowerCase(1) and digits(1) and specialChars(1)`
- Password expiry: 90 days for admin roles

### C. RBAC — DONE
- 5 roles: CIVILIAN_REPORTER, REGIONAL_ENCODER, NATIONAL_VALIDATOR, NATIONAL_ANALYST, SYSTEM_ADMIN
- Least privilege enforced via RLS + route guards
- Role assignment restricted to SYSTEM_ADMIN

### D. Session Management — PARTIAL (MISSING D.4 + D.5)

| # | Requirement | Status |
|---|------------|--------|
| D.1 | Generate secure session token (OIDC) | DONE |
| D.2 | Store in httpOnly + secure + sameSite | DONE |
| D.3 | Auto-renewal on activity (8h max) | HALF — `ssoSessionMaxLifespan: 36000` (10h, not 8h) |
| D.4 | Force logout on password change or role modification | NOT DONE |
| D.5 | Concurrent session detection + terminate option | NOT DONE |

### What's Missing (Sprint 6)
1. Adjust `ssoSessionMaxLifespan` to 28800 (8h) per FRS
2. Add backchannel logout trigger on password change and role modification
3. Backend session listing/termination endpoints
4. Frontend active sessions view

## Module 2: Offline-First Incident Management

**Source:** `raw/sources/wims-bfp-codebase/module2.md`  
**Status:** 30% — skeleton exists, most offline/sync features missing

### Key Implementation Points
- `offlineStore.ts` (64 lines) — idb-based queue buffer, NOT a full offline DB
- `sw.js` (141 lines) — Background Sync handler exists
- `NetworkStatusIndicator.tsx` — offline mode indicator exists
- Missing: queue encryption, queue management UI, integrity verification, atomic sync, retry logic

## Module 3: Conflict Detection & Manual Verification

**Source:** `raw/sources/wims-bfp-codebase/module3.md`  
**Status:** NOT STARTED

### Key Implementation Points
- Frontend `runConflictDetection()` calls non-existent backend endpoint
- No RapidFuzz dependency in requirements.txt
- Detection: exact location+time match (30-min window), narrative similarity (80% threshold), casualty match

## Module 4: Data Commit & Immutable Storage

**Source:** `raw/sources/wims-bfp-codebase/module4.md`  
**Status:** NOT STARTED

### Key Implementation Points
- DB has soft-delete (`deleted_at` columns) — no append-only enforcement
- No `version_id` or `original_record_id` columns
- Needs: GRANT/REVOKE on committed records, version chain, status gate

## Module 5: Analytics and Reporting

**Source:** `raw/sources/wims-bfp-codebase/module5.md`  
**Status:** **DONE** — 87/87 tests green (54 backend + 33 frontend), from 5% baseline

### Implementation Summary (all 4 phases)
- **Phase 1 Foundation:** 4 materialized views (daily counts, by region, by barangay, type dist.), schema expansion (8 new columns), Celery beat hourly refresh
- **Phase 2 Filters+Charts:** casualty severity filter, damage range filter, type distribution pie chart, top-10 barangays bar chart, response time by region chart
- **Phase 3 Export:** PDF export (WeasyPrint), Excel export (openpyxl), analytics_export_log table with RLS
- **Phase 4 Extensions:** multi-region select, cross-region comparison, top-N configurable, scheduled reports CRUD (Celery beat + SMTP)

### Key Implementation Points
- Routes: `analytics.py` — heatmap, trends, comparative, CSV, type-distribution, top-barangays, response-time, compare-regions, top-n, export/pdf, export/excel
- DB migrations: `05_analytics_materialized_views.sql`, `05_analytics_facts_expand.sql`, `07_analytics_export_log.sql`, `08_scheduled_reports.sql`
- Components: HeatmapViewer, TrendCharts, TypeDistributionChart, TopBarangaysChart, ResponseTimeChart, CrossRegionTable
- Celery tasks: `analytics_refresh.py` (hourly MV refresh), `exports.py` (PDF/Excel generation)

## Module 5d: Public Anonymous Incident Submission

**Source:** `raw/articles/wims-bfp-frs-consolidated-2026-05-04.md` (revised)  
**Status:** **DONE** — endpoint + Redis rate limiting implemented

### Key Implementation Points
- Zero-trust public endpoint at POST `/api/v1/public/report` — no authentication
- Redis rate limiting: 3 submissions per IP per rolling hour, HTTP 429 with Retry-After
- Anonymous submissions stored with `encoder_id = NULL` and `verification_status = PENDING_VALIDATION`
- Region resolution via nearest-centroid query against `wims.ref_regions`
- No PII collected beyond operationally necessary data
- Pydantic schema validation before database write
- No CAPTCHA — rate limiting is sole abuse prevention

## Module 6: Cryptographic Security (EXPANDED)

**Source:** `raw/sources/wims-bfp-codebase/module6.md`  
**Status:** HALF — queue expanded from 4→6 phases (17 features total)

### Key Implementation Points
- `crypto.py` — AES-256-GCM SecurityProvider working
- `WIMS_MASTER_KEY` env var — base64 32-byte key
- Queue phases: (1) expanded PII encryption, (2) SQLAlchemy TypeDecorator, (3) key rotation, (4) TLS enforcement, (5) blob versioning + rollback, (6) internal TLS + PII audit log
- Missing: key rotation, TLS enforcement, blob versioning

## Module 7: Intrusion Detection & Network Monitoring

**Source:** `raw/sources/wims-bfp-codebase/module7.md`  
**Status:** HALF

### Key Implementation Points
- Suricata container running with rules
- `suricata_ingestion.py` + Celery beat task (10s interval)
- Missing: AF_PACKET tuning, app-layer parser config

## Module 8: Threat Detection with Explanation AI (XAI)

**Source:** `raw/sources/wims-bfp-codebase/module8.md`  
**Status:** NOT STARTED

### Key Implementation Points
- `ai_service.py` exists but stub/empty
- Ollama Docker container available with Qwen2.5-3B
- Missing: prompt templates, inference pipeline, on-demand mode

## Module 9: System Monitoring and Health Dashboard

**Source:** `raw/sources/wims-bfp-codebase/module9.md`  
**Status:** NOT STARTED

## Module 10: Compliance and Data Privacy

**Source:** `raw/sources/wims-bfp-codebase/module10.md`  
**Status:** NOT STARTED

## Module 11: Penetration Testing and Security Validation

**Source:** `raw/sources/wims-bfp-codebase/module11.md`  
**Status:** Procedure

## Module 12: User Management and Administration

**Source:** `raw/sources/wims-bfp-codebase/module12.md`  
**Status:** **DONE**

### Key Implementation Points
- User onboarding via python-keycloak Admin Client
- Self-service profile view/update/password change
- Admin user management (System Admin only)
- Keycloak integration complete

## Module 13: Notification System

**Source:** `raw/sources/wims-bfp-codebase/module13.md`  
**Status:** DEFERRED — pending completion of all role dashboards

## Module 14: Public Anonymous Incident Submission

**Source:** `raw/articles/wims-bfp-frs-consolidated-2026-05-04.md` (new module)  
**Status:** **DONE** — zero-trust endpoint implemented

### Key Implementation Points
- Zero-trust public endpoint at POST `/api/v1/public/report` — no authentication, no session
- Redis rate limiting: 3 requests per IP per rolling hour, HTTP 429 with Retry-After
- Anonymous submissions: `encoder_id = NULL`, `verification_status = PENDING_VALIDATION`
- Region resolution via nearest-centroid query against `wims.ref_regions`
- No PII collected beyond operationally necessary data
- Pydantic schema validation before database write
- No CAPTCHA — rate limiting is sole abuse prevention

## Module 15: Reference Data Service

**Source:** `raw/articles/wims-bfp-frs-consolidated-2026-05-04.md` (new module)  
**Status:** NOT STARTED

### Key Implementation Points
- Authenticated read-only API for geographic reference hierarchy
- Endpoints: `/api/ref/regions`, `/api/ref/provinces`, `/api/ref/cities`
- RLS restricts visibility: REGIONAL_ENCODER/VALIDATOR see only their region; NATIONAL_ANALYST/ADMIN see all
- Source: `wims.ref_regions`, `wims.ref_provinces`, `wims.ref_cities` — no write operations exposed

## FR Mapping (Cross-Reference to Old Tracker)

| Old (6-area) | New (15-module) | Notes |
|---------------|-----------------|-------|
| FR-1 Crowdsourced Reporting | Module 2 (Offline-First) | Partial overlap |
| FR-2 Geospatial Mapping | Module 5 (Analytics) | Partial overlap |
| FR-3 Data Synchronization | Module 2.C (Sync) | Partial overlap |
| FR-4 Access Control | Module 1 (Auth) + Module 12 (User Mgmt) | Split across 2 modules |
| FR-5 Threat Detection | Module 7 (IDS) + Module 8 (XAI) | Split across 2 modules |
| FR-6 Forensic Reporting | Module 4 (Immutable) + Module 10 (Compliance) | Split across 2 modules |

## Related

- [[concepts/wims-bfp-sprint-timeline]] — sprint schedule for all modules
- [[analyses/wims-bfp-frs-implementation-tracker]] — older FR-1 to FR-6 format
- [[mocs/wims-bfp]] — project map of content
- [[sources/articles/wims-bfp-frs-consolidated-2026-05-04]] — full consolidated specification
