---
source_url: https://github.com/x1n4te/WIMS-BFP-PROTOTYPE (internal FRS document)
ingested: 2026-05-04
sha256: 35ae4c1b91697d35b02cedd19d1a9ed8d1659211063428dbcd9b0415eee91ef5
---
# WIMS-BFP — Functional Requirements Specification
## Module Index (Updated 2026-05-04)

> This document supersedes the original Module 5d and adds Modules 14 and 15.
> All module descriptions use the FRS standard format.

---

## Module Index

| ID | Module Name | Status |
|----|-------------|--------|
| 1 | Authentication and Access Control | Implemented |
| 2 | Offline-First Incident Management | Implemented |
| 3 | Conflict Detection and Manual Verification | Implemented |
| 4 | Data Commit and Immutable Storage | Implemented |
| 5 | Analytics and Reporting | Implemented |
| 5d | Public Anonymous Incident Submission | REVISED |
| 6 | Cryptographic Security | Implemented |
| 7 | Intrusion Detection and Network Monitoring | Implemented |
| 8 | Threat Detection with Explanation AI (XAI) | Implemented |
| 9 | System Monitoring and Health Dashboard | Implemented |
| 10 | Compliance and Data Privacy | Implemented |
| 11 | Penetration Testing and Security Validation | Procedure |
| 12 | User Management and Administration | Implemented |
| 13 | Notification System | DEFERRED |
| 14 | Public Anonymous Incident Submission | NEW |
| 15 | Reference Data Service | NEW |

---

## Module 1: Authentication and Access Control

a. User Authentication

   i.   The system shall allow users to log in using a username and password
        combination meeting the following minimum requirements: minimum eight (8)
        characters, including at least one uppercase letter, one lowercase
        letter, one digit, and one special character, implemented via
        Keycloak Browser Flow.

  ii.   Multi-Factor Authentication (MFA) shall be required for System
        Administrators and National Validators, implemented via Keycloak
        Built-in OTP Policy using a Time-Based One-Time Password (TOTP)
        authenticator application, with an option to remember a trusted
        device for seven (7) days.

 iii.   The system shall enforce account lockout after five (5) consecutive
        failed login attempts, implemented via Keycloak Brute Force Detection.

  iv.   The system shall automatically terminate sessions after thirty (30)
        minutes of inactivity, implemented via Keycloak SSO Session Idle
        timeout.

b. Password Management

   i.   The system shall allow users to reset their password via a secure
        email link containing a one-time token that expires after fifteen
        (15) minutes, implemented via the Keycloak "Forgot Password" flow.

  ii.   Authenticated users shall be permitted to change their password,
        requiring verification of the current password and sending an
        email notification upon successful change, via Keycloak Account
        Console.

 iii.   The system shall enforce a strong password policy via Keycloak
        Password Policies requiring: minimum eight (8) characters; at least
        one uppercase letter, one lowercase letter, one digit, and one
        special character; prohibition against reusing the previous three
        (3) passwords; and a password expiry of ninety (90) days for
        administrative roles.

c. Role-Based Access Control (RBAC)

   i.   The system shall support five (5) distinct user roles, implemented
        via Keycloak Realm Roles:
        (a)  Regional Encoder: Can create, edit, and upload incident
             records via the Regional Web Portal; resolve duplicates;
             access offline mode.
        (b)  National Validator: Can review and approve incident records;
             flag inconsistencies; no record creation rights.
        (c)  National Analyst: Read-only access to aggregated data,
             statistical trends, and reports; cannot modify records.
        (d)  System Administrator: Full system access including user
             management, security monitoring, audit log review, and
             XAI threat analysis.
        (e)  Citizen: Can submit preliminary crowdsourced fire reports
             and securely view anonymized public heatmaps.

  ii.   Access permissions shall be enforced through Keycloak Identity
        Provider using Python Keycloak and FastAPI Dependencies.

 iii.   The principle of least privilege shall be applied — users shall
        only access functions required for their assigned role,
        enforced via React Guard Components.

  iv.   Role assignment and modification shall be restricted exclusively
        to System Administrators via the Keycloak Admin Console.

d. Session Management

   i.   The system shall generate a secure session token upon successful
        authentication using OpenID Connect (OIDC).

  ii.   Session tokens shall be stored securely in the browser with
        httpOnly, secure, and sameSite cookie flags set.

 iii.   The system shall automatically renew sessions on user activity
        up to a maximum session lifetime of eight (8) hours, implemented
        via Keycloak Refresh Token.

  iv.   The system shall force logout upon password change or role
        modification via Keycloak Backchannel Logout.

  v.   The system shall support concurrent session detection with the
        ability to terminate previous sessions, implemented via
        Keycloak User Sessions.

---

## Module 2: Offline-First Incident Management

a. Incident Data Entry

   i.   Regional Encoders shall be able to create new fire incident
        reports containing the following fields, implemented via
        React Hook Form and Zod validation:
        (a)  Incident ID — auto-generated, immutable (UUID v4)
        (b)  Date and time of incident (timestamp)
        (c)  Location — address, municipality, province
        (d)  Incident type — structure fire, vehicular fire,
             grass fire, others
        (e)  Incident narrative — free-text description
        (f)  Casualties — injuries, fatalities
        (g)  Property damage estimate
        (h)  Responders deployed
        (i)  Fire suppression status — ongoing, contained, extinguished

  ii.   The system shall support file attachments including photos,
        reports, and maps with the following constraints:
        (a)  Accepted formats: .jpg, .png, .pdf, .docx
        (b)  Maximum file size: 10 MB per attachment
        (c)  Maximum five (5) attachments per incident
        (d)  Attachments encrypted before storage using Web Crypto API
             (AES-GCM)

 iii.   The incident form shall include client-side validation with
        real-time field-level error messages for required fields:
        Incident ID, date/time, location, incident type, and narrative.

b. Offline Data Capture and Storage

   i.   The system shall automatically detect network availability using
        the Navigator API and React Hook.

  ii.   When offline, incident data shall be stored locally in the
        browser using IndexedDB via Dexie.js wrapper.

 iii.   Offline-captured records shall be encrypted using AES-256-GCM
        before local storage via Web Crypto and ArrayBuffer.

  iv.   The user interface shall display a clear "Offline Mode" indicator
        using Tailwind CSS and toast notifications.

  v.   All CRUD operations — Create, Read, Update, Delete — shall
        function fully in offline mode.

  vi.   Offline storage capacity shall support a minimum of one thousand
        (1,000) incident records with attachments, monitored via the
        StorageManager API.

c. Data Synchronization

   i.   The system shall automatically detect network restoration using
        TanStack Query (React Query).

  ii.   Upon reconnection, the system shall:
        (a)  Upload locally stored incidents to the central server
        (b)  Verify cryptographic integrity of each record via
             AES-256-GCM tag check
        (c)  Detect and resolve conflicts using duplicate incident
             detection
        (d)  Update local database with server response

 iii.   The synchronization process shall be atomic — all-or-nothing
        per incident — using FastAPI transaction.atomic.

  iv.   Failed synchronization attempts shall retry automatically with
        exponential backoff and a maximum of five (5) retries using
        TanStack Query retry.

  v.   Users shall receive notification of synchronization success
        or failure via React Hot Toast.

d. Incident Status Tracking

   i.   The system shall support the following incident statuses
        implemented as a PostgreSQL Enum:
        (a)  Draft: Incomplete record, saved locally, not yet submitted
        (b)  Pending: Submitted for validation, awaiting review
        (c)  Validated: Approved, committed to central database
        (d)  Flagged: Potential duplicate or data integrity issue,
             requires manual verification
        (e)  Rejected: Did not pass validation, returned to encoder

  ii.   Status transitions shall be logged with timestamp and user ID
        via FastAPI Middleware and SQL Triggers.

 iii.   Regional Encoders shall be able to view the complete history
        of status changes for each incident via a React Timeline
        Component.

---

## Module 3: Conflict Detection and Manual Verification

a. Duplicate Detection

   i.   The system shall automatically compare newly uploaded incidents
        against existing records in the central database using FastAPI
        Background Tasks.

  ii.   The conflict detection algorithm shall check for:
        (a)  Exact match of incident location and date/time within a
             thirty (30)-minute window
        (b)  Similarity of incident narrative using fuzzy string
             matching with a threshold of eighty percent (80%)
        (c)  Matching casualty counts and property damage estimates

 iii.   When a potential duplicate is detected:
        (a)  Mark incident status as "Flagged"
        (b)  Generate a "Potential Duplicate Alert" with comparison
             details
        (c)  Route to the Manual Verification queue

b. Manual Verification Workflow

   i.   National Validators shall review flagged incidents in a
        dedicated queue using React Table and React Query.

  ii.   The system shall display a side-by-side comparison of
        conflicting records showing Incident ID, date/time, location,
        narrative text with highlighted differences, casualty and
        damage data, and attachments.

 iii.   National Validators shall be able to:
        (a)  Confirm as Duplicate — merge records, retain one,
             log merge action
        (b)  Confirm as Unique — clear "Flagged" status, approve
             for storage
        (c)  Request Revision — return to Regional Encoder with
             specific instructions

  iv.   Regional Encoders shall be notified of verification
        decisions via in-app notification using Server-Sent Events
        (SSE).

  v.   Regional Encoders shall be able to view comparison details
        and provide clarification when requested.

c. Revision and Resubmission

   i.   If an incident is returned for revision:
        (a)  Regional Encoder receives notification with reason
             for return
        (b)  Encoder can edit incident details and resubmit
        (c)  System logs revision history, preserving original
             version

  ii.   Resubmitted incidents shall re-enter the validation queue
        with a "Resubmitted" tag in the PostgreSQL Tags Column.

 iii.   National Validators shall be able to view the complete
        revision history before making a final decision.

---

## Module 4: Data Commit and Immutable Storage

a. Commit and Store Process

   i.   Once an incident passes manual verification, the system
        shall commit the record to the central database via FastAPI
        Dependency Injection.

  ii.   Committed records shall be stored in an append-only PostgreSQL
        table with no UPDATE or DELETE operations permitted on
        committed records, all modifications creating new version
        entries with reference to the original.

 iii.   Each committed record shall include:
        (a)  SHA-256 cryptographic hash of entire incident data
             for tamper detection
        (b)  Timestamp of commit operation
        (c)  User ID of validator who approved the record

  iv.   The system shall generate an "Insert Validated Record"
        transaction and send it to the Central Database using
        SQLAlchemy ORM.

  v.   The Central Database shall respond with a "Write Result /
       DB Ack" confirmation via the PostgreSQL RETURNING clause.

b. Audit Log Generation

   i.   The system shall log every commit operation in a dedicated
        System Logs table using a Partitioned PostgreSQL Table.

  ii.   Audit log entries shall include:
        (a)  Incident ID
        (b)  Commit timestamp
        (c)  Validator user ID
        (d)  SHA-256 hash of committed data
        (e)  Synchronization status (online/offline)

 iii.   Audit logs shall be immutable — append-only with no deletion
        — implemented via PostgreSQL Rule (DO INSTEAD NOTHING).

  iv.   The system shall send a "Log Import Success" message to the
        System Logs data store via an Asynchronous Message Queue.

---

## Module 5: Analytics and Reporting

a. Statistical Query Engine

   i.   National Analysts shall be able to query aggregated incident
        data from the Central Database using PostgreSQL Materialized
        Views.

  ii.   The system shall support filtering by:
        (a)  Date range (from–to)
        (b)  Incident type
        (c)  Location — municipality, province, region
        (d)  Casualty severity
        (e)  Property damage range

 iii.   The system shall provide the following analytics views:
        (a)  Total incidents by month, quarter, year
        (b)  Incident distribution by type (pie chart)
        (c)  Geographic heatmap of incident frequency
        (d)  Trend analysis — line graph of incidents over time
        (e)  Top ten (10) municipalities with highest incident count
        (f)  Average response time by region

b. Query Execution

   i.   National Analyst submits a query via "Query Parameters /
        Analysis Request" form.

  ii.   The system sends the query to the Analytics service via
        Query process.

 iii.   Analytics fetches data from the Central Database using
        "Aggregate Data" request.

  iv.   The Central Database responds with query results.

  v.   The system generates "Statistical Trends and Reports" output.

c. Report Export

   i.   National Analysts shall be able to export reports in the
        following formats:
        (a)  PDF — formatted for printing
        (b)  Excel (.xlsx) with raw data
        (c)  CSV — comma-separated values

  ii.   Exported reports shall include:
        (a)  Report title and description
        (b)  Query parameters (filters applied)
        (c)  Data visualization (charts/graphs)
        (d)  Summary statistics
        (e)  Generation timestamp and analyst user ID

 iii.   The system shall log all report exports in the audit trail
        via FastAPI Background Tasks.

d. Public Citizen Dashboard and Crowdsourcing

   i.   The system shall provide a publicly accessible incident
        reporting portal requiring no authentication, allowing
        civilians to submit fire reports without account creation
        or login.

  ii.   The system shall notify citizens of status updates regarding
        their submitted reports (e.g., pending, validated, rejected)
        through available notification channels.

 iii.  The system shall enforce compliance with the Data Privacy Act
        (RA 10173) by ensuring that all Personally Identifiable
        Information (PII) submitted by citizens is handled securely
        and only for operationally necessary purposes.

---

## Module 5d: Public Anonymous Incident Submission

> REVISED — removed citizen authentication requirement.
> Reporting a fire and requiring authentication creates user friction
> incompatible with emergency response. Abuse prevention is handled
> exclusively via rate limiting.

   i.   The system shall provide a publicly accessible incident reporting portal requiring no account creation, login, or any form of authentication, so that civilians can report fire incidents without friction.

  ii.   The system shall accept the following fields via POST /api/v1/public/report:
       (a)  latitude and longitude (WGS84 decimal degrees) — required
       (b)  description (free-text incident narrative) — required
       (c)  incident_type (enum: STRUCTURE_FIRE, VEHICULAR_FIRE, GRASS_FIRE, OTHER) — required
       (d)  occurred_at (ISO 8601 datetime) — optional, defaults to server timestamp

 iii.  The system shall enforce Redis-based IP rate limiting of a
        maximum of three (3) submissions per IP address per rolling
        one-hour window, returning HTTP 429 with a Retry-After
        header upon violation.

  iv.   The system shall assign all anonymously submitted incidents
        a verification_status of PENDING_VALIDATION and route them
        to the National Validator triage queue defined in Module 3.

  v.   The system shall resolve the incident region automatically via nearest-centroid geographic lookup against wims.ref_regions, defaulting to the first seeded region if no geometry intersection is found.

  vi.   The encoder_id field shall be set to NULL for all anonymous submissions to distinguish unauthenticated records from authenticated Regional Encoder submissions.

 vii.   No CAPTCHA shall be enforced on the public submission endpoint, as CAPTCHA introduces friction incompatible with emergency reporting; abuse prevention is handled exclusively through rate limiting.

viii.   All submitted data shall be treated as untrusted and subject to Pydantic schema validation before any database write operation.

  ix.   No personally identifiable information (PII) beyond operationally necessary data shall be collected, in compliance with RA 10173 data minimization principles.

---

## Module 6: Cryptographic Security

a. Data-at-Rest Encryption

   i.   All sensitive incident data stored in the Central Database
        shall be encrypted using SQLAlchemy TypeDecorator.

  ii.   Encryption shall be applied to:
        (a)  Incident narratives
        (b)  Casualty details
        (c)  Property damage estimates
        (d)  File attachments

 iii.   Encryption keys shall be managed by a dedicated key management
        service (OpenBao) deployed as a containerized service.

  iv.   Key rotation shall be performed every ninety (90) days via
        OpenBao Auto-Rotate.

b. Data-in-Transit Encryption

   i.   All network communication shall use TLS 1.3, enforced via
        Nginx or Traefik.

  ii.   HTTPS shall be enforced for all web traffic.

 iii.   Weak cipher suites shall be disabled — only AES-256-GCM and
        ChaCha20-Poly1305 allowed, configured in Nginx.

  iv.   HTTP Strict Transport Security (HSTS) shall be applied to
        API endpoints to prevent man-in-the-middle attacks.

---

## Module 7: Intrusion Detection and Network Monitoring

a. Network Traffic Mirroring

   i.   Internal Docker network traffic shall be monitored by the
        Intrusion Detection System (IDS) via a virtualized bridge
        interface using Suricata AF_PACKET.

  ii.   The IDS shall monitor all inbound and outbound traffic
        routed through the Nginx Reverse Proxy on the VPS.

 iii.   Mirrored traffic shall include:
        (a)  HTTP/HTTPS requests
        (b)  Database queries
        (c)  File uploads/downloads
        (d)  Authentication attempts

b. IDS Configuration

   i.   The system shall use Suricata as the network-based IDS engine,
        deployed as a containerized service.

  ii.   Suricata shall be configured with:
        (a)  OWASP Top 10 vulnerability signatures
        (b)  Custom BFP-specific rules (e.g., detect bulk incident
             deletion attempts)
        (c)  Emerging Threats ruleset — updated weekly

 iii.   The IDS shall generate unstructured logs for detected security
        events using EVE JSON Format.

  iv.   Unstructured logs shall be sent to the System Logs data store.

c. Log Collection and Forwarding

   i.   The IDS shall provide raw security logs to the Qwen2.5-3B AI
        module upon System Administrator request via Filebeat or
        volume sharing.

  ii.   Logs shall be forwarded via "Feeds Unstructured Logs" data
        flow using Redis as a message broker.

 iii.   Log forwarding shall occur in real-time with latency not
        exceeding five (5) seconds via FastAPI Background Worker.

---

## Module 8: Threat Detection with Explanation AI (XAI)

a. Qwen2.5-3B Integration

   i.   The system shall deploy Qwen2.5-3B Small Language Model (SLM)
        on the VPS via Docker using Llama.cpp bindings.

  ii.   The SLM shall consume specific Suricata EVE JSON alerts and
        FastAPI audit logs on-demand to generate human-readable
        forensic narratives.

 iii.   The SLM shall operate in synchronous on-request mode for the
        System Administrator, ensuring CPU/GPU resources are utilized
        only during active analysis.

b. Suricata-Driven Anomaly Detection

   i.   Suricata shall perform deterministic behavioral anomaly
        detection via custom rules and thresholds, generating EVE
        JSON alerts for the following:
        (a)  Impossible Travel — rapid logins from distant GeoIP
             locations using GeoIP2 MaxMind and custom Lua
             distance calculation
        (b)  Bulk Deletion Attempts — more than ten (10) deletions
             per five (5) minutes
        (c)  Off-Hours Access — admin actions between 10 PM and 6 AM
        (d)  Privilege Escalation — RBAC violations via endpoint
             access rules
        (e)  Suspicious Query Patterns — SQL injection and XSS
             attempts via signature rules

  ii.   Qwen2.5-3B shall generate explainable narratives for Suricata
        alerts with severity levels:
        (a)  Low — minor policy violation
        (b)  Medium — suspicious activity
        (c)  High — potential breach
        (d)  Critical — active attack

c. Explainable AI (XAI) Reports

   i.   For each selected anomaly, the AI shall generate a
        human-readable explanation using specific system prompts
        to interpret raw log data.

  ii.   Each XAI report shall include:
        (a)  Description of detected anomaly in plain language
        (b)  Evidence — log excerpts, timestamps, user IDs
        (c)  Risk assessment — likelihood and impact
        (d)  Recommended action

 iii.   Reports shall be delivered to the System Monitoring dashboard
        via standard API requests upon completion of the inference
        task.

d. Human-in-the-Loop (HITL) Validation

   i.   System Administrators shall review all Medium, High, and
        Critical alerts.

  ii.   AI-generated alerts shall not trigger automatic blocking
        actions.

 iii.   System Administrator actions shall include:
        (a)  Confirm Threat — escalate to incident response,
             lock affected accounts
        (b)  False Positive — dismiss alert, optionally add to
             AI training exclusions
        (c)  Request More Info — ask AI to re-analyze with
             additional context

  iv.   All HITL decisions shall be logged in the audit trail
        via PostgreSQL JSONB Column.

---

## Module 9: System Monitoring and Health Dashboard

a. System Health Metrics

   i.   The System Monitoring module shall track the following
        metrics using Python psutil and Docker API:
        (a)  Container Status — uptime and health of FastAPI,
             PostgreSQL, Suricata, and Qwen-AI containers
        (b)  VPS Resource Usage — real-time CPU and RAM utilization
        (c)  Database Performance — average query latency in
             milliseconds
        (d)  PWA Sync Health — success rate of background
             synchronization events from the PWA client
        (e)  Network Traffic — inbound/outbound bandwidth usage
             via Nginx
        (f)  AI On-Demand Latency — time in seconds for the SLM
             to generate a forensic narrative per request

  ii.   Metrics shall be refreshed every sixty (60) seconds.

 iii.   System Administrators shall be able to view real-time metrics
        in a dedicated dashboard.

b. Log Query and Review

   i.   System Administrators shall be able to query System Logs
        using filters:
        (a)  Date/time range
        (b)  User ID
        (c)  Log severity — INFO, WARN, ERROR, CRITICAL
        (d)  Event type — authentication, data modification,
             security alert

  ii.   The system shall support full-text search across log entries
        using PostgreSQL tsvector with a GIN index.

 iii.   Query results shall be paginated at fifty (50) entries
        per page using FastAPI LimitOffsetPagination.

c. Health Status Reporting

   i.   System Monitoring shall send periodic "System Health Status"
        reports to the System Administrator every four (4) hours
        or on-demand via FastAPI Utilities repeat_every.

  ii.   Reports shall include:
        (a)  Summary of system metrics
        (b)  List of recent security alerts
        (c)  Database backup status
        (d)  Disk usage and availability

d. Configuration Management

   i.   System Administrators shall be able to update monitoring
        thresholds via the interface.

  ii.   Configurable parameters shall include:
        (a)  Alert severity thresholds
        (b)  Session timeout duration
        (c)  Offline mode maximum storage limit
        (d)  AI Response Timeout — maximum time allowed for an
             AI explanation before request cancellation

---

## Module 10: Compliance and Data Privacy

a. Data Privacy Act (RA 10173) Compliance

   i.   The system shall implement the data minimization principle:
        (a)  Collect only necessary data for fire incident reporting
        (b)  Do not collect Sensitive Personal Information (SPI)
             unless operationally required

  ii.   The system shall provide purpose limitation:
        (a)  Incident data used only for fire suppression operations
             and national statistics
        (b)  Secondary use of data is strictly prohibited without
             explicit consent

 iii.   The system shall support individual rights:
        (a)  Right to Access — users can request a copy of their
             submitted incidents
        (b)  Right to Rectification — users can request correction
             of inaccurate data
        (c)  Right to Erasure — users can request deletion with
             soft delete and audit trail preservation

b. Cloud-Based Data Privacy Impact Assessment (DPIA)

   i.   The system shall maintain DPIA documentation covering:
        (a)  Description of data processing activities within the
             Docker/VPS environment
        (b)  Identified privacy risks and mitigation measures
        (c)  Legal basis for processing (public interest /
             official authority)
        (d)  Data retention periods

  ii.   The DPIA shall be reviewed annually or whenever major
        infrastructure changes occur.

c. Records of Processing Activities (RoPA)

   i.   The system shall maintain RoPA documenting:
        (a)  Categories of data subjects — Regional Encoders,
             Validators, Analysts, Administrators, Citizens
        (b)  Categories of personal data — names, user IDs,
             email addresses, login timestamps
        (c)  Purposes of processing — incident reporting,
             access control, audit logging
        (d)  Data retention periods — active records: indefinite;
             audit logs: seven (7) years
        (e)  Security measures — encryption, access control,
             audit logging

  ii.   The RoPA shall be accessible to System Administrators and
        the Data Protection Officer.

d. Breach Notification

   i.   In the event of a data breach, the system shall:
        (a)  Automatically generate a breach notification report
        (b)  Include date/time of breach, affected data categories,
             and estimated number of affected records
        (c)  Notify the Data Protection Officer and System
             Administrator immediately

  ii.   System Administrators shall assess breach severity and
        determine if National Privacy Commission (NPC) notification
        is required within seventy-two (72) hours if confirmed.

---

## Module 11: Penetration Testing and Security Validation

a. Vulnerability Scanning

   i.   The system shall undergo regular vulnerability scans using:
        (a)  Nmap — network discovery and port scanning
        (b)  OWASP ZAP — web application vulnerability scanning
        (c)  sqlmap — SQL injection testing

  ii.   Scans shall be conducted in a controlled staging environment
        mirroring the VPS production setup.

 iii.   Scan frequency shall be monthly during development and
        quarterly post-deployment.

b. Penetration Testing Scope

   i.   Penetration tests shall target the following attack vectors:
        (a)  Authentication bypass
        (b)  Privilege escalation
        (c)  SQL injection
        (d)  Cross-Site Scripting (XSS) — stored and reflected
        (e)  Cross-Site Request Forgery (CSRF)
        (f)  Sensitive data exposure
        (g)  Denial of Service (DoS)

c. Remediation and Retesting

   i.   All identified vulnerabilities shall be classified by severity:
        Critical, High, Medium, Low.

  ii.   Remediation timelines:
        (a)  Critical — twenty-four (24) hours
        (b)  High — seven (7) days
        (c)  Medium — thirty (30) days
        (d)  Low — ninety (90) days

 iii.   After remediation, the system shall undergo retesting to
        confirm the fix.

  iv.   All vulnerabilities and remediation actions shall be
        documented in a security audit report.

---

## Module 12: User Management and Administration

a. User Onboarding

   i.   System Administrators shall be able to create new user
        accounts using python-keycloak Admin Client.

  ii.   Required user information:
        (a)  Full name
        (b)  Email address (serves as username)
        (c)  Role assignment — Encoder, Validator, Analyst,
             Administrator, Citizen
        (d)  Contact number — optional

 iii.   The system shall auto-generate a temporary password and
        send it via secure email using Keycloak "Execute Actions."

  iv.   Users must change their password upon first login via
        Required Action (Update Password).

b. User Profile Management

   i.   Users shall be able to view and update their own profile
        information via the Keycloak Account API:
        (a)  Full name
        (b)  Email address
        (c)  Contact number

  ii.   Users shall not be permitted to modify their own role
        assignment — only System Administrators can perform this
        action via Keycloak Token Claims.

c. User Deactivation and Deletion

   i.   System Administrators shall be able to deactivate user
        accounts (soft delete) by setting Keycloak enabled to false.

  ii.   Deactivated accounts:
        (a)  Cannot log in
        (b)  Remain in the database for audit purposes
        (c)  Can be reactivated by a System Administrator

 iii.   Hard deletion of user accounts shall not be permitted,
        preserving audit trail integrity via PostgreSQL Foreign
        Keys.

---

## Module 13: Notification System

> DEFERRED — implementation contingent on completion of all role
> dashboards and remaining Phase 1 functional modules.

a. In-App Notifications

   i.   The system shall support real-time in-app notifications for:
        (a)  Incident status updates (Draft → Pending → Validated)
        (b)  Duplicate detection alerts
        (c)  Manual verification decisions
        (d)  Security alerts for System Administrator
        (e)  Synchronization success/failure

  ii.   Notifications shall appear as non-intrusive pop-ups in the
        top-right corner using react-hot-toast.

 iii.   Users shall be able to view notification history in a
        dedicated Notifications panel using Redis List as a
        user inbox.

b. Email Notifications

   i.   The system shall send email notifications for:
        (a)  Password reset requests
        (b)  Account lockout warnings
        (c)  Critical security alerts for System Administrator
        (d)  Weekly summary reports — optional and configurable

  ii.   Email templates shall be professional and include:
        (a)  BFP logo and branding
        (b)  Clear subject line
        (c)  Action required (if applicable)
        (d)  Link to relevant system page

---

## Module 14: Public Anonymous Incident Submission

> NEW MODULE — zero-trust anonymous ingestion channel.
> No authentication, no citizen account. Rate limiting is the sole
> abuse vector control. Implemented as the /api/v1/public/report
> endpoint.

i.   The system shall provide a zero-trust public endpoint at POST /api/v1/public/report accepting fire incident reports without any authentication token, session cookie, or credential exchange.

ii.   Rate limiting shall be enforced via Redis with a threshold of three (3) requests per source IP address per rolling one-hour window, applied before any database connection acquisition.
  
iii.   Anonymous submissions shall be stored in wims.fire_incidents with encoder_id set to NULL and verification_status set to PENDING_VALIDATION.

 iv.   The system shall resolve region_id automatically via a nearest-centroid query against wims.ref_regions geometry, with a fail-safe fallback to the first seeded region if no geometry intersection is found.

 v.   Exceeding the rate limit shall return HTTP 429 (Too Many Requests) with a Retry-After HTTP header indicating the number of seconds until the window resets.

vi.   No attachment upload capability shall be exposed on the public endpoint; file attachments require an authenticated session and shall use Module 2 functionality.

vii.   No CAPTCHA shall be enforced; rate limiting is the sole abuse prevention mechanism.

viii.   All submitted data shall be subject to Pydantic schema validation before any database write.

ix.   No personally identifiable information (PII) beyond operationally necessary data shall be collected, in compliance with RA 10173 data minimization.

---

## Module 15: Reference Data Service

> NEW MODULE — shared geographic hierarchy lookup API.
> Read-only authenticated service used by all modules requiring
> regions, provinces, or cities data.

   i.   The system shall provide an authenticated read-only API for querying the geographic reference hierarchy used across all system modules.

  ii.   The system shall expose GET /api/ref/regions returning region_id, region_name, and region_code; optionally filtered by region_id.

 iii.   The system shall expose GET /api/ref/provinces returning province_id, province_name, and region_id; optionally filtered by region_id.

  iv.   The system shall expose GET /api/ref/cities returning city_id, city_name, and province_id; optionally filtered by single province_id or a comma-separated list of province_ids for batch lookup.

  v.   All reference data endpoints shall require authentication via any valid WIMS user role.

 vi.   Row-level security policies shall restrict visibility so that REGIONAL_ENCODER and REGIONAL_VALIDATOR roles see only reference data for their assigned region; NATIONAL_ANALYST and SYSTEM_ADMIN shall see all regions.

vii.   Reference data shall be sourced exclusively from wims.ref_regions, wims.ref_provinces, and wims.ref_cities; no write operations on reference data shall be exposed through this API.

---

## Change Log

| Date | Change | Rationale |
|------|--------|-----------|
| 2026-05-04 | Module 5d revised — removed citizen authentication | Authentication before fire reporting creates UX friction incompatible with emergency response |
| 2026-05-04 | Module 14 added — Public Anonymous Incident Submission | Formalized public_dmz.py as a standalone FRS module |
| 2026-05-04 | Module 15 added — Reference Data Service | Formalized ref.py as a shared infrastructure module |
| 2026-05-04 | Module 13 marked DEFERRED | Notification System postponed until all role dashboards are functional |
