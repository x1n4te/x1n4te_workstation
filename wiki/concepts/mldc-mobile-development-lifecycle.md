---
id: mldc-mobile-development-lifecycle-001
type: concept
created: 2026-04-10
updated: 2026-04-10
last_verified: 2026-04-10
review_after: 2026-07-10
stale_after: 2026-10-09
confidence: high
source_refs:
  - sources/operational/2026-04-10-smart-parenting-ui-redesign
status: active
tags:
  - mldc
  - mobile-development
  - methodology
  - android
  - ios
  - software-engineering
related:
  - concepts/smart-parenting-app-tech-stack
  - sources/software-dev/wims-bfp-ch3a-research-design
---

# MDLC — Mobile Development Life Cycle

**What:** A structured methodology for developing mobile applications, covering the full lifecycle from concept to deployment and maintenance.

**Used in:** Smart Parenting App thesis (Section 3.1), and this commission.

---

## The 6 Stages (ResearchGate/Standard Model)

```
Conceptualization → Design → Development → Testing → Deployment → Maintenance
```

| Stage | Activities | Deliverables |
|---|---|---|
| **1. Conceptualization & Planning** | Define problem, objectives, scope, target audience, feasibility study | Project charter, requirements doc |
| **2. Design** | UI/UX wireframes, system architecture, database schema, API design | Wireframes, architecture diagrams, ERD |
| **3. Material Collecting** | Gather assets, libraries, APIs, frameworks, third-party services | Tech stack, dependency list, assets |
| **4. Assembly (Development)** | Code the app — frontend, backend, database, integrations | Working prototype/app |
| **5. Testing** | Unit, integration, usability, performance, security testing | Test reports, bug fixes |
| **6. Deployment & Maintenance** | App store submission, monitoring, updates, user support | Published app, maintenance plan |

---

## The 7 Stages (LinkedIn/Extended Model)

| Stage | Focus |
|---|---|
| 1. Ideation | Concept, market research, competitive analysis |
| 2. Planning | Requirements, user stories, project timeline |
| 3. Design | UI/UX, wireframes, prototypes |
| 4. Development | Coding, integration, API development |
| 5. Testing | QA, bug fixing, performance optimization |
| 6. Deployment | App store submission, launch |
| 7. Maintenance | Updates, bug fixes, feature additions |

---

## The 8 Phases (Queppelin/Enterprise Model)

| Phase | Activities |
|---|---|
| 1. Pre-planning & Research | Market analysis, user research, competitor study |
| 2. Mental Prototyping | Concept sketches, user journey mapping |
| 3. Technical Feasibility | Tech stack evaluation, resource assessment |
| 4. Building a Prototype | Interactive mockups, clickable wireframes |
| 5. Design | UI/UX design, design system, visual assets |
| 6. Development | Coding, API integration, database setup |
| 7. Testing | QA, UAT, security testing, performance testing |
| 8. Deployment & Maintenance | Launch, monitoring, updates, support |

---

## Connection to This Project

The Smart Parenting App commission follows MDLC:

| MDLC Stage | Project Activity |
|---|---|
| Conceptualization | Thesis spec (Ch 1-3), requirements analysis |
| Design | Use case diagrams, activity diagrams, storyboard |
| Material Collecting | Tech stack selection (Expo, Supabase, OpenRouter) |
| Assembly | React Native development, backend API, AI integration |
| Testing | Functional testing, usability testing, AI output validation |
| Deployment | EAS Build → APK/IPA → app stores |

The thesis uses Agile sprints within the MDLC framework:
- Sprint 1: Core features (auth, dashboard, logging)
- Sprint 2: AI features (analysis, recommendations)
- Sprint 3: Testing + refinement

---

## MDLC vs Other Methodologies

| Methodology | Focus | Best For |
|---|---|---|
| **MDLC** | Mobile-specific lifecycle | Mobile apps |
| SDLC | General software lifecycle | Any software |
| Agile/Scrum | Iterative development | Flexible requirements |
| Waterfall | Sequential phases | Fixed requirements |
| DevOps | Development + operations | Continuous delivery |

MDLC is NOT a replacement for Agile — it's a framework that Agile sprints fit within.

---

## Resources

| Resource | Link |
|---|---|
| MDLC stages (ResearchGate) | https://www.researchgate.net/figure/Stages-of-MDLC-Method-23_fig1_336791054 |
| 7 Stages of Mobile App Dev (LinkedIn) | https://www.linkedin.com/pulse/7-stages-mobile-app-development-life-cycle-comprehensive-cl1cc |
| 8 Phases (Queppelin) | https://www.queppelin.com/8-phases-of-mobile-app-development-lifecycle/ |
| 10 Key Stages (LANSA) | https://lansa.com/blog/app-development/mobile-app-development/mobile-app-development-lifecycle/ |

---

## Related

- [[concepts/smart-parenting-app-tech-stack]] — Tech stack for this project
- [[sources/software-dev/wims-bfp-ch3a-research-design]] — WIMS-BFP research design (different methodology — V-Model)
