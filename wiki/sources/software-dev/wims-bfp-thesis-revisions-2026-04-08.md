---
id: wims-bfp-thesis-revisions-2026-04-08-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - raw/misc/ (original thesis — immutable, unmodified)
  - analyses/wims-bfp-thesis-codebase-gaps
status: active
tags:
  - wims-bfp
  - thesis
  - revisions
  - discrepancy-fixes
  - chapter-1
  - chapter-2
  - chapter-3
related:
  - analyses/wims-bfp-thesis-codebase-gaps
  - sources/software-dev/wims-bfp-ch1-introduction
  - sources/software-dev/wims-bfp-ch2-rrl
  - sources/software-dev/wims-bfp-ch3a-research-design
---

# WIMS-BFP Thesis Revisions — 2026-04-08

**Date:** 2026-04-08
**Scope:** Full thesis Ch 1–3 review against codebase
**Method:** Ultraplan (AUDIT → ANALYZE → PLAN → REVIEW)
**Verdict:** All discrepancies resolved via thesis-language edits. Codebase unchanged.

---

## Why These Revisions Were Needed

Ultraplan cross-referenced 55 thesis files against 158 codebase source files. Found 10 discrepancies where the thesis claimed technologies/patterns not present in `requirements.txt` or docker-compose.yml. Root cause: thesis Ch 3.6.1 Table 21 over-specified tools that were descoped during development.

**No code changes needed.** The codebase works correctly. The thesis needed to match reality.

---

## Revision Summary by Chapter

### Chapter 1 (7 changes across 5 subchapters)

| Subchapter | What Changed | Why |
|---|---|---|
| 1.2 Project Context | "microservices-based" → "containerized" (2 instances) | Codebase is a modular monolith, not microservices. `regional.py` is 1,876 lines. |
| 1.3 Objectives | Objective 1: "Service Workers for seamless local caching and automated background synchronization" → "IndexedDB for local caching and synchronization" | No Service Workers in codebase. `offlineStore.ts` uses `idb` (IndexedDB wrapper). |
| 1.5 Significance | "PWA Service Workers" → "IndexedDB caching" | Same reason — no Service Workers. |
| 1.6 Conceptual Framework | "Offline-First Cache (IndexedDB/Dexie.js)" → "local browser cache (IndexedDB)" | Dexie.js not in package.json. `idb` (v8.0.3) is used instead. |
| 1.7 Cybersecurity Principles | "hybrid encryption pipeline utilizing AES-256-GCM" → "AES-256-GCM authenticated encryption" | X25519 out of scope. Pure AES-256-GCM via `cryptography` package. |

**Subchapters unchanged:** 1.1, 1.4, 1.8

---

### Chapter 2 (6 changes across 2 subchapters)

| Subchapter | What Changed | Why |
|---|---|---|
| 2.3 Related Studies | "hybrid encryption" → "AES-256-GCM encryption" (Malanin comparison) | X25519 out of scope. |
| 2.3 Related Studies | Table 1: toned down offline claims in WIMS-BFP row | Partial implementation — idb queuing, no auto-sync. |
| 2.3 Related Studies | "offline-first PWA support" → "PWA-based data capture support" | Same reason. |
| 2.4 Synthesis | "Offline-First PWA design" → "PWA-based incident capture design" | Same reason. |
| 2.4 Synthesis | "offline-first incident monitoring system" → "incident monitoring system with offline data capture capability" | Honest framing of partial implementation. |

**Subchapters unchanged:** 2.0, 2.1, 2.2

---

### Chapter 3 (38 changes across 18 subchapters)

| Subchapter | Changes | Key Edits |
|---|---|---|
| 3.1 Research Design | 0 | Test objectives — describes what will be tested, not implementation claims. |
| 3.2.1 Functional Requirements | 3 | "offline-first capability" → "offline data capture capability"; Table 2 sync row toned down. |
| 3.2.2 Non-Functional Requirements | 2 | Drop "100%" sync claims; remove "digital envelopes" from Table 3. |
| 3.2.3 Security Requirements | 1 | Table 4: "SHA-256 hashing and digital signatures" → "SHA-256 hashing" (digital signatures not implemented). |
| 3.2.4 Feasibility Study | 7 | Table 5: "Service Workers and Dexie.js" → "IndexedDB"; Table 6: same; Table 7: remove Service Workers. |
| 3.3 Project Dev Model | 1 | "Dexie.js offline cache" → "IndexedDB offline cache" |
| 3.4.1 Architecture Overview | 2 | "offline-first PWA" → "PWA with local caching"; "Dexie.js" → "IndexedDB" |
| 3.4.3 Data Flow Diagram | 1 | "Instructor library" → "prompt engineering and schema validation" |
| 3.4.4 Use Case Diagram | 1 | "offline-first data operations" → "offline data operations" |
| 3.4.9 Comparative Design | 1 | Table 20: "Offline-first capabilities" → "Local caching capabilities" |
| 3.5.1 Security Practices | 1 | "Hybrid Encryption (ECC + AES)" → "AES-256-GCM authenticated encryption" |
| 3.5.2 Cybersecurity Measures | 3 | Remove Digital Envelope strategy; remove X25519 wrapping; "Offline-First PWA Architecture" → "PWA local caching architecture" |
| 3.6.1 Development Tools | 10 | **Table 21 rewrite:** Remove TanStack Query, Instructor, OpenBao, PyNaCl. Dexie.js → idb. Llama.cpp → Ollama. Body text: 4 edits. |
| 3.6.2 Security Testing Tools | 1 | "AES-256-GCM digital envelope" → "AES-256-GCM" |
| 3.6.3 AI Testing Tools | 5 | Llama.cpp → Ollama (3 instances). Remove Instructor. Fix copy-paste error (duplicate paragraph). Replace JSON Schema paragraph with Pydantic-focused content. |
| 3.7.1 Testing Methodologies | 2 | "Offline-First architecture" → "local data caching mechanism"; "Digital Envelope Inspection" → "Encryption Inspection" |
| 3.7.2 Evaluation Criteria | 1 | Table 23: add "TLS 1.3 in transit" to crypto row |
| 3.8.1 Data Sources | 1 | "Offline-First synchronization mechanism" → "data synchronization mechanism" |
| 3.8.2 Participants | 2 | "offline-first data entry" → "offline data entry" (2 instances) |

**Subchapters unchanged:** 3.0, 3.4.2, 3.4.5, 3.4.6, 3.4.7, 3.4.8, 3.7.3, 3.8.3, 3.8.4, 3.8.5, 3.9, 3.9.1

---

## Technology Table (Table 21) — Before vs After

| Category | Before | After | Reason |
|---|---|---|---|
| Local DB | IndexedDB + Dexie.js | IndexedDB + idb | Dexie.js not in package.json |
| State & Async | TanStack Query | *(removed)* | Not in package.json |
| AI & Intelligence | Llama.cpp | Ollama | Ollama wraps llama.cpp internally |
| AI & Intelligence | Instructor | *(removed)* | Not in requirements.txt |
| Security & IDS | OpenBao | *(removed)* | Not in docker-compose.yml |
| DevOps | PyNaCl / Libsodium | cryptography | Not in requirements.txt; AES-256-GCM via `cryptography` package |
| Encryption scope | ECC + AES (hybrid) | AES-256-GCM at rest, TLS 1.3 in transit | X25519 out of scope per user |

---

## What Was NOT Changed (Intentionally)

| Claim | Status | Why Keep |
|---|---|---|
| Qwen2.5-3B | ✅ Verified | CLAUDE.md confirms Ollama serves qwen2.5:3b locally |
| Suricata IDS | ✅ Verified | docker-compose.yml + celery_config.py + ai_service.py |
| Keycloak RBAC | ✅ Verified | auth.py, 36 files reference all 5 FRS roles |
| PostgreSQL RLS | ✅ Verified | 01_wims_initial.sql has policies |
| PostGIS spatial | ✅ Verified | SQL schema + 7 backend files |
| Celery + Redis | ✅ Verified | celery_config.py, docker-compose.yml |
| SHA-256 hashing | ✅ Verified | incidents.py has 7 hashlib/sha256 references |
| Nginx reverse proxy | ✅ Verified | nginx/nginx.conf exists |
| Docker containerization | ✅ Verified | docker-compose.yml with 10 services |
| IndexedDB | ✅ Verified | offlineStore.ts uses idb (v8.0.3) |
| "Offline-first" in test objectives | ✅ Kept | Research design describes what will be tested, not what's built |

---

## Discrepancy Resolution Summary

| ID | Discrepancy | Resolution | Target |
|---|---|---|---|
| C-1 | Offline-first PWA partial | Changed "offline-first" to "offline data capture" / "local caching" | Thesis (5 subchapters) |
| C-2 | Model mismatch | Resolved — Ollama serves Qwen2.5-3B correctly | None (false alarm) |
| C-3 | Microservices claim | "microservices" → "containerized" | Thesis Ch 1.2 |
| H-1 | No Alembic | Documented as limitation (out of scope) | No thesis change needed |
| H-2 | ECC+AES hybrid | "Hybrid Encryption" → "AES-256-GCM authenticated encryption" | Thesis Ch 1.7, 3.5.1, 3.5.2 |
| H-3 | OpenBao not deployed | Removed from Table 21 | Thesis Ch 3.6.1 |
| H-4 | Instructor not installed | Removed from Table 21, 3.4.3, 3.6.3 | Thesis Ch 3.4.3, 3.6.1, 3.6.3 |
| H-5 | PyNaCl not installed | Removed from Table 21 | Thesis Ch 3.6.1 |
| M-1 | Audit log RLS | Verified — no change needed | None |
| M-2 | AI pipeline 4 stages | Verified — no change needed | None |
| M-3 | SHA-256 chain hashing | Verified — no change needed | None |

---

## Cross-References

- [[analyses/wims-bfp-thesis-codebase-gaps]] — Full discrepancy analysis with evidence
- [[sources/software-dev/wims-bfp-ch1-introduction]] — Chapter 1 wiki ingestion
- [[sources/software-dev/wims-bfp-ch2-rrl]] — Chapter 2 wiki ingestion
- [[sources/software-dev/wims-bfp-ch3a-research-design]] — Chapter 3a wiki ingestion
- [[sources/software-dev/wims-bfp-ch3b-architecture]] — Chapter 3b wiki ingestion
- [[sources/software-dev/wims-bfp-ch3c-security-tools]] — Chapter 3c wiki ingestion
- [[sources/software-dev/wims-bfp-ch3d-testing-data]] — Chapter 3d wiki ingestion
