---
id: wims-bfp-ch1-introduction-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-07-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - raw/misc/01-intro.md
  - raw/misc/01-01-purpose-description.md
  - raw/misc/01-02-project-context.md
  - raw/misc/01-03-objectives-study.md
  - raw/misc/01-04-scope-limitations.md
  - raw/misc/01-05-significance-study.md
  - raw/misc/01-06-conceptual-framework.md
  - raw/misc/01-07-cybersecurity-principles.md
  - raw/misc/01-08-definition-terms.md
status: active
tags:
  - wims-bfp
  - thesis
  - chapter-1
  - introduction
  - bfp
  - fire-protection
related:
  - concepts/zero-trust-architecture
  - concepts/keycloak-fastapi-security-wims-bfp
  - concepts/postgis-security-wims-bfp
---

# WIMS-BFP Chapter 1: Introduction

**Source:** raw/misc/ (9 files, ~42 KB)
**Chapter:** 1 — Introduction
**Thesis:** "WIMS-BFP: A Secure Web Incident Monitoring System with AI-Assisted Threat Detection for Cybersecurity-Specific Forensics-Driven Analysis in the Bureau of Fire Protection"

---

## 1.1 Purpose and Description

WIMS-BFP is a cloud-based participatory mapping and triage platform with AI-Assisted Threat Detection for the Bureau of Fire Protection (BFP). The system serves the Fire Suppression Operation Division (FSOD) and system administrators.

**Core purpose:** Equip BFP personnel with tools to proactively defend public-facing infrastructure while consolidating public incident reports and regional dispatches in real-time.

**Architecture transition:** From localized architecture to Virtual Private Server (VPS) deployment, bridging communication between community, regional BFP offices, and National Headquarters.

**Key innovation:** Integration of geospatial analytics with a validation workflow. Community reports are visualized through interactive heatmaps. Regional Validators use a triage dashboard to cross-reference unverified public reports with official BFP ground dispatches.

**AI component:** Qwen2.5-3B as an Explainable AI (XAI) layer — strictly assistive, not autonomous. Converts Suricata IDS logs into human-readable forensic narratives for BFP personnel regardless of cybersecurity training depth.

---

## 1.2 Project Context

**Organization:** Bureau of Fire Protection (BFP), Fire Suppression Operation Division (FSOD)

**Operational mandate:** Comprehensive monitoring of fire events and rescue missions nationwide.

**Transition:** From internal-only systems to cloud-based VPS with crowdsourced intelligence from community reporters.

**CIA Triad threats identified:**

| Principle | Threat | Description |
|---|---|---|
| Confidentiality | Broken cloud access controls, stolen credentials | Threat actors bypass authentication, expose citizen PII or operational intelligence |
| Integrity | Malicious payloads, False Data Injection Attacks | Community portal spammed with structurally valid but fake incident reports to distort operational view |
| Availability | DDoS attacks on public VPS | Crash public application, halt community reporting, sever triage communication during active disasters |

**Root cause analysis (Ishikawa diagram) — 6 categories:**
- **Machine:** Monolithic setups lacking offline resilience; flat internal networks without container isolation
- **Security:** Alert fatigue from unstructured security telemetry; standard systems fail to filter efficiently
- **Method:** Manual validation workflows and reactive monitoring
- **Material:** Fragmented intelligence lacking automated spatial context (geospatial heatmaps)
- **Man:** System administrators face cognitive overload; operational staff lack forensic training
- **Compliance:** Compromised chain of custody; difficulty meeting RA 10173 mandates

**STRIDE Threat Model applied:**

| Threat | Mitigation |
|---|---|
| Spoofing | Keycloak Identity Provisioning, MFA, token-based session validation |
| Tampering | Payload validation, PostGIS DB isolation in Docker bridge network, append-only audit logging |
| Repudiation | Immutable PostgreSQL audit logs, Suricata IDS + Qwen2.5-3B XAI for forensic narratives |
| Information Disclosure | Container isolation, Keycloak RBAC, AES-256-GCM encryption |
| Denial of Service | Rate limiting, decentralized PWA caches for offline resilience |
| Elevation of Privilege | Container isolation, Keycloak RBAC preventing lateral movement |

**Existing system analyzed:** BFP-AIMS (Advanced Incident Management System)
- Successfully deployed nationally but has flat architecture increasing cognitive load
- Heavy reliance on manual data entry (typographical errors, reporting delays)
- Serves as centralized digital ledger but lacks geospatial mapping and predictive analytics

---

## 1.3 Objectives of the Study

### General Objective

Develop WIMS-BFP: a secure, dual-edge incident monitoring system combining offline-first PWA, public-facing portal for crowdsourced citizen reporting, and Forensics-Driven AI module ensuring proactive threat interpretability and RA 10173 compliance.

### Specific Objectives (9)

| # | Objective | Key Technologies |
|---|---|---|
| 1 | Design offline-first PWA for data capture | FastAPI backend, Service Workers, local caching |
| 2 | Implement RBAC via Keycloak | JWT, MFA, least privilege |
| 3 | Establish cryptographic pipeline | AES-256-GCM, TLS 1.3 |
| 4 | Integrate Suricata IDS + Qwen2.5-3B XAI | Deterministic anomaly detection, human-readable forensic narratives |
| 5 | Secure ingestion framework | Public portal + email verification + rate limiting + geographically-bound triage |
| 6 | National Analytics module | PostGIS geospatial clustering, heatmaps, comparative analysis, variance tracking |
| 7 | Align with RA 10173 + ISO/IEC 27001 | PostgreSQL RLS, DPIA, ROPA |
| 8 | OWASP ASVS Level 2 compliance | STRIDE threat model validation across Identity, Crypto, Forensics, Infra |
| 9 | ISO/IEC 25010 evaluation | Usability, Reliability, Functional Suitability, Performance Efficiency |

---

## 1.4 Scope and Limitations

### Modules in Scope (12)

| Module | Description |
|---|---|
| PWA Frontend + User Management | Role-based dashboards, incident forms, spatial mapping, offline access (internal BFP only) |
| RBAC + Identity Module | Role separation via Keycloak |
| Authentication + MFA | Identity verification for sensitive operations |
| Regional Access + Authorization | Geographically-bound data entry and sync for regional BFP personnel |
| Incident Capture + Workflow | Validation rules, attachments, revision handling, status transitions, triage |
| National Export + Data Import | Structured intake of regional submissions, controlled export |
| Data Security + Encryption | AES-256-GCM at rest, TLS 1.3 in transit |
| Threat Detection + Interpretability | Suricata IDS + Qwen2.5-3B XAI narratives |
| Monitoring, Metrics, Logging | Immutable auditability, compliance tracing |
| National Analytics | Filtering, comparative analysis, variance tracking, heatmaps, downloadable outputs |
| Penetration Testing + QA | OWASP ASVS Level 2, ISO/IEC 25010 evaluation |
| Civilian Reporting + Notification | Public VPS portal, email-verified accounts, rate limiting, 5MB upload limit |

### Intended Users (5 FRS Roles)

1. **CIVILIAN_REPORTER** — Public community members submitting fire incident reports
2. **REGIONAL_ENCODER** — Regional BFP personnel for data entry (Create + Read only)
3. **NATIONAL_VALIDATOR** — National HQ personnel verifying accuracy, marking records as "Verified"
4. **NATIONAL_ANALYST** — Interprets statistical dashboards and AI threat reports
5. **SYSTEM_ADMIN** — Full system administration and security oversight

### Limitations

- No live deployment to actual public during evaluation (simulated traffic + synthetic datasets only)
- XAI module strictly assistive — no autonomous mitigation or network-blocking
- No long-term production maintenance or APT defense
- Security evaluation bounded to OWASP Top 10, automated botnets, opportunistic app-layer attacks
- No live citizen data used during testing (RA 10173 compliance)

---

## 1.5 Significance of the Study

| Stakeholder | Value |
|---|---|
| FSOD | Resilient command-and-control functioning irrespective of internet availability; offline reporting via PWA Service Workers |
| Institutional Data Stewardship | PostgreSQL RLS as technical control for Data Minimization (RA 10173); regional encoders bound to geographic jurisdiction |
| Cybersecurity Operations | AES-256-GCM + append-only audit logs = digital chain of custody; XAI translates Suricata logs to reduce alert fatigue |
| Sovereign Trust | Qwen2.5-3B hosted locally — eliminates reliance on external AI APIs; BFP retains absolute data stewardship |
| Academic Domain | Validates Secure-by-Design methodology in resource-constrained environments; demonstrates local SLM feasibility for security interpretability |
| Strategic Policy | PostGIS geospatial analytics + crowdsourcing portal → real-time spatial intelligence for BFP National Directorate |

---

## 1.6 Conceptual Framework (IPO Model)

**Model:** Input-Process-Output (IPO) with Human-in-the-Loop (HITL) Security Feedback Loop

```
INPUT → Zero-Trust Enforcement → PROCESS → OUTPUT → HITL Resilience Loop
```

### Input Layer (2 pathways)
1. **Public portal:** Real-time crowdsourced reports (requires internet)
2. **Internal BFP:** Offline-First Cache (IndexedDB/Dexie.js) buffers inputs locally; auto-syncs on reconnection

### Enforcement Point
- Nginx reverse proxy + Keycloak + FastAPI middleware
- Public traffic: TLS 1.3 + rate limiting
- Internal syncs: Keycloak JWTs + AES-256-GCM

### Processing Layer
- PostGIS spatial processing for triage workflow
- Suricata IDS continuous network monitoring
- Qwen2.5-3B consumes flagged anomalies → generates XAI narratives

### Output Layer
- Interactive geospatial heatmaps (risk assessment)
- Verified official incident records
- XAI threat narratives (human-readable)

### HITL Resilience Loop
- System Administrators manually review XAI narratives
- Validated insights → manually refine Keycloak policies + Suricata detection rules
- Continuous human-driven feedback ensures dynamic threat adaptation

---

## 1.7 Cybersecurity Principles

### CIA Triad + Extensions

| Principle | Technical Control | Legal Alignment |
|---|---|---|
| **Confidentiality** | AES-256-GCM (authenticated encryption) | RA 10173 Section 20 |
| **Integrity** | Authentication tags (mathematical proof of tampering) | RA 10173 accurate data processing |
| **Availability** | PWA offline-first + VPS rate limiting + decentralized caches | BFP disaster response mandate |
| **Accountability** | Immutable PostgreSQL audit logs | Forensic chain of custody |
| **Non-repudiation** | Append-only logging + XAI interpretability | Legal verifiability |

### Framework (3 layers)

1. **Strategic Core:** National Fire Incident Monitoring (centralized, trustworthy, crowdsourced)
2. **Primary Defense:** CIA Triad — Confidentiality (encryption), Integrity (SHA-256 hashing), Availability (dual-pronged PWA + VPS)
3. **Institutional Shield:** Accountability & Non-repudiation (immutable logging + XAI) + Secure-by-Design (strict access controls from earliest stages)

Situates within Government Regulatory Environment (RA 10173, STRIDE threat model).

---

## 1.8 Key Definitions

| Term | Definition |
|---|---|
| AES-256-GCM | Symmetric-key block cipher providing authenticated encryption (NIST SP 800-38D) |
| Audit Log | Chronological record of system activities (NIST SP 800-53) |
| Chain of Custody | Process tracking evidence movement from collection through analysis (NIST SP 800-72) |
| DPIA | Documented risk assessment for processing sensitive data |
| XAI | Suite of ML techniques producing explainable models (DARPA) |
| Geospatial Data | Information identifying geographic location and characteristics (ISO 19111) |
| ISO/IEC 27001 | Information Security Management System framework |
| MFA | Authentication requiring 2+ pieces of evidence (NIST SP 800-63) |
| Offline-First Design | App designed to function without internet by default (Google Developers) |
| PWA | Web application using HTML/CSS/JS, standards-compliant browser (MDN) |
| RBAC | Access control around roles and privileges (NIST SP 800-162) |
| ROPA | Record of Processing Activities (RA 10173 IRR) |
| Service Workers | Background scripts enabling offline-first capabilities (MDN) |
| ZTA | Cybersecurity plan using zero trust concepts (NIST SP 800-207) |

### Operational Terms (WIMS-BFP specific)

| Term | Definition |
|---|---|
| Anomaly Detection | Deterministic identification via Suricata IDS rules; Qwen2.5-3B interprets but does NOT classify |
| Append-Only Logging | PostgreSQL mechanism for non-repudiation; audit logs remain immutable |
| Crowdsourced Reporting | Public fire incident data via VPS portal |
| Dual-Tier Triage | Unverified "pins" cross-referenced with official BFP dispatches before "Verified" status |
| Geospatial Heatmap | Interactive color-coded density visualization of fire incidents |
| HITL | System Administrator manually reviews XAI narratives; refines Keycloak/Suricata policies |
| Regional Encoder | BFP personnel — Create + Read permissions only |
| National Validator | BFP HQ personnel — unique privilege to mark records "Verified" |
| Regional Data Bundle | Cryptographically secured, compressed offline records for manual import |
| Tamper-Evident Record | Incident record with hash; mismatch → "Compromised" flag |
| Threat Interpretability | Qwen2.5-3B converts raw Suricata logs to human-readable narratives (explains "why" and "how") |

---

## Cross-References

- [[concepts/zero-trust-architecture]] — ZTA framework referenced throughout
- [[concepts/keycloak-fastapi-security-wims-bfp]] — Auth implementation
- [[concepts/postgis-security-wims-bfp]] — Spatial security
- [[concepts/postgresql-security-wims-bfp]] — RLS and audit logging
