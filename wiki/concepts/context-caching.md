---
id: context-caching-001
type: concept
created: 2026-04-07
updated: 2026-04-07
last_verified: 2026-04-07
review_after: 2026-05-07
stale_after: 2026-07-06
confidence: high
source_refs:
  - raw/ai-research/HERMES-AGENT.md
status: active
tags:
  - hermes-agent
  - context-compression
  - prompt-caching
  - token-optimization
  - anthropic
related:
  - concepts/model-routing
  - entities/hermes-agent
---

# Context Caching & Token Management

**Framework:** Hermes-Agent (Nous Research)  
**Section:** 6 of architectural analysis  

---

## Definition

Hermes-Agent uses a **dual compression architecture** plus **stable-prefix prompt caching** to combat the quadratic cost scaling of Transformer attention layers. Without active management, research workflows browsing hundreds of pages and executing dozens of tools would hit prohibitive API costs and latency.

---

## Dual Compression Architecture

Two independent threshold triggers ensure session stability:

### 50% Threshold — Agent Context Compressor
- **Location:** `agent/context_compressor.py` (embedded in core tool execution loop)
- **Trigger:** Context reaches 50% of active model's max length
- **Action:** LLM-driven summarization protocol
- **What it preserves:** Critical factual state + system instructions
- **Advantage:** Has real-time API-reported token metrics → precise timing

### 85% Threshold — Gateway Session Hygiene
- **Location:** `gateway/run.py` (`_maybe_compress_session`)
- **Trigger:** Overall payload exceeds 85% of model's total capacity
- **Action:** Aggressive truncation/compression at messaging perimeter
- **Purpose:** Ultimate failsafe before passing to costly inference engine
- **Use case:** Long-running unattended sessions (e.g., overnight Telegram/Discord accumulations)

---

## Anthropic Prompt Caching Mechanics

**Location:** `agent/prompt_caching.py`  
**Activation:** Automatic when Claude model detected (native API or OpenRouter)

### The Cache Invalidation Problem

The Anthropic API caches **stable system prompt prefixes** across sequential API calls within a session. Traditional agent loops inject dynamic timestamps or reload memories on every tool call — this **invalidates the cache instantly**, causing a cache miss and full input token billing on every iteration.

### Hermes-Agent's Stable-Prefix Architecture

Hermes-Agent assembles the prompt **strictly at message boundary**. During multi-step sub-tasks (file searches, code execution), the system instructions and historical context remain **mathematically identical** across turns. Result: every subsequent tool call triggers an **immediate cache hit**.

### Measured Performance

| Scenario | TTFT | Token Cost |
|---|---|---|
| Un-cached (33K tokens) | 28 seconds | Full input token count |
| Cache hit (33K tokens) | 0.3 seconds | ~75% input token reduction |

This creates the computational illusion of an **infinite, zero-latency context window**.

### Cache Integrity Rules

To preserve this optimization, the architecture **prohibits** any modification that would reload memories or alter toolsets mid-conversation. Doing so would shatter cache integrity.

---

## Implications for Deep Research

Without caching/compression:
- Research workflow with 100 web pages → context window exhausted in ~20 steps
- Each step progressively slower (quadratic attention cost)
- Cost becomes prohibitive

With dual compression + caching:
- 50% threshold proactively summarizes before crisis
- 85% threshold is edge failsafe
- Stable-prefix caching keeps repeated operations near-zero cost
- Research can run for hours/days unattended

---

## Related

- [[concepts/model-routing]] — Combined with caching for optimal cost/velocity
- [[entities/hermes-agent]] — Parent entity
