---
id: wims-bfp-ch3b-architecture-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-07-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - raw/misc/03-04-01-architecture-overview.md
  - raw/misc/03-04-02-context-diagram.md
  - raw/misc/03-04-03-data-flow-diagram.md
  - raw/misc/03-04-04-use-case-diagram.md
  - raw/misc/03-04-05-er-diagram.md
  - raw/misc/03-04-06-ai-workflow.md
  - raw/misc/03-04-07-deployment-diagram.md
  - raw/misc/03-04-08-activity-diagram.md
  - raw/misc/03-04-09-comparative-design.md
  - raw/misc/03-04-system-architecture.md
status: active
tags:
  - wims-bfp
  - thesis
  - chapter-3
  - architecture
  - system-design
related:
  - sources/software-dev/wims-bfp-ch3a-research-design
  - concepts/postgis-security-wims-bfp
  - concepts/keycloak-fastapi-security-wims-bfp
---

# WIMS-BFP Chapter 3b: System Architecture

**Source:** raw/misc/ (10 files)
**Chapter:** 3b — Architecture Overview, Diagrams, AI Workflow, Deployment

---

## Architecture Overview

**Pattern:** Highly decoupled, hybrid architecture bridging public VPS with Sovereign LAN, enforcing [[concepts/zero-trust-architecture|Zero-Trust]].

### Three-Layer Architecture

**1. Public and Regional Edge**
- Public-facing VPS portal for Civilian Reporters (crowdsourced fire alerts)
- Offline-first PWA for Regional Encoders ([[sources/software-dev/wims-bfp-ch3b-architecture|Dexie.js/IndexedDB]] for local caching)
- Auto-sync on connectivity restoration

**2. Internal Workstations and Access Control**
- Nginx reverse proxy routes all incoming traffic
- [[concepts/keycloak-fastapi-security-wims-bfp|Keycloak]] enforces RBAC via JWT
- Strict Separation of Duties (SoD)

**3. Sovereign Core ([[concepts/docker-security-wims-bfp|Docker-containerized]])**
- [[concepts/fastapi-security-wims-bfp|FastAPI]] orchestrator (ingests alerts, parses sync data, executes triage)
- Redis + Celery for async operations (AI inference, report generation)
- [[concepts/postgresql-security-wims-bfp|PostgreSQL]] + [[concepts/postgis-security-wims-bfp|PostGIS]] for verified records + geospatial heatmaps
- Suricata IDS for network monitoring
- Qwen2.5-3B for XAI narrative generation

---

## Data Flow

```
Civilian Reporter → VPS Portal → FastAPI (rate-limited) → DMZ queue
Regional Encoder → PWA (offline) → IndexedDB → Sync → FastAPI
FastAPI → Validation → PostgreSQL (with RLS)
Suricata → EVE JSON → Celery → Qwen2.5-3B → security_logs table
National Validator → Dashboard → Triage workflow → Verified status
National Analyst → Heatmaps → PostGIS spatial queries → Geospatial output
```

---

## ER Diagram (Key Entities)

| Entity | Purpose | Security Attributes |
|---|---|---|
| fire_incidents | Primary relational hub | UUID, non-repudiable link to source |
| incident_nonsensitive_details | Operational metrics (classification, damages, casualties) | Accessible to National Analysts |
| incident_sensitive_details | PII (addresses, narratives, caller contact) | Restricted to Validators + Admins |
| regions → provinces → cities | Hierarchical geographic lookup | Sovereignty enforcement |
| responding_units | Fire engine timelines | One-to-many with incidents |
| involved_parties | Occupant/owner documentation | PII protected |
| incident_attachments | File metadata + SHA-256 hashes | Mathematical proof of integrity |
| security_logs | Suricata alerts + XAI narratives | Human-readable audit trail |
| incident_bundles | Regional data packages | AES-256-GCM encrypted |

### Data Partitioning Strategy
- 1:1 relationship between core incident and partitioned details
- Separates operational transparency from PII privacy
- Supports RA 10173 data minimization

---

## AI Workflow (4-Stage Contextualization Pipeline)

| Stage | Input | Process | Output |
|---|---|---|---|
| 1. Deterministic Trigger | Suricata IDS signature-based threat | EVE JSON log generated | Raw alert data |
| 2. Prompt Construction | FastAPI extracts metadata (source IP, dest port, signature) | Injected into "Sovereign Forensic Template" | Structured prompt |
| 3. In-Context Inference | Qwen2.5-3B receives structured prompt | In-Context Learning synthesizes technobabble | Concise narrative |
| 4. Forensic Presentation | Narrative stored in security_logs | Displayed on admin dashboard | Human-readable intelligence |

**Key distinction:** AI does NOT perform anomaly detection. It only translates deterministic [[sources/software-dev/wims-bfp-ch3c-security-tools|Suricata alerts]] into narratives. Detection = Suricata (rules). Interpretation = Qwen2.5-3B (XAI).

---

## Deployment Architecture

| Component | Technology | Network Zone |
|---|---|---|
| Public Portal | Next.js PWA on VPS | DMZ (public internet) |
| Reverse Proxy | Nginx | DMZ → Internal boundary |
| Identity Provider | Keycloak | Internal LAN |
| Backend API | FastAPI + Celery | Internal LAN |
| Message Broker | Redis | Internal LAN |
| Database | PostgreSQL + PostGIS | Sovereign LAN (isolated) |
| IDS | Suricata (containerized) | Internal LAN (traffic mirror) |
| AI Engine | Qwen2.5-3B via Llama.cpp | Sovereign LAN |
| KMS | OpenBao | Sovereign LAN |

### Container Isolation
- Docker bridge network isolates DB from public exposure
- Security infrastructure (Suricata, OpenBao) as isolated containers
- Platform-agnostic deployment on standard government hardware

---

## Use Cases (5 Actors)

| Actor | Primary Actions |
|---|---|
| Civilian Reporter | Submit incident report, upload evidence (5MB limit), view public status |
| Regional Encoder | Encode incidents (offline/online), sync data, view regional dashboard |
| National Validator | Cross-reference reports with dispatches, mark "Verified", manage triage |
| National Analyst | View heatmaps, filter by date/region, generate comparative analysis, export |
| System Admin | View audit logs, review XAI narratives, manage users, configure Suricata rules |

---

## Comparative Design

| Criterion | WIMS-BFP | Traditional (BFP-AIMS) |
|---|---|---|
| Offline Support | First-class (PWA + IndexedDB) | None |
| Spatial Analytics | PostGIS heatmaps | Static tabular records |
| Threat Interpretation | XAI human-readable narratives | Raw logs (black box) |
| Access Control | Keycloak RBAC + MFA | Basic authentication |
| Data Integrity | SHA-256 hash chaining | None |
| Cloud Architecture | VPS + Sovereign LAN | Monolithic server |
