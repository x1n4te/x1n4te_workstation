---
id: wims-bfp-ch2-rrl-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-07-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - raw/misc/02-rorl.md
  - raw/misc/02-01-theoretical-framework.md
  - raw/misc/02-02-related-literature.md
  - raw/misc/02-03-related-studies.md
  - raw/misc/02-04-synthesis.md
status: active
tags:
  - wims-bfp
  - thesis
  - chapter-2
  - rrl
  - literature-review
  - zero-trust
  - xai
related:
  - concepts/zero-trust-architecture
  - sources/cybersecurity/zero-trust-complete-guide-2026
  - sources/software-dev/wims-bfp-ch1-introduction
---

# WIMS-BFP Chapter 2: Review of Related Literature

**Source:** raw/misc/ (5 files, ~51 KB)
**Chapter:** 2 — Review of Related Literature

---

## Scope

Reviews foundational cybersecurity theories and modern threat landscape. Focuses on integration of Suricata IDS deterministic detection with Qwen2.5-3B Explainable AI (XAI). Integrates regulatory compliance standards (NIST, RA 10173). Identifies gaps in Suricata's signature limitations for zero-days, black-box interpretability, and alert fatigue. Establishes theoretical basis for WIMS-BFP's hybrid Cognitive IDS architecture.

---

## 2.1 Theoretical Framework

WIMS-BFP is built on convergence of 4 cybersecurity paradigms:

### 1. Zero Trust Architecture (ZTA)

**Core principle:** "Never trust, always verify" — no implicit trust regardless of network location.

| Source | Key Argument |
|---|---|
| Blancaflor et al. (2023) | ZTA is a process (not a tool) relying on continuous identity verification, least-privilege, micro-segmentation |
| Ojo & Ojo (2025) | Digital transformation has blurred traditional network boundaries — perimeter models insufficient |
| Abdelmagid & Diaz (2025) | ZTA essential for resource-constrained agencies to mitigate cascading ransomware effects |

**WIMS-BFP application:** Treats every login as potential threat; justifies strict RBAC + MFA to prevent lateral movement even if local workstation compromised.

### 2. Cyber Resilience

**Core principle:** Anticipate, withstand, recover from, and adapt to attacks — "mission assurance."

**Key adaptation:** Organizational Co-Production (Christine & Thinyane, 2020) — users as active sensors, not passive recipients. WIMS-BFP adapts this to institutional level: BFP encoders and validators become active monitors providing real-time data on system health.

**Operational goal:** Fire incident reporting available even during cyber-attacks; human operators remain final fail-safe in security loop.

### 3. Offline-First Design (PWA)

**Core principle:** Prioritize local execution; distinguish offline storage from data synchronization.

| Source | Key Contribution |
|---|---|
| Agbeyangi & Suleman (2024) | Design pattern for low-resource environments: "Pre-Populate" and "Offline Operation" sub-patterns to mitigate high latency |
| Kalembo & Ntalasha (2025) | Secure offline frameworks indispensable for institutional software in regions with inconsistent connectivity |

**WIMS-BFP application:** Local database for immediate encoding + background sync mechanism that pushes to National HQ only when connectivity restored. Ensures zero downtime during typhoons.

### 4. Digital Sovereignty

**Core principle:** State authority to manage data within its jurisdiction — prioritize "Data Residency."

**WIMS-BFP application:** Hosted on secure, controlled LAN at National HQ. Eliminates dependence on third-party foreign cloud providers. BFP retains absolute custody over sensitive fire incident records.

---

## 2.2 Related Literature (Thematic Summary)

### Theme 1: Evolving Cyber Threat Landscape

| Finding | Source | WIMS-BFP Relevance |
|---|---|---|
| Lateral movement is defining characteristic of modern intrusions; detection shifted to log-centric telemetry + EDR | Smiliotopoulos et al. (2024) | Justifies Suricata IDS for post-compromise visibility |
| APT progression in IIoT environments; early containment reduces total operational loss | Bi et al. (2022) | Supports continuous internal monitoring |
| Cloud-hosted systems inherit shared-responsibility model; app-layer security is deployer's obligation | Armbrust et al. (2010) | Justifies WIMS-BFP's application-layer controls |
| Stealthy integrity attacks evade standard detection by mimicking normal patterns | Duo et al. (2022) | Supports integrity-aware detection for event-driven operations |
| Hybrid IDS combining deterministic rules + LLM-assisted explanations improves analyst understanding | Ahmed (2025) | Direct validation of WIMS-BFP's Suricata + XAI architecture |
| Language models better suited for unstructured logs than traditional ML classifiers | Tejero-Fernández & Sánchez-Macín (2025) | Supports XAI as interpretability layer |

### Theme 2: Cloud Deployment + Defensive Technologies

| Finding | Source | WIMS-BFP Relevance |
|---|---|---|
| ZTA functionally necessary for cloud-hosted systems (no trusted perimeter) | Mell & Grance (2011) | Validates ZTA implementation |
| ZTA reduces ransomware risks for Philippine institutions | Blancaflor et al. (2023) | Local relevance for BFP |
| Resource-constrained orgs face hurdles implementing ZTA | Abdelmagid & Diaz (2025) | Justifies WIMS-BFP's lightweight approach |
| IaaS model: provider manages infrastructure, deployer responsible for app-layer | NIST (Mell & Grance, 2011) | Defines WIMS-BFP's security responsibility boundary |
| CSA framework: controls across identity, data security, infra hardening, incident response | CSA (2017) | Guides WIMS-BFP's security architecture |
| Cloud-hosted gov systems must implement compensating controls (firewall, encryption, logging) | NIST SP 800-144 (2011) | Maps to WIMS-BFP's specific implementations |

### Theme 3: Offline-First for Critical Systems

- PWA offline patterns validated for remote healthcare (Malanin, 2025)
- Service Workers + IndexedDB preserve data during outages
- Gap identified: offline systems prioritize sync/usability but lack forensic integrity

### Theme 4: AI-Assisted Cybersecurity

- AI as interpretability layer (not autonomous detector) validated by multiple studies
- Generative AI better suited for supporting human decision-making than replacing it
- Risks: hallucination and misinterpretation in high-stakes security settings
- Lightweight models demonstrate interpretability AI is accessible to resource-constrained institutions

---

## 2.3 Related Studies (Comparative Analysis)

| Study | Approach | Strength | Limitation | WIMS-BFP Differentiation |
|---|---|---|---|---|
| Malanin (2025) | Service Workers + IndexedDB for offline healthcare | Zero data loss during outages | Lacks forensic security for cached data | Adds tamper-evident logging + hybrid encryption for legal verifiability |
| Mintoo et al. (2022) | Qualitative AI/ZTA in crisis response | Validates AI + ZTA for situational awareness | Gaps in "inclusive design" for non-technical users | Focuses on Usability alongside ZTA for exhausted fire officers |
| Obuse et al. (2023) | AI incident response in critical infra | Reduces MTTD; ISO 27001 compliance | Struggles with false positives + legacy integration | HITL workflow — AI assists but doesn't replace analyst |
| Kaya et al. (2024) | GNN + XAI (X-CBA) for IDS | 99.47% accuracy; solves black-box trust | High GPU requirements for GNN | Uses lightweight Qwen2.5-3B for standard office PCs |
| Malagad (2022) | Blockchain (Hyperledger) for audit logs | Guarantees non-repudiation + tamper-proofing | High latency; fails in offline disasters | Uses lightweight hash chaining instead of heavy blockchain |
| Salaguste (2022) | Open-source WAF | Cost-effective perimeter security | Layer 7 only; lacks internal Zero Trust | Full Zero Trust inside application, not just perimeter |

### Key Gap Identified

Existing solutions satisfy only part of WIMS-BFP's requirements:
- Offline-first systems lack forensic integrity
- Forensic systems require continuous connectivity
- AI studies frame AI as detector or classifier, not post-detection interpretability layer
- Few studies address cloud-hosted gov systems with offline-first + secure auditability + XAI

---

## 2.4 Synthesis

### Research Gaps Justifying WIMS-BFP

1. **Fragmented research:** Resilience, cloud security, XAI, forensic integrity discussed as separate concerns, not integrated architectural requirements
2. **AI framing limitation:** AI treated as autonomous detector or supplementary classifier, not as post-detection interpretability layer for human analysts
3. **Cloud + offline gap:** NIST/CSA guide cloud deployments, but few address how controls operationalize in systems that also support offline-first workflows

### WIMS-BFP as Gap Closure

| Gap | WIMS-BFP Solution |
|---|---|
| Offline-first lacks forensic integrity | Offline PWA + tamper-evident logging + hash-chained audit |
| Forensic systems need continuous connectivity | Append-only PostgreSQL logs work offline; sync when connected |
| AI as detector vs interpreter | Qwen2.5-3B strictly as interpretability layer (post-Suricata detection) |
| Cloud security without offline support | VPS deployment + offline-first PWA + regional accessibility |
| Complex systems for non-technical users | XAI narratives + user-centric explainable interface |

### Compliance Alignment

- Data protection obligations: RA 10173
- Evidentiary considerations: Philippine electronic records law
- Security frameworks: NIST CSF, ISO/IEC 27001

---

## Cross-References

- [[concepts/zero-trust-architecture]] — ZTA synthesis
- [[sources/cybersecurity/zero-trust-complete-guide-2026]] — ZTA market data
- [[sources/software-dev/wims-bfp-ch1-introduction]] — Chapter 1 context
