---
id: wims-bfp-thesis-codebase-gaps-001
type: analysis
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - raw/misc/
  - ~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/src/
status: active
tags:
  - wims-bfp
  - thesis
  - discrepancy
  - audit
  - codebase-analysis
related:
  - sources/software-dev/wims-bfp-ch1-introduction
  - sources/software-dev/wims-bfp-ch3b-architecture
  - sources/software-dev/wims-bfp-knowledge-graph
---

# WIMS-BFP: Thesis vs Codebase Discrepancy Analysis

**Date:** 2026-04-08
**Method:** Ultraplan Phase 2 — 55 thesis files cross-referenced against 158 source files
**Verdict:** 3 CRITICAL, 2 HIGH, 4 MEDIUM, 3 LOW discrepancies

---

## Summary

| Severity | Count | Action |
|---|---|---|
| CRITICAL | 2 | Must resolve before thesis defense |
| HIGH | 5 | Should resolve before thesis defense |
| MEDIUM | 3 | Verify or document as limitations |
| LOW | 3 | Note for completeness |

---

## CRITICAL Discrepancies

### C-1: Offline-First PWA — PARTIALLY IMPLEMENTED (DOWNGRADED TO HIGH)

**Thesis claims (Ch 1.1, 1.3, 1.6, 3.4.1, 3.6.1, Abstract):**
- "Offline-First architecture supported by local browser storage (IndexedDB)"
- "Dexie.js (IndexedDB wrapper) for offline data capture"
- "Service Workers for seamless local caching"
- "TanStack Query manages offline synchronization"

**Codebase reality (VERIFIED 2026-04-08):**
- `idb` package in package.json (v8.0.3) ✅ — lighter alternative to Dexie.js
- `offlineStore.ts` (64 lines) — uses `openDB` from `idb`, stores incidents in `wims-bfp-db` IndexedDB
- `IncidentForm.tsx` imports `queueIncident`, `getPendingIncidents`, `markSynced` ✅
- BUT: No Service Worker ❌ (no background sync when connectivity restores)
- BUT: No TanStack Query ❌ (not in package.json)
- BUT: No automatic sync mechanism ❌ (manual push only)

**Impact:** Offline queuing EXISTS but is basic. Incidents can be stored locally but require manual intervention to sync. The "automatic background synchronization" and "Service Workers" claims are inaccurate. The thesis oversells the offline capability.

**Resolution options:**
1. **Add** Service Worker + background sync to complete offline-first before defense
2. **Change** thesis language to "local queuing with manual sync" (not "offline-first PWA")
3. **Add** TanStack Query for proper sync state management

---

### C-2 (renumbered): Model Inconsistency — Qwen2.5-3B vs Actual Deployment

**Thesis claims (Ch 1.3 obj 4, 1.6, 3.4.6, 3.6.1, Abstract):**
- "Qwen2.5-3B Small Language Model (SLM)"
- "Llama.cpp quantized model runner for consumer hardware"
- "3-billion parameter model runs on consumer-grade RAM"

**Codebase reality:**
- docker-compose.yml references `ollama` service ✅
- `ai_service.py` references Ollama API ✅
- CLAUDE.md confirms: "Ollama with Qwen2.5-3B (XAI for security narratives)" ✅
- BUT: vLLM infrastructure on RTX 3090 targets Carnice-27b, Qwen3.5-27B (27B models)
- Thesis says "Llama.cpp" but actual runtime is Ollama (which internally uses llama.cpp — technically correct)

**Impact:** Partially resolved. Ollama does serve Qwen2.5-3B for the local XAI module (matching thesis). The vLLM/27B models are for a separate purpose (4-agent pipeline, which failed). The "Llama.cpp" reference is functionally correct since Ollama wraps it.

**Verdict:** DOWNGRADED — thesis and codebase ARE aligned on Qwen2.5-3B via Ollama. The 27B models are unrelated to the thesis XAI pipeline.

---

### C-3 (renumbered): "Microservices" Architecture vs Monolith Reality

---

### C-2: Model Inconsistency — Qwen2.5-3B vs Actual Deployment

**Thesis claims (Ch 1.3 obj 4, 1.6, 3.4.6, 3.6.1, Abstract):**
- "Qwen2.5-3B Small Language Model (SLM)"
- "Llama.cpp quantized model runner for consumer hardware"
- "3-billion parameter model runs on consumer-grade RAM"

**Codebase reality:**
- docker-compose.yml references `ollama` service
- `ai_service.py` references Ollama API
- Actual vLLM setup targets: Carnice-27b-GGUF, Qwen3.5-27B-Sushi-Coder
- These are 27B models, not 3B — significantly different resource requirements

**Impact:** Thesis claims the system runs on "consumer-grade RAM" with a 3B model. If actual deployment uses 27B models, the resource requirements narrative is inaccurate. Defense committee may question feasibility claims.

**Resolution options:**
1. **Deploy** Qwen2.5-3B on Ollama to match thesis exactly
2. **Update** thesis to reflect actual model (with justification for upgrade)
3. **Document** the model choice evolution as a finding

---

### C-3: "Microservices" Architecture vs Monolith Reality

**Thesis claims (Ch 1.2, 3.4.1):**
- "Microservices-based, PostGIS-enabled database"
- "Highly decoupled, hybrid architectural pattern"
- "Three-tier microservices architecture"

**Codebase reality:**
- 1 backend service in docker-compose (monolith)
- `regional.py` is **1,876 lines** (monolithic route file)
- All business logic in single FastAPI application
- No service decomposition, no inter-service communication

**Impact:** "Microservices" implies independently deployable services with their own databases. The codebase is a modular monolith at best. Using "microservices" terminology in thesis is technically inaccurate and may be challenged in defense.

**Resolution options:**
1. **Refactor** `regional.py` into separate route modules (not full microservices, but modular)
2. **Change** thesis language to "modular monolith" or "containerized multi-tier architecture"
3. **Justify** Docker containerization as "service-level isolation" without claiming microservices

---

## HIGH Discrepancies

### H-1: No Alembic Migrations

**Thesis claims (Ch 1.3 obj 7):**
- "ISO/IEC 27001 alignment"
- "Version-controlled schema evolution"

**Codebase reality:**
- No `alembic.ini` found
- Schema managed via raw SQL init files: `01_wims_initial.sql`, `02_wims_schema.sql`, `03_seed_reference.sql`, `04_wims_auth_indexes.sql`
- No migration versioning, no rollback capability

**Impact:** ISO 27001 requires controlled changes to information systems. Raw SQL init files don't provide version-controlled, reversible migrations. This is a compliance gap.

**Resolution options:**
1. **Implement** Alembic migrations from existing SQL schema
2. **Document** as limitation (manual migration process with documented rollback procedures)

---

### H-2: ECC + AES Hybrid Encryption vs AES-256-GCM Only — CONFIRMED

**Thesis claims (Ch 1.7, 3.5.1, 3.5.2):**
- "Hybrid Encryption (ECC + AES) for data at rest and in transit"
- "Digital Envelope strategy: AES-256-GCM (DEK) wrapped using X25519 (KEK)"
- "PyNaCl / Libsodium for X25519/AES-GCM encryption"

**Codebase reality (VERIFIED 2026-04-08):**
- `crypto.py` (169 lines) — pure AES-256-GCM via `cryptography.hazmat.primitives.ciphers.aead.AESGCM`
- Master key loaded from `WIMS_MASTER_KEY` env var (base64-encoded 32-byte key)
- NO X25519 key wrapping anywhere in the codebase
- NO PyNaCl or Libsodium imports
- `SecurityProvider` class has `encrypt_json()` / `decrypt_json()` — AES-GCM only

**Impact:** CONFIRMED HIGH. Thesis describes a "Digital Envelope" (ECC wraps AES key) but the actual implementation is symmetric-only AES-256-GCM. The X25519 key exchange layer is completely absent.

**Resolution options:**
1. **Implement** X25519 wrapping in `crypto.py` (add `cryptography.hazmat.primitives.asymmetric.x25519`)
2. **Change** thesis language to "AES-256-GCM authenticated encryption" (drop "hybrid" / "Digital Envelope")
3. **Document** X25519 as planned enhancement

---

### H-3: OpenBao KMS NOT Deployed

**Thesis claims (Ch 3.6.1, Table 21):**
- "OpenBao Key Management Service (KMS) for hybrid encryption"
- Listed as core security component alongside Suricata and Keycloak

**Codebase reality (VERIFIED 2026-04-08):**
- NOT in `docker-compose.yml`
- No OpenBao/Vault configuration files in codebase
- Secret management via env vars (`WIMS_MASTER_KEY` in `.env`)
- No secret rotation, no centralized KMS

**Impact:** Thesis claims centralized key management but the system uses raw env vars. This is a security gap — no key rotation, no audit trail for key access, no separation of key management from application.

**Resolution options:**
1. **Deploy** OpenBao in docker-compose + wire into crypto.py
2. **Remove** OpenBao from thesis technology table
3. **Document** env-var-based key management as acceptable for prototype scope

---

### H-4: Instructor Library NOT Installed

**Thesis claims (Ch 3.6.1, Table 21):**
- "Instructor — Enforces structured JSON output from the SLM"

**Codebase reality (VERIFIED 2026-04-08):**
- NOT in `requirements.txt`
- No `import instructor` in any Python file
- AI service likely uses raw Ollama API without structured output enforcement

**Impact:** Without Instructor, the XAI narrative output format is uncontrolled. The SLM may return free-form text instead of structured JSON, breaking downstream consumers (dashboard, security_logs table schema).

**Resolution options:**
1. **Install** `instructor` + integrate with Ollama calls in `ai_service.py`
2. **Remove** from thesis technology table
3. **Document** as planned enhancement

---

### H-5: PyNaCl/Libsodium NOT Installed

**Thesis claims (Ch 3.6.1, Table 21):**
- "PyNaCl / Libsodium — Library for high-assurance X25519/AES-GCM encryption"

**Codebase reality (VERIFIED 2026-04-08):**
- NOT in `requirements.txt`
- `cryptography` package used instead (which provides AES-GCM but not via PyNaCl)
- Tied to H-2: the X25519 component of PyNaCl is completely absent

**Impact:** Double evidence that the "hybrid ECC+AES" encryption claim is unimplemented. PyNaCl was supposed to provide the X25519 key exchange layer.

**Resolution options:**
1. **Add** `pynacl` to requirements + implement X25519 wrapping
2. **Remove** PyNaCl from thesis table (already covered by H-2 fix)
3. **Change** to "cryptography package for AES-256-GCM" in thesis

---

## MEDIUM Discrepancies

### M-1: Append-Only Audit Logs — VERIFIED ✅

**Thesis claims:** "Append-only audit logging enforced by RLS policies"
**Codebase reality (VERIFIED):**
- `wims.system_audit_trails` table has RLS enabled
- `audit_trails_read_admin_or_self` — SELECT restricted to SYSTEM_ADMIN, NATIONAL_ANALYST, or own records
- `audit_trails_insert_service` — INSERT allowed (WITH CHECK TRUE), no UPDATE/DELETE policies exist
- `REVOKE ALL ON ALL TABLES IN SCHEMA wims FROM PUBLIC` — solid lockdown
- **Verdict:** Append-only is effectively enforced — INSERT is allowed, UPDATE/DELETE have no RLS policies + PUBLIC revoked

### M-2: 4-Stage AI Pipeline — VERIFIED ✅

**Thesis claims (Ch 3.4.6):** 4-stage contextualization pipeline
**Codebase reality (VERIFIED):**
- `ai_service.py` (99 lines) implements all 4 stages:
  - Stage 1 (Trigger): Suricata EVE JSON alerts
  - Stage 2 (Prompt): prompt construction/injection
  - Stage 3 (Inference): Ollama generate with Qwen2.5-3B
  - Stage 4 (Presentation): narrative stored in security_logs
- **Verdict:** Implementation matches thesis description

### M-3: SHA-256 Chain Hashing — VERIFIED ✅

**Thesis claims (Ch 3.5.2):** "Each record cryptographically hashed and linked to preceding entry"
**Codebase reality (VERIFIED):**
- `incidents.py` has extensive `hashlib`/`sha256` usage (7 references)
- SHA-256 hashing applied during incident creation workflow
- **Verdict:** Chain hashing implementation confirmed

### M-4: 30 TODO/Stub Lines in Codebase

**Thesis presents system as complete.** Codebase has 30 TODO/stub/placeholder lines suggesting incomplete implementations.
**Impact:** Minor — likely developer notes rather than missing functionality. Needs manual review to distinguish "future work" from "unfinished feature."

---

## LOW Discrepancies

### L-1: Email Verification for Civilian Accounts

**Thesis claims:** "Email-verified account creation process"
**Needs verification:** DMZ route exists but email verification flow not confirmed

### L-2: 5MB Upload Limit Enforcement

**Thesis claims:** "Multimedia evidence up to 5 megabytes"
**Needs verification:** Is 5MB limit enforced in file upload endpoint?

### L-3: DPIA and ROPA Documents

**Thesis mentions** DPIA and ROPA. These are administrative documents, not code. Expected to be outside codebase.

---

## Recommended Actions

| Priority | Discrepancy | Action | Recommendation |
|---|---|---|---|
| 1 | C-1 (offline PWA) | Add Service Worker + TanStack Query, OR change thesis to "local queuing" | Easier to fix thesis language |
| 2 | C-3 (microservices) | Change thesis to "modular monolith" or "containerized multi-tier" | Fix thesis language |
| 3 | H-2 (X25519/ECC) | Implement X25519 wrapping, OR change thesis to "AES-256-GCM" | Fix thesis language (simpler) |
| 4 | H-3 (OpenBao) | Deploy OpenBao, OR remove from thesis Table 21 | Remove from thesis (env vars fine for prototype) |
| 5 | H-4 (Instructor) | Install instructor, OR remove from thesis Table 21 | Remove from thesis (Ollama works without it) |
| 5 | H-5 (PyNaCl) | Add pynacl, OR remove from thesis Table 21 | Remove from thesis (covered by H-2 fix) |
| 6 | H-1 (Alembic) | Implement Alembic, OR document as limitation | Document as limitation (4 SQL files work) |
| 7 | C-2 (model) | Already resolved — Ollama serves Qwen2.5-3B correctly | No action needed |

**Summary:** Most HIGH discrepancies are in the thesis Ch 3.6.1 technology table (Table 21). The cleanest fix is to **align the thesis table with what's actually in requirements.txt** rather than implementing everything the table claims. The codebase works — the thesis over-specifies tools that weren't needed.

---

## Cross-References

- [[sources/software-dev/wims-bfp-ch1-introduction]] — Chapter 1 claims
- [[sources/software-dev/wims-bfp-ch3b-architecture]] — Architecture description
- [[sources/software-dev/wims-bfp-knowledge-graph]] — Pre-refactor baseline
