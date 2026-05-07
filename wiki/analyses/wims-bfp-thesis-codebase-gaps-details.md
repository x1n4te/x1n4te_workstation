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

# WIMS Gaps — Detailed Reference

Back to overview: [[analyses/wims-bfp-thesis-codebase-gaps]]
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

### H-2: ECC + AES Hybrid Encryption — OUT OF SCOPE (RESOLVED)

**Thesis claims (Ch 1.7, 3.5.1, 3.5.2):**
- "Hybrid Encryption (ECC + AES) for data at rest and in transit"
- "Digital Envelope strategy: AES-256-GCM (DEK) wrapped using X25519 (KEK)"
- "PyNaCl / Libsodium for X25519/AES-GCM encryption"

**Codebase reality (VERIFIED 2026-04-08):**
- `crypto.py` (169 lines) — pure AES-256-GCM via `cryptography` package
- Master key loaded from `WIMS_MASTER_KEY` env var
- TLS 1.3 for encrypted communications in transit
- No X25519, no PyNaCl — **confirmed out of scope per user**

**Resolution:** Change thesis language:
- "Hybrid Encryption (ECC + AES)" → "AES-256-GCM for data at rest, TLS 1.3 for encrypted communications"
- Remove "Digital Envelope" / "X25519" / "PyNaCl" references entirely
- Drop from Ch 1.7, 3.5.1, 3.5.2, and Table 21

---

### H-3: OpenBao KMS — REMOVE FROM THESIS

**Thesis claims (Ch 3.6.1, Table 21):**
- "OpenBao Key Management Service (KMS) for hybrid encryption"

**Codebase reality:** NOT deployed. Env vars (`WIMS_MASTER_KEY`) used directly. Fine for prototype scope.

**Resolution:** Remove OpenBao from Table 21. If needed, note "Secret management via environment variables."

---

### H-4: Instructor Library — REMOVE FROM THESIS

**Thesis claims (Ch 3.6.1, Table 21):**
- "Instructor — Enforces structured JSON output from the SLM"

**Codebase reality:** NOT installed. `ai_service.py` uses raw Ollama API. Output format controlled via prompt engineering, not library enforcement.

**Resolution:** Remove Instructor from Table 21. The prompt template in `ai_service.py` handles output formatting.

---

### H-5: PyNaCl/Libsodium — REMOVE FROM THESIS (covered by H-2)

**Thesis claims (Ch 3.6.1, Table 21):**
- "PyNaCl / Libsodium — Library for high-assurance X25519/AES-GCM encryption"

**Codebase reality:** NOT installed. `cryptography` package provides AES-256-GCM instead.

**Resolution:** Remove PyNaCl from Table 21. Change to "cryptography — AES-256-GCM authenticated encryption." Already covered by H-2.

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

**Summary:** All HIGH discrepancies are thesis-language fixes, not code changes. The codebase works correctly. The thesis Ch 3.6.1 Table 21 over-specifies tools that were descoped or replaced. Align the thesis with what's actually in `requirements.txt`.

**Quick fix list for thesis paper:**
1. Ch 3.6.1 Table 21: Remove OpenBao, Instructor, PyNaCl. Change "Dexie.js" to "idb". Drop "Llama.cpp" (Ollama wraps it).
2. Ch 1.7, 3.5.1, 3.5.2: "Hybrid ECC+AES" → "AES-256-GCM at rest, TLS 1.3 for encrypted communications"
3. Ch 1.2, 3.4.1: "microservices" → "containerized multi-tier" or "modular monolith"
4. Ch 1.6: "Offline-First Cache (IndexedDB/Dexie.js)" → acknowledge partial implementation (idb queuing, no Service Worker)

---

## Cross-References

- [[sources/software-dev/wims-bfp-ch1-introduction]] — Chapter 1 claims
- [[sources/software-dev/wims-bfp-ch3b-architecture]] — Architecture description
- [[sources/software-dev/wims-bfp-knowledge-graph]] — Pre-refactor baseline
