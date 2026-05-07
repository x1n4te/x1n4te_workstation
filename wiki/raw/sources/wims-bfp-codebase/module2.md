## **Module 2: Offline-First Incident Management**

### A. Incident Data Entry

1. Regional Encoder can create new fire incident reports with the following fields: — `React Hook Form + Zod`
    - Incident ID (auto-generated, immutable) — `UUID (v4)`
    - Date and time of incident (timestamp)
    - Location (address, municipality, province)
    - Incident type (structure fire, vehicular fire, grass fire, others)
    - Incident narrative (free-text description)
    - Casualties (injuries, fatalities)
    - Property damage estimate
    - Responders deployed
    - Fire suppression status (ongoing, contained, extinguished)
2. Support file attachments (photos, reports, maps) — `React Dropzone`
    - Accepted formats: `.jpg`, `.png`, `.pdf`, `.docx` (max 10MB each)
    - Maximum 5 attachments per incident
    - Attachments encrypted before storage — `Web Crypto API (AES-GCM)`
3. Incident form shall include client-side validation
    - Required fields: Incident ID, date/time, location, incident type, narrative
    - Real-time validation feedback (field-level error messages)

### B. Offline Data Capture and Storage

1. System shall detect network availability automatically — `Navigator API + React Hook`
2. When offline, incident data shall be stored locally in browser IndexedDB — `Dexie.js (IndexedDB Wrapper)`
3. Offline-captured records shall be encrypted using AES-256-GCM before local storage — `Web Crypto + ArrayBuffer`
4. User interface shall display clear "Offline Mode" indicator — `Tailwind CSS / Toast`
5. All CRUD operations (Create, Read, Update, Delete) must function fully in offline mode
6. Offline storage capacity: minimum 1,000 incident records with attachments — `StorageManager API`

### C. Data Synchronization

1. System shall automatically detect network restoration — `TanStack Query (React Query)`
2. Upon reconnection, system shall: — `Background Sync API (Service Worker)`
    - Upload locally stored incidents to central server
    - Verify cryptographic integrity of each record (AES-256-GCM tag check)
    - Detect and resolve conflicts (duplicate incident detection)
    - Update local database with server response
3. Synchronization process must be atomic (all-or-nothing per incident) — `FastAPI transaction.atomic`
4. Failed synchronization attempts shall retry automatically (exponential backoff, max 5 retries) — `TanStack Query retry`
5. User shall receive notification of synchronization success or failure — `React Hot Toast`

### D. Incident Status Tracking

1. System shall support the following incident statuses: — `PostgreSQL Enum`
    - **Draft:** Incomplete record, saved locally, not yet submitted
    - **Pending:** Submitted for validation, awaiting National Validator review
    - **Validated:** Approved by National Validator, committed to central database
    - **Flagged:** Potential duplicate or data integrity issue, requires manual verification
    - **Rejected:** Did not pass validation, returned to encoder with reason
2. Status transitions shall be logged with timestamp and user ID — `FastAPI Middleware / SQL Triggers`
3. Regional Encoder can view history of status changes for each incident — `React Timeline Component`