---
id: celery-redis-security-2026-001
type: source
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-05-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - reintech.io/blog/securing-celery-safe-task-processing
  - redis.io/docs/latest/operate/rs/security/recommended-security-practices
status: active
tags:
  - celery
  - redis
  - task-queue
  - security
  - software-dev
related:
  - sources/software-dev/fastapi-security-best-practices
  - sources/software-dev/fastapi-cves-2025-2026
  - concepts/fastapi-security-wims-bfp
  - concepts/docker-security-wims-bfp
  - mocs/cybersecurity
---

# Celery + Redis Security (Source Summary)

**Sources:** Reintech, Redis Official Docs
**Type:** Task queue and message broker security
**Confidence:** High — vendor best practices + community experience

---

## 6 Security Layers for Celery + Redis

| Layer | Focus | Key Controls |
|---|---|---|
| **Transport** | Message encryption | TLS on broker connection |
| **Credentials** | Secret management | File-based secrets, not env vars |
| **Time Limits** | Resource exhaustion prevention | soft + hard time limits on tasks |
| **Serialization** | Message signing | JSON only, no pickle |
| **Network** | Access control | Internal network, no public ports |
| **Concurrency** | Worker resource limits | max_memory_per_child, max_tasks_per_child |

---

## 1. TLS on Broker Connection

```python
# celery_config.py

# Redis (v6.0+)
broker_url = 'rediss://redis:6380/0'  # Note 'rediss' (TLS)
broker_use_ssl = {
    'ssl_cert_reqs': ssl.CERT_REQUIRED,
    'ssl_ca_certs': '/run/secrets/redis_ca_cert',
    'ssl_certfile': '/run/secrets/redis_client_cert',
    'ssl_keyfile': '/run/secrets/redis_client_key',
}

# RabbitMQ (alternative)
broker_url = 'amqp://user:pass@rabbitmq:5671//'
broker_use_ssl = {
    'keyfile': '/run/secrets/rabbitmq_key',
    'certfile': '/run/secrets/rabbitmq_cert',
    'ca_certs': '/run/secrets/rabbitmq_ca',
    'cert_reqs': ssl.CERT_REQUIRED,
}
```

---

## 2. Time Limits (Resource Exhaustion Prevention)

```python
# Global defaults
app.conf.task_time_limit = 300           # 5 min hard limit (SIGKILL)
app.conf.task_soft_time_limit = 240      # 4 min soft limit (SoftTimeLimitExceeded exception)

# Per-task override
@app.task(time_limit=600, soft_time_limit=540)
def process_large_dataset(data):
    try:
        # Processing logic
        pass
    except SoftTimeLimitExceeded:
        cleanup_partial_work()
        raise
```

**WIMS-BFP specific:**
- Suricata ingestion: 60s soft, 120s hard (Eve JSON parsing)
- Report generation: 240s soft, 300s hard (complex queries)
- Email notifications: 30s soft, 60s hard (external SMTP)

---

## 3. Disable Pickle Serialization (Security Risk)

```python
# NEVER use pickle — allows arbitrary code execution
from kombu import serialization

app.conf.update(
    task_serializer='json',       # JSON only
    accept_content=['json'],      # Reject all other formats
    result_serializer='json',
)
```

---

## 4. Worker Resource Limits

```python
app.conf.worker_max_memory_per_child = 200000  # 200MB per child process
app.conf.worker_max_tasks_per_child = 1000     # Restart after 1000 tasks (memory leak prevention)
```

### Concurrency Recommendations

| Task Type | Concurrency | Pool |
|---|---|---|
| CPU-intensive | CPU cores | prefork |
| I/O-bound | 2-4x CPU cores | gevent/eventlet |
| Memory-intensive | Based on available RAM | prefork |

---

## 5. Network Isolation

```
# NEVER expose Redis or RabbitMQ to the public internet
# docker-compose.yml
networks:
  backend:
    driver: bridge
    internal: true  # No internet access

services:
  redis:
    networks: [backend]
    # NO ports published to host
  celery:
    networks: [backend]
    depends_on: [redis, postgres]
```

---

## 6. Redis Security

### Authentication

```bash
# redis.conf
requirepass your_strong_password_here

# Docker Compose
command: redis-server --requirepass "$(cat /run/secrets/redis_password)"
```

### Redis Security Checklist

```
[ ] requirepass enabled
[ ] TLS on Redis connection (rediss://)
[ ] bind to internal network only (not 0.0.0.0)
[ ] rename-command FLUSHALL ""  # Disable dangerous commands
[ ] rename-command FLUSHDB ""
[ ] rename-command DEBUG ""
[ ] maxmemory configured (prevent OOM)
[ ] maxmemory-policy allkeys-lru (eviction policy)
```

---

## Celery Security Checklist

```
[ ] TLS on broker connection (rediss://)
[ ] JSON serializer only (no pickle)
[ ] Time limits on all tasks
[ ] max_memory_per_child configured
[ ] max_tasks_per_child configured
[ ] Broker password in secrets file (not env var)
[ ] Worker on internal network only
[ ] Beat scheduler: run only on trusted hosts
[ ] Task results: expire after 24 hours
[ ] Monitoring: task failure rates, resource usage
```

---

## WIMS-BFP Specific Configuration

```python
# celery_config.py for WIMS-BFP

import ssl

broker_url = 'rediss://redis:6380/0'
result_backend = 'rediss://redis:6380/1'

# TLS
broker_use_ssl = {
    'ssl_cert_reqs': ssl.CERT_REQUIRED,
    'ssl_ca_certs': '/run/secrets/redis_ca_cert',
}

# Security
task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'

# Resource limits
task_time_limit = 300
task_soft_time_limit = 240
worker_max_memory_per_child = 200000
worker_max_tasks_per_child = 1000

# Result expiry
result_expires = 86400  # 24 hours

# Suricata beat task (svc_suricata service account)
beat_schedule = {
    'ingest-suricata-eve': {
        'task': 'celery_tasks.ingest_suricata_eve',
        'schedule': 10.0,  # every 10 seconds
    },
}
```

---

## Related Pages

- [[sources/software-dev/fastapi-security-best-practices]] — FastAPI security reference
- [[sources/software-dev/fastapi-cves-2025-2026]] — FastAPI CVEs
- [[concepts/fastapi-security-wims-bfp]] — WIMS-BFP FastAPI security synthesis
- [[concepts/docker-security-wims-bfp]] — Docker Compose security
- [[mocs/cybersecurity]] — Cybersecurity Map of Content
