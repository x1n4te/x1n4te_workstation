---
id: advisor-strategy-001
type: concept
created: 2026-04-10
updated: 2026-04-10
last_verified: 2026-04-10
review_after: 2026-07-10
stale_after: 2026-10-09
confidence: high
source_refs:
  - https://claude.com/blog/the-advisor-strategy
status: active
tags:
  - llm
  - cost-optimization
  - multi-model
  - claude
  - agents
related:
  - concepts/llm-applied-learning-path
  - concepts/llm-security-learning-path
  - entities/hermes-agent-setup
---

# Advisor Strategy — Multi-Model Agent Architecture

**Source:** Anthropic blog (April 2026)
**Status:** NOT NEEDED for current workflow — documented for reference
**API:** `advisor_20260301` tool in Claude Messages API

---

## What It Is

Pair a cheap model (executor) with an expensive model (advisor). The executor does all the work and only consults the advisor when it hits something it can't handle. The advisor gives guidance, never calls tools.

```
User task → Executor (Sonnet/Haiku) does the work
                ↓ (hits complex decision)
            Advisor (Opus) provides guidance
                ↓
            Executor continues with advice
```

---

## How It Works

- **Executor** (Sonnet/Haiku) — drives the task, calls tools, iterates, produces output
- **Advisor** (Opus) — only consulted when executor needs help; returns plan/correction/stop signal
- **Never inverted** — advisor never calls tools or produces user-facing output
- **Cost-controlled** — `max_uses` caps advisor calls per request

---

## Results (Anthropic's Evaluations)

| Benchmark | Executor Alone | Executor + Advisor | Improvement |
|---|---|---|---|
| SWE-bench Multilingual | Sonnet baseline | +2.7 percentage points | Near-Opus quality |
| BrowseComp | Haiku 19.7% | Haiku + Opus advisor 41.2% | 2x improvement |
| Cost per task | Sonnet solo | Sonnet + Opus advisor | 11.9% reduction |

---

## API Usage

```python
response = client.messages.create(
    model="claude-sonnet-4-6",  # executor
    tools=[{
        "type": "advisor_20260301",
        "name": "advisor",
        "model": "claude-opus-4-6",
        "max_uses": 3,
    }],
    messages=[...]
)
```

---

## Key Differences from Multi-Agent

| Aspect | Multi-Agent (rejected) | Advisor Strategy |
|---|---|---|
| Orchestration | Orchestrator decomposes, delegates | Executor drives, escalates |
| Complexity | Worker pool, coordination logic | Single executor + advisor |
| Model swap | Separate processes | Same API call |
| Cost | Higher (orchestrator overhead) | Lower (advisor only when needed) |

---

## When It's Useful

- Production agents with complex reasoning tasks
- High-volume workflows where cost matters
- Tasks that alternate between routine and complex
- NOT needed when using free-tier models
- NOT needed for simple translation/CRUD tasks

---

## Related

- [[concepts/llm-applied-learning-path]] — Applied LLMs learning path
- [[entities/hermes-agent-setup]] — Hermes uses single model (MiMo v2 Pro free tier)
