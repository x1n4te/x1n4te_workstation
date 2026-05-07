## Module 8: Threat Detection with Explanation AI (XAI)

### A. Qwen2.5-3B Integration

1. The system shall deploy Qwen2.5-3B Small Language Model (SLM) on the VPS via Docker — `Llama.cpp bindings`
2. SLM shall consume specific Suricata EVE JSON alerts + FastAPI audit logs on-demand to generate human-readable forensic narratives.
3. SLM operates in a synchronous on-request mode for the System Administrator, ensuring CPU/GPU resources are only utilized during active analysis.

### B. Suricata-Driven Anomaly Detection (Qwen Explainability Layer)

1. Suricata shall perform deterministic behavioral anomaly detection via custom rules/thresholds, generating EVE JSON alerts for:
    - **Impossible Travel:** Rapid logins from distant GeoIP locations — `GeoIP2 MaxMind + custom Lua distance calc`
    - **Bulk Deletion Attempts:** >10 deletions/5min (threshold: type limit, track by_src)
    - **Off-Hours Access:** Admin actions 10PM–6AM (time-based rule suppression whitelist)
    - **Privilege Escalation:** RBAC violations (endpoint access rules)
    - **Suspicious Query Patterns:** SQLi/XSS attempts (signature rules)
2. Qwen2.5-3B shall generate explainable narratives for Suricata alerts with severity levels:
    - **Low:** Minor policy violation (e.g., "Failed login from known IP—likely mistyped password")
    - **Medium:** Suspicious activity (e.g., "Off-hours access by encoderjuan—review required")
    - **High:** Potential breach (e.g., "Bulk 15 deletions in 3min—possible data poisoning")
    - **Critical:** Active attack (e.g., "Privilege escalation detected: encoder accessing /api/analytics")

### C. Explainable AI (XAI) Reports

1. For a selected anomaly, the AI shall generate a human-readable explanation using specific System Prompts to interpret the raw log data.
2. Each XAI report shall include: — `Guidance / Instructor Library`
    - Description of detected anomaly in plain language
    - Evidence (log excerpts, timestamps, user IDs)
    - Risk assessment (likelihood and impact)
    - Recommended action (e.g., "Lock user account", "Review access logs", "Investigate further")
3. Reports shall be delivered to the System Monitoring dashboard via standard API requests upon completion of the inference task.

### D. Human-in-the-Loop (HITL) Validation

1. System Administrator shall review all Medium, High, and Critical alerts — `React "Tinder for Threats" Card`
2. AI-generated alerts shall not trigger automatic blocking actions
3. System Administrator actions:
    - **Confirm Threat:** Escalate to incident response, lock affected accounts
    - **False Positive:** Dismiss alert, optionally add to AI training exclusions — `Few-Shot Context Injection`
    - **Request More Info:** Ask AI to re-analyze with additional context
4. System shall log all HITL decisions for audit trail — `PostgreSQL JSONB Column`