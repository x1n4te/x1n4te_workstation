---
id: wims-bfp-codebase-data-flow-001
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
  - architecture
  - data-flow
  - design
related:
  - sources/wims-bfp-codebase/wims-bfp-codebase-architecture-summary
  - entities/wims-bfp-codebase-api-endpoints
  - entities/wims-bfp-codebase-database-schema
---

# Data Flow

Civilian → Triage → Incident → Analytics pipeline. The 5-stage data lifecycle of WIMS-BFP.

## Stage 1: Public Submission

```
Civilian → POST /api/v1/public/report
              ↓
         wims.citizen_reports (status: PENDING)
```

No auth required. DMZ endpoint. Captures: location, description, contact info.

## Stage 2: Triage

```
NATIONAL_VALIDATOR → GET /api/triage/pending
                        ↓
                   Review citizen reports
                        ↓
                   POST /api/triage/{id}/promote
                        ↓
                   wims.fire_incidents (status: DRAFT)
```

Validator reviews pending civilian reports, promotes valid ones to official incidents.

## Stage 3: Regional Encoding

```
REGIONAL_ENCODER → POST /api/regional/afor/import (XLSX/CSV)
                      ↓
                 wims.data_import_batches (batch tracking)
                      ↓
                 wims.fire_incidents (status: PENDING)
                 + structural/wildland detail tables
```

AFOR import or manual entry. PostGIS location captured. Attachments uploaded.

## Stage 4: Analytics

```
NATIONAL_ANALYST → GET /api/analytics/heatmap
                        ↓
                   PostGIS spatial aggregation
                        ↓
                   Heatmap tiles + trend data
```

Queries aggregated data. PostGIS clustering. Date/type/location filters.

## Stage 5: Threat Detection (XAI)

```
Suricata → EVE JSON → Celery Beat (10s) → wims.security_threat_log
                                            ↓
                              POST /admin/security-logs/{id}/analyze
                                            ↓
                                   Ollama (Qwen2.5-3B)
                                            ↓
                                   Human-readable forensic narrative
```

On-demand analysis. Suricata does detection (deterministic). SLM translates to English only.

## Related

- [[entities/wims-bfp-codebase-api-endpoints]] — all routes in the pipeline
- [[entities/wims-bfp-codebase-database-schema]] — tables at each stage
- [[concepts/wims-bfp-codebase-xai-pipeline]] — Stage 5 detail
- [[concepts/wims-bfp-codebase-afor-import]] — Stage 3 detail
