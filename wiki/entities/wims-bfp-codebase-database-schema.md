---
id: wims-bfp-codebase-database-schema-001
type: entity
created: 2026-04-21
updated: 2026-04-21
last_verified: 2026-04-21
review_after: 2026-06-21
stale_after: 2026-10-21
confidence: high
source_refs:
  - raw/sources/wims-bfp-codebase/docs/DATABASE.md
  - raw/sources/wims-bfp-codebase/docs/ARCHITECTURE.md
status: active
tags:
  - wims-bfp
  - database
  - schema
  - postgres
  - postgis
related:
  - concepts/wims-bfp-codebase-rls-model
  - entities/wims-bfp-codebase-init-scripts
  - entities/wims-bfp-codebase-api-endpoints
---

# Database Schema

Schema: `wims`. Extensions: `postgis`, `pgcrypto`. All tables have RLS enabled.

## Reference Tables (read-only seed)

| Table | PK | Description |
|-------|----|-------------|
| `ref_regions` | `region_id` (int) | Philippine regions (NCR seeded) |
| `ref_provinces` | `province_id` (int) | Provinces per region |
| `ref_cities` | `city_id` (int) | Cities per province |
| `ref_barangays` | `barangay_id` (int) | Barangays per city |

## Core Tables

| Table | PK | Description | RLS |
|-------|----|-------------|-----|
| `users` | `user_id` (uuid) | User accounts synced from Keycloak | Yes |
| `data_import_batches` | `batch_id` (serial) | AFOR import batch tracking | Yes |
| `fire_incidents` | `incident_id` (serial) | Official fire incidents | Yes |
| `citizen_reports` | `report_id` (serial) | Civilian-submitted reports | Yes |

## Incident Detail Tables (FK → fire_incidents)

| Table | PK | Description |
|-------|----|-------------|
| `incident_attachments` | `attachment_id` (serial) | File attachments |
| `incident_nonsensitive_details` | `detail_id` (serial) | Non-PII details |
| `incident_sensitive_details` | `detail_id` (serial) | PII fields (encrypted) |
| `incident_verification_history` | `history_id` (serial) | Status change audit trail |
| `involved_parties` | `party_id` (serial) | People involved |
| `operational_challenges` | `challenge_id` (serial) | Challenges encountered |
| `responding_units` | `unit_id` (serial) | BFP units that responded |

## Wildland AFOR Tables

| Table | PK | Description |
|-------|----|-------------|
| `incident_wildland_afor` | `afor_id` (serial) | Wildland AFOR header |
| `wildland_afor_alarm_statuses` | `status_id` (serial) | Alarm status details |
| `wildland_afor_assistance_rows` | `row_id` (serial) | Assistance received rows |

## Security & Audit Tables

| Table | PK | Description |
|-------|----|-------------|
| `audit_log` | `log_id` (serial) | System-wide audit trail |
| `security_threat_log` | `threat_id` (serial) | Suricata alerts + XAI narratives |

## Enums

| Enum | Values |
|------|--------|
| `verification_status` | DRAFT, PENDING, VERIFIED, REJECTED |
| `incident_type` | STRUCTURAL, WILDLAND, VEHICLE, OTHER |
| `severity_level` | LOW, MEDIUM, HIGH, CRITICAL |

## Indexes

- `fire_incidents.region_id` — RLS filtering
- `fire_incidents.created_at` — time-range queries
- `fire_incidents.location` (GIST) — PostGIS spatial queries
- `citizen_reports.status` — triage queue
- `audit_log.timestamp` — audit log pagination

## Related

- [[concepts/wims-bfp-codebase-rls-model]] — Row Level Security policies
- [[entities/wims-bfp-codebase-init-scripts]] — SQL migration order
- [[entities/wims-bfp-codebase-api-endpoints]] — routes that use these tables
