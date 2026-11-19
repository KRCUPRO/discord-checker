<div align="center">

# 📖 D4UC Project Master Guide (GUIDE.md)

> **High-Performance Discord Rare Username Availability Engine powered by Chrome 131 TLS Stealth, Surfshark 1:1 Multi-Tunnel Pool, and SQLite WAL Multi-Process Synchronization**

<br />

| [KR 한국어](../ko/GUIDE.md) | [US English](./GUIDE.md) | [JP 日本語](../ja/GUIDE.md) | [CN 简体中文](../zh-CN/GUIDE.md) | [ES Español](../es/GUIDE.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/GUIDE.md) | [DE Deutsch](../de/GUIDE.md) | [RU Русский](../ru/GUIDE.md) | [BR Português](../pt-BR/GUIDE.md) | [SA العربية](../ar/GUIDE.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/GUIDE.md">HI हिन्दी</a> • <a href="../id/GUIDE.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: Nov 19, 2026](../../assets/badges/update_badge_en.svg)](./CHANGELOG.md)
[![Guide Version](https://img.shields.io/badge/Guide-v12.5.0-blue.svg)](./GUIDE.md)

</div>

---

<a id="-table-of-contents"></a>
## 📑 Table of Contents
1. [1. Project Overview & Core Architecture](#-1-project-overview--core-architecture)
2. [2. Operating System & Platform Dedicated Guides](#-2-operating-system--platform-dedicated-guides)
3. [3. Quick Start by Major Environment](#-3-quick-start-by-major-environment)
4. [4. 8 Candidate Username Generation Modes](#-4-8-candidate-username-generation-modes)
5. [5. Proxy Infrastructure & Multi-Country Tunnels](#-5-proxy-infrastructure--multi-country-tunnels)
6. [6. Multi-Window & Multi-Container Sharding](#-6-multi-window--multi-container-sharding)
7. [7. GitHub Safe Deployment & Security Invariants](#-7-github-safe-deployment--security-invariants)
8. [8. Code Architecture & Developer Maintenance Guide](#-8-code-architecture--developer-maintenance-guide)
9. [9. Footnotes & Technical References](#-9-footnotes--technical-references)

---

<a id="-1-project-overview--core-architecture"></a>
## 1. 1. Project Overview & Core Architecture

- **Engine Target Endpoint**: `https://discord.com/api/v9/unique-username/username-attempt-unauthed`
- **Core Technological Invariants**:
  1. <a id="fnref-1"></a><a id="fnref1"></a>**Chrome 131 TLS JA3/JA4 Stealth Impersonation** (`curl_cffi`)[^1].
  2. <a id="fnref-2"></a><a id="fnref2"></a>**Surfshark 1:1 Isolated Multi-Tunnel Pool** (`wireproxy`)[^2].
  3. **0.3s Atomic 429 Hot-Swap**: Uninterrupted continuous scanning across alternate global countries.
  4. **Free Public Proxy Scraper & Live Multi-Threaded Validator** (`src/proxy/free_proxy.py`).
  5. **SQLite WAL Concurrency**: Multi-process safe state synchronization without database locks.

[⬆️ Return to Top](#-table-of-contents)

---

<a id="-2-operating-system--platform-dedicated-guides"></a>
## 2. 2. Operating System & Platform Dedicated Guides

- 🪟 [Windows Guide (WINDOWS_GUIDE.md)](../../guides/WINDOWS_GUIDE.md): 4 Standalone EXEs, Windows Firewall, Task Scheduler 24/7.
- 🍏 [macOS Guide (MACOS_GUIDE.md)](../../guides/MACOS_GUIDE.md): Apple Silicon M1-M4 & Intel, Homebrew, `launchd` automation.
- 🐧 [Linux Guide (LINUX_GUIDE.md)](../../guides/LINUX_GUIDE.md): Ubuntu, Debian, systemd service, tmux/screen background execution.
- 🤖 [Android Guide (ANDROID_GUIDE.md)](../../guides/ANDROID_GUIDE.md): 1-Tap native APK, Wake Lock management, Termux PRoot.
- 📱 [iOS Guide (IOS_GUIDE.md)](../../guides/IOS_GUIDE.md): Safari PWA Home Screen App, 0.1s Discord Webhook push notifications.
- 🐳 [Docker Guide (DOCKER_GUIDE.md)](../../guides/DOCKER_GUIDE.md): Multi-Arch Docker Compose 2-shard acceleration.
- 🍓 [Raspberry Pi Guide (RASPBERRY_PI_GUIDE.md)](../../guides/RASPBERRY_PI_GUIDE.md): 3W low-power homelab 24/7 setup.
- 🧭 [Guides Hub (docs/guides/README.md)](../../guides/README.md) & [Docs Hub (docs/README.md)](../../README.md)

[⬆️ Return to Top](#-table-of-contents)

---

<a id="-3-quick-start-by-major-environment"></a>
## 3. 3. Quick Start by Major Environment

### A. Desktop GUI (Windows & macOS)
```bash
python src/gui_ko.py   # Korean GUI
python src/gui_en.py   # English GUI
```

### B. Mobile Touch Web GUI & PWA
```bash
python src/web_gui.py --port 5000
# Open http://<LOCAL_IP>:5000 on mobile browser or tap 'Add to Home Screen'
```

### C. Android 1-Tap Standalone APK
- Install `dist/DiscordUsernameChecker_v12.3.0.apk` directly on Android 8.0+.

### D. Headless Rich CLI (Linux / Server)
```bash
python src/run.py --mode hybrid --length 4 --workers 10 --proxy free
```

### E. Multi-Arch Docker Compose
```bash
docker compose -f deploy/docker-compose.yml up -d
```

[⬆️ Return to Top](#-table-of-contents)

---

<a id="-4-8-candidate-username-generation-modes"></a>
## 4. 4. 8 Candidate Username Generation Modes

1. **Hybrid**: Combines dictionary bases, consonant-vowel combinations, and alphanumeric affixes.
2. **Permutation**: Pure combinatorial math engine (`[a-z0-9_.]^N`).
3. **Dictionary**: Real word frequency dictionary matching.
4. **Pattern**: Custom regex pattern matching (`a*b?`, `kr_*`).
5. **Numeric**: Consecutive and rare numerical combinations (`0001`~`9999`).
6. **Custom Mask**: Precise position-by-position character masking.
7. **Combinatorial**: User-defined prefix + base + suffix combinations.
8. **Recheck**: Scans previously verified or taken database history.

[⬆️ Return to Top](#-table-of-contents)

---

<a id="-5-proxy-infrastructure--multi-country-tunnels"></a>
## 5. 5. Proxy Infrastructure & Multi-Country Tunnels

- **Surfshark WireGuard Multi-Tunnel**: Maps 142 global server clusters to local ports `127.0.0.1:1081~1085`.
- **Free Public Proxy Scraper**: Aggregates from 18 verified open-source endpoints with Cloudflare trace pre-validation.
- **Tor & User Proxies**: SOCKS5 and HTTP proxy list rotation support.

[⬆️ Return to Top](#-table-of-contents)

---

<a id="-6-multi-window--multi-container-sharding"></a>
## 6. 6. Multi-Window & Multi-Container Sharding

Execute 2 to 4 parallel sharded instances with zero key collisions:
```bash
# Window 1 (Shard 1/2)
python src/run.py --mode permutation --shard 2_1 --length 4

# Window 2 (Shard 2/2)
python src/run.py --mode permutation --shard 2_2 --length 4
```

[⬆️ Return to Top](#-table-of-contents)

---

<a id="-7-github-safe-deployment--security-invariants"></a>
## 7. 7. GitHub Safe Deployment & Security Invariants

- Never commit `config.yaml`, `.env`, or `surfshark_credentials.json`.
- All credentials must be passed via environment variables or template files.
- Refer to [SECURITY.md](./SECURITY.md) for vulnerability reporting.

[⬆️ Return to Top](#-table-of-contents)

---

<a id="-8-code-architecture--developer-maintenance-guide"></a>
## 8. 8. Code Architecture & Developer Maintenance Guide

```text
src/
├── network/    # DiscordApiClient & Chrome 131 TLS handshake
├── proxy/      # UnifiedProxyManager, Surfshark, FreeProxyProvider
├── generator/  # 8 candidate generation algorithms
├── storage/    # SQLite WAL database & text mirrors
└── ui/         # Desktop CustomTkinter & Mobile Web GUI
```

[⬆️ Return to Top](#-table-of-contents)

---

<a id="-9-footnotes--technical-references"></a>
## 9. 9. Footnotes & Technical References

[^1]: <a id="fn-1"></a><a id="fn1"></a>The Chrome 131 BoringSSL handshake completely neutralizes TLS fingerprinting defenses deployed by Cloudflare and modern WAFs. [↩️ Return to Reference](#fnref-1)
[^2]: <a id="fn-2"></a><a id="fn2"></a>wireproxy is a lightweight user-space Go binary translating WireGuard protocol into isolated local SOCKS5 proxies without root privileges. [↩️ Return to Reference](#fnref-2)

[⬆️ Return to Top](#-table-of-contents)
