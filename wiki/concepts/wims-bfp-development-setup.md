---
id: wims-bfp-dev-setup-001
type: concept
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
  - devops
  - docker
  - development
related:
  - concepts/wims-bfp-project-conventions
  - entities/wims-bfp-codebase-docker-services
  - entities/wims-bfp-codebase-database-schema
  - mocs/wims-bfp
---

# WIMS-BFP Development Setup

How to run WIMS-BFP locally. See [[entities/wims-bfp-codebase-docker-services]] for service details.

## Prerequisites

- Docker + Docker Compose v2
- Node.js 20+
- Python 3.11+
- Git

## Quick Start

```bash
# 1. Clone
git clone https://github.com/x1n4te/WIMS-BFP-PROTOTYPE.git
cd WIMS-BFP-PROTOTYPE

# 2. Start all services (from src/)
cd src && docker compose up -d

# 3. Wait for healthchecks (~30s)
docker compose ps  # all should be "healthy"

# 4. Seed dev users
cd .. && ./scripts/seed-dev-users.sh

# 5. Open
# Frontend: http://localhost:3000
# Keycloak: http://localhost:8080 (admin/admin)
# Backend:  http://localhost:8000/docs
```

## Environment Variables

### Backend (`.env` in `src/backend/`)

```bash
SQLALCHEMY_DATABASE_URL=postgresql://postgres:***@localhost:5432/wims
REDIS_URL=redis://localhost:6379/0
KEYCLOAK_REALM_URL=http://localhost:8080/auth/realms/bfp
KEYCLOAK_CLIENT_ID=bfp-client
KEYCLOAK_AUDIENCE=bfp-client
KEYCLOAK_ISSUER=http://localhost:8080/auth/realms/bfp/
WIMS_MASTER_KEY=<base64-encoded-32-byte-key>
```

### Frontend (`.env` in `src/frontend/`)

```bash
NEXT_PUBLIC_AUTH_API_URL=http://localhost:8080/realms/bfp/protocol/openid-connect
NEXT_PUBLIC_BASE_URL=http://localhost:3000
NEXT_PUBLIC_MAPBOX_TOKEN=***  # leave empty for local dev
```

## Running Tests

### Backend
```bash
cd src/backend
pytest -v --ignore=tests/integration/           # unit
pytest -v tests/integration/                     # integration (needs postgres + redis)
pytest -v --cov=. --cov-report=term-missing       # with coverage
```

### Frontend
```bash
cd src/frontend
npx vitest run       # run
npx vitest           # watch
```

## Linting

```bash
cd src/backend && ruff check . && ruff format --check .  # backend
cd src/frontend && npm run lint                           # frontend
```

## Common Issues

| Problem | Fix |
|---------|-----|
| Backend can't connect to postgres | Run from `src/` not root: `cd src && docker compose up -d` |
| Keycloak redirects to wrong URL | `KEYCLOAK_ISSUER` must match browser URL (localhost:8080) |
| RLS errors in tests | Use `get_db()` (no RLS) or `get_db_with_rls()` with context |
| Frontend build fails | `rm -rf .next && npm run build` |

## Related

- [[entities/wims-bfp-codebase-docker-services]] — service ports, health checks, dev users
- [[entities/wims-bfp-codebase-init-scripts]] — database migration order
- [[concepts/wims-bfp-project-conventions]] — branch naming, commit style
