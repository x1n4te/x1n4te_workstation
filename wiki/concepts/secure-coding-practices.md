---
id: secure-coding-practices-concept-001
type: concept
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - sources/software-dev/owasp-top-10-2025
  - sources/software-dev/cwe-top-25-2025
  - sources/software-dev/owasp-secure-code-review
  - sources/cybersecurity/nist-sp-800-207-zero-trust-architecture
status: active
tags:
  - secure-coding
  - owasp
  - cwe
  - software-dev
  - cybersecurity
related:
  - sources/software-dev/owasp-top-10-2025
  - sources/software-dev/cwe-top-25-2025
  - sources/software-dev/owasp-secure-code-review
  - concepts/zero-trust-architecture
  - mocs/cybersecurity
  - mocs/ai-research
---

# Secure Coding Practices

**Synthesis of:** OWASP Top 10 (2025), CWE Top 25 (2025), OWASP Secure Code Review, Zero Trust Architecture
**Purpose:** Unified reference for writing secure code in WIMS-BFP and future projects

---

## The 4 Sources

| Source | Focus | Year |
|---|---|---|
| [[sources/software-dev/owasp-top-10-2025]] | Web application security risks | 2025 |
| [[sources/software-dev/cwe-top-25-2025]] | Most dangerous software weaknesses | 2025 |
| [[sources/software-dev/owasp-secure-code-review]] | Code review methodology | Current |
| [[concepts/zero-trust-architecture]] | Access control and security posture | NIST SP 800-207 |

---

## Core Principles (Consensus Across All Sources)

| Principle | OWASP | CWE | ZTA | Code Review |
|---|---|---|---|---|
| **Validate all input** | A05 (Injection) | CWE-79, CWE-89, CWE-78 | — | Input processing analysis |
| **Enforce access control** | A01 (Broken Access) | CWE-862, CWE-863 | Tenets 3, 4, 6 | AuthZ verification |
| **Fail closed** | A02 (Misconfiguration) | CWE-306 | "Assume breach" | Error handling review |
| **Encrypt sensitive data** | A04 (Crypto Failures) | CWE-200 | Tenet 2 | Crypto review |
| **Least privilege** | A01 (Broken Access) | CWE-862 | "Never trust, always verify" | Access control analysis |
| **Log and monitor** | A09 (Logging Failures) | CWE-20 | Tenet 7 | Logging verification |
| **Handle errors safely** | A10 (Exceptional Conditions) | CWE-476 | — | Error handling review |
| **Audit dependencies** | A03 (Supply Chain) | CWE-502 | — | Third-party review |

---

## Top 5 WIMS-BFP Actions

Based on the synthesis of all sources applied to WIMS-BFP's codebase:

### 1. Audit OWASP A03 (Supply Chain)
```
pip list --outdated
npm audit
```
Verify all dependencies are current. Lock CI/CD pipelines.

### 2. Verify CWE-862 (Missing Authorization) coverage
Every FastAPI route must have:
- JWT validation (kid, iss, aud, signature, expiry)
- RLS context set (SET LOCAL wims.current_user_id)
- FRS role check (one of 5 literals)

### 3. Review CWE-502 (Deserialization)
Pydantic validates all external input. Verify no `pickle.loads()` or unsafe YAML parsing anywhere.

### 4. Check CWE-918 (SSRF)
Any URL fetched from user input must be validated. Restrict outbound to known domains.

### 5. Confirm CWE-770 (Resource Limits)
Rate limiting on all endpoints. Max payload sizes enforced. Timeout on external calls.

---

## Code Review Checklist (OWASP Methodology for WIMS-BFP)

For every PR, the Critic agent should check:

```
[ ] Input validation: Pydantic models on all route handlers
[ ] SQL injection: Parameterized queries only (no f-strings in SQL)
[ ] RLS: SET LOCAL wims.current_user_id in every transaction
[ ] JWT: kid, iss, aud, signature, expiry validated
[ ] Error handling: No stack traces or internal details in responses
[ ] Secrets: No hardcoded API keys, tokens, passwords
[ ] Dependencies: No outdated packages with known CVEs
[ ] Logging: Security events logged (auth failures, RLS denials)
```

---

## Related

- [[concepts/zero-trust-architecture]] — ZTA framework and WIMS-BFP alignment
- [[sources/software-dev/owasp-top-10-2025]] — OWASP Top 10 (2025)
- [[sources/software-dev/cwe-top-25-2025]] — CWE Top 25 (2025)
- [[sources/software-dev/owasp-secure-code-review]] — OWASP code review methodology
- [[mocs/cybersecurity]] — Cybersecurity Map of Content
