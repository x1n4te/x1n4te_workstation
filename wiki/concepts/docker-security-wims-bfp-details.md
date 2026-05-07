---
id: docker-security-wims-bfp-concept-001
type: concept
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - sources/software-dev/docker-security-best-practices
  - sources/software-dev/docker-cves-2025-2026
  - sources/software-dev/docker-compose-security
  - sources/cybersecurity/nist-sp-800-207-zero-trust-architecture
  - concepts/postgresql-security-wims-bfp
status: active
tags:
  - docker
  - container-security
  - devops
  - wims-bfp
  - software-dev
related:
  - sources/software-dev/docker-security-best-practices
  - sources/software-dev/docker-cves-2025-2026
  - sources/software-dev/docker-compose-security
  - concepts/postgresql-security-wims-bfp
  - concepts/secure-coding-practices
  - mocs/cybersecurity
---

# Docker Security for WIMS-BFP

**Synthesis of:** Docker best practices, runc CVEs, PostgreSQL/Redis Compose hardening
**Purpose:** Unified security reference for WIMS-BFP's containerized production stack

---

# Docker Security — Detailed Reference

Back to overview: [[concepts/docker-security-wims-bfp]]
## Security Audit Checklist

### Images
```
[ ] Base images use Alpine (postgres:16-alpine, redis:7-alpine)
[ ] Multi-stage builds for FastAPI and Celery
[ ] trivy image scanning in CI/CD (fail on CRITICAL/HIGH)
[ ] Image digests used (not tags) for production
[ ] .dockerignore excludes .env, *.key, *.pem, .git
```

### Build
```
[ ] All containers run as non-root (user: "1001:1001")
[ ] No secrets in Dockerfile layers (use --mount=type=secret)
[ ] COPY --chown for all files
[ ] Minimal RUN commands (reduce layers)
```

### Runtime
```
[ ] read_only: true on all services except PostgreSQL
[ ] cap_drop: ALL on all services
[ ] cap_add: only what's needed per service
[ ] security_opt: no-new-privileges:true
[ ] Resource limits (cpus, memory) on all services
[ ] Ulimits set (nproc, nofile)
```

### Network
```
[ ] Internal-only bridge for PostgreSQL + Redis
[ ] PostgreSQL port NOT published to host
[ ] Redis port NOT published to host
[ ] chat-network used by application services
[ ] FastAPI is the ONLY entry point to backend network
```

### Secrets
```
[ ] All DB/Redis passwords in /run/secrets/ (not env vars)
[ ] docker secrets or external vault (HashiCorp Vault, AWS Secrets Manager)
[ ] Secrets files in .gitignore and .dockerignore
[ ] Docker socket NEVER mounted in any container
```

### CVEs
```
[ ] runc version ≥1.3.3 (CVE-2025-31133, CVE-2025-52565, CVE-2025-52881)
[ ] Docker Desktop ≥4.61.0 (CVE-2026-28400)
[ ] Never run containers from untrusted images
[ ] Monitor: https://github.com/opencontainers/runc/security/advisories
```

---

## Related

- [[concepts/postgresql-security-wims-bfp]] — PostgreSQL container security
- [[concepts/secure-coding-practices]] — OWASP/CWE coding standards
- [[concepts/zero-trust-architecture]] — ZTA framework mapping
- [[sources/software-dev/docker-security-best-practices]] — Docker security reference
- [[sources/software-dev/docker-cves-2025-2026]] — runc CVEs
- [[mocs/cybersecurity]] — Cybersecurity Map of Content
