---
id: mitre-attack-command-sheet-001
type: source
created: 2026-04-10
updated: 2026-04-10
last_verified: 2026-04-10
review_after: 2026-07-10
stale_after: 2026-10-10
confidence: medium
source_refs:
  - raw/misc/Command Sheet/
status: active
tags:
  - mitre-attack
  - kill-chain
  - command-reference
  - cybersecurity
related:
  - sources/cybersecurity/ctf-writeups-hackthebox
  - sources/cybersecurity/ctf-writeups-tryhackme
  - mocs/cybersecurity
---

# MITRE ATT&CK Command Sheet

**Source:** `raw/misc/Command Sheet/`
**Count:** 4 files
**Format:** Kill chain phase references

---

## Kill Chain Phases

| Phase | File | Content |
|---|---|---|
| Reconnaissance | `Reconnaisance.md` | Initial information gathering |
| Weaponization | `Weaponization.md` | Payload creation |
| Exploitation | `Exploitation.md` | Vulnerability exploitation |
| Action on Objectives | `Action on Objectives.md` | Post-exploitation goals |

---

## Notes

These files are minimal references — mostly phase names with Obsidian wikilinks to the next phase. They follow the MITRE ATT&CK kill chain structure.

**Obsidian tags:** `[[Weaponization]]`, `[[Action on Objectives]]`, etc.

---

## Connection to Other Sources

The CTF writeups demonstrate these phases in practice:
- Reconnaissance: Nmap scans, service enumeration (HTB: Funnel, Redeemer)
- Exploitation: SQL injection (Appointment), FTP access (Crocodile), SSH tunneling (Funnel)
- Action on Objectives: Flag capture, privilege escalation, data exfiltration

---

## Related

- [[sources/cybersecurity/ctf-writeups-hackthebox]] — Practical demonstrations
- [[sources/cybersecurity/ctf-writeups-tryhackme]] — More demonstrations
- [[mocs/cybersecurity]] — Cybersecurity Map of Content
