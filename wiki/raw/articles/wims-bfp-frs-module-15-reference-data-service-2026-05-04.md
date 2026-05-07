# FRS Module 15 — Reference Data Service

> **Status:** NEW MODULE
> **Implementation:** `api/ref.py`
> **Rationale:** Geographic hierarchy lookup API (regions, provinces, cities) used as a shared dependency across Modules 2, 5, 5d, and 9. Not previously documented in FRS. Provides consistent reference data to all authenticated modules without coupling to operational data models.

---

## Module 15: Reference Data Service

### 15.1 Overview

| Attribute | Detail |
|-----------|--------|
| Module ID | 15 |
| Category | Shared Infrastructure / Reference Data |
| Auth Required | Yes (any authenticated WIMS role) |
| Implementation | `src/backend/api/routes/ref.py` |
| Endpoints | `GET /api/ref/regions`, `GET /api/ref/provinces`, `GET /api/ref/cities` |

### 15.2 Purpose

The Reference Data Service provides a read-only authenticated API for querying the geographic hierarchy used throughout the system — regions, provinces, and cities/municipalities. All authenticated modules requiring geographic lookups (incident submission, analytics filtering, geographic boundary enforcement, report generation) depend on this service rather than querying operational tables directly. This separation ensures consistent reference data across modules and isolates geographic schema changes from operational queries.

### 15.3 Functional Specification

**15.3.1 Regions Lookup**

- `GET /api/ref/regions`
- Returns: `region_id`, `region_name`, `region_code`
- Optional filter: `region_id` (single)
- Requires: Any authenticated WIMS user role

**15.3.2 Provinces Lookup**

- `GET /api/ref/provinces`
- Returns: `province_id`, `province_name`, `region_id`
- Optional filter: `region_id` (single)
- Requires: Any authenticated WIMS user role

**15.3.3 Cities Lookup**

- `GET /api/ref/cities`
- Returns: `city_id`, `city_name`, `province_id`
- Optional filters: `province_id` (single), `province_ids` (comma-separated list)
- Supports batch lookup for analytics multi-province comparison
- Requires: Any authenticated WIMS user role

### 15.4 Role Usage

| Consuming Module | Usage |
|----------------|-------|
| Module 2 (Offline Incident Mgmt) | Form dropdowns for region/province/city selection |
| Module 5 (Analytics) | `province_ids` filter for regional comparison queries |
| Module 5d (Public Submission) | Region auto-resolution via centroid |
| Module 9 (System Monitoring) | Geographic context in health reports |
| Module 12 (User Admin) | Assigning users to `assigned_region_id` |

### 15.5 Data Source

- All reference data sourced from `wims.ref_regions`, `wims.ref_provinces`, `wims.ref_cities`
- Read-only; no write endpoints exposed
- RLS policies applied — users see only reference data for their assigned region (except NATIONAL_ANALYST and SYSTEM_ADMIN who see all)

### 15.6 Out of Scope

- Write operations on reference data (managed via database seed scripts)
- Hierarchical tree representation (flat lists returned; frontend builds the tree)
- Real-time reference data sync between systems
