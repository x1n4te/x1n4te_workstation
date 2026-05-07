---
id: wims-bfp-codebase-ingestion-2026-04-08
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-06-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - ~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/
status: active
tags:
  - wims-bfp
  - codebase-ingestion
  - pre-refactor
  - fastapi
  - nextjs
  - postgresql
related:
  - concepts/docker-security-wims-bfp
  - concepts/fastapi-security-wims-bfp
  - concepts/postgresql-security-wims-bfp
  - concepts/keycloak-fastapi-security-wims-bfp
  - entities/wims-bfp-agentic-workflow
---

# WIMS-BFP Codebase Ingestion — Pre-Refactor Baseline

Related: [[sources/software-dev/wims-bfp-codebase-metrics]], [[analyses/wims-bfp-thesis-codebase-gaps]], [[mocs/wims-bfp]]

**Date:** 2026-04-08
**Purpose:** Full codebase snapshot before ground-up feature refactoring.
**Source:** `~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/`

---

## 1. Repository Topology

```
LOCAL-WIMS-BFP-PROTOTYPE/
├── .github/workflows/ci.yml          # CI: frontend lint+build, backend lint+test
├── .ai-context/
├── AFORs/                             # 6 AFOR template/spreadsheet files
├── archive/sql/                       # Superseded SQL (CONSOLIDATED_UNUSED_SQL.sql)
├── docs/
│   ├── ARCHITECTURE.md                # System stack, services, data flow
│   └── API_AND_FUNCTIONS.md           # Complete API reference
├── scripts/                           # seed-dev-users.sh, seed-analytics-*
├── src/
│   ├── docker-compose.yml             # 10 services
│   ├── .env                           # WIMS_MASTER_KEY
│   ├── backend/                       # FastAPI (Python 3.11)
│   │   ├── main.py                    # App entry, routes, rate-limit, PKCE callback
│   │   ├── auth.py                    # Keycloak JWT/OIDC (353 lines)
│   │   ├── database.py                # SQLAlchemy + RLS context
│   │   ├── celery_config.py           # Beat: suricata ingestion 10s
│   │   ├── api/routes/                # 8 route modules
│   │   ├── models/                    # 6 SQLAlchemy models
│   │   ├── schemas/                   # 3 Pydantic schemas
│   │   ├── services/                  # ai_service, suricata_ingestion, analytics_read_model
│   │   ├── tasks/                     # suricata, exports (Celery)
│   │   ├── utils/crypto.py            # AES-256-GCM PII encryption
│   │   └── tests/                     # 18 test files (6 unit + 12 integration)
│   ├── frontend/                      # Next.js 16, React 19, TypeScript
│   │   ├── src/app/                   # App Router pages
│   │   ├── src/components/            # 10 React components
│   │   ├── src/context/AuthContext.tsx
│   │   ├── src/lib/                   # api, auth, oidc, offlineStore
│   │   └── src/types/api.ts
│   ├── postgres-init/                 # 01_wims_initial.sql (1468 lines DDL+RLS)
│   ├── keycloak/bfp-realm.json
│   ├── nginx/nginx.conf
│   └── suricata/                      # IDS rules + logs
├── CLAUDE.md                          # Project conventions
├── README.md                          # Quick start, security architecture
├── CHANGELOG.md                       # v0.1.0, v0.2.0, Unreleased
├── implementation_plan.md             # REGIONAL_ENCODER + AFOR import plan
├── SCHEMA_MERGE_NOTES.md              # Schema precedence, wildland AFOR mapping
└── tasks.md                           # Tier 3 compliance tasks (login)
```

**File counts:** 199 source files (61 Python, 56 TypeScript/TSX, 1468-line SQL DDL).

---

## 2. Stack Summary

| Layer      | Technology                                           | Version         |
| ---------- | ---------------------------------------------------- | --------------- |
| Frontend   | Next.js (App Router), React, TypeScript, TailwindCSS | 16 / 19 / 4     |
| Backend    | FastAPI + SQLAlchemy + GeoAlchemy2                   | Python 3.11     |
| Queue      | Celery + Redis                                       | 5.4 / 7.2       |
| Database   | PostgreSQL + PostGIS                                 | 15 / 3.4        |
| Auth       | Keycloak (JWT/OIDC, PKCE)                            | 24.0.0          |
| AI/XAI     | Ollama + Qwen2.5-3B                                  | local inference |
| IDS        | Suricata (EVE JSON)                                  | latest          |
| Gateway    | Nginx reverse proxy                                  | alpine          |
| Encryption | AES-256-GCM (cryptography lib)                       | 43.0+           |

---

## Related Sections
*Detailed content split into sub-pages for readability. See [[sources/software-dev/wims-bfp-codebase-ingestion-2026-04-08-details]] for the full reference.*

---

*This page is scannable in 30 seconds. Full reference content moved to sub-pages.*
