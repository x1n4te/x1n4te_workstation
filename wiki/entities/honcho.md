---
id: honcho-entity-001
type: entity
title: "Honcho — Cloud Memory Provider"
created: 2026-04-18
updated: 2026-04-18
last_verified: 2026-04-18
review_after: 2026-05-18
stale_after: 2026-07-18
confidence: high
source_refs:
  - log-archives/log-2026-04-18-hindsight-migration.md
status: active
tags:
  - memory-systems
  - llm-agents
  - cloud
  - hermes
related:
  - entities/hindsight
  - concepts/agent-memory-taxonomy
  - entities/hermes-agent
---

## Overview

**Honcho** is a cloud-based memory provider for AI agents, built by withhoncho.com. It provides persistent, compounding memory with background reasoning and observation synthesis.

**Status for x1n4te:** Currently active. $40 USD credits remaining (as of 2026-04-18). Migration to Hindsight deferred until credits approach exhaustion.

---

## Key Facts

| Property | Value |
|---|---|
| Type | Cloud memory provider |
| Pricing | Pay-as-you-go + free tier credits |
| Credits remaining | ~$40 USD (2026-04-18) |
| Benchmark scores | Not publicly published |
| Reasoning | Background automated reasoning |
| Self-hosted available | No |

---

## Integration

- Used by [[entities/hermes-agent]] as memory provider
- Peer cards, conclusions, and observations stored via `honcho_profile`, `honcho_conclude`, `honcho_reasoning` tools
- Honcho Cloud stores data remotely

---

## Comparison with Hindsight

| Dimension | Honcho | Hindsight |
|---|---|---|
| Cost | $0.10–0.30/session (cloud) | Free (self-hosted) |
| Benchmarks | Not published | 91.4–94.6% LongMemEval |
| Self-hosted | No | Yes (Docker) |
| Embeddings | Included | Built-in (local) |
| Reasoning | Automated background | LLM-based consolidation |
| TPM constraints | None (cloud) | Limited by LLM provider |
| Credits | $40 remaining | Free |

**Decision (2026-04-18):** Stay on Honcho until credits exhaust. Hindsight skill updated and ready for when migration is needed.

---

## See Also

- [[entities/hindsight]] — Self-hosted alternative (deferred)
- [[analyses/memory-systems-comparison]] — Full benchmark comparison
- [[concepts/agent-memory-taxonomy]] — Memory type taxonomy
- [[entities/hermes-agent]] — Hermes agent integration
