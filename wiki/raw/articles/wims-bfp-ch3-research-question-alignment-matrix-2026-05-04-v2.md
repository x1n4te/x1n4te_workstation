# WIMS-BFP — Research Question Alignment Matrix v2
# WIMS-BFP — Ch3 Research Question Alignment Matrix

> **Status:** Thesis-ready artifact — WIMS-BFP-specific, built from actual implemented modules
> **Chapter:** 3 — Methodology
> **Section:** Requirements Analysis → Security Requirements
> **Based on:** `wims-bfp-research-question-alignment-matrix-2026-05-04` (source #2)
> **Ground truth source:** `~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/src/backend/api/routes/` + `src/frontend/src/app/`
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

### Research Objective Alignment Matrix

| #   | Specific Objective                                                                                                                                                                                                                                                                                                           | Functional Output / Module                                                                       | Functionality Evaluation                                               | STRIDE Threat                                              | Security Test / Metric                                                                                                             | Expected Chapter 4 Evidence                           |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| 1   | Design and develop a PWA enabling offline data capture utilizing FastAPI backend and IndexedDB for local caching and synchronization                                                                                                                                                                                         | `pages/report`, `pages/incidents` (frontend PWA); `api/incidents` (backend)                      | Functional Suitability                                                 | **Tampering**                                              | Offline data integrity on sync; duplicate incident detection; successful sync completion rate                                      | Offline-First PWA Evaluation Results                  |
| 2   | Implement Role-Based Access Control (RBAC) governed by Keycloak, enforcing the principle of least privilege within the PWA                                                                                                                                                                                                   | `pages/login`; `api/admin`; `api/sessions`; `services/keycloak_admin.py`                         | Functional Suitability, Usability                                      | **Spoofing**                                               | Authentication lockout after 5 failed attempts; role access restriction enforcement; JWT token expiry behavior; session revocation | Authentication & Authorization Security Results       |
| 3   | Establish a robust cryptographic pipeline utilizing AES-256-GCM and TLS 1.3 protocols to ensure strict data protection at rest and in transit, protecting sensitive BFP repositories from information disclosure                                                                                                             | `services/ai_service.py`; `database.py`; TLS termination at reverse proxy                        | Reliability, Information Disclosure                                    | **Information Disclosure**                                 | HTTPS enforcement verification; unauthorized access block rate; encrypted field access tests                                       | Data Protection & Cryptographic Results               |
| 4   | Integrate a Suricata IDS for deterministic network anomaly detection alongside the Qwen2.5-3B SLM as an Explainable AI (XAI) engine to translate complex security alerts into human-readable forensic narratives                                                                                                             | `services/suricata_ingestion.py`; `services/ai_service.py`                                       | Functional Suitability, Explainability                                 | **Repudiation + Information Disclosure**                   | Suricata rule coverage; alert-to-narrative translation accuracy; AI response time under load                                       | Threat Detection & XAI Explainability Results         |
| 5   | Establish a secure ingestion framework providing a public-facing civilian reporting portal—protected by email-based account verification and per-account rate limiting—paired with a triage workflow and geographically-bound controls ensuring operational integrity of verified incident data                              | `api/civilian`; `api/triage`; `services/analytics_read_model.py`                                 | Functional Correctness, Task Appropriateness                           | **Tampering**, **Elevation of Privilege**                  | Rate limit enforcement (requests per account); unauthorized record modification detection; geographic boundary enforcement         | Civilian Reporting Security & Triage Results          |
| 6   | Establish a National Analytics module utilizing PostGIS performing geospatial clustering and visualization via heatmaps, alongside dynamic comparative analysis and variance tracking across multiple categories within user-defined date ranges to support executive policy and resource optimization                       | `api/analytics`; `services/analytics_read_model.py`                                              | Functional Suitability, Performance Efficiency                         | **N/A**                                                    | Analytics query response time; geospatial clustering correctness; heatmap rendering completeness                                   | National Analytics Module Evaluation Results          |
| 7   | Align system architecture with the Data Privacy Act of 2012 (RA 10173) and ISO/IEC 27001 by mechanically enforcing data minimization through PostgreSQL Row-Level Security (RLS) policies, supported by the administrative production of a Data Privacy Impact Assessment (DPIA) and Records of Processing Activities (ROPA) | `database.py`; `auth.py`; RLS policies on `wims.users`, `wims.incidents`, `wims.citizen_reports` | Functional Suitability, Reliability                                    | **Tampering**, **Repudiation**, **Information Disclosure** | Unauthorized cross-region data access attempts blocked by RLS; audit log completeness; RLS policy enforcement verification         | Data Privacy & Compliance Results                     |
| 8   | Execute rigorous security testing achieving OWASP ASVS Level 2 compliance, validating the system's defense against the STRIDE threat model across Identity, Cryptography, Forensic Logging, Threat Detection, and Infrastructure Resilience                                                                                  | All modules                                                                                      | All applicable                                                         | **All STRIDE categories**                                  | ASVS Level 2 checklist compliance rate; per-category pass/fail tally; penetration test outcomes                                    | Security Testing and Vulnerability Assessment Results |
| 9   | Evaluate WIMS-BFP according to ISO/IEC 25010 standards, specifically assessing the Usability and Reliability of the offline-first web application, as well as the Functional Suitability and Performance Efficiency of the local AI module                                                                                   | `pages/report`, `pages/dashboard`; `services/ai_service.py`                                      | Usability, Reliability, Functional Suitability, Performance Efficiency | **N/A**                                                    | ISO 25010 survey weighted mean per category; AI inference latency; system error rate under normal operation                        | System Quality Evaluation Results                     |

---

### STRIDE Threat Category Summary

| STRIDE Category            | Threat Description                                           | Mitigated By                                                                                                                  | WIMS-BFP Implementation Reference                              |
| -------------------------- | ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| **Spoofing**               | Impersonating an authorized user to gain unauthorized access | MFA enforcement via Keycloak; JWT HttpOnly cookies with short-lived access tokens; account lockout after 5 failed attempts    | `services/keycloak_admin.py`; `api/sessions`; `auth.py`        |
| **Tampering**              | Modifying data or records without authorization              | SQLAlchemy ORM (parameterized queries); PostgreSQL RLS policies; audit trail via `utils/audit.py`                             | `api/incidents`; `api/triage`; RLS policies on `wims.*` tables |
| **Repudiation**            | User denies having performed an action                       | Immutable audit logs (`log_system_audit()`); tamper-detection on log records                                                  | `utils/audit.py`; `api/admin.py`                               |
| **Information Disclosure** | Exposing sensitive data to unauthorized parties              | AES-256-GCM field encryption; HTTPS/TLS 1.3 enforcement; RLS column-level restrictions; HttpOnly/Secure/SameSite cookie flags | `services/ai_service.py`; `database.py`; reverse proxy config  |
| **Denial of Service**      | Making the system unavailable to authorized users            | Redis/Celery background tasks; offline PWA with Service Worker + IndexedDB; graceful degradation under load                   | `tasks/`; `pages/report` (offline-capable PWA)                 |
| **Elevation of Privilege** | Gaining capabilities beyond authorized scope                 | Keycloak RBAC with principle of least privilege; role-scoped API routes; RLS enforcement at database layer                    | `auth.py`; `api/admin`; `api/analytics` role guards            |

---

### Implemented Module Inventory (Ground Truth)

**Frontend (Next.js PWA — `src/frontend/src/app/`):**

| Module | Path | Purpose |
|--------|------|---------|
| Login | `login/` | Keycloak authentication, MFA enrollment |
| Report | `report/` | Civilian incident submission (offline-capable) |
| Incidents | `incidents/` | Incident management and browsing |
| Dashboard | `dashboard/` | National overview, heatmap, alerts |
| Admin | `admin/` | User management, session oversight |
| Afor | `afor/` | Area of Responsibility (AOR) boundary management |
| Profile | `profile/` | Self-service profile management |

**Backend API Routes (`src/backend/api/routes/`):**

| Module | File | Purpose |
|--------|------|---------|
| Incidents | `incidents.py` | Incident CRUD, bundle upload, attachment storage |
| User Profile | `user.py` | Self-service profile, password change |
| Civilian Reports | `civilian.py` | Public report submission (zero-trust, no auth) |
| Triage | `triage.py` | ENCODER/VALIDATOR promotion workflow |
| Analytics | `analytics.py` | National Analyst read-only queries (PostGIS) |
| Admin | `admin.py` | Keycloak user lifecycle, audit telemetry |
| Sessions | `sessions.py` | Active session listing and revocation |
| Regional | `regional.py` | Regional-scoped incident operations |

**Backend Services (`src/backend/services/`):**

| Service | File | Purpose |
|---------|------|---------|
| AI Service | `ai_service.py` | Qwen2.5-3B SLM integration, XAI narrative generation |
| Suricata Ingestion | `suricata_ingestion.py` | IDS log parsing and threat categorization |
| Analytics Read Model | `analytics_read_model.py` | PostGIS-backed analytics facts, heatmap points, trends |
| Keycloak Admin | `keycloak_admin.py` | Keycloak user CRUD, session management, MFA |

---

### Chapter 1 → Chapter 3 → Chapter 4 Traceability Flow

```
Chapter 1 Objectives
    │
    ├── General Objective ─────────────────────────────────────────────────► Chapter 5 Conclusions
    │
    └── Specific Objectives
            │
            ├── Obj 1 (PWA Offline) ─────► Ch3 PWA Architecture ─────────────────► Ch4 Offline-First Evaluation
            ├── Obj 2 (RBAC/Keycloak) ───► Ch3 Security Requirements ───────────► Ch4 Auth Security Results
            ├── Obj 3 (Crypto/TLS) ──────► Ch3 Cryptographic Pipeline ────────────► Ch4 Data Protection Results
            ├── Obj 4 (Suricata+XAI) ─────► Ch3 Threat Detection + XAI ───────────► Ch4 Threat Detection Results
            ├── Obj 5 (Civilian Portal) ──► Ch3 Secure Ingestion Framework ───────► Ch4 Civilian Reporting Results
            ├── Obj 6 (National Analytics)► Ch3 Analytics Module ─────────────────► Ch4 Analytics Evaluation Results
            ├── Obj 7 (RA 10173/RLS) ─────► Ch3 Data Privacy Compliance ───────────► Ch4 Privacy Compliance Results
            ├── Obj 8 (OWASP ASVS L2) ────► Ch3 Security Testing (NIST 800-115) ─► Ch4 Security Testing Results
            └── Obj 9 (ISO 25010) ────────► Ch3 System Quality Evaluation ─────────► Ch4 Quality Evaluation Results
```

---

### Sample Chapter 3 Narrative Text

> The Research Question Alignment Matrix was prepared to operationalize the Specific Objectives of the study. Each row in the matrix maps one specific objective from Chapter 1 to a functional module, an ISO/IEC 25010 quality characteristic, a STRIDE threat category, a security test metric aligned with OWASP ASVS and NIST SP 800-115, and the corresponding expected evidence label in Chapter 4. This ensures that every testing activity reported in Chapter 4 is traceable to an approved objective and a defined security requirement, satisfying the consistency requirement for cybersecurity capstone evaluations.
>
> The nine specific objectives of WIMS-BFP were mapped to fourteen distinct backend API route modules and seven frontend page modules, covering the full spectrum from unauthenticated civilian reporting to privileged administrative oversight. The STRIDE threat model was applied across all six categories, with cryptographic controls (AES-256-GCM, TLS 1.3) addressing Information Disclosure, Keycloak MFA and RBAC addressing Spoofing and Elevation of Privilege, PostgreSQL RLS policies addressing Tampering and Repudiation, and offline-first PWA architecture addressing Denial of Service. The alignment matrix confirms complete coverage: every specific objective has at least one security test, every STRIDE category has at least one mitigant, and every test has a defined evidence artifact for Chapter 4.

---

### Alignment Verification Checklist

For panel defense readiness, each of the following questions must be answerable with reference to this matrix:

- [ ] "How does this objective relate to your testing?" → See column "Security Test / Metric"
- [ ] "Why did you choose these security tests?" → See column "STRIDE Threat" + Evaluation Standards Reference
- [ ] "Where did your metrics come from?" → See column "Functionality Evaluation" (ISO/IEC 25010)
- [ ] "How is STRIDE reflected in your system?" → See STRIDE Threat Category Summary table
- [ ] "Which specific objective does your civilian portal map to?" → Objective 5 / `api/civilian.py`
- [ ] "How does the AI module satisfy Explainability under ISO 25010?" → Objective 4 + Objective 9 / `services/ai_service.py`
- [ ] "How is RA 10173 mechanically enforced, not just documented?" → Objective 7 / RLS policies on `wims.*` tables

---

### WIMS-BFP Implementation Reference (per Objective)

| Objective | Codebase Module(s) | Key Security Control |
|-----------|-------------------|---------------------|
| Obj 1: PWA Offline | `pages/report`, `pages/incidents`, `api/incidents` | IndexedDB sync; offline mutation queue |
| Obj 2: RBAC / Keycloak | `pages/login`, `api/admin`, `api/sessions`, `services/keycloak_admin.py` | Keycloak MFA; JWT HttpOnly; role-gated routes |
| Obj 3: Crypto Pipeline | `services/ai_service.py`, `database.py`, reverse proxy | AES-256-GCM; TLS 1.3; HttpOnly/Secure/SameSite |
| Obj 4: Suricata + XAI | `services/suricata_ingestion.py`, `services/ai_service.py` | Suricata rules; Qwen2.5-3B narrative generation |
| Obj 5: Civilian Portal | `api/civilian`, `api/triage` | Zero-trust public endpoint; rate limiting; geographic bounds |
| Obj 6: National Analytics | `api/analytics`, `services/analytics_read_model.py` | PostGIS queries; geospatial clustering; heatmap |
| Obj 7: RA 10173 / RLS | `database.py`, `auth.py`, RLS policies | FORCE ROW LEVEL SECURITY; `SECURITY DEFINER` helpers |
| Obj 8: OWASP ASVS L2 | All modules | ASVS checklist; NIST SP 800-115 test procedures |
| Obj 9: ISO 25010 | `pages/report`, `pages/dashboard`, `services/ai_service.py` | Post-test evaluation questionnaire; AI latency benchmarks |
