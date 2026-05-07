# Ubiquitous Language — WIMS-BFP

> Domain terminology for the Web Incident Monitoring System - Bureau of Fire Protection.
> Based on Eric Evans' DDD ubiquitous language.
> All code, documentation, and AI interactions MUST use these terms.
> Last updated: 2026-04-26

---

## Bounded Contexts

### Incident Reporting
The public-facing and triage flow: civilians submit reports, validators review and promote them to official incidents.

### Incident Management
The regional encoding and verification flow: encoders import AFORs, validators verify/reject incidents.

### Analytics
The read-only analytical layer: heatmaps, trends, spatial aggregation for decision support.

### Security Monitoring
The Suricata IDS + XAI pipeline: network threat detection, alert classification, narrative generation.

### Identity & Access
Keycloak-based authentication, RBAC roles, MFA enforcement, JWT token resolution.

---

## Core Terms

### Incident
- **Definition:** A fire event that has been officially recorded in the system as a `fire_incidents` row.
- **Context:** Incident Reporting, Incident Management
- **Code:** `wims.fire_incidents` table, `FireIncident` model
- **Not:** A citizen report (which is unvalidated), a Suricata alert (which is a network event)
- **Related:** Citizen Report, Verification Status, AFOR

### Citizen Report
- **Definition:** A fire report submitted by the public via the unauthenticated `/api/v1/public/report` endpoint. Has not been validated.
- **Context:** Incident Reporting
- **Code:** `wims.citizen_reports` table
- **Not:** An Incident (citizen reports are promoted to incidents after triage)
- **Related:** Incident, Triage

### Triage
- **Definition:** The process by which a NATIONAL_VALIDATOR reviews citizen reports and promotes valid ones to official incidents.
- **Context:** Incident Reporting
- **Code:** `POST /api/triage/{id}/promote` endpoint
- **Not:** Verification (which is the review of already-created incidents)
- **Related:** Citizen Report, Incident, NATIONAL_VALIDATOR

### AFOR (Accident/Fire Occurrence Report)
- **Definition:** The official BFP form for recording fire incidents. Imported in bulk via XLSX/CSV or entered manually. Comes in Structural and Wildland variants.
- **Context:** Incident Management
- **Code:** `wims.data_import_batches`, `wims.incident_wildland_afor`, `wims.incident_structural_afor`
- **Not:** A citizen report (AFORs are official BFP forms, not public submissions)
- **Related:** Incident, Data Import Batch, Regional Encoder

### Data Import Batch
- **Definition:** A tracked batch of AFOR records imported by a REGIONAL_ENCODER. Groups related imports for auditability.
- **Context:** Incident Management
- **Code:** `wims.data_import_batches` table
- **Not:** A single incident (a batch contains multiple incidents)
- **Related:** AFOR, Regional Encoder

### Verification Status
- **Definition:** The lifecycle state of an incident: DRAFT → PENDING → VERIFIED or REJECTED.
- **Context:** Incident Management
- **Code:** `wims.verification_status` enum
- **Not:** Triage status (triage is about citizen reports, verification is about incidents)
- **Related:** Incident, National Validator

### Region
- **Definition:** A Philippine administrative region (e.g., NCR). Used for RBAC scoping — REGIONAL_ENCODER can only access their assigned region.
- **Context:** Incident Management, Analytics, Identity & Access
- **Code:** `wims.ref_regions` table
- **Not:** A city or barangay (those are lower-level geographic divisions)
- **Related:** Province, City, Barangay, Regional Encoder

### PostGIS Location
- **Definition:** A geographic coordinate stored as a PostGIS geometry point, used for spatial queries (heatmap, proximity search, clustering).
- **Context:** Analytics, Incident Management
- **Code:** PostGIS `geometry(Point, 4326)` columns
- **Not:** A text address (PostGIS is geometric, not textual)
- **Related:** Incident, Heatmap

### Heatmap
- **Definition:** A spatial aggregation of incidents rendered as map tiles, showing fire density by geographic area.
- **Context:** Analytics
- **Code:** `GET /api/analytics/heatmap` endpoint, PostGIS spatial aggregation
- **Not:** A list of incidents (heatmap is aggregated, not individual records)
- **Related:** Incident, PostGIS Location, National Analyst

### XAI Pipeline
- **Definition:** The Explainable AI pipeline: Suricata EVE JSON → Celery Beat (10s poll) → Qwen2.5-3B SLM classification → human-readable narrative stored in `security_threat_log`.
- **Context:** Security Monitoring
- **Code:** Celery worker, Qwen2.5-3B model, `wims.security_threat_log` table
- **Not:** A firewall rule (XAI explains threats, it doesn't block them)
- **Related:** Suricata, Security Threat Log, Threat Narrative

### Security Threat Log
- **Definition:** A record of a network threat detected by Suricata, enriched with an XAI-generated narrative explaining the threat.
- **Context:** Security Monitoring
- **Code:** `wims.security_threat_log` table
- **Not:** An audit log entry (threat logs are about network security, audit logs are about system actions)
- **Related:** Suricata, XAI Pipeline, Threat Narrative

### Threat Narrative
- **Definition:** A human-readable explanation of a security threat, generated by the Qwen2.5-3B SLM from Suricata alert data.
- **Context:** Security Monitoring
- **Code:** `security_threat_log.narrative` column
- **Not:** A raw Suricata alert (narratives are AI-interpreted, not raw IDS output)
- **Related:** Security Threat Log, XAI Pipeline, Qwen2.5-3B

### BFP Role
- **Definition:** One of 5 system roles that determine access scope: CIVILIAN_REPORTER, REGIONAL_ENCODER, NATIONAL_VALIDATOR, NATIONAL_ANALYST, SYSTEM_ADMIN.
- **Context:** Identity & Access
- **Code:** Keycloak `realm_access.roles` / `resource_access.bfp-client.roles`
- **Not:** A Keycloak realm role (BFP roles are application-level, scoped to the bfp-client)
- **Related:** RBAC, JWT, MFA

### RLS (Row-Level Security)
- **Definition:** PostgreSQL's row-level security feature, used to enforce data isolation — users can only see rows they're authorized for based on their role and region.
- **Context:** Identity & Access, Incident Management
- **Code:** PostgreSQL RLS policies on all `wims.*` tables
- **Not:** API-level authorization (RLS is database-enforced, not application-enforced)
- **Related:** BFP Role, Region, PostGIS Location

### Audit Log
- **Definition:** A system-wide record of all significant actions (create, update, delete, login, role change) for compliance and forensics.
- **Context:** Identity & Access, Security Monitoring
- **Code:** `wims.audit_log` table
- **Not:** A security threat log (audit logs track user actions, threat logs track network events)
- **Related:** System Admin, Security Threat Log

---

## Ambiguities (Resolved)

| Term | Context A | Context B | Resolution |
|------|-----------|-----------|------------|
| "Incident" | Incident Reporting = a fire event record | Security Monitoring = a network alert | Use "Incident" for fire events, "Threat Alert" for network events |
| "Report" | Incident Reporting = citizen report | Analytics = generated report document | Use "Citizen Report" for submissions, "Analytics Report" for generated docs |
| "Region" | Incident Management = geographic scope | Identity & Access = RBAC scope | Same entity — `ref_regions` table serves both purposes |
| "Status" | Incident = verification_status (DRAFT/PENDING/VERIFIED/REJECTED) | Citizen Report = triage status (PENDING/PROMOTED/DISMISSED) | Always qualify: "verification status" vs "triage status" |
| "Import" | Incident Management = AFOR batch import | Data pipeline = database migration | Use "AFOR Import" for data, "Migration" for schema changes |

---

## Anti-Terms (What These Do NOT Mean)

| Term | Does NOT mean |
|------|---------------|
| "Incident" | Does NOT mean a Suricata network alert, a bug report, or a system error |
| "Report" | Does NOT mean a log entry, an analytics export, or a thesis chapter |
| "Region" | Does NOT mean a cloud region, a deployment zone, or a database partition |
| "Batch" | Does NOT mean a Docker container, a background job, or a test suite |
| "Validation" | Does NOT mean input validation, schema validation, or test validation |
| "Encoder" | Does NOT mean a character encoding, a video encoder, or a data transformer |
| "AFOR" | Does NOT mean a generic form, a PDF template, or a web form |

---

## Changelog

| Date | Change | Reason |
|------|--------|--------|
| 2026-04-26 | Initial creation | Mac Poynton talk triggered ubiquitous language review |
