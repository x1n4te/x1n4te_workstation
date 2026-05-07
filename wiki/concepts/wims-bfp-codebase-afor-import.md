---
id: wims-bfp-codebase-afor-import-001
type: concept
created: 2026-04-21
updated: 2026-04-21
last_verified: 2026-04-21
review_after: 2026-06-21
stale_after: 2026-10-21
confidence: high
source_refs:
  - raw/sources/wims-bfp-codebase/docs/API_AND_FUNCTIONS.md
status: active
tags:
  - wims-bfp
  - api
  - domain
related:
  - concepts/wims-bfp-codebase-data-flow
  - entities/wims-bfp-codebase-api-endpoints
  - entities/wims-bfp-codebase-database-schema
---

# AFOR Import

Accident/Incident Form Official Record import from XLSX/CSV. Two types: structural and wildland.

## Import Types

| Type | Tables | Format |
|------|--------|--------|
| Structural | `fire_incidents` + `incident_nonsensitive_details` | Standard AFOR fields |
| Wildland | `incident_wildland_afor` + alarm/assistance detail tables | Wildland-specific fields |

## Endpoint

```
POST /api/regional/afor/import
Content-Type: multipart/form-data

Body: file (.xlsx or .csv), import_type ("structural" | "wildland")
```

## Processing

1. File uploaded → `data_import_batches` record created (batch tracking)
2. Pandas parses XLSX/CSV → validates against schema
3. Each row → `fire_incidents` INSERT with region_id from encoder's JWT
4. PostGIS geocoding (if address provided) → `location` column
5. Batch summary returned: total rows, success, failures, errors

## Validation

- Required fields enforced per AFOR template
- Date format validation
- Region scoping (encoder can only import to their region)
- Duplicate detection (future — Module 3 conflict detection)

## Related

- [[concepts/wims-bfp-codebase-data-flow]] — Stage 3 in pipeline
- [[entities/wims-bfp-codebase-api-endpoints]] — import endpoint
- [[entities/wims-bfp-codebase-database-schema]] — import batch tracking table
