---
id: model-routing-001
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
  - model-routing
  - openrouter
  - minimax
  - api-optimization
  - asymmetric-delegation
related:
  - concepts/delegate-task-architecture
  - concepts/context-caching
  - entities/hermes-agent
---

# High-Velocity Model Routing

**Framework:** Hermes-Agent (Nous Research)  
**Section:** 5 of architectural analysis  

---

## Definition

Hermes-Agent implements sophisticated **provider routing** via OpenRouter and direct provider integration, enabling deterministic model selection based on latency, throughput, or price. Combined with **asymmetric delegation**, this allows expensive frontier models to handle strategic orchestration while fast/cheap models handle bulk data processing.

---

## OpenRouter Deterministic Routing

Identical models (Llama 3, Qwen 3.5) are hosted across multiple infrastructure providers (Together AI, DeepInfra, AWS Bedrock). Routing is controlled via `config.yaml`:

```yaml
model:
  sort: "latency"   # | "throughput" | "price"
  only: ["Anthropic"]  # Optional whitelist
  order: ["anthropic/claude-3-5-sonnet", "openai/gpt-4o"]  # Failover hierarchy
  require_parameters: true  # Block silent failures on incomplete tool schemas
```

### Routing Sort Parameters

| Parameter | Optimization | Deep Research Application |
|---|---|---|
| `latency` | Lowest TTFT | Interactive CLI, fast approval routing |
| `throughput` | Tokens/sec | Long-form synthesis, bulk report generation |
| `price` | Cost-per-token | Mass scraping, raw data categorization |

---

## Asymmetric Model Delegation

Deep research requires asymmetric cognitive loads:

| Agent Role | Cognitive Demand | Model Choice | Example |
|---|---|---|---|
| **Orchestrator (parent)** | Strategic reasoning, synthesis, goal alignment | Frontier (max reasoning) | Claude 3.5 Sonnet/Opus, GPT-4o |
| **Worker (child)** | Data extraction, parsing, simple transforms | Fast/cheap (high throughput) | Gemini Flash 2.0, Claude 3.5 Haiku, Qwen 3.5 MLX |

Configured via delegation block:
```yaml
delegation:
  model: "google/gemini-flash-2.0"   # Override for ALL child agents
  provider: "openrouter"
```

Local models at 50-80 tokens/sec (Qwen 3.5 MLX) are sufficient for worker tasks. This drops token expenditure by **orders of magnitude** vs. routing all tasks through frontier models.

---

## MiniMax-M2.7

Highlighted as a specialized **agent-native** model optimized for autonomous multi-agent workflows:

| Benchmark | Score |
|---|---|
| SWE-Pro | 56.2% success rate |
| GDPval-AA | 1495 ELO |

Key properties:
- Explicitly optimized for phased autonomous processing
- Low temporal latency and financial cost vs. frontier models (Claude 3.5 Opus)
- Direct integration via `provider: "minimax"` or OpenRouter

Provider: MiniMax (direct) or OpenRouter

---

## Provider Failover & Safety

`require_parameters: true` ensures requests only route to endpoints supporting full tool schemas — prevents silent failures during critical subagent loops.

Explicit `order` array defines failover hierarchy — if primary provider fails mid-research, automatically routes to next configured provider.

---

## Relevance to WIMS-BFP 4-Agent Discord Setup

Each of the 4 Hermes profiles (Orchestrator, Builder, Critic, Tester) can use different models:
- Orchestrator: Claude 3.5 Sonnet (strategic)
- Builder/Tester: Gemini Flash 2.0 or MiniMax-M2.7 (fast execution)
- Critic: Claude 3.5 Sonnet or DeepSeek (review/analysis)

---

## Related

- [[concepts/delegate-task-architecture]] — Child agent spawning
- [[concepts/context-caching]] — Stable-prefix optimization
- [[entities/hermes-agent]] — Parent entity
