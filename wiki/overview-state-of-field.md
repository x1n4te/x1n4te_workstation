---
id: overview-state-of-field-001
type: concept
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - sources/software-dev/wims-bfp-abstract
  - sources/software-dev/wims-bfp-ch1-introduction
status: active
tags:
  - overview
  - state-of-field
  - wims-bfp
related:
  - sources/software-dev/wims-bfp-abstract
  - sources/software-dev/wims-bfp-ch1-introduction
  - sources/software-dev/wims-bfp-ch2-rrl
  - mocs/cybersecurity
  - mocs/ai-research
---

# State of the Field — WIMS-BFP Context

---

## The Problem Space

Philippine government agencies (specifically BFP) rely on monolithic, internally-hosted systems for fire incident reporting. These systems have three critical gaps:

1. **No offline resilience** — disaster areas lose connectivity; field encoders can't capture data
2. **No spatial analytics** — incident data stays in flat tabular records; no geospatial heatmaps for pattern recognition
3. **Opaque security tools** — IDS alerts are raw logs that require specialized training to interpret; non-technical personnel can't act on them

WIMS-BFP addresses all three simultaneously.

---

## Research Landscape

### Offline-First PWAs for Government
Progressive Web Apps with IndexedDB caching are well-established for consumer apps but rare in Philippine government systems. The key challenge is maintaining data integrity during offline-to-online sync without conflicts or loss. WIMS-BFP uses AES-256-GCM encrypted bundles with SHA-256 chain hashing to ensure tamper-evidence during sync.

### Geospatial Analytics in Incident Management
PostGIS spatial queries for heatmap rendering are standard in commercial GIS platforms (ArcGIS, QGIS Server) but uncommon in Philippine government applications due to infrastructure cost. WIMS-BFP proves this is viable on consumer-grade VPS with open-source tooling.

### Explainable AI in Cybersecurity
The XAI field is dominated by LIME/SHAP for model interpretability. WIMS-BFP takes a different approach — it doesn't explain ML model decisions. Instead, it uses a Small Language Model (Qwen2.5-3B) to translate deterministic Suricata IDS alerts into human-readable narratives. This is "explainable security" not "explainable ML" — a narrower but more immediately actionable application.

### IDS Alert Fatigue
Suricata is widely deployed but produces high-volume, low-context alerts. The industry response is SIEM aggregation (Splunk, ELK). WIMS-BFP's contribution is an on-premise AI layer that converts alerts to narratives without external cloud dependency — critical for government data sovereignty.

---

## Where WIMS-BFP Fits

| Dimension           | State of the Art                     | WIMS-BFP Position                            |
| ------------------- | ------------------------------------ | -------------------------------------------- |
| Offline-first PWA   | Common in commercial, rare in PH gov | First-class offline with encrypted sync      |
| Geospatial heatmaps | Standard in commercial GIS           | Open-source PostGIS on VPS                   |
| XAI for security    | LIME/SHAP for ML models              | SLM narrative generation (novel application) |
| IDS integration     | SIEM-based aggregation               | On-premise AI interpretation                 |
| Data sovereignty    | Cloud SIEM (Splunk, Elastic)         | Fully self-hosted, no external AI dependency |
| Compliance          | Varies                               | RA 10173 + ISO 27001 + STRIDE mapped         |

---

## Key Technologies in This Vault

- **Suricata** — network IDS engine, signature-based detection → [[sources/cybersecurity/suricata-cves-2026]]
- **PostGIS** — spatial database extension for PostgreSQL → [[concepts/postgis-security-wims-bfp]]
- **FastAPI** — async Python backend framework → [[concepts/fastapi-security-wims-bfp]]
- **Keycloak** — identity and access management → [[concepts/keycloak-fastapi-security-wims-bfp]]
- **Qwen2.5-3B** — small language model for XAI narratives (runs on Llama.cpp, consumer hardware)
- **Docker** — containerized deployment → [[concepts/docker-security-wims-bfp]]
- **OWASP ASVS** — security verification standard → [[sources/software-dev/owasp-secure-code-review]]

---

## Active Research Threads

1. **WIMS-BFP thesis** — primary project, active development → [[sources/software-dev/wims-bfp-abstract]]
2. **AI agent memory systems** — comparative research (Mem0, MemGPT, MemMachine, DSPy) → [[analyses/memory-systems-comparison]]
3. **Hermes agent architectures** — operational use and configuration → [[entities/hermes-agent-setup]]
4. **Cybersecurity threat landscape** — CVE tracking for WIMS-BFP stack → [[mocs/cybersecurity]]
5. **LLM learning pathway** — 5-category curriculum for cybersecurity practitioners → [[mocs/llm-learning]]
6. **SLM/XAI pipeline** — Qwen2.5-3B log reading pipeline → [[concepts/slm-log-reading-pipeline]]

---

## Knowledge Gaps (to investigate)

- Real-world BFP adoption metrics (not yet available)
- Comparative benchmarks against commercial SIEM solutions
- Long-term XAI narrative quality with Suricata rule updates
- Performance under sustained high-volume attack (stress testing pending)

---

*This page is the LLM's orientation map. Read at session start to understand what this vault covers and where things fit.*
