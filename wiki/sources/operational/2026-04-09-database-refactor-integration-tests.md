---
id: ops-2026-04-09-database-refactor-001
type: source
created: 2026-04-09
confidence: high
source_refs:
  - ~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/src/backend/database.py
  - ~/WIMS-BFP-NEW/LOCAL-WIMS-BFP-PROTOTYPE/src/backend/tests/integration/test_regional_crud.py
status: active
tags:
  - operational
  - database
  - integration-tests
  - regional-crud
  - wims-bfp
related:
  - sources/software-dev/wims-bfp-codebase-ingestion-2026-04-08
  - concepts/fastapi-security-wims-bfp
  - concepts/postgresql-security-wims-bfp
---

# Database Refactor + Integration Tests — 2026-04-09

**Delegated to:** Claude Code (print mode)
**Cost:** $1.74, 23 turns
**Result:** 15/15 tests passed after 2 fixes

---

## What Was Broken

### 1. `_SessionLocal` was `None` (TypeError)
`database.py` used a lazy initialization pattern where `_engine` and `_SessionLocal` started as `None` and only populated when `get_session_maker()` was called. Tests imported `_SessionLocal` directly before that happened.

### 2. Database URL resolved to Docker hostname (OperationalError)
`database.py` read `SQLALCHEMY_DATABASE_URL` from env vars before `load_dotenv()` ran. Fell back to `postgres:5432` (Docker service name), causing `could not translate host name "postgres"`.

---

## What Was Fixed (in `database.py`)

### Eager initialization
```python
# BEFORE (lazy — None until get_session_maker() called)
_engine: Engine | None = None
_SessionLocal: sessionmaker | None = None

# AFTER (eager — initialized at module load)
_engine: Engine = create_engine(SQLALCHEMY_DATABASE_URL)
_SessionLocal: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
```

### load_dotenv() before URL resolution
```python
+from dotenv import load_dotenv
+load_dotenv()
 SQLALCHEMY_DATABASE_URL = os.environ.get(...)
```

### Split get_db → get_db() + get_db_with_rls()
- `get_db()` — bare session, no RLS context (for tests and simple routes)
- `get_db_with_rls(request)` — sets RLS via `SET LOCAL wims.current_user_id` (for protected routes)
- Avoids dependency cycle where `get_current_wims_user` depends on `get_db` but `get_db` needs user resolved first

---

## Test Results

| Class              | Tests  | Result         |
| ------------------ | ------ | -------------- |
| TestCreateIncident | 4      | All pass       |
| TestReadIncidents  | 3      | All pass       |
| TestUpdateIncident | 4      | All pass       |
| TestDeleteIncident | 4      | All pass       |
| **Total**          | **15** | **15/15 pass** |

---

## Side Effects

Claude also cleaned up 11 stale files (`.ai-context/`, `CHANGELOG.md`→`docs/`, `SCHEMA_MERGE_NOTES.md`, `archive/sql/`, etc. — 1,655 lines removed). CHANGELOG.md restored and moved to `docs/CHANGELOG.md`.

---

## Lessons

- Lazy initialization of SQLAlchemy engine/session is a common test footgun — eager init is safer for integration tests
- Always call `load_dotenv()` before reading env vars that depend on `.env`
- Claude Code print mode worked well for this — one-shot task, structured output, no tmux needed
