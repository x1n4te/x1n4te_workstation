---
id: karpathy-loop-autoresearch-001
type: concept
created: 2026-04-12
updated: 2026-04-12
last_verified: 2026-04-12
review_after: 2026-05-12
stale_after: 2026-10-12
confidence: high
source_refs:
  - raw/articles/karpathy-autoresearch-loop-2026-03
status: active
tags:
  - agents
  - llm
  - training
  - ai-research
  - design
related:
  - entities/andrej-karpathy
  - concepts/slm-log-reading-pipeline
  - concepts/ai-cybersecurity-pipeline
  - concepts/jagged-frontier-ai-capability
  - concepts/llm-wiki-pattern
  - concepts/local-llm-finetuning-roadmap
---

# The Karpathy Loop — Autonomous ML Experimentation

## Definition

A 3-component agentic loop for autonomous machine learning experimentation. An AI agent iteratively modifies code, runs experiments, evaluates a metric, and proposes the next change — without human intervention.

Coined by Andrej Karpathy in March 2026 based on his "autoresearch" system.

## The 3 Components

| Component | What | Why |
|---|---|---|
| **Single file** | Agent can modify ONE file (training script) | Constrains scope, prevents runaway changes |
| **Single metric** | One objectively testable number to optimize | Clear signal, no ambiguity |
| **Fixed time** | Each experiment has a time limit | Prevents infinite loops, enables parallelism |

## How It Works

```
┌─────────────────────────────────────────────┐
│  Agent reads training code (single file)     │
│  Agent proposes a change (hyperparameter,    │
│    architecture tweak, data augmentation)     │
│  Agent runs experiment (fixed time limit)     │
│  Agent evaluates metric (loss, accuracy,      │
│    training speed)                            │
│  Agent logs result + proposes next change     │
│  Repeat N times                              │
└─────────────────────────────────────────────┘
```

## Proven Results

| Who | Experiments | Time | Result |
|---|---|---|---|
| Karpathy | 700 | 2 days | 20 optimizations, 11% training speedup |
| Shopify CEO (Tobias Lütke) | 37 | Overnight | 19% performance gain |

## Why This Works

1. **Breadth over depth** — agent tries 700 experiments vs human's 10-20
2. **No ego** — agent doesn't get attached to ideas, discards failures instantly
3. **Pattern recognition** — agent learns from experiment history what works
4. **Tight feedback loop** — change → measure → learn → repeat, no context switching

## Generalization: "Any Metric You Care About"

Karpathy's claim: any metric that is (a) efficiently evaluable or (b) has an efficient proxy metric can be autoresearched by an agent swarm.

This applies beyond ML training:
- **Software performance:** optimize any function's runtime
- **Security:** optimize detection rate while minimizing false positives
- **Business:** optimize conversion rate, retention, revenue
- **DevOps:** optimize deployment speed, resource usage

## Future: Multi-Agent Research Community

Current: single agent, sequential experiments, single path.

Future (Karpathy's vision): "Asynchronously massively collaborative for agents."
- Multiple agents exploring different optimizations in parallel
- Agents collaborating, sharing findings
- "Not emulating a single PhD student — emulating a research community of them"
- Humans contribute on the edges (curate, direct, validate)

## Application to WIMS-BFP

The Karpathy Loop directly applies to fine-tuning the SLM for Suricata alert analysis:

| Component | WIMS-BFP Implementation |
|---|---|
| Single file | `train_slm.py` — Unsloth LoRA training script |
| Single metric | F1 score on Suricata alert classification |
| Fixed time | 30 min per experiment (fits Vast.ai billing) |

**Experiment swarm plan:**
- LoRA rank: 8, 16, 32, 64
- Learning rate: 1e-4, 2e-4, 5e-4
- Epochs: 1, 2, 3
- Data augmentation: prompt variations
- Total: 4 × 3 × 3 × 2 = 72 experiments
- Time: 72 × 30 min = 36 hours on Vast.ai
- Cost: ~$7 on RTX 3090
- Result: optimal training config for SLM

## Application to Sushi Coder Training

Same pattern for fine-tuning Qwen2.5-Coder-3B:
- Metric: LiveCodeBench pass@1 or HumanEval pass@1
- Experiments: LoRA rank, learning rate, dataset mix, epochs
- Agent: Karpathy's autoresearch or custom GRPO loop

## Key Quote

"All LLM frontier labs will do this. It's the final boss battle. It's just engineering and it's going to work." — Andrej Karpathy

## Sources

- [[concepts/karpathy-loop-autoresearch]]
- [[entities/andrej-karpathy]]
- GitHub: https://github.com/karpathy/autoresearch
