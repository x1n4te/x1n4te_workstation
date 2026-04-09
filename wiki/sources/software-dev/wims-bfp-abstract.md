---
id: wims-bfp-abstract-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-07-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - raw/misc/abstract.md
status: active
tags:
  - wims-bfp
  - thesis
  - abstract
related:
  - sources/software-dev/wims-bfp-ch1-introduction
  - sources/software-dev/wims-bfp-ch2-rrl
---

# WIMS-BFP Abstract

**Thesis:** "WIMS-BFP: A Secured Web Offline-First Incident Monitoring System with Explainable AI for Threat Interpretability in the Bureau of Fire Protection"

**Authors:** Cabrales, Nathan Josua C.; Camama, Earl Justin P.; Dela Cruz, Red Gabrielle A.; Tendero, Guinevere T.
**Adviser:** Dr. Kirk Alvin S. Awat
**Institution:** FEU Institute of Technology, March 2026
**Source:** `raw/misc/WIMS-BFP.pdf` (revised, 2026-04-09)

---

## Abstract

This study presents the development and evaluation of [[sources/software-dev/wims-bfp-ch1-introduction|WIMS-BFP]], an offline-capable Progressive Web Application (PWA) designed to provide the Bureau of Fire Protection's (BFP) Fire Suppression Operation Division (FSOD) with a resilient and secure incident monitoring system.

Addressing the operational realities of unstable connectivity and infrastructure disruption in disaster-affected areas, WIMS-BFP adopts an Offline-First architecture supported by local browser storage (IndexedDB) to enable uninterrupted data capture and subsequent synchronization.

The system is deployed through a cloud-hosted Virtual Private Server (VPS) environment while maintaining the strict custody of sensitive records through [[concepts/keycloak-fastapi-security-wims-bfp|role-based access control]], secure transmission protocols, and immutable audit logging.

To reduce the opacity of conventional cybersecurity tools and mitigate alert fatigue, WIMS-BFP incorporates a self-hosted Explainable AI (XAI) support layer powered by the Qwen2.5-3B Small Language Model (SLM). Integrated alongside a Suricata Intrusion Detection System (IDS), this component converts deterministic network security alerts into human-readable forensic narratives for administrator review.

Testing methodologies applied the [[sources/software-dev/owasp-secure-code-review|OWASP Application Security Verification Standard (ASVS)]] Level 2 mapped against a STRIDE threat model, while system quality was evaluated using [[sources/software-dev/wims-bfp-ch3d-testing-data|ISO/IEC 25010]] standards.

The final design successfully bridges offline-first resilience, cloud-based regional accessibility, and explainable security support, all while aligning with the strict compliance mandates of the Data Privacy Act of 2012 (RA 10173).

**Keywords:** Progressive Web Application (PWA), Offline-First Architecture, Explainable AI (XAI), Intrusion Detection System (IDS), Bureau of Fire Protection (BFP)
