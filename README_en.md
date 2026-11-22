<div align="center">

# ⚡ D4UC — Discord 4-Character Usernames Checker

[![Language](https://img.shields.io/badge/Language-10%20Languages%20Supported-58a6ff?style=for-the-badge&logo=google-translate)](./README.md)
[![Devices](https://img.shields.io/badge/Mobile-iPhone%20|%20iPad%20|%20Android%20|%20Tablet%20|%20PC-ff69b4?style=for-the-badge&logo=apple)](./docs/MOBILE_AND_IPHONE_GUIDE.md)
[![Cloud Execution](https://img.shields.io/badge/100%25%20Browser--Based-Google%20Colab%20|%20Apps%20Script%2024%2F7-blueviolet?style=for-the-badge&logo=google)](./docs/GAS_24H_CHECKER_GUIDE.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](./LICENSE)

---

### 🌐 Select Your Language / 언어 선택 / 言語を選択 / 选择语言 / Seleccionar idioma / Выберите язык / Choisir la langue / Sprache wählen / Selecionar idioma / Chọn ngôn ngữ

[ 🇰🇷 한국어 ](./README_ko.md) • [ 🇺🇸 English ](./README.md) • [ 🇯🇵 日本語 ](./README_ja.md) • [ 🇨🇳 简体中文 ](./README_zh.md) • [ 🇪🇸 Español ](./README_es.md) • [ 🇷🇺 Русский ](./README_ru.md) • [ 🇫🇷 Français ](./README_fr.md) • [ 🇩🇪 Deutsch ](./README_de.md) • [ 🇧🇷 Português ](./README_pt.md) • [ 🇻🇳 Tiếng Việt ](./README_vi.md)

---

</div>

## 📖 Overview

**D4UC (Discord 4-Character Usernames Checker)** is an enterprise-grade, high-performance automated engine engineered to search, check, and claim rare Discord usernames (3 to 6 characters) with zero rate limits and maximum stealth.

Featuring Chrome 131 TLS fingerprint masquerading, user-space Surfshark WireGuard 1:1 isolated tunneling, SQLite WAL real-time deduplication, permutation sharding, and full cloud capabilities including **100% Device-Agnostic Browser Execution for iPhone, iPad, Android, Tablets, and PCs** via **Google Colab Interactive Web GUI** and **Google Apps Script 24/7 Serverless Automated Checker**.

---

## 📱 100% Device-Agnostic: iPhone, iPad, Android & Tablet Support (Zero-Install)

> **"No computer? No installation needed!"**  
> Simply open your web browser (Safari, Chrome) on any iPhone, iPad, Android phone, or Tablet to start checking instantly. Read the [📱 Mobile & iPhone Guide](./docs/MOBILE_AND_IPHONE_GUIDE.md) for full details.

1. **🍏 Apple iOS (iPhone & iPad)**:
   - 100% compatible with native **Safari browser** without jailbreaking or third-party app installations. Launch [Google Colab](./D4UC_Google_Colab.ipynb) or [Google Apps Script](./docs/GAS_24H_CHECKER_GUIDE.md) in 1 click.
2. **🤖 Android Phones & Tablets**:
   - Run the responsive In-Cell Web GUI in Chrome, or run Google Apps Script 24/7. (Native Termux proot is also fully supported for terminal enthusiasts).
3. **🔋 0% Battery Drain & Operates Even When Device is Turned Off (24/7 Cloud)**:
   - **Google Apps Script** runs entirely on Google's cloud infrastructure. Turn off your phone, switch to airplane mode, or run out of battery—the checker never stops running 24/7/365.
4. **🔔 Instant Mobile Alerts**:
   - Discovered available usernames immediately push notifications to your mobile **Discord app** and log into your mobile **Google Sheets app**.

---

## 🚀 6 Cross-Platform Execution Environments

| Platform | Supported Devices | Key Features & Architecture | Quick Start / Guide |
| :--- | :--- | :--- | :--- |
| **☁️ Google Apps Script** | 📱 **100% All Devices** (iPhone, iPad, Android, Tablet, PC) | **Runs even when device is OFF**, 24/7/365 serverless cloud checker | [GAS 24/7 Guide](./docs/GAS_24H_CHECKER_GUIDE.md) |
| **⚡ Google Colab Web GUI** | 📱 **100% All Devices** (Safari, Chrome, all mobile browsers) | In-cell interactive dark dashboard & Google Drive persistence | [`D4UC_Google_Colab.ipynb`](./D4UC_Google_Colab.ipynb) |
| **🖥️ Windows Desktop GUI** | 💻 Windows PC (Windows 10/11) | Cyberpunk dark theme GUI, live KPI cards, full widget tooltips | `DiscordUsernameCheckerV2.exe` |
| **📱 Android Termux** | 🤖 Android Only (No root required) | Mobile background 24/7 headless runner (Debian proot) | [Termux Guide](./docs/TERMUX_DEBIAN_GUIDE.md) |
| **🐳 Docker & Compose** | 🖥️ Linux / Mac / Server / NAS | Multi-arch ARM64/AMD64 server containerization | `docker compose up -d` |
| **⚙️ Headless CLI** | 🖥️ Linux / Windows / Server | High-throughput console runner for bulk checks | `python run.py --mode Permutation` |

---

## 🌟 Key Features

1. **Google Apps Script 24/7 Serverless Checker (`gas/`)**:
   - Automated 24/7 cloud checking powered by Google Time-driven Triggers.
   - Self-Chaining State Machine overcoming the 6-minute execution timeout.
   - Dual persistence: Google Drive files (`available_usernames.txt`) + Google Sheets Live Dashboard (`D4UC_Tracker`).
   - Dual execution modes: Standalone 24/7 & Colab Watchdog Failover.
2. **Google Colab Interactive Web GUI (`colab_gui.py`)**:
   - Zero-tunneling in-cell responsive dark dashboard inside Colab.
   - 6 live KPI cards (RPS, Checked, Available, Taken, 429, Skipped), progress bar, live table, and streaming terminal log.
3. **10-Language 1:1 Matching System**:
   - 100% complete translations across 10 official languages (ko, en, ja, zh, es, ru, fr, de, pt, vi).
4. **Surfshark WireGuard 1:1 Multi-Tunnel Engine (`surfshark-proxy-engine/`)**:
   - 1:1 dedicated exit IPs per worker for complete 429 immunity.
5. **Discord Webhook Real-Time Alerts**:
   - Instant Spring Green embeds with `@here` mentions and one-click registration links upon discovery.

---

## 📄 License
Distributed under the [MIT License](./LICENSE).
