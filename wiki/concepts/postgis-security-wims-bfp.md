---
id: postgis-security-wims-bfp-001
type: concept
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-07-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - sources/software-dev/postgis-secure-coding-practices
  - sources/software-dev/postgresql-security-best-practices
  - sources/software-dev/postgresql-rls-limitations
status: active
tags:
  - postgis
  - spatial
  - security
  - wims-bfp
  - rls
  - zero-trust
related:
  - sources/software-dev/postgis-secure-coding-practices
  - concepts/postgresql-security-wims-bfp
  - concepts/keycloak-fastapi-security-wims-bfp
---

# PostGIS Security for WIMS-BFP

**Component:** PostgreSQL PostGIS extension
**Usage:** Incident geolocation, regional boundary enforcement, spatial proximity search, BFP station mapping
**SRID Standard:** 4326 (WGS84) globally

---

## WIMS-BFP Spatial Data Flow

```
Civilian Reporter (DMZ)
  → /api/v1/public/report (lat, lon)
  → FastAPI validates + sanitizes geometry
  → ST_MakePoint(%s, %s)::geography — parameterized
  → INSERT into wims.incidents (geom, region_id)
  → RLS policy checks region_id = wims.current_region_id

Regional Encoder
  → Spatial queries (ST_DWithin, ST_Contains)
  → RLS filters by region_id
  → PostGIS metadata (spatial_ref_sys) read-only

National Analyst
  → Global spatial read (no RLS region filter)
  → GeoJSON output via ST_AsGeoJSON
  → READ-ONLY — no INSERT/UPDATE/DELETE
```

---

## Security Layers

### Layer 1: Input Validation
- WKT/WKB validated via Shapely before DB touch
- Vertex count limit: 10,000
- Empty/degenerate geometry rejection
- SRID enforcement (4326 only)

### Layer 2: Parameterized Queries
- All spatial functions use `%s` or `:param` placeholders
- NEVER f-string interpolation in ST_GeomFromText, Find_SRID, ST_MakePoint
- GeoPandas >= 1.1.2 (CVE-2025-69662 patched)

### Layer 3: RLS + Spatial Filtering
- RLS policies on wims.incidents enforce region_id
- Spatial queries automatically filtered by RLS
- ST_DWithin results scoped to authorized region

### Layer 4: Metadata Isolation
- spatial_ref_sys: SELECT revoked from PUBLIC
- geometry_columns: SELECT revoked from PUBLIC
- postgis_reader/postgis_writer roles for granular access

### Layer 5: DoS Prevention
- Statement timeout: 30s for spatial queries
- Geometry complexity limits (CHECK constraints)
- GiST index required on all geometry columns

---

## ZTA Mapping

| ZTA Principle | PostGIS Implementation |
|---|---|
| Never trust, always verify | Parameterized queries, input validation |
| Least privilege | postgis_reader/postgis_writer roles, metadata REVOKE |
| Assume breach | RLS filters spatial queries, region isolation |
| Verify explicitly | SRID CHECK constraints, ST_IsValid enforcement |
| Minimize surface | PostGIS in dedicated schema, PUBLIC revoked |

---

## Related Sections
*Detailed content split into sub-pages for readability. See [[concepts/postgis-security-wims-bfp-details]] for the full reference.*

---

*This page is scannable in 30 seconds. Full reference content moved to sub-pages.*
