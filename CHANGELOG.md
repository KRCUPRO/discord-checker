# Changelog

All notable changes to **D4UC (`discord-checker`)** are documented in this file.

| [KR 한국어](./docs/locales/ko/CHANGELOG.md) | [US English](./CHANGELOG.md) | [JP 日本語](./docs/locales/ja/CHANGELOG.md) | [CN 简体中文](./docs/locales/zh-CN/CHANGELOG.md) | [ES Español](./docs/locales/es/CHANGELOG.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](./docs/locales/fr/CHANGELOG.md) | [DE Deutsch](./docs/locales/de/CHANGELOG.md) | [RU Русский](./docs/locales/ru/CHANGELOG.md) | [BR Português](./docs/locales/pt-BR/CHANGELOG.md) | [SA العربية](./docs/locales/ar/CHANGELOG.md) |

<p align="center"><sub>🌐 Also available: <a href="./docs/locales/hi/CHANGELOG.md">HI हिन्दी</a> • <a href="./docs/locales/id/CHANGELOG.md">ID Bahasa Indonesia</a></sub></p>

## [v12.5.0] — 2026-11-19

### Added
- **12-Language 1:1 Complete Documentation Suite (`docs/locales/<lang>/`)**:
  - Full 1:1 professional localization for all 8 core documents across 12 languages (Korean, English, Japanese, Simplified Chinese, Spanish, French, German, Russian, Portuguese, Arabic, Hindi, Indonesian).
  - Clean modular hierarchy: `docs/locales/<lang>/` housing `README.md`, `ARCHITECTURE_MAP.md`, `GUIDE.md`, `TASKS.md`, `CHANGELOG.md`, `LICENSE.md`, `NOTICE.md`, `SECURITY.md`.
- **GitHub Repository Root Streamlining & Modular Reorganization**:
  - Moved internal maintenance scripts to `deploy/scripts/` and test configuration to `tests/pytest.ini`.
  - Removed duplicate root scripts, reducing root clutter to 6 directories and 8 essential files so README and preview media render prominently above the fold on GitHub.
- **Above-the-Fold Quick Jump Navigation Bar**:
  - Instant one-touch navigation bar below badge strip (`[ Previews | Features | Requirements | Quick Start | Mobile PWA | Architecture | OS Guides | License ]`).

## [v12.4.0] — 2026-11-19

### Added
- **Two-Way Document Navigation (TOC Anchor Links & Return-to-Top Navigation)**:
  - Full interactive Table of Contents (TOC) with working anchor links added to `README.md`, all 11 locale documents in `docs/locales/` (`ko.md`, `ja.md`, `zh-CN.md`, `es.md`, `fr.md`, `de.md`, `ru.md`, `pt-BR.md`, `ar.md`, `hi.md`, `id.md`), and all OS guides.
  - Every single section header equipped with direct anchor IDs and localized clean `[⬆️ Return to Top]` links returning to the TOC.
  - Bidirectional footnote jumping `[^1]` / `[^2]` with clean return references (`↩`).
- **Dedicated OS & Platform Comprehensive Guides (`docs/guides/`)**:
  - `WINDOWS_GUIDE.md`: Complete Windows 10/11 setup, 4 standalone EXEs, Defender & firewall PowerShell script (ports 5000 / 1081+), Python source setup, Task Scheduler 24/7 background autorun.
  - `MACOS_GUIDE.md`: Apple Silicon (M1-M4) & Intel x86_64 setup, Homebrew, BoringSSL `curl_cffi` native acceleration, Safari Dock Web App, `launchd` background daemon.
  - `LINUX_GUIDE.md`: Ubuntu, Debian, Kali, Fedora, Arch Linux packages, `systemd` unit service (`d4uc.service`), `tmux`/`screen` multiplexer, UFW/iptables rules, multi-shard scanning.
  - `ANDROID_GUIDE.md`: 1-Tap native APK installation (`DiscordUsernameChecker_v12.3.0.apk`), One UI / HyperOS / Pixel battery optimization exclusion, Wake Lock management, Termux PRoot Debian runner.
  - `IOS_GUIDE.md`: Safari PWA "Add to Home Screen" borderless touch app, 0.1s Discord Webhook push notifications, Termius / Blink SSH management.
  - `DOCKER_GUIDE.md`: Multi-Arch Docker Compose (`amd64`, `arm64`), 2-shard multi-container setup, volume persistence (`./data:/app/data`), environment variable matrix.
  - `RASPBERRY_PI_GUIDE.md`: Raspberry Pi 4 & 5 (Debian Bookworm ARM64) 3W homelab setup, Tailscale mesh remote control, SD card WAL I/O protection.
  - `docs/guides/README.md` & `docs/README.md`: Central documentation hub and OS guides matrix linking all platform manuals, architecture specs, and locale documents.
- **Enhanced Concrete Evidence Deliverables Verification**:
  - Updated `tests/test_deliverables_verification.py` with Deliverables 12 & 13 verifying two-way navigation, TOC anchor integrity, return-to-top links, and all 13 OS guide manuals (100% passed, exit code 0).

## [v12.3.0] — 2026-11-19

### Added
- **Free Public Proxy Scraper & Live Multi-Threaded Validator (`src/proxy/free_proxy.py`)**:
  - Automated open-source candidate aggregation from 14+ continually updated GitHub repositories and Hugging Face datasets (TheSpeedX, monosans, hookzof, roosterkid, ShiftyTR, mertguvencli, Hugging Face).
  - Multi-protocol support across HTTP, HTTPS, SOCKS4, and SOCKS5 free proxies.
  - High-speed concurrent asynchronous validation against Discord unique-username API (`/api/v9/unique-username/username-attempt-unauthed`) and Cloudflare edge traces.
  - Automated filtering of dead nodes, latency exceeding 3,500ms, and 403 Cloudflare WAF blocks.
  - Round-robin proxy leasing with lowest-latency prioritization, 429 rate limit cooldown handling (15s), and background auto-refresher.
  - Clean integration into `UnifiedProxyManager` under mode `"free"` / `"free_public"`.
- **Desktop GUI Free Proxy Mode**:
  - Added `🌐 무료 프록시 자동 수집 (Free Public)` in proxy dropdown with live `[🔄 무료 프록시 수집 & 검증]` button and active count badge.
- **Mobile Touch Web GUI & PWA REST APIs**:
  - Added `Free Public` option to `#proxyMode`, 1-tap `🔄 무료 프록시 수집 & 검증` button with live polling telemetry.
  - New REST API endpoints: `POST /api/proxy/scrape` and `GET /api/proxy/free_status`.
- **Headless CLI Free Proxy Support**:
  - Support for `--proxy free` (or `-p free`) with automatic pre-flight scraping and validation before launching check workers.
- **Full Localization and Comprehensive Test Coverage**:
  - Documented in `README.md` and all 11 locale files in `docs/locales/`.
  - Added unit test suite `tests/test_free_proxy.py` and updated `tests/test_deliverables_verification.py` (95 passing tests, exit code 0).

## [v12.2.0] — 2026-11-19

### Added
- **Mobile Touch-Optimized Responsive Web GUI & PWA Engine (`src/ui/web/` / `src/web_gui.py`)**:
  - Full-featured, Discord-dark-themed responsive web interface accessible from any smartphone browser (iPhone Safari, Android Chrome) at `http://<host>:5000`.
  - Native **"Add to Home Screen" (PWA)** support via `manifest.json` and service worker (`sw.js`), launching as a borderless full-screen mobile app with app icons.
  - Large touch-optimized controls: Start / Stop / Restart buttons, live rolling RPS canvas speed curve, 1-tap username copy with toast feedback, and instant TXT / CSV / JSON export.
  - Mobile remote configuration: 8 username generation modes, target length (3–6), sharding, custom masks, proxy modes (Surfshark private keys, proxy files, Thordata), and dynamic worker slider (1–50) with live hot-scaling.
  - Zero external frontend dependencies: 100% self-contained HTML5, CSS3, and Vanilla JS.
- **Standalone Windows Executable for Web GUI (`DiscordUsernameCheckerV2_Web.exe`)**:
  - Added PyInstaller build target in `deploy/build_exe.py` compiling standalone Web GUI binary with embedded PWA assets.
- **1:1 Full Localization for ALL 11 Locale Documents (`docs/locales/*.md`)**:
  - Complete native 1:1 professional translation across all sections for Japanese (`ja.md`), Simplified Chinese (`zh-CN.md`), Spanish (`es.md`), French (`fr.md`), German (`de.md`), Russian (`ru.md`), Portuguese (`pt-BR.md`), Arabic (`ar.md`), Hindi (`hi.md`), and Indonesian (`id.md`).
- **12 Localized SVG Update Badges (`docs/assets/badges/`)**:
  - Pixel-perfect localized badges for Korean, English, Japanese, Chinese, Spanish, French, German, Russian, Portuguese, Arabic, Hindi, and Indonesian.
- **Mobile Web GUI Visual Media Assets**:
  - High-fidelity smartphone mockup screenshot (`docs/assets/mobile_web_main.png`) and animated touch demo GIF (`docs/assets/mobile_web_demo.gif`).

## [v12.1.0] — 2026-11-19

### Added
- **Strict Username Exclusion Rules**: Comprehensive validation preventing consecutive dots (`..`, e.g. `ab..`, `a..1`), leading/trailing dots (`.abc`, `abc.`), invalid symbols, and reserved terms across all candidate generators. Verified via 84 unit tests.
- **High-Fidelity Visual Documentation**: Generated pixel-perfect screenshots and animated GIFs with natural mouse-cursor movement in `docs/assets/` (`gui_ko_main.png`, `gui_ko_demo.gif`, `gui_en_main.png`, `gui_en_demo.gif`, `gui_settings_modal.png`, `cli_dashboard.png`, `cli_demo.gif`, `docker_linux_capture.png`).
- **Standardized Language Selector Grid**: Exact 5x2 bordered language selector table matching UI specifications across `README.md` and all 11 locale documents in `docs/locales/`.
- **Platform Deep-Dive Guides**: Added `docs/guides/MOBILE_IOS_GUIDE.md` (iOS sandbox limits & SSH/webhook bridge) and `docs/guides/PC_GUIDE.md` (Windows Defender firewall rules & macOS Homebrew setup).
- **Windows Standalone `.exe` Binaries**: Automated PyInstaller packaging for Python 3.12: `DiscordUsernameCheckerV2_KO.exe`, `DiscordUsernameCheckerV2_EN.exe`, and `DiscordUsernameCheckerV2_CLI.exe`.
- **SVG Status Badges**: Added `docs/assets/badges/update_badge.svg` and `update_badge_en.svg` tracking release timestamps.

## [v12.0.0] — 2026-11-19

### Added
- **Clean Modular Repository Structure**: Reorganized configuration (`config/`), deployment (`deploy/`), documentation (`docs/`), core runtime (`src/`), and regression suite (`tests/`).
- **12-Language Documentation Localization (`docs/locales/`)**: Full native documentation support for English, Korean, Japanese, Simplified Chinese, Spanish, German, French, Portuguese (Brazil), Russian, Hindi, Arabic, and Indonesian.
- **Proprietary Licensing & Security Hardening**: Added [LICENSE](LICENSE), [NOTICE](NOTICE), strict secret isolation, portable path resolution across Windows/Linux/Docker/Termux, and verified zero-leak repository audits.

### Core Platform Capabilities (v1.0 – v12.0 Architecture)
- **Chrome 131 TLS JA3/JA4 Impersonation**: Powered by `curl_cffi` BoringSSL async sessions with browser-matched headers.
- **1:1 Isolated Multi-Tunnel Pool**: User-space `wireproxy` tunnels mapped per worker across 142 global Surfshark clusters without altering OS-wide network routes.
- **0.3s Atomic 429 Hot-Swap**: Worker-level instant cluster cooldown & fresh node swap without stalling sibling workers.
- **8 Candidate Generators**: Hybrid, Permutation (mathematical 2/3/4-way sharding), Dictionary, Pattern/Symmetry, Numeric, Custom Mask, Combinatorial, and Recheck.
- **SQLite WAL Multi-Process Synchronization**: Concurrent GUI/Docker/CLI sharded instances sharing `data/d4uc_results.db` cleanly.
- **Cross-Platform Deployment**: CustomTkinter Desktop GUI (KO/EN), Headless Rich CLI, Android Termux (`proot-distro debian`), and Multi-Arch Docker Compose (`2shard` profile).
