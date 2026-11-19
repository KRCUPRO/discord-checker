<div align="center">

# 📖 D4UC プロジェクトマスターガイド (GUIDE.md)

> **Chrome 131 TLS ステルス偽装 + Surfshark 1:1 複数国トンネルプール + SQLite WAL 並行同期に基づく高スループット Discord ユーザー名可用性探索エンジン**

<br />

| [KR 한국어](../ko/GUIDE.md) | [US English](../en/GUIDE.md) | [JP 日本語](./GUIDE.md) | [CN 简体中文](../zh-CN/GUIDE.md) | [ES Español](../es/GUIDE.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/GUIDE.md) | [DE Deutsch](../de/GUIDE.md) | [RU Русский](../ru/GUIDE.md) | [BR Português](../pt-BR/GUIDE.md) | [SA العربية](../ar/GUIDE.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/GUIDE.md">HI हिन्दी</a> • <a href="../id/GUIDE.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 2026年11月19日](../../assets/badges/update_badge_ja.svg)](./CHANGELOG.md)
[![Guide Version](https://img.shields.io/badge/Guide-v12.5.0-blue.svg)](./GUIDE.md)

</div>

---

<a id="目次"></a>
## 📑 目次
1. [1. プロジェクト概要とコアアーキテクチャ](#-1-プロジェクト概要とコアアーキテクチャ)
2. [2. OS・環境別専用ガイドリンク](#-2-os環境別専用ガイドリンク)
3. [3. 主要環境別クイックスタート](#-3-主要環境別クイックスタート)
4. [4. 8大ユーザー名生成・探索モード](#-4-8大ユーザー名生成探索モード)
5. [5. プロキシ基盤および複数国トンネリング](#-5-プロキシ基盤および複数国トンネリング)
6. [6. 複数ウィンドウ/コンテナ分割シャーディング](#-6-複数ウィンドウコンテナ分割シャーディング)
7. [7. GitHub 安全配布およびセキュリティ規則](#-7-github-安全配布およびセキュリティ規則)
8. [8. 体系的コード構造と開発者メンテナンスガイド](#-8-体系的コード構造と開発者メンテナンスガイド)
9. [9. 脚注および技術参考文献](#-9-脚注および技術参考文献)

---

<a id="-1-プロジェクト概要とコアアーキテクチャ"></a>
## 1. 1. プロジェクト概要とコアアーキテクチャ

- **Engine Target Endpoint**: `https://discord.com/api/v9/unique-username/username-attempt-unauthed`
- **Core Technological Invariants**:
  1. <a id="fnref-1"></a><a id="fnref1"></a>**Chrome 131 TLS JA3/JA4 Stealth Impersonation** (`curl_cffi`)[^1].
  2. <a id="fnref-2"></a><a id="fnref2"></a>**Surfshark 1:1 Isolated Multi-Tunnel Pool** (`wireproxy`)[^2].
  3. **0.3s Atomic 429 Hot-Swap**: Uninterrupted continuous scanning across alternate global countries.
  4. **Free Public Proxy Scraper & Live Multi-Threaded Validator** (`src/proxy/free_proxy.py`).
  5. **SQLite WAL Concurrency**: Multi-process safe state synchronization without database locks.

[⬆️ 目次の先頭へ移動](#目次)

---

<a id="-2-os環境別専用ガイドリンク"></a>
## 2. 2. OS・環境別専用ガイドリンク

- 🪟 [Windows Guide (WINDOWS_GUIDE.md)](../../guides/WINDOWS_GUIDE.md): 4 Standalone EXEs, Windows Firewall, Task Scheduler 24/7.
- 🍏 [macOS Guide (MACOS_GUIDE.md)](../../guides/MACOS_GUIDE.md): Apple Silicon M1-M4 & Intel, Homebrew, `launchd` automation.
- 🐧 [Linux Guide (LINUX_GUIDE.md)](../../guides/LINUX_GUIDE.md): Ubuntu, Debian, systemd service, tmux/screen background execution.
- 🤖 [Android Guide (ANDROID_GUIDE.md)](../../guides/ANDROID_GUIDE.md): 1-Tap native APK, Wake Lock management, Termux PRoot.
- 📱 [iOS Guide (IOS_GUIDE.md)](../../guides/IOS_GUIDE.md): Safari PWA Home Screen App, 0.1s Discord Webhook push notifications.
- 🐳 [Docker Guide (DOCKER_GUIDE.md)](../../guides/DOCKER_GUIDE.md): Multi-Arch Docker Compose 2-shard acceleration.
- 🍓 [Raspberry Pi Guide (RASPBERRY_PI_GUIDE.md)](../../guides/RASPBERRY_PI_GUIDE.md): 3W low-power homelab 24/7 setup.
- 🧭 [Guides Hub (docs/guides/README.md)](../../guides/README.md) & [Docs Hub (docs/README.md)](../../README.md)

[⬆️ 目次の先頭へ移動](#目次)

---

<a id="-3-主要環境別クイックスタート"></a>
## 3. 3. 主要環境別クイックスタート

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

[⬆️ 目次の先頭へ移動](#目次)

---

<a id="-4-8大ユーザー名生成探索モード"></a>
## 4. 4. 8大ユーザー名生成・探索モード

1. **Hybrid**: Combines dictionary bases, consonant-vowel combinations, and alphanumeric affixes.
2. **Permutation**: Pure combinatorial math engine (`[a-z0-9_.]^N`).
3. **Dictionary**: Real word frequency dictionary matching.
4. **Pattern**: Custom regex pattern matching (`a*b?`, `kr_*`).
5. **Numeric**: Consecutive and rare numerical combinations (`0001`~`9999`).
6. **Custom Mask**: Precise position-by-position character masking.
7. **Combinatorial**: User-defined prefix + base + suffix combinations.
8. **Recheck**: Scans previously verified or taken database history.

[⬆️ 目次の先頭へ移動](#目次)

---

<a id="-5-プロキシ基盤および複数国トンネリング"></a>
## 5. 5. プロキシ基盤および複数国トンネリング

- **Surfshark WireGuard Multi-Tunnel**: Maps 142 global server clusters to local ports `127.0.0.1:1081~1085`.
- **Free Public Proxy Scraper**: Aggregates from 18 verified open-source endpoints with Cloudflare trace pre-validation.
- **Tor & User Proxies**: SOCKS5 and HTTP proxy list rotation support.

[⬆️ 目次の先頭へ移動](#目次)

---

<a id="-6-複数ウィンドウコンテナ分割シャーディング"></a>
## 6. 6. 複数ウィンドウ/コンテナ分割シャーディング

Execute 2 to 4 parallel sharded instances with zero key collisions:
```bash
# Window 1 (Shard 1/2)
python src/run.py --mode permutation --shard 2_1 --length 4

# Window 2 (Shard 2/2)
python src/run.py --mode permutation --shard 2_2 --length 4
```

[⬆️ 目次の先頭へ移動](#目次)

---

<a id="-7-github-安全配布およびセキュリティ規則"></a>
## 7. 7. GitHub 安全配布およびセキュリティ規則

- Never commit `config.yaml`, `.env`, or `surfshark_credentials.json`.
- All credentials must be passed via environment variables or template files.
- Refer to [SECURITY.md](./SECURITY.md) for vulnerability reporting.

[⬆️ 目次の先頭へ移動](#目次)

---

<a id="-8-体系的コード構造と開発者メンテナンスガイド"></a>
## 8. 8. 体系的コード構造と開発者メンテナンスガイド

```text
src/
├── network/    # DiscordApiClient & Chrome 131 TLS handshake
├── proxy/      # UnifiedProxyManager, Surfshark, FreeProxyProvider
├── generator/  # 8 candidate generation algorithms
├── storage/    # SQLite WAL database & text mirrors
└── ui/         # Desktop CustomTkinter & Mobile Web GUI
```

[⬆️ 目次の先頭へ移動](#目次)

---

<a id="-9-脚注および技術参考文献"></a>
## 9. 9. 脚注および技術参考文献

[^1]: <a id="fn-1"></a><a id="fn1"></a>Chrome 131 BoringSSL ハンドシェイクは、Cloudflare 等の最新 WAF による TLS 指紋検知を完全に無力化します。 [↩️ 本文に戻る](#fnref-1)
[^2]: <a id="fn-2"></a><a id="fn2"></a>wireproxy は管理者権限なしで WireGuard プロトコルをローカル SOCKS5 プロキシへ変換する軽量な Go バイナリです。 [↩️ 本文に戻る](#fnref-2)

[⬆️ 目次の先頭へ移動](#目次)
