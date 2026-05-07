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

# PostGIS Security — Detailed Reference

Back to overview: [[concepts/postgis-security-wims-bfp]]
## Critical Rules for WIMS-BFP

1. **ST_MakePoint, NOT ST_GeomFromText** — ST_MakePoint accepts numeric params directly (no WKT parsing = no injection surface)
2. **Always SET wims.current_region_id** — RLS depends on this; missing = data leak across regions
3. **Validate geometry BEFORE DB** — Shapely in application layer, CHECK constraint in DB
4. **GeoPandas >= 1.1.2** — CVE-2025-69662 is critical; any version < 1.1.2 is exploitable
5. **SRID 4326 everywhere** — Mixed SRIDs cause silent distance errors, bypass regional boundaries

---

## Audit Checklist Summary

15-point checklist in [[sources/software-dev/postgis-secure-coding-practices]] §8. Key items:
- No string interpolation in spatial constructors
- Parameterized queries everywhere
- Geometry validation at app + DB layer
- Metadata table access hardened
- RLS + spatial filtering integrated

---

## Related

- [[sources/software-dev/postgis-secure-coding-practices]] — Full secure coding guide
- [[concepts/postgresql-security-wims-bfp]] — PostgreSQL base security
- [[concepts/keycloak-fastapi-security-wims-bfp]] — Auth layer
- [[concepts/docker-security-wims-bfp]] — Container security
