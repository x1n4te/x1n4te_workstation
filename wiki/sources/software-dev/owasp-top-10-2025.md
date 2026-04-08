---
id: owasp-top-10-2025-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - owasp.org/Top10/2025/en/
  - blog.securelayer7.net/owasp-top-10-security-risks/
status: active
tags:
  - owasp
  - web-security
  - secure-coding
  - software-dev
related:
  - sources/software-dev/cwe-top-25-2025
  - sources/software-dev/owasp-secure-code-review
  - concepts/secure-coding-practices
  - mocs/cybersecurity
---

# OWASP Top 10 — 2025 (Source Summary)

**Source:** OWASP Foundation (2025 release)
**Type:** Authoritative web application security risk list
**Confidence:** High — industry standard, referenced by compliance frameworks

---

## Key Changes from 2021 → 2025

| Change | Details |
|---|---|
| **New** | A03: Software Supply Chain Failures (absorbed vulnerable components) |
| **New** | A10: Mishandling of Exceptional Conditions |
| **Rose** | Security Misconfiguration: #5 → #2 |
| **Rose** | Software Supply Chain Failures: entered at #3 |
| **Merged** | SSRF merged into Broken Access Control |
| **Merged** | Vulnerable/Outdated Components absorbed into Supply Chain |

---

## The OWASP Top 10 (2025)

| Rank | Category | CWEs Mapped | Incidence Rate | Key Mitigation |
|---|---|---|---|---|
| **A01** | Broken Access Control | 40 | 20.15% | Deny by default, server-side checks every request |
| **A02** | Security Misconfiguration | 16 | 27.70% | Automate hardening, remove unused features |
| **A03** | Software Supply Chain Failures | 6 | 9.6% | Dependency inventory, signed packages, CI/CD lockdown |
| **A04** | Cryptographic Failures | 32 | 13.77% | Encrypt at rest + transit, enforce TLS, proper key mgmt |
| **A05** | Injection | 37 | 13.77% | Validate/sanitize input, parameterized queries, least privilege |
| **A06** | Insecure Design | — | — | Threat modeling, security in architecture phase |
| **A07** | Authentication Failures | — | — | MFA, strong password policies, session management |
| **A08** | Software and Data Integrity Failures | — | — | Code signing, CI/CD integrity checks |
| **A09** | Security Logging and Monitoring Failures | — | — | Comprehensive logging, SIEM integration |
| **A10** | Mishandling of Exceptional Conditions | — | — | Proper error handling, fail-safe defaults |

---

## WIMS-BFP Mapping

| OWASP Category | WIMS-BFP Component | Current Status |
|---|---|---|
| A01: Broken Access Control | RLS (wims.current_user_id), JWT validation | ✅ Implemented |
| A02: Security Misconfiguration | Keycloak config, default credentials | ⚠️ Verify defaults |
| A03: Supply Chain | Python/Node dependencies, CI/CD pipeline | ⚠️ Needs audit |
| A04: Cryptographic Failures | pgcrypto for UUIDs, TLS | ⚠️ Check TLS config |
| A05: Injection | Parameterized queries via psycopg2 | ✅ Implemented |
| A06: Insecure Design | DMZ air-lock, FRS roles | ✅ Implemented |
| A07: Authentication | Keycloak MFA, JWT | ✅ Implemented |
| A08: Integrity Failures | Git signing, CI/CD checks | ⚠️ Partial |
| A09: Logging/Monitoring | Audit logging, Suricata | ✅ Implemented |
| A10: Exceptional Conditions | Error handling in FastAPI | ⚠️ Needs review |

---

## Related Pages

- [[mocs/cybersecurity]] — Cybersecurity Map of Content
- [[sources/software-dev/cwe-top-25-2025]] — CWE Top 25 (software weaknesses)
- [[sources/software-dev/owasp-secure-code-review]] — OWASP secure code review methodology
- [[concepts/secure-coding-practices]] — Synthesis page
