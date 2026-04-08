---
id: postgresql-security-wims-bfp-concept-001
type: concept
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - sources/software-dev/postgresql-security-best-practices
  - sources/software-dev/postgresql-rls-limitations
  - sources/software-dev/postgresql-cves-2025-2026
  - sources/cybersecurity/nist-sp-800-207-zero-trust-architecture
status: active
tags:
  - postgresql
  - rls
  - security
  - database
  - wims-bfp
  - software-dev
related:
  - sources/software-dev/postgresql-security-best-practices
  - sources/software-dev/postgresql-rls-limitations
  - sources/software-dev/postgresql-cves-2025-2026
  - concepts/secure-coding-practices
  - concepts/zero-trust-architecture
  - rls-null-bypass-fix
  - mocs/cybersecurity
---

# PostgreSQL Security for WIMS-BFP

**Synthesis of:** PostgreSQL best practices, RLS limitations, CVEs, Zero Trust Architecture
**Purpose:** Unified security reference for WIMS-BFP's PostgreSQL database layer

---

## WIMS-BFP's PostgreSQL Security Stack

| Component | Mechanism | ZTA Mapping |
|---|---|---|
| **RLS** (Row Level Security) | Per-user, per-region row filtering | Tenet 3: Per-session access |
| **wims.current_user_id** | SET LOCAL context in every transaction | Tenet 4: Dynamic policy |
| **pgcrypto** | UUID generation via gen_random_uuid() | Tenet 6: Authentication |
| **PostGIS** | Region-based spatial isolation | Microsegmentation (network pillar) |
| **pgAudit** | Audit trail for all queries | Tenet 7: Improve security posture |

---

## The RLS Architecture

```
FastAPI Request
  → get_db(request)
    → SET LOCAL wims.current_user_id = '<user_uuid>'
    → SET LOCAL wims.current_role = 'REGIONAL_ENCODER'
    → SET LOCAL wims.current_region = 'NCR'
  → Query executes
  → RLS policy evaluates against SET LOCAL context
  → Results filtered by user_id / region / role
```

---

## RLS Security Rules (WIMS-BFP)

### Rule 1: Every Transaction Sets Context

```python
# FastAPI middleware — MUST execute before any query
cursor.execute("SET LOCAL wims.current_user_id = %s", (user_id,))
cursor.execute("SET LOCAL wims.current_role = %s", (role,))
cursor.execute("SET LOCAL wims.current_region = %s", (region,))
```

### Rule 2: RLS Policies Use OR Logic (Not AND)

```sql
-- ✅ CORRECT: Single policy with OR
CREATE POLICY incidents_access ON wims.incidents
  FOR ALL USING (
    user_id = current_setting('wims.current_user_id')::uuid
    OR region = current_setting('wims.current_region')::text
    OR current_setting('wims.current_role') IN ('NATIONAL_ANALYST', 'SYSTEM_ADMIN')
  );

-- ❌ WRONG: Multiple policies (AND composition — over-restrictive)
CREATE POLICY p1 ON wims.incidents USING (user_id = ...);
CREATE POLICY p2 ON wims.incidents USING (region = ...);
```

### Rule 3: NULL Safety

```sql
-- ✅ CORRECT: Handle NULL context
USING (
  COALESCE(current_setting('wims.current_user_id', true), '') != ''
  AND user_id = current_setting('wims.current_user_id')::uuid
)

-- ❌ WRONG: NULL context = silent deny (no rows returned)
USING (user_id = current_setting('wims.current_user_id')::uuid)
```

### Rule 4: FORCE ROW LEVEL SECURITY

```sql
ALTER TABLE wims.incidents FORCE ROW LEVEL SECURITY;
ALTER TABLE wims.verification_logs FORCE ROW LEVEL SECURITY;
ALTER TABLE wims.batches FORCE ROW LEVEL SECURITY;
-- All wims.* operational tables
```

### Rule 5: Child Table Policies

Every child table needs its own policy — policies don't inherit:

```sql
-- verification_logs references incidents
CREATE POLICY verification_logs_access ON wims.verification_logs
  FOR ALL USING (
    incident_id IN (
      SELECT id FROM wims.incidents
      WHERE user_id = current_setting('wims.current_user_id')::uuid
      OR region = current_setting('wims.current_region')::text
    )
  );
```

---

## Known RLS Limitations and WIMS-BFP Mitigations

| Limitation | Impact | WIMS-BFP Fix |
|---|---|---|
| Post-processing filter (slow) | Query planner can't optimize | Index RLS columns (user_id, region) |
| AND composition | Over-restrictive with multiple policies | Single policy with OR logic |
| NULL bypass | NULL = NULL → FALSE → silent deny | COALESCE, NOT NULL constraints |
| Owner bypass | Table owner sees everything | FORCE ROW LEVEL SECURITY |
| JOIN performance | Row-by-row RLS evaluation | Materialized views for reports |
| View bypass | Views owned by DBA bypass RLS | security_invoker = true |

---

## Security Audit Checklist

### Authentication
```
[ ] pg_hba.conf: scram-sha-256 (not trust, not md5)
[ ] TLS enabled: SHOW ssl = on
[ ] No superuser for application connections
[ ] Dedicated service accounts (svc_backend, svc_celery, svc_analyst)
```

### Authorization
```
[ ] RLS enabled on ALL wims.* operational tables
[ ] FORCE ROW LEVEL SECURITY set on all tables
[ ] USING clause on every policy (read control)
[ ] WITH CHECK clause on every INSERT/UPDATE policy (write control)
[ ] SET LOCAL wims.current_user_id in every transaction
[ ] Child tables have independent policies
[ ] NULL checks in all RLS predicates
[ ] Indexes on RLS predicate columns
```

### CVEs
```
[ ] PostgreSQL version ≥17.3 (CVE-2025-1094 fix)
[ ] PostgreSQL version ≥17.6 (CVE-2025-8714 fix)
[ ] No interactive psql for production restores
[ ] Encoding verification: client_encoding, server_encoding
```

### Encryption
```
[ ] pgcrypto for gen_random_uuid()
[ ] TLS for all remote connections
[ ] No plaintext passwords in wims.users
[ ] Key rotation policy for SSL certificates
```

### Auditing
```
[ ] pgAudit installed and configured
[ ] Failed login attempts logged
[ ] RLS denials logged
[ ] Schema changes logged
```

---

## Related

- [[concepts/zero-trust-architecture]] — ZTA framework mapping
- [[concepts/secure-coding-practices]] — OWASP/CWE coding standards
- [[sources/software-dev/postgresql-security-best-practices]] — PostgreSQL security reference
- [[sources/software-dev/postgresql-rls-limitations]] — RLS pitfalls and NULL bypass
- [[sources/software-dev/postgresql-cves-2025-2026]] — PostgreSQL CVEs
- [[rls-null-bypass-fix]] — WIMS-BFP-specific NULL bypass fix skill
- [[mocs/cybersecurity]] — Cybersecurity Map of Content
