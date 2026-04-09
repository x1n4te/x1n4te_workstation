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
