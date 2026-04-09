---
id: decisions-rationale-001
type: concept
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-07-08
stale_after: 2026-10-08
confidence: high
status: active
tags:
  - decisions
  - rationale
  - architecture
related:
  - entities/hermes-agent-setup
---

# Decisions & Rationale

Log of significant decisions and why they were made. Prevents second-guessing and provides context for future changes.

---

## Active Decisions

### Use MiMo v2 Pro as orchestrator (Nous Portal free-tier)
- **When:** Current
- **Why:** Free-tier, sufficient for tool-use orchestration, no cost, officially supported in v0.8.0
- **Tradeoff:** Not as capable as Claude/GPT for complex reasoning, but zero cost for daily use
- **Revisit when:** Need exceeds MiMo's capability, or free-tier changes

### Telegram as primary remote gateway (not Discord)
- **When:** Current
- **Why:** Already established, reliable, image sending works, mobile access
- **Tradeoff:** No rich embeds like Discord, but simpler and already working

### CLI as primary local interface (not Matrix, not Discord)
- **When:** Current
- **Why:** Fastest, zero overhead, no gateway indirection
- **Tradeoff:** No image paste on Linux (use Telegram for that)

### Abandon multi-agent Discord architecture
- **When:** Pre-2026-04-08
- **Why:** Didn't work as intended, complexity wasn't justified
- **Lesson:** Single-agent with good tools beats multi-agent with coordination overhead

### LLM Wiki vault pattern (Karpathy-style)
- **When:** Vault creation
- **Why:** Compounding knowledge base, interlinked, agent-maintained, grows richer over time
- **Tradeoff:** Requires discipline (session close, wiki sweep, frontmatter hygiene)

### raw/ is immutable (root-owned, chattr +i)
- **When:** Vault creation
- **Why:** Source of truth must never be corrupted. wipe-and-recompile.py can rebuild wiki/ from raw/, but only if raw/ is pristine.
- **Tradeoff:** Adding files requires sudo raw-ingest alias

### PyNaCl/Libsodium deprecated in WIMS-BFP
- **When:** Pre-2026-04-08
- **Why:** X25519 is deprecated for the project's use case
- **Action:** Do not reference as current in any documentation

### FARM stack for WIMS-BFP
- **When:** Thesis design phase
- **Why:** FastAPI async, React type safety, PostgreSQL reliability, Python ecosystem for AI integration
- **Tradeoff:** Not as battle-tested as Django for some patterns, but async-first advantage for the workload

---

## Pending Decisions

### Split regional.py (1,876 lines → 5 modules)
- **Status:** Deferred
- **Why not now:** CRUD endpoints are tested and passing. Splitting introduces import/circular dependency risk. Thesis paper fixes and frontend CRUD integration are higher priority.
- **Case for splitting:** Cognitive load (can't hold 1,876 lines in head), merge conflicts (concurrent edits guaranteed), test isolation (CRUD vs AFOR vs stats all in one file), import side effects (one break kills all regional endpoints).
- **Case against (for now):** It works. 1,876 lines isn't a runtime problem, it's a DX problem. Split itself is non-trivial — AFOR import/commit/CRUD/stats share models, auth guards, helpers. Half-day minimum, every route needs re-testing.
- **Planned split structure when ready:**
  ```
  regional/
  ├── __init__.py       # mount sub-routers
  ├── crud.py           # POST/PUT/DELETE/GET incidents (~400 lines)
  ├── afor_import.py    # import + commit (~500 lines)
  ├── stats.py          # analytics endpoints (~100 lines)
  └── _deps.py          # shared auth guards, helpers
  ```
- **Trigger to revisit:** When thesis work is done and you have breathing room for refactoring.

### Split get_db() into get_db() + get_db_with_rls()
- **Status:** DONE (2026-04-09)
- **Why:** Avoid dependency cycle where `get_current_wims_user` depends on `get_db` but `get_db` needs user resolved first to set RLS context. Split into bare session (`get_db()`) and RLS-aware session (`get_db_with_rls(request)`).
- **Also fixed:** Eager initialization of `_engine`/`_SessionLocal` (was lazy `None`, caused TypeError in tests), `load_dotenv()` before URL resolution (was falling back to Docker hostname).

### Matrix gateway for localhost image sending
- **Status:** Deferred
- **Why deferred:** Telegram image pipeline sufficient for now, Matrix adds infrastructure overhead
- **Trigger to revisit:** When Telegram workflow becomes insufficient

### Local LLM on GTX 1050 Max-Q
- **Status:** Not started
- **Constraint:** 3 GB VRAM — only small quantized models viable
- **Options:** Qwen2.5-3B quantized, Phi-3-mini, or similar

---

## Reversed Decisions

### Multi-agent Discord architecture
- **Was:** 4-agent setup with Discord channels
- **Reversed because:** Didn't work, coordination overhead exceeded value
- **Replaced with:** Single-agent with Telegram + CLI

---

*Add new decisions at the top of their section. Move reversed decisions to the Reversed section.*
