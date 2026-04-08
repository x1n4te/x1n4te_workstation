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

| Layer | Technology | Version |
|---|---|---|
| Frontend | Next.js (App Router), React, TypeScript, TailwindCSS | 16 / 19 / 4 |
| Backend | FastAPI + SQLAlchemy + GeoAlchemy2 | Python 3.11 |
| Queue | Celery + Redis | 5.4 / 7.2 |
| Database | PostgreSQL + PostGIS | 15 / 3.4 |
| Auth | Keycloak (JWT/OIDC, PKCE) | 24.0.0 |
| AI/XAI | Ollama + Qwen2.5-3B | local inference |
| IDS | Suricata (EVE JSON) | latest |
| Gateway | Nginx reverse proxy | alpine |
| Encryption | AES-256-GCM (cryptography lib) | 43.0+ |

---

## 3. FRS Roles (Strict Literals)

Exactly 5 roles, no aliases:
- `CIVILIAN_REPORTER` — public DMZ only, CREATE only
- `REGIONAL_ENCODER` — region-scoped CRUD on operational tables
- `NATIONAL_VALIDATOR` — region-scoped CRUD on operational tables
- `NATIONAL_ANALYST` — global READ-ONLY on operational tables
- `SYSTEM_ADMIN` — full CRUD everywhere

---

## 4. Docker Services (10 containers, `wims_internal` network)

| Service | Image | Port |
|---|---|---|
| postgres | postgis/postgis:15-3.4-alpine | 5432 |
| redis | redis:7.2-alpine | 6379 |
| keycloak | keycloak:24.0.0 | 8080 |
| ollama | (local LLM) | 11434 |
| backend | FastAPI custom Dockerfile | 8000 |
| celery-worker | Same as backend | — |
| frontend | Next.js custom Dockerfile | 3000 |
| wims-suricata | jasonish/suricata:latest | — |
| nginx-gateway | nginx:alpine | 80/443 |

---

## 5. Database Schema (1468 lines)

### Extensions
- PostGIS (geography/geometry)
- pgcrypto (gen_random_uuid)

### Core Tables (17 with RLS enabled)
| Table | Purpose |
|---|---|
| `wims.users` | Keycloak-linked identity (keycloak_id UUID, role, assigned_region_id) |
| `wims.fire_incidents` | Core incident with GEOGRAPHY(POINT,4326) location |
| `wims.citizen_reports` | Public submissions (trust_score, PENDING status) |
| `wims.incident_nonsensitive_details` | Public incident metadata (damage, resources JSONB) |
| `wims.incident_sensitive_details` | PII with AES-256-GCM blob (pii_blob_enc, encryption_iv) |
| `wims.incident_verification_history` | Status change audit trail |
| `wims.incident_attachments` | File metadata with SHA-256 |
| `wims.involved_parties` | Persons involved |
| `wims.operational_challenges` | Problems encountered |
| `wims.responding_units` | Fire truck/engine dispatch |
| `wims.data_import_batches` | Batch tracking for AFOR imports |
| `wims.incident_wildland_afor` | Wildland fire form data |
| `wims.wildland_afor_alarm_statuses` | Alarm escalation timeline |
| `wims.wildland_afor_assistance_rows` | External assistance records |
| `wims.security_threat_logs` | Suricata IDS ingestion + XAI |
| `wims.system_audit_trails` | User action audit log |
| `wims.analytics_incident_facts` | Denormalized analyst read model |

### RLS Infrastructure
- GUC: `wims.current_user_id` (set per-transaction via `SET LOCAL`)
- Helper functions: `current_user_uuid()`, `current_user_role()`, `current_user_region_id()`
- 65 RLS policies across 17 tables
- Region isolation via fire_incidents.region_id join chain

### Service Accounts
- `svc_suricata` (user_id: `00000000-0000-0000-0000-000000000001`, role: NATIONAL_ANALYST)

---

## 6. Backend API Routes

| Route Module | Prefix | Auth | Key Endpoints |
|---|---|---|---|
| `main.py` | `/api/auth/*` | Public/JWT | login (stub 401), callback (PKCE), user/me |
| `incidents.py` | `/api/incidents` | JWT | create incident, upload attachment |
| `civilian.py` | `/api/civilian` | Public | submit report (trust_score=0) |
| `public_dmz.py` | `/api/v1/public/report` | Public+RateLimit | submit public incident (encoder_id=NULL) |
| `triage.py` | `/api/triage` | ENCODER/VALIDATOR | pending queue, promote report |
| `admin.py` | `/api/admin` | SYSTEM_ADMIN | user mgmt, security logs, AI analyze, audit |
| `analytics.py` | `/api/analytics` | ANALYST/ADMIN | heatmap, trends, comparative, CSV export |
| `regional.py` | `/api/regional` | REGIONAL_ENCODER | AFOR import/commit, incidents, stats |
| `ref.py` | `/api/ref` | JWT | regions, provinces, cities |

---

## 7. Security Architecture

### Authentication
- Keycloak OIDC/PKCE via `oidc-client-ts` (frontend)
- JWT validation via `python-jose` with JWKS caching (60s TTL)
- HttpOnly cookie transport (no Authorization header)
- Role resolution: `realm_access.roles` or `resource_access.<client>.roles`
- Rate limiting: Redis Lua sliding window (5 req/15min per IP on login)

### Authorization
- `get_current_wims_user` → resolves JWT to wims.users row, attaches to request.state
- `get_system_admin` → SYSTEM_ADMIN only
- `get_regional_encoder` → REGIONAL_ENCODER with assigned_region_id
- `get_analyst_or_admin` → NATIONAL_ANALYST or SYSTEM_ADMIN
- `get_regional_user` → any user with assigned_region_id

### Encryption at Rest
- AES-256-GCM for PII in incident_sensitive_details
- Fields: caller_name, caller_number, owner_name, occupant_name
- AAD bound to incident_id
- WIMS_MASTER_KEY from env (base64-encoded 32-byte key)

### RLS Enforcement
- `get_db_with_rls()` dependency sets `SET LOCAL wims.current_user_id` per transaction
- All 17 operational tables have RLS ENABLE + FORCE
- Region-scoped roles filtered via fire_incidents.region_id join chain
- NATIONAL_ANALYST: global read
- SYSTEM_ADMIN: full CRUD bypass

---

## 8. Frontend Pages

| Route | Purpose |
|---|---|
| `/` | Landing → login |
| `/login` | Login screen (Keycloak OIDC) |
| `/callback` | OIDC callback + token sync |
| `/report` | Public emergency report |
| `/dashboard` | Main dashboard (role-based) |
| `/dashboard/regional` | Regional encoder dashboard |
| `/dashboard/regional/incidents/[id]` | Region-scoped incident detail |
| `/dashboard/analyst` | Analyst heatmap/trends |
| `/home` | Operations center |
| `/incidents` | Incident list/table |
| `/incidents/create` | Manual incident entry |
| `/incidents/import` | Bulk import |
| `/incidents/triage` | Triage queue |
| `/incidents/[id]` | Incident detail |
| `/afor/import` | AFOR file upload (structural + wildland) |
| `/afor/create` | Manual AFOR entry |
| `/admin/system` | SYSTEM_ADMIN hub |

---

## 9. CI/CD (GitHub Actions)

**ci.yml** — Two jobs:
- **frontend:** Node 20, ESLint, Next.js build
- **backend:** Python 3.12, Ruff lint + format check, pytest with PostGIS+Redis services
- **merge-gate:** Both jobs must pass

---

## 10. Celery Tasks

| Task | Schedule | Purpose |
|---|---|---|
| `tasks.suricata.ingest_suricata_eve` | Every 10s | Parse EVE JSON alerts → security_threat_logs |
| `tasks.exports` | On-demand | CSV export for analysts |

---

## 11. Known Issues & Tech Debt (Pre-Refactor)

1. **Login is a stub** — `POST /api/auth/login` always returns 401; actual auth is via PKCE callback
2. **RLS not universally wired** — Some routes use `get_db()` instead of `get_db_with_rls()`
3. **No Alembic migrations** — Schema bootstrapped via Docker entrypoint SQL only
4. **AFOR parser is monolithic** — `regional.py` is 1876 lines (parsing + routes)
5. **Suricata ingestion uses in-memory file positions** — Lost on restart; should use Redis
6. **analytics_incident_facts** — Manual sync required; no triggers
7. **No CSRF protection** — Relies on HttpOnly cookies alone
8. **Docker compose has hardcoded secrets** — .env contains WIMS_MASTER_KEY in plaintext

---

## 12. Pre-Refactor Baseline

This ingestion captures the complete state of the WIMS-BFP codebase as of 2026-04-08, before the ground-up feature refactoring begins. All architectural decisions, security patterns, and known issues documented here serve as the reference point for the refactoring effort.
