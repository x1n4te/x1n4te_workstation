---
id: docker-security-best-practices-2026-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - zeonedge.com/en/blog/docker-security-best-practices-2026-hardening-containers-build-runtime
  - sysdig.com/learn-cloud-native/container-security-best-practices
status: active
tags:
  - docker
  - container-security
  - devops
  - software-dev
related:
  - sources/software-dev/docker-cves-2025-2026
  - sources/software-dev/docker-compose-security
  - concepts/docker-security-wims-bfp
  - concepts/secure-coding-practices
  - mocs/cybersecurity
---

# Docker Security Best Practices — 2026 (Source Summary)

**Sources:** ZeonEdge, Sysdig
**Type:** Container security reference
**Confidence:** High — industry best practices, data-driven (2025 container incidents up 47% YoY)

---

## 5 Security Layers

| Layer | Focus | Key Controls |
|---|---|---|
| **Image** | What you build FROM | Alpine/distroless base, image scanning, SBOM, digests |
| **Build** | How you build | Multi-stage, non-root, .dockerignore, no secrets in layers |
| **Runtime** | How containers run | Read-only filesystem, capabilities, resource limits, seccomp |
| **Network** | How containers communicate | Network isolation, internal-only networks, no published ports |
| **Secrets** | How secrets are managed | File-based secrets, external vaults, no env vars |

---

## Image Security

### Base Image Selection

| Image | Size | Best For | Attack Surface |
|---|---|---|---|
| Alpine Linux | 5MB | Go, Node.js | Minimal (musl libc) |
| Google Distroless | 2-15MB | Production Java, Python, Go | Very minimal (no shell) |
| Chainguard Images | Varies | Regulated environments | Hardened, FIPS-compliant, daily SBOM |
| Ubuntu/Debian | 75-125MB | Only if necessary | Large (use multi-stage) |

### Image Scanning

```bash
# Scan for critical/high vulnerabilities and fail CI
trivy image --exit-code 1 --severity CRITICAL,HIGH myapp:v1.2.3

# Generate SBOM (Software Bill of Materials)
trivy image --format spdx-json --output sbom.json myapp:v1.2.3
```

### Image Digest (Immutable)

```dockerfile
# ❌ BAD: tag is mutable (can be overwritten)
FROM nginx:latest

# ✅ GOOD: digest is immutable
FROM nginx@sha256:6db391d1c0cfb30588ba0bf72ea999404f2764e...
```

---

## Build Hardening

### Multi-Stage Builds

```dockerfile
# Python example: Build with full deps, run with minimal
FROM python:3.12-slim AS builder
RUN pip install --user -r requirements.txt

FROM python:3.12-slim AS runtime
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app
USER nonroot:nonroot
# Result: smaller image, no build tools, no shell
```

### Never Run as Root

```dockerfile
RUN groupadd --system --gid 1001 appgroup && \
    useradd --system --uid 1001 --gid appgroup appuser
COPY --chown=appuser:appgroup . /app
USER appuser
```

### Read-Only Filesystem

```yaml
services:
  app:
    read_only: true
    tmpfs: [/tmp:rw,noexec,nosuid]
    cap_drop: [ALL]
    cap_add: [NET_BIND_SERVICE]
    security_opt: [no-new-privileges:true]
```

### .dockerignore

```
.git
.env
*.key
*.pem
node_modules
__pycache__
*.pyc
docker-compose*.yml
```

---

## Runtime Security

### Resource Limits

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
    ulimits:
      nproc: 100
      nofile: {soft: 1024, hard: 2048}
```

### Network Isolation

```yaml
networks:
  frontend-net: {driver: bridge}
  backend-net: {driver: bridge, internal: true}  # No internet access

services:
  frontend:
    networks: [frontend-net]
  backend:
    networks: [frontend-net, backend-net]
  database:
    networks: [backend-net]  # Only accessible from backend
```

### Docker Socket Protection

```yaml
# ❌ NEVER mount docker socket directly
# volumes: ["/var/run/docker.sock:/var/run/docker.sock"]

# ✅ Use socket proxy that restricts API access
services:
  socket-proxy:
    image: tecnativa/docker-socket-proxy
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    environment:
      CONTAINERS: 1
      IMAGES: 0
      EXEC: 0
      VOLUMES: 0
      POST: 0
```

---

## Secrets Management

### ❌ Never Use Environment Variables for Secrets

```yaml
# BAD: visible in docker inspect, process listing, crash dumps
environment:
  DB_PASSWORD=supersecret123
```

### ✅ Use Docker Secrets (File-Based)

```yaml
services:
  app:
    secrets: [db_password]
    environment:
      DB_PASSWORD_FILE: /run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

---

## WIMS-BFP Audit Checklist

```
[ ] Base images use Alpine or distroless
[ ] Multi-stage builds for all services
[ ] All containers run as non-root user
[ ] Read-only filesystem where possible
[ ] cap_drop: ALL, cap_add only what's needed
[ ] no-new-privileges: true on all services
[ ] Network isolation (internal networks for DB/Redis)
[ ] Resource limits on all services
[ ] Secrets via files, not env vars
[ ] Docker socket NOT mounted in any container
[ ] .dockerignore excludes .env, *.key, *.pem
[ ] Image scanning in CI/CD pipeline
```

---

## Related Pages

- [[sources/software-dev/docker-cves-2025-2026]] — Docker/runc CVEs
- [[sources/software-dev/docker-compose-security]] — PostgreSQL/Redis Docker Compose hardening
- [[concepts/docker-security-wims-bfp]] — WIMS-BFP Docker security synthesis
- [[mocs/cybersecurity]] — Cybersecurity Map of Content
