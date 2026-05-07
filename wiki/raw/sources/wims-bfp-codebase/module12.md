## Module 12: User Management and Administration

### A. User Onboarding

1. System Administrator can create new user accounts — `python-keycloak (Admin Client)`
2. Required user information:
    - Full name
    - Email address (serves as username)
    - Role assignment (Encoder, Validator, Analyst, Administrator, Citizen)
    - Contact number (optional)
3. System shall auto-generate temporary password and send via secure email — `Keycloak "Execute Actions"`
4. User must change password upon first login — `Required Action: Update Password`

### B. User Profile Management

1. Users can view and update their own profile information: — `Keycloak Account API`
    - Full name
    - Email address
    - Contact number
2. Users cannot modify their own role assignment (only System Administrator can) — `Keycloak Token Claims`

### C. User Deactivation and Deletion

1. System Administrator can deactivate user accounts (soft delete) — `Keycloak enabled: false`
2. Deactivated accounts:
    - Cannot log in
    - Remain in database for audit purposes
    - Can be reactivated by System Administrator
3. Hard deletion of user accounts is not allowed (to preserve audit trail integrity) — `PostgreSQL Foreign Keys`
