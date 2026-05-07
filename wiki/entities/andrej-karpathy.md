---
id: andrej-karpathy-001
type: entity
created: 2026-04-12
updated: 2026-04-12
last_verified: 2026-04-12
review_after: 2026-06-12
stale_after: 2026-10-12
confidence: high
source_refs:
  - raw/articles/karpathy-autoresearch-loop-2026-03
status: active
tags:
  - llm
  - agents
  - training
  - ai-research
related:
  - concepts/karpathy-loop-autoresearch
  - concepts/llm-foundations-learning-path
  - concepts/applied-llms
---

# Andrej Karpathy — AI Researcher

**Role:** Independent AI researcher, founder of Eureka Labs
**Background:** Founding employee of OpenAI, former head of AI at Tesla
**Followers:** 1.9M on X (@karpathy)

## Key Contributions

### Neural Network Lectures (2015-2017)
Stanford CS231n — the definitive deep learning course. Most widely used neural network educational resource.

### LLM Wiki (2025-2026)
Proposed using LLMs to build persistent, interlinked markdown knowledge bases instead of traditional RAG. "Compile knowledge once, keep it current." This wiki is based on his pattern.

### AutoResearch / The Karpathy Loop (March 2026)
Built an autonomous ML experimentation agent that ran 700 experiments in 2 days, discovering 20 training optimizations. See [[concepts/karpathy-loop-autoresearch]].

### "The Jagged Frontier" Alignment (March 2026)
Popularized the concept that AI capability doesn't scale smoothly — models that dominate one task can fail on similar tasks. Independently validated by AISLE's cybersecurity testing.

### "The Loopy Era" (2026)
Coined the transition from "coding" to "looping" — where humans assign tasks to agents that loop through implementation, testing, and iteration autonomously. "Code isn't even the right verb anymore."

## Philosophy

- **Model-agnostic:** "I simultaneously feel like I'm talking to an extremely brilliant PhD student and a 10-year-old." Jagged capability means no single model is always best.
- **Agent-first workflow:** Went from 80% writing code himself to 20% — delegates nearly everything to agents now.
- **Parallel agents:** "You're not running enough agents in parallel. Working serially in a parallel world is a mistake."
- **Self-improving systems:** "All LLM frontier labs will do this. It's the final boss battle."

## Relevance to x1n4te

Karpathy's ideas directly shaped multiple components:
- This LLM Wiki uses his LLM Wiki pattern
- The Karpathy Loop applies to WIMS-BFP SLM fine-tuning
- The "jagged frontier" concept validates WIMS-BFP's multi-model architecture
- The "loopy era" philosophy matches x1n4te's Claude Code delegation workflow

## Links

- X: https://x.com/karpathy
- GitHub: https://github.com/karpathy
- Eureka Labs: https://eurekalabs.com
- AutoResearch: https://github.com/karpathy/autoresearch
- LLM Wiki Gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
