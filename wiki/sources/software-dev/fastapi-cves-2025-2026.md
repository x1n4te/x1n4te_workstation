---
id: fastapi-cves-2025-2026-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-04-15
stale_after: 2026-04-29
confidence: high
source_refs:
  - nvd.nist.gov/vuln/detail/CVE-2025-68481
  - sentinelone.com/vulnerability-database/cve-2025-55526
  - security.snyk.io/vuln/SNYK-PYTHON-FASTAPIGUARD-10245561
  - github.com/topoteretes/cognee/issues/2101
status: active
tags:
  - fastapi
  - python
  - cve
  - vulnerability
  - api-security
  - software-dev
related:
  - sources/software-dev/fastapi-security-best-practices
  - sources/software-dev/celery-redis-security
  - concepts/fastapi-security-wims-bfp
  - mocs/cybersecurity
---

# FastAPI Ecosystem CVEs — 2025-2026 (Source Summary)

**Sources:** NVD, SentinelOne, Snyk, GitHub
**Technology:** FastAPI + ecosystem (python-multipart, fastapi-users, fastapi-guard)
**Confidence:** High — NVD official + vendor advisories

---

## CVE-2025-68481 — fastapi-users OAuth Token Injection (HIGH)

**Affected:** fastapi-users <15.0.2
**CVSS:** 8.8 (High)
**Type:** OAuth Token Injection

**Description:** FastAPI Users (an authentication library for FastAPI) allows token injection through improper OAuth handling in `fastapi_users/router/oauth.py`. An attacker can manipulate OAuth tokens to gain unauthorized access.

**Impact on WIMS-BFP:** If WIMS-BFP uses fastapi-users for any OAuth flows (SSO), this is critical. WIMS-BFP uses Keycloak directly, so risk depends on whether fastapi-users is a dependency.

**Patch:** Upgrade to fastapi-users ≥15.0.2

---

## CVE-2025-55526 — n8n FastAPI Path Traversal (CRITICAL)

**Affected:** n8n-workflows project (FastAPI-based)
**CVSS:** Critical
**Type:** Directory Traversal

**Description:** A path traversal vulnerability in a FastAPI application allows attackers to access files outside the intended directory via the `download_workflow` function. Attacker includes `../` or `..\\` sequences to escape the directory and access arbitrary files on the system.

**Impact on WIMS-BFP:** If WIMS-BFP exposes any file download endpoints (e.g., report downloads), verify path traversal protection.

**Patch:** Ensure all file paths are sanitized and validated against a whitelist.

---

## CVE-2025-46814 — fastapi-guard X-Forwarded-For Header Spoofing (HIGH)

**Affected:** fastapi-guard <2.0.0
**Type:** IP Spoofing via Header Manipulation

**Description:** The fastapi-guard security library (IP blocking, rate limiting) is vulnerable to header spoofing via `X-Forwarded-For`. An attacker can inject arbitrary IP addresses to bypass IP-based security measures.

**Impact on WIMS-BFP:** If WIMS-BFP uses fastapi-guard for IP-based rate limiting or blocking, an attacker can spoof their IP to bypass protections.

**Patch:** Upgrade to fastapi-guard ≥2.0.0. Use a trusted reverse proxy that strips/overwrites X-Forwarded-For headers.

---

## CVE-2026-24486 — python-multipart ReDoS (HIGH)

**Affected:** python-multipart <0.0.20
**Type:** Regular Expression Denial of Service (ReDoS)

**Description:** A ReDoS vulnerability in python-multipart (used by FastAPI for file uploads) allows an attacker to send a specially crafted multipart request that causes excessive CPU consumption.

**Impact on WIMS-BFP:** FastAPI uses python-multipart by default. WIMS-BFP's file upload endpoints (if any) are vulnerable.

**Patch:** Upgrade to python-multipart ≥0.0.20

---

## CVE-2025-14546 — fastapi-sso CSRF Vulnerability

**Affected:** fastapi-sso (multiple versions)
**Type:** Cross-Site Request Forgery (CSRF)

**Description:** The fastapi-sso package is vulnerable to CSRF due to improper state validation during the OAuth2 callback flow.

**Impact on WIMS-BFP:** If using fastapi-sso for SSO integration, CSRF can be used to authenticate as another user.

**Patch:** Verify state parameter is properly validated in OAuth2 callbacks.

---

## Mitigation Checklist

```
[ ] Check fastapi-users version: pip show fastapi-users
[ ] Check python-multipart version: pip show python-multipart
[ ] Check fastapi-guard version: pip show fastapi-guard
[ ] Upgrade python-multipart to ≥0.0.20
[ ] Sanitize all file paths in download endpoints (no ../)
[ ] Strip X-Forwarded-For at reverse proxy level
[ ] Verify CSRF state parameter in all OAuth2 callbacks
[ ] Monitor: https://github.com/fastapi/fastapi/security/advisories
```

---

## Related Pages

- [[sources/software-dev/fastapi-security-best-practices]] — FastAPI security reference
- [[sources/software-dev/celery-redis-security]] — Celery + Redis security
- [[concepts/fastapi-security-wims-bfp]] — WIMS-BFP FastAPI security synthesis
- [[mocs/cybersecurity]] — Cybersecurity Map of Content
