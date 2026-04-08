---
id: keycloak-production-security-2026-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - keycloak.org/server/configuration-production
  - documentation.cloud-iam.com/resources/keycloak-best-practices-guide.html
  - hoop.dev/blog/keycloak-production-environment-best-practices-for-high-availability-security-and-scalability
status: active
tags:
  - keycloak
  - authentication
  - security
  - production
  - software-dev
related:
  - sources/software-dev/fastapi-keycloak-jwt-rbac
  - concepts/keycloak-fastapi-security-wims-bfp
  - sources/cybersecurity/keycloak-cves-2026
  - concepts/secure-coding-practices
  - mocs/cybersecurity
---

# Keycloak Production Security Hardening (Source Summary)

**Sources:** Keycloak Official Docs, Cloud-IAM, Hoop.dev
**Type:** Identity provider hardening guide
**Confidence:** High — official Keycloak docs + vendor best practices

---

## 8 Hardening Priorities

| Priority | Action | Effort |
|---|---|---|
| 🔴 High | Secure admin accounts | Quick win |
| 🔴 High | Strong password policy for admins | Quick win |
| 🔴 High | Activate MFA for admins | Quick win |
| 🔴 High | Brute force detection | Quick win |
| 🔴 High | Restrict admin access by IP | Quick win |
| 🟠 Medium | Monitor logs & security events | Setup required |
| 🟠 Medium | Configure SMTP | Setup required |
| 🟠 Medium | Password blacklist | Quick win |

---

## 1. Admin Account Security

### Master Realm Hardening

```bash
# Keycloak startup flags for production
bin/kc.sh start \
  --https-port=8443 \
  --https-certificate-file=/path/to/cert.pem \
  --https-certificate-key-file=/path/to/key.pem \
  --hostname=keycloak.example.com \
  --hostname-admin=admin.keycloak.example.com  # Separate admin hostname
```

### Admin Configuration Checklist

```
[ ] Change default admin password immediately
[ ] Enable MFA (TOTP) for admin accounts
[ ] Apply password policy: min 12 chars, special chars, numbers, uppercase
[ ] Enable password blacklist (top 10K breached passwords)
[ ] Enable brute force detection on master realm
[ ] Restrict admin console access by IP (allowlist)
[ ] Separate admin hostname from user-facing endpoints
[ ] Disable admin account creation via REST API
```

---

## 2. TLS Configuration

```
[ ] HTTPS on all Keycloak endpoints
[ ] TLS on database connection (Keycloak → PostgreSQL)
[ ] TLS on cache communication (JGroups clustering)
[ ] TLS on reverse proxy → Keycloak
[ ] Certificates auto-renewed (Let's Encrypt or internal CA)
```

---

## 3. Brute Force Detection

| Setting | Value | Purpose |
|---|---|---|
| Enabled | true | Activate protection |
| Permanent lockout | false | Temporary lockout (not permanent) |
| Max login failures | 5 | Lock after 5 failed attempts |
| Wait increment | 30 seconds | Cooldown between failures |
| Max wait | 15 minutes | Maximum lockout duration |
| Failure reset time | 12 hours | Reset failure count after |

**WIMS-BFP Config:**
- Master realm: Brute force ON, 5 failures → 15min lockout
- Application realm: Brute force ON, 10 failures → 30min lockout (higher tolerance for civilian users)

---

## 4. Session & Token Settings

| Setting | Production Value | Purpose |
|---|---|---|
| Access Token Lifespan | 5-15 minutes | Short-lived tokens |
| SSO Session Idle | 30 minutes | Auto-logout after inactivity |
| SSO Session Max | 8 hours | Force re-auth after 8 hours |
| Refresh Token Max Reuse | 0 | Single-use refresh tokens |
| Client Session Idle | 15 minutes | Client session timeout |
| Client Session Max | 1 hour | Maximum client session |

---

## 5. Password Policy (Recommended)

```
[ ] Minimum length: 12 characters
[ ] Maximum length: 128 characters
[ ] Special characters: required
[ ] Digits: required
[ ] Uppercase characters: required
[ ] Not username: not allowed
[ ] Password blacklist: enabled (top 10K)
[ ] Hashing iterations: 27,500+ (PBKDF2)
```

---

## 6. Network & Deployment

### Architecture

```
Internet
  → Reverse Proxy (TLS termination)
    → Keycloak (HTTPS, non-public ports)
      → PostgreSQL (TLS, internal network)
      → Redis (internal network, no internet)
```

### Keycloak Cluster (High Availability)

```
[ ] Multiple Keycloak instances behind load balancer
[ ] External database (PostgreSQL 16)
[ ] Distributed cache (Infinispan/JGroups) for session replication
[ ] Health checks on all nodes
[ ] Auto-scaling based on auth request volume
```

### Resource Limits

```yaml
# docker-compose.yml
services:
  keycloak:
    deploy:
      resources:
        limits: {cpus: '2.0', memory: 2G}
        reservations: {cpus: '0.5', memory: 512M}
```

---

## 7. Monitoring & Logging

```
[ ] Enable login events
[ ] Enable admin events
[ ] Configure event listeners: jboss-logging, email
[ ] Set up log forwarding to SIEM
[ ] Monitor: failed logins, brute force detections, admin actions
[ ] Alert on: >100 failed logins/hour, admin account lockout
```

---

## 8. SMTP Configuration

```
[ ] Configure SMTP for Keycloak (password resets, login alerts)
[ ] Test: send verification email from Keycloak admin
[ ] Alert on suspicious login from new device/location
```

---

## WIMS-BFP Keycloak Configuration

| Setting | WIMS-BFP Value | Rationale |
|---|---|---|
| Access Token Lifespan | 10 minutes | Short-lived JWT for API calls |
| SSO Session Idle | 30 minutes | Balanced for active users |
| SSO Session Max | 8 hours | Workday-length sessions |
| Brute Force Max Failures | 5 (master), 10 (app) | Tighter for admins |
| MFA | TOTP required for all users | FRS mandates MFA |
| Password Policy | 12+ chars, special, digits, uppercase | CIS benchmark |
| Admin IP Restriction | Localhost + VPN only | Minimize attack surface |

---

## Related Pages

- [[sources/software-dev/fastapi-keycloak-jwt-rbac]] — FastAPI + Keycloak JWT integration
- [[concepts/keycloak-fastapi-security-wims-bfp]] — WIMS-BFP security synthesis
- [[sources/cybersecurity/keycloak-cves-2026]] — Keycloak CVEs
- [[mocs/cybersecurity]] — Cybersecurity Map of Content
