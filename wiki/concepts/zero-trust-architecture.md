---
id: zero-trust-architecture-concept-001
type: concept
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - sources/cybersecurity/nist-sp-800-207-zero-trust-architecture
  - sources/cybersecurity/dod-zta-implementation-primer-2026
  - sources/cybersecurity/zero-trust-complete-guide-2026
status: active
tags:
  - zero-trust
  - cybersecurity-framework
  - access-control
  - nist
  - identity-management
related:
  - concepts/authentication-architecture
  - sources/cybersecurity/nist-sp-800-207-zero-trust-architecture
  - sources/cybersecurity/dod-zta-implementation-primer-2026
---

# Zero Trust Architecture (ZTA)

**Framework:** NIST SP 800-207 (Aug 2020)
**Updated:** DoW/NSA Implementation Primer (Jan 2026)
**Principle:** "Never trust, always verify"

---

## Definition

Zero Trust Architecture (ZTA) is a cybersecurity framework that eliminates the concept of a trusted internal network. Every user, device, and application must prove identity and authorization before every access request. There are no trusted network zones.

## Core Principles

| Principle | Description |
|---|---|
| **Never trust, always verify** | Treat every entity as untrusted. Dynamically authenticate and approve all activity. |
| **Assume breach** | Operate under the assumption an adversary is present. Deny-by-default. |
| **Verify explicitly** | Use multiple attributes to derive confidence levels for contextual access decisions. |
| **Least privilege** | Grant minimum access rights necessary. Regular permission reviews. |

## The 7 NIST Tenets

| # | Tenet |
|---|---|
| 1 | All data sources and computing services are considered resources |
| 2 | All communication is secured regardless of network location |
| 3 | Access to individual resources granted on a per-session basis |
| 4 | Access determined by dynamic policy |
| 5 | Monitor integrity and security posture of all owned/associated assets |
| 6 | All resource authentication and authorization are dynamic and strictly enforced |
| 7 | Collect as much information as possible to improve security posture |

## 3 Core Components (NIST)

| Component | Role |
|---|---|
| **Policy Engine** | Makes access decisions based on policies + trust score |
| **Policy Administrator** | Manages and configures access policies |
| **Policy Enforcement Point** | Enforces decisions at the resource boundary |

## 7 Pillars (NIST/CISA)

| Pillar | Focus |
|---|---|
| Identity | User authentication and authorization |
| Devices | Endpoint health and compliance |
| Networks | Microsegmentation and encrypted communications |
| Applications | App-level security and runtime protection |
| Data | Classification, encryption, and loss prevention |
| Infrastructure | Cloud, on-prem, hybrid, IoT security |
| Visibility & Analytics | Continuous monitoring and threat detection |

## Implementation Phases (DoD 2026)

| Phase | Focus |
|---|---|
| Discovery | Collect environment info (DAAS, users, devices) |
| Phase 1 | Build secure foundation |
| Phase 2 | Integrate ZT fundamental solutions |
| Phase 3-4 | Advanced and optimal-level ZT |

## Market Impact (2026)

- 81% of organizations planning ZTA implementation
- $78 billion projected global market by 2030
- Organizations without ZTA face 38% higher breach costs
- ZTA reduces breach costs by $1.76 million on average

## Common Mistakes

1. **Treating ZTA as a product purchase** — it's an architecture + cultural shift
2. **Ignoring legacy systems** — isolate what you can't upgrade
3. **Skipping identity foundation** — strong identity controls are the bedrock
4. **Boiling the ocean** — start with one protect surface, expand incrementally

---

## WIMS-BFP Alignment

| WIMS-BFP Component | ZTA Tenet/Mechanism |
|---|---|
| Keycloak RBAC + MFA | Identity pillar, Tenet 6 |
| RLS (wims.current_user_id) | Tenet 3: Per-session access |
| JWT validation (kid, iss, aud, sig, exp) | Tenet 4: Dynamic policy |
| DMZ air-lock (public/reporting separation) | Tenet 2: Security regardless of network |
| Audit logging | Tenet 7: Improve security posture |
| PostGIS region isolation | Microsegmentation (network pillar) |

---

## Related

- [[concepts/authentication-architecture]] — Keycloak + JWT validation
- [[sources/cybersecurity/nist-sp-800-207-zero-trust-architecture]] — Primary source
- [[sources/cybersecurity/dod-zta-implementation-primer-2026]] — Practical implementation
- [[sources/cybersecurity/zero-trust-complete-guide-2026]] — Market data + challenges
