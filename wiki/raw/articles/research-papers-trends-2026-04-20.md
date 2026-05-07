---
title: "Research Paper & Trend Scan — WIMS-BFP Workflow (2026-04-20)"
created: 2026-04-20
type: source
---

# Research Paper & Trend Scan — 2026-04-20

Aggregated research scan across four domains relevant to WIMS-BFP thesis and active workflows.

---

## PART A: arXiv Papers (Tier 2)

### Domain 1: Explainable AI for Cybersecurity & Fire Operations

**1. Too Much to Trust? XAI Impacts in AI-Driven SOCs**
- arXiv: 2503.02065 | 2025-03-03 | ACM CCS 2025
- Authors: Rastogi et al.
- Studies SOC analyst trust in XAI explanations. Role-aware, context-rich explanations improve triage efficiency and analyst confidence.
- Key finding: Analysts accept XAI outputs even at lower accuracy when explanations are perceived as relevant and evidence-backed.

**2. XAI for Deep Learning-Based NIDS Alert Classification**
- arXiv: 2506.07882 | 2025-06-09 | ICISSP 2025
- Authors: Kalakoti et al.
- Compares LIME, SHAP, Integrated Gradients, DeepLIFT on real SOC NIDS data.
- Key finding: DeepLIFT consistently outperforms other XAI methods for faithfulness, complexity, robustness, and reliability.

**3. XAI Comparative Analysis of Intrusion Detection Models**
- arXiv: 2406.09684 | 2024-06-14 | IEEE MeditCom 2024
- Authors: Corea et al.
- Applies occlusion sensitivity to compare ML models on UNSW-NB15.
- Key finding: Most classifiers use <3 critical features for ~90% accuracy. Random Forest best performer.

**4. XAI-CF: Explainable AI for Cyber Forensics**
- arXiv: 2402.02452 | 2024-02-04 | Engineering Applications of AI, 2026
- Authors: Alam & Altiparmak
- Comprehensive survey on XAI trust and legal standards in cyber forensics.

**5. Digital Twin + Agentic AI for Wildfire Management**
- arXiv: 2602.08949 | 2026-02-09
- Authors: Morsali & Khajavi
- Intelligent Virtual Situation Room (IVSR) for real-time fire incident monitoring with AI agents.
- Key finding: Closed-loop detection-to-intervention with reduced latency vs traditional systems.

### Domain 2: Zero Trust & STRIDE Threat Modeling

**6. Zero Trust Architecture: Systematic Literature Review**
- arXiv: 2503.11659 | 2025-03 | J Netw Syst Manage, 2026
- PRISMA framework analysis of 10 years of ZTA research. Covers identity-centric access, micro-segmentation, continuous verification.

**7. Lockbox: ZTA for Sensitive Cloud Workloads**
- arXiv: 2603.09025 | 2026-03
- Concrete ZTA implementation with secure enclaves, attestation, policy enforcement for multi-tenant SaaS.

**8. LLMs for STRIDE Threat Modeling**
- arXiv: 2505.04101 | 2025-05
- Evaluates 5 LLMs with 4 prompting techniques for automated STRIDE on 5G threats.
- Key finding: 63-71% accuracy depending on strategy. Few-shot with internet context performs best.

**9. ThreatGPT: Agentic AI for Threat Modeling**
- arXiv: 2509.05379 | 2025-09 | IEEE WF-PST 2025
- Agentic architecture where AI agents collaborate on STRIDE analysis with graph-based system representation.

**10. STRIDE-Based Threat Modelling of CI/CD Pipelines**
- arXiv: 2506.06478 | 2025-06
- STRIDE applied to build integrity, artifact signing, dependency verification in CI/CD.

### Domain 3: Small LLMs & Edge Deployment

**11. Compact LLMs via Pruning + Knowledge Distillation**
- arXiv: 2407.14679 | 2024-07 | NeurIPS 2024
- NVIDIA. Practical compression methodology combining depth/width/attention/MLP pruning with KD retraining.

**12. Post-Training for Small LLMs via Knowledge Distillation**
- arXiv: 2509.26497 | 2025-09
- openPangu Embedded-1B achieves Qwen3-1.7B-level performance via curriculum SFT + on-policy KD.

**13. Distilling LLM Agents into Small Models with Retrieval and Code Tools**
- arXiv: 2505.17612 | 2025-05 | NeurIPS 2025
- KAIST. Agent distillation > CoT distillation. Qwen2.5-Instruct 0.5B-3B models match next-tier larger models.

**14. SlideFormer: Fine-Tuning on Single GPU**
- arXiv: 2603.16428 | 2026-03
- Heterogeneous memory approach for low-VRAM fine-tuning. GPU as sliding window with CPU offloading + NVMe tiering.

**15. Accelerating Local LLMs on Edge via Distributed Prompt Caching**
- arXiv: 2602.22812 | 2026-02 | EuroMLSys'26
- Runs LLMs on RPi Zero 2W (512MB RAM). 93% TTFT reduction via Bloom-filter caching.

### Domain 4: Suricata / NIDS with ML

**16. GRIDAI: Generating & Repairing Suricata Rules via Multi-Agent LLMs**
- arXiv: 2510.13257 | 2025-10
- Multi-agent LLM framework auto-generates and repairs Suricata detection rules from pcap traffic.

**17. Deep Learning for Contextualized NetFlow NIDS (Survey)**
- arXiv: 2602.05594 | 2026-02
- 4D taxonomy for context-aware NIDS: temporal, graph, multimodal, multi-resolution context.

**18. Robust Anomaly Detection on CICIDS2017**
- arXiv: 2506.19877 | 2025-06 | IEEE CNS 2025
- Controlled comparison of MLP, 1D-CNN for anomaly detection baseline.

**19. Lightweight ML for IIoT Intrusion Detection**
- arXiv: 2501.15266 | 2025-01
- Resource-constrained IDS for edge/IoT environments.

**20. Hybrid ResNet-1D-BiGRU with Multi-Head Attention for Cyberattack Detection**
- arXiv: 2604.06481 | 2026-04
- 98.71% accuracy on Edge-IIoTSet. Hybrid DL architecture reference.

---

## PART B: Industry Trends (Tier 3-4, April 2026)

### 1. Agentic SOCs Going Production-Grade
2026 is the inflection point for autonomous SOC agents. Platforms like Conifers CognitiveSOC, Elastic Attack Discovery, and Cyble Blaze AI now correlate alerts into full attack chains. Gartner: 60% of SOC workload will shift to AI, but penetration still only 1-5% of enterprises.
Sources: elastic.co/security-labs, simplico.net (Apr 2026)

### 2. XAI Becomes a Compliance Mandate
Countries across Asia rolling out transparency mandates similar to EU AI Act. Security teams need auditable reasoning trails. Elastic's agentic SOC blueprint demands "transparent reasoning traces grounded in evidence."
Sources: cogentinfo.com, group-ib.com, nature.com/articles/s41598-026-43440-9

### 3. SOAR Is Dead — Long Live Agentic Workflows
Classic SOAR (pre-written playbooks) replaced by LLM agents that reason through novel threats. Production stack: Wazuh + Shuffle SOAR + DFIR-IRIS with agentic AI on top.
Source: simplico.net (Apr 2026)

### 4. SLMs Dominate Edge Deployment
Liquid AI LFM2.5: 1.2B params running at ~2975 tokens/sec on AMD Ryzen CPUs. Dell/Gartner predict task-specific SLMs used 3x more than general-purpose LLMs by 2027.
Sources: liquid.ai/blog, dell.com/en-us/blog

### 5. Alert Fatigue Crisis
SOC teams: avg 2,992 alerts/day, 63% go unaddressed (Vectra AI 2026). AI-driven false positive reduction is #1 ROI driver for SOC tooling.
Source: vectra.ai/topics/soc-operations

### 6. Keycloak 26.4 Ships Native Passkey Support
Conditional UI, modal UI, passkey-based re-authentication built in. Passkeys via Webauthn Passwordless Policy.
Source: keycloak.org/2025/09/passkeys-support-26-4

### 7. Passkeys-First Is Default Mindset
FIDO moved from pilot to scaled enterprise. Adaptive, risk-based step-up auth expected.
Sources: authsignal.com, hidglobal.com

### 8. GitHub Actions Rivals Jenkins
JetBrains 2026 CI/CD survey: GitHub Actions growing fastest due to native repo integration.
Source: blog.jetbrains.com/teamcity/2026/03

### 9. Container Usage Hit 92%
"Serverless containers" combining containerization + on-demand scalability. AI-native containers standard practice.
Sources: risingtrends.co, devopsdigest.com

### 10. Agentic AI Dominant OS Theme of 2026
Dify, n8n, Bifrost, Claude Code. Trend toward private, local, extensible agent workflows — not cloud-locked APIs.
Sources: dev.to, vertu.com

### 11. Hugging Face Expanding Fast
Kernel Hub (GPU-optimized kernels for NVIDIA/AMD), Chinese open models, regional ecosystems growing.
Source: huggingface.co/blog/state-of-os-hf-spring-2026

---

## GAP NOTE

No academic papers found on PostgreSQL RLS for multi-tenancy. Topic covered in practitioner docs (Crunchy Data, PostgreSQL docs). Reference OWASP ASVS Level 2 for data isolation.

---

## PRIORITY READING QUEUE

1. GRIDAI (2510.13257) — Multi-agent Suricata rule generation
2. LLMs for STRIDE (2505.04101) — Automated threat modeling baseline
3. XAI for NIDS (2506.07882) — DeepLIFT methodology on real SOC data
4. Agent Distillation (2505.17612) — Making Qwen2.5-3B more capable
5. Digital Twin for Wildfire (2602.08949) — AI + fire safety + incident monitoring
