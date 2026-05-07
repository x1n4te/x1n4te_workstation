# Wiki Schema

## Domain
Personal knowledge base covering:
- **WIMS-BFP** — thesis project (cybersecurity incident monitoring for BFP)
- **Hermes Agent** — CLI AI agent configuration, skills, workflows
- **Cybersecurity** — CVEs, OWASP, Zero Trust, penetration testing, SOC lab
- **AI/ML Research** — LLMs, SLMs, training, inference, XAI
- **Software Dev** — FastAPI, PostgreSQL, Docker, Keycloak, Next.js, React Native

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `transformer-architecture.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- `raw/` is immutable — never modify source files after ingestion

## Frontmatter
```yaml
---
id: deterministic-slug-001          # slug + hash suffix
type: source | concept | entity | analysis | MOC
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_verified: YYYY-MM-DD
review_after: YYYY-MM-DD            # created + 90 days (default)
stale_after: YYYY-MM-DD             # created + 180 days (default)
confidence: high | medium | low
source_refs:                         # what backs this page
  - raw/path/to/source.md
status: active | archived | under_review | stale
tags:                                # from taxonomy below ONLY
  - tag1
  - tag2
related:                             # cross-references to other wiki pages
  - concepts/other-page
  - entities/some-entity
---
```

**TTL defaults by category:**

| Category | review_after | stale_after |
|---|---|---|
| AI Research | 30 days | 90 days |
| Cybersecurity (threat intel) | 7 days | 21 days |
| Cybersecurity (architecture) | 90 days | 180 days |
| Software Dev | 60 days | 120 days |
| Operational (session logs) | 30 days | 90 days |

## Tag Taxonomy

Valid tags only. Add new tags here BEFORE using them.

### Project Tags
| Tag | Scope |
|---|---|
| `wims-bfp` | WIMS-BFP thesis project |
| `thesis` | Thesis documentation, methodology, chapters |
| `hermes` | Hermes agent, skills, workflows |
| `smart-parenting-app` | NestNote / Smart Parenting App |
| `frs` | Functional Requirements Specification |
| `ierc` | Institutional Ethics Review Committee |

### Security Domain
| Tag | Scope |
|---|---|
| `security` | General security concepts |
| `cybersecurity` | Threat intel, SOC, incident response |
| `cybersecurity-framework` | NIST, DoD, NSA frameworks |
| `cve` | CVE tracking and analysis |
| `cwe` | Common Weakness Enumeration |
| `owasp` | OWASP standards, Top 10, ASVS |
| `owasp-api` | OWASP API Security Top 10 |
| `zero-trust` | Zero Trust Architecture |
| `pen-testing` | Penetration testing, red teaming |
| `red-teaming` | Adversarial simulation, red team ops |
| `ctf` | Capture the flag writeups |
| `suricata` | Suricata IDS/IPS |
| `ids-ips` | Intrusion detection/prevention systems |
| `auth` | Authentication, authorization, identity |
| `authentication` | Auth mechanisms, login flows |
| `mfa` | Multi-factor authentication, TOTP |
| `jwt` | JSON Web Tokens |
| `oauth2` | OAuth 2.0 protocol |
| `totp` | Time-based one-time passwords |
| `rbac` | Role-based access control |
| `rls` | Row-Level Security policies |
| `access-control` | Access control mechanisms |
| `identity-management` | Identity providers, user management |
| `identity` | Identity concepts |
| `iam` | Identity and Access Management |
| `api-security` | API security, rate limiting, validation |
| `vulnerability` | Vulnerability analysis, CVEs |
| `encryption` | Encryption, PII protection |
| `threat-model` | Threat modeling, STRIDE |
| `sql-injection` | SQL injection attacks and defenses |
| `prompt-injection` | LLM prompt injection attacks |
| `adversarial-ml` | Adversarial machine learning |
| `jailbreaking` | LLM jailbreaking techniques |
| `container-security` | Docker/container security |
| `container-escape` | Container escape vulnerabilities |
| `runc` | runc container runtime CVEs |
| `web-security` | Web application security |
| `mitre` | MITRE ATT&CK framework |
| `mitre-attack` | MITRE ATT&CK tactics/techniques |
| `kill-chain` | Cyber kill chain model |
| `nist` | NIST standards and frameworks |
| `dod` | Department of Defense guidelines |
| `nsa` | NSA security guidelines |
| `secure-coding` | Secure coding practices |
| `social-engineering` | Social engineering attacks |
| `error-leakage` | Error message information leakage |

### Infrastructure & Backend
| Tag | Scope |
|---|---|
| `docker` | Docker, containerization, compose |
| `postgresql` | PostgreSQL, PostGIS |
| `postgres` | PostgreSQL (alternate) |
| `postgis` | PostGIS spatial extensions |
| `spatial` | Spatial data, GIS, geolocation |
| `keycloak` | Keycloak, identity provider |
| `fastapi` | FastAPI, backend API |
| `redis` | Redis, caching, message broker |
| `celery` | Celery task queue |
| `task-queue` | Task queue patterns |
| `nginx` | Nginx, reverse proxy |
| `database` | Database design, migrations, schema |
| `supabase` | Supabase platform |
| `pgbouncer` | PgBouncer connection pooling |
| `alembic` | Alembic database migrations |
| `schema` | Database/API schema design |
| `data-flow` | Data flow patterns, pipelines |
| `encryption` | Data encryption at rest/transit |
| `ci-cd` | CI/CD pipelines |
| `deployment` | Deployment strategies |
| `infrastructure` | Infrastructure as code |
| `production` | Production environment |
| `production-ready` | Production readiness |
| `offline` | Offline-first, PWA patterns |
| `pwa` | Progressive Web Apps |
| `cloud` | Cloud platforms |
| `self-hosted` | Self-hosted software |

### Mobile & Frontend
| Tag | Scope |
|---|---|
| `react-native` | React Native framework |
| `expo` | Expo SDK, Expo Router |
| `expo-notifications` | Expo push/local notifications |
| `nextjs` | Next.js framework |
| `frontend` | Frontend development |
| `android` | Android platform |
| `ios` | iOS platform |
| `mobile` | Mobile development general |
| `mobile-dev` | React Native, Expo, mobile apps |
| `mobile-development` | Mobile development practices |
| `ui` | User interface design |
| `ui-design` | UI design patterns |
| `ui-ux` | UI/UX combined |
| `hci` | Human-Computer Interaction |
| `accessibility` | Accessibility (a11y) |
| `themes` | Theming, styling |
| `dashboard` | Dashboard UI patterns |

### AI/ML
| Tag | Scope |
|---|---|
| `ai-research` | AI/ML research, theory |
| `ai` | Artificial intelligence general |
| `llm` | Large language models |
| `slm` | Small language models |
| `llm-agents` | LLM-based agents |
| `ai-agents` | AI agent systems |
| `agentic-ai` | Agentic AI concepts |
| `agentic-workflows` | Agentic workflow patterns |
| `multi-agent` | Multi-agent systems |
| `xai` | Explainable AI |
| `agents` | AI agents, multi-agent systems |
| `training` | Model training, fine-tuning, RLHF |
| `fine-tuning` | Model fine-tuning |
| `inference` | Model serving, quantization, deployment |
| `deep-learning` | Neural networks, architectures |
| `transformers` | Transformer architecture |
| `moe` | Mixture of Experts |
| `multi-token-prediction` | Multi-token prediction |
| `hardware-efficient` | Hardware-efficient architectures |
| `attention` | Attention mechanisms |
| `neural-networks` | Neural network architectures |
| `benchmark` | Model benchmarks, evaluation |
| `model` | Model architecture, design |
| `reasoning` | Reasoning capabilities |
| `qwen2.5-3b` | Qwen2.5-3B model |
| `minimax` | MiniMax models |
| `openrouter` | OpenRouter API |
| `anthropic` | Anthropic (Claude) |
| `claude` | Claude models |
| `nous-research` | Nous Research models |
| `prompt-engineering` | Prompt engineering techniques |
| `prompt-caching` | Prompt caching strategies |
| `context-compression` | Context compression techniques |
| `token-optimization` | Token usage optimization |
| `cost-optimization` | API cost optimization |
| `multi-model` | Multi-model routing |
| `model-routing` | Model routing strategies |
| `hallucinations` | LLM hallucination issues |
| `ai-detection` | AI content detection |
| `ai-writing-revision` | De-AI-ify writing |
| `rag` | Retrieval-Augmented Generation |
| `retrieval` | Information retrieval |
| `knowledge-management` | Knowledge management systems |
| `knowledge-graph` | Knowledge graphs |
| `pipeline` | Data/ML pipelines |
| `evaluation` | Model/system evaluation |
| `dspy` | DSPy framework |
| `declarative-learning` | Declarative learning systems |
| `optimization` | Optimization techniques |

### Memory Systems
| Tag | Scope |
|---|---|
| `memory-systems` | Memory system architectures |
| `memory-system` | Memory system (singular) |
| `memory-architecture` | Memory architecture patterns |
| `procedural-memory` | Procedural memory (skills) |
| `episodic-memory` | Episodic memory (sessions) |
| `semantic-memory` | Semantic memory (facts) |
| `observational-memory` | Observational memory |
| `virtual-memory` | Virtual memory concepts |
| `os-inspired` | OS-inspired agent patterns |
| `agent-framework` | Agent framework design |
| `learning-loop` | Learning loop patterns |
| `autonomous-learning` | Autonomous learning systems |
| `compression` | Context/memory compression |
| `code-map` | Code mapping techniques |

### Development Practices
| Tag | Scope |
|---|---|
| `software-dev` | Software development practices |
| `software-engineering` | Software engineering principles |
| `design` | Architecture, system design, patterns |
| `system-design` | System design patterns |
| `testing` | Testing, QA, evaluation |
| `integration-tests` | Integration testing |
| `debugging` | Debugging techniques |
| `code-review` | Code review practices |
| `review-checklist` | Review checklists |
| `refactoring` | Code refactoring |
| `devops` | CI/CD, deployment, infrastructure |
| `github` | GitHub repositories, issues, pull requests, Actions |
| `coding` | Coding practices |
| `python` | Python language |
| `implementation` | Implementation details |
| `framework` | Framework design |
| `api` | API design |
| `endpoint` | API endpoints |
| `rest-api` | REST API patterns |
| `admin-api` | Admin API patterns |
| `api-optimization` | API optimization |
| `cli` | Command-line interfaces |
| `tools` | Development tools |
| `commands` | CLI commands |
| `quick-reference` | Quick reference guides |
| `configuration` | Configuration management |
| `config` | Configuration files |
| `setup` | Setup/installation guides |
| `environment` | Environment management |
| `arch-linux` | Arch Linux specific |
| `hardware` | Hardware considerations |
| `migration` | Data/system migrations |
| `breaking-changes` | Breaking changes |
| `release-notes` | Release notes |

### Hermes Agent
| Tag | Scope |
|---|---|
| `hermes-agent` | Hermes agent platform |
| `skills` | Hermes skills |
| `skill-md` | SKILL.md format |
| `delegation` | Task delegation |
| `subagent` | Sub-agent patterns |
| `parallelism` | Parallel execution |
| `asymmetric-delegation` | Asymmetric delegation patterns |
| `activity-logging` | Activity logging |
| `deep-research` | Deep research workflows |

### Research & Learning
| Tag | Scope |
|---|---|
| `learning` | Learning paths, educational content |
| `papers` | Academic papers, research |
| `foundations` | Foundational concepts |
| `applied` | Applied techniques, practical |
| `practical` | Practical applications |
| `research` | Research activities |
| `reference` | Reference material |
| `taxonomy` | Classification systems |
| `domain` | Domain knowledge |
| `open-standard` | Open standards |
| `open-source` | Open source projects |
| `writeups` | Technical writeups |
| `cognitive-science` | Cognitive science |
| `tulving` | Tulving memory taxonomy |
| `health` | Health/medical topics |
| `pediatrics` | Pediatric topics |
| `bmi-calculator` | BMI calculation |

### CTF & Security Labs
| Tag | Scope |
|---|---|
| `tryhackme` | TryHackMe labs |
| `hackthebox` | HackTheBox labs |
| `soc` | Security Operations Center |
| `wazuh` | Wazuh SIEM |
| `siem` | SIEM systems |
| `qemu` | QEMU virtualization |
| `kvm` | KVM virtualization |
| `home-lab` | Home lab setups |
| `market-data` | Market/threat intelligence data |

### Thesis Specific
| Tag | Scope |
|---|---|
| `chapter-1` | Thesis Chapter 1 |
| `chapter-2` | Thesis Chapter 2 |
| `chapter-3` | Thesis Chapter 3 |
| `section-3-9` | Thesis Section 3.9 |
| `appendix-a` | Thesis Appendix A |
| `appendix-h` | Thesis Appendix H |
| `abstract` | Thesis abstract |
| `methodology` | Research methodology |
| `research-design` | Research design |
| `requirements` | Requirements gathering |
| `ethics` | Ethics review |
| `mldc` | MLDC methodology |
| `technologies` | Technology stack |
| `revisions` | Document revisions |
| `implementation-tracker` | Implementation tracking |

### WIMS-BFP Specific
| Tag | Scope |
|---|---|
| `bfp` | Bureau of Fire Protection |
| `fire-protection` | Fire protection domain |
| `regional-encoder` | Regional encoder role |
| `regional-crud` | Regional CRUD operations |
| `crud` | CRUD operations |
| `module-12` | WIMS Module 12 |
| `ai-insights` | AI insights features |
| `supabase-edge-functions` | Supabase Edge Functions |
| `recommendations` | Recommendation systems |
| `user-management` | User management |
| `discrepancy` | Code/doc discrepancies |
| `discrepancy-fixes` | Discrepancy fixes |
| `codebase-analysis` | Codebase analysis |
| `codebase-ingestion` | Codebase ingestion |
| `pre-refactor` | Pre-refactor state |
| `health-report` | System health reports |
| `inventory` | Inventory/cataloging |
| `loc` | Lines of code metrics |
| `pygount` | Pygount LOC tool |

### Smart Parenting App
| Tag | Scope |
|---|---|
| `scheduled-activities` | Scheduled activity features |
| `ui-redesign` | UI redesign efforts |
| `commission` | Commissioned project |

### Page Types (for MOCs and special pages)
| Tag | Scope |
|---|---|
| `moc` | Map of Content pages |
| `operational` | Session logs, debugging, daily ops |
| `comparison` | Side-by-side analyses |
| `analysis` | Synthesis, audit, postmortem |
| `comparative-analysis` | Comparative analysis |
| `postmortem` | Post-incident reviews |
| `lessons-learned` | Lessons learned |
| `introduction` | Introductory content |
| `literature-review` | Literature reviews |
| `rrl` | Review of Related Literature |
| `codebase` | Codebase documentation |
| `metrics` | Metrics and measurements |

### General
| Tag | Scope |
|---|---|
| `data-gathering` | Data collection methods |
| `ai` | Artificial intelligence general |

**Rule:** Every tag on a page must appear in this table. If you need a new tag, add it here first, then use it.

**Deprecated tags (do not use):**
- `archived` — use `status: archived` in frontmatter instead
- `<relevant tags>` — placeholder, never use

## Page Types

| Type | What it holds | Example |
|---|---|---|
| `source` | Summary of a raw source document | `wiki/sources/software-dev/wims-bfp-ch1-introduction.md` |
| `concept` | Ideas, theories, patterns, how-tos | `wiki/concepts/zero-trust-architecture.md` |
| `entity` | People, orgs, products, tools | `wiki/entities/hermes-agent.md` |
| `analysis` | Syntheses, comparisons, audits | `wiki/analyses/wims-bfp-thesis-codebase-gaps.md` |
| `MOC` | Thematic hub with reading path | `wiki/mocs/wims-bfp.md` |

## Page Thresholds
- **Create a page** when an entity/concept appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions, minor details, or things outside the domain
- **Split a page** when it exceeds ~200 lines — break into sub-topics with cross-links
- **Archive a page** when its content is fully superseded — move to `.archived/` subdirectory, remove from index

## Cross-Referencing
- Every page needs minimum 2 outbound `[[wikilinks]]` in body text
- `related:` in frontmatter is for Obsidian graph view
- Inline `[[wikilinks]]` in body text are for LLM traversal
- Both are needed — they serve different purposes

## Update Policy
When new information conflicts with existing content:
1. Check dates — newer sources supersede older
2. If genuinely contradictory, note both with dates and sources
3. Mark contradiction in frontmatter: add to `related:` pointing to the conflicting page
4. Flag for user review in session close

## Archiving
When content is fully superseded:
1. Move to `<page>.archived/YYYY-MM-DD-<title>.md` subdirectory
2. Remove from `index.md`
3. Update pages that linked to it — replace wikilink with plain text + "(archived)"
4. Log the archive action
