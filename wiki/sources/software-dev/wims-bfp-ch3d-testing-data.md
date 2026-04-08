---
id: wims-bfp-ch3d-testing-data-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-07-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - raw/misc/03-07-01-testing-methodologies.md
  - raw/misc/03-07-02-evaluation-criteria.md
  - raw/misc/03-07-03-statistical-treatment.md
  - raw/misc/03-07-testing-evaluation.md
  - raw/misc/03-08-01-data-sources.md
  - raw/misc/03-08-02-participants-study.md
  - raw/misc/03-08-03-data-gathering-instruments.md
  - raw/misc/03-08-04-data-collection-techniques.md
  - raw/misc/03-08-05-tools-data-gathering.md
  - raw/misc/03-08-data-gathering.md
  - raw/misc/03-09-01-data-migration-plans.md
  - raw/misc/03-09-ethical-legal.md
  - raw/misc/03-methodology.md
status: active
tags:
  - wims-bfp
  - thesis
  - chapter-3
  - testing
  - evaluation
  - data-gathering
  - ethics
related:
  - sources/software-dev/wims-bfp-ch3a-research-design
  - sources/software-dev/wims-bfp-ch3b-architecture
---

# WIMS-BFP Chapter 3d: Testing, Evaluation, Data Gathering + Ethics

**Source:** raw/misc/ (13 files)
**Chapter:** 3d — Testing Methodologies, Evaluation Criteria, Data Gathering, Ethical/Legal

---

## Testing Methodologies

### Functional Testing
- Validates each module against functional requirements
- Unit tests for cryptographic functions, API endpoints, spatial queries
- Integration tests for end-to-end workflows (civilian report → triage → verified)

### Performance Testing
| Test | Tool | Metric |
|---|---|---|
| Concurrent user load | Locust | Response time under N concurrent users |
| Heatmap rendering | Browser profiling | Render time for PostGIS spatial queries |
| AI inference latency | Custom profiler | Mean inference latency (target: <5s) |
| Offline sync | Manual disconnect/reconnect | Synchronization Success Rate (SSR) |

### Security Testing
| Test | Method | Standard |
|---|---|---|
| Web vulnerability | OWASP ZAP automated scan | OWASP ASVS Level 2 |
| SQL injection | sqlmap targeted testing | STRIDE: Tampering |
| Penetration testing | Manual + automated | OWASP Top 10 coverage |
| Access control | Role boundary testing | RBAC enforcement verification |
| Cryptographic validation | Hash chain verification | SHA-256 integrity checks |

### Usability Testing
- XAI Mean Opinion Score (MOS) — target >= 4.0/5.0
- Survey instruments for non-technical BFP personnel
- Task completion rate for offline encoding workflows

---

## Evaluation Criteria (ISO/IEC 25010)

| Quality | Sub-characteristic | Measurement |
|---|---|---|
| Functional Suitability | Completeness, Correctness | Feature coverage vs requirements |
| Performance Efficiency | Time behavior, Resource utilization | Latency, throughput, CPU/memory |
| Reliability | Availability, Fault tolerance | SSR, error recovery rate |
| Usability | Learnability, Operability | MOS, task completion time |
| Security | Confidentiality, Integrity, Non-repudiation | Encryption verification, audit log integrity |

---

## Statistical Treatment

| Analysis | Purpose | Application |
|---|---|---|
| Descriptive Statistics | Summarize evaluation scores | Mean, median, SD for MOS |
| F1-Score | Detection accuracy | Suricata IDS precision/recall |
| Confidence Intervals | Reliability of measurements | 95% CI for performance metrics |
| Comparative Analysis | WIMS-BFP vs existing systems | Feature-by-feature comparison |
| Load Testing Curves | Performance under stress | Response time vs concurrent users |

---

## Data Sources

| Source | Type | Purpose |
|---|---|---|
| Suricata EVE JSON logs | Primary | Real-time network traffic alerts |
| Simulated civilian reports | Synthetic | Load testing, triage workflow validation |
| BFP operational templates | Secondary | Realistic incident data structure |
| OWASP test payloads | Standard | Security vulnerability testing |
| XAI narrative outputs | Generated | Usability evaluation (MOS scoring) |

---

## Participants

| Role | Count | Purpose |
|---|---|---|
| BFP IT Personnel | N | Security testing + system evaluation |
| Regional Encoders (simulated) | N | Offline-first workflow testing |
| National Validators (simulated) | N | Triage workflow testing |
| Non-technical evaluators | N | XAI MOS scoring |
| Security testers | N | Penetration testing |

*No live citizen data used — RA 10173 compliance.*

---

## Data Gathering

### Instruments
- Standardized survey questionnaires (Likert scale for MOS)
- Automated test result logging
- Performance monitoring dashboards
- Security scan reports (OWASP ZAP, sqlmap)

### Techniques
- Simulation-based testing (offline disconnect/reconnect)
- Load testing (Locust concurrent user simulation)
- Controlled adversarial simulation (OWASP ASVS L2)
- Expert evaluation (security testers)

---

## Data Migration Plans

| Phase | Source | Target | Method |
|---|---|---|---|
| Initial Load | BFP-AIMS reference data | WIMS-BFP PostgreSQL | Structured CSV import |
| Regional Sync | Offline IndexedDB bundles | Central DB | AES-256-GCM encrypted sync |
| Ongoing | Continuous input | Incremental append | API-based ingestion |

---

## Ethical and Legal Compliance

### RA 10173 (Data Privacy Act)
- No live citizen data during testing
- Synthetic datasets only for evaluation
- Data minimization enforced via RLS
- DPIA and ROPA documentation prepared

### IRB Considerations
- Human participants limited to BFP personnel evaluating system usability
- No personal data collected from evaluators
- Informed consent for survey participation

### Chain of Custody
- All test data cryptographically hashed
- Audit logs for every data access during testing
- Tamper-evident records for forensic validity

### Data Retention
- Test data purged after evaluation
- Only aggregate statistical results retained
- No PII in final thesis documentation

---

## Cross-References

- [[sources/software-dev/wims-bfp-ch3a-research-design]] — Research design
- [[sources/software-dev/wims-bfp-ch3b-architecture]] — System architecture
- [[sources/software-dev/wims-bfp-ch1-introduction]] — Scope and limitations
