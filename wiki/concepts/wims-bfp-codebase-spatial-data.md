---
id: wims-bfp-codebase-spatial-data-001
type: concept
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
  - postgis
  - spatial
related:
  - entities/wims-bfp-codebase-database-schema
  - concepts/wims-bfp-codebase-data-flow
---

# Spatial Data

PostGIS geography columns for incident location tracking and heatmap generation.

## Implementation

| Table | Column | Type | SRID |
|-------|--------|------|------|
| `fire_incidents` | `location` | `geography(Point, 4326)` | 4326 |
| `citizen_reports` | `location` | `geography(Point, 4326)` | 4326 |

## Queries

### Heatmap aggregation
```sql
SELECT
  ST_Y(location::geometry) AS latitude,
  ST_X(location::geometry) AS longitude,
  COUNT(*) as incident_count
FROM wims.fire_incidents
WHERE created_at BETWEEN $1 AND $2
GROUP BY location;
```

### Spatial clustering (Celery)
```sql
-- Cluster incidents within 500m radius
SELECT ST_ClusterDBSCAN(location::geometry, eps := 0.005, minpoints := 3)
  OVER () as cluster_id,
  incident_id, location
FROM wims.fire_incidents
WHERE status = 'VERIFIED';
```

### Coordinate extraction (GET detail)
```sql
SELECT
  fi.*,
  ST_Y(fi.location::geometry) AS latitude,
  ST_X(fi.location::geometry) AS longitude
FROM wims.fire_incidents fi
WHERE fi.incident_id = $1;
```

## Frontend Integration

`MapPickerInner.tsx` — Leaflet map for location selection (create) and display (detail view).
- Shows incident pin when coordinates exist
- Hidden when null (legacy imports without location)

## Related

- [[entities/wims-bfp-codebase-database-schema]] — PostGIS column definitions
- [[concepts/wims-bfp-codebase-data-flow]] — analytics stage
