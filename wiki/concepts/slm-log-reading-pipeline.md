---
id: slm-log-reading-pipeline-001
type: concept
created: 2026-04-09
updated: 2026-04-09
last_verified: 2026-04-09
review_after: 2026-07-09
stale_after: 2026-10-09
confidence: high
source_refs:
  - sources/software-dev/wims-bfp-ch3b-architecture
status: active
tags:
  - slm
  - xai
  - qwen2.5-3b
  - suricata
  - pipeline
  - wims-bfp
related:
  - sources/software-dev/wims-bfp-ch3b-architecture
  - sources/software-dev/wims-bfp-ch3c-security-tools
  - concepts/llm-applied-learning-path
  - entities/hermes-agent-setup
---

# SLM Log Reading Pipeline — Qwen2.5-3B for Suricata Alerts

**System:** WIMS-BFP XAI Layer
**Model:** Qwen2.5-3B (dense, 3B parameters, no MoE)
**Runtime:** Llama.cpp (quantized, consumer hardware)
**Purpose:** Translate Suricata IDS alerts into human-readable forensic narratives

---

## The Core Insight

The SLM is NOT doing cybersecurity reasoning. It's doing **structured-to-natural-language translation**. The cybersecurity knowledge is already in the Suricata rules — the model just translates.

```
What the SLM does:    JSON → English
What the SLM doesn't: Detect threats, correlate alerts, find CVEs
What provides security: Suricata rules (deterministic)
What provides language: Qwen2.5-3B (generative)
```

---

## Pipeline Flow

```
Suricata IDS
    ↓ (signature-based detection)
EVE JSON alert
    ↓
Celery worker (suricata.py task)
    ↓
FastAPI extracts metadata:
    - timestamp, src_ip, src_port
    - dest_ip, dest_port, protocol
    - signature, category, severity
    ↓
Prompt template injects into "Sovereign Forensic Template"
    ↓
Qwen2.5-3B via Llama.cpp (inference)
    ↓
Forensic narrative (2-3 sentences, plain English)
    ↓
Stored in wims.security_threat_logs
    ↓
Dashboard displays for BFP administrators
```

---

## What Qwen2.5-3B Handles Well

| Task | Difficulty | Capable? |
|---|---|---|
| "Describe this alert in plain English" | Easy | Yes |
| "Translate this JSON to a report" | Easy | Yes |
| "What does port 445 mean?" | Easy | Yes |
| "Is this a real threat or false positive?" | Hard | Barely |
| "Correlate this with 5 other alerts" | Hard | No |
| "What CVE does this exploit?" | Medium | Sometimes |

The pipeline only asks for the easy tasks.

---

## Related Sections
*Detailed content split into sub-pages for readability. See [[concepts/slm-log-reading-pipeline-details]] for the full reference.*

---

*This page is scannable in 30 seconds. Full reference content moved to sub-pages.*
