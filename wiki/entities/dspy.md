---
id: dspy-entity-001
type: entity
title: DSPy (Declarative Self-improving Python)
created: 2026-04-07
updated: 2026-04-07
last_verified: 2026-04-07
review_after: 2026-05-07
stale_after: 2026-07-07
confidence: high
source_refs:
  - raw/ai-research/2604.04869v1.pdf
status: active
tags:
  - llm
  - prompt-engineering
  - framework
  - open-source
related:
  - sources/ai-research/dspy-declarative-prompt-optimization
  - concepts/declarative-prompt-optimization
  - concepts/hallucination-reduction
---

## DSPy

**Type:** Declarative framework for LLM prompt optimization  
**Paper:** Baradwaj et al., arXiv:2604.04869v1 [cs.CL], April 2026  
**Key claim:** Prompts are learnable parameters, not fixed text

### What It Is

DSPy automates prompt engineering by treating prompts as optimizable parameters. Instead of manually writing/cooking prompts, you declare the task and DSPy learns the best prompt structure through gradient-free search.

### Key Numbers

- **30-45%** factual accuracy improvement
- **~25%** hallucination reduction
- Works with: GPT-4-Turbo, LLaMA-3-70B, Mistral-Large

### Modules

`Predict` · `Rewrite` · `Score` · `Retrieve`

### Optimizers

`BootstrapOptimizer` · `MIPRO`

### See Also

- [[sources/ai-research/dspy-declarative-prompt-optimization]] — Full source summary
