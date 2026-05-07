## Module 5: Analytics and Reporting

### A. Statistical Query Engine

1. National Analyst can query aggregated incident data from Central Database — `PostgreSQL Materialized Views`
2. System shall support filtering by: — `FastAPI Depends (Query Params)`
    - Date range (from–to)
    - Incident type
    - Location (municipality, province, region)
    - Casualty severity
    - Property damage range
3. System shall provide the following analytics views: — `SQLAlchemy + Pandas`
    - Total incidents by month, quarter, year
    - Incident distribution by type (pie chart) — `Recharts`
    - Geographic heatmap of incident frequency — `React Leaflet + Leaflet.heat`
    - Trend analysis (line graph of incidents over time) — `Recharts (ComposedChart)`
    - Top 10 municipalities with highest incident count
    - Average response time by region

### B. Query Execution

1. National Analyst submits query via "Query Parameters / Analysis Request" form
2. System sends query to Analytics via Query process
3. Analytics via Query fetches data from Central Database using "Aggregate Data" request
4. Central Database responds with query results
5. System generates "Statistical Trends and Reports" output

### C. Report Export

1. National Analyst can export reports in the following formats:
    - PDF (formatted for printing) — `WeasyPrint`
    - Excel (`.xlsx`) with raw data — `Pandas (to_excel, to_csv)`
    - CSV (comma-separated values)
2. Exported reports shall include:
    - Report title and description
    - Query parameters (filters applied)
    - Data visualization (charts/graphs)
    - Summary statistics
    - Generation timestamp and analyst user ID
3. System shall log all report exports in audit trail — `FastAPI Background Tasks`

### D. Public Citizen Dashboard and Crowdsourcing

1. The system shall provide a secure, authenticated portal for the Citizen role, requiring login before access to any functionality.
2. Citizens shall be allowed to submit incident reports through a structured reporting interface, including necessary incident details.
3. Citizens may optionally upload supporting media (e.g., images or files) as evidence during report submission.
4. All submitted citizen reports shall be automatically routed to the "Pending" queue for the National Validator’s review.
5. The system shall notify citizens of status updates regarding their submitted reports (e.g., pending, validated, rejected).
6. The system shall enforce compliance with the Data Privacy Act (RA 10173) by ensuring that all Personally Identifiable Information (PII) submitted by citizens is secure.