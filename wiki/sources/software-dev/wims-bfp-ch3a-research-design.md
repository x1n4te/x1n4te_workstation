---
id: wims-bfp-ch3a-research-design-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-07-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - raw/misc/03-01-research-design.md
  - raw/misc/03-02-01-functional-requirements.md
  - raw/misc/03-02-02-nonfunctional-requirements.md
  - raw/misc/03-02-03-security-requirements.md
  - raw/misc/03-02-04-feasibility-study.md
  - raw/misc/03-02-requirements-analysis.md
  - raw/misc/03-03-project-dev-model.md
  - raw/misc/03-methodology.md
status: active
tags:
  - wims-bfp
  - thesis
  - chapter-3
  - research-design
  - requirements
related:
  - sources/software-dev/wims-bfp-ch1-introduction
  - sources/software-dev/wims-bfp-ch2-rrl
---

# WIMS-BFP Chapter 3a: Research Design + Requirements

**Source:** raw/misc/ (8 files)
**Chapter:** 3a — Research Design, Requirements Analysis, Development Model

---

## Research Design

**Type:** Hybrid — Developmental Research + Experimental Security Research

### Developmental Research
Systematic design, development, and evaluation of the WIMS-BFP artifact:
- Cloud-based public reporting portal
- PostGIS geospatial heatmap rendering
- PWA offline-first capabilities for internal BFP

### Experimental Security Research
Controlled adversarial simulations against STRIDE threats:
- Validates Suricata IDS detection mechanisms
- Tests defenses against False Data Injection and volumetric attacks
- Empirically verifies defensive capabilities against cloud-specific threats

### Testing Environments (2 sequential)

| Environment | Purpose | Method |
|---|---|---|
| Sovereign LAN Simulation | Offline-first testing | Artificially sever client internet; test IndexedDB persistence + SSR |
| Cloud Edge Simulation | Public portal testing | Phase A: Locust load testing; Phase B: OWASP ASVS L2 pen testing |

### Evaluation (bifurcated)

| Evaluation | Standards | Metrics |
|---|---|---|
| System Quality | ISO/IEC 25010 | Functional Suitability, Performance Efficiency, Reliability, Usability (MOS) |
| Security | F1-Score + OWASP ASVS | Detection accuracy, compliance pass rates |

---

## Functional Requirements (6 areas)

| Area | Requirement | Supported Objective |
|---|---|---|
| Crowdsourced Reporting | Public VPS portal for civilian incident submission; internal users encode/update/track | Cloud-based participatory mapping |
| Geospatial Mapping | PostGIS interactive heatmaps; centralized validation workflow | Spatial dashboard for visualization |
| Data Synchronization | Auto-detect network restoration; sync offline bundles without data loss | PWA offline-first continuity |
| Access Control | Strict RBAC via Keycloak across 5 roles | Least privilege enforcement |
| Threat Detection | Suricata IDS alerts consumed by Qwen2.5-3B XAI | Human-readable forensic narratives |
| Forensic Reporting | Immutable timestamped audit logs; chain of custody | ISO 27001 + RA 10173 compliance |

---

## Non-Functional Requirements

| Quality Attribute | Requirement | Evaluation Criteria |
|---|---|---|
| Performance Efficiency | Mean inference latency <5s for XAI narratives | Inference latency profiling |
| Performance Efficiency (Cloud) | Sustain concurrent loads + rapid heatmap rendering | Locust load testing |
| Reliability | PWA caches 100% offline data; 100% sync accuracy | Synchronization Success Rate (SSR) |
| Usability | XAI narratives intelligible to non-technical personnel | Mean Opinion Score (MOS) >= 4.0/5.0 |
| Portability | PWA works across standard browsers, no special install | Cross-browser compatibility |
| Security (Integrity) | AES-256-GCM + digital envelopes; tamper-evident | Hash validation checks |

---

## Security Requirements (5 domains)

| Domain | Requirement | Mitigated Risk |
|---|---|---|
| Authentication + Identity | MFA + token-based sessions | Spoofing (Zero Trust) |
| Data Confidentiality | AES-256-GCM at rest + TLS 1.3 in transit | Information Disclosure (RA 10173) |
| Data Integrity | SHA-256 hashing + digital signatures | Tampering (falsified reports) |
| Forensic Accountability | Append-only audit logs + XAI narratives | Repudiation (ISO 27001) |
| Anomaly Detection | Suricata IDS + XAI narratives for behavioral deviations | Elevation of Privilege |

---

## Project Development Model

**Model:** Hybrid Incremental V-Model (Agile-Scrum overlay on Systems V-Model)

### Left Arm (Regulatory Engineering)
1. Requirements & Threat Analysis — RA 10173 compliance, civilian PII protection
2. System Architecture Design — VPS + Sovereign LAN bridge, Nginx/Keycloak boundaries
3. Subsystem & Module Design — AES-256-GCM logic, PostGIS queries, Redis/Celery queues

### Base (Iterative Agile Sprints)
- Next.js/React frontend + FastAPI backend in timeboxed iterations
- Rapid iteration on Dexie.js offline cache, heatmaps, XAI narratives

### Right Arm (Verification Gates)
| Testing Phase | Validates |
|---|---|
| Cryptographic & Unit Testing | Module Design (key management, memory leaks) |
| System Integration Testing | Architecture Design (VPS→FastAPI handoff, Redis→AI routing) |
| User Acceptance Testing | Requirements (offline sync, RBAC, triage workflow) |
