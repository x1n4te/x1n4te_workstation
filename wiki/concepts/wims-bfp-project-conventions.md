---
id: wims-bfp-project-conventions-001
type: concept
created: 2026-04-21
updated: 2026-04-21
last_verified: 2026-04-21
review_after: 2026-06-21
stale_after: 2026-10-21
confidence: high
source_refs:
  - raw/sources/wims-bfp-codebase/specs/memory__constitution.md
status: active
tags:
  - wims-bfp
  - devops
  - software-dev
related:
  - concepts/wims-bfp-development-setup
  - concepts/wims-bfp-sprint-timeline
  - mocs/wims-bfp
---

# WIMS-BFP Project Conventions

Rules every agent and developer must follow before writing code.

## Code Organization

- **All code lives in `src/`.** Root-level directories are for AFORs, scripts, docs only.

## Git Conventions

### Branch Naming
- `feature/<module>-<desc>`
- `fix/<module>-<desc>`
- `refactor/*`
- `hotfix/*`
- `docs/*`

### Commit Style
Conventional commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`

### PR Rules
- All changes go through PR to `master`
- Squash merge enforced
- Tests required for new endpoints
- Lint must pass: `ruff check .` and `npm run lint`

## Security Rules

- **No secrets in code:** Use environment variables. See [[concepts/wims-bfp-development-setup]].
- **RLS is mandatory:** All `wims.*` tables have RLS enabled. Never bypass RLS in production code paths.
- **No hard deletes:** Use `deleted_at` soft-delete. Constitution mandate.

## Constitution Mandates

1. **Hybrid Single-Segmented VPS:** Public edge and Sovereign Core firewalled via Docker networks
2. **Offline-First:** PWA MUST use IndexedDB + Service Workers
3. **Zero-Trust:** Every route protected by Keycloak JWT
4. **No Hard Deletes:** Soft-deletes only
5. **Strict Role Boundaries:** National Validator is the ONLY role that can change `is_verified`
6. **Async Heavy Lifting:** >500ms processes → Celery workers
7. **Explainability, Not Autonomy:** AI cannot execute code, block IPs, or alter DB
8. **RA 10173 Compliance:** PII minimized, encrypted, subject to RLS

## File Map

```
WIMS-BFP-PROTOTYPE/
├── AGENTS.md                 ← AI agent entry point
├── README.md                 ← human-facing overview
├── wiki/                     ← LLM-optimized knowledge base (codebase-level)
├── docs/                     ← human documentation
├── scripts/                  ← seed scripts, dev utilities
├── AFORs/                    ← reference AFOR form templates
├── src/
│   ├── docker-compose.yml    ← MAIN: all services
│   ├── backend/              ← FastAPI app
│   ├── frontend/             ← Next.js app
│   ├── postgres-init/        ← SQL migrations
│   ├── keycloak/             ← realm JSON
│   ├── nginx/                ← reverse proxy
│   └── suricata/             ← IDS rules + logs
├── .github/                  ← CI workflow + PR template
├── .cursor/                  ← Cursor IDE rules
└── .specify/                 ← constitution + specs
```

## Quick Commands

```bash
cd src && docker compose up -d           # start all
./scripts/seed-dev-users.sh              # seed users
cd src/backend && pytest -v              # backend tests
cd src/frontend && npm run dev           # frontend dev
cd src/backend && ruff check .           # lint backend
cd src/frontend && npm run lint          # lint frontend
```

## Related

- [[concepts/wims-bfp-development-setup]] — local dev guide
- [[entities/wims-bfp-codebase-rbac-roles]] — role definitions
- [[mocs/wims-bfp]] — project map of content
