---
id: wims-bfp-ierc-appendices-001
type: source
created: 2026-04-11
updated: 2026-04-11
last_verified: 2026-04-11
review_after: 2026-07-11
stale_after: 2026-10-11
confidence: high
source_refs:
  - raw/misc/Appendix A Human participation.pdf
  - raw/misc/Appendix H ALGORITHMIC AND AUTOMATED DECISION  IMPACT ASSESSMENT.pdf
  - raw/misc/Informed Consent Form Template V0 022026.docx.pdf
  - raw/misc/IREC Form No. 01 Application Form for Ethical Review.pdf
status: active
tags:
  - wims-bfp
  - thesis
  - ierc
  - ethics
  - appendix-a
  - appendix-h
related:
  - sources/software-dev/wims-bfp-ch3d-testing-data
---

# WIMS-BFP IERC Appendix Key Details

**Source:** raw/misc/ (4 IERC form PDFs)
**Institution:** FEU Institute of Technology — Institutional Research Ethics Committee (IERC)

---

## IERC Form Reference Numbers

| Form | Title | Version | Effectivity |
|---|---|---|---|
| FO-IREC-001 | Application Form for Research Ethics Review | 1.0 | Jan 1, 2026 |
| FO-IREC-002 | Informed Consent Form Template | 1 | Feb 23, 2026 |
| FO-IREC-003 | Appendix A — Human Participants | 1.0 | Feb 23, 2026 |
| FO-IREC-010 | Appendix H — Algorithmic and Automated Decision Impact Assessment | 1.0 | Feb 23, 2026 |

---

## Appendix A — Human Participants (FO-IREC-003)

### Key Fields to Fill

**I. Description of Participants**
- Type: BFP operational personnel (Encoders, Validators, Analysts, Administrators) and IT professionals
- Estimated count: 14-16 (11 operational + 3-5 IT professionals); research team (4) separate
- Age group: ☑ 18 years old and above only
- Recruitment: BFP management coordination; voluntary sign-up

**II. Nature of Participation**
- ☑ Survey or questionnaire (SUS + XAI Likert)
- ☑ Usability testing (system, app, website, prototype)
- ☑ Observation of user interaction (task completion metrics)

**III. Informed Consent Process**
- ☑ Written consent form
- Participants informed of: purpose, what participation involves, voluntary nature, right to withdraw, data use and protection
- ☑ Sample informed consent form attached (FO-IREC-002 format)

**IV. Risks, Discomforts, and Safeguards**
- Risk level: ☑ Minimal risk (no greater than everyday activities)
- Risks: Time commitment, mild survey discomfort
- Safeguards: Voluntary participation, ability to skip questions, anonymity, no employment impact

**V. Privacy, Confidentiality, and Data Protection**
- Data types: ☑ System/app interaction data, ☑ Survey responses, ☑ Anonymous data only
- Confidentiality: ☑ Anonymization of data, ☑ Restricted access, ☑ Password-protected storage, ☑ Encrypted storage
- Access: ☑ Principal Investigator only, ☑ Adviser
- Raw data shared outside team: ☑ No
- Storage: Encrypted local/PostgreSQL; Retention: 30 days post-evaluation for individual responses; Disposal: Cryptographic erasure per ISO/IEC 27037
- De-identification: ☑ No direct identifiers collected; ☑ Final dataset: Fully anonymous

**VII. Multimedia/Digital** — ☑ Not applicable (no participant images/audio/video)

**IX. Ethical Assurance** — Signatures from all proponents

---

## Appendix H — Algorithmic Impact (FO-IREC-010)

### Key Fields to Fill

**I. Nature of Algorithmic Processing**
- ☑ Yes — uses AI/ML
- Performs: ☑ Pattern analysis, ☑ Classification or categorization
- Does NOT perform: ranking, prediction, recommendation, behavioral inference

**II. Impact on Individuals**
- ☑ None — output is purely technical or experimental
- XAI narratives are advisory only; no real-world decision impact
- NOT deployed in real-world environment: ☑ No (simulation or laboratory testing only)

**III. Risk of Bias, Profiling, or Misclassification**
- ☑ None identified
- System does not profile individuals or make demographic inferences
- Mitigation: Human validation required before any action; XAI outputs flagged as AI-generated

**IV. Human Oversight and Safeguards**
- Human review before decisions: ☑ Yes
- Users informed of algorithmic processing: ☑ Yes
- Explainable outputs: ☑ Yes (XAI is the core feature — human-readable narratives)

**V. Ethical Assurance** — Signatures from all proponents

---

## Informed Consent Form (FO-IREC-002)

### Template Structure (for final participant-facing version)

1. Title of project + proponent info
2. Invitation to participate + voluntary statement
3. Purpose of the study (non-technical language)
4. Participant selection (why they were chosen)
5. Nature of participation (what they do, topic, duration, recordings if any)
6. Duration and location
7. Risks and discomforts (minimal risk)
8. Benefits (early exposure to XAI tools, input on system design)
9. Voluntary participation and withdrawal
10. Confidentiality and data protection
11. Contact information (PI, adviser, IERC: research@feutech.edu.ph)
12. Certificate of consent (signature lines)
13. Impartial witness statement (if needed)
14. Statement of researcher

### Notes
- Final version must be clear sentences, not template prompts
- Checklist items and bracketed instructions must NOT appear in signed version
- Language appropriate to participant understanding level

---

## IREC Screening Checklist (Section D) — Which Appendices Apply

| Question | Answer | Appendix |
|---|---|---|
| Human participants? | YES | Appendix A (FO-IREC-003) |
| Action research? | NO | — |
| Online/internet data? | NO | — |
| Community-based? | NO | — |
| Documents/media needing permission? | NO (MOA covers) | — |
| Animals? | NO | — |
| Toxic/hazardous substances? | NO | — |
| Physical hazards? | NO | — |
| Creative/multimedia/game-based? | NO | — |
| AI/ML/algorithmic decision-making? | YES | Appendix H (FO-IREC-010) |

---

## Required Documents Checklist (Section E)

| Document | Status |
|---|---|
| Research Proposal/Thesis Approved Intro + Methodology | ☐ |
| Informed Consent Form(s) | ☐ |
| Curriculum Vitae of Proponents (faculty only) | ☐ |
| Appendix A — Human Participants | ☐ |
| Appendix H — Algorithmic Impact | ☐ |

---

## Cross-References

- [[sources/software-dev/wims-bfp-ch3d-testing-data]] — Testing, evaluation, data gathering + ethics
- [[sources/software-dev/wims-bfp-ch3a-research-design]] — Research design
- [[sources/software-dev/wims-bfp-ch3b-architecture]] — System architecture (XAI module)
