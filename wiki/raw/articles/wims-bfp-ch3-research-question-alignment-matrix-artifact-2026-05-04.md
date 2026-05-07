# WIMS-BFP — Ch3 Research Question Alignment Matrix

> **Status:** Thesis-ready artifact — WIMS-BFP-specific, built from actual implemented modules
> **Chapter:** 3 — Methodology
> **Section:** Requirements Analysis → Security Requirements
> **Based on:** `wims-bfp-research-question-alignment-matrix-2026-05-04` (source #2)
> **FRS modules:** `~/Documents/WIMS-BFP-FRS-Modules-2026-05-04.md`
> **Specific objectives:** User-provided (2026-05-04)

---

## 3.X Research Question Alignment Matrix

The study employs a Research Question Alignment Matrix to ensure that every specific objective stated in Chapter 1 has a corresponding evaluation measure and security validation activity in Chapter 3, with results reported in Chapter 4. This approach guarantees traceable alignment from problem identification to evidence collection, addressing the following questions for each objective: (1) Which objective is being measured? (2) How will functionality be evaluated? (3) What security risks are relevant? (4) What test will validate the safeguard? (5) What result should appear in Chapter 4?

### Evaluation Standards Reference

| Area | Standard Reference |
|------|-------------------|
| Functionality Evaluation | ISO/IEC 25010 |
| Security Testing | OWASP ASVS (Application Security Verification Standard) |
| Testing Process | NIST SP 800-115 (Technical Security Testing) |
| Threat Identification | STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) |

---

## 3.X.1 Research Objective Alignment Matrix

| # | Specific Objective | Functional Output / Module | Functionality Evaluation | STRIDE Threat | Security Test / Metric | Expected Chapter 4 Evidence |
|---|---|---|---|---|---|---|
| 1 | Design and develop a PWA enabling offline data capture utilizing FastAPI backend and IndexedDB for local caching and synchronization | **Module 2** — Offline-First Incident Management | Functional Suitability | **Tampering** | Offline data integrity on sync; duplicate incident detection; successful sync completion rate | Offline-First PWA Evaluation Results |
| 2 | Implement Role-Based Access Control (RBAC) governed by Keycloak, enforcing the principle of least privilege within the PWA | **Module 1** — Authentication and Access Control | Functional Suitability, Usability | **Spoofing** | Authentication lockout after 5 failed attempts; role access restriction enforcement; JWT token expiry behavior; session revocation | Authentication & Authorization Security Results |
| 3 | Establish a robust cryptographic pipeline utilizing AES-256-GCM and TLS 1.3 protocols to ensure strict data protection at rest and in transit, protecting sensitive BFP repositories from information disclosure | **Module 6** — Cryptographic Security | Reliability, Information Disclosure | **Information Disclosure** | HTTPS enforcement verification; unauthorized access block rate; encrypted field access tests | Data Protection & Cryptographic Results |
| 4 | Integrate a Suricata IDS for deterministic network anomaly detection alongside the Qwen2.5-3B SLM as an Explainable AI (XAI) engine to translate complex security alerts into human-readable forensic narratives | **Modules 7 & 8** — Intrusion Detection; Threat Detection with XAI | Functional Suitability, Explainability | **Repudiation**, **Information Disclosure** | Suricata rule coverage; alert-to-narrative translation accuracy; AI response time under load | Threat Detection & XAI Explainability Results |
| 5 | Establish a secure ingestion framework providing a public-facing civilian reporting portal—protected by email-based account verification and per-account rate limiting—paired with a triage workflow and geographically-bound controls ensuring operational integrity of verified incident data | **Module 5d** — Public Anonymous Incident Submission; **Module 3** — Conflict Detection and Manual Verification | Functional Correctness, Task Appropriateness | **Tampering**, **Elevation of Privilege** | Rate limit enforcement (requests per IP per hour); unauthorized record modification detection; geographic boundary enforcement | Civilian Reporting Security & Triage Results |
| 6 | Establish a National Analytics module utilizing PostGIS performing geospatial clustering and visualization via heatmaps, alongside dynamic comparative analysis and variance tracking across multiple categories within user-defined date ranges to support executive policy and resource optimization | **Module 5** — Analytics and Reporting; **Module 15** — Reference Data Service | Functional Suitability, Performance Efficiency | N/A (functional/performance objective) | Analytics query response time; geospatial clustering correctness; heatmap rendering completeness | National Analytics Module Evaluation Results |
| 7 | Align system architecture with the Data Privacy Act of 2012 (RA 10173) and ISO/IEC 27001 by mechanically enforcing data minimization through PostgreSQL Row-Level Security (RLS) policies, supported by the administrative production of a Data Privacy Impact Assessment (DPIA) and Records of Processing Activities (ROPA) | **Module 10** — Compliance and Data Privacy | Functional Suitability, Reliability | **Tampering**, **Repudiation**, **Information Disclosure** | Unauthorized cross-region data access attempts blocked by RLS; audit log completeness; RLS policy enforcement verification | Data Privacy & Compliance Results |
| 8 | Execute rigorous security testing achieving OWASP ASVS Level 2 compliance, validating the system's defense against the STRIDE threat model across Identity, Cryptography, Forensic Logging, Threat Detection, and Infrastructure Resilience | **Module 11** — Penetration Testing and Security Validation | All applicable | **All STRIDE categories** | ASVS Level 2 checklist compliance rate; per-category pass/fail tally; penetration test outcomes | Security Testing and Vulnerability Assessment Results |
| 9 | Evaluate WIMS-BFP according to ISO/IEC 25010 standards, specifically assessing the Usability and Reliability of the offline-first web application, as well as the Functional Suitability and Performance Efficiency of the local AI module | **Module 2** (PWA); **Module 8** (AI); **Module 9** (System Monitoring) | Usability, Reliability, Functional Suitability, Performance Efficiency | N/A (evaluation framework) | ISO 25010 survey weighted mean per category; AI inference latency; system error rate under normal operation | System Quality Evaluation Results |

---

## 3.X.2 STRIDE Threat Category Summary

| STRIDE Category | Threat Description | Mitigated By | FRS Module Reference |
|---|---|---|---|
| **Spoofing** | Impersonating an authorized user to gain unauthorized access | MFA enforcement via Keycloak; JWT HttpOnly cookies; account lockout after 5 failed attempts | Module 1 (Auth & Access Control) |
| **Tampering** | Modifying data or records without authorization | SQLAlchemy ORM (parameterized queries); PostgreSQL RLS policies; audit trail | Module 4 (Data Commit); Module 10 (Compliance) |
| **Repudiation** | User denies having performed an action | Immutable audit logs (`log_system_audit()`); tamper-detection on log records | Module 4 (Data Commit & Immutable Storage) |
| **Information Disclosure** | Exposing sensitive data to unauthorized parties | AES-256-GCM field encryption; HTTPS/TLS 1.3; RLS column-level restrictions; HttpOnly/Secure/SameSite | Module 6 (Cryptographic Security); Module 10 (Compliance) |
| **Denial of Service** | Making the system unavailable to authorized users | Redis/Celery background tasks; offline PWA with Service Worker + IndexedDB; graceful degradation | Module 2 (Offline-First Incident Mgmt) |
| **Elevation of Privilege** | Gaining capabilities beyond authorized scope | Keycloak RBAC with least privilege; role-scoped API routes; RLS at database layer | Module 1 (Auth & Access Control); Module 3 (Conflict Detection) |

---

## 3.X.3 FRS Module Inventory (Ground Truth)

| ID | Module Name | Implementation | Status |
|---|---|---|---|
| 1 | Authentication and Access Control | `api/admin`, `api/sessions`, `services/keycloak_admin.py`, Keycloak config | Implemented |
| 2 | Offline-First Incident Management | `api/incidents`, `pages/report`, `pages/incidents` | Implemented |
| 3 | Conflict Detection and Manual Verification | `api/triage` | Implemented |
| 4 | Data Commit and Immutable Storage | `api/incidents`, `utils/audit.py` | Implemented |
| 5 | Analytics and Reporting | `api/analytics`, `services/analytics_read_model.py` | Implemented |
| 5d | Public Anonymous Incident Submission | `api/public_dmz.py`, `api/civilian.py` | REVISED — no-auth, rate-limited |
| 6 | Cryptographic Security | `services/ai_service.py`, `database.py`, reverse proxy TLS config | Implemented |
| 7 | Intrusion Detection and Network Monitoring | `services/suricata_ingestion.py` | Implemented |
| 8 | Threat Detection with Explanation AI (XAI) | `services/ai_service.py`, `services/suricata_ingestion.py` | Implemented |
| 9 | System Monitoring and Health Dashboard | Admin dashboard | Implemented |
| 10 | Compliance and Data Privacy | `database.py`, `auth.py`, RLS policies | Implemented |
| 11 | Penetration Testing and Security Validation | Testing procedures | Procedure (not code) |
| 12 | User Management and Administration | `api/admin`, `api/user` | Implemented |
| 13 | Notification System | SSE endpoints | DEFERRED |
| 14 | Public Anonymous Incident Submission | `api/public_dmz.py` | NEW — see Module 5d |
| 15 | Reference Data Service | `api/ref.py` | NEW |

---

## 3.X.4 Codebase Module Inventory (FRS → Implementation Mapping)

### Backend API Routes (`src/backend/api/routes/`)

| FRS Module | Route File | Purpose |
|---|---|---|
| Module 1 | `admin.py`, `sessions.py` | Keycloak user lifecycle, session revocation |
| Module 2 | `incidents.py` | Incident CRUD, bundle upload, attachment storage |
| Module 3 | `triage.py` | ENCODER/VALIDATOR promotion workflow |
| Module 4 | `incidents.py`, `utils/audit.py` | Immutable commit, audit log generation |
| Module 5 | `analytics.py` | National Analyst read-only PostGIS queries |
| Module 5d | `public_dmz.py`, `civilian.py` | Zero-trust public submission (no auth); rate-limited |
| Module 9 | `admin.py` | System health monitoring |
| Module 12 | `admin.py`, `user.py` | User onboarding, profile self-service |
| Module 15 | `ref.py` | Geographic reference data lookup (regions, provinces, cities) |
| — | `regional.py` | Regional-scoped incident operations (sub-component of Module 2) |

### Backend Services (`src/backend/services/`)

| FRS Module | Service File | Purpose |
|---|---|---|
| Module 6 | `ai_service.py`, `database.py` | AES-256-GCM encryption, TLS termination |
| Module 7 | `suricata_ingestion.py` | IDS log parsing, EVE JSON alert generation |
| Module 8 | `ai_service.py` | Qwen2.5-3B SLM, XAI narrative generation |
| Module 5 | `analytics_read_model.py` | PostGIS analytics read model, heatmap points, trends |

### Frontend Pages (`src/frontend/src/app/`)

| FRS Module | Page | Purpose |
|---|---|---|
| Module 1 | `login/` | Keycloak authentication, MFA enrollment |
| Module 2 | `report/`, `incidents/` | Offline-capable PWA incident submission |
| Module 5 | `dashboard/` | National overview, heatmap, analytics views |
| Module 9 | `admin/` | System health monitoring dashboard |
| Module 12 | `profile/` | Self-service profile management |
| Module 5d | `report/` | Anonymous public submission (same UI, no login) |

---

## 3.X.5 Chapter 1 → Chapter 3 → Chapter 4 Traceability Flow

```
Chapter 1 Objectives
    │
    ├── General Objective ─────────────────────────────────────────────────► Chapter 5 Conclusions
    │
    └── Specific Objectives
            │
            ├── Obj 1 (PWA Offline) ─────► Module 2 PWA Architecture ──────────────► Ch4 Offline-First Evaluation
            ├── Obj 2 (RBAC/Keycloak) ───► Module 1 Auth & Access Control ─────────► Ch4 Auth Security Results
            ├── Obj 3 (Crypto/TLS) ──────► Module 6 Cryptographic Pipeline ─────────► Ch4 Data Protection Results
            ├── Obj 4 (Suricata+XAI) ─────► Modules 7 & 8 Threat Detection + XAI ───► Ch4 Threat Detection Results
            ├── Obj 5 (Public Ingestion) ─► Module 5d + Module 3 Triage ───────────► Ch4 Civilian Reporting Results
            ├── Obj 6 (National Analytics)► Module 5 + Module 15 Reference Data ─────► Ch4 Analytics Evaluation Results
            ├── Obj 7 (RA 10173/RLS) ─────► Module 10 Compliance & Data Privacy ────► Ch4 Privacy Compliance Results
            ├── Obj 8 (OWASP ASVS L2) ────► Module 11 Security Testing ────────────► Ch4 Security Testing Results
            └── Obj 9 (ISO 25010) ────────► Modules 2, 8, 9 Quality Evaluation ─────► Ch4 Quality Evaluation Results
```

---

## 3.X.6 Sample Chapter 3 Narrative Text

> The Research Question Alignment Matrix was prepared to operationalize the Specific Objectives of the study. Each row in the matrix maps one specific objective from Chapter 1 to an FRS module, an ISO/IEC 25010 quality characteristic, a STRIDE threat category, a security test metric aligned with OWASP ASVS and NIST SP 800-115, and the corresponding expected evidence label in Chapter 4. This ensures that every testing activity reported in Chapter 4 is traceable to an approved objective and a defined security requirement, satisfying the consistency requirement for cybersecurity capstone evaluations.
>
> The nine specific objectives of WIMS-BFP were mapped across fifteen FRS modules spanning authentication, offline-first incident management, conflict detection, immutable data storage, analytics, cryptographic security, intrusion detection, threat detection with XAI, system monitoring, and data privacy compliance. The STRIDE threat model was applied across all six categories: Keycloak MFA and account lockout address Spoofing; SQLAlchemy ORM and PostgreSQL RLS policies address Tampering; immutable audit logs address Repudiation; AES-256-GCM encryption and TLS 1.3 address Information Disclosure; offline-first PWA architecture and Redis/Celery task queues address Denial of Service; and Keycloak RBAC with least-privilege role scoping addresses Elevation of Privilege. The alignment matrix confirms complete coverage: every specific objective has at least one FRS module and at least one security test, every STRIDE category has at least one mitigant with a defined FRS module reference, and every test has a designated evidence artifact in Chapter 4.

---

## 3.X.7 Alignment Verification Checklist

For panel defense readiness, each of the following questions must be answerable with reference to this matrix:

- [ ] "Which FRS module covers your offline PWA?" → Obj 1 / Module 2 / `api/incidents`, `pages/report`
- [ ] "How does this objective relate to your testing?" → See column "Security Test / Metric"
- [ ] "Why did you choose these security tests?" → See column "STRIDE Threat" + Evaluation Standards Reference
- [ ] "Where did your metrics come from?" → See column "Functionality Evaluation" (ISO/IEC 25010)
- [ ] "How is STRIDE reflected in your system?" → See STRIDE Threat Category Summary table
- [ ] "Which module handles your public anonymous reporting?" → Obj 5 / Module 5d / `api/public_dmz.py` (3 req/IP/hr, no auth)
- [ ] "How does the AI module satisfy Explainability under ISO 25010?" → Obj 4 / Module 8 / `services/ai_service.py`
- [ ] "How is RA 10173 mechanically enforced, not just documented?" → Obj 7 / Module 10 / RLS on `wims.*` tables; `FORCE ROW LEVEL SECURITY`
- [ ] "Why does Module 5d have no authentication?" → Anonymous reporting eliminates UX friction in emergency situations; abuse controlled by Redis IP rate limiting only
- [ ] "What is Module 15 and why does it exist?" → Module 15 / `api/ref.py` — shared geographic reference data service for regions, provinces, cities used across Modules 2, 5, 5d

---

## 3.X.8 FRS Module Coverage per Objective

| Objective | Primary FRS Module(s) | Supporting FRS Module(s) |
|-----------|----------------------|------------------------|
| Obj 1: PWA Offline | Module 2 | Module 4 (sync commit), Module 6 (local encryption) |
| Obj 2: RBAC/Keycloak | Module 1 | Module 12 (user admin) |
| Obj 3: Crypto/TLS | Module 6 | Module 10 (RA 10173 data protection) |
| Obj 4: Suricata + XAI | Modules 7, 8 | Module 9 (health monitoring) |
| Obj 5: Public Portal | Module 5d | Module 3 (triage workflow) |
| Obj 6: National Analytics | Module 5 | Module 15 (reference data) |
| Obj 7: RA 10173/RLS | Module 10 | Module 4 (audit logging) |
| Obj 8: OWASP ASVS L2 | Module 11 | All modules |
| Obj 9: ISO 25010 | Modules 2, 8, 9 | Module 5 (analytics evaluation) |
