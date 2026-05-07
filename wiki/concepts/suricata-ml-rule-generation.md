---
id: suricata-ml-rule-generation-001
type: concept
created: 2026-04-20
updated: 2026-04-20
last_verified: 2026-04-20
confidence: medium
source_refs:
  - raw/articles/research-papers-trends-2026-04-20.md
status: active
tags:
  - suricata
  - cybersecurity
  - ai-research
  - papers
  - wims-bfp
related:
  - concepts/slm-log-reading-pipeline
  - concepts/xai-soc-operations
  - mocs/wims-bfp
---

# ML-Enhanced Suricata & Network Intrusion Detection

## Definition
Using machine learning and LLMs to enhance Suricata IDS capabilities — from automated rule generation and repair to alert classification and anomaly detection in network traffic.

## Key Papers

| Paper | arXiv | Contribution |
|-------|-------|--------------|
| GRIDAI Multi-Agent Suricata Rules (2025) | 2510.13257 | Multi-agent LLM framework auto-generates and repairs Suricata rules from pcap |
| Contextualized NetFlow NIDS Survey (2026) | 2602.05594 | 4D taxonomy: temporal, graph, multimodal, multi-resolution context |
| Robust Anomaly Detection CICIDS2017 (2025) | 2506.19877 | MLP vs 1D-CNN baseline comparison |
| Lightweight ML for IIoT IDS (2025) | 2501.15266 | Resource-constrained anomaly detection |
| Hybrid ResNet-1D-BiGRU (2026) | 2604.06481 | 98.71% accuracy on Edge-IIoTSet |

## GRIDAI Architecture (Most Relevant)
Multi-agent system with specialized roles:
1. **New-Rule-Generate** — analyzes pcap traffic, produces candidate rules
2. **Existing-Rule-Repair** — fixes broken or outdated rules
3. **Relation-Assess** — evaluates rule relationships and conflicts
4. **Memory-Update** — maintains rule knowledge base

## Industry Context (2026)
- Classic SOAR playbooks being replaced by agentic AI workflows
- Alert fatigue: avg 2,992 alerts/day, 63% go unaddressed
- AI-driven false positive reduction is #1 ROI driver for SOC tooling
- Wazuh + Shuffle SOAR + DFIR-IRIS + agentic AI = production stack pattern

## Applicability to WIMS-BFP
- Suricata is the IDS layer in WIMS-BFP architecture
- GRIDAI pattern could auto-generate rules for BFP-specific network traffic patterns
- DeepLIFT XAI integration for explainable alert classification
- Edge-deployed anomaly detection at fire station network boundaries

## NIDS Evaluation Pitfalls (from survey)
- **Temporal leakage** — training on future data inflates accuracy
- **Dataset flaws** — CICIDS2017 has known imbalance issues
- **Concept drift** — network traffic patterns change over time, models need retraining

## Related
- [[concepts/slm-log-reading-pipeline]] — Qwen2.5-3B for alert analysis
- [[concepts/xai-soc-operations]] — Explainable alert classification
- [[mocs/wims-bfp]] — Thesis project hub
