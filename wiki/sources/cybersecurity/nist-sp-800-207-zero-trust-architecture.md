---
id: nist-sp-800-207-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf
  - cyberark.com/what-is/nist-sp-800-207-cybersecurity-framework/
status: active
tags:
  - zero-trust
  - nist
  - cybersecurity-framework
  - access-control
  - identity-management
related:
  - concepts/zero-trust-architecture
  - concepts/authentication-architecture
  - concepts/defense-in-depth
---

# NIST SP 800-207 — Zero Trust Architecture (Source Summary)

**Source:** NIST SP 800-207 (Aug 2020) + CyberArk interpretation
**Type:** Foundational framework document
**Confidence:** High — authoritative government standard

---

## The 7 Tenets of Zero Trust

These tenets define the core of Zero Trust Architecture per NIST SP 800-207:

| # | Tenet | Meaning |
|---|---|---|
| 1 | All data sources and computing services are considered resources | Extend ZT to all resources — SaaS, personal devices, cloud |
| 2 | All communication is secured regardless of network location | No trusted network zones — consistent controls everywhere |
| 3 | Access granted on a per-session basis | Evaluate trust before each access, grant least privileges |
| 4 | Access determined by dynamic policy | Policies based on behavioral and environmental attributes |
| 5 | Monitor integrity and security posture of all assets | Patch and fix systems, including personal devices |
| 6 | Authentication and authorization are dynamic and strictly enforced | Use ICAM policies, MFA, continual monitoring |
| 7 | Collect as much information as possible to improve security posture | Fine-tune access policies based on collected data |

## 3 Core Components

| Component | Role |
|---|---|
| **Policy Engine** | Makes access decisions based on policies + trust score |
| **Policy Administrator** | Manages and configures access policies |
| **Policy Enforcement Point** | Enforces access decisions at the resource boundary |

## Trust Algorithm

NIST recommends a trust algorithm built on:
- **Observable entity and system data** — what can be measured about the requestor
- **Threat intelligence** — current threat landscape
- **Dynamic trust score** — changes over time based on entity behavior

## 4 Use Cases

1. **Regulated industries** — finance, healthcare, government protecting critical infrastructure
2. **Digital transformation** — securing remote work, cloud apps, distributed networks
3. **SaaS protection** — securing cloud-based applications and services
4. **Hybrid environments** — on-prem + cloud with consistent security posture

## Benefits

- Reduces breach risk through continuous verification
- Secures data regardless of location
- Enables effective threat response
- Meets regulatory requirements

## Challenges

- Requires major infrastructure changes from perimeter-based model
- Needs advanced technologies (IAM, MFA, endpoint security)
- Resource-intensive — continuous monitoring, real-time analysis
- Legacy system compatibility issues

---

## WIMS-BFP Mapping

WIMS-BFP already implements several NIST tenets:

| WIMS-BFP Component | Maps to NIST Tenet |
|---|---|
| Keycloak RBAC + MFA | Tenet 6: Dynamic authentication/authorization |
| RLS (wims.current_user_id) | Tenet 3: Per-session access control |
| JWT validation (kid, iss, aud, signature, expiry) | Tenet 4: Dynamic policy |
| DMZ air-lock (public/internal separation) | Tenet 2: Security regardless of network |
| Audit logging | Tenet 7: Collect information to improve posture |

---

## Concepts Derived From This Source

- [[concepts/zero-trust-architecture]] — Full ZTA concept page
