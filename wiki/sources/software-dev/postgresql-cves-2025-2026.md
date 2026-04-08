---
id: postgresql-cves-2025-2026-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-04-15
stale_after: 2026-04-29
confidence: high
source_refs:
  - postgresql.org/support/security/CVE-2025-1094/
  - postgresql.org/support/security/CVE-2025-8714/
  - rapid7.com/blog/post/2025/02/13/cve-2025-1094-postgresql-psql-sql-injection-fixed/
  - thehackernews.com/2025/02/postgresql-vulnerability-exploited.html
status: active
tags:
  - postgresql
  - cve
  - sql-injection
  - database
  - vulnerability
  - software-dev
related:
  - sources/software-dev/postgresql-security-best-practices
  - sources/software-dev/postgresql-rls-limitations
  - concepts/postgresql-security-wims-bfp
  - mocs/cybersecurity
---

# PostgreSQL CVEs — 2025-2026 (Source Summary)

**Sources:** PostgreSQL Security, Rapid7, The Hacker News
**Technology:** PostgreSQL (WIMS-BFP's primary database)
**Confidence:** High — official PostgreSQL security advisories

---

## CVE-2025-1094 — psql SQL Injection via Invalid UTF-8 (HIGH)

**Affected:** PostgreSQL <17.3, <16.7, <15.11, <14.16, <13.19
**CVSS:** High (7.5+)
**Exploited:** YES — used in the wild alongside BeyondTrust CVE-2024-12356

**Description:** PostgreSQL's `libpq` functions (`PQescapeLiteral()`, `PQescapeIdentifier()`, `PQescapeString()`, `PQescapeStringConn()`) fail to properly neutralize quoting syntax in text that fails encoding validation. Specifically:
- When `client_encoding` is `BIG5` and `server_encoding` is `EUC_TW` or `MULE_INTERNAL`
- Invalid UTF-8 byte sequences bypass the escaping logic
- Combined with psql's `\\!` meta-command (shell execution), achieves **arbitrary code execution (ACE)**

**How it works:**
1. Attacker controls database input
2. Invalid UTF-8 bypasses `PQescapeString()` sanitization
3. Malicious string reaches psql
4. psql interprets `\\!` meta-command → shell command execution

**Impact on WIMS-BFP:** If any FastAPI route accepts user input that's passed to PostgreSQL with encoding issues, or if any tooling uses `psql` interactively, this is a critical RCE vector.

**Patch:** Upgrade to PostgreSQL ≥17.3 (or ≥16.7, ≥15.11, ≥14.16, ≥13.19)

**Reference:** https://www.postgresql.org/support/security/CVE-2025-1094/

---

## CVE-2025-8714 — pg_dump RCE via psql Meta-Commands (HIGH)

**Affected:** PostgreSQL <17.6, <16.10, <15.14, <14.19, <13.22
**CVSS:** High
**Type:** Remote Code Execution

**Description:** A malicious superuser on the origin server can inject arbitrary code into a `pg_dump` output that executes during restore as the client operating system account running `psql`. The injection happens via psql meta-commands in the dump file.

**Impact on WIMS-BFP:** If database backups are restored via `psql` (not `pg_restore`), a compromised origin server or manipulated dump file could execute arbitrary code on the restore machine.

**Patch:** Upgrade to PostgreSQL ≥17.6

**Reference:** https://www.postgresql.org/support/security/CVE-2025-8714/

---

## CVE-2025-66260 — SQL Injection via status_sql.php (MEDIUM)

**Affected:** PostgreSQL-related web interfaces
**CVSS:** Medium
**Type:** SQL Injection

**Description:** SQL injection vulnerability via the `status_sql.php` endpoint, exploitable by manipulating parameters `sw1` and `sw2`.

**Impact on WIMS-BFP:** If WIMS-BFP exposes any PostgreSQL status or monitoring endpoints, this is relevant. Mitigate by never exposing pgAdmin or similar web UIs to the public internet.

---

## Active Exploitation Timeline

| Date | Event |
|---|---|
| Dec 2024 | BeyondTrust CVE-2024-12356 exploited in the wild |
| Feb 2025 | Rapid7 discovers CVE-2025-1094 was chained with BeyondTrust |
| Feb 2025 | PostgreSQL patches released (17.3, 16.7, etc.) |
| Feb 2026 | PostgreSQL 18.2, 17.8, 16.12, 15.16, 14.21 released |

---

## WIMS-BFP Mitigation

```
[ ] Verify PostgreSQL version: psql --version
[ ] Patch to ≥17.3 (fixes CVE-2025-1094) or latest
[ ] Patch to ≥17.6 (fixes CVE-2025-8714) or latest
[ ] Never use psql interactively for production restores (use pg_restore)
[ ] Verify encoding: SHOW client_encoding; SHOW server_encoding;
[ ] Audit any pgAdmin or web-based PostgreSQL tools (CVE-2025-66260)
[ ] Monitor: https://www.postgresql.org/support/security/
```

---

## Related Pages

- [[sources/software-dev/postgresql-security-best-practices]] — PostgreSQL security reference
- [[sources/software-dev/postgresql-rls-limitations]] — RLS pitfalls
- [[concepts/postgresql-security-wims-bfp]] — WIMS-BFP PostgreSQL security synthesis
- [[sources/cybersecurity/suricata-cves-2026]] — Suricata CVEs (IDS layer)
- [[sources/cybersecurity/keycloak-cves-2026]] — Keycloak CVEs (auth layer)
- [[mocs/cybersecurity]] — Cybersecurity Map of Content
