---
id: wims-bfp-codebase-pii-encryption-001
type: concept
created: 2026-04-21
updated: 2026-04-21
last_verified: 2026-04-21
review_after: 2026-06-21
stale_after: 2026-10-21
confidence: high
source_refs:
  - raw/sources/wims-bfp-codebase/docs/SECURITY.md
status: active
tags:
  - wims-bfp
  - security
  - encryption
related:
  - entities/wims-bfp-codebase-database-schema
  - concepts/wims-bfp-codebase-threat-model
  - concepts/wims-bfp-codebase-rls-model
---

# PII Encryption

AES-256-GCM encryption for sensitive fields at rest. RA 10173 compliance.

## Mechanism

`src/backend/utils/crypto.py` — `SecurityProvider` class using AES-256-GCM.

```python
class SecurityProvider:
    def __init__(self, master_key: bytes):
        self.master_key = master_key  # 32-byte key from WIMS_MASTER_KEY env var

    def encrypt(self, plaintext: str) -> bytes:
        # Generates random 12-byte nonce
        # Encrypts with AES-256-GCM
        # Returns: nonce + ciphertext + tag (concatenated)

    def decrypt(self, ciphertext: bytes) -> str:
        # Splits nonce, ciphertext, tag
        # Decrypts with AES-256-GCM
        # Returns plaintext
```

## Encrypted Fields

| Table | Column | Field Type |
|-------|--------|------------|
| `incident_sensitive_details` | `pii_blob_enc` | Encrypted blob (all PII) |
| `incident_sensitive_details` | `narrative_enc` | Encrypted narrative |
| `incident_attachments` | `file_data_enc` | Encrypted file content |

## Key Management

| Aspect | Current | Target |
|--------|---------|--------|
| Key source | `WIMS_MASTER_KEY` env var | OpenBao (Docker) |
| Key rotation | None | Every 90 days |
| Key format | Base64-encoded 32-byte | Same |
| TLS | Manual config | Nginx SSL termination |

## Related

- [[entities/wims-bfp-codebase-database-schema]] — tables with encrypted columns
- [[concepts/wims-bfp-codebase-threat-model]] — STRIDE mitigation
- [[concepts/wims-bfp-codebase-rls-model]] — access control layer
