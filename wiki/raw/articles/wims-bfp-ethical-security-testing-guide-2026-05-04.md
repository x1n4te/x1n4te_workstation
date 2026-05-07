# WIMS-BFP — Ethical Security Testing Guide

> **Source:** User-provided ethical security testing guidelines
> **Captured:** 2026-05-04
> **Purpose:** Conducting responsible, legally-compliant security testing for the WIMS-BFP capstone project
> **Type:** Methodology reference

---

## Core Ethical Principle

> Test only what you own, what you built, or what you have explicit permission to test.

For capstone projects, the safest scope is the researchers' own developed system in a controlled environment.

---

## I. Pre-Testing Preparation

Before conducting any security test, complete the following:

### 1. Define the Scope of Testing

Clearly identify what will be tested. Examples:
- Login module
- Input forms
- Database records
- Audit logs
- Availability under load
- Session management

**Do not test systems, servers, or networks outside the approved project scope.**

### 2. Use a Controlled Environment

Testing should be conducted in an isolated and safe environment such as:
- Localhost / Deployed Environment
- Development server
- Test machine
- Sandbox environment
- Private laboratory network

**Avoid testing on public or production systems unless formally authorized.**

### 3. Prepare Safe Test Data

Use only non-sensitive and non-production data such as:
- Dummy accounts
- Sample records
- Test passwords
- Simulated transactions

**Do not use real personal data unless properly approved and protected.**

### 4. Inform Relevant Supervisors

When required by institution, adviser, or laboratory rules:
- Inform your adviser
- Coordinate with faculty mentor
- Notify laboratory administrator

This promotes accountability and proper oversight.

### 5. Backup the System

Before testing, prepare backups of:
- Source code
- Database
- Configuration files
- Logs

This allows recovery if testing causes unexpected issues.

---

## II. Ethical Testing Procedure

### Step 1: Review the Objective of the Test

Identify what the test is meant to evaluate. Examples:
- Can login resist brute-force attempts?
- Is SQL injection blocked?
- Are logs protected from tampering?
- Does HTTPS enforce encryption?
- Does the system remain available under load?

Each test must align with the approved objectives of the study.

### Step 2: Select Appropriate Tools

Use tools suitable for the scope and skill level. Examples:
- Browser developer tools
- Burp Suite (Community Edition)
- SQLMap
- OWASP ZAP
- JMeter
- Wireshark

Use tools responsibly and only within scope.

### Step 3: Execute the Test Carefully

Perform only the planned steps. Examples:
- Controlled invalid login attempts
- Safe SQL payload testing on your own form
- Simulated log modification attempt
- Moderate load simulation

**Avoid excessive actions that may crash systems unnecessarily.**

### Step 4: Observe and Record Results

Document:
- Date and time
- Tool used
- Steps performed
- Expected result
- Actual result
- Screenshot or screen recording
- Logs generated
- Status (Passed / Failed)

If a vulnerability is found, document it professionally.

### Step 5: Apply Remediation

If weaknesses are identified:
1. Fix the issue
2. Retest after correction
3. Record improvement

The goal of testing is improvement, not merely finding faults.

---

## III. Required Ethical Reminders

**Do:**
- Test only approved systems
- Use dummy/test data
- Keep evidence organized
- Follow adviser instructions
- Use minimal necessary force/load
- Protect collected logs and data
- Stop testing if instability occurs

**Do Not:**
- Test external websites or third-party apps without permission
- Use real user credentials without consent
- Exfiltrate or copy sensitive data
- Cause intentional damage
- Hide vulnerabilities from adviser/team
- Misrepresent results

---

## IV. Minimum Documentation Requirements

Each test should have evidence.

**Required Files:**
| Document | Purpose |
|----------|---------|
| Test case sheet | Planned test steps and pass criteria |
| Screenshots | Visual evidence of results |
| Video demonstration | Step-by-step execution record |
| Logs or outputs | Raw tool/system output |
| Result summary | Pass/fail with metrics |
| Remediation notes | How the issue was fixed |

If reported in Chapter 4, it must have supporting evidence.

---

## V. Suggested Student Workflow

```
Review objective
       ↓
Prepare environment
       ↓
Backup system
       ↓
Use dummy data
       ↓
Run test
       ↓
Record evidence
       ↓
Fix issues
       ↓
Retest
       ↓
Summarize results
       ↓
Prepare defense materials
```

---

## VI. Sample Ethical Statement for Chapter 3

> All security tests were conducted only on the researchers' developed system within a controlled test environment using non-production data. The procedures were limited to the approved scope of the study and were performed solely for academic evaluation and system improvement purposes.

---

## VII. Defense Reminder

**If asked, "Was this ethical?" — answer:**

> Yes. The tests were performed only on our own developed system in a controlled environment using test data and documented procedures.

---

## WIMS-BFP Security Test Scope Reference

Based on the [[raw/articles/wims-bfp-research-question-alignment-matrix-2026-05-04]], the approved test scope maps to:

| Test Category | Scope (WIMS-BFP) | Tool Reference |
|--------------|------------------|---------------|
| Authentication / Spoofing | Login module, JWT refresh | Burp Suite, browser DevTools |
| Input Validation / Tampering | Data entry forms, SQL injection | SQLMap, OWASP ZAP |
| Repudiation / Logging | Audit logs, log tamper detection | Custom tamper scripts, log export |
| Information Disclosure | HTTPS enforcement, session controls | ZAP, Wireshark |
| Denial of Service | Uptime under load, recovery | JMeter |
| AI Explainability | Response time, access restriction | Timing logs, endpoint tests |

Each test case falls under the WIMS-BFP-developed system only — no external targets.

---

## Relevant Standards Alignment

| Standard | Role in This Guide |
|----------|-------------------|
| NIST SP 800-115 | Testing methodology (phases: planning → discovery → attack → reporting) |
| OWASP ASVS | Verification criteria for each test case |
| ISO/IEC 25010 | Quality attributes evaluated (FURPS) |
| ISO 27001 | Security governance, logging controls, incident handling |
| WIMS-BFP Thesis | Alignment with Ch1 objectives → Ch3 scope → Ch4 evidence |
