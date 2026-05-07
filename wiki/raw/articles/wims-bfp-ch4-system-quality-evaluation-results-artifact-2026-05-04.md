# WIMS-BFP — Ch4 System Evaluation Results

> **Status:** Thesis-ready artifact for Chapter 4
> **Chapter:** 4 — Results and Discussion
> **Section:** Results of System Quality Evaluation
> **Based on:** `wims-bfp-post-test-evaluation-questionnaire-2026-05-04`

---

## 4.X Results of System Quality Evaluation

### 4.X.1 System Implementation Overview

*The system was implemented as a three-tier architecture: a Next.js PWA frontend deployed on Vercel, a FastAPI backend orchestrating PostgreSQL+PostGIS and Redis+Celery services, Keycloak for identity and access management with MFA enforcement, Suricata for network intrusion detection, and Qwen2.5-3B as the local SLM for explainable AI alert generation. The system was developed across thirteen functional modules aligned with the approved FRS. Deployment was conducted in a controlled environment using Docker Compose with HTTPS enforcement, RLS policies enforced at the database layer, and AES-256-GCM encryption for sensitive PII fields.*

### 4.X.2 Functional Suitability Results

*Output from Section 3.X (Functional Requirements)*

#### 4.X.2.1 Description

Functional suitability was evaluated based on the extent to which the system provides functions that meet stated and implied needs. Five evaluation items were prepared covering the core incident monitoring and reporting workflow.

#### 4.X.2.2 Findings

**Table 4.X** Functional Suitability Evaluation Results

| No. | Evaluation Statement | WM | VI |
|-----|---------------------|----|----|
| 1 | The system provides the functions needed for incident monitoring and reporting. | X.XX | (VI) |
| 2 | The system features operate correctly during use. | X.XX | (VI) |
| 3 | The generated outputs are relevant to operational needs. | X.XX | (VI) |
| 4 | The system supports the intended tasks efficiently. | X.XX | (VI) |
| 5 | The system meets the expected requirements of its intended users. | X.XX | (VI) |

**Legend:** WM = Weighted Mean; VI = Verbal Interpretation using scale: 4.21–5.00 = Very Satisfactory (VS); 3.41–4.20 = Satisfactory (S); 2.61–3.40 = Neutral (N); 1.81–2.60 = Unsatisfactory (U); 1.00–1.80 = Poor (P)

**Composite Mean:** X.XX — **Verbal Interpretation**

#### 4.X.2.3 Interpretation

*The system demonstrates [high/provisional] functional suitability. All five items scored above the 3.41 threshold, indicating that the implemented modules fulfill the core incident monitoring and reporting requirements defined in the functional requirements specification. Item X (lowest-scoring) suggests an area for improvement in [specific module].*

---

### 4.X.3 Performance Efficiency Results

*Output from Section 3.X (Non-Functional Requirements + KPIs)*

#### 4.X.3.1 Description

Performance efficiency was measured in terms of response time, processing speed, and resource usage under normal and elevated conditions.

#### 4.X.3.2 Findings

**Table 4.X** Performance Efficiency Evaluation Results

| No. | Evaluation Statement | WM | VI |
|-----|---------------------|----|----|
| 6 | The system responds promptly when commands or requests are submitted. | X.XX | (VI) |
| 7 | The system processes records and outputs without unnecessary delay. | X.XX | (VI) |
| 8 | AI-generated outputs are produced within an acceptable time. | X.XX | (VI) |
| 9 | The system performs efficiently without slowing down the device or browser. | X.XX | (VI) |
| 10 | The system maintains stable performance during repeated or simultaneous use. | X.XX | (VI) |

**Composite Mean:** X.XX — **Verbal Interpretation**

#### 4.X.3.3 Interpretation

*[To be populated with actual survey results. Expected interpretation: AI inference time averaged X.X seconds per alert; page load time under X.Xs at P95; system maintained responsiveness during simulated concurrent access.]*

---

### 4.X.4 Reliability Results

*From uptime/stability tests*

#### 4.X.4.1 Description

Reliability was assessed through continuous operation monitoring and user-reported stability during the evaluation period.

#### 4.X.4.2 Findings

**Table 4.X** Reliability Evaluation Results

| No. | Evaluation Statement | WM | VI |
|-----|---------------------|----|----|
| 11 | The system remains stable during continuous use. | X.XX | (VI) |
| 12 | The system recovers properly after interruptions or refresh. | X.XX | (VI) |
| 13 | The system maintains access to important functions when connectivity is unstable. | X.XX | (VI) |
| 14 | Data entered into the system is retained correctly during operation. | X.XX | (VI) |
| 15 | The system performs consistently during normal use. | X.XX | (VI) |

**Composite Mean:** X.XX — **Verbal Interpretation**

#### 4.X.4.3 Interpretation

*[To be populated. Expected: offline PWA capability enabled continued data entry during connectivity loss; sync occurred automatically upon reconnection without data loss.]*

---

### 4.X.5 Usability Results

*From Survey + XAI evaluation results*

#### 4.X.5.1 Description

Usability was measured through interface clarity, navigation efficiency, and learnability assessments with representative users.

#### 4.X.5.2 Findings

**Table 4.X** Usability Evaluation Results

| No. | Evaluation Statement | WM | VI |
|-----|---------------------|----|----|
| 16 | The system interface is clear and easy to understand. | X.XX | (VI) |
| 17 | Navigation between system features is easy to perform. | X.XX | (VI) |
| 18 | Instructions, labels, and menus are understandable. | X.XX | (VI) |
| 19 | The system is easy to learn for first-time users. | X.XX | (VI) |
| 20 | Overall, the system is user-friendly. | X.XX | (VI) |

**Composite Mean:** X.XX — **Verbal Interpretation**

#### 4.X.5.3 Interpretation

*[To be populated. Expected: dashboard rated X.XX; sidebar navigation efficiency noted; AI output clarity contributed to usability scores.]*

---

### 4.X.6 Explainability (AI Outputs) Results

*From dedicated XAI evaluation items*

#### 4.X.6.1 Description

Explainability was assessed by evaluating whether AI-generated outputs are understandable, relevant, and actionable for decision support.

#### 4.X.6.2 Findings

**Table 4.X** Explainability Evaluation Results

| No. | Evaluation Statement | WM | VI |
|-----|---------------------|----|----|
| 21 | The AI-generated results are understandable. | X.XX | (VI) |
| 22 | The explanations provided by the system are relevant to the result. | X.XX | (VI) |
| 23 | The AI outputs help support decision-making. | X.XX | (VI) |
| 24 | I can understand why the system produced a specific result. | X.XX | (VI) |
| 25 | The AI recommendations are presented clearly. | X.XX | (VI) |

**Composite Mean:** X.XX — **Verbal Interpretation**

#### 4.X.6.3 Interpretation

*[To be populated. Expected: XAI pipeline via Qwen2.5-3B generates natural language forensic narratives per Suricata alert; mean understandability rating X.XX; "why" attribution supported decision confidence.]*

---

### 4.X.7 System Quality Evaluation Summary

**Table 4.X** Summary of System Quality Evaluation Results

| Quality Characteristic | Composite Mean | Verbal Interpretation |
|----------------------|----------------|-----------------------|
| Functional Suitability | X.XX | (VI) |
| Performance Efficiency | X.XX | (VI) |
| Reliability | X.XX | (VI) |
| Usability | X.XX | (VI) |
| Explainability (AI Outputs) | X.XX | (VI) |
| **Overall System Quality** | **X.XX** | **(VI)** |

#### 4.X.7.1 Interpretation

*The developed system achieved an overall composite mean of X.XX, interpreted as [Verbal Interpretation], across all five ISO/IEC 25010 quality characteristics. This indicates that the system meets the defined quality requirements and is suitable for operational deployment within the Bureau of Fire Protection. The highest-rated characteristic was [X] at X.XX, while [X] received the lowest score at X.XX, suggesting targeted improvements in [specific area]. These results are consistent with the functional and non-functional requirements established in Chapter 3.*

---

## Statistical Treatment Note

**Weighted Mean Formula:**
```
WM = (Σfx) / N
Where:
  f = frequency of responses per rating
  x = scale value (1–5)
  N = total number of responses
```

**Scale Interpretation:**

| Mean Range | Interpretation |
|------------|----------------|
| 4.21 – 5.00 | Very Satisfactory |
| 3.41 – 4.20 | Satisfactory |
| 2.61 – 3.40 | Neutral |
| 1.81 – 2.60 | Unsatisfactory |
| 1.00 – 1.80 | Poor |

**Reliability Test:**
> Internal consistency of the instrument was assessed using Cronbach's Alpha. The computed alpha value of X.XX [exceeds/does not exceed] the recommended threshold of 0.70, indicating [acceptable/excellent/good/internal consistency concerns].

---

## Data Gathering Procedure Reference

| Parameter | Value |
|-----------|-------|
| Instrument | Post-Test Evaluation Questionnaire (30 items) |
| Respondents | N = XX [BFP personnel / IT professionals / faculty / students] |
| Sampling Method | Purposive sampling based on technical knowledge and operational relevance |
| Venue / Mode | [Physical / Online / Blended] |
| Date Administered | [Date] |
| Statistical Tool | Weighted Mean, Frequency, Percentage |
