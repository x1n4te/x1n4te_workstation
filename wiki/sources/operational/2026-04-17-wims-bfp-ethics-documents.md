---
id: 2026-04-17-wims-bfp-ethics-documents
type: source
created: 2026-04-17
updated: 2026-04-17
last_verified: 2026-04-17
review_after: 2026-05-17
stale_after: 2026-07-17
confidence: high
source_refs:
  - /home/xynate/Documents/WIMS-BFP/ETHICS/
status: active
tags:
  - wims-bfp
  - thesis
  - operational
related:
  - mocs/wims-bfp
  - entities/hermes-agent
---

# WIMS-BFP IREC Ethics Documents — Full Inventory

## Document Structure

```
ETHICS/
├── IREC Form No. 01 Application Form for Ethical Review.md   ← IREC-Form01.md
├── Appendix A/APPENDIX A.md                                  ← Human Participants
├── Appendix A/APPENDIX A.pdf
├── Appendix D/APPENDIX D.md                                  ← Community-Based Research
├── Appendix H/appendix h.md                                  ← Algorithmic Impact Assessment
├── Informed Consent Forms/informed consent form i.md         ← Consent Form I (BFP Personnel)
├── Informed Consent Forms/informed consent form ii.md        ← Consent Form II
├── Informed Consent Form.md                                  ← Standalone consent (duplicate?)
└── Informed-Consent-Form-Template-V0-022026.pdf
```

**Total documents:** 9 files (6 markdown, 1 PDF form, 1 PDF appendix, 1 standalone consent)

---

## IREC Form No. 01 (Main Application)

**Two versions detected:**
- `informed consent form i.md` — contains IREC form frontmatter + Ethics Section 3.9 + SDG with SDG 16 + Action Research ✅
- `IREC Form No. 01 Application Form for Ethical Review.md` — contains IREC form frontmatter + Ethics Section 3.9 + SDG without SDG 16 + Action Research ❌

**Version discrepancies (CRITICAL):**

| Field | Form i (Corrected) | Form 01 (Older) | Status |
|-------|-------------------|-----------------|--------|
| Title (B.) | "Secured Web Offline-First...Explainable AI for Threat Interpretability" | "Secure Web...AI-Assisted Threat Detection for Cybersecurity-Specific Forensics-Driven Analysis" | MISMATCH |
| Prototype/Experimental | ✅ | ❌ (not checked) | MISMATCH |
| System Software | ✅ | ✅ | OK |
| Action Research | ✅ | ✅ | OK |
| SDG paragraph | Includes SDG 16 (Peace, Justice, Strong Institutions) | Only SDG 9 | MISMATCH |

**Team members (Section F — Declaration):**

| Name | Email | FEU ID | Contact | Status |
|------|-------|--------|---------|--------|
| Cabrales, Nathan Josua C. | nathancabrales10@gmail.com | 202312375 | 09765005009 | Complete |
| Camama, Earl Justin P. | camamaearl24@gmail.com | **MISSING** | **MISSING** | INCOMPLETE |
| Dela Cruz, Red Gabrielle A. | redgab0406@gmail.com | 202312784 | 09198862333 | Complete |
| Tendero, Guinevere T. | gwntendero@gmail.com | 202311695 | 09682728735 | Complete |

**Camama details missing in IREC Form 01 but present in Appendix A** (FEUTECH ID: 202311034, Contact: 09156877216). Needs reconciliation.

---

## Appendix A — Human Participants

- **Participants:** BFP FSOD Operational Personnel (11) + IT Professionals (3-5) = 14-16 total
- **Activities:** Usability testing, surveys, observation
- **Consent:** Written consent form (sample attached)
- **Risk level:** Minimal
- **Data types:** Survey responses, system interaction data, anonymous data
- **Storage:** Encrypted local/PostgreSQL, 30-day retention post-evaluation
- **Disposal:** Cryptographic erasure per ISO/IEC 27037
- **Faculty Adviser:** Abricam S. Tinga

---

## Appendix D — Community-Based Research

- **Community:** BFP Fire Safety and Operational Division, Directorate of Operations
- **Role:** Source of info, design basis, test participants, end users, deployment target
- **Engagement:** Short-term (1-week prototype testing, June 2026)
- **Permission:** Written letter of cooperation
- **Risks:** Additional time/workload for members, technology dependence
- **Mitigation:** Testing during free time, voluntary participation, MOA defines scope
- **Compensation:** Non-monetary (lunch/merienda, refreshments)
- **Deployment:** Scope explained, managed expectations, exit/handover plan disclosed

---

## Appendix H — Algorithmic Impact Assessment

- **AI used:** Yes — Qwen2.5-3B SLM for threat log analysis
- **Function:** Recommendation generation (not classification/prediction)
- **Impact:** Access to services, reputation (threat interpretation affects operations)
- **Deployment:** Real-world environment (not simulation only)
- **Bias mitigation:** Human-in-the-loop, advisory-only outputs, no demographic data used
- **Transparency:** Explainable outputs, users informed of AI involvement
- **Safeguards:** Administrator review, rule tuning, continuous false positive monitoring

---

## Informed Consent Forms

**Form I** — BFP Personnel and End-Users
- For UAT participants at BFP National Headquarters
- Duration: 30-45 minutes single session
- Tasks: Navigate prototype with test account, encode mock incident, upload sample AFOR, view analytics dashboard
- Risk: Minimal (time commitment only)
- Data: No audio/video/screen recording, survey responses only
- Contact: nccabrales@fit.edu.ph (PI), abtinga@feutech.edu.ph (Adviser)

**Form II** — (Not fully read yet, but appears to be a second consent form variant)

---

## Discrepancies from Previous Audit (2026-04-16)

From the prior wiki entry `2026-04-16-wims-bfp-irec-form-audit`:

1. **Title mismatch** — IREC Form 01 uses old title ("AI-Assisted Threat Detection for Cybersecurity-Specific Forensics-Driven Analysis") while corrected version uses new title ("Explainable AI for Threat Interpretability")
2. **Action Research** — Form 01 has it checked ✅ but Appendix D is included despite the "No" checkbox in Form 01's Section D Checklist (inconsistent state in older version)
3. **Internet data** — Form 01 marked "No" but system uses cloud backend (Supabase). This may be acceptable if no internet-based participant data collection, but should be reviewed
4. **Missing attachments** — Form 01 checklist has some items unchecked (Informed Consent, Appendix A, Appendix D, Appendix H, Letter of Agreement)
5. **Camama's FEUTECH ID and contact** — missing in IREC Form 01 Section F, present in Appendix A and Appendix H

**Recommendation:** Use the corrected version from `informed consent form i.md` as the canonical IREC Form 01. Reconcile Camama's details. Ensure all appendix checkmarks match actual attached documents.

---

## Cross-References
- See [[mocs/wims-bfp]] for overall WIMS-BFP project context
- See [[analyses/wims-bfp-thesis-codebase-gaps]] for codebase vs thesis discrepancies
- Ethics review complements the codebase security work in [[concepts/postgresql-security-wims-bfp]] and [[concepts/keycloak-fastapi-security-wims-bfp]]
