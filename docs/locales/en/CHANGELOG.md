<div align="center">

# 📋 Changelog

> **All notable changes to D4UC (discord-checker) documented across releases**

<br />

| [KR 한국어](../ko/CHANGELOG.md) | [US English](./CHANGELOG.md) | [JP 日本語](../ja/CHANGELOG.md) | [CN 简体中文](../zh-CN/CHANGELOG.md) | [ES Español](../es/CHANGELOG.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/CHANGELOG.md) | [DE Deutsch](../de/CHANGELOG.md) | [RU Русский](../ru/CHANGELOG.md) | [BR Português](../pt-BR/CHANGELOG.md) | [SA العربية](../ar/CHANGELOG.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/CHANGELOG.md">HI हिन्दी</a> • <a href="../id/CHANGELOG.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: Nov 19, 2026](../../assets/badges/update_badge_en.svg)](./CHANGELOG.md)
[![Latest Release](https://img.shields.io/badge/Release-v12.5.0-blue.svg)](https://github.com/KRCUPRO/discord-checker/releases)

</div>

---

<a id="-table-of-contents"></a>
## 📑 Table of Contents
1. [[v12.5.0] — 2026-11-19](#-v1250-2026-11-19)
1. [[v12.4.0] — 2026-11-19](#-v1240-2026-11-19)
1. [[v12.3.0] — 2026-11-19](#-v1230-2026-11-19)
1. [[v12.2.0] — 2026-11-19](#-v1220-2026-11-19)
1. [[v12.0.0] — 2026-11-18](#-v1200-2026-11-18)

---

> This log documents all official releases, major architectural improvements, and bug fixes for D4UC.

---

<a id="-v1250-2026-11-19"></a>
## [v12.5.0] — 2026-11-19

### Added
- **12-Language 1:1 Complete Documentation Suite (`docs/locales/<lang>/`)**: Full 1:1 translations for all 8 core documents (`README.md`, `ARCHITECTURE_MAP.md`, `GUIDE.md`, `TASKS.md`, `CHANGELOG.md`, `LICENSE.md`, `NOTICE.md`, `SECURITY.md`) across 12 languages (Korean, English, Japanese, Simplified Chinese, Spanish, French, German, Russian, Portuguese, Arabic, Hindi, Indonesian).
- **GitHub Repository Root Streamlining & Modularization**: Moved internal scripts to `deploy/scripts/`, eliminated duplicate scripts, and reduced root clutter to 6 folders + 8 files so README and preview media appear above the fold.
- **Above-the-Fold Quick Jump Navigation Bar**: One-click anchor bar below badge strip ([ Overview | Previews | Quick Start | Architecture | Guides | License ]).

### Changed
- Standardized 5x2 symmetrical language selector grid and synchronized live SVG date badge (`Nov 19, 2026`) across all files.

[⬆️ Return to Top](#-table-of-contents)

---

<a id="-v1240-2026-11-19"></a>
## [v12.4.0] — 2026-11-19

### Added
- **Two-Way Document Navigation (TOC Anchor Links & Return-to-Top Navigation)**: Full interactive Table of Contents and return-to-top links across all 26 markdown documents.
- **Dedicated OS & Platform Comprehensive Guides (`docs/guides/`)**: 13 platform manuals covering Windows, macOS, Linux, Android APK, iOS Safari PWA, Docker Compose, Raspberry Pi.

[⬆️ Return to Top](#-table-of-contents)

---

<a id="-v1230-2026-11-19"></a>
## [v12.3.0] — 2026-11-19

### Added
- **Free Public Proxy Scraper & Live Multi-Threaded Validator (`src/proxy/free_proxy.py`)**: 18 public candidate sources, Cloudflare WAF validation, 15s 429 rate limit cooldown queue.
- **Standalone Android 1-Tap Signed APK (`dist/DiscordUsernameChecker_v12.3.0.apk`)**: Cryptographically verified v1/v2/v3 signatures with background battery optimization guides.

[⬆️ Return to Top](#-table-of-contents)

---

<a id="-v1220-2026-11-19"></a>
## [v12.2.0] — 2026-11-19

### Added
- **Mobile Touch Web GUI & PWA Engine (`src/web_gui.py`, `src/ui/web/`)**: Port 5000 responsive smartphone UI, Service Worker offline caching, 0.1s Discord Webhook push.

[⬆️ Return to Top](#-table-of-contents)

---

<a id="-v1200-2026-11-18"></a>
## [v12.0.0] — 2026-11-18

### Added
- **Official Cross-Platform Production Release**: 4 standalone Windows EXEs, 8 candidate nickname engines, Chrome 131 TLS stealth, 1:1 multi-tunnel proxy pool.

[⬆️ Return to Top](#-table-of-contents)

