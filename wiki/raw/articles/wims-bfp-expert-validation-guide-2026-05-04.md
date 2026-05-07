# WIMS-BFP — Expert Validation Guide

> **Source:** User-provided expert validation guidance
> **Captured:** 2026-05-04
> **Purpose:** Guide for validating research questionnaires for WIMS-BFP cybersecurity evaluation instruments
> **Type:** Methodology reference

---

## What is Expert Validation?

Expert validation is the review of the questionnaire by qualified individuals to determine whether the instrument is:
- Relevant to the study objectives
- Clear and understandable
- Appropriate for respondents
- Aligned with standards/frameworks
- Sufficient to measure intended variables
- Free from ambiguity or bias

For cybersecurity questionnaires, validators may also assess alignment with:
- NIST
- Security test planning
- Vulnerability assessment documentation
- Test methodology
- Evidence collection
- Reporting findings
- Remediation documentation

---

## Applicable Standards

### Guideline References

- **Guideline on Network Security Testing**
- **Guidelines on Minimum Standards for Developer Verification of Software**
- **ISO/IEC standards** — Functional Suitability, Reliability, Performance Efficiency, Usability, Security-related quality interpretation, System and Software Quality Models

### Cybersecurity Frameworks

- **Access control checklist**
- **Logging controls**
- **Incident handling**
- **Risk management**
- **Governance controls**
- **Information Security Management Systems — ISO 27001**

### OWASP ASVS — Test Cases Covered

| Test Case | Category |
|-----------|----------|
| Authentication Lockout | Authentication |
| Session Management | Security |
| Input Validation | Input Validation |
| SQL Injection Prevention | Injection |
| Access Control | Authorization |
| Secure Configuration | Configuration |
| Logging and Monitoring | Logging |
| Data Protection | Data Security |

### NIST CSF Core Functions

- Identify
- Protect
- Detect
- Respond
- Recover

---

## Test Case to Standard Mapping

| Test Case | Best Reference |
|-----------|---------------|
| Authentication Lockout | OWASP ASVS + NIST |
| SQL Injection | OWASP ASVS |
| Log Tamper Detection | NIST + ISO 27001 |
| HTTPS Enforcement | OWASP ASVS + ISO 27001 |
| Uptime Under Load | ISO 25010 + NIST |
| Role-Based Access Control | ISO 27001 + OWASP |
| Incident Logging | NIST + ISO 27001 |

### Combination Approach

- **OWASP ASVS** = Web application controls
- **NIST SP 800-115** = Testing process
- **ISO 25010** = System quality evaluation
- **ISO 27001** = Security governance / controls

---

## 7-Step Validation Procedure

### Step 1: Prepare the Draft Questionnaire

Before validation, finalize the initial version containing:
- Title of instrument
- Instructions
- Demographics
- Consent section
- Likert items
- Open-ended items (if any)
- Mapping to objectives/categories

**Internal Preparation Tip — Create an item matrix:**

| Item No. | Category | Objective | Standard Basis |
|----------|----------|-----------|----------------|
| Q1 | Authentication | Spoofing | OWASP ASVS |
| Q6 | Input Validation | Tampering | OWASP Top 10 |

---

### Step 2: Select Qualified Validators

Choose 3–5 validators.

| Validator Type | Example | Minimum |
|---------------|--------|---------|
| Academic Expert | IT/Cybersecurity faculty | 1 |
| Industry Expert | Security practitioner | 1 |
| Research Expert | Adviser / methodology expert | 1 |
| Domain Expert | Government IT personnel | 1 |

**Minimum recommendation:** At least 3 validators is strong and common.

---

### Step 3: Provide Validation Package

Send each validator a complete review packet. Include:
- Cover letter / request letter
- Research title
- Objectives of the study
- Questionnaire draft
- Validation rating sheet
- Instructions and deadline

---

### Step 4: Use a Validation Rating Form

Ask experts to rate each item.

**Sample Criteria:**

| Criterion | Meaning |
|-----------|---------|
| Relevance | Matches objective |
| Clarity | Easy to understand |
| Specificity | Clear and focused |
| Appropriateness | Suitable for respondents |
| Completeness | Enough items included |

**Example Scale:**

| Score | Meaning |
|-------|---------|
| 4 | Highly Valid |
| 3 | Valid |
| 2 | Needs Revision |
| 1 | Not Valid |

---

### Step 5: Consolidate Feedback

Collect:
- Scores
- Comments
- Suggested revisions
- Items to remove/add/edit

---

### Step 6: Revise the Questionnaire

Document all improvements made after validation.

**Example Revision Log:**

| Item | Original | Feedback | Revised Version |
|------|----------|----------|-----------------|
| Q9 | System is secure | Too broad | System appears protected against manipulation of form data |

---

### Step 7: Finalize Validated Instrument

Prepare the final version for pilot test or distribution.

---

## What to Write in Chapter 3

### Sample Academic Statement

> The questionnaire underwent expert validation prior to data collection. Three validators composed of one cybersecurity faculty member, one IT practitioner, and one research adviser reviewed the instrument in terms of relevance, clarity, appropriateness, and alignment with the study objectives. Comments and recommendations were consolidated, and necessary revisions were incorporated before final administration.

---

## Optional Quantitative Validation (Strongly Recommended)

### Content Validity Index (CVI)

If the panel expects stronger evidence, compute CVI.

**Item-Level CVI (I-CVI):**
```
I-CVI = Number of experts rating item as relevant / Total number of experts
```

Example: 3 out of 3 experts approved item → I-CVI = 1.00

**Scale-Level CVI (S-CVI):**
Average of all I-CVI scores.

**Suggested Interpretation:**

| CVI Score | Meaning |
|-----------|---------|
| 0.90 – 1.00 | Excellent |
| 0.80 – 0.89 | Good |
| Below 0.80 | Needs Revision |

---

## Documentation Requirements

### Required Files (Keep as Appendix or Adviser Evidence)

| Document | Purpose |
|----------|---------|
| Draft Questionnaire | Initial version |
| Validation Request Letter | Formal review request |
| Validator Profiles | Qualification evidence |
| Signed Validation Forms | Proof of review |
| Consolidated Feedback Sheet | Summary comments |
| Revision Log | Changes made |
| Final Questionnaire | Validated version |

### Suggested Supporting Evidence

- Email confirmations
- Signed certificates/endorsement
- Screenshots of meetings
- Expert comments sheets
- CV/position of validators

---

## Validation Form Template

### Questionnaire Validation Sheet

```
Research Title: ___________________
Validator Name: ___________________
Role/Position: ___________________    Company/Dept: ___________________

Direction:
Please rate each criterion using the four-point scale provided below.
A rating of 4 is the highest score and indicates that the item is highly
valid or excellent in quality. A rating of 3 means the item is valid and
generally acceptable, though minor improvements may still be considered. A
rating of 2 indicates that the item needs revision and requires improvement
before final use. A rating of 1 is the lowest score and means the item is
not valid or requires major revision prior to approval.

Criterion | Description | Rating (1–4) | Comment
---------|-------------|-------------|-------
Relevance | Matches objective |
Clarity | Easy to understand |
Appropriateness | Suitable for respondents |
Completeness | Enough items included |

Overall Recommendation:
[ ] Approved
[ ] Approved with Revisions
[ ] Needs Major Revision

Signature: ___________________
Date: ___________________
```

---

## Validation Request Letter Template

```
[Date]

[Name of Validator]
[Position / Designation]
[Department / Organization]
[Institution Name]
[Address]

Subject: Request for Expert Validation of Research Questionnaire

Dear [Name of Validator],

Warm greetings.

We, the undersigned researchers, respectfully request your assistance as an
expert validator for our research instrument entitled:

WIMS-BFP: Forensics-Driven, Offline-Resilient Incident Monitoring Framework
with Explainable AI for the Bureau of Fire Protection

This study is being conducted in partial fulfillment of the requirements
for the degree Bachelor of Science in Information Technology with
Specialization in Cybersecurity. The research focuses on the development
and evaluation of a secure and resilient incident monitoring framework
designed for mission-critical government operations, particularly within
the Bureau of Fire Protection (BFP).

Your professional knowledge and experience in the fields of information
technology, cybersecurity, systems evaluation, or research methodology
would be highly valuable in assessing the quality and appropriateness
of our questionnaire prior to its official distribution.

Objectives of the Study

The study generally aims to design, develop, and evaluate a secure
incident monitoring framework integrating explainable artificial intelligence,
cybersecurity safeguards, and offline-resilient capabilities.

Specifically, the study seeks to:
1. Develop a forensics-driven and offline-capable incident monitoring
   system for the Bureau of Fire Protection.
2. Integrate AI-assisted threat detection with explainable outputs to
   support decision-making.
3. Implement cybersecurity controls aligned with recognized standards
   and secure system design principles.
4. Evaluate the developed system in terms of Functional Suitability,
   Performance Efficiency, Reliability, Usability, Explainability, and
   Security Readiness.
5. Conduct Security Testing and Vulnerability Assessment using
   standards-based criteria.

Purpose of Validation

We respectfully request your review of the attached questionnaire in terms
of the following criteria:
- Relevance to the study objectives
- Clarity of statements and instructions
- Appropriateness for intended respondents
- Completeness of coverage
- Alignment with recognized standards or professional practice

Requested Action

Kindly review the attached questionnaire (Appendix A) and complete the
accompanying validation form (Appendix B). Any comments, recommendations,
or suggested revisions will be greatly appreciated and will be used solely
to improve the quality of the instrument.

Confidentiality and Ethical Use

Your feedback will be treated with respect and used only for academic
research purposes. Your name and professional role may be acknowledged
in the study, subject to your consent.

We sincerely hope for your favorable consideration of this request.
Your contribution will greatly strengthen the academic quality and
credibility of this study.

Thank you very much for your time, expertise, and support.

Respectfully yours,

[Lead Researcher Name]
Lead Researcher
BSIT-CST
FEU Institute of Technology

Noted by:
[Adviser's Name]
Research Adviser
[Department / Institution]
```

---

## WIMS-BFP Specific Validator Targets

Based on the [[raw/articles/wims-bfp-research-question-alignment-matrix-2026-05-04]], the questionnaire must cover these 6 objective areas:

| Objective | STRIDE Category | Relevant Standards |
|-----------|----------------|-------------------|
| User access management | Spoofing | OWASP ASVS + NIST |
| Data entry / records | Tampering | OWASP ASVS |
| Audit trail / logging | Repudiation | NIST + ISO 27001 |
| Sensitive information protection | Information Disclosure | OWASP ASVS + ISO 27001 |
| System continuity | Denial of Service | ISO 25010 + NIST |
| AI explainable outputs | (Cross-cutting) | ISO 25010 (Usability) |

Each questionnaire item should be mapped in the item matrix (Step 1) to one of these objective-STRIDE pairs with its OWASP ASVS or ISO 25010 basis.
