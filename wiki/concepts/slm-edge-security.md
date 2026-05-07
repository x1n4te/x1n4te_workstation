---
id: slm-edge-security-001
type: concept
created: 2026-04-20
updated: 2026-04-20
last_verified: 2026-04-20
confidence: high
source_refs:
  - raw/articles/research-papers-trends-2026-04-20.md
status: active
tags:
  - llm
  - ai-research
  - inference
  - papers
  - wims-bfp
related:
  - concepts/slm-log-reading-pipeline
  - concepts/xai-soc-operations
  - mocs/llm-learning-pathway
---

# Small Language Models for Edge Security Deployment

## Definition
Deploying compressed or purpose-built small language models (0.5B–4B parameters) on edge/consumer hardware for local AI inference in security applications — avoiding cloud dependency, latency, and data leakage.

## Why It Matters (2026)
- Liquid AI LFM2.5: 1.2B params at ~2975 tokens/sec on AMD Ryzen CPUs
- Dell/Gartner predict task-specific SLMs used 3x more than general-purpose LLMs by 2027
- 75% of enterprise data now created outside traditional data centers
- 73% of organizations moving AI inferencing to the edge for energy efficiency

## Key Papers

| Paper | arXiv | Approach | Target |
|-------|-------|----------|--------|
| Compact LLMs via Pruning + KD (NVIDIA 2024) | 2407.14679 | Depth/width/attention/MLP pruning + KD retraining | General compression |
| Post-Training SLMs via KD (2025) | 2509.26497 | Curriculum SFT + on-policy KD from 7B teacher | 1B → Qwen3-1.7B parity |
| Agent Distillation (KAIST 2025) | 2505.17612 | Tool-augmented distillation > CoT distillation | Qwen2.5-3B matches 7B-class |
| SlideFormer (2026) | 2603.16428 | GPU sliding window + CPU offload + NVMe tiering | Single consumer GPU fine-tuning |
| Edge Prompt Caching (EuroMLSys'26) | 2602.22812 | Distributed Bloom-filter caching | RPi Zero 2W (512MB RAM) |

## Applicability to WIMS-BFP
- **Current:** Qwen2.5-3B running on GTX 1050 (3GB VRAM) for Suricata log analysis
- **Path to upgrade:** Agent distillation from 7B teacher → more capable 3B model
- **BFP station deployment:** 1-2B model quantized to Q4 on commodity hardware
- **Edge caching:** Bloom-filter prompt caching for repeated incident patterns

## Models to Watch (2026)
- **LFM2.5** (Liquid AI) — 1.2B, runs on CPUs/NPUs/Qualcomm Hexagon
- **Qwen2.5-3B** — Current baseline, agent distillation proven effective
- **Gemma-3** (Google) — 270M/1B variants for extreme edge

## Open Questions
- Can a 3B model reliably classify Suricata alert severity with human-level accuracy?
- Knowledge distillation overhead — how much training data needed from 7B teacher?
- On-premise security implications of running models at fire stations with limited IT support?

## Related
- [[concepts/slm-log-reading-pipeline]] — Current Qwen2.5-3B deployment for WIMS
- [[concepts/xai-soc-operations]] — Explainability layer for model outputs
- [[mocs/llm-learning-pathway]] — LLM learning roadmap
