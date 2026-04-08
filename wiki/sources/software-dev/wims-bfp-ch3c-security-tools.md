---
id: wims-bfp-ch3c-security-tools-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-07-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - raw/misc/03-05-01-security-practices.md
  - raw/misc/03-05-02-app-cybersecurity-measures.md
  - raw/misc/03-05-cybersecurity-measures.md
  - raw/misc/03-06-01-development-tools.md
  - raw/misc/03-06-02-security-testing-tools.md
  - raw/misc/03-06-03-ai-testing-tools.md
  - raw/misc/03-06-tools-technologies.md
status: active
tags:
  - wims-bfp
  - thesis
  - chapter-3
  - security
  - tools
  - technologies
related:
  - sources/software-dev/wims-bfp-ch3a-research-design
  - sources/software-dev/wims-bfp-ch3b-architecture
  - concepts/postgis-security-wims-bfp
---

# WIMS-BFP Chapter 3c: Security Practices + Tools & Technologies

**Source:** raw/misc/ (7 files)
**Chapter:** 3c — Cybersecurity Measures, Development Tools, Testing Tools

---

## Security Practices (4 domains)

### Authentication and Access Control
- Multi-Factor Authentication (MFA) via Time-Based One-Time Passwords (TOTP) for admin/validation roles
- Identity federation via localized Keycloak instance
- Session management: automatic timeouts + concurrent session limits
- RBAC granularly applied: Encoders restricted to data entry; Validators hold exclusive approval privilege
- Principle of least privilege enforced

### Data Protection
- **Hybrid Encryption Pipeline:** Digital Envelope strategy
  - Data encrypted locally with AES-256-GCM (Data Encryption Key)
  - DEK wrapped using X25519 (Key Encryption Key) before transmission
- **Immutable Storage:** SHA-256 Chain Hashing upon commitment to central DB
  - Each record hashed and linked to preceding entry
  - Tamper-evident ledger: unauthorized modification breaks cryptographic chain
- **Offline-to-Online transition:** Secured via Digital Envelope strategy

### Network Defense and Threat Detection
- Containerized Suricata IDS with threshold-based anomaly detection
- Traffic Mirroring to forward internal packets to Suricata
- Custom rules for: SQL injection, bulk requests, unauthorized scanning
- Qwen2.5-3B asynchronously consumes Suricata EVE JSON → generates forensic narratives
- XAI explains "Impossible Travel" logins, "Bulk Deletion" patterns

### Availability and Resilience
- Offline-first PWA: critical encoding operational during DoS or ISP failures
- Real-time resource monitoring: CPU, RAM, Disk utilization
- Preventative alerts before append-only logging exhausts storage

### Privacy and Compliance
- Automated data classification: segregate Sensitive Personal Information (SPI) from public stats
- Audit trails for every "Read" and "Export" by National Analysts
- DPIA-ready breach notification protocols
- RA 10173 compliance throughout

---

## Technology Stack (FARM Stack)

| Category | Tool | Purpose |
|---|---|---|
| **Backend** | FastAPI | High-performance async orchestration |
| **Frontend** | React.js + Vite (TypeScript) | PWA construction, type safety |
| **Database** | PostgreSQL + PostGIS | Primary relational DB, immutable logs, spatial queries |
| **Local Storage** | IndexedDB + Dexie.js | Browser-side NoSQL for offline capture |
| **Message Broker** | Redis | In-memory broker for decoupling AI tasks |
| **Task Queue** | Celery | Distributed background AI jobs |
| **State Management** | TanStack Query | Offline sync + server state |
| **AI Model** | Qwen2.5-3B | Small Language Model for threat analysis |
| **AI Runtime** | Llama.cpp | Quantized model runner for consumer hardware |
| **AI Structuring** | Instructor | Enforces structured JSON output from SLM |
| **IDS** | Suricata | Network intrusion detection engine |
| **KMS** | OpenBao | Key Management Service for hybrid encryption |
| **Identity** | Keycloak | IdP for RBAC and MFA |
| **Cryptography** | PyNaCl / Libsodium | X25519/AES-GCM encryption |
| **Containerization** | Docker + Docker Compose | Consistent air-gapped deployment |
| **Reverse Proxy** | Nginx | TLS termination + static file serving |

### Why FARM Stack
- Native async concurrency support
- Python/FastAPI handles high-throughput HTTP while offloading to Celery
- React.js + TypeScript for strict type safety in data entry modules
- TanStack Query + Dexie.js abstract browser storage/sync complexity

### Why Llama.cpp + Qwen2.5-3B
- 3B parameter model runs on consumer-grade RAM via quantization
- "AI-on-Premise" economically feasible for BFP
- No dependency on external cloud AI providers

---

## Security Testing Tools

| Tool | Purpose | Application |
|---|---|---|
| OWASP ZAP | Web application security scanner | Automated vulnerability scanning |
| sqlmap | SQL injection detection + exploitation | Verify parameterized query defenses |
| Burp Suite | Web vulnerability scanning | Manual penetration testing |
| Nmap | Network discovery + port scanning | Infrastructure enumeration |
| Nikto | Web server scanner | Server misconfiguration detection |

## AI Testing Tools

| Tool | Purpose | Application |
|---|---|---|
| Locust | Load testing | Concurrent user simulation |
| Custom MOS Survey | Usability evaluation | XAI narrative clarity scoring |
| F1-Score Analysis | Detection accuracy | Suricata IDS precision/recall |
| Inference Profiling | Latency measurement | Qwen2.5-3B response time |

---

## Cross-References

- [[sources/software-dev/wims-bfp-ch3a-research-design]] — Research design + requirements
- [[concepts/postgis-security-wims-bfp]] — PostGIS security
- [[concepts/keycloak-fastapi-security-wims-bfp]] — Auth security
