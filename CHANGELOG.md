# Changelog

All notable changes to **D4UC (`discord-checker`)** are documented in this file.

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
