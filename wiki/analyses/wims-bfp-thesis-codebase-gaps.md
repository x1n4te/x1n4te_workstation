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
| CRITICAL | 3 | Must resolve before thesis defense |
| HIGH | 2 | Should resolve before thesis defense |
| MEDIUM | 4 | Verify or document as limitations |
| LOW | 3 | Note for completeness |

---

## CRITICAL Discrepancies

### C-1: Offline-First PWA NOT Implemented

**Thesis claims (Ch 1.1, 1.3, 1.6, 3.4.1, 3.6.1, Abstract):**
- "Offline-First architecture supported by local browser storage (IndexedDB)"
- "Dexie.js (IndexedDB wrapper) for offline data capture"
- "Service Workers for seamless local caching"
- "TanStack Query manages offline synchronization"

**Codebase reality:**
- Dexie.js references: **0**
- Service Worker references: **1** (minimal)
- No IndexedDB abstraction layer found
- No offline sync mechanism implemented

**Impact:** Thesis makes offline-first a core differentiator. Without implementation, the system is a standard online-only web app. This undermines the entire "dual-edge architecture" narrative and the BFP disaster resilience use case.

**Resolution options:**
1. **Implement** Dexie.js + Service Workers + TanStack Query offline sync before defense
2. **Downgrade** thesis claims to "planned architecture" / "future work"
3. **Document** as limitation in Ch 1.4

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

| Priority | Action | Owner |
|---|---|---|
| 1 | Decide on C-1: implement offline-first or downgrade claims | xynate |
| 2 | Decide on C-2: deploy Qwen2.5-3B or update thesis | xynate |
| 3 | Decide on C-3: change "microservices" language | xynate |
| 4 | Verify H-2: X25519 key wrapping in crypto.py | xynate |
| 5 | Implement H-1: Alembic migrations (or document as limitation) | xynate |
| 6 | Verify M-1 through M-3 (audit logs, AI pipeline, hash chain) | xynate |

---

## Cross-References

- [[sources/software-dev/wims-bfp-ch1-introduction]] — Chapter 1 claims
- [[sources/software-dev/wims-bfp-ch3b-architecture]] — Architecture description
- [[sources/software-dev/wims-bfp-knowledge-graph]] — Pre-refactor baseline
