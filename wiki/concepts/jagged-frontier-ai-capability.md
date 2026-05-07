---
id: jagged-frontier-ai-capability-001
type: concept
created: 2026-04-12
updated: 2026-04-12
last_verified: 2026-04-12
review_after: 2026-06-12
stale_after: 2026-10-12
confidence: high
source_refs:
  - raw/articles/aisle-jagged-frontier-2026-04-12
status: active
tags:
  - ai-research
  - llm
  - cybersecurity
  - xai
  - agents
related:
  - entities/aisle
  - concepts/ai-cybersecurity-pipeline
  - concepts/applied-llms
  - concepts/state-of-the-field-wims-bfp
  - concepts/ai-benchmark-exploitation
  - concepts/goodhart-law-ai-metrics
---

# The Jagged Frontier — AI Capability Doesn't Scale Smoothly

## Definition

**AI capability across tasks is not a smooth curve.** Models that dominate one task can fail catastrophically on a superficially similar task. There is no stable "best model" — rankings reshuffle completely depending on the specific task.

The term was popularized by Stanislav Fort (AISLE) in April 2026, based on empirical testing across 25+ models on cybersecurity tasks.

## The Core Insight

Traditional assumption: bigger model = better across all tasks. Frontiers labs (OpenAI, Anthropic, Google) implicitly sell this narrative.

Reality from AISLE's testing:
- **GPT-OSS-120b** (5.1B active params): Recovers full exploit chain on 27-year-old OpenBSD bug → BUT fails to trace data flow through a Java ArrayList
- **Qwen3 32B**: Scores perfect 9.8 CVSS on FreeBSD detection → BUT declares the OpenBSD SACK code "robust" (it's not)
- **Small open models** ($0.11/M tokens): Detect Mythos's flagship exploit → BUT frontier models (Claude 3.5 Sonnet) get the OWASP false-positive test WRONG

## Evidence Table (Cybersecurity Tasks)

| Model | FreeBSD Detection | OpenBSD SACK | OWASP False Positive | FreeBSD Patched |
|---|---|---|---|---|
| GPT-OSS-120b (5.1B) | ✅ A+ | ✅ Full chain | ✅ Correct | ✅ Perfect |
| GPT-OSS-20b (3.6B) | ✅ | ❌ B- | ✅ Correct | ❌ FP |
| Kimi K2 (open) | ✅ | ✅ Concrete bypass | ✅ Correct | ❌ FP |
| DeepSeek R1 (open) | ✅ Most precise | ❌ F | ✅ Correct | ❌ FP |
| Qwen3 32B | ✅ Perfect CVSS | ❌ "Robust" | ❌ | ❌ FP |
| Claude Opus 4.6 | ✅ | ❌ | ✅ Correct | ❌ FP |
| Claude 3.5/3.7 Sonnet | ✅ | ❌ | ❌ Wrong | ❌ FP |

**Pattern:** 100% sensitivity across all models (all find bugs). Wildly varying specificity (most false-positive on patched code). Only GPT-OSS-120b is reliable in both directions.

## Inverse Scaling

On the OWASP false-positive test (tracing data flow through a Java ArrayList to distinguish real SQL injection from safe code):

- **Small open models**: Correctly trace that `get(1)` returns "moresafe", not user input
- **Large frontier models**: Confidently wrong — "Index 1: param → this is returned!" (Claude 3.7 Sonnet), "get(1) which is basically param" (GPT-4o-mini)

This is inverse scaling — smaller models outperforming larger ones on a specific task type.

## Implications

### 1. The moat is the system, not the model
The scaffolding, validation pipeline, triage logic, and security expertise embedded in the system matter more than which model runs inside it.

### 2. Deploy cheap models broadly
"A thousand adequate detectives searching everywhere will find more bugs than one brilliant detective who has to guess where to look." Coverage > per-token intelligence.

### 3. No stable "best model"
Don't commit to a single model provider. Build model-agnostic systems. The best model for task A may be the worst for task B.

### 4. Sensitivity ≠ Utility
A model that finds every bug but also false-positives on safe code is worse than useless at scale — it drowns reviewers in noise (this killed curl's bug bounty program).

## Relevance to WIMS-BFP

This concept directly supports WIMS-BFP's architecture decisions:
- **Multi-model approach:** Qwen 2.5-3B for log reading (cheap, task-specific) rather than a single expensive model
- **System > Model:** The security pipeline (Suricata → Celery → SLM → human review) is the moat
- **Triage layer matters:** The human-in-the-loop validator step is essential because model specificity is unreliable
- **Budget-aware deployment:** A 3B model at $0.11/M tokens is sufficient for many detection tasks

## Open Questions

- Does jaggedness apply equally to non-security tasks? (Likely yes — early evidence from coding benchmarks)
- Can jaggedness be predicted from model architecture or training data?
- How should system designers allocate budget across models vs. scaffolding?

## Sources

- [[raw/articles/aisle-jagged-frontier-2026-04-12]] — full article with model quotes
- [[entities/aisle]] — company profile and track record
- [[concepts/ai-cybersecurity-pipeline]] — 5-stage decomposition
- [[concepts/ai-benchmark-exploitation]] — benchmark gaming as jaggedness enabler
- [[concepts/goodhart-law-ai-metrics]] — why benchmarks lose validity under optimization pressure
