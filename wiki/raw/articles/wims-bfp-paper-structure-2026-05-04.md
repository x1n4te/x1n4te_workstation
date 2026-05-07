# WIMS-BFP — Full Paper Structure

> **Source:** User-provided thesis paper outline
> **Captured:** 2026-05-04
> **Type:** Structural reference

---

## A. Preliminaries

1. Approval and Acceptance Sheet
2. Acknowledgment
3. Table of Contents
4. List of Tables
5. List of Figures
6. List of Abbreviations
7. Abstract

---

## B. Body

### Chapter 1 | Introduction

- Purpose and Description
- Project Context
  - Ishikawa Diagram — identifies root causes of the problem
  - STRIDE — identifies threats arising from those causes
    - STRIDE identifies what can go wrong
- Objectives of the Study
  - General Objective
  - Specific Objectives
    - Developmental
    - Cybersecurity Components
    - Cybersecurity Compliance
    - Security Testing
    - System Evaluation
- Scope and Limitations
- Significance of the Study
- Conceptual Framework
  - Cybersecurity Principles
    - e.g. CIA Triad — defines what must be protected
- Definition of Terms

---

### Chapter 2 | Review of Related Literature and Studies

- Related Literature
- Related Studies
- Synthesis

---

### Chapter 3 | Methodology

- Research Design
- Requirements Analysis
  - Functional Requirements
  - Non-Functional Requirements
  - Security Requirements
    - Define what the system must enforce
    - Translate concepts into clear, testable requirements
    - What must the system do?
- Feasibility of the Study
  - Technical Feasibility
  - Operational Feasibility
  - Economic Feasibility
  - Schedule Feasibility
  - Security Feasibility
  - Legal and Ethical Feasibility
- Project Development Model
- Secure System Architecture and Design
  - Architecture Overview
  - Context Diagram
  - Data Flow Diagram
  - Use Case Diagram
  - Entity Relationship Diagram
  - Activity Diagram (Optional)
  - Sequence Diagram (Optional)
  - Network/Deployment Diagram
    - Docker/Container/Serverless/Intranet
- Cybersecurity Measures
  - Explain how protection is applied
- Security Practices
  - Describe categories of protection (what is used and why)
  - What type of protection is used?
- Application of Cybersecurity Measures
  - Explain how practices are applied within the system context
  - Where does security appear in the system?
- Tools and Technologies
  - Development Tools
  - Security Testing Tools
- Testing and Evaluation
  - Testing Methodologies
  - System Testing (FURPS/ISO)
  - Security Testing and Vulnerability Assessment
  - Evaluation Criteria
    - FURPS/ISO Metrics
    - Security Metrics
- Statistical Treatment of Data
  - Survey Statistics
  - Security Quantitative Metrics
- Data Gathering Procedure
  - Data Source
  - Participants of the Study
  - Data Gathering Instruments
  - Data Collection Techniques
  - Tools Used for Data Gathering
- Ethical and Legal Considerations

---

### Chapter 4 | Results and Discussion

- System Implementation Overview
  - Output of 3.3 and 3.4
- Results of System Quality Evaluation
  - Output of 3.7.1 + 3.7.2 + 3.7.3
  - Functional Suitability Results
    - Output from Functionality Requirements
  - Performance Efficiency Results
    - Output from Non-Functionality Requirements + KPIs
  - Reliability Results
    - From uptime/stability tests
  - Usability Results
    - From Survey + XAI evaluation results
- Results of Security Testing and Vulnerability Assessment
  - Output of 3.2.3 + 3.5 + 3.7.1, with pass/fail, metrics, and remediation
  - Spoofing Results
    - Table 1 – Security Testing Results
      - Technical evidence, shows actual control effectiveness
    - Table 2 – Security Evaluation Survey
      - Human evaluation, shows expert acceptance and readiness
  - Tampering Results
    - Table 1 – Security Testing
    - Table 2 – Security Evaluation Survey
  - Repudiation Results
    - Table 1 – Security Testing
    - Table 2 – Security Evaluation Survey
  - Information Disclosure Results
  - DoS Results
- Discussion of Findings
  - Interpretation of Results
    - Meaning of findings + compare with literature
  - Implication of Findings
    - Why results matter to users, agencies, and research

---

### Chapter 5 | Conclusion

- Summary of Key Findings
  - Condensed major results
- Conclusions and Implications
  - Judgment based on objectives achieved

---

### Chapter 6 | Recommendations

- System Enhancements
- Security Improvements
- Future Research
- Deployment Advice

---

## C. Bibliography

---

## D. Appendices

- Communication Letter
- Transcript of Interview
- Panel Comments
- Signed FRS
- Expert Validation
- System Functionality Evaluation Questionnaire
- Security Testing and Assessment Evaluation
- Security Test Case
- Ethics Clearance Certification
- Security Testing Video Review and Validation Form
- Curriculum Vitae

---

## Structural Mapping Notes

| Chapter | Key Inputs | Key Outputs |
|---------|-----------|-------------|
| Ch1 Intro | Ishikawa, STRIDE, CIA Triad | Problem context, objectives, scope |
| Ch2 RRL | Literature, studies | Synthesis gap |
| Ch3 Methodology | Ch1 + Ch2 inputs | Architecture, security requirements, testing plan |
| Ch4 Results | Ch3 outputs | Pass/fail tables, FURPS metrics, STRIDE test results |
| Ch5 Conclusion | Ch4 results | Conclusions against objectives |
| Ch6 Recommendations | Ch4 gaps | Enhancements, future work |
