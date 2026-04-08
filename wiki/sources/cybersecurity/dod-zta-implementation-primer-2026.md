---
id: dod-zta-primer-2026-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - media.defense.gov/2026/Jan/08/2003852320/-1/-1/0/CTR_ZERO_TRUST_IMPLEMENTATION_GUIDELINE_PRIMER.PDF
status: active
tags:
  - zero-trust
  - dod
  - nsa
  - cybersecurity-framework
  - implementation
related:
  - concepts/zero-trust-architecture
  - sources/cybersecurity/nist-sp-800-207-zero-trust-architecture
---

# DoW/NSA Zero Trust Implementation Guideline Primer (Jan 2026)

**Source:** Department of War / NSA — Zero Trust Implementation Guideline Primer v1.0
**Date:** January 2026
**Type:** Practical implementation guide (latest government ZTA guidance)

---

## 3 Core Principles (aligned with NIST SP 800-207)

| Principle | Description |
|---|---|
| **"Never trust, always verify"** | Treat every user, device, application, and data flow as untrusted. Dynamically authenticate and explicitly approve all activity based on Least Privilege. |
| **"Assume breach"** | Operate and defend resources under the assumption an adversary is present. Plan for deny-by-default, scrutinize all entities, continuously log/inspect/monitor. |
| **"Verify explicitly"** | Securely and consistently verify access using multiple attributes to derive confidence levels for contextual access decisions. |

## Design Methodology

1. **Architect from inside out** — First protect critical DAAS (Data, Applications, Assets, Services), then secure all access paths
2. **Define mission outcomes** — Derived from critical DAAS
3. **Determine who/what needs access** — Create consistent access control policies
4. **Inspect and log all traffic before acting** — Enable comprehensive visibility and analytics

## 5-Phase Implementation Framework

| Phase | Activities | Focus |
|---|---|---|
| **Discovery** | 14 Activities, 13 Capabilities | Collect info about environment (DAAS, users, devices) |
| **Phase 1** | 36 Activities, 30 Capabilities | Build secure foundation for ZT |
| **Phase 2** | 41 Activities, 34 Capabilities | Integrate distinct ZT fundamental solutions |
| **Phase 3** | Advanced ZIGs (developed later) | Advanced-level ZT |
| **Phase 4** | Advanced ZIGs (developed later) | Optimal-level ZT |

## ZIG Structure (Per Activity)

Each Activity follows:
1. **Activity Table** — ID, Description, Predecessor(s), Successor(s), Expected Outcomes, End State
2. **Considerations** — Prerequisites, challenges, lessons learned, dependencies
3. **Implementation** — Actionable roadmap with Tasks and process steps
4. **Summary** — Readiness assessment, strategic insights, expected outcomes

## 4 Strategic Goals (DoW ZT Strategy)

| Goal | Description |
|---|---|
| ZT cultural adoption | Enterprise-wide mindset shift |
| Secured and defended information systems | Protected resources |
| Technology acceleration | Rapid deployment of ZT technologies |
| ZT enablement | Tools and frameworks for practitioners |

## Foundational Documents

- NIST SP 800-207 (Aug 2020)
- CISA Zero Trust Maturity Model v2.0 (Jan 2022)
- DoW Zero Trust Reference Architecture v2.0 (Jul 2022)
- DoW Zero Trust Strategy v1.0 (Oct 2022)
- Executive Order 14028 ("Improving the Nation's Cybersecurity")
- National Security Memorandum 8 (NSM-8)

---

## Concepts Derived From This Source

- [[concepts/zero-trust-architecture]] — Full ZTA concept page
