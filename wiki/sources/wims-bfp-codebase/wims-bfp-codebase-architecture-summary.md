---
id: wims-bfp-codebase-architecture-001
type: source
created: 2026-04-21
updated: 2026-04-21
last_verified: 2026-04-21
review_after: 2026-06-21
stale_after: 2026-10-21
confidence: high
source_refs:
  - raw/sources/wims-bfp-codebase/docs/ARCHITECTURE.md
status: active
tags:
  - wims-bfp
  - architecture
  - docker
  - design
related:
  - entities/wims-bfp-codebase-docker-services
  - entities/wims-bfp-codebase-database-schema
  - concepts/wims-bfp-codebase-data-flow
  - mocs/wims-bfp
---

# WIMS-BFP Architecture Summary (Codebase)

Full-stack incident management platform for the Philippine Bureau of Fire Protection. Civilian reporters submit fire incidents via a public PWA. Regional encoders import AFORs from Excel. National validators review. Analysts see heatmaps and trends. System admins manage users and Suricata IDS alerts processed by Qwen2.5-3B (XAI).

## Stack (Verified from package.json + docker-compose.yml)

| Layer | Tech | Version | Source |
|-------|------|---------|--------|
| Frontend | Next.js + React + TypeScript | 16 / 19 / 5.x | `src/frontend/package.json` |
| Backend | FastAPI + SQLAlchemy + Celery | 0.135+ / 2.0+ / 5.4+ | `src/backend/main.py` |
| Database | PostgreSQL + PostGIS | 15 / 3.4 | `src/docker-compose.yml` |
| Cache/Queue | Redis + Celery | 7.2 / 5.4 | `src/docker-compose.yml` |
| Auth | Keycloak (OIDC + MFA) | 24 | `src/keycloak/bfp-realm.json` |
| AI/XAI | Ollama (Qwen2.5-3B) | — | `src/backend/services/ai_service.py` |
| IDS | Suricata | — | `src/suricata/` |
| Gateway | Nginx | Alpine | `src/nginx/` |

All services run on `wims_internal` Docker network. See [[entities/wims-bfp-codebase-docker-services]].

## Key Directories

| Path | Role |
|------|------|
| `src/backend/` | FastAPI entry, auth, SQLAlchemy, Celery |
| `src/backend/api/routes/` | HTTP route modules |
| `src/frontend/src/app/` | Next.js App Router pages |
| `src/postgres-init/` | DB bootstrap SQL |
| `src/keycloak/` | Realm import JSON |
| `src/suricata/` | IDS rules + logs |
| `src/nginx/` | Reverse proxy config |

## High-Level Data Flow

1. Public submissions → `POST /api/civilian/reports` → `wims.citizen_reports`
2. Triage → `GET /api/triage/pending` → `POST /api/triage/{id}/promote` → `wims.fire_incidents`
3. Regional encoders → `POST /api/regional/afor/import` → commit → structural or wildland tables
4. Analysts → `/api/analytics/*` → heatmaps, trends
5. Admin → `/api/admin/security-logs` → XAI narrative analysis

See [[concepts/wims-bfp-codebase-data-flow]] for full pipeline and [[entities/wims-bfp-codebase-api-endpoints]] for all routes.

## Design Principles

- **Zero Trust:** No trusted network zones. Every request authenticated via [[concepts/wims-bfp-codebase-auth-flow]].
- **Explainability, Not Autonomy:** Qwen2.5 translates Suricata JSON to English. It does NOT detect threats or execute actions.
- **No Hard Deletes:** All tables use `deleted_at` soft-delete.
- **RLS Mandatory:** All `wims.*` tables have RLS enabled.
- **Offline-First:** PWA uses IndexedDB + Service Workers.

## Constitution Alignment

- Hybrid single-segmented VPS: public edge and Sovereign Core firewalled via Docker networks
- PII minimized, encrypted at rest, subject to RLS
- Heavy processes (>500ms) offloaded to Celery workers
- Governed by `.specify/memory/constitution.md`

## Related

- [[entities/wims-bfp-codebase-docker-services]] — all Docker services, ports, health checks
- [[entities/wims-bfp-codebase-database-schema]] — full table listing
- [[entities/wims-bfp-codebase-api-endpoints]] — all API routes
- [[concepts/wims-bfp-sprint-timeline]] — current sprint plan
- [[mocs/wims-bfp]] — project map of content
