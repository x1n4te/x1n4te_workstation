## Module 10: Compliance and Data Privacy

### A. Data Privacy Act (RA 10173) Compliance

1. System shall implement data minimization principle
    - Collect only necessary data for fire incident reporting
    - Do not collect Sensitive Personal Information (SPI) unless operationally required
2. System shall provide purpose limitation
    - Incident data used only for fire suppression operations and national statistics
    - Secondary use of data is strictly prohibited without explicit consent
3. System shall support individual rights
    - **Right to access:** Users can request copy of their submitted incidents
    - **Right to rectification:** Users can request correction of inaccurate data
    - **Right to erasure:** Users can request deletion (soft delete with audit trail)

### B. Cloud-Based Data Protection Impact Assessment (DPIA)

1. System shall maintain DPIA documentation covering:
    - Description of data processing activities within the Docker/VPS environment.
    - Identified privacy risks (e.g., cloud-based data exposure) and mitigation measures.
    - Legal basis for processing (public interest / official authority)
    - Data retention periods
2. DPIA shall be reviewed annually or whenever major infrastructure changes occur.

### C. Records of Processing Activities (RoPA)

1. System shall maintain RoPA documenting:
    - Categories of data subjects (Regional Encoders, Validators, Analysts, Administrators, Citizens)
    - Categories of personal data (names, user IDs, email addresses, login timestamps)
    - Purposes of processing (incident reporting, access control, audit logging)
    - Data retention periods (active records: indefinite; audit logs: 7 years)
    - Security measures (encryption, access control, audit logging)
2. RoPA shall be accessible to System Administrator and Data Protection Officer

### D. Breach Notification

1. In the event of data breach, system shall:
    - Automatically generate breach notification report
    - Include details: date/time of breach, affected data categories, estimated number of affected records
    - Notify Data Protection Officer and System Administrator immediately
2. System Administrator shall assess breach severity and determine if National Privacy Commission (NPC) notification is required (within 72 hours if confirmed)