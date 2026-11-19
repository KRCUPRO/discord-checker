# ⚡ D4UC (`discord-checker`) v12.4.0

## 🧭 What's New in v12.4.0: Two-Way Document Navigation & Complete OS Guides Suite

### 1. Two-Way Document Navigation (TOC Anchor Links & Return-to-Top Navigation)
- **Full Interactive Table of Contents (TOC)**:
  - Added complete, jumpable Table of Contents (`## 📑 `) with working anchor links across `README.md`, all 11 locale documents in `docs/locales/` (`ko.md`, `ja.md`, `zh-CN.md`, `es.md`, `fr.md`, `de.md`, `ru.md`, `pt-BR.md`, `ar.md`, `hi.md`, `id.md`), and all OS guides.
  - Every single section header is equipped with direct anchor IDs (`<a id="...">`) for universal compatibility across GitHub, GitLab, and local Markdown viewers.
- **Localized Clean Return-to-Top Links**:
  - Under every single section block, a localized return link jumps instantly back to the top Table of Contents:
    * Korean: `[⬆️ 목차 맨 위로 이동](#-목차)`
    * English: `[⬆️ Back to Top](#-table-of-contents)`
    * Japanese: `[⬆️ 目次へ戻る](#-目次)`
    * Chinese: `[⬆️ 返回顶部目录](#-目录)`
    * Spanish: `[⬆️ Volver al inicio](#-tabla-de-contenidos)`
    * French: `[⬆️ Haut de page](#-table-des-matières)`
    * German: `[⬆️ Nach oben](#-inhaltsverzeichnis)`
    * Russian: `[⬆️ Наверх к оглавлению](#-содержание)`
    * Portuguese: `[⬆️ Voltar ao topo](#-índice)`
    * Arabic: `[⬆️ العودة إلى أعلى الفهرس](#-جدول-المحتويات)`
    * Hindi: `[⬆️ सामग्री सूची पर वापस जाएं](#-सामग्री-तालिका)`
    * Indonesian: `[⬆️ Kembali ke Daftar Isi](#-daftar-isi)`
- **Bidirectional Footnote Navigation**:
  - Embedded bidirectional footnote anchors `[^1]` / `[^2]` with clean return references (`↩`) for deep technical citations.

### 2. Dedicated OS & Platform Comprehensive Guides Suite (`docs/guides/`)
- **`WINDOWS_GUIDE.md`**: Complete Windows 10 & 11 guide covering the 4 standalone executables (`.exe`), Windows Defender SmartScreen instructions, one-click PowerShell firewall scripts (ports 5000 / 1081+), Python 3.12 source setup, and Task Scheduler 24/7 background runner.
- **`MACOS_GUIDE.md`**: Apple Silicon (M1/M2/M3/M4) & Intel x86_64 setup, Homebrew package management, native `curl_cffi` BoringSSL acceleration, Safari "Add to Dock" macOS Web App, and `launchd` background daemon.
- **`LINUX_GUIDE.md`**: Ubuntu (20.04/22.04/24.04), Debian (11/12), Kali, Fedora, Arch Linux packages, systemd 24/7 service unit (`d4uc.service`), `tmux`/`screen` multiplexer, and UFW/iptables firewall rules.
- **`ANDROID_GUIDE.md`**: 1-Tap native `.apk` installation (`DiscordUsernameChecker_v12.3.0.apk`), One UI / HyperOS / Pixel battery optimization exclusion, Wake Lock management, and Termux PRoot Debian fallback runner.
- **`IOS_GUIDE.md`**: Apple Safari PWA "Add to Home Screen" borderless touch app, 0.1s Discord Webhook push notifications, and Termius / Blink SSH management.
- **`DOCKER_GUIDE.md`**: Multi-Arch Docker Compose (`amd64`, `arm64`), 2-shard multi-container setup, volume persistence (`./data:/app/data`), and environment variable matrix.
- **`RASPBERRY_PI_GUIDE.md`**: Raspberry Pi 4 & 5 (Debian Bookworm ARM64) 3W homelab setup, Tailscale mesh remote control, and SD card WAL I/O protection.
- **`docs/guides/README.md` & `docs/README.md`**: Comprehensive master index linking all platform manuals, architecture specs, and 11 locale documents.

### 3. Concrete Evidence Verification (Deliverables 12 & 13)
- Extended `tests/test_deliverables_verification.py` with Deliverables 12 & 13:
  - 100% automated validation of 2-way TOC anchors, return links, and footnotes across all 12 docs.
  - 100% automated validation of all 13 OS guide manuals and documentation hubs.
  - Test suite passes with Exit Code 0.

---

## 📦 Attached Deliverable Binaries
- `DiscordUsernameChecker_v12.3.0.apk`: Android Smartphone 1-Tap Package (Signed v1/v2/v3)
- `DiscordUsernameCheckerV2_Web.exe`: Mobile Web GUI & PWA HTTP Server (Windows 64-bit)
- `DiscordUsernameCheckerV2_KO.exe`: Korean Desktop GUI (CustomTkinter)
- `DiscordUsernameCheckerV2_EN.exe`: English Desktop GUI (CustomTkinter)
- `DiscordUsernameCheckerV2_CLI.exe`: Headless CLI Dashboard (Rich)
