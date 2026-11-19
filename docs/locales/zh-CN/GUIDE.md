<div align="center">

# 📖 D4UC 项目主开发指南 (GUIDE.md)

> **基于 Chrome 131 TLS 隐形网络栈 + Surfshark 1:1 多国隧道池 + SQLite WAL 多进程无锁同步的高性能 Discord 稀有用户名全量探测与可用性扫描引擎**

<br />

| [KR 한국어](../ko/GUIDE.md) | [US English](../en/GUIDE.md) | [JP 日本語](../ja/GUIDE.md) | [CN 简体中文](./GUIDE.md) | [ES Español](../es/GUIDE.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/GUIDE.md) | [DE Deutsch](../de/GUIDE.md) | [RU Русский](../ru/GUIDE.md) | [BR Português](../pt-BR/GUIDE.md) | [SA العربية](../ar/GUIDE.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/GUIDE.md">HI हिन्दी</a> • <a href="../id/GUIDE.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 2026年11月19日](../../assets/badges/update_badge_zh.svg)](./CHANGELOG.md)
[![Guide Version](https://img.shields.io/badge/Guide-v12.5.0-blue.svg)](./GUIDE.md)

</div>

---

<a id="目录"></a>
## 📑 目录
1. [1. 项目概述与核心架构](#-1-项目概述与核心架构)
2. [2. 操作系统与平台专属指南索引](#-2-操作系统与平台专属指南索引)
3. [3. 主流运行环境快速上手](#-3-主流运行环境快速上手)
4. [4. 八大候选用户名生成与扫描模式](#-4-八大候选用户名生成与扫描模式)
5. [5. 代理基础设施与多国隧道技术](#-5-代理基础设施与多国隧道技术)
6. [6. 多窗口/多容器并发分片扫描 (2~4倍加速)](#-6-多窗口多容器并发分片扫描-24倍加速)
7. [7. GitHub 安全交付与零泄漏守则](#-7-github-安全交付与零泄漏守则)
8. [8. 规范化代码架构与开发者维护指南](#-8-规范化代码架构与开发者维护指南)
9. [9. 脚注与技术参考文献](#-9-脚注与技术参考文献)

---

<a id="-1-项目概述与核心架构"></a>
## 1. 1. 项目概述与核心架构

- **Engine Target Endpoint**: `https://discord.com/api/v9/unique-username/username-attempt-unauthed`
- **Core Technological Invariants**:
  1. <a id="fnref-1"></a><a id="fnref1"></a>**Chrome 131 TLS JA3/JA4 Stealth Impersonation** (`curl_cffi`)[^1].
  2. <a id="fnref-2"></a><a id="fnref2"></a>**Surfshark 1:1 Isolated Multi-Tunnel Pool** (`wireproxy`)[^2].
  3. **0.3s Atomic 429 Hot-Swap**: Uninterrupted continuous scanning across alternate global countries.
  4. **Free Public Proxy Scraper & Live Multi-Threaded Validator** (`src/proxy/free_proxy.py`).
  5. **SQLite WAL Concurrency**: Multi-process safe state synchronization without database locks.

[⬆️ 返回目录顶部](#目录)

---

<a id="-2-操作系统与平台专属指南索引"></a>
## 2. 2. 操作系统与平台专属指南索引

- 🪟 [Windows Guide (WINDOWS_GUIDE.md)](../../guides/WINDOWS_GUIDE.md): 4 Standalone EXEs, Windows Firewall, Task Scheduler 24/7.
- 🍏 [macOS Guide (MACOS_GUIDE.md)](../../guides/MACOS_GUIDE.md): Apple Silicon M1-M4 & Intel, Homebrew, `launchd` automation.
- 🐧 [Linux Guide (LINUX_GUIDE.md)](../../guides/LINUX_GUIDE.md): Ubuntu, Debian, systemd service, tmux/screen background execution.
- 🤖 [Android Guide (ANDROID_GUIDE.md)](../../guides/ANDROID_GUIDE.md): 1-Tap native APK, Wake Lock management, Termux PRoot.
- 📱 [iOS Guide (IOS_GUIDE.md)](../../guides/IOS_GUIDE.md): Safari PWA Home Screen App, 0.1s Discord Webhook push notifications.
- 🐳 [Docker Guide (DOCKER_GUIDE.md)](../../guides/DOCKER_GUIDE.md): Multi-Arch Docker Compose 2-shard acceleration.
- 🍓 [Raspberry Pi Guide (RASPBERRY_PI_GUIDE.md)](../../guides/RASPBERRY_PI_GUIDE.md): 3W low-power homelab 24/7 setup.
- 🧭 [Guides Hub (docs/guides/README.md)](../../guides/README.md) & [Docs Hub (docs/README.md)](../../README.md)

[⬆️ 返回目录顶部](#目录)

---

<a id="-3-主流运行环境快速上手"></a>
## 3. 3. 主流运行环境快速上手

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

[⬆️ 返回目录顶部](#目录)

---

<a id="-4-八大候选用户名生成与扫描模式"></a>
## 4. 4. 八大候选用户名生成与扫描模式

1. **Hybrid**: Combines dictionary bases, consonant-vowel combinations, and alphanumeric affixes.
2. **Permutation**: Pure combinatorial math engine (`[a-z0-9_.]^N`).
3. **Dictionary**: Real word frequency dictionary matching.
4. **Pattern**: Custom regex pattern matching (`a*b?`, `kr_*`).
5. **Numeric**: Consecutive and rare numerical combinations (`0001`~`9999`).
6. **Custom Mask**: Precise position-by-position character masking.
7. **Combinatorial**: User-defined prefix + base + suffix combinations.
8. **Recheck**: Scans previously verified or taken database history.

[⬆️ 返回目录顶部](#目录)

---

<a id="-5-代理基础设施与多国隧道技术"></a>
## 5. 5. 代理基础设施与多国隧道技术

- **Surfshark WireGuard Multi-Tunnel**: Maps 142 global server clusters to local ports `127.0.0.1:1081~1085`.
- **Free Public Proxy Scraper**: Aggregates from 18 verified open-source endpoints with Cloudflare trace pre-validation.
- **Tor & User Proxies**: SOCKS5 and HTTP proxy list rotation support.

[⬆️ 返回目录顶部](#目录)

---

<a id="-6-多窗口多容器并发分片扫描-24倍加速"></a>
## 6. 6. 多窗口/多容器并发分片扫描 (2~4倍加速)

Execute 2 to 4 parallel sharded instances with zero key collisions:
```bash
# Window 1 (Shard 1/2)
python src/run.py --mode permutation --shard 2_1 --length 4

# Window 2 (Shard 2/2)
python src/run.py --mode permutation --shard 2_2 --length 4
```

[⬆️ 返回目录顶部](#目录)

---

<a id="-7-github-安全交付与零泄漏守则"></a>
## 7. 7. GitHub 安全交付与零泄漏守则

- Never commit `config.yaml`, `.env`, or `surfshark_credentials.json`.
- All credentials must be passed via environment variables or template files.
- Refer to [SECURITY.md](./SECURITY.md) for vulnerability reporting.

[⬆️ 返回目录顶部](#目录)

---

<a id="-8-规范化代码架构与开发者维护指南"></a>
## 8. 8. 规范化代码架构与开发者维护指南

```text
src/
├── network/    # DiscordApiClient & Chrome 131 TLS handshake
├── proxy/      # UnifiedProxyManager, Surfshark, FreeProxyProvider
├── generator/  # 8 candidate generation algorithms
├── storage/    # SQLite WAL database & text mirrors
└── ui/         # Desktop CustomTkinter & Mobile Web GUI
```

[⬆️ 返回目录顶部](#目录)

---

<a id="-9-脚注与技术参考文献"></a>
## 9. 9. 脚注与技术参考文献

[^1]: <a id="fn-1"></a><a id="fn1"></a>Chrome 131 BoringSSL 握手特征能够 100% 绕过 Cloudflare 与现代 Web 应用程序防火墙（WAF）的 TLS 指纹拦截。 [↩️ 返回正文](#fnref-1)
[^2]: <a id="fn-2"></a><a id="fn2"></a>wireproxy 是一个无需 root 权限即可在用户空间将 WireGuard 流量转换为本地 SOCKS5 代理的高性能 Go 独立程序。 [↩️ 返回正文](#fnref-2)

[⬆️ 返回目录顶部](#目录)
