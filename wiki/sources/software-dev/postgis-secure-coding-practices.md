---
id: postgis-secure-coding-practices-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-07-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - https://postgis.net/workshops/postgis-intro/security.html
  - https://nvd.nist.gov/vuln/detail/CVE-2025-69662
  - https://aydinnyunus.github.io/2025/12/27/sql-injection-geopandas/
  - https://www.cvedetails.com/product/65981/Postgis-Postgis.html
status: active
tags:
  - postgis
  - postgresql
  - spatial
  - security
  - sql-injection
  - rls
  - wims-bfp
related:
  - concepts/postgresql-security-wims-bfp
  - sources/software-dev/postgresql-security-best-practices
  - sources/software-dev/postgresql-rls-limitations
---

# PostGIS Secure Coding Practices

**PostGIS Version:** 3.x (latest stable)
**PostgreSQL Compatibility:** 14-16
**WIMS-BFP Usage:** Incident geolocation, regional boundary enforcement, spatial queries for BFP operations

---

## 1. PostGIS Attack Surface

PostGIS extends PostgreSQL with spatial types and functions. This introduces unique attack vectors beyond standard SQL injection:

| Vector | Risk | Description |
|---|---|---|
| Spatial SQL Injection | CRITICAL | User-controlled WKT/WKB input injected into geometry constructors |
| Geometry Validation Bypass | HIGH | Malformed geometries cause crashes, incorrect spatial results, or DoS |
| Metadata Table Exposure | MEDIUM | `spatial_ref_sys`, `geometry_columns` leak SRID/schema info if over-granted |
| Client Library Injection | HIGH | GeoPandas `to_postgis()`, Shapely, GDAL — unsanitized params in spatial queries |
| SRID Confusion | MEDIUM | Wrong SRID causes silent coordinate shifts, bypasses regional RLS |
| Computation DoS | MEDIUM | Complex geometries (10K+ vertices) exhaust CPU on spatial operations |

---

## 2. CVEs (2025-2026)

### CVE-2025-69662 — GeoPandas `to_postgis()` SQL Injection

| Field | Value |
|---|---|
| **CVE** | CVE-2025-69662 |
| **CVSS 3.1** | 9.8 Critical (AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N) |
| **CWE** | CWE-89 (SQL Injection) |
| **Affected** | GeoPandas < 1.1.2 |
| **Component** | `geopandas/io/sql.py`, line 434 |
| **Attack Vector** | `geom_name` parameter via `rename_geometry()` |
| **Impact** | Data theft, data modification, system command execution |

**Vulnerable Code:**
```python
# ❌ VULNERABLE — f-string interpolation into SQL
target_srid = connection.execute(
    text(f"SELECT Find_SRID('{schema_name}', '{name}', '{geom_name}');")
).fetchone()[0]
```

**Exploit:**
```python
# Attacker-controlled geometry column name
malicious_geom_name = "geom'); SELECT CAST(version() AS int); --"
gdf = gdf.rename_geometry(malicious_geom_name)
gdf.to_postgis(name="test_table", con=engine, if_exists="append")
# Result: PostgreSQL version leaked via error-based injection
```

**Fixed Code:**
```python
# ✅ FIXED — parameterized query
target_srid = connection.execute(
    text("SELECT Find_SRID(:schema_name, :name, :geom_name);")
    .bindparams(schema_name=schema_name, name=name, geom_name=geom_name)
).fetchone()[0]
```

**WIMS-BFP Impact:** If using GeoPandas for spatial data ingestion (Suricata geo-IP, incident coordinates), upgrade to >= 1.1.2 immediately.

---

## 3. Spatial SQL Injection Prevention

### 3.1 Geometry Constructors — NEVER Interpolate User Input

```python
# ❌ CRITICAL VULNERABILITY — string interpolation into WKT
user_lat = request.json['lat']
user_lon = request.json['lon']
query = f"SELECT * FROM incidents WHERE ST_DWithin(geom, ST_GeomFromText('POINT({user_lon} {user_lat})'), 1000)"

# ✅ SAFE — parameterized query with ST_MakePoint
query = "SELECT * FROM incidents WHERE ST_DWithin(geom, ST_MakePoint(%s, %s)::geography, 1000)"
cursor.execute(query, (user_lon, user_lat))
```

### 3.2 WKT/WKB Input Validation

```python
# ❌ UNSAFE — raw WKT from user input
wkt = request.json['boundary']  # User-controlled WKT
query = f"INSERT INTO regions (geom) VALUES (ST_GeomFromText('{wkt}'))"

# ✅ SAFE — validate and parameterize
from shapely import wkt as shapely_wkt
from shapely.geometry import shape

def safe_geometry_from_input(geojson_or_wkt: str, max_vertices: int = 1000) -> str:
    """Validate and sanitize geometry input."""
    try:
        if geojson_or_wkt.strip().startswith('{'):
            # GeoJSON
            geom = shape(json.loads(geojson_or_wkt))
        else:
            # WKT
            geom = shapely_wkt.loads(geojson_or_wkt)
    except Exception:
        raise ValueError("Invalid geometry format")

    # Reject empty geometries
    if geom.is_empty:
        raise ValueError("Empty geometry not allowed")

    # Reject excessively complex geometries (DoS prevention)
    if hasattr(geom, 'exterior') and len(geom.exterior.coords) > max_vertices:
        raise ValueError(f"Geometry too complex: {len(geom.exterior.coords)} vertices (max {max_vertices})")

    # Validate geometry
    if not geom.is_valid:
        geom = geom.buffer(0)  # Attempt self-repair
        if not geom.is_valid:
            raise ValueError("Invalid geometry (self-repair failed)")

    return geom.wkt
```

### 3.3 FastAPI + psycopg2 Safe Pattern (WIMS-BFP)

```python
# ✅ SAFE — parameterized spatial query with psycopg2
from psycopg2.extras import RealDictCursor

def get_nearby_incidents(db, lat: float, lon: float, radius_m: int = 5000):
    query = """
        SELECT i.incident_id, i.title, i.status,
               ST_Distance(i.geom, ST_MakePoint(%s, %s)::geography) AS distance_m
        FROM wims.incidents i
        WHERE ST_DWithin(
            i.geom,
            ST_MakePoint(%s, %s)::geography,
            %s
        )
        ORDER BY distance_m
        LIMIT 100
    """
    with db.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, (lon, lat, lon, lat, radius_m))
        return cur.fetchall()
```

---

## 4. PostGIS Metadata Access Control

PostGIS requires read access to metadata tables for spatial operations. Over-granting is a common mistake.

### Required Metadata Tables

| Table | Required For | Minimum Grant |
|---|---|---|
| `geometry_columns` | Schema introspection, ORMs | `SELECT` |
| `geography_columns` | Geography type queries | `SELECT` |
| `spatial_ref_sys` | `ST_Transform()`, SRID lookups | `SELECT` |

### Role-Based PostGIS Access (WIMS-BFP Pattern)

```sql
-- Read-only spatial role (CIVILIAN_REPORTER, NATIONAL_ANALYST)
CREATE ROLE postgis_reader NOLOGIN;
GRANT USAGE ON SCHEMA public TO postgis_reader;
GRANT SELECT ON geometry_columns TO postgis_reader;
GRANT SELECT ON geography_columns TO postgis_reader;
GRANT SELECT ON spatial_ref_sys TO postgis_reader;

-- Read-write spatial role (REGIONAL_ENCODER, NATIONAL_VALIDATOR)
CREATE ROLE postgis_writer NOLOGIN;
GRANT postgis_reader TO postgis_writer;
GRANT INSERT, UPDATE, DELETE ON spatial_ref_sys TO postgis_writer;

-- Assign to FRS roles
GRANT postgis_reader TO svc_analyst;      -- NATIONAL_ANALYST
GRANT postgis_writer TO svc_encoder;       -- REGIONAL_ENCODER
GRANT postgis_writer TO svc_validator;     -- NATIONAL_VALIDATOR
```

### Metadata Table Hardening

```sql
-- ❌ NEVER grant to PUBLIC
-- GRANT SELECT ON spatial_ref_sys TO PUBLIC;  -- default in some installs

-- ✅ REVOKE default PUBLIC access, grant explicitly
REVOKE ALL ON spatial_ref_sys FROM PUBLIC;
REVOKE ALL ON geometry_columns FROM PUBLIC;
REVOKE ALL ON geography_columns FROM PUBLIC;

-- Grant only to roles that need spatial operations
GRANT SELECT ON spatial_ref_sys TO postgis_reader;
```

---

## 5. Geometry Validation and DoS Prevention

### 5.1 Input Validation Gates

```sql
-- Create a CHECK constraint for geometry validation
ALTER TABLE wims.incidents
    ADD CONSTRAINT valid_geom CHECK (ST_IsValid(geom));

-- Reject geometries exceeding vertex limits
ALTER TABLE wims.incidents
    ADD CONSTRAINT geom_complexity CHECK (
        ST_NPoints(geom) <= 10000
    );

-- Enforce SRID consistency
ALTER TABLE wims.incidents
    ADD CONSTRAINT correct_srid CHECK (ST_SRID(geom) = 4326);
```

### 5.2 Application-Level Geometry Sanitization

```python
def sanitize_spatial_input(geojson: dict, max_vertices: int = 5000) -> dict:
    """Validate and repair geometry before database insertion."""
    from shapely.geometry import shape
    from shapely.validation import make_valid

    geom = shape(geojson)

    # 1. Reject empty
    if geom.is_empty:
        raise ValueError("Empty geometry rejected")

    # 2. Reject overly complex (DoS prevention)
    if geom.num_coords > max_vertices:
        raise ValueError(f"Geometry exceeds {max_vertices} vertex limit")

    # 3. Validate and repair
    if not geom.is_valid:
        geom = make_valid(geom)
        if not geom.is_valid:
            raise ValueError("Geometry invalid after repair")

    # 4. Reject degenerate geometries (zero-area polygons)
    if geom.geom_type == 'Polygon' and geom.area == 0:
        raise ValueError("Degenerate polygon (zero area)")

    return geom.__geo_interface__
```

### 5.3 Query Timeout for Spatial Operations

```sql
-- Set statement timeout for spatial queries (prevent DoS)
SET statement_timeout = '30s';

-- Complex spatial join with timeout protection
SELECT a.id, b.id
FROM large_table_a a
JOIN large_table_b b ON ST_Intersects(a.geom, b.geom)
LIMIT 10000;
```

```python
# FastAPI middleware for spatial query timeout
from contextlib import contextmanager

@contextmanager
def spatial_query_timeout(db, timeout_seconds: int = 30):
    """Set per-query timeout for spatial operations."""
    cursor = db.cursor()
    cursor.execute(f"SET LOCAL statement_timeout = '{timeout_seconds}s'")
    try:
        yield cursor
    finally:
        cursor.execute("RESET statement_timeout")
```

---

## 6. RLS + PostGIS Integration (WIMS-BFP)

Spatial queries must respect RLS policies. Common pitfalls:

### 6.1 ST_DWithin Bypass Risk

```sql
-- ❌ DANGER: If RLS filters by region_id but spatial query ignores it,
-- a user can retrieve incidents outside their region via proximity search
SELECT * FROM wims.incidents
WHERE ST_DWithin(geom, ST_MakePoint(%s, %s)::geography, 50000);
-- Returns ALL nearby incidents, including other regions

-- ✅ SAFE: RLS policy must include spatial + region enforcement
CREATE POLICY incidents_select_regional ON wims.incidents
    FOR SELECT USING (
        region_id = current_setting('wims.current_region_id')::integer
    );
-- RLS automatically filters — spatial query only sees authorized rows
```

### 6.2 Spatial Index Performance + Security

```sql
-- GiST index for spatial queries (required for performance)
CREATE INDEX idx_incidents_geom ON wims.incidents USING GIST (geom);

-- Combined spatial + region index for RLS-filtered queries
CREATE INDEX idx_incidents_geom_region
    ON wims.incidents USING GIST (geom, region_id);
```

### 6.3 SRID Consistency for Regional Boundaries

```sql
-- ✅ Enforce SRID 4326 (WGS84) globally for WIMS-BFP
ALTER TABLE wims.regions
    ADD CONSTRAINT regions_srid CHECK (ST_SRID(boundary_geom) = 4326);

ALTER TABLE wims.incidents
    ADD CONSTRAINT incidents_srid CHECK (ST_SRID(geom) = 4326);

-- If SRIDs are mixed, ST_DWithin returns WRONG results silently
-- Example: mixing 4326 (degrees) with 3857 (meters) gives 100x distance errors
```

---

## 7. Secure Spatial Query Patterns

### 7.1 Parameterized Geometry Insert (psycopg2)

```python
def insert_incident(db, title: str, lat: float, lon: float, region_id: int):
    """Safe geometry insertion with parameterized query."""
    query = """
        INSERT INTO wims.incidents (title, region_id, geom)
        VALUES (%s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
        RETURNING incident_id
    """
    with db.cursor() as cur:
        cur.execute(query, (title, region_id, lon, lat))
        db.commit()
        return cur.fetchone()[0]
```

### 7.2 Safe Spatial Search (GeoJSON Output)

```python
def search_nearby(db, lat: float, lon: float, radius_m: int) -> list[dict]:
    """Safe spatial search with GeoJSON output."""
    query = """
        SELECT
            i.incident_id,
            i.title,
            ST_AsGeoJSON(i.geom)::json AS geometry,
            ST_Distance(i.geom, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography) AS distance_m
        FROM wims.incidents i
        WHERE ST_DWithin(
            i.geom,
            ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
            %s
        )
        AND i.region_id = current_setting('wims.current_region_id')::integer
        ORDER BY distance_m
        LIMIT 50
    """
    with db.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, (lon, lat, lon, lat, radius_m))
        return cur.fetchall()
```

### 7.3 Region Boundary Enforcement

```python
def validate_incident_in_region(db, lat: float, lon: float, region_id: int) -> bool:
    """Verify incident coordinates fall within assigned region boundary."""
    query = """
        SELECT EXISTS(
            SELECT 1 FROM wims.regions r
            WHERE r.region_id = %s
            AND ST_Contains(
                r.boundary_geom,
                ST_SetSRID(ST_MakePoint(%s, %s), 4326)
            )
        )
    """
    with db.cursor() as cur:
        cur.execute(query, (region_id, lon, lat))
        return cur.fetchone()[0]
```

---

## 8. WIMS-BFP PostGIS Audit Checklist

| # | Check | Status |
|---|---|---|
| 1 | No f-string/format interpolation in ST_GeomFromText, ST_MakePoint, Find_SRID | ☐ |
| 2 | All spatial queries use parameterized placeholders (%s or :param) | ☐ |
| 3 | WKT/WKB input validated with Shapely before DB insertion | ☐ |
| 4 | Geometry vertex count limited (max 10000) | ☐ |
| 5 | ST_IsValid() enforced via CHECK constraint or app logic | ☐ |
| 6 | SRID 4326 enforced via CHECK constraint on all geometry columns | ☐ |
| 7 | spatial_ref_sys SELECT revoked from PUBLIC, granted only to postgis_reader | ☐ |
| 8 | geometry_columns SELECT revoked from PUBLIC, granted only to postgis_reader | ☐ |
| 9 | RLS policies filter spatial queries by region_id | ☐ |
| 10 | GiST spatial indexes created on all geometry columns | ☐ |
| 11 | Statement timeout set for spatial queries (30s default) | ☐ |
| 12 | GeoPandas >= 1.1.2 (CVE-2025-69662 patched) | ☐ |
| 13 | Region boundary validated before incident insertion | ☐ |
| 14 | No spatial functions in SECURITY DEFINER (privilege escalation risk) | ☐ |
| 15 | PostGIS extension installed in dedicated schema (not public) | ☐ |

---

## 9. PostGIS Extension Hardening

```sql
-- ✅ Install PostGIS in dedicated schema (not public)
CREATE SCHEMA IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA postgis;

-- Grant usage only to roles that need spatial operations
GRANT USAGE ON SCHEMA postgis TO postgis_reader;

-- ✅ Revoke from PUBLIC
REVOKE ALL ON SCHEMA postgis FROM PUBLIC;
```

---

## 10. Related

- [[concepts/postgresql-security-wims-bfp]] — PostgreSQL security layer
- [[sources/software-dev/postgresql-security-best-practices]] — Base PostgreSQL hardening
- [[sources/software-dev/postgresql-rls-limitations]] — RLS pitfalls
