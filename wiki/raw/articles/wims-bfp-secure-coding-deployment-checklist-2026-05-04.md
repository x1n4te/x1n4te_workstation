# WIMS-BFP — Secure Coding and Secure Deployment Checklist

> **Source:** User-provided secure coding and deployment hardening checklist
> **Captured:** 2026-05-04
> **Purpose:** Ensure system is securely built and safely deployed — code-level protections and deployment hardening for web/cloud/VM environments
> **Type:** Checklist / deployment guide

---

## Overview

This guide ensures the system is not only functional but also securely built and safely deployed. It complements the development compliance checklist by focusing on code-level protections and deployment hardening.

---

## A. Secure Coding Practices (During Development)

### Input Handling and Validation

- [ ] All inputs are validated on the server side.
- [ ] Data types, length, and format are enforced.
- [ ] Parameterized queries or ORM are used (no raw SQL concatenation).
- [ ] Output encoding is applied to prevent XSS.
- [ ] CSRF protection tokens are implemented.
- [ ] File uploads are validated (type, size, content).

### Authentication and Authorization Logic

- [ ] Authentication logic is centralized and not duplicated.
- [ ] Authorization checks are enforced on every protected endpoint.
- [ ] Role-based access control is implemented correctly.
- [ ] No direct object access without permission checks (prevent IDOR).
- [ ] Sensitive operations require re-authentication or verification.

### Secrets and Credentials Handling

- [ ] No hardcoded passwords, API keys, or tokens in source code.
- [ ] Secrets are stored in environment variables or secret managers.
- [ ] .env or config files are excluded from version control.
- [ ] API keys are restricted by domain/IP when possible.

### Error Handling and Logging

- [ ] System errors do not expose stack traces to users.
- [ ] Logs do not contain sensitive data (passwords, tokens).
- [ ] Debug mode is disabled in production builds.
- [ ] Custom error pages are implemented.

### Dependency and Library Security

- [ ] All libraries and frameworks are updated.
- [ ] Vulnerability scanning of dependencies is performed.
- [ ] Only trusted and maintained packages are used.
- [ ] Unused dependencies are removed.

### Code Quality and Review

- [ ] Code is reviewed by team members or mentor.
- [ ] Secure coding guidelines are followed (OWASP best practices).
- [ ] Static analysis tools are used when possible.
- [ ] Reusable secure components are used (auth, validation, etc.).

---

## B. Secure Deployment (Cloud / VM / Web Server)

### Server and Environment Hardening

- [ ] Default ports and services are reviewed and minimized.
- [ ] Unused services are disabled.
- [ ] Firewall rules are configured (allow only required ports).
- [ ] SSH access is restricted (key-based authentication preferred).
- [ ] Root login is disabled or limited.
- [ ] System packages are updated regularly.

### Web Server Security (Nginx / Apache / IIS)

- [ ] Directory listing is disabled.
- [ ] Security headers are configured:
  - Content-Security-Policy (CSP)
  - X-Frame-Options
  - X-Content-Type-Options
  - Strict-Transport-Security (HSTS)
- [ ] HTTPS is enforced (redirect HTTP → HTTPS).
- [ ] TLS certificates are valid and updated.
- [ ] Only secure TLS versions are enabled.

### Application Deployment Security

- [ ] Production build is used (not development mode).
- [ ] Debugging features are disabled.
- [ ] Environment variables are configured securely.
- [ ] API endpoints are protected (authentication required).
- [ ] Rate limiting is applied where needed.

### Database Security

- [ ] Database is not publicly exposed (private network if possible).
- [ ] Strong credentials are used.
- [ ] Least privilege principle applied to database users.
- [ ] Database backups are secured and encrypted.
- [ ] Default database ports are restricted.

---

### Cloud Security (AWS / Azure / GCP / VM)

#### Access Control

- [ ] IAM roles and permissions follow least privilege.
- [ ] Admin access is limited and monitored.
- [ ] Multi-factor authentication (MFA) is enabled for cloud accounts.

#### Network Security

- [ ] Security groups/firewall rules restrict inbound/outbound traffic.
- [ ] Only required ports (e.g., 443, 80) are open.
- [ ] Private subnets are used for sensitive components.

#### Storage Security

- [ ] Cloud storage buckets are not publicly accessible unless intended.
- [ ] Access policies are properly configured.
- [ ] Sensitive files are encrypted.

#### Monitoring and Logging

- [ ] Server logs are enabled and reviewed.
- [ ] Access logs are recorded (who accessed what and when).
- [ ] Suspicious activity alerts are configured when possible.
- [ ] Failed login attempts are monitored.

#### Backup and Recovery

- [ ] Regular backups are configured.
- [ ] Backup restoration is tested.
- [ ] Disaster recovery plan is defined (basic level acceptable for capstone).

---

## C. Deployment Testing Before Release

- [ ] Test system using production-like environment.
- [ ] Validate HTTPS and domain configuration.
- [ ] Re-run security test cases after deployment.
- [ ] Check for exposed endpoints or misconfigurations.
- [ ] Verify logs are working correctly.
- [ ] Confirm no sensitive data is exposed in UI or API.

---

## D. Common Deployment Mistakes to Avoid

- Leaving debug mode ON
- Exposing database to public internet
- Using default credentials
- Hardcoding API keys
- Forgetting HTTPS
- Leaving open ports unnecessarily
- Uploading .env files publicly
- Not restricting admin access
- Ignoring logs and monitoring

---

## E. Sample Chapter 3 Statement

> The system was developed following secure coding practices and deployed in a controlled server environment with appropriate security configurations. Measures such as input validation, secure authentication, encrypted communication, restricted access controls, and server hardening were implemented to ensure the confidentiality, integrity, and availability of the system.

---

## Final Principle

> Secure coding protects the system during development.
> Secure deployment protects the system in real-world operation.
> Both must be present to claim a secure system.

---

## WIMS-BFP Implementation Alignment

| Section | WIMS-BFP Implementation | Relevant Files |
|---------|------------------------|---------------|
| A. Input Handling | SQLAlchemy ORM (parameterized), Pydantic validation, CSRF tokens | FastAPI `routers/`, `schemas/` |
| A. Auth/AuthZ | Keycloak JWT-gated endpoints, RBAC enforcement | `lib/auth.ts`, `backend/app/api/` |
| A. Secrets | `.env` excluded from git, `KEYCLOAK_ADMIN_PASSWORD` in env vars | `docker-compose.yml`, `.gitignore` |
| A. Error Handling | Custom exception handlers, stack traces not exposed | FastAPI `main.py` |
| A. Dependencies | `pip audit`, `npm audit`, `ruff` linting | CI pipeline (`pyproject.toml`, `package.json`) |
| B. Server Hardening | Docker containers isolated, non-root users, minimal base images | `Dockerfile` per service |
| B. Nginx | CSP, HSTS, X-Frame-Options headers | `nginx.conf` |
| B. HTTPS | Let's Encrypt or self-signed for dev, redirect HTTP→HTTPS | Nginx config |
| B. Database | PostgreSQL on private network, RLS enforced, strong passwords | `docker-compose.yml`, `init-scripts/` |
| C. Cloud/VM | Keycloak, FastAPI, Next.js in Docker Compose, no public DB | `docker-compose.yml` |
| C. IAM | Keycloak roles mapped to RBAC, least-privilege | `backend/app/core/roles.py` |
| C. Monitoring | Health dashboard endpoints, Redis health, Celery monitoring | `backend/app/api/routes/health.py` |
| C. Backups | Database backup scripts, encrypted backups | `scripts/backup/` |
| C. Deployment Testing | Security test cases re-run post-deploy | [[raw/articles/wims-bfp-security-testing-evaluation-questionnaire-2026-05-04]] |
| D. Mistakes | .env not committed, debug=False in production | `docker-compose.yml`, CI env vars |

Companion checklists: [[raw/articles/wims-bfp-system-development-compliance-checklist-2026-05-04]] (general compliance) and [[raw/articles/wims-bfp-enhanced-cybersecurity-development-checklist-2026-05-04]] (advanced technical controls).
