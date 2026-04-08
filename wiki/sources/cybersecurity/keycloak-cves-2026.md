---
id: keycloak-cves-2026-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-04-15
stale_after: 2026-04-29
confidence: high
source_refs:
  - github.com/0x240x23elu/CVE-2026-1529
  - sentinelone.com/vulnerability-database/cve-2026-4366
  - access.redhat.com/security/cve/CVE-2026-4634
status: active
tags:
  - keycloak
  - cve
  - authentication
  - vulnerability
  - cybersecurity
related:
  - entities/keycloak
  - concepts/authentication-architecture
---

# Keycloak CVEs — 2026 (Source Summary)

**Source:** GitHub, SentinelOne, Red Hat
**Technology:** Keycloak Identity Provider
**Relevance:** WIMS-BFP's authentication provider (RBAC + MFA)

---

## CVE-2026-4634 — Unauthenticated Crafted POST Request

**Affected:** Keycloak (multiple versions, check Red Hat advisory)
**CVSS:** Medium-High
**Type:** Remote, unauthenticated

**Description:** An unauthenticated attacker can exploit this vulnerability by sending a specially crafted POST request with an excessively large payload. This triggers a flaw in Keycloak's request processing logic.

**Impact on WIMS-BFP:** WIMS-BFP uses Keycloak for all user authentication. An unauthenticated attacker could potentially overwhelm or bypass the authentication layer.

**Patch:** Apply Keycloak security updates. Monitor: https://access.redhat.com/security/cve/CVE-2026-4634

---

## CVE-2026-4366 — SSRF via Improper Redirect Handling (Information Disclosure)

**Affected:** Keycloak (multiple versions)
**Type:** Server-Side Request Forgery (SSRF) / Information Disclosure
**Attack vector:** Remote, unauthenticated

**Description:** Keycloak improperly follows HTTP redirects when processing certain client configuration requests. An attacker can manipulate the server into making unintended requests to internal or restricted resources, potentially exposing:
- Cloud metadata endpoints (AWS, GCP, Azure)
- Internal network resources
- Sensitive configuration data

**Impact on WIMS-BFP:** If WIMS-BFP is deployed in a cloud environment (e.g., Vast.ai RTX 3090), an attacker could access cloud instance metadata, retrieve IAM credentials, or map internal infrastructure. This could lead to privilege escalation and data exfiltration.

**Patch:** Apply Keycloak security updates. Monitor: https://www.sentinelone.com/vulnerability-database/cve-2026-4366/

---

## CVE-2026-1529 — Unauthorized Organization Registration via JWT Flaw

**Affected:** Keycloak
**Severity:** High
**Type:** Remote, unauthenticated

**Description:** A vulnerability in Keycloak allows unauthorized organization registration through improper JWT validation. An attacker can bypass authorization checks by manipulating JWT tokens.

**Impact on WIMS-BFP:** WIMS-BFP uses JWT-based RBAC with 5 FRS roles (CIVILIAN_REPORTER through SYSTEM_ADMIN). A JWT validation bypass could allow an attacker to escalate privileges or register unauthorized organizational accounts.

**Patch:** Apply Keycloak security updates. Verify JWT validation: check `kid`, `iss`, `aud`, signature, and expiry on all endpoints.

---

## Mitigation Checklist for WIMS-BFP

```
[ ] Verify Keycloak version and apply patches
[ ] Block SSRF vectors: restrict outbound HTTP from Keycloak to internal-only
[ ] Audit JWT validation: confirm all 5 checks (kid, iss, aud, signature, expiry)
[ ] Rate-limit POST endpoints to mitigate CVE-2026-4634 payload exhaustion
[ ] Monitor: https://access.redhat.com/security/cve/ for new Keycloak CVEs
```

---

## Related Pages

- [[mocs/cybersecurity]] — Cybersecurity Map of Content (CVE tracking, ZTA, frameworks)
- [[concepts/zero-trust-architecture]] — ZTA frameworks and WIMS-BFP alignment
- [[sources/cybersecurity/suricata-cves-2026]] — Suricata CVEs (detection layer)
- [[sources/cybersecurity/nextjs-cves-2026]] — Next.js CVEs (frontend layer)
