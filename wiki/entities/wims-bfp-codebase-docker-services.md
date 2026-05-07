---
id: wims-bfp-codebase-docker-services-001
type: entity
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
  - docker
  - devops
  - architecture
related:
  - sources/wims-bfp-codebase/wims-bfp-codebase-architecture-summary
  - concepts/wims-bfp-development-setup
  - entities/wims-bfp-codebase-keycloak-config
---

# Docker Services

All services in `src/docker-compose.yml` on the `wims_internal` Docker network.

## Service Inventory

| Service | Container | Port | Health Check | Purpose |
|---------|-----------|------|-------------|---------|
| `wims-postgres` | postgres:15 | 5432 | `pg_isready` | PostgreSQL + PostGIS |
| `wims-redis` | redis:7.2 | 6379 | `redis-cli ping` | Cache + Celery broker |
| `wims-keycloak` | keycloak:24 | 8080 | `/health/ready` | Identity provider (OIDC + MFA) |
| `wims-backend` | custom (FastAPI) | 8000 | `/health` | API server |
| `wims-frontend` | custom (Next.js) | 3000 | HTTP 200 | PWA frontend |
| `wims-celery-worker` | custom (Celery) | — | — | Async task execution |
| `wims-celery-beat` | custom (Celery) | — | — | Periodic task scheduler |
| `wims-ollama` | ollama | 11434 | `/api/tags` | Qwen2.5-3B inference |
| `wims-suricata` | custom | — | EVE JSON | IDS network monitoring |
| `wims-nginx` | nginx:alpine | 80/443 | HTTP 200 | Reverse proxy |

## Network Architecture

```
Internet
   │
   ▼
┌──────────┐
│  Nginx   │  :80/:443 (SSL termination)
└────┬─────┘
     │
     ▼ wims_internal network
┌────────────────────────────────────────────────┐
│  Keycloak (:8080)  ←→  Backend (:8000)        │
│       │                    │                    │
│       ▼                    ▼                    │
│  PostgreSQL (:5432)   Redis (:6379)            │
│                          │                     │
│                     Celery Worker              │
│                          │                     │
│                ┌─────────┴─────────┐           │
│                ▼                   ▼           │
│           Suricata            Ollama           │
│           (:EVE)           (:11434)            │
└────────────────────────────────────────────────┘
     │
     ▼
  Frontend (:3000)  ← Next.js PWA
```

## Related

- [[sources/wims-bfp-codebase/wims-bfp-codebase-architecture-summary]] — full stack overview
- [[concepts/wims-bfp-development-setup]] — how to start services locally
- [[entities/wims-bfp-codebase-keycloak-config]] — Keycloak realm configuration
