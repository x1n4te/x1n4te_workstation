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

# PostgreSQL Security — Detailed Reference

Back to overview: [[concepts/postgresql-security-wims-bfp]]
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
- rls-null-bypass-fix — WIMS-BFP-specific NULL bypass fix skill (see [[mocs/skills]])
- [[mocs/cybersecurity]] — Cybersecurity Map of Content
