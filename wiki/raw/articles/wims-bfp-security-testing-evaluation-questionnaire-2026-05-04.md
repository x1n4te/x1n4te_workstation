# WIMS-BFP — Security Testing Evaluation Questionnaire + Guidelines

> **Source:** User-provided security testing evaluation instrument + technical testing guidelines
> **Captured:** 2026-05-04
> **Purpose:** Gather expert perception data on security controls + guide technical security test documentation for Ch4
> **Type:** Research instrument + methodology guide

---

## Instrument Overview

This instrument has two parts:
1. **Security Testing Evaluation Questionnaire** — perception-based expert feedback on security controls (survey)
2. **Security Testing and Vulnerability Assessment Guidelines** — technical testing documentation format for Ch4 evidence

The questionnaire provides **expert/perception evidence** for security readiness. The guidelines produce **technical evidence** through actual testing. Together they form the complete security findings in Chapter 4.

---

# PART I: SECURITY TESTING EVALUATION QUESTIONNAIRE

## Instrument Purpose

Gather evaluator or subject expert feedback regarding the effectiveness, suitability, and readiness of the security controls implemented in the developed system. Supports the research objectives by providing perception-based evidence that complements the technical results of the Security Testing and Vulnerability Assessment.

---

## PART I-A. Demographics

| Item | Response |
|------|---------|
| Name (Optional) | |
| Age | |
| Sex | [ ] Male  [ ] Female  [ ] Prefer not to say |
| Current Role | [ ] IT Professional  [ ] Cybersecurity Expert  [ ] Faculty  [ ] Student  [ ] Government Personnel  [ ] Other: ______ |
| Organization / Institution (Optional) | |
| Years of Relevant Experience | [ ] Less than 1 year  [ ] 1–3 years  [ ] 4–6 years  [ ] 7+ years |
| Familiarity with Information Security | [ ] Beginner  [ ] Intermediate  [ ] Advanced |
| Familiarity with System Evaluation | [ ] Beginner  [ ] Intermediate  [ ] Advanced |
| Familiarity with Similar Systems | [ ] Beginner  [ ] Intermediate  [ ] Advanced |

**Purpose of Demographic Data:**
The demographic information will be used only to describe the profile of the respondents in summarized form (e.g., frequency and percentage distribution). Individual identities will not be disclosed in any report or publication.

---

## PART I-B. Data Privacy and Consent Agreement

**Privacy Notice and Informed Consent**

This questionnaire is being conducted as part of an academic research study. Your participation is voluntary. Before you decide to participate, please note the following:

1. **Data to Be Collected**
   - Basic demographic information (role, experience level, familiarity with topic)
   - Responses to evaluation questions
   - Optional comments or suggestions
   - No highly sensitive personal information is required.

2. **Purpose of Data Collection**
   - To evaluate the security quality and readiness of the developed system
   - To compute statistical summaries such as weighted mean, frequency, and percentage
   - To support the findings, conclusions, and recommendations of the study

3. **Data Processing and Storage**
   - Encoded and processed only by the authorized researchers
   - Stored securely in password-protected digital files or secured storage devices
   - Used only within the duration of the study and related academic review process

4. **Confidentiality and Anonymity**
   - Identity will remain confidential
   - Individual responses will not be publicly disclosed
   - Results will be presented only in aggregated or summarized form

5. **Voluntary Participation**
   - Participation is completely voluntary
   - May decline to answer any question or withdraw at any time without penalty

6. **Legal Basis**
   - Aligned with the Data Privacy Act of 2012 (Republic Act No. 10173), particularly transparency, legitimate purpose, and proportionality

**Consent Statement:**
[ ] I have read and understood the information above. I voluntarily agree to participate in this study.
[ ] I do not agree to participate.

*(Only respondents who provide consent should proceed to Part III.)*

---

## PART I-C. Evaluation Questionnaire (5-Point Likert Scale)

**Directions:** Please rate each statement based on your assessment of the developed system.

| Scale | Meaning |
|-------|---------|
| 5 | Strongly Agree |
| 4 | Agree |
| 3 | Neutral |
| 2 | Disagree |
| 1 | Strongly Disagree |

### A. Authentication Security

| No. | Evaluation Statement | Rating |
|-----|---------------------|--------|
| 1 | The login process allows access only to authorized users. | 1 2 3 4 5 |
| 2 | The system properly blocks invalid login attempts. | 1 2 3 4 5 |
| 3 | The account lockout mechanism helps protect against repeated login abuse. | 1 2 3 4 5 |
| 4 | Access restrictions based on user roles are properly enforced. | 1 2 3 4 5 |
| 5 | Session controls help protect the system from unauthorized reuse. | 1 2 3 4 5 |

### B. Input Validation Security

| No. | Evaluation Statement | Rating |
|-----|---------------------|--------|
| 6 | The system properly validates required user inputs. | 1 2 3 4 5 |
| 7 | The system prevents invalid or suspicious data submission. | 1 2 3 4 5 |
| 8 | Error messages are clear and helpful during invalid input. | 1 2 3 4 5 |
| 9 | The system appears protected against manipulation of form data. | 1 2 3 4 5 |
| 10 | Overall, the input controls improve system trustworthiness. | 1 2 3 4 5 |

### C. Logging Integrity

| No. | Evaluation Statement | Rating |
|-----|---------------------|--------|
| 11 | Important user activities are properly recorded by the system. | 1 2 3 4 5 |
| 12 | Logs appear reliable and complete. | 1 2 3 4 5 |
| 13 | The logging feature supports accountability of actions performed. | 1 2 3 4 5 |
| 14 | The system appears resistant to unauthorized log changes. | 1 2 3 4 5 |
| 15 | Logs can help during review or investigation activities. | 1 2 3 4 5 |

### D. Data Protection

| No. | Evaluation Statement | Rating |
|-----|---------------------|--------|
| 16 | The system appears to protect sensitive information properly. | 1 2 3 4 5 |
| 17 | Access to confidential data is limited to authorized users. | 1 2 3 4 5 |
| 18 | Sensitive information is not unnecessarily exposed on screen. | 1 2 3 4 5 |
| 19 | The system handles login and account data securely. | 1 2 3 4 5 |
| 20 | Overall, the system demonstrates acceptable data confidentiality. | 1 2 3 4 5 |

### E. Availability

| No. | Evaluation Statement | Rating |
|-----|---------------------|--------|
| 21 | The system remains accessible when needed. | 1 2 3 4 5 |
| 22 | The system performs reliably during repeated use. | 1 2 3 4 5 |
| 23 | The system continues to support important tasks during connectivity issues. | 1 2 3 4 5 |
| 24 | The system recovers properly after interruptions. | 1 2 3 4 5 |
| 25 | Overall, the system demonstrates dependable availability. | 1 2 3 4 5 |

### F. Overall Security Readiness

| No. | Evaluation Statement | Rating |
|-----|---------------------|--------|
| 26 | The implemented security controls are appropriate for the intended environment. | 1 2 3 4 5 |
| 27 | The system demonstrates acceptable readiness for operational use. | 1 2 3 4 5 |
| 28 | The system balances usability and security effectively. | 1 2 3 4 5 |
| 29 | The identified safeguards strengthen trust in the system. | 1 2 3 4 5 |
| 30 | Overall, the developed system demonstrates strong security quality. | 1 2 3 4 5 |

---

## PART I-D. Open-Ended Feedback (Optional)

1. What security feature of the system did you find most effective?

2. What improvements would you recommend for the system's security controls?

3. Additional comments or observations:

---

## Suggested KPI Table

| Category | Target Weighted Mean |
|----------|-------------------|
| Authentication Security | ≥ 4.00 |
| Input Validation | ≥ 4.00 |
| Logging Integrity | ≥ 4.00 |
| Data Protection | ≥ 4.00 |
| Availability | ≥ 4.00 |
| Overall Security Readiness | ≥ 4.00 |

---

## Documentation Note

This instrument may be attached in the Appendix and referenced in Chapter 3 under:
- Data Gathering Instruments
- Data Gathering Procedure
- Ethical and Legal Considerations
- Statistical Treatment of Data

---

# PART II: RESEARCH GUIDELINES FOR THE SECURITY TESTING EVALUATION QUESTIONNAIRE

## 1. Documented Computation for Evidence

All survey results must be supported by clear and traceable computations.

**Researchers should maintain:**
- Completed response forms or digital responses
- Encoded datasets (Excel, spreadsheet, or statistical software)
- Formula-based computations
- Summary tables used in the manuscript
- Copies of charts or graphs generated from the data

**Minimum Expected Outputs:**
- Weighted Mean per item
- Weighted Mean per category
- Composite Mean for overall security readiness
- Frequency or percentage distribution of respondents (if applicable)

**Weighted Mean Formula:**
```
WM = (Σfx) / N
Where:
  f = frequency of responses
  x = scale value
  N = total number of responses
```

**Guideline:** Calculations in the manuscript must be reproducible from the stored dataset.

---

## 2. Questionnaire Must Be Validated Before Distribution

**Recommended Validation Process:**

**A. Content Validation**
Reviewers should assess whether items are:
- Relevant to the study objectives
- Clear and understandable
- Free from ambiguity
- Appropriate for the intended respondents
- Sufficient to measure the target constructs

**B. Face Validation**
A small group of intended respondents may review the questionnaire for ease of understanding.

**C. Pilot Testing (Recommended)**
A limited trial administration before actual data collection to identify unclear items.

**Guideline:** Only validated instruments should be used for final data gathering.

---

## 3. Questionnaire Must Be Aligned with Cybersecurity Standards

Items should reflect recognized cybersecurity principles, control domains, or industry standards — not personal opinion.

| Standard / Framework | Example Use in Questionnaire |
|---------------------|------------------------------|
| NIST Cybersecurity Framework (CSF) | Access control, detection, response readiness |
| NIST SP 800 Series | Authentication, logging, incident handling |
| ISO/IEC 27001 | Information security controls and governance |
| ISO/IEC 25010 | Security, reliability, usability quality factors |
| OWASP ASVS | Secure authentication, validation, session management |
| OWASP Top 10 | Common web vulnerabilities |
| CIS Controls | Defensive baseline controls |

**Examples of Alignment:**

| Questionnaire Section | Standards |
|-----------------------|-----------|
| Authentication Security | NIST / OWASP ASVS |
| Input Validation | OWASP ASVS / OWASP Top 10 |
| Logging Integrity | NIST / ISO 27001 |
| Data Protection | ISO 27001 / Data Privacy principles |
| Availability | NIST / Resilience frameworks |

**Guideline:** State in Chapter 3 that items were developed or reviewed with reference to recognized cybersecurity standards.

---

## 4. Identify the Qualification and Role of Respondents

**Possible Respondent Categories:**
- Cybersecurity professionals
- IT administrators
- Software developers
- Faculty members in IT/Cybersecurity
- Government IT personnel
- System users with operational experience
- Graduate students with relevant specialization

**Qualification Criteria:**
- Educational background in IT or related field
- Professional experience in security or systems
- Familiarity with system testing or evaluation
- Experience using similar systems
- Role related to the project environment

**Example Statement:**
> Respondents were selected using purposive sampling based on their relevant experience in cybersecurity, system evaluation, or operational use of similar information systems.

---

## 5. Ethical and Legal Compliance

Obtain informed consent and explain how responses will be collected, stored, processed, and reported. Align with institutional ethics policies and Data Privacy Act of 2012 (RA 10173).

---

## 6. Appropriate Statistical Treatment

**Recommended:**
- Weighted Mean
- Frequency and Percentage
- Composite Mean
- Ranking
- Standard Deviation (optional)
- Cronbach's Alpha (for reliability testing, recommended)

---

## 7. Clear Use of Results in Chapter 4

Survey findings support interpretation of security readiness — they do not replace actual technical testing.

**Best practice:**
- Technical testing = objective evidence
- Survey evaluation = expert/perception evidence
- Together, they produce stronger findings

**One-Line Research Principle:**
> A strong security questionnaire is not only well-written — it is validated, standards-based, evidence-supported, and answered by qualified respondents.

---

# PART III: SECURITY TESTING AND VULNERABILITY ASSESSMENT GUIDELINES

## Purpose

Security Testing and Vulnerability Assessment produces **technical evidence** through actual testing, measurable outcomes, and documented remediation results — distinct from the perception-based survey above.

Testing scope must align with identified security requirements, STRIDE threat categories, and recognized standards (OWASP ASVS, OWASP Top 10, NIST guidance).

---

## I. Recommended Security Testing Areas

### Core Security Evidence Table

| Security Area | Example Metric | STRIDE Category |
|--------------|---------------|-----------------|
| Authentication Security | Authentication Lockout | Spoofing |
| Input Validation | SQL Injection Success Rate | Tampering |
| Logging Integrity | Log Tamper Detection | Repudiation |
| Data Protection | HTTPS Enforcement | Information Disclosure |
| Availability | Uptime Under Load | Denial of Service |

### Aligned with Approved Objectives

**Example Approved Objective:**
> To conduct structured Security Testing and Vulnerability Assessment aligned with the OWASP Application Security Verification Standard (ASVS) to evaluate, document, and remediate vulnerabilities related to the STRIDE threat categories, including:
> a. Spoofing — Credential abuse and authentication bypass
> b. Tampering — SQL injection and unauthorized record modification
> c. Repudiation — Audit log modification and activity traceability weaknesses
> d. Information Disclosure — Unauthorized exposure of sensitive data
> e. Denial of Service — System availability disruption under stress conditions

### Detailed Test Mapping Table

| Security Area | Example Metric | STRIDE | Objective Alignment |
|--------------|---------------|--------|-------------------|
| Authentication Security | Authentication Lockout | Spoofing | Credential abuse / authentication bypass |
| Input Validation | SQL Injection Success Rate | Tampering | SQL injection prevention |
| Record Integrity | Unauthorized Record Modification Detection | Tampering | Record modification attempts |
| Logging Integrity | Log Tamper Detection | Repudiation | Audit log modification |
| Activity Traceability | Activity Logging Completeness | Repudiation | Activity traceability weaknesses |
| Data Protection | HTTPS Enforcement | Information Disclosure | Sensitive data protection |
| Access Control | Unauthorized Data Access Block Rate | Information Disclosure | Unauthorized exposure prevention |
| Availability | Uptime Under Load | Denial of Service | Service continuity under stress |
| Resilience | Recovery After Interruption | Denial of Service | Operational continuity |

---

## Research Notes for Students

1. **Every Security Test Must Match an Objective**
   Before conducting any test, ask: Which specific objective does this support? Which threat category? Which requirement?
   If no clear connection exists, reconsider whether the test belongs.

2. **Do Not Add Random Security Tests**
   Avoid adding tests only because tools are available (e.g., wireless hacking if system is web-based only).
   All testing must remain within approved project boundaries.

3. **Show Traceability in Documentation**
   Example traceability table for Chapter 4:

   | Objective | Test Conducted | Result |
   |-----------|---------------|--------|
   | Prevent SQL Injection | SQL Injection Test | Passed |
   | Protect Logs | Log Tamper Detection | Passed |
   | Maintain Availability | Load Test | Passed |

4. **Chapter Consistency Rule**
   - Chapter 1 = What will be achieved
   - Chapter 3 = How it will be tested
   - Chapter 4 = What the results were
   The same security themes appear consistently across all three chapters.

---

## II. Security Testing Documentation Format

Each test case documented using this structure:

| Field | Description |
|-------|-------------|
| Test Case ID | Unique identifier |
| Test Area | Security domain being tested |
| Threat Category | STRIDE mapping |
| Objective | Purpose of the test |
| Tool Used | Software or method used |
| Test Environment | Controlled setup used |
| Steps Performed | Actual procedure |
| Expected Result | Secure behavior expected |
| Actual Result | Observed outcome |
| KPI / Threshold | Success benchmark |
| Status | Passed / Failed |
| Risk Level | High / Medium / Low |
| Evidence | Screenshot / Log / Video Ref |
| Remediation Action | Fix applied or recommended |

---

## III. Sample Security Testing Results

### A. Authentication Lockout

| Field | Result |
|-------|--------|
| Test Case ID | AUTH-001 |
| Threat Category | Spoofing |
| Objective | Verify account lockout after repeated failed login attempts |
| Tool Used | Manual Testing / Browser |
| Steps Performed | Enter incorrect password repeatedly |
| Expected Result | Account locked after threshold |
| Actual Result | Account locked after 5 attempts |
| KPI | ≤ 5 failed attempts |
| Status | Passed |
| Evidence | Screenshot + Video Clip |

**Interpretation:** The system successfully enforced account lockout after five consecutive failed login attempts. This indicates that the authentication control can reduce exposure to brute-force and credential guessing attacks.

---

### B. SQL Injection Success Rate

| Field | Result |
|-------|--------|
| Test Case ID | VAL-001 |
| Threat Category | Tampering |
| Objective | Determine resistance to SQL injection |
| Tool Used | SQLMap / Burp Suite |
| Steps Performed | Submit malicious payloads in input fields |
| Expected Result | Requests blocked or sanitized |
| Actual Result | No injection succeeded |
| KPI | 0% success rate |
| Status | Passed |
| Evidence | Logs + Screenshot + Video Clip |

**Interpretation:** No successful SQL injection attempts were recorded during testing. This suggests that the system implemented effective input validation and secure query handling controls.

---

### C. Log Tamper Detection

| Field | Result |
|-------|--------|
| Test Case ID | LOG-001 |
| Threat Category | Repudiation |
| Objective | Verify whether unauthorized log modification is detected |
| Tool Used | Manual Test / Database Review |
| Steps Performed | Attempt log edit or delete action |
| Expected Result | Tampering blocked or detected |
| Actual Result | Modification attempt detected |
| KPI | 100% detection |
| Status | Passed |
| Evidence | Audit Trail + Screenshot |

**Interpretation:** The system detected simulated unauthorized modification attempts on audit records. This supports accountability and forensic traceability requirements.

---

### D. HTTPS Enforcement

| Field | Result |
|-------|--------|
| Test Case ID | DATA-001 |
| Threat Category | Information Disclosure |
| Objective | Verify encrypted communication |
| Tool Used | Browser Inspection / Network Monitor |
| Steps Performed | Access system using HTTP |
| Expected Result | Redirect to HTTPS |
| Actual Result | Redirect successful |
| KPI | 100% encrypted sessions |
| Status | Passed |
| Evidence | Browser Screenshot |

**Interpretation:** All tested connections were redirected to secure HTTPS sessions. This indicates that the system protects transmitted credentials and sensitive data against interception risks.

---

### E. Uptime Under Load

| Field | Result |
|-------|--------|
| Test Case ID | AVAIL-001 |
| Threat Category | Denial of Service |
| Objective | Evaluate system stability under increased usage |
| Tool Used | JMeter / Load Test Tool |
| Steps Performed | Simulate concurrent requests |
| Expected Result | System remains responsive |
| Actual Result | 96% uptime maintained |
| KPI | ≥ 95% uptime |
| Status | Passed |
| Evidence | Test Report + Graph |

**Interpretation:** The system maintained 96% uptime during controlled load simulation. This suggests acceptable availability and resilience under moderate stress conditions.

---

## IV. Research Guidelines for Security Testing

### 1. Each Test Must Be Properly Documented

**Minimum Required Documentation:**
- Test plan
- Test case sheet
- Tools used
- Steps performed
- Expected vs actual result
- KPI / threshold
- Screenshots
- Logs
- Remediation notes
- Final status

**Guideline:** If a result is written in Chapter 4, there must be supporting evidence in the appendix or project files.

---

### 2. Ethical Considerations Must Be Followed

**Required Conditions:**
- Test only the developed system owned by the researchers
- Use isolated or controlled environment
- Use test accounts / sample data only
- Avoid affecting production systems
- Avoid harming third-party networks or services
- Inform adviser or authorized supervisor if required

**Suggested Statement:**
> All security tests were conducted in a controlled environment using the researchers' own developed system with non-production data.

---

### 3. Tools Utilized and Minimum Requirements

| Test Area | Suggested Tools |
|-----------|----------------|
| Authentication | Browser, Manual Testing |
| SQL Injection | SQLMap, Burp Suite |
| Logging Review | Database Viewer, Audit Logs |
| HTTPS Check | Browser Dev Tools, Wireshark |
| Load Testing | Apache JMeter, Locust |

**Minimum Requirements:**
- Stable local or test environment
- Backup copy of database
- Test user accounts
- Logging enabled
- Browser with developer tools
- Permission to run the test within scope

---

### 4. Video Documentation for Final Defense

All security tests explicitly stated in the approved objectives must be documented through separate video simulations. Each required security test should have its own corresponding video evidence.

**Recommended Video Content:**
- Brief test objective
- Tool used
- Steps performed
- Actual execution
- Result shown
- Explanation of mitigation or control

**Recommended Video Coverage:**

| Objective / Test Area | Required Video |
|-----------------------|---------------|
| Authentication Lockout | Video 1 |
| SQL Injection Test | Video 2 |
| Unauthorized Record Modification Test | Video 3 |
| Log Tamper Detection | Video 4 |
| Activity Traceability Review | Video 5 |
| HTTPS Enforcement | Video 6 |
| Availability / Load Test | Video 7 |

**Minimum Content of Each Video:**
- Test title / objective
- Environment or module being tested
- Tool used (if applicable)
- Steps performed
- Actual execution
- Result observed
- Interpretation or conclusion

**Recommended Format:**
- Duration: 1 to 3 minutes per test
- Clear screen recording
- Readable text or zoomed interface
- Visible result or logs
- Optional voice explanation or captions

---

## Questionnaire-to-Test Alignment Summary

The two instruments (Post-Test Evaluation + Security Testing Evaluation) and the technical guidelines form a three-layer evidence system for Ch4:

| Layer | Instrument | Evidence Type |
|-------|-----------|--------------|
| ISO 25010 Quality | [[raw/articles/wims-bfp-post-test-evaluation-questionnaire-2026-05-04]] | Perception / user feedback |
| Security Controls Perception | Security Testing Evaluation Questionnaire (this page) | Expert perception / judgment |
| Technical Security Tests | Security Testing Guidelines (this page) | Objective pass/fail + metrics |

All three are linked from the [[raw/articles/wims-bfp-research-question-alignment-matrix-2026-05-04]] which maps each objective to expected Ch4 evidence.
