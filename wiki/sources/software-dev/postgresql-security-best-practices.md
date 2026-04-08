---
id: postgresql-security-best-practices-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - dev.to/hardikkanajariya/day-13-security-best-practices-locking-down-your-postgresql-data-2l8o
  - permit.io/blog/postgres-rls-implementation-guide
  - hoop.dev/blog/row-level-security-in-postgresql-the-last-line-of-defense-for-your-data
status: active
tags:
  - postgresql
  - security
  - rls
  - database
  - software-dev
related:
  - sources/software-dev/postgresql-rls-limitations
  - sources/software-dev/postgresql-cves-2025-2026
  - concepts/postgresql-security-wims-bfp
  - concepts/secure-coding-practices
  - mocs/cybersecurity
---

# PostgreSQL Security Best Practices (Source Summary)

**Sources:** PostgreSQL docs, Dev.to, Permit.io, Hoop.dev
**Type:** Database security reference
**Confidence:** High — PostgreSQL official + industry best practices

---

## 4 Security Layers

| Layer | Question | Mechanism |
|---|---|---|
| **Authentication** | "Who are you?" | pg_hba.conf, SCRAM-SHA-256, TLS |
| **Authorization** | "What can you do?" | Roles, GRANT/REVOKE, RLS |
| **Encryption** | "Is data protected?" | TLS (in transit), pgcrypto (at rest), key management |
| **Auditing** | "What happened?" | pgAudit, log_statement, audit triggers |

---

## Authentication Best Practices

### pg_hba.conf Configuration

```
# ORDER MATTERS — first match wins

# Local: require SCRAM-SHA-256 (not trust, not md5)
local   all   all   scram-sha-256

# Remote: require TLS + SCRAM
hostssl all   all   0.0.0.0/0   scram-sha-256

# Reject everything else
host    all   all   0.0.0.0/0   reject
```

### Password Hashing

| Method | Security | WIMS-BFP Status |
|---|---|---|
| `trust` | ❌ NEVER use | ✅ Not used |
| `md5` | ⚠️ Weak, rainbow-table vulnerable | ✅ Not used |
| `scram-sha-256` | ✅ Strong (salt + iterations) | ✅ Recommended |

### Connection Encryption

```sql
-- Verify SSL is active
SHOW ssl;

-- Force SSL for specific users
ALTER ROLE app_user SET ssl = on;
```

---

## Authorization Best Practices

### Role-Based Access Control (RBAC)

```sql
-- Create group roles (job functions)
CREATE ROLE readonly;
CREATE ROLE readwrite;
CREATE ROLE admin;

-- Grant privileges to groups (not individuals)
GRANT SELECT ON ALL TABLES IN SCHEMA wims TO readonly;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA wims TO readwrite;
GRANT ALL PRIVILEGES ON SCHEMA wims TO admin;

-- Assign groups to login roles
GRANT readonly TO analyst_user;
GRANT readwrite TO encoder_user;
GRANT admin TO sysadmin_user;
```

### Principle of Least Privilege

- Never use `SUPERUSER` for application connections
- Create dedicated roles per service: `svc_backend`, `svc_celery`, `svc_analyst`
- Use `SET ROLE` for temporary elevation instead of persistent grants
- Revoke default public schema access: `REVOKE CREATE ON SCHEMA public FROM PUBLIC`

---

## RLS Best Practices

### Enable RLS on Every Operational Table

```sql
-- Enable RLS
ALTER TABLE wims.incidents ENABLE ROW LEVEL SECURITY;

-- Force RLS even for table owners
ALTER TABLE wims.incidents FORCE ROW LEVEL SECURITY;
```

### Policy Design Patterns

```sql
-- Pattern 1: User-scoped access (private data)
CREATE POLICY incidents_user_scoped ON wims.incidents
  FOR ALL USING (user_id = current_setting('wims.current_user_id')::uuid);

-- Pattern 2: Region-scoped access (operational data)
CREATE POLICY incidents_region_scoped ON wims.incidents
  FOR ALL USING (
    region = current_setting('wims.current_region')::text
    OR current_setting('wims.current_role') IN ('NATIONAL_ANALYST', 'SYSTEM_ADMIN')
  );

-- Pattern 3: Public DMZ (civilian reporting only)
CREATE POLICY dmz_insert_only ON wims.dmz_incidents
  FOR INSERT WITH CHECK (true);  -- Anyone can insert
CREATE POLICY dmz_no_read ON wims.dmz_incidents
  FOR SELECT USING (false);  -- Nobody reads (air-locked)
```

### RLS Checklist

```
[ ] RLS enabled on ALL wims.* operational tables
[ ] FORCE ROW LEVEL SECURITY set (owner can't bypass)
[ ] USING clause on every policy (read access control)
[ ] WITH CHECK clause on every INSERT/UPDATE policy (write access control)
[ ] SET LOCAL wims.current_user_id called in every transaction
[ ] Child tables have policies (not just parent)
[ ] NULL values tested (NULL = NULL is NULL, not true)
[ ] Indexes on columns used in RLS predicates (performance)
```

---

## WIMS-BFP Specific Patterns

### Current User Context

```sql
-- FastAPI sets this at the start of every transaction:
SET LOCAL wims.current_user_id = 'uuid-of-authenticated-user';
SET LOCAL wims.current_role = 'REGIONAL_ENCODER';
SET LOCAL wims.current_region = 'NCR';
```

### wims.users Table (Must Exist for RLS)

```sql
CREATE TABLE wims.users (
  user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  keycloak_id TEXT UNIQUE NOT NULL,
  role TEXT NOT NULL CHECK (role IN (
    'CIVILIAN_REPORTER',
    'REGIONAL_ENCODER',
    'NATIONAL_VALIDATOR',
    'NATIONAL_ANALYST',
    'SYSTEM_ADMIN'
  )),
  region TEXT,  -- NULL for NATIONAL_ANALYST and SYSTEM_ADMIN
  is_active BOOLEAN DEFAULT true
);
```

### Service Account (svc_suricata)

```sql
-- Suricata Celery tasks use this account
INSERT INTO wims.users (user_id, keycloak_id, role, region)
VALUES (
  '00000000-0000-0000-0000-000000000001',
  '00000000-0000-0000-0000-000000000000',
  'NATIONAL_ANALYST',
  NULL  -- Global read access
);
```

---

## Related Pages

- [[sources/software-dev/postgresql-rls-limitations]] — RLS pitfalls and NULL bypass
- [[sources/software-dev/postgresql-cves-2025-2026]] — PostgreSQL CVEs
- [[concepts/postgresql-security-wims-bfp]] — WIMS-BFP PostgreSQL security synthesis
- [[concepts/secure-coding-practices]] — OWASP/CWE secure coding
- [[mocs/cybersecurity]] — Cybersecurity Map of Content
