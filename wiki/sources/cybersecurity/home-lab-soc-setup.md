---
id: home-lab-soc-setup-001
type: source
created: 2026-04-10
updated: 2026-04-10
last_verified: 2026-04-10
review_after: 2026-07-10
stale_after: 2026-10-10
confidence: high
source_refs:
  - raw/misc/Home-Lab-Journey/SOC-SETUP/
status: active
tags:
  - home-lab
  - soc
  - wazuh
  - siem
  - cybersecurity
  - qemu
  - kvm
related:
  - sources/cybersecurity/ctf-writeups-tryhackme
  - mocs/cybersecurity
---

# Home Lab — SOC Setup

**Source:** `raw/misc/Home-Lab-Journey/SOC-SETUP/`
**Date:** November 21, 2025
**Status:** WIP (at time of writing)

---

## Infrastructure

| Component | Technology | Purpose |
|---|---|---|
| Hypervisor | QEMU/KVM + virt-manager | VM hosting |
| Windows VM | Windows 10 LTSC Enterprise | Target machine for SOC monitoring |
| Ubuntu Server VM | Ubuntu Server | Wazuh SIEM host |
| SIEM | Wazuh (Docker) | Security monitoring and alerting |

---

## Setup Steps (Documented)

### 1. Hypervisor Setup
- Downloaded QEMU/KVM and virt-manager
- Installed Windows 10 LTSC Enterprise from massgrave
- License reset: `slmgr /rearm` (90-day timer, max 3 resets)

### 2. Ubuntu Server Setup
- Installed Ubuntu Server
- Fixed networking: created `/etc/netplan/01-netcfg.yaml`:
  ```yaml
  network:
    version: 2
    renderer: networkd
    ethernets:
      enp1s0:
        dhcp4: true
  ```

### 3. Wazuh Deployment (Docker)
- Generated certificates: `docker compose -f generate-indexer-certs.yml run --rm generator`
- Single-node deployment (all components in one stack)
- Started with `docker compose up -d` (sudo required)
- Components: Wazuh Indexer, Manager, Dashboard

### 4. Network Configuration
- SOC Wazuh IP: `192.168.122.7`
- Dashboard accessible via browser

---

## Lessons Learned

- Ubuntu Server networking requires manual netplan configuration in some VM setups
- Wazuh Docker deployment needs sudo for certificate generation
- Single-node deployment is sufficient for home lab SOC
- Windows LTSC can be re-armed 3 times (270 days total free usage)

---

## Related

- [[sources/cybersecurity/ctf-writeups-tryhackme]] — CTF challenges
- [[mocs/cybersecurity]] — Cybersecurity Map of Content
