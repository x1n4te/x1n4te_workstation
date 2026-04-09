# Wiki Log

Append-only activity log. Newest entries first.

**Entries archived:** 12 older entries moved to wiki/log-archives/log-2026-04-08.md

---

## 2026-04-09

**2026-04-09 | fix | Auth loop — 5 root causes in docker-compose.yml**
- Fixed: keycloak ports 8080:8080 (browser OIDC redirect blocked)
- Fixed: keycloak healthcheck accepts 302 (was expecting 200 OK)
- Fixed: frontend ports 3000:3000 (callback URL unreachable)
- Fixed: ollama healthcheck removed (no curl/wget in image)
- Fixed: backend ollama dependency relaxed to service_started
- Fixed: BACKEND_URL routed through nginx (cookie domain fix)
- Fixed: sw.js URL exclusions for /api/ and /auth/ (CORS + OIDC state fix)
- Root cause: 7 issues total — exited containers, missing ports, broken healthchecks, cookie routing, service worker interception
- Wiki: created wiki/sources/operational/2026-04-09-auth-loop-fix.md
- Commit: cd519f6

**2026-04-09 | code | Database refactor + integration tests delegated to Claude Code**
- Delegated: Claude Code print mode ($1.74, 23 turns)
- Fixed: database.py — eager init of _engine/_SessionLocal, load_dotenv() before URL resolution
- Added: get_db() (bare) + get_db_with_rls() (RLS-aware) split to avoid dependency cycle
- Tests: 15/15 passed (test_regional_crud.py — create, read, update, delete with status gating)
- Docs: updated docs/API_AND_FUNCTIONS.md (3 CRUD endpoints added), docs/ARCHITECTURE.md (DB session management section), docs/CHANGELOG.md (new Unreleased entry)
- Cleanup: Claude removed 11 stale files (1,655 lines), CHANGELOG.md moved to docs/
- Wiki: created wiki/sources/operational/2026-04-09-database-refactor-integration-tests.md

---

## 2026-04-08

**2026-04-08 | wiki | LLM Wiki audit gate — 6 Karpathy-pattern fixes applied**
- Created: wiki/overview-state-of-field.md — WIMS-BFP field overview, research landscape, knowledge gaps
- Added: inline [[wikilinks]] to abstract (6), ch3b-architecture (5), hermes-agent-setup (3)
- Created: wiki/mocs/wims-bfp.md — thesis architectural MOC tying all sources/concepts together
- Normalized: wiki/index.md table formatting (all sections now use standard | markdown)
- Truncated: wiki/log.md to 20 entries (12 archived to wiki/log-archives/)
- Reclassified: 4-agent postmortem → archived/lessons-learned with decision rationale cross-links
- Index: updated (68 pages)

**2026-04-08 | wiki | LLM Wiki audit gate — 6 fixes applied**
- Created: wiki/overview-state-of-field.md — WIMS-BFP field overview, research landscape, knowledge gaps
- Added: inline [[wikilinks]] to abstract (6), ch3b-architecture (5), hermes-agent-setup (3)
- Created: wiki/mocs/wims-bfp.md — thesis architectural MOC tying all sources/concepts together
- Normalized: wiki/index.md table formatting (all sections now use standard | markdown)
- Truncated: wiki/log.md to 20 entries (12 older entries archived)
- Index: updated (68 pages)

**2026-04-08 | wiki | Created skills MOC, environment, decisions, commands quick ref**
- Created: wiki/mocs/skills.md — 88 skills indexed by category (WIMS-BFP, dev, MLOps, creative, research, etc.)
- Created: wiki/concepts/environment-snapshot.md — Arch Linux, i5-9300H, 19GB RAM, GTX 1050 Max-Q, Wayland+Kitty
- Created: wiki/concepts/decisions-and-rationale.md — MiMo v2 Pro choice, Telegram over Discord, abandoned multi-agent, FARM stack rationale
- Created: wiki/concepts/common-hermes-commands.md — session, gateway, model, auth, cron, skills, approval commands
- Updated: wiki/index.md (67 pages)

**2026-04-08 | wiki | Created hermes-agent-setup.md + operational/ directory + artifacts/**
- Created: wiki/entities/hermes-agent-setup.md — personal hermes config, provider setup, gateway config, Telegram image pipeline
- Created: wiki/sources/operational/ — directory for session logs, incident notes, debug artifacts
- Created: wiki/artifacts/ — image descriptions from Telegram/CLI (vision-analyze pipeline)
- Updated: wiki/index.md (63 pages, artifacts section added)
- Note: multi-agent Discord architecture documented as abandoned

**2026-04-08 | skill | Created docs-vs-code-discrepancy-scan + patched ultraplan**
- Created: ~/.hermes/skills/software-development/docs-vs-code-discrepancy-scan/SKILL.md (5-phase methodology: extract claims → scan evidence → cross-reference matrix → severity → resolution)
- Patched: ultraplan skill with execution lessons (delegate failures, iterative deepening, ground truth sources)
- Inventory: updated (25 dirs, ~85 skills)

**2026-04-08 | session-close | End of session — session file updated**
- Session: 2026-04-08.md rewritten with full session summary
- Memory: codebase entry updated with regional CRUD + Docker state
- Wiki: 61 pages total
- Commits today: 12 (thesis ingestion, discrepancy analysis, codebase metrics, Docker lockdown, CRUD, security fixes, tests, wiki logging)

**2026-04-08 | audit | Regional Encoder CRUD + backend security scan**
- Created: wiki/sources/software-dev/wims-bfp-regional-encoder-audit-2026-04-08.md
- CRUD: POST/PUT/DELETE routes added to regional.py (8 total routes)
- Security: 4 error message leakage fixes (str(e) -> generic messages + logger.exception)
- CVE check: all packages at safe versions
- Tests: 10/10 passing
- Index: updated (total pages: 61)

**2026-04-08 | ingest | WIMS-BFP codebase metrics — refactoring targets identified**
- Created: wiki/sources/software-dev/wims-bfp-codebase-metrics.md
- 118 code files, 19,879 lines (Python 45%, TSX 37%, TS 10%, SQL 8%)
- CRITICAL: regional.py (1,876 lines), 01_wims_initial.sql (1,468 lines)
- HIGH: WildlandAforManualForm (927), IncidentForm (772), api.ts (507)
- Refactoring plan: Phase 1 backend (2 files → 10), Phase 2 frontend (4 files → 12)
- Index: updated (total pages: 60)

**2026-04-08 | ingest | WIMS-BFP thesis revision log — 51 changes documented**
- Created: wiki/sources/software-dev/wims-bfp-thesis-revisions-2026-04-08.md
- Ch1: 7 changes (microservices→containerized, Dexie→idb, hybrid→AES-256-GCM)
- Ch2: 6 changes (offline claims toned down, hybrid→AES-256-GCM)
- Ch3: 38 changes (Table 21 rewrite, Dexie→idb, X25519 removed, OpenBao/Instructor/PyNaCl/TanStack removed, Llama.cpp→Ollama)
- All 10 discrepancies resolved. No code changes needed.
- Index: updated (total pages: 59)

**2026-04-08 | ingest | WIMS-BFP Thesis Chapters 1-3 + Abstract (55 files → 8 wiki pages)**
- Created: wiki/sources/software-dev/wims-bfp-ch1-introduction.md (9 files, purpose/context/objectives/scope/CIA/STRIDE/definitions)
- Created: wiki/sources/software-dev/wims-bfp-ch2-rrl.md (5 files, theoretical framework/4 paradigms, related literature/6 themes, related studies/6 comparative, synthesis/3 gaps)
- Created: wiki/sources/software-dev/wims-bfp-ch3a-research-design.md (8 files, hybrid research design, FR/NFR/security requirements, V-model)
- Created: wiki/sources/software-dev/wims-bfp-ch3b-architecture.md (10 files, 3-layer architecture, ER diagram, AI 4-stage pipeline, deployment)
- Created: wiki/sources/software-dev/wims-bfp-ch3c-security-tools.md (7 files, security practices/hybrid encryption, FARM stack, testing tools)
- Created: wiki/sources/software-dev/wims-bfp-ch3d-testing-data.md (13 files, testing methodologies, ISO 25010 evaluation, data gathering, ethics/RA 10173)
- Created: wiki/sources/software-dev/wims-bfp-abstract.md (full abstract)
- Created: wiki/sources/software-dev/wims-bfp-knowledge-graph.md (architecture alignment, health report findings)
- Created: wiki/analyses/wims-bfp-thesis-codebase-gaps.md (3 CRITICAL, 2 HIGH discrepancies: offline PWA not implemented, model mismatch, microservices claim)
- Index: updated (total pages: 58)

**2026-04-08 | skill | Created ultraplan skill**
- Created: ~/.hermes/skills/software-development/ultraplan/SKILL.md
- 4-phase workflow: AUDIT (scan codebase) → ANALYZE (gaps/risks) → PLAN (bite-sized tasks) → REVIEW (security gate)
- WIMS-BFP specific: RLS, PostGIS, DMZ, Celery RLS context, SRID 4326 checks

**2026-04-08 | ingest | PostGIS Secure Coding Practices + concept**
- Sources: wiki/sources/software-dev/postgis-secure-coding-practices.md (15-point audit checklist, CVE-2025-69662, spatial SQL injection, geometry validation, RLS integration)
- Concept: wiki/concepts/postgis-security-wims-bfp.md (5 security layers, ZTA mapping, critical rules)
- MOC: updated cybersecurity MOC
- Index: updated (total pages: 50)

**2026-04-08 | ingest | Hermes skills inventory documented**
- Created: wiki/sources/software-dev/hermes-skills-inventory.md (23 dirs, ~83 skills, categorized by priority tier)
- Index: updated (total pages: 48)

**2026-04-08 | postmortem | 4-agent pipeline failure documented**
- Created: wiki/analyses/4-agent-pipeline-postmortem.md (full postmortem: 5 root causes, lessons learned, next steps)
- Updated: wiki/entities/hermes-agent.md (WIMS-BFP section now references failure, not proposal)
- Index: updated (total pages: 47)

**2026-04-08 | step-1 | Orchestrator config → Nous Portal (OAuth)**
- Changed: provider: nous, default: mimo-v2-pro
- Auth: hermes login --provider nous

**2026-04-08 | ingest | FastAPI + Celery/Redis Security → 3 sources + 1 concept**
- Sources: wiki/sources/software-dev/fastapi-security-best-practices.md, wiki/sources/software-dev/fastapi-cves-2025-2026.md, wiki/sources/software-dev/celery-redis-security.md
- Concept: wiki/concepts/fastapi-security-wims-bfp.md (8-layer security stack, complete backend checklist)
- MOC: updated cybersecurity MOC with FastAPI/Celery section
- Index: updated (total pages: 45)

**2026-04-08 | ingest | Keycloak + FastAPI Auth Security → 2 sources + 1 concept**
- Sources: wiki/sources/software-dev/keycloak-production-security.md, wiki/sources/software-dev/fastapi-keycloak-jwt-rbac.md
- Concept: wiki/concepts/keycloak-fastapi-security-wims-bfp.md (auth flow, ZTA mapping, complete auth audit checklist)
- MOC: updated cybersecurity MOC with Keycloak section
- Index: updated (total pages: 41)

**2026-04-08 | ingest | Docker Security → 2 sources + 1 concept**
- Sources: wiki/sources/software-dev/docker-security-best-practices.md, wiki/sources/software-dev/docker-cves-2025-2026.md
- Concept: wiki/concepts/docker-security-wims-bfp.md (Compose template, runc CVEs, ZTA mapping, audit checklist)
- MOC: updated cybersecurity MOC with Docker section
- Index: updated (total pages: 38)

**2026-04-08 | ingest | PostgreSQL Security → 3 sources + 1 concept**
- Sources: wiki/sources/software-dev/postgresql-security-best-practices.md, wiki/sources/software-dev/postgresql-rls-limitations.md, wiki/sources/software-dev/postgresql-cves-2025-2026.md
- Concept: wiki/concepts/postgresql-security-wims-bfp.md (RLS rules, NULL safety, CVE checklist, ZTA mapping)
- MOC: updated cybersecurity MOC with PostgreSQL security section
- Index: updated (total pages: 35)

**2026-04-08 | ingest | Secure Coding Practices → 3 sources + 1 concept (OWASP, CWE, code review)**
- Sources: wiki/sources/software-dev/owasp-top-10-2025.md, wiki/sources/software-dev/cwe-top-25-2025.md, wiki/sources/software-dev/owasp-secure-code-review.md
- Concept: wiki/concepts/secure-coding-practices.md (synthesis, WIMS-BFP checklist, cross-links to ZTA/CVEs)
- MOC: updated cybersecurity MOC with secure coding section
- Index: updated (total pages: 31)

**2026-04-08 | wiki | Cybersecurity MOC created + cross-links fixed**
- MOC: wiki/mocs/cybersecurity.md (CVE summary, ZTA reading path, WIMS-BFP relevance)
- Fixed 7 broken cross-references (concepts/threat-detection-pipeline, authentication-architecture, frontend-security → replaced with existing pages)
- Added bidirectional wikilinks between all 6 cybersecurity source pages + ZTA concept

**2026-04-08 | ingest | Zero Trust Architecture → 3 sources + 1 concept page**
- Sources: wiki/sources/cybersecurity/nist-sp-800-207-zero-trust-architecture.md, wiki/sources/cybersecurity/dod-zta-implementation-primer-2026.md, wiki/sources/cybersecurity/zero-trust-complete-guide-2026.md
- Concept: wiki/concepts/zero-trust-architecture.md (7 tenets, 7 pillars, WIMS-BFP alignment)
- Index: updated (total pages: 27)
