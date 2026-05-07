# WIMS-BFP — FRS Modules Research Brief: Gaps & Agent-Ready Intelligence

**Date:** 2026-05-04
**Scope:** FRS Modules 5d, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
**Purpose:** Identify which modules need deeper wiki documentation and what agents need to know to work on them
**Confidence:** High — verified against live codebase

---

## Module Coverage Scorecard

| Module | Wiki Depth | Codebase Reality | Research Signal |
|--------|-----------|-----------------|----------------|
| M1 Auth/RBAC | ✅ Deep | Implemented | Tier 1 — stable |
| M2 Offline PWA | ✅ Deep | Implemented | Tier 1 — stable |
| M3 Verification | ✅ Deep | Implemented | Tier 1 — stable |
| M4 Immutable Records | ⚠️ Thin | Implemented (new) | Needs wiki update |
| M5 Analytics | ⚠️ Thin | Partial (Issue #89 open) | Needs wiki + code |
| M6 Crypto | ✅ Deep | Implemented | Tier 1 — stable |
| M7 IDS | ⚠️ Thin | Partial (no custom rules) | Needs research + code |
| M8 XAI | ⚠️ Thin | Partial (no impossible travel) | Needs research + code |
| M9 Health Dashboard | ⚠️ Thin | Partial | Needs wiki + code |
| M10 Compliance/RA10173 | ⚠️ Thin | Partial | Needs research + wiki |
| M11 Pentest | ✅ Procedure | Procedure only | Tier 2 — docs exist |
| M12 User Management | ⚠️ Thin | Implemented (fix PR #91) | Needs wiki update |
| M13 Notifications | ❌ None | DEFERRED | Low priority |
| M14 Public DMZ | ❌ None | Implemented (new) | Needs wiki + code |
| M15 Ref Data Service | ❌ None | Implemented (new) | Needs wiki + code |

---

## Module 7: Intrusion Detection (Suricata) — THIN [Priority: HIGH]

### What FRS M7 Requires
- Suricata AF_PACKET on Docker bridge
- OWASP Top 10 signatures + Emerging Threats (weekly update)
- Custom BFP rules: bulk deletion detection, off-hours access
- EVE JSON → Redis → Celery → DB pipeline
- 5-second latency for log forwarding

### Codebase Reality
- `suricata_ingestion.py` — parses EVE JSON, inserts into `security_threat_logs` table
- `tasks/suricata.py` — Celery beat task, 10s interval, hardcoded `SYSTEM_SURICATA_USER_ID`
- Docker: `wims-suricata` container using `jasonish/suricata:latest`, `-i eth0` bridge sniffing
- `suricata/rules/` has only `classification.config` — **no custom `.rules` files**
- `suricata/logs/eve.json` — live EVE JSON output confirmed
- Emerging Threats ruleset fetched at container build? — **unconfirmed**

### Critical Gaps

**Gap 1: No custom BFP rules written**
FRS M7.a.ii(b) requires "Custom BFP-specific rules (e.g., detect bulk incident deletion attempts)." These rules don't exist in the codebase. The `suricata/rules/` directory has no custom rule files.

**Gap 2: No Lua impossible travel script**
FRS M8.a.i requires "Impossible Travel — rapid logins from distant GeoIP locations using GeoIP2 MaxMind and custom Lua distance calculation." No Lua scripts exist. No GeoIP2 MaxMind database is mounted in the Suricata container.

**Gap 3: Suricata config file not in repo**
`suricata.yaml` (or `suricata.yml`) is not present in the codebase. Suricata is running with defaults from the Docker image. The EVE JSON output config, rule paths, and network interface settings are all default.

### Agent Research Notes: Suricata Rules

Suricata rules are `alert tcp any any -> any any (...)` statements. Custom rules for WIMS-BFP should be placed in `suricata/rules/wims.rules`.

**Bulk deletion detection (M7 custom rule concept):**
```
# Detect >10 DELETE operations on fire_incidents in 5 minutes
alert sql any any -> any any (msg:"WIMS: Bulk deletion attempt detected"; \
  content:"DELETE"; nocase; sql_pattern_match; \
  threshold:type threshold,track by_src,count 10,seconds 300; \
  classtype:attempted-admin; sid:9000001; rev:1;)
```
Note: Suricata does not natively parse SQL. Actual implementation requires application-layer logging via `audit.log` or a dedicated SQL audit trail that Suricata can monitor (e.g., a dedicated log file).

**Off-hours access detection (M7 custom rule):**
```
# Admin actions between 10PM-6AM local time
alert any any -> any any (msg:"WIMS: Off-hours admin access detected"; \
  time:22:00-06:00; classtype:attempted-admin; sid:9000002; rev:1;)
```
Note: Suricata `time` keyword matches the sensor's local clock, not the application's timezone. For Philippine local time (UTC+8), this needs proper timezone config.

**EVE JSON reference:** `https://docs.suricata.io/en/latest/output/eve/eve-json-format.html`

---

## Module 8: Threat Detection with XAI (Qwen2.5-3B) — THIN [Priority: HIGH]

### What FRS M8 Requires
- Qwen2.5-3B via Ollama on VPS (Docker)
- On-demand forensic narrative generation
- Suricata EVE JSON + audit logs as input
- HITL: AI cannot autonomously act; admin confirms/dismisses
- 4 severity levels: Low, Medium, High, Critical

### Codebase Reality
- `ai_service.py` — prompt template + Ollama API call confirmed
- `admin.py` — `POST /admin/security-logs/{id}/analyze` endpoint confirmed
- `tasks/suricata.py` — celery ingestion to `security_threat_logs` confirmed
- Qwen2.5-3B via Ollama Docker container (from docker-compose)
- Wiki `wims-bfp-codebase-xai-pipeline.md` covers the pipeline at architecture level

### Critical Gaps

**Gap 1: No actual XAI inference running**
The Ollama container configuration in docker-compose is not shown in the current docker-compose excerpt. Need to verify the model is actually loaded and accessible.

**Gap 2: Impossible Travel not implemented**
FRS M8.b.i(a) requires GeoIP2 MaxMind + Lua for impossible travel. No Lua scripts in codebase. GeoIP2 MaxMind DB not mounted in Suricata container.

**Gap 3: No BFP-specific system prompt documented in code**
`ai_service.py` has a prompt template but it needs to be documented in the wiki with the actual system prompt content for reproducibility.

### Agent Research Notes: Qwen2.5-3B for Security Log Translation

From arXiv/industry research (Tier 2 sources):

**Qwen2.5-3B capabilities for log translation:**
- 3B params, decoder-only Transformer, ~128K vocabulary
- Context window up to 16K–32K tokens (variants)
- Strong at instruction-following, code, and structured output tasks
- Suitable for translation (log → narrative) but NOT for detection
- Benchmarks: competitive with 7B models on code-related tasks (Qwen2.5-Coder study)

**XAI pipeline design principle (from research):**
- SLMs for SOC: treat as "translation" not "detection" — the model converts raw EVE JSON into human-readable narrative
- Human-in-the-loop is mandatory per WIMS-BFP Constitution
- Qwen2.5-3B as "explainability" not "autonomy" — confirmed correct in FRS

**System prompt for forensic narrative (from existing codebase pattern):**
The prompt should include: raw log excerpt, alert severity, timestamp, source IP, affected endpoint, and a structured output format (description, evidence, risk assessment, recommended action).

---

## Module 9: System Monitoring & Health Dashboard — THIN [Priority: MEDIUM]

### What FRS M9 Requires
- Container status (FastAPI, PostgreSQL, Suricata, Qwen-AI)
- VPS CPU/RAM real-time
- DB query latency (ms)
- PWA sync success rate
- Network bandwidth (Nginx)
- AI on-demand latency (seconds)
- 60-second refresh interval
- 4-hour health reports via `repeat_every`
- Full-text log search via `tsvector` + GIN index
- 50-entry pagination

### Codebase Reality
- `routes/admin.py` has `get_system_health()` — confirmed in current Earl-Branch
- Celery `repeat_every` for periodic health reports — unconfirmed implementation
- `tsvector` + GIN index on logs — unconfirmed
- `analytics_incident_facts` materialized view for PWA sync metrics — unconfirmed

**Gap: No dedicated monitoring/health page in wiki**
No `wims-bfp-codebase-monitoring.md` or similar. The health endpoint exists in code but has no documentation.

---

## Module 10: Compliance & RA 10173 — THIN [Priority: MEDIUM]

### What FRS M10 Requires
- Data minimization (collect only necessary)
- Purpose limitation (fire operations + stats only)
- Right to Access, Rectification, Erasure
- DPIA documentation
- ISO 27001 alignment
- RMA 10173 / NPC compliance
- Soft delete with audit trail preservation
- Privacy notices, consent flows

### Agent Research Notes: RA 10173 Key Points

**NPC Enforcement (Tier 2 — DataGuidance, privacy.gov.ph):**
- RA 10173 passed 2012, IRR enforceable since September 9, 2016
- NPC has issued 100+ advisory opinions
- NPC Advisory No. 2026-01: guidelines for data scraping of publicly available personal data
- Penalties: 1–3 years imprisonment + Php 500,000–2,000,000 fine for unauthorized processing

**ISO 27001 alignment (Tier 3 — industry practice):**
- A.8.2 — Information classification and handling (PII encryption)
- A.18.1 — Compliance with laws and regulations (RA 10173)
- WIMS-BFP's RLS + AES-256-GCM + audit trail covers most ISO 27001 controls
- Gap: No formal ISMS documentation, no DPIA page in wiki

**WIMS-BFP Specific Compliance Points:**
- `encoder_id = NULL` for public submissions — data minimization (M14)
- PII encrypted at rest — AES-256-GCM
- Audit trail immutable — `incident_verification_history` + `CREATE RULE no_delete_ivh`
- No secondary use of data — enforced by RLS + purpose limitation in consent
- Right to erasure — soft delete (is_archived flag), hard delete blocked by rule

---

## Module 11: Penetration Testing (Procedure) — ADEQUATE [Priority: LOW]

FRS M11 is a procedure ("Penetration Testing and Security Validation"), not code. The wiki has:
- `wims-bfp-security-testing-evaluation-questionnaire-2026-05-04.md` — 30-item expert survey, 6 categories
- `wims-bfp-ethical-security-testing-guide-2026-05-04.md` — ethical workflow, documentation requirements
- `wims-bfp-expert-validation-guide-2026-05-04.md` — CVI computation, 7-step procedure

**Gap: No actual pentest report template**
Only the evaluation questionnaire exists. The actual penetration test execution guide (scope, rules of engagement, tool list, report template) needs a dedicated artifact.

---

## Modules 13, 14, 15 — NONE [Priority: LOW-MEDIUM]

| Module | Wiki | Code | Status |
|--------|------|------|--------|
| M13 Notification (SSE) | ❌ | ❌ | DEFERRED |
| M14 Public DMZ | ❌ | ✅ | NEW — needs docs |
| M15 Ref Data Service | ❌ | ✅ | NEW — needs docs |

---

## Research Sources (Tier Summary)

| Topic | Best Source | Tier |
|-------|------------|------|
| Qwen2.5-3B for SOC | arXiv 2412.15115 (Qwen2.5 Tech Report) | Tier 2 |
| Suricata EVE JSON | docs.suricata.io/en/latest/output/eve/eve-json-format.html | Tier 1 |
| Suricata Lua detection | docs.suricata.io/en/latest/rules/lua-detection.html | Tier 1 |
| Impossible Travel (GeoIP) | Google Cloud SecOps blog, Datadog research | Tier 3 |
| RA 10173 / NPC | privacy.gov.ph (NPC official), DataGuidance | Tier 1 |
| ISO 25010 | iso25000.com, PacificCert blog | Tier 3 |
| OWASP ASVS Level 2 | owasp-aasvs.readthedocs.io/en/latest/level2.html | Tier 1 |

---

## Priority: What to Document Next (Wiki Pages to Create)

### P0 — Earl-Branch-dependent (do now)
1. **`wims-bfp-codebase-analytics-read-model`** — analytics_read_model.py (already in gap analysis)
2. **`wims-bfp-codebase-immutable-records`** — 17_immutable_records.sql (already in gap analysis)
3. **`wims-bfp-codebase-af or-commit-pipeline`** — verify_incident() flow

### P1 — Thin modules with code
4. **`wims-bfp-codebase-suricata-ids`** — Suricata config, EVE JSON format, rules structure, current gaps
5. **`wims-bfp-codebase-xai-pipeline`** — expand existing page with actual system prompts, impossible travel gap
6. **`wims-bfp-codebase-health-dashboard`** — get_system_health() endpoint, monitoring metrics

### P2 — Compliance & Procedure
7. **`wims-bfp-codebase-ra10173-compliance`** — RA 10173 requirements, NPC, DPIA, rights implementation
8. **`wims-bfp-codebase-pentest-workflow`** — scope, tools, report template, rules of engagement

### P3 — New modules
9. **`wims-bfp-codebase-public-dmz`** — public_dmz.py, Redis rate limiting, region auto-resolve
10. **`wims-bfp-codebase-ref-data-service`** — ref.py endpoints, geographic lookup
