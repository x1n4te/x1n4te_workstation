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

## Related Sections
*Detailed content split into sub-pages for readability. See [[analyses/wims-bfp-thesis-codebase-gaps-details]] for the full reference.*

---

*This page is scannable in 30 seconds. Full reference content moved to sub-pages.*
