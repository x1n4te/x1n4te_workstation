# WIMS-BFP — Authority Approval Letter Template

> **Source:** User-provided authority approval / consent form template
> **Captured:** 2026-05-04
> **Purpose:** Formal request for permission to conduct controlled security testing for academic research (BFP or agency context)
> **Type:** Template

---

## Request Letter Template

```
[Date]

[Name of Authorized Officer]
[Position / Designation]
[Company / Institution / Agency Name]
[Address]

Subject: Request for Permission to Conduct Controlled Security Testing for Academic Research

Dear [Name of Authorized Officer],

Greetings.

We are undergraduate students currently enrolled in the Bachelor of Science in
Information Technology with Specialization in Cybersecurity program at
[University Name]. We are respectfully requesting permission to conduct a
controlled and limited security testing activity as part of our capstone/
research study entitled:

[Research Title]

The purpose of the study is to design, develop, evaluate, and improve
cybersecurity controls through structured testing and assessment. As part of
the approved methodology, we seek authorization to perform security testing
within your environment under clearly defined scope, safeguards, and supervision.

Nature of the Requested Activity

The proposed activity will involve only approved and non-destructive security
testing procedures such as:

  - Authentication and access control validation
  - Input validation testing
  - Secure communication verification
  - Logging and audit trail review
  - Controlled performance / availability testing

No destructive, unauthorized, or disruptive activities will be performed.

Proposed Scope

Testing will be limited only to the following approved systems/assets:

  [System / Application Name]
  [Server / Test URL / Environment]
  [Specific Module or Area]

No systems outside the approved scope will be accessed or tested.

Schedule of Activity

  Proposed Date(s): ____________________
  Proposed Time: ____________________
  Location / Environment: ____________________

Safeguards and Ethical Commitments

We commit to the following:

  1. Testing will be conducted only upon written approval.
  2. Activities will remain within the approved scope and schedule.
  3. Non-production or approved data will be used whenever possible.
  4. Confidentiality of information will be strictly observed.
  5. Findings will be used solely for academic and improvement purposes.
  6. Any identified vulnerabilities will be reported responsibly to
     authorized personnel.
  7. All applicable policies, laws, and ethical standards, including
     the Data Privacy Act of 2012 (RA 10173) and related regulations,
     will be observed.

Research Team

  [Leader Name]
  [Member 1]
  [Member 2]
  [Member 3]
  [Member 4]

Faculty Adviser

  [Adviser Name]
  [Department / University]

We respectfully hope for your favorable consideration of this request.
Your approval will greatly assist us in completing a responsible and
meaningful academic study.

Thank you for your time and consideration.

Respectfully yours,

[Leader Name]
Group Leader / Researcher
On behalf of the Research Team

Noted by:
[Adviser Name]
Research Adviser
```

---

## Authority Approval / Consent Block

```
After review of this request, the undersigned hereby:

[ ] Approves the conduct of controlled security testing under the agreed
    scope and conditions.

[ ] Approves with Conditions (see remarks below).

[ ] Does Not Approve the request.

Remarks / Conditions:
_________________________________________________________________________
_________________________________________________________________________

Authorized By:

Name:     __________________________
Position: ________________________
Signature: ______________________
Date:     ___________________________
```

---

## WIMS-BFP-Specific Fields

| Field | WIMS-BFP Value |
|-------|----------------|
| Research Title | WIMS-BFP: Forensics-Driven, Offline-Resilient Incident Monitoring Framework with Explainable AI for the Bureau of Fire Protection |
| Institution | FEU Institute of Technology |
| Program | BSIT with Specialization in Cybersecurity |
| Lead Researcher | Abricam Santillan Tinga |
| Faculty Adviser | [Adviser's Name] |
| Scope (example) | WIMS-BFP incident monitoring system, deployed test environment, login and records modules |
| Data Privacy | RA 10173 (Data Privacy Act of 2012) |

---

## Usage Context

This letter is part of the [[raw/articles/wims-bfp-ethical-security-testing-guide-2026-05-04]] package. It is sent **before** any testing begins, to the BFP IT department or designated authority.

**When to use:**
- If the panel or adviser requires documented external authorization
- If BFP will be the deployment environment and formal approval is needed
- When the IERC or ethics review board requires proof of authorized testing scope

**What to keep in the Appendices (Ch3 / Ch4 evidence):**
- Signed copy of this letter
- Authorized officer's name, position, and signature
- Approved scope description (from the filled-in form)

This document combined with the [[raw/articles/wims-bfp-ethical-security-testing-guide-2026-05-04]] provides the full ethical chain: authorized permission → controlled scope → documented evidence → responsible disclosure.
