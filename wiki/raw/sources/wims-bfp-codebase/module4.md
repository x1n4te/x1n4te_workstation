## Module 4: Data Commit and Immutable Storage

### A. Commit and Store Process

1. Once incident passes manual verification, system shall commit record to central database — `FastAPI Dependency Injection`
2. Committed records shall be stored in append-only PostgreSQL table — `PostgreSQL Permissions (GRANT/REVOKE)`
    - No `UPDATE` or `DELETE` operations allowed on committed records
    - All modifications create new version entries with reference to original
3. Each committed record shall include: — `Python hashlib + SQL Trigger`
    - SHA-256 cryptographic hash of entire incident data (for tamper detection)
    - Timestamp of commit operation
    - User ID of validator who approved the record
4. System shall generate "Insert Validated Record" transaction and send to Central Database — `SQLAlchemy ORM`
5. Central Database shall respond with "Write Result / DB Ack" confirmation — `PostgreSQL RETURNING clause`

### B. Audit Log Generation

1. System shall log every commit operation in dedicated System Logs table — `Partitioned PostgreSQL Table`
2. Audit log entry shall include: — `Pydantic Middleware`
    - Incident ID
    - Commit timestamp
    - Validator user ID
    - SHA-256 hash of committed data
    - Synchronization status (online/offline)
3. Audit logs shall be immutable (append-only, no deletion) — `PostgreSQL Rule (DO INSTEAD NOTHING)`
4. System shall send "Log Import Success" message to System Logs data store — `Asynchronous Message Queue`
