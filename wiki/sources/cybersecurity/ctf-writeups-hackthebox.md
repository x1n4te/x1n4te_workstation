---
id: ctf-writeups-hackthebox-001
type: source
created: 2026-04-10
updated: 2026-04-10
last_verified: 2026-04-10
review_after: 2026-07-10
stale_after: 2026-10-10
confidence: high
source_refs:
  - raw/misc/Writeups/HTB Writeups/
status: active
tags:
  - ctf
  - hackthebox
  - cybersecurity
  - writeups
  - practical
related:
  - sources/cybersecurity/ctf-writeups-tryhackme
  - mocs/cybersecurity
---

# HackTheBox Writeups

**Source:** `raw/misc/Writeups/HTB Writeups/`
**Count:** 16 writeups
**Date range:** ~Dec 2025
**Difficulty:** Starting Point / Very Easy

---

## Writeups

| Box | Topic | Key Skills |
|---|---|---|
| Funnel | FTP creds → SSH → PostgreSQL tunneling | SSH port forwarding, local/dynamic tunneling, PostgreSQL enumeration |
| Redeemer | Redis exploitation | Redis enumeration, key-value store exploitation |
| Appointment | SQL injection | SQLi, database enumeration |
| Synced | Rsync misconfiguration | Rsync enumeration, file access |
| Responder | LLMNR/NBT-NS poisoning | Responder tool, credential capture |
| Three | Web exploitation | Web enumeration, privilege escalation |
| Previous | Service enumeration | Port scanning, service exploitation |
| Explosion | RDP exploitation | RDP access, Windows enumeration |
| Crocodile | FTP + web exploitation | FTP anonymous access, web enumeration |

---

## Funnel Writeup (Detailed Example)

**Attack chain:**
1. Port scan: 21 (FTP), 22 (SSH)
2. FTP anonymous access → found `mail_backup/` directory
3. PDF with password policy + email with user list
4. Default password `funnel123#!#` → SSH access
5. PostgreSQL on localhost:5432 (not accessible externally)
6. SSH local port forwarding: `ssh -L 5433:localhost:5432 christine@<IP>`
7. PostgreSQL enumeration → flag in database

**Key learning:** SSH tunneling (local vs dynamic), PostgreSQL client commands, default credential exploitation.

---

## Format

Frontmatter with Obsidian tags:
```yaml
date: 2025-12-29
status: #completed
platform: HTB Starting Point
difficulty: VERY EASY
tags: Linux ftp SSH PostgreSQL
```

Sections: First Look → Exploit → Questions → Further Improvements

---

## Skills Demonstrated

- SSH (port forwarding, local/dynamic tunneling)
- FTP enumeration and anonymous access
- PostgreSQL client (connect, enumerate, query)
- SQL injection
- Redis enumeration
- LLMNR/NBT-NS poisoning (Responder)
- RDP exploitation
- Web application security

---

## Related

- [[sources/cybersecurity/ctf-writeups-tryhackme]] — THM writeups
- [[mocs/cybersecurity]] — Cybersecurity Map of Content
