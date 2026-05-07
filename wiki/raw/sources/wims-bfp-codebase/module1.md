## Module 1: Authentication and Access Control

### A. User Authentication

1. Login with username and password (minimum 8 characters, including uppercase, lowercase, digit, and special character) — `Keycloak (Browser Flow)`
2. Multi-Factor Authentication (MFA) required for System Administrators and National Validators — `Keycloak Built-in OTP Policy`
    - MFA via Time-Based One-Time Password (TOTP) using authenticator app
    - Option to remember trusted device for 7 days
3. Account lockout after 5 consecutive failed login attempts — `Keycloak Brute Force Detection`
4. Automatic session timeout after 30 minutes of inactivity — `Keycloak SSO Session Idle`

### B. Password Management

1. Reset password via secure email link with one-time token (expires after 15 minutes) — `Keycloak "Forgot Password" Flow`
2. Change password for authenticated users — `Keycloak Account Console`
    - Requires current password verification
    - Sends email notification upon successful password change
3. Enforce strong password policy — `Keycloak Password Policies`
    - Minimum 8 characters
    - Must include uppercase letter, lowercase letter, digit, and special character
    - Password cannot match previous 3 passwords
    - Password expiry set to 90 days for administrative roles

### C. Role-Based Access Control (RBAC)

1. System shall support five (5) distinct user roles: — `Keycloak Realm Roles`
    - **Regional Encoder:** Can create, edit, and upload incident records via the Regional Web Portal; resolve duplicates; access offline mode
    - **National Validator:** Can review and approve incident records; flag inconsistencies; no creation rights
    - **National Analyst:** Read-only access to aggregated data, statistical trends, and reports; cannot modify records
    - **System Administrator:** Full system access including user management, security monitoring, audit log review, and XAI threat analysis
    - **Citizen:** Can submit preliminary crowdsourced fire reports and securely view anonymized public heatmaps.
2. Access permissions enforced through Keycloak Identity Provider — `Python Keycloak + FastAPI Dependencies`
3. Least privilege principle applied – users can only access functions required for their role — `React Guard Components`
4. Role assignment and modification restricted to System Administrators — `Keycloak Admin Console`

### D. Session Management

1. Generate secure session token upon successful authentication — `OIDC (OpenID Connect)`
2. Session token stored securely in browser (httpOnly, secure, sameSite flags) — `Browser Cookies / Memory`
3. Automatic session renewal on user activity (up to maximum session lifetime of 8 hours) — `Keycloak Refresh Token`
4. Force logout on password change or role modification — `Backchannel Logout`
5. Support concurrent session detection with option to terminate previous session — `Keycloak User Sessions`