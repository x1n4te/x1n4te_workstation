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

## WIMS-BFP Docker Architecture

```
┌─────────────────────────────────────────────┐
│                 chat-network                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ FastAPI   │  │ Celery   │  │ Suricata  │ │
│  │ (backend) │  │ (worker) │  │ (beat)    │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
│       │              │              │        │
│  ┌────┴──────────────┴──────────────┴─────┐  │
│  │           PostgreSQL + PostGIS         │  │
│  └────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────┐  │
│  │              Redis                     │  │
│  └────────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
                │
           ┌────┴────┐
           │ Next.js  │
           │ (PWA)    │
           └─────────┘
```

---

## ZTA Mapping for Docker

| Component | ZTA Tenet | Implementation |
|---|---|---|
| **Network isolation** | Tenet 2: Security regardless of network | chat-network internal bridge, no exposed DB ports |
| **Non-root containers** | Tenet 6: Dynamic auth | Containers run as dedicated service accounts |
| **Secrets via files** | Tenet 4: Dynamic policy | DB passwords in `/run/secrets/`, not env vars |
| **Image scanning** | Tenet 7: Improve posture | trivy in CI/CD pipeline |
| **Read-only filesystem** | Tenet 5: Monitor assets | Immutable container filesystem |

---

## docker-compose.yml Security Template

```yaml
version: '3.8'

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No internet access — PostgreSQL + Redis only

services:
  fastapi:
    image: wims-bfp/backend:latest
    user: "1001:1001"  # Non-root
    read_only: true
    tmpfs:
      - /tmp:rw,noexec,nosuid
    cap_drop: [ALL]
    cap_add: [NET_BIND_SERVICE]
    security_opt: [no-new-privileges:true]
    deploy:
      resources:
        limits: {cpus: '1.0', memory: 512M}
    networks:
      - frontend
      - backend
    depends_on:
      postgres: {condition: service_healthy}
      redis: {condition: service_healthy}
    environment:
      DATABASE_URL_FILE: /run/secrets/db_url
      REDIS_URL_FILE: /run/secrets/redis_url
    secrets: [db_url, redis_url]

  celery:
    image: wims-bfp/worker:latest
    user: "1001:1001"
    read_only: true
    cap_drop: [ALL]
    security_opt: [no-new-privileges:true]
    deploy:
      resources:
        limits: {cpus: '0.5', memory: 256M}
    networks:
      - backend
    depends_on:
      postgres: {condition: service_healthy}
      redis: {condition: service_healthy}
    environment:
      DATABASE_URL_FILE: /run/secrets/db_url
    secrets: [db_url]

  postgres:
    image: postgres:16-alpine
    user: "999:999"  # postgres user
    read_only: false  # Needs write for data
    tmpfs:
      - /tmp:rw,noexec,nosuid
      - /run/postgresql:rw,noexec,nosuid
    cap_drop: [ALL]
    cap_add: [DAC_OVERRIDE, CHOWN, FOWNER, SETGID, SETUID]  # Minimal for PG
    security_opt: [no-new-privileges:true]
    networks:
      - backend
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/pg_password
    secrets: [pg_password]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    command: >
      postgres -c ssl=on
      -c ssl_cert_file=/etc/ssl/certs/server.crt
      -c ssl_key_file=/etc/ssl/private/server.key
      -c log_statement=all

  redis:
    image: redis:7-alpine
    user: "999:999"
    read_only: true
    tmpfs: [/data:rw,noexec,nosuid]
    cap_drop: [ALL]
    security_opt: [no-new-privileges:true]
    networks:
      - backend
    command: redis-server --requirepass "$(cat /run/secrets/redis_password)"
    secrets: [redis_password]
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "$(cat /run/secrets/redis_password)", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

secrets:
  db_url:
    file: ./secrets/db_url.txt
  redis_url:
    file: ./secrets/redis_url.txt
  pg_password:
    file: ./secrets/pg_password.txt
  redis_password:
    file: ./secrets/redis_password.txt
```

---

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
