## Module 7: Intrusion Detection and Network Monitoring

### A. Network Traffic Mirroring

1. Internal Docker Network Traffic shall be monitored by the IDS (Intrusion Detection System) via a virtualized bridge interface — `Suricata AF_PACKET`
2. IDS shall monitor all inbound and outbound traffic routed through the Nginx Reverse Proxy on the VPS.
3. Mirrored traffic includes: — `Suricata App-Layer Parsers`
    - HTTP/HTTPS requests
    - Database queries
    - File uploads/downloads
    - Authentication attempts

### B. IDS Configuration

1. System shall use Suricata as the network-based IDS engine, deployed as a containerized service — `Suricata (Dockerized)`
2. Suricata shall be configured with: — `Suricata-Update Tool`
    - OWASP Top 10 vulnerability signatures
    - Custom BFP-specific rules (e.g., detect bulk incident deletion attempts)
    - Emerging Threats ruleset (updated weekly)
3. IDS shall generate Unstructured Logs for detected security events — `EVE JSON Format`
4. Unstructured logs shall be sent to System Logs data store

### C. Log Collection and Forwarding

1. IDS shall provide raw security logs to the Qwen2.5-3B AI module upon System Administrator request — `Filebeat / Volume Sharing`
2. Logs forwarded via "Feeds Unstructured Logs" data flow — `Redis (Message Broker)`
3. Log forwarding occurs in real-time (latency < 5 seconds) — `FastAPI Background Worker`