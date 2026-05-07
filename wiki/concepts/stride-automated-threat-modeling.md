---
id: stride-automated-threat-modeling-001
type: concept
created: 2026-04-20
updated: 2026-04-20
last_verified: 2026-04-20
confidence: medium
source_refs:
  - raw/articles/research-papers-trends-2026-04-20.md
status: active
tags:
  - cybersecurity
  - ai-research
  - papers
  - design
  - wims-bfp
related:
  - concepts/xai-soc-operations
  - concepts/zero-trust-architecture
  - mocs/wims-bfp
---

# Automated STRIDE Threat Modeling with LLMs

## Definition
Using Large Language Models and agentic AI to automate the STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation of Privilege) threat identification and risk assessment process.

## Current State (2026)

### LLM Performance
| Approach | Accuracy | Notes |
|----------|----------|-------|
| Few-shot + internet context | 71% | Best performing (arXiv:2505.04101) |
| Chain-of-thought | 68% | Middle ground |
| Zero-shot | 63% | Baseline |
| ThreatGPT (agentic) | Promising | Graph-based system repr + multi-agent reasoning (arXiv:2509.05379) |

### Key Findings
- LLMs can classify STRIDE categories at 63-71% accuracy — useful as first-pass triage, not replacement for human analysis
- Agentic architectures (ThreatGPT) outperform single-prompt approaches by using specialized agents for different threat categories
- STRIDE for CI/CD pipelines is a practical application area (arXiv:2506.06478)

## Applicability to WIMS-BFP
- Can automate initial STRIDE classification for web endpoints
- Human analyst reviews and validates LLM-generated threats
- Reduces time from hours to minutes for threat modeling sessions
- Integration with [[concepts/xai-soc-operations]] for explainable threat scoring

## Open Questions
- Can fine-tuned Qwen2.5-3B perform STRIDE classification locally?
- How to handle novel attack patterns not in training data?
- Legal validity of LLM-generated threat models for compliance audits?

## Related
- [[concepts/xai-soc-operations]] — Explainability for AI-driven security decisions
- [[concepts/zero-trust-architecture]] — ZTA patterns that STRIDE analysis informs
- [[mocs/wims-bfp]] — Thesis project hub
