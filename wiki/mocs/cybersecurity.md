---
id: cybersecurity-moc-001
type: MOC
title: "Cybersecurity — Map of Content"
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-10-08
confidence: high
source_refs: []
status: active
tags:
  - moc
  - cybersecurity
related:
  - sources/cybersecurity/suricata-cves-2026
  - sources/cybersecurity/keycloak-cves-2026
  - sources/cybersecurity/nextjs-cves-2026
  - sources/cybersecurity/nist-sp-800-207-zero-trust-architecture
  - sources/cybersecurity/dod-zta-implementation-primer-2026
  - sources/cybersecurity/zero-trust-complete-guide-2026
  - concepts/zero-trust-architecture
  - sources/software-dev/owasp-top-10-2025
  - sources/software-dev/cwe-top-25-2025
  - sources/software-dev/owasp-secure-code-review
  - concepts/secure-coding-practices
  - sources/software-dev/postgresql-security-best-practices
  - sources/software-dev/postgresql-rls-limitations
  - sources/software-dev/postgresql-cves-2025-2026
  - concepts/postgresql-security-wims-bfp
  - sources/software-dev/docker-security-best-practices
  - sources/software-dev/docker-cves-2025-2026
  - concepts/docker-security-wims-bfp
---

# Cybersecurity — Map of Content

*Reading path for cybersecurity research, CVE tracking, and security frameworks in the vault.*

---

## Overview

Cybersecurity research in this vault covers two primary themes:

1. **Active CVE Tracking** — Critical vulnerabilities affecting WIMS-BFP's technology stack (Suricata, Keycloak, Next.js)
2. **Security Frameworks** — Zero Trust Architecture, access control models, defense-in-depth

---

## CVE Tracking

*Start here for vulnerabilities affecting WIMS-BFP's production stack.*

### Reading Path

1. [[sources/cybersecurity/suricata-cves-2026]] — 5 CVEs affecting Suricata IDS/IPS (CVSS up to 9.8)
2. [[sources/cybersecurity/keycloak-cves-2026]] — 3 CVEs affecting Keycloak auth (JWT, SSRF, POST)
3. [[sources/cybersecurity/nextjs-cves-2026]] — 3 CVEs affecting Next.js frontend (smuggling, DoS, RCE)

### CVE Summary Table

| CVE | Technology | Severity | Type | Impact on WIMS-BFP |
|---|---|---|---|---|
| CVE-2026-31934 | Suricata | High (7.5) | SMTP DoS | Degrade detection capability |
| CVE-2026-22264 | Suricata | Critical (9.1) | Processing flaw | Bypass detection |
| CVE-2026-22262 | Suricata | Critical (9.8) | Remote | Highest severity |
| CVE-2026-22259 | Suricata | High | Crafted traffic | Processing errors |
| CVE-2026-31937 | Suricata | Medium | DCERPC DoS | Performance degradation |
| CVE-2026-4634 | Keycloak | Medium-High | POST exhaustion | Auth bypass |
| CVE-2026-4366 | Keycloak | High | SSRF | Cloud metadata access |
| CVE-2026-1529 | Keycloak | High | JWT bypass | Privilege escalation |
| CVE-2026-29057 | Next.js | Medium (5.3) | Request smuggling | Auth bypass via proxy |
| CVE-2026-27980 | Next.js | Medium | Image cache DoS | Disk exhaustion |
| CVE-2025-55182 | Next.js | Critical (9.0+) | RCE | Server compromise |

### Mitigation Priority

```
CRITICAL (patch immediately):
  - CVE-2026-22262 (Suricata, CVSS 9.8)
  - CVE-2026-22264 (Suricata, CVSS 9.1)
  - CVE-2025-55182 (Next.js, RCE)

HIGH (patch this week):
  - CVE-2026-31934 (Suricata, SMTP DoS)
  - CVE-2026-4366 (Keycloak, SSRF)
  - CVE-2026-1529 (Keycloak, JWT)

MEDIUM (patch this month):
  - CVE-2026-4634 (Keycloak, POST)
  - CVE-2026-29057 (Next.js, smuggling)
  - CVE-2026-27980 (Next.js, DoS)
  - CVE-2026-31937 (Suricata, DCERPC)
```

---

## Secure Coding Practices

*Start here for writing secure code — OWASP, CWE, and code review methodology.*

### Reading Path

1. [[concepts/secure-coding-practices]] — Synthesis of OWASP Top 10 + CWE Top 25 + ZTA + code review
2. [[sources/software-dev/owasp-top-10-2025]] — Web application security risks (2025)
3. [[sources/software-dev/cwe-top-25-2025]] — Most dangerous software weaknesses (2025)
4. [[sources/software-dev/owasp-secure-code-review]] — Code review methodology

---

## Docker Container Security

*Start here for container security — images, runtime, runc CVEs, Compose hardening.*

### Reading Path

1. [[concepts/docker-security-wims-bfp]] — WIMS-BFP Docker security synthesis (Compose template, audit checklist)
2. [[sources/software-dev/docker-security-best-practices]] — 5 layers: image, build, runtime, network, secrets
3. [[sources/software-dev/docker-cves-2025-2026]] — runc escape CVEs (CVE-2025-31133, CVE-2025-52565, CVE-2025-52881)

---

## PostgreSQL Security

*Start here for database-level security — RLS, CVEs, and WIMS-BFP patterns.*

### Reading Path

1. [[concepts/postgresql-security-wims-bfp]] — WIMS-BFP PostgreSQL security synthesis (RLS, CVEs, audit checklist)
2. [[sources/software-dev/postgresql-security-best-practices]] — Authentication, authorization, encryption, auditing
3. [[sources/software-dev/postgresql-rls-limitations]] — 6 RLS pitfalls + WIMS-BFP mitigations
4. [[sources/software-dev/postgresql-cves-2025-2026]] — CVE-2025-1094 (psql RCE), CVE-2025-8714 (pg_dump RCE)

---

## Security Frameworks

*Start here for foundational security architecture knowledge.*

### Reading Path

1. [[concepts/zero-trust-architecture]] — Synthesis of ZTA principles, pillars, and WIMS-BFP alignment
2. [[sources/cybersecurity/nist-sp-800-207-zero-trust-architecture]] — NIST's foundational ZTA document (7 tenets)
3. [[sources/cybersecurity/dod-zta-implementation-primer-2026]] — DoW/NSA practical implementation (Jan 2026)
4. [[sources/cybersecurity/zero-trust-complete-guide-2026]] — Market data, 7 pillars, real-world challenges

### Key Numbers

- **81%** of organizations planning ZTA implementation (Gartner)
- **$78 billion** projected global ZTA market by 2030
- **38% higher** breach costs without ZTA
- **$1.76 million** average breach cost reduction with ZTA

---

## Open Questions / Research Gaps

- No cybersecurity MOC existed before today — CVEs were isolated pages
- No concept pages for: threat detection pipeline, authentication architecture, defense-in-depth
- Biomechanics and software-dev raw sources not yet ingested
- How does ZTA apply to multi-agent architectures (WIMS-BFP 4-agent setup)?
- Post-quantum cryptography impact on WIMS-BFP's RSA/ECDSA key infrastructure (not yet researched)

---

## WIMS-BFP Relevance

**WIMS-BFP's stack and its security posture:**

| Component | CVEs Tracked | ZTA Mapping | Framework |
|---|---|---|---|
| Suricata IDS | 5 CVEs (CVSS 7.5-9.8) | Visibility & Analytics pillar | MITRE ATT&CK |
| Keycloak Auth | 3 CVEs (JWT, SSRF, POST) | Identity pillar, Tenet 6 | FRS RBAC |
| Next.js Frontend | 3 CVEs (smuggling, DoS, RCE) | Applications pillar | CSP, headers |
| PostgreSQL RLS | — | Data pillar, Tenet 3 | Per-session access |
| FastAPI Backend | — | Applications pillar | JWT validation |

---

## Related MOCs

- [[mocs/ai-research]] — AI agent memory, prompt optimization, agentic architecture
