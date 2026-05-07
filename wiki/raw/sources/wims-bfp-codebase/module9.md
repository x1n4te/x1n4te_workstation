## Module 9: System Monitoring and Health Dashboard

### A. System Health Metrics

1. System Monitoring module shall track the following metrics (using Python psutil and Docker API):
    - **Container Status:** Uptime and health of specific containers (FastAPI, PostgreSQL, Suricata, Qwen-AI).
    - **VPS Resource Usage:** Real-time CPU and RAM utilization (critical for monitoring AI spikes).
    - **Database Performance:** Average query latency in milliseconds.
    - **PWA Sync Health:** Success rate of background synchronization events from the PWA client.
    - **Network Traffic:** Inbound/outbound bandwidth usage via Nginx.
    - **AI On-Demand Latency:** Time taken (in seconds) for the SLM to generate a forensic narrative per request.
2. Metrics shall be refreshed every 60 seconds to ensure real-time visibility without over-burdening VPS resources.
3. System Administrator can view real-time metrics in dedicated dashboard

### B. Log Query and Review

1. System Administrator can query System Logs using filters: — `PostgreSQL JSONB Queries`
    - Date/time range
    - User ID
    - Log severity (INFO, WARN, ERROR, CRITICAL)
    - Event type (authentication, data modification, security alert)
2. System shall support full-text search across log entries — `PostgreSQL tsvector (Gin Index)`
3. Query results shall be paginated (50 entries per page) — `FastAPI LimitOffsetPagination`

### C. Health Status Reporting

1. System Monitoring shall send periodic "System Health Status" reports to System Administrator — `FastAPI Utilities repeat_every`
2. Reports generated every 4 hours (or on-demand)
3. Report includes:
    - Summary of system metrics
    - List of recent security alerts
    - Database backup status — `Pg_Dump Exit Codes`
    - Disk usage and available — `storage psutil.disk_usage('/')`

### D. Configuration Management

1. System Administrator can update monitoring thresholds via the interface.
2. Configurable parameters:
    - Alert severity thresholds (e.g., trigger High alert if > 5 failed logins in 10 minutes)
    - Session timeout duration
    - Offline mode maximum storage limit
    - AI Response Timeout: Maximum time allowed for an AI explanation before the request is canceled.
