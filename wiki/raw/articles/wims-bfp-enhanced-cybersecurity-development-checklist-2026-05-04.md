# WIMS-BFP — Enhanced Cybersecurity Development Checklist

> **Source:** User-provided advanced cybersecurity development checklist
> **Captured:** 2026-05-04
> **Purpose:** Advanced technical controls for cybersecurity-focused systems — demonstrates security-by-design, not end-point hardening
> **Type:** Checklist / technical controls guide

---

## Overview

This expanded checklist adds deeper technical safeguards for cybersecurity-focused systems. Not every item is required for every project — controls should be selected based on system scope, risk level, user needs, and approved research objectives.

The goal is to demonstrate that cybersecurity principles were considered during development — not added only at the end.

---

## A. Identity, Authentication, and Account Security

### Login Protection

- [ ] Secure login page is implemented.
- [ ] Login attempts are rate-limited.
- [ ] Account lockout is triggered after repeated failed attempts.
- [ ] Cooldown period is applied after lockout.
- [ ] Generic error messages are used (no username enumeration).
- [ ] Last login date/time is displayed when appropriate.

### Multi-Factor Authentication (MFA)

- [ ] One-Time Password (OTP) is implemented for sensitive actions or login.
- [ ] OTP has expiration time.
- [ ] OTP can be used only once.
- [ ] OTP retry attempts are limited.
- [ ] Backup recovery method is available.

### Verification Controls

- [ ] Email verification is required during registration.
- [ ] Password reset uses secure tokenized links.
- [ ] Verification links expire after a defined period.
- [ ] Email change requires reconfirmation.

### Password Security

- [ ] Strong password policy is enforced.
- [ ] Minimum password length is defined.
- [ ] Password complexity rules are implemented.
- [ ] Password strength meter is displayed during registration/change.
- [ ] Common or breached passwords are blocked when possible.
- [ ] Password history prevents reuse when applicable.
- [ ] Passwords are hashed securely (e.g., bcrypt, Argon2, PBKDF2).
- [ ] Password reset requires identity verification.

---

## B. Bot Protection and Abuse Prevention

- [ ] CAPTCHA is enabled for login, registration, or suspicious activity.
- [ ] CAPTCHA appears after repeated failed attempts.
- [ ] Rate limiting is enabled for APIs and forms.
- [ ] Anti-spam validation is implemented.
- [ ] Automated bulk requests are detected or blocked.
- [ ] Temporary IP throttling is enabled for abuse patterns.

---

## C. Zero Trust Security Controls

> Never trust automatically. Always verify access requests.

### Continuous Verification

- [ ] Every sensitive action requires authentication or re-authentication.
- [ ] Viewing confidential records may require password re-entry or MFA.
- [ ] Editing critical records requires elevated verification.
- [ ] Session validity is checked continuously.

### Least Privilege Access

- [ ] Users access only data needed for their role.
- [ ] Admin features are hidden from standard users.
- [ ] Role changes are logged and controlled.
- [ ] Temporary privileges expire automatically when possible.

### Device and Network Trust

- [ ] Only approved devices can access sensitive modules (if applicable).
- [ ] IP allowlisting is implemented for admin access when applicable.
- [ ] New device login triggers verification alert.
- [ ] Suspicious locations trigger additional verification.

---

## D. Session and Token Security

- [ ] Secure session management is implemented.
- [ ] Session timeout after inactivity is enabled.
- [ ] Logout invalidates active session tokens.
- [ ] Concurrent session control is considered.
- [ ] Session hijacking protections are implemented.
- [ ] Cookies use HttpOnly flag.
- [ ] Cookies use Secure flag over HTTPS.
- [ ] SameSite cookie policy is configured.
- [ ] JWT or tokens have expiration and rotation when used.

---

## E. Input Security and Secure Coding

- [ ] Server-side validation is implemented.
- [ ] Client-side validation is supplemental only.
- [ ] Parameterized queries / ORM used to prevent SQL injection.
- [ ] Output encoding prevents XSS.
- [ ] CSRF protection is implemented for state-changing requests.
- [ ] File upload type validation is enforced.
- [ ] File size limits are defined.
- [ ] Dangerous file extensions are blocked.
- [ ] Uploaded files stored outside executable directories.
- [ ] Error messages do not expose stack traces or secrets.

---

## F. Data Protection and Privacy Controls

- [ ] HTTPS/TLS is enforced.
- [ ] HSTS is enabled when deployed publicly.
- [ ] Sensitive fields are encrypted at rest when appropriate.
- [ ] Secrets/API keys are stored in environment variables.
- [ ] Backups are encrypted when necessary.
- [ ] Personal data masking is used in logs or screens.
- [ ] Downloaded reports follow access restrictions.
- [ ] Data export actions are logged.

---

## G. Logging, Monitoring, and Forensics

- [ ] Successful and failed login attempts are logged.
- [ ] Critical record changes are logged.
- [ ] Admin actions are logged.
- [ ] Timestamp and user identity are included in logs.
- [ ] Logs are protected from unauthorized editing.
- [ ] Alerting exists for suspicious activity.
- [ ] Repeated failed logins trigger alerts.
- [ ] Logs support incident investigation.

---

## H. Availability and Resilience

- [ ] Input spikes do not crash the system easily.
- [ ] Load testing has been performed.
- [ ] Retry logic exists for temporary failures.
- [ ] Database backup and restore tested.
- [ ] Graceful error handling is implemented.
- [ ] Offline mode exists if part of objectives.
- [ ] Sync conflict handling is considered.
- [ ] Redundancy or fallback process exists when applicable.

---

## I. API and Integration Security

- [ ] APIs require authentication.
- [ ] API authorization checks are enforced.
- [ ] Rate limiting applied to API endpoints.
- [ ] CORS is configured securely.
- [ ] API responses avoid excessive data exposure.
- [ ] Webhooks are signed or verified when used.
- [ ] Third-party integrations are reviewed for permissions.

---

## J. Admin and High-Risk Features

- [ ] Admin panel uses stronger authentication.
- [ ] Sensitive settings changes require confirmation.
- [ ] User deletion or privilege changes are logged.
- [ ] Bulk actions require confirmation prompts.
- [ ] Critical actions use dual confirmation when possible.

---

## K. Security Testing Readiness

- [ ] Test cases exist for authentication bypass.
- [ ] Test cases exist for SQL injection.
- [ ] Test cases exist for access control flaws.
- [ ] Test cases exist for log tampering.
- [ ] Test cases exist for data exposure.
- [ ] Test cases exist for uptime/load conditions.
- [ ] Remediation steps are documented after findings.

---

## L. Cybersecurity Design Mindset Reminders

- [ ] Default deny, then grant access intentionally.
- [ ] Verify every request.
- [ ] Minimize collected data.
- [ ] Log important actions.
- [ ] Encrypt sensitive data.
- [ ] Assume misuse is possible.
- [ ] Build for recovery, not only prevention.
- [ ] Security decisions are documented in the research paper.

---

## WIMS-BFP Implementation Alignment

| Section | WIMS-BFP Implementation | Relevant Standards |
|---------|------------------------|------------------|
| A. Identity/Auth | Keycloak RBAC + MFA, account lockout, JWT short-lived tokens | OWASP ASVS, NIST SP 800-63B |
| B. Bot Protection | Rate limiting on auth endpoints, CAPTCHA on forms | OWASP Top 10 |
| C. Zero Trust | RLS enforcement, least-privilege roles, session re-verification | NIST SP 800-207 |
| D. Session/Token | HttpOnly + Secure + SameSite cookies, JWT refresh rotation | OWASP ASVS |
| E. Input Security | Parameterized queries via SQLAlchemy, server-side validation, XSS encoding | OWASP Top 10, CWE 89/79 |
| F. Data Protection | AES-256-GCM for PII, HTTPS/TLS enforced, env vars for secrets | ISO 27001, OWASP ASVS |
| G. Logging | Audit log helpers, immutable logs, login attempt logging | NIST SP 800-115, ISO 27001 |
| H. Availability | Uptime load testing (JMeter), offline PWA, recovery procedures | ISO 25010, NIST CSF |
| I. API Security | Keycloak token-gated FastAPI endpoints, CORS config | OWASP API Security Top 10 |
| J. Admin Features | Separate admin auth, dual confirmation for bulk operations | OWASP ASVS |
| K. Security Testing | AUTH-001 through AVAIL-001 test cases | [[raw/articles/wims-bfp-security-testing-evaluation-questionnaire-2026-05-04]] |
| L. Design Mindset | Security decisions documented in Ch3 + Ch4 | [[raw/articles/wims-bfp-ethical-security-testing-guide-2026-05-04]] |

See also: [[raw/articles/wims-bfp-system-development-compliance-checklist-2026-05-04]] (compliance-focused) and [[raw/articles/wims-bfp-secure-coding-deployment-checklist-2026-05-04]] (code + deployment hardening).
