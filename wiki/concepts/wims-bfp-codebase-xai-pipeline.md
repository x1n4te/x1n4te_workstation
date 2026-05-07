---
id: wims-bfp-codebase-xai-pipeline-001
type: concept
created: 2026-04-21
updated: 2026-04-21
last_verified: 2026-04-21
review_after: 2026-06-21
stale_after: 2026-10-21
confidence: high
source_refs:
  - raw/sources/wims-bfp-codebase/docs/ARCHITECTURE.md
status: active
tags:
  - wims-bfp
  - ai
  - xai
  - security
related:
  - concepts/wims-bfp-codebase-data-flow
  - entities/wims-bfp-codebase-docker-services
  - concepts/wims-bfp-codebase-threat-model
---

# XAI Pipeline

Suricata → Celery → Qwen2.5-3B → human-readable forensic narrative. **Explainability, not autonomy** — the SLM translates only, it does NOT detect threats or execute actions.

## Pipeline Stages

```
1. Suricata IDS → EVE JSON log (/var/log/suricata/eve.json)
                      ↓
2. Celery Beat (10s interval) → suricata_ingestion.py parses EVE
                      ↓
3. security_threat_log table (raw alert stored)
                      ↓
4. Admin triggers: POST /admin/security-logs/{id}/analyze
                      ↓
5. ai_service.py → Ollama API (Qwen2.5-3B)
                      ↓
6. Human-readable narrative stored in security_threat_log.narrative
                      ↓
7. Frontend displays narrative alongside raw alert data
```

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| On-demand (not continuous) | Saves CPU/GPU resources; admin controls when analysis runs |
| Suricata does detection | Deterministic rule-based. SLM is not trusted for detection. |
| SLM translates only | Constitution: "Explainability, Not Autonomy" — AI cannot block IPs or alter DB |
| Qwen2.5-3B (not 7B) | Fits in available VRAM; 3B sufficient for translation task |
| Ollama (not raw llama.cpp) | Simpler API, Docker-friendly |

## Implementation

- `src/backend/services/ai_service.py` — prompt template + Ollama API call
- `src/backend/api/routes/admin.py` — `POST /admin/security-logs/{id}/analyze`
- Ollama Docker container with Qwen2.5-3B model loaded
- Response: structured JSON with alert summary, severity, recommended action

## NFR

| Metric | Requirement |
|--------|-------------|
| Inference latency | <5s mean |
| Narrative quality | MOS ≥ 4.0 (human evaluation) |
| Availability | On-demand; no SLA for continuous |

## Related

- [[concepts/wims-bfp-codebase-data-flow]] — full data pipeline
- [[entities/wims-bfp-codebase-docker-services]] — Ollama container
- [[concepts/wims-bfp-codebase-threat-model]] — threat landscape
