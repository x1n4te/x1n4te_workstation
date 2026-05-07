---
id: wims-bfp-ethics-revision-2026-04-11
type: source
created: 2026-04-11
updated: 2026-04-11
last_verified: 2026-04-11
review_after: 2026-07-11
stale_after: 2026-10-11
confidence: high
source_refs:
  - raw/software-dev/wims-bfp/thesis/03-09-ethical-legal.md
  - raw/software-dev/wims-bfp/thesis/03-09-01-data-migration-plans.md
  - raw/misc/IREC Form No. 01 Application Form for Ethical Review.pdf
  - raw/misc/Appendix A Human participation.pdf
  - raw/misc/Appendix H ALGORITHMIC AND AUTOMATED DECISION  IMPACT ASSESSMENT.pdf
  - raw/misc/Informed Consent Form Template V0 022026.docx.pdf
status: active
tags:
  - wims-bfp
  - thesis
  - ethics
  - ierc
  - section-3-9
  - ai-writing-revision
related:
  - sources/software-dev/wims-bfp-ch3d-testing-data
  - sources/software-dev/wims-bfp-ierc-appendices
  - concepts/signs-of-ai-writing
---

# WIMS-BFP Thesis Ethics Section (3.9) — Full Revision Log

**Date:** 2026-04-11
**Files modified:** 03-09-ethical-legal.md, 03-09-01-data-migration-plans.md
**Files created:** IRB-Submission-WIMS-BFP.md, IREC-Form-01-WIMS-BFP.md, wims-bfp-ierc-appendices.md

---

## What Changed

### 1. Section 3.9 Expansion (03-09-ethical-legal.md)

**Before:** ~47 lines. Flat section covering RA 10173, RA 10175, data sovereignty, RBAC, encryption, audit logs, disposal.

**After:** ~210 lines. Structured with sub-sections:

```
3.9   Ethical and Legal Considerations (intro — RA 10173, MOA, IERC, PHREB)
3.9.1   Regulatory Compliance Framework
  3.9.1.1   Data Privacy Act of 2012 (RA 10173) — lawful bases, 7 data subject rights
  3.9.1.2   Cybercrime Prevention Act (RA 10175) — 5 provisions mapped to mitigations
  3.9.1.3   NPC Circulars — framed as "designed to support," not "compliant with"
  3.9.1.4   Data Protection Impact Assessment — risk assessment, not formal DPIA
3.9.2   Ethical Safeguards for Human Participants
  3.9.2.1   Informed Consent Protocol — IERC FO-IREC-002 format
  3.9.2.2   Vulnerable Population Considerations — anti-coercion measures
  3.9.2.3   Data Sovereignty and Localization — local AI, no cross-border
  3.9.2.4   Algorithmic and Automated Decision Impact — XAI assessment (NEW)
3.9.3   Technical Data Protection Measures
  3.9.3.1   Encryption Standards — AES-256-GCM, TLS 1.3, NIST SP 800-57
  3.9.3.2   Access Control Enforcement — Keycloak RBAC, RLS, least privilege
  3.9.3.3   Audit and Non-Repudiation — append-only logs, SHA-256, Suricata
3.9.4   Data Retention and Disposal — lifecycle from test purge to certificate
3.9.5   Data Migration Plans — EVS pipeline (moved from old 3.9.1)
```

### 2. Data Migration Renumbering

- Old: 3.9.1 Data Migration Plans
- New: 3.9.5 Data Migration Plans
- Rationale: Old 3.9.1 conflicted with new Regulatory Compliance Framework. Migration is a lifecycle operation (migrate in → process → dispose out), fits after retention.

### 3. NPC Circulars Reframed

- Old: "The system complies with the following NPC Circulars" + claims of DPO registration, breach teams, 72-hour notification
- New: "As a thesis prototype, this project is not subject to NPC Circular compliance obligations. However, the system is designed to support compliance once deployed by the BFP"
- Rationale: NPC Circulars bind organizations with active data processing. A thesis prototype is not that. The system architecture supports compliance at deployment.

### 4. DPIA → Risk Assessment

- Old: "A formal DPIA was done per NPC Circular 20-01" + "DPO maintains the register"
- New: "A risk assessment was conducted during system design" + "formal DPIA registration is the BFP's responsibility upon deployment"
- Rationale: Same as above — thesis project, not an operational entity.

### 5. Algorithmic Impact Section Added (3.9.2.4)

New subsection covering the XAI module per IERC Appendix H (FO-IREC-010):
- Nature of Processing: Pattern analysis, classification. No autonomous decisions.
- Impact on Individuals: Advisory only. No academic/employment/reputation impact.
- Bias Risk: None identified. No demographic profiling. Human validation required.
- Human Oversight: All outputs flagged AI-generated. Admin must confirm.
- Transparency: Documented in architecture. Confidence indicators. Participants informed.

### 6. IERC Integration (IRB → IERC)

- Old: "Institutional Review Board (IRB)"
- New: "FEU Institute of Technology Institutional Research Ethics Committee (IERC)"
- Added: Form numbers (FO-IREC-001, 002, 003, 010), PHREB compliance note
- Updated: Consent protocol references FO-IREC-002 template, IERC contact (research@feutech.edu.ph)

### 7. AI Writing Remediation

Both documents rewritten using the Signs of AI Writing reference (wiki/concepts/signs-of-ai-writing.md) to eliminate:

| Pattern Killed | Example |
|---|---|
| Copulative avoidance | "serves as" → "is"; "functions as" → removed |
| AI vocabulary | "comprehensive," "rigorous," "systematic," "robust" → deleted |
| Rule of three | Tripled adjectives/phrases → cut to 1-2 |
| Significance puff | "demonstrates the research team's commitment" → deleted |
| Superficial -ing | "ensuring research data is restricted" → "restricting research data" |
| Promotional tone | "robust container isolation" → "container isolation" |
| Em dashes | Formulaic parentheticals → reduced to functional only |
| Vague attributions | "rigorously reviewed and approved" → "reviewed and approved" |

### 8. Bullet Points → Paragraphs (3.9.3, 3.9.4)

3.9.3.1, 3.9.3.2, 3.9.3.3, and 3.9.4 converted from bullet lists to flowing paragraph prose. Technical details preserved, just embedded in sentences instead of listed.

---

## Files Created

| File | Purpose |
|---|---|
| ethics/IRB-Submission-WIMS-BFP.md | Standalone IRB protocol — consent forms, risk-benefit analysis, data protection plan, breach response, compliance checklist. Adapted to IERC terminology. |
| ethics/IREC-Form-01-WIMS-BFP.md | Filled IREC Form No. 01 — Sections A-F with WIMS-BFP specifics. Executive summary, screening checklist with justifications, document checklist, declaration template. |
| wiki/.../wims-bfp-ierc-appendices.md | Key details from IERC Appendix A (Human Participants), Appendix H (Algorithmic Impact), and Consent Form template (FO-IREC-002). Field-by-field mapping to WIMS-BFP. |

---

## Decision Log

1. **NPC Circulars: thesis prototype exemption.** User correctly noted NPC Circulars don't bind a thesis project. Reframed as "designed to support" compliance at BFP deployment.

2. **IERC not IRB.** The institutional body is the FEU-TECH Institutional Research Ethics Committee (IERC), not a generic IRB. Updated all terminology and form references.

3. **Appendix H applies.** The XAI module (Qwen2.5-3B) triggers the algorithmic/automated decision-making screening question. New 3.9.2.4 covers this.

4. **Data migration renumbered to 3.9.5.** Old 3.9.1 conflicted with new Regulatory Compliance Framework structure.

---

## Cross-References

- [[sources/software-dev/wims-bfp-ch3d-testing-data]] — original ethics summary (now outdated in parts)
- [[sources/software-dev/wims-bfp-ierc-appendices]] — IERC form field details
- [[concepts/signs-of-ai-writing]] — detection patterns used for rewriting
