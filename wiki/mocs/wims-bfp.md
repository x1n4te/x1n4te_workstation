---
id: wims-bfp-moc-001
type: MOC
created: 2026-04-08
updated: 2026-05-04
last_verified: 2026-05-03
review_after: 2026-07-08
stale_after: 2026-10-08
confidence: high
source_refs: []
status: active
tags:
  - moc
  - wims-bfp
  - thesis
related:
  - sources/operational/2026-05-03-wims-bfp-pr78-pr83-integration-closeout
  - sources/software-dev/wims-bfp-abstract
  - sources/software-dev/wims-bfp-ch1-introduction
  - analyses/wims-bfp-frs-implementation-tracker
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

### Ethics & IERC Compliance
[[sources/software-dev/wims-bfp-ethics-section-revision-2026-04-11]] — Section 3.9 expansion, IERC integration, AI writing remediation
[[sources/software-dev/wims-bfp-ierc-appendices]] — IERC form field details (Appendix A, H, Consent template)

### Codebase Reality
[[sources/software-dev/wims-bfp-knowledge-graph]] — thesis vs actual codebase alignment, health report
[[analyses/wims-bfp-thesis-codebase-gaps]] — discrepancy analysis
[[raw/articles/wims-bfp-frs-modules-deep-research-2026-05-04]] — M5d/M6–M12/M14–M15 gap analysis + agent research brief

### Thesis Structure Reference
[[raw/articles/wims-bfp-paper-structure-2026-05-04]] — full 6-chapter paper outline with structural mapping
[[raw/articles/wims-bfp-research-question-alignment-matrix-2026-05-04]] — objective-to-evidence alignment matrix (Ch1→Ch3→Ch4)
[[raw/articles/wims-bfp-expert-validation-guide-2026-05-04]] — 7-step expert validation procedure, CVI computation, letter + form templates
[[raw/articles/wims-bfp-ethical-security-testing-guide-2026-05-04]] — ethical testing procedure, documentation requirements, panel defense template
[[raw/articles/wims-bfp-authority-approval-letter-template-2026-05-04]] — formal permission request letter, consent block, WIMS-BFP pre-filled fields
[[raw/articles/wims-bfp-post-test-evaluation-questionnaire-2026-05-04]] — ISO 25010 survey: 30 items, 5 categories, weighted mean analysis guide, Ch4 evidence mapping
[[raw/articles/wims-bfp-security-testing-evaluation-questionnaire-2026-05-04]] — security expert survey (30 items, 6 categories) + technical testing guidelines (7 test areas, AUTH-001 AVAIL-001 samples, video requirements)
[[raw/articles/wims-bfp-system-development-compliance-checklist-2026-05-04]] — 11-section development checklist: legal/ethical, requirements, UI/UX, functional, DB, security, performance, AI, testing, docs, defense
[[raw/articles/wims-bfp-enhanced-cybersecurity-development-checklist-2026-05-04]] — advanced technical controls: MFA, Zero Trust, session security, input validation, data protection, logging, API security, security testing readiness
[[raw/articles/wims-bfp-secure-coding-deployment-checklist-2026-05-04]] — secure coding (input handling, auth, secrets, deps) + secure deployment (server hardening, Nginx headers, HTTPS, cloud IAM/storage, backups)

### Codebase Documentation (LLM Wiki)
[[sources/wims-bfp-codebase/wims-bfp-codebase-architecture-summary]] — verified tech stack, data flow, design principles
[[sources/wims-bfp-codebase/wims-bfp-codebase-wiki-github-activity-2026-04-21]] — in-repo wiki evolution + GitHub PR/issues/commits (Apr 21–22)
[[concepts/wims-bfp-sprint-timeline]] — 6-sprint plan (Apr 22–May 5), all 13 modules mapped
[[concepts/wims-bfp-sprint-gantt]] — Mermaid Gantt chart, visual sprint overview
[[concepts/wims-bfp-frs-modules]] — 13-module FRS tracker, codebase-verified status
[[concepts/wims-bfp-development-setup]] — quick start, env vars, tests, lint
[[concepts/wims-bfp-project-conventions]] — git, security, constitution mandates

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

| Stack Component        | Security Page                                   |
| ---------------------- | ----------------------------------------------- |
| Docker + Compose       | [[concepts/docker-security-wims-bfp]]           |
| FastAPI + Celery/Redis | [[concepts/fastapi-security-wims-bfp]]          |
| Keycloak + JWT         | [[concepts/keycloak-fastapi-security-wims-bfp]] |
| Keycloak Auth Flows    | [[concepts/keycloak-authentication-flows]]      |
| Keycloak Themes        | [[concepts/keycloak-custom-themes]]             |
| Keycloak Admin API     | [[concepts/keycloak-admin-rest-api]]            |
| Keycloak Docker        | [[concepts/keycloak-docker-deployment]]         |
| PostgreSQL + RLS       | [[concepts/postgresql-security-wims-bfp]]       |
| PostGIS + Spatial      | [[concepts/postgis-security-wims-bfp]]          |

---

## Codebase Reference (Verified 2026-04-21)

Codebase-accurate pages from the in-repo wiki. These contain verified tech versions, exact API paths, and implementation status.

### Entities

| Page | What |
|------|------|
| [[entities/wims-bfp-codebase-api-endpoints]] | All backend + frontend API routes with role guards |
| [[entities/wims-bfp-codebase-database-schema]] | Full table listing, enums, indexes |
| [[entities/wims-bfp-codebase-docker-services]] | Docker Compose services, ports, health checks |
| [[entities/wims-bfp-codebase-frontend-pages]] | Page routes, components, lib files |
| [[entities/wims-bfp-codebase-init-scripts]] | SQL migration order and what each does |
| [[entities/wims-bfp-codebase-keycloak-config]] | Realm config, clients, roles, session settings |
| [[entities/wims-bfp-codebase-rbac-roles]] | 5 roles, scope, guard implementation |

### Concepts

| Page                                          | What                                                |
| --------------------------------------------- | --------------------------------------------------- |
| [[concepts/wims-bfp-codebase-afor-import]]    | AFOR XLSX/CSV import: structural vs wildland        |
| [[concepts/wims-bfp-codebase-auth-flow]]      | Keycloak OIDC → JWT → HttpOnly cookie → RLS context |
| [[concepts/wims-bfp-codebase-data-flow]]      | Civilian → Triage → Incident → Analytics pipeline   |
| [[concepts/wims-bfp-codebase-offline-pwa]]    | Service Worker, IndexedDB, offline sync             |
| [[concepts/wims-bfp-codebase-pii-encryption]] | AES-256-GCM encryption for sensitive fields         |
| [[concepts/wims-bfp-codebase-rls-model]]      | Row Level Security policies, helpers, patterns      |
| [[concepts/wims-bfp-codebase-spatial-data]]   | PostGIS geography columns, SRID 4326, queries       |
| [[concepts/wims-bfp-codebase-threat-model]]   | OWASP alignment, STRIDE mapping, mitigations        |
| [[concepts/wims-bfp-codebase-xai-pipeline]]   | Suricata → Celery → Qwen2.5-3B → narrative          |
| [[concepts/wims-bfp-ci-cd-pipeline]]          | GitHub Actions CI (6 jobs) + CD (GHCR build)        |

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

## Pending Refactoring

| Task | Status | Rationale |
|------|--------|-----------|
| Split regional.py (1,876 lines) | Deferred | See [[concepts/decisions-and-rationale]] — DX problem, not runtime. Thesis + frontend CRUD higher priority. |
| Alembic migrations | Pending | Versioned schema management, currently manual SQL. |

---

## Wiki Gap Analysis

| Date       | What                                                | Page                                                                   |
| ---------- | --------------------------------------------------- | ---------------------------------------------------------------------- |
| 2026-05-04 | Earl-Branch review + SPEC audit + Wiki MOC gap analysis | [[analyses/wims-bfp-wiki-moc-gap-analysis-2026-05-04]] |

## Operational

| Date       | What                                                | Page                                                                   |
| ---------- | --------------------------------------------------- | ---------------------------------------------------------------------- |
| 2026-05-04 | WIMS-BFP Earl-Branch review + SPEC audit | [[sources/operational/2026-05-04-wims-bfp-earl-branch-spec-audit]] |
|| 2026-05-04 | Session persistence — silent proactive JWT refresh for lib/auth.tsx | [[sources/operational/2026-05-04-wims-bfp-session-persistence-fix]] |
| 2026-05-03 | PR #78–#83 integration closeout, CI/CD, proactive JWT refresh hotfix | [[sources/operational/2026-05-03-wims-bfp-pr78-pr83-integration-closeout]] |
| 2026-05-03 | PR #78–#83 detailed integration record | [[sources/operational/2026-05-03-wims-bfp-pr78-pr83-integration-details]] |
| 2026-05-03 | Pre-purge session handoff archive | [[sources/operational/2026-05-03-wims-bfp-session-handoff-archive]] |
| 2026-04-22 | Codebase wiki + GitHub activity capture (Apr 21–22) | [[sources/wims-bfp-codebase/wims-bfp-codebase-wiki-github-activity-2026-04-21]] |
| 2026-04-09 | Database refactor + integration tests (Claude Code) | [[sources/operational/2026-04-09-database-refactor-integration-tests]] |
| 2026-04-08 | 4-Agent pipeline postmortem (archived)              | [[analyses/4-agent-pipeline-postmortem]]                               |

---

## Research & Trends (April 2026)

| Topic | Page |
|-------|------|
| XAI for SOC Operations | [[concepts/xai-soc-operations]] |
| Automated STRIDE Threat Modeling | [[concepts/stride-automated-threat-modeling]] |
| SLMs for Edge Security | [[concepts/slm-edge-security]] |
| ML-Enhanced Suricata | [[concepts/suricata-ml-rule-generation]] |
| Agentic SOC Trends 2026 | [[concepts/agentic-soc-trends-2026]] |
| Full Research Scan | [[sources/ai-research/ai-security-trends-april-2026]] |

---

*This MOC is the single entry point for all WIMS-BFP related content in the vault.*
