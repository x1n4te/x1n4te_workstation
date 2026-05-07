---
id: wims-bfp-ci-cd-pipeline-001
type: concept
created: 2026-04-22
updated: 2026-04-22
last_verified: 2026-04-22
review_after: 2026-06-22
stale_after: 2026-10-22
confidence: high
source_refs:
  - raw/sources/wims-bfp-codebase/wims-bfp-codebase-wiki-and-github-activity-2026-04-21.md
status: active
tags:
  - wims-bfp
  - devops
  - ci-cd
  - docker
  - testing
related:
  - concepts/wims-bfp-project-conventions
  - concepts/wims-bfp-development-setup
  - entities/wims-bfp-codebase-docker-services
  - concepts/wims-bfp-frs-modules
  - mocs/wims-bfp
---

# WIMS-BFP CI/CD Pipeline

Two-stage pipeline: **CI** validates on every push/PR, **CD** builds and deploys on merge to master. Overhauled 2026-04-21 (split monolithic job into 6 specialized jobs).

## Pipeline Overview

```
PR / Push to branch
  └─ ci.yml
       ├─ security-audit (advisory, non-blocking)
       ├─ migrations (PostGIS schema validation)
       ├─ frontend (lint → vitest → build)
       ├─ backend (lint → format → pytest + coverage)
       ├─ docker-build (compose config + build, PR only)
       └─ merge-gate (blocks if migrations/frontend/backend fail)

Merge to master
  └─ cd.yml
       ├─ build-images (backend + frontend → GHCR)
       └─ notify (build summary)
```

## CI Pipeline (`ci.yml`)

Triggered on: PR to `master`, push to `master`, `fix/*`, `feature/*`, `refactor/*`, `hotfix/*`

### Jobs

| Job | What it does | Blocking? |
|-----|-------------|-----------|
| `security-audit` | `pip-audit` + `npm audit` for known CVEs | Advisory (won't block PRs yet) |
| `migrations` | Applies all init scripts to a fresh PostGIS container, verifies `wims.*` tables exist | Yes |
| `frontend` | ESLint → vitest → Next.js build | Yes |
| `backend` | Ruff lint + format → pytest with PostGIS + Redis → coverage report | Yes (coverage advisory at 30%) |
| `docker-build` | `docker compose config` + `docker compose build` | Only on PRs touching Dockerfiles |
| `merge-gate` | Blocks merge if migrations/frontend/backend fail | Yes |

### Skipped Tests

Two test files excluded from CI (require live services):
- `tests/test_rate_limiting.py` — requires live Keycloak rate-limit config
- `tests/test_suricata_ingestion.py` — requires Suricata daemon + live EVE log

### Concurrency

Branch-level concurrency group cancels in-progress runs when a new push arrives on the same branch.

## CD Pipeline (`cd.yml`)

Triggered on: merge to `master` only

| Job | What it does |
|-----|-------------|
| `build-images` | Builds backend + frontend Docker images, pushes to GHCR with `latest` + SHA tag |
| `notify` | Writes build summary to GitHub Actions UI |

> **Note:** Production deployment (VPS SSH) pending infrastructure provisioning.
> CD currently publishes images to GHCR only.

### Image Registry

```
ghcr.io/x1n4te/wims-backend:latest
ghcr.io/x1n4te/wims-frontend:latest
```

## Coverage Gates

Backend coverage set to 30% minimum (advisory). Roadmap: 30% → 50% → 70% → 85%.

## Adding New Migrations

1. Add `.sql` file to `src/postgres-init/` with sequential numbering
2. Add filename to `ORDERED_SCRIPTS` array in `ci.yml` → `migrations` job

## Related

- [[concepts/wims-bfp-project-conventions]] — branch naming, commit style, PR rules
- [[concepts/wims-bfp-development-setup]] — local dev environment
- [[entities/wims-bfp-codebase-docker-services]] — service architecture
- [[concepts/wims-bfp-frs-modules]] — module status tracker
