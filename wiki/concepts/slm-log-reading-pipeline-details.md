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

# SLM Pipeline — Detailed Reference

Back to overview: [[concepts/slm-log-reading-pipeline]]
## What Optimizes This Pipeline

### High Priority (Do These)

| Optimization | Why | Cost |
|---|---|---|
| **Prompt template quality** | 90% of output quality comes from the template | Free |
| **Structured output (Instructor/Pydantic)** | Prevents hallucinated fields, reliable parsing | Free |
| **Inference speed** | Batch processing, Celery queuing for bursts | Free |
| **Template A/B testing** | Iterating on phrasing gives 10x more than model upgrades | Free |

### Low Priority (Not Needed Now)

| Optimization | Why Not Needed |
|---|---|
| Fine-tuning | Translation task, not domain reasoning |
| MoE architecture | 3B is fast enough for single alerts |
| RAG | Alert data is self-contained |
| Larger model | 3B handles simple translation well |
| Cybersecurity training data | Suricata rules ARE the cybersecurity knowledge |

---

## Prompt Template Design

The template is the most important component. Quality in = quality out.

### Template Structure

```
You are a cybersecurity analyst writing incident reports for non-technical staff.

Suricata Alert:
- Timestamp: {timestamp}
- Source IP: {src_ip}:{src_port}
- Destination IP: {dest_ip}:{dest_port}
- Protocol: {protocol}
- Signature: {signature}
- Category: {category}
- Severity: {severity}

Write a 2-3 sentence forensic narrative explaining:
1. What happened
2. What it means for the network
3. Recommended action

Use plain English. No jargon.
```

### Template Iteration Tips

- Test different phrasings against the same alerts
- Include edge cases (empty fields, unknown values)
- A/B test output quality using MOS scoring (your thesis evaluation method)
- Include explicit format instructions ("2-3 sentences", "plain English")

---

## Structured Output (Recommended)

Use Instructor + Pydantic to force schema-compliant output:

```python
from pydantic import BaseModel
from typing import List

class ForensicNarrative(BaseModel):
    summary: str              # 1-sentence what happened
    threat_level: str         # low/medium/high/critical
    affected_assets: List[str]  # IPs, ports
    recommended_action: str   # what to do
    technical_detail: str     # for admins who want detail
```

Benefits:
- Consistent output format across all alerts
- Parseable by the dashboard frontend
- No hallucinated fields
- Enables programmatic quality checks

---

## Inference Configuration

| Setting | Value | Why |
|---|---|---|
| Temperature | 0.3 | Low — deterministic for consistent reports |
| Max tokens | 256 | Short narratives, not long analysis |
| Top-p | 0.9 | Slight diversity for natural language |
| Repeat penalty | 1.1 | Prevent repetitive phrasing |
| Batch size | 1 | One alert at a time (or small batch during bursts) |

---

## Celery Integration

Suricata alerts come in bursts during incidents. The pipeline uses Celery to prevent blocking:

```
Suricata EVE JSON → Celery task (suricata.py)
    ↓
Task reads alert from file/watch
    ↓
Extracts metadata
    ↓
Calls Qwen2.5-3B inference
    ↓
Stores narrative in security_threat_logs
```

The Celery worker handles:
- Deduplication (same alert logged multiple times)
- Rate limiting (prevent flooding the SLM)
- Error handling (what if inference fails?)

---

## What NOT to Optimize

| Temptation | Why to Resist |
|---|---|
| "Let's use a bigger model" | 3B is sufficient for translation. Larger = slower, more VRAM |
| "Let's fine-tune on cybersecurity data" | The task is translation, not reasoning. Fine-tuning risks overfitting |
| "Let's add RAG for CVE lookup" | Alerts contain the relevant context. RAG adds latency for marginal gain |
| "Let's use MoE for efficiency" | Your hardware (3GB VRAM) is the constraint, not architecture |
| "Let's make the SLM detect threats" | Suricata already does this deterministically. Don't replace it. |

---

## Connection to Thesis

See also: [[overview-state-of-field]] for where this fits in the WIMS-BFP research landscape.

This pipeline is evaluated in Chapter 3 using:
- **Inference latency profiling** — target <5s (NFR requirement)
- **MOS scoring** — XAI narrative intelligibility for non-technical BFP personnel
- **F1-Score** — Suricata detection accuracy (not SLM accuracy)

The SLM is evaluated on **usability** (MOS), not **accuracy** (F1). This is correct — the SLM translates, Suricata detects.

---

## Summary

The SLM log reading pipeline is simple by design:
- Suricata detects (deterministic, rule-based)
- Qwen2.5-3B translates (generative, language-based)
- Template quality drives output quality
- Don't over-engineer what's already working

Focus optimization effort on the prompt template, not the model.

---

*Part of the WIMS-BFP architecture. See [[sources/software-dev/wims-bfp-ch3b-architecture]] for the full system design.*
