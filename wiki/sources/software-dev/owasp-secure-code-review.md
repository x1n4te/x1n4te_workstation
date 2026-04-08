---
id: owasp-secure-code-review-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html
status: active
tags:
  - owasp
  - code-review
  - secure-coding
  - software-dev
related:
  - sources/software-dev/owasp-top-10-2025
  - sources/software-dev/cwe-top-25-2025
  - concepts/secure-coding-practices
  - mocs/cybersecurity
---

# OWASP Secure Code Review Cheat Sheet (Source Summary)

**Source:** OWASP Cheat Sheet Series
**Type:** Practical code review methodology
**Confidence:** High — OWASP official, used by security teams worldwide

---

## Review Types

| Type | Scope | Use Case |
|---|---|---|
| **Baseline Review** | Entire codebase | New apps, major releases, compliance, post-incident |
| **Diff-Based Review** | Changed code only | Pull requests, daily dev, feature completion |

---

## Review Methodology

### Preparation (All Reviews)
- Understand architecture and business requirements
- Gather threat models and previous findings
- Identify critical assets and high-risk functions
- Review security requirements

### Baseline Review Steps
1. Architecture review for anti-patterns
2. Entry point and input validation analysis
3. Authentication and authorization verification
4. Data flow tracing
5. Business logic analysis
6. Cryptographic implementation review
7. Error handling verification
8. Configuration and deployment review

### Diff-Based Review Steps
1. Analyze impact on existing security controls
2. Identify new attack vectors
3. Verify security at modified trust boundaries
4. Check new integrations
5. Ensure no security regression
6. Apply relevant security patterns

---

## Common Vulnerability Patterns

| Pattern | What to Look For | OWASP Reference |
|---|---|---|
| **Input Validation** | Missing server-side validation, improper sanitization | Input Validation CS |
| **SQL Injection** | String concatenation in queries | SQLi Prevention CS |
| **XSS** | Improper output encoding, unsafe DOM manipulation | XSS Prevention CS |
| **Path Traversal** | Unsafe file path construction | File Upload CS |
| **Command Injection** | Direct command execution with user input | OS Command Injection CS |
| **Auth/Session** | Token generation flaws, credential handling | Auth & Session Mgmt CS |
| **Access Control** | Missing authorization checks, privilege escalation | Authorization CS |
| **Deserialization** | Unsafe deserialization, XXE | Deserialization & XXE CS |
| **Crypto Flaws** | Weak algorithms, poor key management | Crypto Storage CS |

---

## Code Pattern Analysis — High-Risk Patterns

Focus on these patterns during review:

1. **Input processing** — validation, sanitization, filtering
2. **Database queries** — construction, ORM usage, parameterization
3. **File operations** — path handling, upload validation
4. **Authentication/session** — token generation, credential handling
5. **Authorization logic** — access control, privilege escalation
6. **Cryptographic operations** — algorithm choice, key management
7. **Error handling** — logging, exception management
8. **Configuration** — env vars, secrets management

---

## Data Flow Analysis

Trace data through the app:
1. **Identify Sources** — user input, files, APIs, DB reads, env vars
2. **Follow Processing** — validation, transformation, business logic
3. **Check Sinks** — DB queries, file writes, output rendering, logs
4. **Validate Boundaries** — input validation + output encoding at trust boundaries
5. **Trust Zones** — verify controls at each boundary crossing
6. **Data Classification** — sensitive data protected appropriately

---

## WIMS-BFP Application

For WIMS-BFP code reviews, focus on:

| Pattern | WIMS-BFP Location | What to Check |
|---|---|---|
| Input validation | FastAPI route handlers | Pydantic models, field validators |
| SQL injection | psycopg2 queries | Parameterized queries, no string concatenation |
| RLS bypass | PostgreSQL policies | wims.current_user_id set in every transaction |
| JWT auth | All endpoints | kid, iss, aud, signature, expiry |
| Error handling | Exception handlers | No sensitive info in error responses |
| Secrets | .env files | No hardcoded API keys, tokens in code |

---

## Related Pages

- [[mocs/cybersecurity]] — Cybersecurity Map of Content
- [[sources/software-dev/owasp-top-10-2025]] — OWASP Top 10 (risks list)
- [[sources/software-dev/cwe-top-25-2025]] — CWE Top 25 (weaknesses list)
- [[concepts/secure-coding-practices]] — Synthesis page
