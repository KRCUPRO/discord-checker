<div align="center">

# 📖 D4UC (Discord Username Checker) 프로젝트 마스터 가이드 (GUIDE.md)

> **Chrome 131 TLS 스텔스 위장 + Surfshark 1:1 다중 국적 터널 풀 + SQLite WAL 멀티프로세스 동기화 기반 고성능 디스코드 닉네임 전수검사 및 가용성 탐색 엔진**

<br />

| [KR 한국어](./GUIDE.md) | [US English](../en/GUIDE.md) | [JP 日本語](../ja/GUIDE.md) | [CN 简体中文](../zh-CN/GUIDE.md) | [ES Español](../es/GUIDE.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/GUIDE.md) | [DE Deutsch](../de/GUIDE.md) | [RU Русский](../ru/GUIDE.md) | [BR Português](../pt-BR/GUIDE.md) | [SA العربية](../ar/GUIDE.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/GUIDE.md">HI हिन्दी</a> • <a href="../id/GUIDE.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 2026년 11월 19일](../../assets/badges/update_badge.svg)](./CHANGELOG.md)
[![Guide Version](https://img.shields.io/badge/Guide-v12.5.0-blue.svg)](./GUIDE.md)

</div>

---

<a id="목차"></a>
## 📑 목차
1. [1. 프로젝트 개요 및 핵심 아키텍처](#-1-프로젝트-개요-및-핵심-아키텍처)
2. [2. 운영체제 및 환경별 전용 가이드 링크](#-2-운영체제-및-환경별-전용-가이드-링크)
3. [3. 주요 실행 환경별 빠른 시작](#-3-주요-실행-환경별-빠른-시작)
4. [4. 8대 닉네임 생성 및 탐색 모드](#-4-8대-닉네임-생성-및-탐색-모드)
5. [5. 프록시 인프라 및 다중 국적 터널링](#-5-프록시-인프라-및-다중-국적-터널링)
6. [6. 다중 창/다중 컨테이너 분할 샤딩 (2배~4배 가속)](#-6-다중-창다중-컨테이너-분할-샤딩-2배4배-가속)
7. [7. 깃허브(GitHub) 안전 배포 및 보안 수칙](#-7-깃허브github-안전-배포-및-보안-수칙)
8. [8. 체계적 코드 구조 및 개발자 유지보수 가이드](#-8-체계적-코드-구조-및-개발자-유지보수-가이드)
9. [9. 각주 및 기술 참고문헌](#-9-각주-및-기술-참고문헌)

---

<a id="-1-프로젝트-개요-및-핵심-아키텍처"></a>
## 1. 1. 프로젝트 개요 및 핵심 아키텍처

- **Engine Target Endpoint**: `https://discord.com/api/v9/unique-username/username-attempt-unauthed`
- **Core Technological Invariants**:
  1. <a id="fnref-1"></a><a id="fnref1"></a>**Chrome 131 TLS JA3/JA4 Stealth Impersonation** (`curl_cffi`)[^1].
  2. <a id="fnref-2"></a><a id="fnref2"></a>**Surfshark 1:1 Isolated Multi-Tunnel Pool** (`wireproxy`)[^2].
  3. **0.3s Atomic 429 Hot-Swap**: Uninterrupted continuous scanning across alternate global countries.
  4. **Free Public Proxy Scraper & Live Multi-Threaded Validator** (`src/proxy/free_proxy.py`).
  5. **SQLite WAL Concurrency**: Multi-process safe state synchronization without database locks.

[⬆️ 목차 맨 위로 이동](#목차)

---

<a id="-2-운영체제-및-환경별-전용-가이드-링크"></a>
## 2. 2. 운영체제 및 환경별 전용 가이드 링크

- 🪟 [Windows Guide (WINDOWS_GUIDE.md)](../../guides/WINDOWS_GUIDE.md): 4 Standalone EXEs, Windows Firewall, Task Scheduler 24/7.
- 🍏 [macOS Guide (MACOS_GUIDE.md)](../../guides/MACOS_GUIDE.md): Apple Silicon M1-M4 & Intel, Homebrew, `launchd` automation.
- 🐧 [Linux Guide (LINUX_GUIDE.md)](../../guides/LINUX_GUIDE.md): Ubuntu, Debian, systemd service, tmux/screen background execution.
- 🤖 [Android Guide (ANDROID_GUIDE.md)](../../guides/ANDROID_GUIDE.md): 1-Tap native APK, Wake Lock management, Termux PRoot.
- 📱 [iOS Guide (IOS_GUIDE.md)](../../guides/IOS_GUIDE.md): Safari PWA Home Screen App, 0.1s Discord Webhook push notifications.
- 🐳 [Docker Guide (DOCKER_GUIDE.md)](../../guides/DOCKER_GUIDE.md): Multi-Arch Docker Compose 2-shard acceleration.
- 🍓 [Raspberry Pi Guide (RASPBERRY_PI_GUIDE.md)](../../guides/RASPBERRY_PI_GUIDE.md): 3W low-power homelab 24/7 setup.
- 🧭 [Guides Hub (docs/guides/README.md)](../../guides/README.md) & [Docs Hub (docs/README.md)](../../README.md)

[⬆️ 목차 맨 위로 이동](#목차)

---

<a id="-3-주요-실행-환경별-빠른-시작"></a>
## 3. 3. 주요 실행 환경별 빠른 시작

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

[⬆️ 목차 맨 위로 이동](#목차)

---

<a id="-4-8대-닉네임-생성-및-탐색-모드"></a>
## 4. 4. 8대 닉네임 생성 및 탐색 모드

1. **Hybrid**: Combines dictionary bases, consonant-vowel combinations, and alphanumeric affixes.
2. **Permutation**: Pure combinatorial math engine (`[a-z0-9_.]^N`).
3. **Dictionary**: Real word frequency dictionary matching.
4. **Pattern**: Custom regex pattern matching (`a*b?`, `kr_*`).
5. **Numeric**: Consecutive and rare numerical combinations (`0001`~`9999`).
6. **Custom Mask**: Precise position-by-position character masking.
7. **Combinatorial**: User-defined prefix + base + suffix combinations.
8. **Recheck**: Scans previously verified or taken database history.

[⬆️ 목차 맨 위로 이동](#목차)

---

<a id="-5-프록시-인프라-및-다중-국적-터널링"></a>
## 5. 5. 프록시 인프라 및 다중 국적 터널링

- **Surfshark WireGuard Multi-Tunnel**: Maps 142 global server clusters to local ports `127.0.0.1:1081~1085`.
- **Free Public Proxy Scraper**: Aggregates from 18 verified open-source endpoints with Cloudflare trace pre-validation.
- **Tor & User Proxies**: SOCKS5 and HTTP proxy list rotation support.

[⬆️ 목차 맨 위로 이동](#목차)

---

<a id="-6-다중-창다중-컨테이너-분할-샤딩-2배4배-가속"></a>
## 6. 6. 다중 창/다중 컨테이너 분할 샤딩 (2배~4배 가속)

Execute 2 to 4 parallel sharded instances with zero key collisions:
```bash
# Window 1 (Shard 1/2)
python src/run.py --mode permutation --shard 2_1 --length 4

# Window 2 (Shard 2/2)
python src/run.py --mode permutation --shard 2_2 --length 4
```

[⬆️ 목차 맨 위로 이동](#목차)

---

<a id="-7-깃허브github-안전-배포-및-보안-수칙"></a>
## 7. 7. 깃허브(GitHub) 안전 배포 및 보안 수칙

- Never commit `config.yaml`, `.env`, or `surfshark_credentials.json`.
- All credentials must be passed via environment variables or template files.
- Refer to [SECURITY.md](./SECURITY.md) for vulnerability reporting.

[⬆️ 목차 맨 위로 이동](#목차)

---

<a id="-8-체계적-코드-구조-및-개발자-유지보수-가이드"></a>
## 8. 8. 체계적 코드 구조 및 개발자 유지보수 가이드

```text
src/
├── network/    # DiscordApiClient & Chrome 131 TLS handshake
├── proxy/      # UnifiedProxyManager, Surfshark, FreeProxyProvider
├── generator/  # 8 candidate generation algorithms
├── storage/    # SQLite WAL database & text mirrors
└── ui/         # Desktop CustomTkinter & Mobile Web GUI
```

[⬆️ 목차 맨 위로 이동](#목차)

---

<a id="-9-각주-및-기술-참고문헌"></a>
## 9. 9. 각주 및 기술 참고문헌

[^1]: <a id="fn-1"></a><a id="fn1"></a>Chrome 131 BoringSSL 핸드셰이크는 Cloudflare 및 최신 웹 방화벽(WAF)의 TLS 핑거프린팅 감지를 100% 무력화합니다. [↩️ 본문으로 돌아가기](#fnref-1)
[^2]: <a id="fn-2"></a><a id="fn2"></a>wireproxy는 루트 권한 없이 WireGuard 프로토콜을 로컬 SOCKS5 프록시로 변환하는 고성능 유저스페이스 Go 바이너리입니다. [↩️ 본문으로 돌아가기](#fnref-2)

[⬆️ 목차 맨 위로 이동](#목차)
