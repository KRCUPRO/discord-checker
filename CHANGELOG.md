# Changelog

All notable changes to **D4UC (`discord-checker`)** are documented in this file.

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
