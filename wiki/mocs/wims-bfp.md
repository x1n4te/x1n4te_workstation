---
id: wims-bfp-moc-001
type: MOC
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-07-08
stale_after: 2026-10-08
confidence: high
status: active
tags:
  - moc
  - wims-bfp
  - thesis
related:
  - sources/software-dev/wims-bfp-abstract
  - sources/software-dev/wims-bfp-ch1-introduction
  - overview-state-of-field
---

# WIMS-BFP — Map of Content

**Project:** Secure Web Incident Monitoring System for Bureau of Fire Protection
**Status:** Active thesis year

---

## Reading Path

### Start Here
[[sources/software-dev/wims-bfp-abstract]] — what WIMS-BFP is and why it matters

### The Problem
[[sources/software-dev/wims-bfp-ch1-introduction]] — purpose, context, CIA threats, STRIDE model, scope

### What Exists Already
[[sources/software-dev/wims-bfp-ch2-rrl]] — related literature, what's been done, what's missing

### How We're Building It
[[sources/software-dev/wims-bfp-ch3a-research-design]] — research design, requirements (FR/NFR/security), development model

### The Architecture
[[sources/software-dev/wims-bfp-ch3b-architecture]] — three-layer architecture, data flow, AI workflow, deployment

### Security & Tools
[[sources/software-dev/wims-bfp-ch3c-security-tools]] — security practices, FARM stack, testing tools

### Testing & Evaluation
[[sources/software-dev/wims-bfp-ch3d-testing-data]] — methodologies, ISO/IEC 25010, statistical treatment, ethics

### Codebase Reality
[[sources/software-dev/wims-bfp-knowledge-graph]] — thesis vs actual codebase alignment, health report
[[analyses/wims-bfp-thesis-codebase-gaps]] — discrepancy analysis

---

## Architecture Stack

```
Civilian Reporter → VPS Portal (Next.js PWA)
                         ↓
                    Nginx Reverse Proxy
                         ↓
              Keycloak (RBAC + MFA)
                         ↓
              FastAPI Orchestrator
              ↙          ↘
    PostgreSQL+PostGIS    Redis → Celery
         ↕                    ↓
    PostGIS Heatmaps    Suricata IDS
                             ↓
                       Qwen2.5-3B (XAI)
                             ↓
                    Forensic Narratives
```

**Full stack breakdown:** [[sources/software-dev/wims-bfp-ch3b-architecture]]

---

## Security Concepts (per stack)

| Stack Component | Security Page |
|----------------|---------------|
| Docker + Compose | [[concepts/docker-security-wims-bfp]] |
| FastAPI + Celery/Redis | [[concepts/fastapi-security-wims-bfp]] |
| Keycloak + JWT | [[concepts/keycloak-fastapi-security-wims-bfp]] |
| PostgreSQL + RLS | [[concepts/postgresql-security-wims-bfp]] |
| PostGIS + Spatial | [[concepts/postgis-security-wims-bfp]] |

---

## Threat Landscape

| Concern | Source |
|---------|-------|
| OWASP Top 10 (2025) | [[sources/software-dev/owasp-top-10-2025]] |
| CWE Top 25 (2025) | [[sources/software-dev/cwe-top-25-2025]] |
| Zero Trust Architecture | [[concepts/zero-trust-architecture]] |
| Secure Coding Practices | [[concepts/secure-coding-practices]] |

---

## CVE Tracking

| Component | CVEs |
|-----------|------|
| Docker/runc | [[sources/software-dev/docker-cves-2025-2026]] |
| PostgreSQL | [[sources/software-dev/postgresql-cves-2025-2026]] |
| FastAPI | [[sources/software-dev/fastapi-cves-2025-2026]] |
| Next.js | [[sources/cybersecurity/nextjs-cves-2026]] |
| Keycloak | [[sources/cybersecurity/keycloak-cves-2026]] |
| Suricata | [[sources/cybersecurity/suricata-cves-2026]] |

---

## Codebase Audit

| What | Page |
|------|------|
| Pre-refactor ingestion | [[sources/software-dev/wims-bfp-codebase-ingestion-2026-04-08]] |
| Codebase metrics | [[sources/software-dev/wims-bfp-codebase-metrics]] |
| Regional encoder CRUD audit | [[sources/software-dev/wims-bfp-regional-encoder-audit-2026-04-08]] |
| Thesis revisions (51 changes) | [[sources/software-dev/wims-bfp-thesis-revisions-2026-04-08]] |
| Thesis vs codebase gaps | [[analyses/wims-bfp-thesis-codebase-gaps]] |

---

## Operational

| What | Page |
|------|------|
| 4-Agent pipeline postmortem | [[analyses/4-agent-pipeline-postmortem]] |

---

*This MOC is the single entry point for all WIMS-BFP related content in the vault.*
