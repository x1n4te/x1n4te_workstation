# WIMS-BFP — Expert Validation Questionnaire (Draft)
## WIMS-BFP: Forensics-Driven, Offline-Resilient Incident Monitoring Framework with Explainable AI for the Bureau of Fire Protection

> **Source:** Derived from `[[raw/articles/wims-bfp-expert-validation-guide-2026-05-04]]`, `[[raw/articles/wims-bfp-security-testing-evaluation-questionnaire-2026-05-04]]`, and `[[raw/articles/wims-bfp-research-question-alignment-matrix-2026-05-04]]`
> **Purpose:** Expert validation package — questionnaire draft + item matrix + validation rating sheet
> **Date:** 2026-05-05
> **Status:** Draft — for expert validation only

---

# QUESTIONNAIRE DRAFT

## Section 1: Title of Instrument

**WIMS-BFP Expert Evaluation Questionnaire: Security and System Quality Assessment**

---

## Section 2: Instructions

**To the Validator:**

You are invited to review a draft questionnaire designed to gather expert evaluation data for the WIMS-BFP thesis research project. The questionnaire has two parts:

- **Part I** — Security Testing Evaluation (30 items, 6 categories)
- **Part II** — System Quality Evaluation (25 items, 5 categories)

Please evaluate each item using the four validation criteria: **Relevance**, **Clarity**, **Appropriateness**, and **Completeness**. Rate each item on a scale of 1 to 4:

| Score | Meaning       |
|-------|---------------|
| 4     | Highly Valid  |
| 3     | Valid         |
| 2     | Needs Revision|
| 1     | Not Valid     |

Your feedback will be used solely to improve the instrument before final administration. All responses will be treated confidentially.

**Deadline for submission:** [INSERT DATE]

---

## Section 3: Demographics of Validator

| Item                         | Response                                                                                                                                                                    |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Name (Optional)              |                                                                                                                                                                             |
| Highest Degree Earned        | [ ] Bachelor's  [ ] Master's  [ ] Doctorate  [ ] Other: ____                                                                                                                |
| Field of Specialization      |                                                                                                                                                                             |
| Current Role / Position      |                                                                                                                                                                             |
| Organization / Institution   |                                                                                                                                                                             |
| Years of Relevant Experience | [ ] Less than 1 year  [ ] 1–3 years  [ ] 4–6 years  [ ] 7+ years                                                                                                            |
| Role Category                | [ ] Academic Expert (IT/Cybersecurity faculty)  [ ] Industry Expert (Security practitioner)  [ ] Research Expert (Adviser / methodology)  [ ] Domain Expert (Government IT) |

---

## Section 4: Consent Statement

By completing and submitting this validation form, you confirm that:

1. You have read and understood the purpose of this validation
2. Your feedback will be used solely for academic research purposes
3. You voluntarily agree to participate in this validation review
4. Your name and role may be acknowledged in the study, subject to your consent

[ ] I consent to participate in this validation
[ ] I do not consent

---

## Section 5: Evaluation Questionnaire — Part I (Security Testing)

**Directions:** Rate each item below using the 4-point scale. Circle or mark your chosen score.

### 5A. Authentication Security
*Mapped to Objective 1: Secure user access management | STRIDE: Spoofing | Standard: OWASP ASVS + NIST*

| No. | Evaluation Statement                                                                 | Relevance | Clarity | Appropriateness | Completeness |
|-----|-------------------------------------------------------------------------------------|:---------:|:-------:|:---------------:|:------------:|
| 1   | The login process allows access only to authorized users.                           | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 2   | The system properly blocks repeated invalid login attempts.                         | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 3   | The account lockout mechanism protects against brute-force login abuse.             | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 4   | Access restrictions based on user roles are properly enforced.                      | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 5   | Session controls protect the system from unauthorized session reuse or hijacking.   | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |

**Comments on Authentication Security items:**
_______________________________________________________________

---

### 5B. Input Validation Security
*Mapped to Objective 2: Secure data entry and record management | STRIDE: Tampering | Standard: OWASP ASVS + OWASP Top 10*

| No. | Evaluation Statement                                                                 | Relevance | Clarity | Appropriateness | Completeness |
|-----|-------------------------------------------------------------------------------------|:---------:|:-------:|:---------------:|:------------:|
| 6   | The system properly validates required and optional user inputs before processing.   | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 7   | The system prevents or blocks submission of invalid or suspicious data.             | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 8   | Error messages during invalid input are clear and helpful to the user.              | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 9   | The system is protected against manipulation of form data by malicious users.       | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 10  | The input validation controls improve the overall trustworthiness of the system.     | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |

**Comments on Input Validation Security items:**
_______________________________________________________________

---

### 5C. Logging Integrity
*Mapped to Objective 3: Audit trail and activity monitoring | STRIDE: Repudiation | Standard: NIST + ISO 27001*

| No. | Evaluation Statement                                                                 | Relevance | Clarity | Appropriateness | Completeness |
|-----|-------------------------------------------------------------------------------------|:---------:|:-------:|:---------------:|:------------:|
| 11  | Important user activities are properly recorded by the system.                      | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 12  | Logs maintained by the system appear reliable and complete.                         | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 13  | The logging feature supports accountability of actions performed in the system.       | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 14  | The system is resistant to unauthorized modification of log records.                 | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 15  | Logs can support review and investigation activities when needed.                   | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |

**Comments on Logging Integrity items:**
_______________________________________________________________

---

### 5D. Data Protection
*Mapped to Objective 4: Protect sensitive information | STRIDE: Information Disclosure | Standard: OWASP ASVS + ISO 27001*

| No. | Evaluation Statement                                                                 | Relevance | Clarity | Appropriateness | Completeness |
|-----|-------------------------------------------------------------------------------------|:---------:|:-------:|:---------------:|:------------:|
| 16  | The system appears to protect sensitive information properly.                        | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 17  | Access to confidential data is limited to authorized users only.                    | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 18  | Sensitive information is not unnecessarily exposed on screen or in responses.        | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 19  | Login credentials and account data are handled securely throughout the session.      | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 20  | Overall, the system demonstrates acceptable data confidentiality practices.           | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |

**Comments on Data Protection items:**
_______________________________________________________________

---

### 5E. Availability
*Mapped to Objective 5: System continuity | STRIDE: Denial of Service | Standard: ISO 25010 + NIST*

| No. | Evaluation Statement                                                                 | Relevance | Clarity | Appropriateness | Completeness |
|-----|-------------------------------------------------------------------------------------|:---------:|:-------:|:---------------:|:------------:|
| 21  | The system remains accessible when needed by authorized users.                       | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 22  | The system performs reliably during repeated or continuous use.                     | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 23  | The system continues to support important tasks during connectivity interruptions.   | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 24  | The system recovers properly after unexpected interruptions or failures.             | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 25  | Overall, the system demonstrates dependable availability under normal conditions.    | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |

**Comments on Availability items:**
_______________________________________________________________

---

### 5F. Overall Security Readiness
*Cross-cutting — all 6 objectives | Standard: OWASP ASVS + NIST CSF*

| No. | Evaluation Statement                                                                 | Relevance | Clarity | Appropriateness | Completeness |
|-----|-------------------------------------------------------------------------------------|:---------:|:-------:|:---------------:|:------------:|
| 26  | The implemented security controls are appropriate for a government operational environment. | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 27  | The system demonstrates acceptable readiness for operational use in the BFP.        | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 28  | The system balances usability and security effectively for its intended users.       | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 29  | The identified safeguards strengthen overall trust in the system.                    | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 30  | Overall, the developed system demonstrates strong security quality for its purpose.  | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |

**Comments on Overall Security Readiness items:**
_______________________________________________________________

---

## Section 6: Evaluation Questionnaire — Part II (System Quality Evaluation)

**Directions:** Rate each item using the 4-point validation scale.

### 6A. Functional Suitability
*Mapped to all developmental objectives | Standard: ISO/IEC 25010*

| No. | Evaluation Statement                                                                 | Relevance | Clarity | Appropriateness | Completeness |
|-----|-------------------------------------------------------------------------------------|:---------:|:-------:|:---------------:|:------------:|
| 31  | The system provides the functions needed for fire incident monitoring and reporting. | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 32  | The system features operate correctly during actual use.                            | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 33  | The AI-generated outputs are relevant to operational decision-support needs.         | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 34  | The system supports intended tasks efficiently without unnecessary steps.             | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 35  | The system meets the expected requirements of its intended BFP users.               | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |

**Comments on Functional Suitability items:**
_______________________________________________________________

---

### 6B. Performance Efficiency
*Mapped to Objective 5: System continuity | Standard: ISO/IEC 25010*

| No. | Evaluation Statement                                                                 | Relevance | Clarity | Appropriateness | Completeness |
|-----|-------------------------------------------------------------------------------------|:---------:|:-------:|:---------------:|:------------:|
| 36  | The system responds promptly when commands or requests are submitted.                | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 37  | The system processes records and generates outputs without unnecessary delay.         | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 38  | AI-generated forensic narratives are produced within an acceptable time frame.        | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 39  | The system performs efficiently without significantly slowing down the browser.      | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 40  | The system maintains stable performance during repeated or simultaneous operations. | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |

**Comments on Performance Efficiency items:**
_______________________________________________________________

---

### 6C. Reliability
*Mapped to Objective 5: System continuity + Objective 3: Audit trail | Standard: ISO/IEC 25010*

| No. | Evaluation Statement                                                                 | Relevance | Clarity | Appropriateness | Completeness |
|-----|-------------------------------------------------------------------------------------|:---------:|:-------:|:---------------:|:------------:|
| 41  | The system remains stable during continuous operation over extended periods.         | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 42  | The system recovers properly after interruptions, refreshes, or unexpected exits.    | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 43  | The offline-first capability allows continued task support during connectivity loss.| 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 44  | Data entered offline is retained correctly and synced when connectivity returns.      | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 45  | The system performs consistently during normal operational use.                       | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |

**Comments on Reliability items:**
_______________________________________________________________

---

### 6D. Usability
*Mapped to all objectives | Standard: ISO/IEC 25010*

| No. | Evaluation Statement                                                                 | Relevance | Clarity | Appropriateness | Completeness |
|-----|-------------------------------------------------------------------------------------|:---------:|:-------:|:---------------:|:------------:|
| 46  | The system interface is clear and easy to understand for BFP personnel.              | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 47  | Navigation between system features is intuitive and easy to perform.                | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 48  | Labels, instructions, and menu options are understandable to the intended users.    | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 49  | The system is easy to learn for first-time users without extensive training.          | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 50  | Overall, the system is user-friendly for its intended BFP operational context.        | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |

**Comments on Usability items:**
_______________________________________________________________

---

### 6E. Explainability (AI Outputs)
*Mapped to Objective 6: Understandable automated outputs | Standard: ISO/IEC 25010 (Usability/Interpretability)*

| No. | Evaluation Statement                                                                 | Relevance | Clarity | Appropriateness | Completeness |
|-----|-------------------------------------------------------------------------------------|:---------:|:-------:|:---------------:|:------------:|
| 51  | AI-generated forensic narratives are presented in a format understandable to BFP personnel. | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 52  | The rationale behind AI-generated alerts or recommendations is clearly explained.  | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 53  | AI outputs are relevant and actionable for incident response decision-making.        | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 54  | The system provides sufficient transparency in how AI conclusions are derived.       | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |
| 55  | Overall, AI-generated outputs support informed decision-making by BFP operators.   | 1 2 3 4   | 1 2 3 4 | 1 2 3 4        | 1 2 3 4      |

**Comments on Explainability items:**
_______________________________________________________________

---

## Section 7: Open-Ended Feedback

**1. Which items did you find most effective or well-constructed? Why?**

_______________________________________________________________
_______________________________________________________________
_______________________________________________________________

**2. Which items need revision or improvement? Please specify the item number and reason.**

_______________________________________________________________
_______________________________________________________________
_______________________________________________________________

**3. Are there any missing topics or areas that should be covered in this instrument?**

_______________________________________________________________
_______________________________________________________________
_______________________________________________________________

**4. Additional comments or observations:**

_______________________________________________________________
_______________________________________________________________
_______________________________________________________________

---

## Section 8: Overall Recommendation

**Please check one:**

[ ] **Approved** — The instrument is ready for pilot testing
[ ] **Approved with Minor Revisions** — The instrument is fundamentally sound but needs minor improvements (specify in comments above)
[ ] **Needs Major Revision** — Significant changes are required before the instrument can be used

---

## Section 9: Signature

Validator Name (print): _______________________________

Signature: _______________________________

Date: _______________________________

---

---

# ITEM MATRIX (Internal Preparation Reference)

## Purpose
This matrix maps every questionnaire item to its category, research objective, and standards basis. Created during Step 1 of the validation procedure.

## Part I — Security Testing Evaluation (Q1–Q30)

| Item No. | Category              | Research Objective                   | STRIDE Category        | Standard Basis              |
|----------|-----------------------|-------------------------------------|------------------------|----------------------------|
| Q1       | Authentication        | Obj 1: Secure user access mgmt     | Spoofing               | OWASP ASVS + NIST          |
| Q2       | Authentication        | Obj 1: Secure user access mgmt     | Spoofing               | OWASP ASVS + NIST          |
| Q3       | Authentication        | Obj 1: Secure user access mgmt     | Spoofing               | OWASP ASVS + NIST          |
| Q4       | Authentication        | Obj 1: Secure user access mgmt     | Spoofing               | OWASP ASVS + NIST          |
| Q5       | Authentication        | Obj 1: Secure user access mgmt     | Spoofing               | OWASP ASVS + NIST          |
| Q6       | Input Validation      | Obj 2: Secure data entry mgmt      | Tampering              | OWASP ASVS + OWASP Top 10  |
| Q7       | Input Validation      | Obj 2: Secure data entry mgmt      | Tampering              | OWASP ASVS + OWASP Top 10  |
| Q8       | Input Validation      | Obj 2: Secure data entry mgmt      | Tampering              | OWASP ASVS + OWASP Top 10  |
| Q9       | Input Validation      | Obj 2: Secure data entry mgmt      | Tampering              | OWASP ASVS + OWASP Top 10  |
| Q10      | Input Validation      | Obj 2: Secure data entry mgmt      | Tampering              | OWASP ASVS + OWASP Top 10  |
| Q11      | Logging Integrity     | Obj 3: Audit trail & monitoring    | Repudiation            | NIST + ISO 27001           |
| Q12      | Logging Integrity     | Obj 3: Audit trail & monitoring    | Repudiation            | NIST + ISO 27001           |
| Q13      | Logging Integrity     | Obj 3: Audit trail & monitoring    | Repudiation            | NIST + ISO 27001           |
| Q14      | Logging Integrity     | Obj 3: Audit trail & monitoring    | Repudiation            | NIST + ISO 27001           |
| Q15      | Logging Integrity     | Obj 3: Audit trail & monitoring    | Repudiation            | NIST + ISO 27001           |
| Q16      | Data Protection       | Obj 4: Protect sensitive info      | Information Disclosure | OWASP ASVS + ISO 27001     |
| Q17      | Data Protection       | Obj 4: Protect sensitive info      | Information Disclosure | OWASP ASVS + ISO 27001     |
| Q18      | Data Protection       | Obj 4: Protect sensitive info      | Information Disclosure | OWASP ASVS + ISO 27001     |
| Q19      | Data Protection       | Obj 4: Protect sensitive info      | Information Disclosure | OWASP ASVS + ISO 27001     |
| Q20      | Data Protection       | Obj 4: Protect sensitive info      | Information Disclosure | OWASP ASVS + ISO 27001     |
| Q21      | Availability          | Obj 5: System continuity           | Denial of Service      | ISO 25010 + NIST           |
| Q22      | Availability          | Obj 5: System continuity           | Denial of Service      | ISO 25010 + NIST           |
| Q23      | Availability          | Obj 5: System continuity           | Denial of Service      | ISO 25010 + NIST           |
| Q24      | Availability          | Obj 5: System continuity           | Denial of Service      | ISO 25010 + NIST           |
| Q25      | Availability          | Obj 5: System continuity           | Denial of Service      | ISO 25010 + NIST           |
| Q26      | Overall Security      | All 6 objectives (cross-cutting)   | All categories          | OWASP ASVS + NIST CSF      |
| Q27      | Overall Security      | All 6 objectives (cross-cutting)   | All categories          | OWASP ASVS + NIST CSF      |
| Q28      | Overall Security      | All 6 objectives (cross-cutting)   | All categories          | OWASP ASVS + NIST CSF      |
| Q29      | Overall Security      | All 6 objectives (cross-cutting)   | All categories          | OWASP ASVS + NIST CSF      |
| Q30      | Overall Security      | All 6 objectives (cross-cutting)   | All categories          | OWASP ASVS + NIST CSF      |

## Part II — System Quality Evaluation (Q31–Q55)

| Item No. | Category              | Research Objective                   | ISO/IEC 25010 Quality Factor |
|----------|-----------------------|-------------------------------------|-----------------------------|
| Q31      | Functional Suitability | All developmental objectives        | Functional Suitability      |
| Q32      | Functional Suitability | All developmental objectives        | Functional Suitability      |
| Q33      | Functional Suitability | Obj 6: AI explainable outputs       | Functional Suitability      |
| Q34      | Functional Suitability | All developmental objectives        | Functional Suitability      |
| Q35      | Functional Suitability | All developmental objectives        | Functional Suitability      |
| Q36      | Performance Efficiency | Obj 5: System continuity            | Performance Efficiency       |
| Q37      | Performance Efficiency | Obj 5: System continuity            | Performance Efficiency       |
| Q38      | Performance Efficiency | Obj 6: AI explainable outputs       | Performance Efficiency       |
| Q39      | Performance Efficiency | Obj 5: System continuity            | Performance Efficiency       |
| Q40      | Performance Efficiency | Obj 5: System continuity            | Performance Efficiency       |
| Q41      | Reliability           | Obj 5: System continuity              | Reliability                  |
| Q42      | Reliability           | Obj 5: System continuity              | Reliability                  |
| Q43      | Reliability           | Obj 5: System continuity              | Reliability                  |
| Q44      | Reliability           | Obj 3: Audit trail (data integrity) | Reliability                  |
| Q45      | Reliability           | Obj 5: System continuity              | Reliability                  |
| Q46      | Usability             | All objectives (user-facing)          | Usability                   |
| Q47      | Usability             | All objectives (user-facing)          | Usability                   |
| Q48      | Usability             | All objectives (user-facing)          | Usability                   |
| Q49      | Usability             | All objectives (user-facing)          | Usability                   |
| Q50      | Usability             | All objectives (user-facing)          | Usability                   |
| Q51      | Explainability        | Obj 6: AI explainable outputs        | Usability/Interpretability   |
| Q52      | Explainability        | Obj 6: AI explainable outputs        | Usability/Interpretability   |
| Q53      | Explainability        | Obj 6: AI explainable outputs        | Usability/Interpretability   |
| Q54      | Explainability        | Obj 6: AI explainable outputs        | Usability/Interpretability   |
| Q55      | Explainability        | Obj 6: AI explainable outputs        | Usability/Interpretability   |

---

## Research Objective Reference

| # | Objective | STRIDE | ISO 25010 |
|---|-----------|--------|-----------|
| 1 | Develop secure user access management for authorized users | Spoofing | Functional Suitability + Usability |
| 2 | Develop secure data entry and record management features | Tampering | Functional Suitability |
| 3 | Implement audit trail and activity monitoring features | Repudiation | Functional Suitability + Reliability |
| 4 | Protect sensitive information during access and transmission | Information Disclosure | Reliability + Functional Correctness |
| 5 | Maintain system continuity during stress or interruptions | Denial of Service | Performance Efficiency + Reliability |
| 6 | Provide understandable automated outputs for decision support | (Cross-cutting) | Usability + Explainability |

---

## Validation Criteria Definitions

| Criterion       | Meaning                                                          |
| --------------- | ---------------------------------------------------------------- |
| Relevance       | Item matches the stated objective and category appropriately     |
| Clarity         | Item is easy to understand, free from ambiguity                  |
| Appropriateness | Item is suitable for the intended respondents (BFP context)      |
| Completeness    | Item sufficiently covers the objective; no major gaps identified |

---

## CVI Computation Guide

**Item-Level CVI (I-CVI):**
```
I-CVI = Number of validators rating item as 3 or 4 (Valid or Highly Valid) / Total number of validators
```

**Scale-Level CVI (S-CVI):**
```
S-CVI = Average of all I-CVI scores across the instrument
```

**Interpretation:**

| CVI Score | Meaning     |
|-----------|-------------|
| 0.90–1.00 | Excellent   |
| 0.80–0.89 | Good        |
| Below 0.80 | Needs Revision |

---

## Revision Log Template (Step 6)

| Item No. | Original Statement | Validator Feedback | Revised Statement |
|----------|-------------------|--------------------|-------------------|
| Q__      | (copy original)   | (feedback summary) | (revised version) |
|          |                   |                    |                   |
|          |                   |                    |                   |

---

*Prepared according to the 7-step expert validation procedure.*
*For WIMS-BFP thesis research — FEU Institute of Technology, BSIT-Cybersecurity*
