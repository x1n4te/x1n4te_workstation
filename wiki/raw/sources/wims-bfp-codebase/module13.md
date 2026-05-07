## Module 13: Notification System

### A. In-App Notifications

1. System shall support real-time in-app notifications for: — `Server-Sent Events (SSE)`
    - Incident status updates (Draft → Pending → Validated)
    - Duplicate detection alerts
    - Manual verification decisions
    - Security alerts (for System Administrator)
    - Synchronization success/failure
2. Notifications shall appear as non-intrusive pop-up in top-right corner — `react-hot-toast`
3. Users can view notification history in dedicated Notifications panel — `Redis List (User Inbox)`

### B. Email Notifications

1. System shall send email notifications for: — `FastAPI Background Tasks`
    - Password reset requests
    - Account lockout warnings
    - Critical security alerts (for System Administrator)
    - Weekly summary reports (optional, configurable)
2. Email templates shall be professional and include: — `Jinja2 + MJML`
    - BFP logo and branding
    - Clear subject line
    - Action required (if applicable)
    - Link to relevant system page