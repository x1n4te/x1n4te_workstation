---
id: wims-bfp-expert-validation-questionnaire-001
type: analysis
created: 2026-05-04
updated: 2026-05-04
last_verified: 2026-05-04
review_after: 2026-08-04
stale_after: 2026-11-04
confidence: high
source_refs:
  - raw/articles/wims-bfp-frs-consolidated-2026-05-04.md
  - raw/articles/wims-bfp-expert-validation-guide-2026-05-04.md
status: active
tags:
  - wims-bfp
  - thesis
  - expert-validation
  - questionnaire
  - cybersecurity
related:
  - analyses/wims-bfp-thesis-codebase-gaps
  - concepts/wims-bfp-codebase-threat-model
  - sources/articles/wims-bfp-frs-consolidated-2026-05-04.md
  - raw/articles/wims-bfp-expert-validation-guide-2026-05-04.md
---

# WIMS-BFP Cybersecurity Evaluation Instrument: Expert Validation Questionnaire

> **Version:** 1.0  
> **Date:** May 4, 2026  
> **Purpose:** Expert validation of the cybersecurity evaluation instruments for WIMS-BFP  
> **Target Validators:** Cybersecurity faculty, industry practitioners, research advisers, government IT personnel

---

## Instructions to Validators

**Dear Expert,**

Thank you for agreeing to review this instrument. Your expertise is invaluable in ensuring the quality and validity of this research.

**Please review each item carefully and rate it according to the following criteria:**

- **4 - Highly Valid:** The item is excellent, clear, and perfectly aligned with the objective
- **3 - Valid:** The item is good and generally aligned, but may need minor improvements
- **2 - Needs Revision:** The item has significant issues and requires substantial revision
- **1 - Not Valid:** The item is inappropriate and should be removed or completely rewritten

**For any item rated 2 or 1, please provide specific suggestions for improvement in the comments section.**

**Please also complete the demographic information and consent form at the beginning of this questionnaire.**

**Deadline for submission:** [Insert deadline date]

**Contact:** [Your email address]

We greatly appreciate your time and expertise!

---

## Part A: Demographics and Consent

### A1: Validator Information

| # | Question | Options |
|---|----------|---------|
| 1 | Full Name | ________ |
| 2 | Professional Title/Position | ________ |
| 3 | Affiliation/Organization | ________ |
| 4 | Highest Educational Attainment | ☐ Bachelor's ☐ Master's ☐ PhD/EdD ☐ Other |
| 5 | Area of Specialization | ________ |
| 6 | Years of Experience in Cybersecurity | ☐ <2 ☐ 2-5 ☐ 6-10 ☐ >10 |
| 7 | Email Address | ________ |

### A2: Consent to Participate

**Research Title:** WIMS-BFP: A Secure Web Incident Monitoring System with AI-Assisted Threat Detection for Cybersecurity-Specific Forensics-Driven Analysis in the Bureau of Fire Protection

**Researcher:** [Your Name], BSIT Cybersecurity Student, FEU-TECH

**Purpose:** You are being asked to participate in this study as an expert validator to review the cybersecurity evaluation instruments for WIMS-BFP. Your feedback will help ensure the validity and reliability of the research instruments.

**Procedures:** You will be asked to review several instruments (questionnaires, evaluation criteria, validation guides) and provide ratings and comments on their relevance, clarity, appropriateness, and alignment with study objectives.

**Risks/Discomforts:** There are no anticipated risks beyond normal educational activities.

**Benefits:** Your participation will contribute to the improvement of cybersecurity evaluation instruments for incident monitoring systems, which may benefit future research and practice.

**Confidentiality:** Your responses will be kept confidential. Only the research team will have access to the data. Your name will not be associated with any published findings without your consent.

**Voluntary Participation:** Your participation is voluntary. You may skip any item or withdraw from the study at any time without penalty.

**Contact Information:**
- **Researcher:** [Your Name], [Your Email], [Your Phone]
- **Adviser:** [Adviser Name], [Adviser Email]
- **Institution:** FEU-TECH, BSIT Cybersecurity Program

**I have read and understood the above information and consent to participate in this study.**

☐ Yes, I consent to participate  
☐ No, I do not wish to participate

---

## Part B: Instrument Validation Items

### B1: FRS Modules Implementation Tracker

**Instructions:** The following table maps research objectives to FRS modules. Please rate each objective's alignment with the corresponding module.

| # | Research Objective | Corresponding FRS Module | Relevance (1-4) | Clarity (1-4) | Appropriateness (1-4) | Comments/Suggestions |
|---|--------------------|--------------------------|-----------------|---------------|----------------------|----------------------|
| 1 | Design PWA offline data capture | Module 2: Offline-First Incident Management | | | | |
| 2 | Implement RBAC with Keycloak | Module 1: Authentication and Access Control | | | | |
| 3 | Establish cryptographic pipeline | Module 6: Cryptographic Security | | | | |
| 4 | Integrate Suricata IDS + Qwen2.5-3B XAI | Module 8: Threat Detection with Explanation AI | | | | |
| 5 | Public civilian reporting portal | Module 5d: Public Anonymous Incident Submission | | | | |
| 6 | National Analytics with PostGIS | Module 5: Analytics and Reporting | | | | |
| 7 | Data Privacy Act compliance | Module 10: Compliance and Data Privacy | | | | |
| 8 | Security testing & OWASP ASVS | Module 11: Penetration Testing and Security Validation | | | | |

### B2: Security Testing Evaluation Criteria

**Instructions:** Rate the relevance and clarity of the security testing evaluation criteria.

| # | Evaluation Category | Test Case Description | Relevance (1-4) | Clarity (1-4) | Appropriateness (1-4) | Comments/Suggestions |
|---|---------------------|----------------------|-----------------|---------------|----------------------|----------------------|
| 1 | Authentication | Authentication lockout after 5 failed attempts | | | | |
| 2 | Session Management | JWT token expiry behavior; session revocation | | | | |
| 3 | Input Validation | Input sanitization and validation | | | | |
| 4 | SQL Injection Prevention | Database query parameterization | | | | |
| 5 | Access Control | Role-based access enforcement | | | | |
| 6 | Secure Configuration | HTTPS enforcement, security headers | | | | |
| 7 | Logging and Monitoring | Audit log completeness, tamper detection | | | | |
| 8 | Data Protection | Encryption at rest and in transit | | | | |

### B3: Threat Detection XAI Evaluation Criteria

**Instructions:** Rate the criteria for evaluating the Explainable AI (XAI) component.

| # | Evaluation Aspect | Specific Criteria | Relevance (1-4) | Clarity (1-4) | Appropriateness (1-4) | Comments/Suggestions |
|---|-------------------|-------------------|-----------------|---------------|----------------------|----------------------|
| 1 | Suricata Rule Coverage | Coverage of OWASP Top 10, custom BFP rules | | | | |
| 2 | Alert-to-Narrative Translation | Accuracy of AI-generated explanations | | | | |
| 3 | AI Response Time | Under load conditions | | | | |
| 4 | Explainability Quality | Clarity of forensic narratives | | | | |
| 5 | Integration with IDS | Seamless workflow with Suricata alerts | | | | |

### B4: Civilian Reporting Portal Evaluation Criteria

**Instructions:** Rate the criteria for evaluating the public anonymous incident submission portal.

| # | Evaluation Aspect | Specific Criteria | Relevance (1-4) | Clarity (1-4) | Appropriateness (1-4) | Comments/Suggestions |
|---|-------------------|-------------------|-----------------|---------------|----------------------|----------------------|
| 1 | Rate Limiting | 3 requests per IP per hour enforcement | | | | |
| 2 | Geographic Boundary Enforcement | Region resolution via nearest-centroid | | | | |
| 3 | Data Validation | Pydantic schema validation effectiveness | | | | |
| 4 | PII Minimization | No unnecessary personal information collected | | | | |
| 5 | Abuse Prevention | Rate limiting as sole mechanism | | | | |

### B5: Analytics Module Evaluation Criteria

**Instructions:** Rate the criteria for evaluating the National Analytics module.

| # | Evaluation Aspect | Specific Criteria | Relevance (1-4) | Clarity (1-4) | Appropriateness (1-4) | Comments/Suggestions |
|---|-------------------|-------------------|-----------------|---------------|----------------------|----------------------|
| 1 | Geospatial Clustering | Correctness of PostGIS clustering | | | | |
| 2 | Heatmap Rendering | Completeness and performance | | | | |
| 3 | Query Response Time | Under various date ranges and filters | | | | |
| 4 | Comparative Analysis | Cross-region comparison accuracy | | | | |
| 5 | Variance Tracking | Trend analysis correctness | | | | |

### B6: Data Privacy Compliance Evaluation Criteria

**Instructions:** Rate the criteria for evaluating compliance with RA 10173 and ISO 27001.

| # | Evaluation Aspect | Specific Criteria | Relevance (1-4) | Clarity (1-4) | Appropriateness (1-4) | Comments/Suggestions |
|---|-------------------|-------------------|-----------------|---------------|----------------------|----------------------|
| 1 | RLS Enforcement | Cross-region data access blocking | | | | |
| 2 | Audit Log Completeness | Logging of all relevant events | | | | |
| 3 | Data Minimization | Collection of only necessary data | | | | |
| 4 | Retention Policies | Compliance with 10-year requirement | | | | |
| 5 | DPIA Documentation | Completeness of Data Privacy Impact Assessment | | | | |

### B7: Overall System Evaluation (ISO 25010)

**Instructions:** Rate the overall system quality based on ISO 25010 characteristics.

| # | ISO 25010 Characteristic | Relevance to WIMS-BFP (1-4) | Comments/Suggestions |
|---|--------------------------|-----------------------------|----------------------|
| 1 | Functional Suitability | | |
| 2 | Performance Efficiency | | |
| 3 | Reliability | | |
| 4 | Usability | | |
| 5 | Security | | |
| 6 | Maintainability | | |
| 7 | Portability | | |

---

## Part C: Open-Ended Feedback

### C1: General Comments
Please provide any additional comments, suggestions, or concerns about the instruments:

---

### C2: Suggested Improvements
What specific improvements would you recommend for the cybersecurity evaluation instruments?

---

### C3: Missing Elements
Do you think any important elements are missing from the instruments? If yes, please specify:

---

## Part D: Validator's Declaration

I have reviewed the WIMS-BFP cybersecurity evaluation instruments and provide the ratings and comments above based on my expertise.

**Validator Signature:** ____________________  
**Date:** ____________________  
**Position/Title:** ____________________  
**Affiliation:** ____________________  

---

## Item Matrix for Validation

| Item # | Category | Research Objective | Corresponding FRS Module | Standard Basis |
|--------|----------|-------------------|--------------------------|----------------|
| Q1 | Offline-First PWA | Design PWA offline data capture | Module 2 | ISO 25010, NIST SP 800-147 |
| Q2 | RBAC Implementation | Implement RBAC with Keycloak | Module 1 | OWASP ASVS, ISO 27001 |
| Q3 | Cryptographic Security | Establish cryptographic pipeline | Module 6 | FIPS 140-2, NIST SP 800-52 |
| Q4 | XAI Integration | Integrate Suricata IDS + Qwen2.5-3B | Module 8 | OWASP Application Security Verification Standard |
| Q5 | Civilian Reporting | Public civilian reporting portal | Module 5d | RA 10173, Data Privacy Act |
| Q6 | Analytics Evaluation | National Analytics with PostGIS | Module 5 | ISO 25010, NIST SP 800-115 |
| Q7 | Data Privacy Compliance | RA 10173 and ISO 27001 alignment | Module 10 | RA 10173, ISO 27001:2013 |
| Q8 | Security Testing | OWASP ASVS Level 2 compliance | Module 11 | OWASP ASVS, NIST SP 800-115 |

---

**Thank you for your valuable contribution to this research!**
