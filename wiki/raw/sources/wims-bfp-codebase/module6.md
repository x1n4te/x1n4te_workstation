## Module 6: Cryptographic Security

### A. Data-at-Rest Encryption

1. All sensitive incident data stored in Central Database shall be encrypted — `SQLAlchemy TypeDecorator`
2. Encryption applied to:
    - Incident narratives
    - Casualty details
    - Property damage estimates
    - File attachments
3. Encryption keys managed by dedicated key management service — `OpenBao (Docker)`
4. Key rotation performed every 90 days — `OpenBao Auto-Rotate`

### B. Data-in-Transit Encryption

1. All network communication shall use TLS 1.3 — `Nginx / Traefik`
2. Enforce HTTPS for all web traffic
3. Disable weak cipher suites (only AES-256-GCM and ChaCha20-Poly1305 allowed) — `Nginx Configuration`
4. HTTP Strict Transport Security (HSTS) for API endpoints to prevent MITM attacks. — `Expect-CT / HSTS`