---
id: wims-bfp-codebase-init-scripts-001
type: entity
created: 2026-04-21
updated: 2026-04-21
last_verified: 2026-04-21
review_after: 2026-06-21
stale_after: 2026-10-21
confidence: high
source_refs:
  - raw/sources/wims-bfp-codebase/docs/DATABASE.md
status: active
tags:
  - wims-bfp
  - database
  - postgres
  - migration
related:
  - entities/wims-bfp-codebase-database-schema
  - concepts/wims-bfp-codebase-rls-model
  - concepts/wims-bfp-development-setup
---

# Init Scripts (Database Migrations)

SQL scripts in `src/postgres-init/` run on PostgreSQL container first start.

## Migration Order

| File | Purpose | Tables Created |
|------|---------|----------------|
| `01_wims_initial.sql` | Main schema + seed data | All core tables, enums, RLS policies |
| `02_wims_seed_regions.sql` | Reference data seed | `ref_regions`, `ref_provinces` |
| `03_wims_analytics.sql` | Analytics tables | `analytics_incident_facts` (if exists) |
| `04_wims_wildland.sql` | Wildland AFOR tables | `incident_wildland_afor`, detail tables |

## Key Tables in 01_wims_initial.sql

- Schema creation: `CREATE SCHEMA wims;`
- Extensions: `CREATE EXTENSION postgis; CREATE EXTENSION pgcrypto;`
- Enums: `verification_status`, `incident_type`, `severity_level`
- Reference tables: `ref_regions`, `ref_provinces`, `ref_cities`, `ref_barangays`
- Core tables: `users`, `fire_incidents`, `citizen_reports`, `data_import_batches`
- Detail tables: `incident_attachments`, `incident_nonsensitive_details`, `incident_sensitive_details`, `incident_verification_history`, `involved_parties`, `operational_challenges`, `responding_units`
- Audit tables: `audit_log`, `security_threat_log`
- RLS policies: per-table SELECT/INSERT/UPDATE policies
- Helper functions: `wims.current_user_uuid()`, `wims.current_user_role()`, `wims.current_user_region_id()`

## RLS Session Variables

Set per-request by backend before queries:
```sql
SET LOCAL wims.current_user_id = '<user_uuid>';
SET LOCAL wims.current_user_role = 'REGIONAL_ENCODER';
SET LOCAL wims.current_user_region_id = '1';
```

## Related

- [[entities/wims-bfp-codebase-database-schema]] — full table listing
- [[concepts/wims-bfp-codebase-rls-model]] — RLS policy patterns
