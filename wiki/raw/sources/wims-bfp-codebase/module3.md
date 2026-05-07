## Module 3: Conflict Detection and Manual Verification

### A. Duplicate Detection

1. System shall automatically compare newly uploaded incidents against existing records in the central database — `FastAPI Background Tasks`
2. Conflict detection algorithm shall check for: — `Python RapidFuzz + SQL Intervals`
    - Exact match of incident location and date/time (within 30-minute window)
    - Similarity of incident narrative (using fuzzy string matching, threshold 80%)
    - Matching casualty counts and property damage estimates
3. When potential duplicate is detected: — `PostgreSQL Status Update`
    - Mark incident status as "Flagged"
    - Generate "Potential Duplicate Alert" with comparison details
    - Route to Manual Verification queue

### B. Manual Verification Workflow

1. National Validator shall review flagged incidents in dedicated queue — `React Table + React Query`
2. System shall display side-by-side comparison of conflicting records: — `react-diff-viewer-continued`
    - Incident ID, date/time, location
    - Narrative text (with highlighted differences)
    - Casualty and damage data
    - Attachments (if any)
3. National Validator actions: — `FastAPI RPC-style Endpoints`
    - **Confirm as Duplicate:** Merge records, retain only one in database, log merge action
    - **Confirm as Unique:** Clear "Flagged" status, approve for storage
    - **Request Revision:** Return to Regional Encoder with specific instructions
4. Regional Encoder shall be notified of verification decision via in-app notification — `Server-Sent Events (SSE)`
5. Regional Encoder can view comparison details and provide clarification if requested

### C. Revision and Resubmission

1. If incident is returned for revision: — `sqlalchemy-continuum`
    - Regional Encoder receives notification with reason for return
    - Encoder can edit incident details and resubmit
    - System logs revision history (original version preserved)
2. Resubmitted incident re-enters validation queue with "Resubmitted" tag — `PostgreSQL Tags Column`
3. National Validator can view revision history before making final decision — `React Timeline Component`