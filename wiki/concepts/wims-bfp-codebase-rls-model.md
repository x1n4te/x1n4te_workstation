---
id: wims-bfp-codebase-rls-model-001
type: concept
created: 2026-04-21
updated: 2026-04-21
last_verified: 2026-04-21
review_after: 2026-06-21
stale_after: 2026-10-21
confidence: high
source_refs:
  - raw/sources/wims-bfp-codebase/docs/SECURITY.md
  - raw/sources/wims-bfp-codebase/docs/DATABASE.md
status: active
tags:
  - wims-bfp
  - database
  - rls
  - security
  - postgres
related:
  - entities/wims-bfp-codebase-database-schema
  - entities/wims-bfp-codebase-rbac-roles
  - concepts/wims-bfp-codebase-auth-flow
---

# Row Level Security (RLS) Model

All `wims.*` tables have RLS enabled. Security enforced at the database level, not just route guards.

## Mechanism

PostgreSQL session variables set per-request via `SET LOCAL`:

```sql
SET LOCAL wims.current_user_id = '<user_uuid>';
SET LOCAL wims.current_user_role = 'REGIONAL_ENCODER';
SET LOCAL wims.current_user_region_id = '1';
```

## Helper Functions

```sql
wims.current_user_uuid()      → current_setting('wims.current_user_id')::uuid
wims.current_user_role()      → current_setting('wims.current_user_role')
wims.current_user_region_id() → current_setting('wims.current_user_region_id')::int
```

## Policy Patterns

### Regional Scoping
`REGIONAL_ENCODER` sees only incidents in their `assigned_region_id`:
```sql
CREATE POLICY incidents_read_regional ON wims.fire_incidents
  FOR SELECT USING (
    current_user_role() = 'REGIONAL_ENCODER'
    AND region_id = current_user_region_id()
  );
```

### Global Read
`NATIONAL_ANALYST` and `SYSTEM_ADMIN` see all rows:
```sql
CREATE POLICY incidents_read_global ON wims.fire_incidents
  FOR SELECT USING (
    current_user_role() IN ('NATIONAL_ANALYST', 'SYSTEM_ADMIN')
  );
```

### Validator Access
`NATIONAL_VALIDATOR` can read all incidents for verification:
```sql
CREATE POLICY incidents_read_validator ON wims.fire_incidents
  FOR SELECT USING (
    current_user_role() = 'NATIONAL_VALIDATOR'
  );
```

### Insert Policies
- `REGIONAL_ENCODER`: can INSERT only in their region
- `CIVILIAN_REPORTER`: can INSERT into `citizen_reports` only

### Update Policies
- `REGIONAL_ENCODER`: can UPDATE only non-verified incidents in their region
- `NATIONAL_VALIDATOR`: can UPDATE `is_verified` status on any incident

### No DELETE Policies
Constitution mandate: no hard deletes. All tables use `deleted_at` soft-delete.

## Test Pattern

```python
# Tests that need RLS should use get_db_with_rls()
async def test_regional_scoping():
    async with get_db_with_rls(
        user_id="uuid",
        role="REGIONAL_ENCODER",
        region_id=1
    ) as db:
        result = await db.execute(select(FireIncident))
        incidents = result.scalars().all()
        # Only incidents from region 1 should be returned
```

## Related

- [[entities/wims-bfp-codebase-database-schema]] — tables with RLS enabled
- [[entities/wims-bfp-codebase-rbac-roles]] — role definitions
- [[concepts/wims-bfp-codebase-auth-flow]] — how RLS context is set per-request
