---
id: docker-cves-2025-2026-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-04-15
stale_after: 2026-04-29
confidence: high
source_refs:
  - cncf.io/blog/2025/11/28/runc-container-breakout-vulnerabilities-a-technical-overview/
  - sysdig.com/blog/runc-container-escape-vulnerabilities
  - bleepingcomputer.com/news/security/dangerous-runc-flaws-could-allow-hackers-to-escape-docker-containers
  - nvd.nist.gov/vuln/detail/CVE-2026-28400
status: active
tags:
  - docker
  - runc
  - cve
  - container-escape
  - vulnerability
  - software-dev
related:
  - sources/software-dev/docker-security-best-practices
  - sources/software-dev/docker-compose-security
  - concepts/docker-security-wims-bfp
  - mocs/cybersecurity
---

# Docker/runc CVEs — 2025-2026 (Source Summary)

**Sources:** CNCF, Sysdig, BleepingComputer, NVD
**Technology:** Docker, runc (container runtime)
**Confidence:** High — CNCF official + active exploitation research

---

## CVE-2025-31133 — Container Escape via Masked Path Abuse (CRITICAL)

**Affected:** runc <1.4.0-rc.3, <1.3.3, <1.2.8
**CVSS:** 7.3
**Type:** Container escape (full host access)

**Description:** Race condition in runc's masked path implementation. An attacker replaces `/dev/null` with a symlink to a sensitive procfs file (e.g., `/proc/sys/kernel/core_pattern`). Runc then bind-mounts the target **read-write**, enabling container escape and host compromise.

**Attack vector:** Crafted `RUN --mount=...` instruction in Dockerfile → malicious image → container escape when built/run.

**Impact:** Full root access to the host system. In multi-tenant environments, one compromised container = full cluster compromise.

**Patch:** Upgrade runc to v1.4.0-rc.3, v1.3.3, or v1.2.8

---

## CVE-2025-52565 — Container Escape via /dev/console Mount Races (CRITICAL)

**Affected:** runc <1.4.0-rc.3, <1.3.3, <1.2.8
**CVSS:** 7.3
**Type:** Container escape (full host access)

**Description:** Similar flaw involving `/dev/console` bind-mounts. Attacker replaces `/dev/pts/$n` with a symlink, causing runc to bind-mount the symlink target over `/dev/console`, granting read-write access to sensitive procfs files.

**Patch:** Upgrade runc to v1.4.0-rc.3, v1.3.3, or v1.2.8

---

## CVE-2025-52881 — Arbitrary Write via procfs Redirects (CRITICAL)

**Affected:** runc <1.4.0-rc.3, <1.3.3, <1.2.8
**CVSS:** 7.3
**Type:** Container escape (full host access)

**Description:** Most sophisticated attack — **bypasses Linux Security Module (LSM) checks**. Makes `/proc/self/attr/<label>` reference a real procfs file, redirecting writes to malicious targets like `/proc/sysrq-trigger` (host crash) or `/proc/sys/kernel/core_pattern` (full breakout).

**Patch:** Upgrade runc to v1.4.0-rc.3, v1.3.3, or v1.2.8

---

## CVE-2026-28400 — Docker Model Runner Container Escape

**Affected:** Docker Model Runner <1.0.16
**Type:** Container escape

**Description:** Vulnerability in Docker Model Runner allowing container escape. Fixed in Docker Model Runner 1.0.16. Docker Desktop users should update to 4.61.0 or later.

**Patch:** Update Docker Desktop to ≥4.61.0

---

## Exploitation Context

| Factor | Risk Level |
|---|---|
| Multi-tenant environments (users define own containers) | **CRITICAL** |
| Untrusted/vetted images can be introduced | **CRITICAL** |
| Hardened image set + CI/CD security controls | **LOW** |
| Single-tenant, controlled images | **LOW** |

---

## WIMS-BFP Mitigation

```
[ ] Check runc version: runc --version
[ ] Upgrade runc to v1.3.3+ or v1.4.0-rc.3+
[ ] Verify Docker Desktop version: docker --version
[ ] Use only hardened base images (Alpine, distroless)
[ ] Scan images in CI/CD: trivy image --exit-code 1 --severity CRITICAL
[ ] Never run containers from untrusted images
[ ] Monitor: https://github.com/opencontainers/runc/security/advisories
```

---

## Related Pages

- [[sources/software-dev/docker-security-best-practices]] — Docker security reference
- [[sources/software-dev/docker-compose-security]] — PostgreSQL/Redis Docker Compose hardening
- [[concepts/docker-security-wims-bfp]] — WIMS-BFP Docker security synthesis
- [[mocs/cybersecurity]] — Cybersecurity Map of Content
