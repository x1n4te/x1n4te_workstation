# WIMS-BFP — Research Question Alignment Matrix

> **Source:** User-provided alignment guide
> **Captured:** 2026-05-04
> **Purpose:** Ensure study consistency from Ch1 (Objectives) → Ch3 (Methodology) → Ch4 (Results and Discussion)
> **Type:** Structural reference

---

## Purpose of the Matrix

The matrix connects:
- Research objectives
- Functional requirements
- System quality evaluation
- Security testing evidence
- STRIDE threat categories

**Key questions it answers:**
- Which objective is being measured?
- How will functionality be evaluated?
- What security risks are relevant?
- What test will validate the safeguard?
- What result should appear in Chapter 4?

**Panel cross-check questions:**
- "How does this objective relate to your testing?"
- "Why did you choose these security tests?"
- "Where did your metrics come from?"
- "How is STRIDE reflected in your system?"

---

## Evaluation Standards Reference

| Area | Standard Reference |
|------|-------------------|
| Functionality Evaluation | ISO/IEC 25010 |
| Security Testing | OWASP ASVS |
| Testing Process | NIST SP 800-115 |
| Threat Identification | STRIDE |

---

## Research Objective Alignment Matrix

| Research Objective | Functional Output / Module | Functionality Evaluation | STRIDE Threat | Security Test / Metric | Expected Chapter 4 Evidence |
|---|---|---|---|---|---|
| Develop secure user access management for authorized users | Login / User Management Module | Functional Suitability, Usability | Spoofing | Authentication Lockout, Invalid Login Denial Rate, Role Access Restriction | Authentication Security Results |
| Develop secure data entry and record management features | Data Entry / Records Module | Functional Correctness, Task Appropriateness | Tampering | SQL Injection Success Rate, Unauthorized Record Modification Detection | Input Validation Results |
| Implement audit trail and activity monitoring features | Logs / Audit Trail Module | Functional Suitability, Reliability | Repudiation | Log Tamper Detection, Activity Logging Completeness | Logging Integrity Results |
| Protect sensitive information during access and transmission | Reports / Protected Records / Session Controls | Reliability, Functional Correctness | Information Disclosure | HTTPS Enforcement, Unauthorized Access Block Rate | Data Protection Results |
| Maintain system continuity during stress or interruptions | Dashboard / Core Services / Sync Module | Performance Efficiency, Reliability | Denial of Service | Uptime Under Load, Recovery After Interruption | Availability Results |
| Provide understandable automated outputs for decision support | AI Recommendation / Alert Module | Usability, Explainability | (Supports multiple categories) | Access Restriction to AI Outputs, Reliable Response Time | Usability / Explainability Results |

---

## STRIDE Mapping Summary

| STRIDE Category | Threat Description | Mitigated By |
|---|---|---|
| **Spoofing** | Impersonating authorized users | MFA, JWT with short-lived tokens, session revocation |
| **Tampering** | Modifying data or records without authorization | RLS policies, SQL injection prevention, audit logs |
| **Repudiation** | User denies performing an action | Immutable audit logs, log tamper detection |
| **Information Disclosure** | Exposing sensitive data to unauthorized parties | HTTPS, AES-256-GCM encryption, access control |
| **Denial of Service** | Making system unavailable | Uptime monitoring, load resilience, recovery procedures |

---

## Ch1 → Ch3 → Ch4 Flow

```
Chapter 1 Objectives
    │
    ├── General Objective ──────────────────────────────► Chapter 5 Conclusions
    │
    └── Specific Objectives
            │
            ├── Developmental ────────────► Ch3 Project Development Model ──► Ch4 Functional Suitability
            ├── Cybersecurity Components ─► Ch3 Security Requirements ───────► Ch4 STRIDE Test Results
            ├── Cybersecurity Compliance ──► Ch3 Security Practices ──────────► Ch4 Security Metrics
            ├── Security Testing ─────────► Ch3 Security Testing + NIST 800-115► Ch4 Pass/Fail Evidence
            └── System Evaluation ────────► Ch3 ISO/IEC 25010 (FURPS) ────────► Ch4 Quality Evaluation
```

---

## Notes

- Each row in the matrix maps to exactly one Chapter 4 results subsection
- Security test metrics should be quantitative (pass/fail rates, % thresholds)
- OWASP ASVS Level 2 is the recommended baseline for cybersecurity capstone projects
- NIST SP 800-115 provides the testing methodology — walk-through, penetration testing, interview phases
