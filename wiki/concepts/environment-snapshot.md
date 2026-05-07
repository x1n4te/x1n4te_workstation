---
id: environment-snapshot-001
type: concept
created: 2026-04-08
updated: 2026-04-08
last_verified: 2026-04-08
review_after: 2026-07-08
stale_after: 2026-10-08
confidence: high
source_refs:
  - ~/
  - ~/.hermes/config.yaml
status: active
tags:
  - environment
  - hardware
  - arch-linux
related:
  - entities/hermes-agent-setup
---

# Environment Snapshot

**Captured:** 2026-04-08

---

## Hardware

Related: [[entities/hermes-agent-setup]], [[concepts/secure-coding-practices]]

| Component | Spec |
|-----------|------|
| **CPU** | Intel Core i5-9300H @ 2.40GHz (4 cores / 8 threads) |
| **RAM** | 19 GB |
| **GPU (integrated)** | Intel UHD Graphics 630 |
| **GPU (dedicated)** | NVIDIA GeForce GTX 1050 3 GB Max-Q |
| **Storage** | 476.9 GB NVMe (nvme0n1) + 7.4 GB (sda) |
| **Swap** | zram0 9.7 GB |

**Note:** GTX 1050 Max-Q has 3GB VRAM — sufficient for Qwen2.5-3B quantized, tight for larger models.

---

## Software

| Component | Version/Detail |
|-----------|----------------|
| **OS** | Arch Linux (rolling) |
| **Kernel** | 6.19.10-zen1-1-zen (Zen kernel, PREEMPT_DYNAMIC) |
| **Shell** | zsh |
| **Terminal** | Kitty (xterm-kitty) |
| **Display Server** | Wayland |
| **Window Manager** | Hyprland (per skill: hyprland-nvidia-arch-setup) |

---

## Hermes Configuration

| Setting | Value |
|---------|-------|
| **Orchestrator** | xiaomi/mimo-v2-pro (Nous Portal, free-tier) |
| **Auxiliary** | xiaomi/mimo-v2-pro (Nous Portal, free-tier) |
| **Primary Gateway** | Telegram (remote/mobile) |
| **Primary Interface** | CLI (localhost) |
| **Vault** | ~/Documents/x1n4te-workstation/ |
| **Hermes Config** | ~/.hermes/config.yaml |

---

## Known Constraints

- **Terminal image paste:** Not supported on Linux. Use Telegram as image pipeline or save-to-file workflow.
- **VRAM:** 3 GB — local LLM inference limited to small quantized models (Qwen2.5-3B or smaller).
- **Wayland:** Some X11-specific tools won't work natively. Use `grim`/`slurp` for screenshots, not `scrot`.
- **Zen kernel:** Low-latency scheduling. Good for desktop responsiveness, no impact on hermes.

---

## Update Log

| Date | Change |
|------|--------|
| 2026-04-08 | Initial snapshot |
