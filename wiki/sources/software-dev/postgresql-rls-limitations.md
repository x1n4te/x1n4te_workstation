---
id: postgresql-rls-limitations-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - bytebase.com/blog/postgres-row-level-security-limitations-and-alternatives/
  - supabase.com/docs/guides/database/postgres/row-level-security
status: active
tags:
  - postgresql
  - rls
  - security
  - database
  - vulnerability
  - software-dev
related:
  - sources/software-dev/postgresql-security-best-practices
  - sources/software-dev/postgresql-cves-2025-2026
  - concepts/postgresql-security-wims-bfp
  - rls-null-bypass-fix
  - mocs/cybersecurity
---

# PostgreSQL RLS Limitations and Pitfalls

**Sources:** Bytebase, Supabase Docs
**Type:** Security analysis — RLS failure modes
**Confidence:** High — based on PostgreSQL source behavior + real-world deployments

---

## 6 Limitations of PostgreSQL RLS

### 1. Post-Processing Security Filter (Performance)

RLS policies are evaluated **for every single row** during query execution — they're NOT part of query optimization. This means:

```sql
-- RLS adds a WHERE clause AFTER query planning
-- The planner doesn't know about RLS filters
SELECT * FROM wims.incidents WHERE severity = 'HIGH';
-- Internally becomes:
-- SELECT * FROM wims.incidents WHERE severity = 'HIGH' AND <rls_policy>;
-- But the planner optimized WITHOUT knowing about the RLS filter
```

**Impact:** Performance degrades on large tables because the planner can't optimize around RLS predicates.

**WIMS-BFP Mitigation:** Add indexes on columns used in RLS predicates (user_id, region).

### 2. AND Composition (Policy Overlap)

Multiple RLS policies on the same table are combined with **AND logic**:

```sql
-- Policy 1: user sees own incidents
CREATE POLICY p1 ON wims.incidents USING (user_id = current_setting('wims.current_user_id'));

-- Policy 2: user sees incidents in their region
CREATE POLICY p2 ON wims.incidents USING (region = current_setting('wims.current_region'));

-- Result: user sees ONLY incidents that are BOTH their own AND in their region
-- NOT: user sees incidents that are either their own OR in their region
```

**Impact:** Unintended over-restriction — users can't see their own incidents in other regions.

**WIMS-BFP Mitigation:** Use OR logic within a single policy, not multiple policies with AND.

### 3. NULL Value Bypass

`NULL = NULL` evaluates to `NULL` (not `TRUE`), which is treated as `FALSE` in RLS predicates:

```sql
-- If user_id is NULL in the table, this policy DENIES access to that row
USING (user_id = current_setting('wims.current_user_id')::uuid)

-- But if current_setting returns NULL (not set), ALL rows are denied
-- This is a silent failure — no error, just empty results
```

**Impact:** Users with NULL user_id in the database lose access to their own data.

**WIMS-BFP Mitigation:** Never allow NULL in RLS-referenced columns. Use COALESCE or IS NOT NULL guards.

### 4. Owner Bypass (Unless FORCED)

By default, the table owner bypasses ALL RLS policies:

```sql
-- Owner can see everything unless explicitly forced
ALTER TABLE wims.incidents FORCE ROW LEVEL SECURITY;

-- Without FORCE, a compromised owner account = full data access
```

**Impact:** False sense of security if RLS is enabled but FORCE is not set.

**WIMS-BFP Mitigation:** Always use FORCE ROW LEVEL SECURITY on all wims.* tables.

### 5. JOIN Performance (Row-by-Row Evaluation)

RLS is evaluated for joined rows individually:

```sql
-- Each joined row triggers RLS evaluation
SELECT i.*, v.* FROM incidents i JOIN verifications v ON i.id = v.incident_id;
-- RLS on 'incidents' evaluated for EACH matched row
-- RLS on 'verifications' evaluated for EACH matched row
-- Cartesian explosion possible on large joins
```

**Impact:** Queries with JOINs across multiple RLS-enabled tables are significantly slower.

**WIMS-BFP Mitigation:** Keep JOINs minimal. Use materialized views for reporting queries.

### 6. Views Can Bypass RLS

Views created by the table owner can bypass RLS unless explicitly configured:

```sql
-- This view bypasses RLS because it's owned by the DBA
CREATE VIEW wims.all_incidents AS SELECT * FROM wims.incidents;

-- Fix: use security_invoker
CREATE VIEW wims.all_incidents
  WITH (security_invoker = true)
  AS SELECT * FROM wims.incidents;
```

**Impact:** Reporting views can leak data if not created with `security_invoker`.

---

## RLS vs. Views — When to Use Which

| Factor | RLS | Views |
|---|---|---|
| Security enforcement | Per-row filter | Per-query filter |
| Performance | Post-processing (slower) | Part of query plan (faster) |
| Complexity | Policy logic in DB | Logic in view definition |
| Multi-tenancy | Excellent | Possible but harder |
| RLS-able by owner | Only with FORCE | Yes (unless security_invoker) |

---

## WIMS-BFP RLS Audit Checklist

```
[ ] FORCE ROW LEVEL SECURITY on all wims.* tables
[ ] NULL checks in all RLS predicates (COALESCE, IS NOT NULL)
[ ] OR logic within single policy (not multiple AND policies)
[ ] Indexes on RLS predicate columns (user_id, region, role)
[ ] security_invoker = true on all views
[ ] No owner-bypassing functions (SECURITY DEFINER without RLS context)
[ ] SET LOCAL wims.current_user_id never returns NULL
[ ] Child tables have independent policies (not just inherited)
```

---

## Related Pages

- [[sources/software-dev/postgresql-security-best-practices]] — PostgreSQL security reference
- [[sources/software-dev/postgresql-cves-2025-2026]] — PostgreSQL CVEs
- [[concepts/postgresql-security-wims-bfp]] — WIMS-BFP PostgreSQL security synthesis
- [[rls-null-bypass-fix]] — WIMS-BFP-specific NULL bypass fix skill
- [[mocs/cybersecurity]] — Cybersecurity Map of Content
