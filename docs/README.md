# 📖 D4UC Documentation Hub & Technical Specifications (docs/README.md)

> **프로젝트**: D4UC (`discord-checker`) v12.3.0 / <a id="fnref-1"></a><a id="fnref1"></a>v12.4.0[^1]  
> **설명**: D4UC 고성능 디스코드 희귀 사용자명 체커 공식 문서 통합 허브  
> **최종 개정일**: 2026년 11월 19일  

| [KR 한국어](./README.md) | [US English](./locales/en/README.md) | [JP 日本語](./locales/ja/README.md) | [CN 简体中文](./locales/zh-CN/README.md) | [ES Español](./locales/es/README.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](./locales/fr/README.md) | [DE Deutsch](./locales/de/README.md) | [RU Русский](./locales/ru/README.md) | [BR Português](./locales/pt-BR/README.md) | [SA العربية](./locales/ar/README.md) |

<p align="center"><sub>🌐 Also available: <a href="./locales/hi/README.md">HI हिन्दी</a> • <a href="./locales/id/README.md">ID Bahasa Indonesia</a></sub></p>

---

<a id="목차"></a><a id="-목차"></a>
## 📑 목차
1. [문서 허브 구조 및 디렉터리 맵](#-문서-허브-구조-및-디렉터리-맵)
2. [운영체제 환경별 공식 가이드 (docs/guides/)](#-운영체제-환경별-공식-가이드-docsguides)
3. [11개 다국어 현지화 매뉴얼 (docs/locales/)](#-11개-다국어-현지화-매뉴얼-docslocales)
4. [엔진 내부 아키텍처 기술 명세서 (docs/specs/)](#-엔진-내부-아키텍처-기술-명세서-docsspecs)
5. [프로젝트 관리 및 유지보수 문서](#-프로젝트-관리-및-유지보수-문서)
6. [각주 및 기술 참고문헌](#-각주-및-기술-참고문헌)

---

<a id="문서-허브-구조-및-디렉터리-맵"></a><a id="-문서-허브-구조-및-디렉터리-맵"></a>
## 🧭 문서 허브 구조 및 디렉터리 맵

```text
docs/
├── README.md                  # [현재 문서] 전체 문서 통합 허브 인덱스
├── GUIDE.md                   # D4UC 프로젝트 총괄 마스터 가이드
├── ARCHITECTURE_MAP.md        # 전체 소스코드 아키텍처 및 모듈 호출 흐름도
├── TASKS.md                   # 버전별 개발 작업 및 백로그
├── guides/                    # 운영체제 및 플랫폼별 상세 설치/운용 가이드
│   ├── README.md              # 플랫폼 가이드 통합 인덱스
│   ├── WINDOWS_GUIDE.md       # Windows 10/11 전용 4종 실행파일 및 방화벽 설정
│   ├── MACOS_GUIDE.md         # Apple macOS (M1-M4 & Intel) 및 Homebrew 세팅
│   ├── LINUX_GUIDE.md         # Linux (Ubuntu/Debian) Systemd 24/7 서비스 데몬
│   ├── ANDROID_GUIDE.md       # Android 네이티브 1-Tap APK 및 Wake Lock 설정
│   ├── IOS_GUIDE.md           # Apple iOS Safari PWA 전체화면 앱 & Webhook
│   ├── DOCKER_GUIDE.md        # Multi-Arch Docker Compose 2-샤드 병렬 가속
│   ├── RASPBERRY_PI_GUIDE.md  # Raspberry Pi 4/5 3W 저전력 홈랩 24/7 구동
│   ├── PC_GUIDE.md            # Windows & macOS PC 통합 가이드
│   ├── MOBILE_IOS_GUIDE.md    # 모바일 터치 Web GUI & PWA 안내
│   ├── TERMUX_DEBIAN_GUIDE.md # Android Termux proot-distro 데비안 가이드
│   └── GITHUB_PUSH_GUIDE.md   # GitHub 커밋 보안 및 릴리스 배포 가이드
├── locales/                   # 11개 언어 1:1 완벽 번역 공식 문서
│   ├── ko.md                  # 한국어 (Korean)
│   ├── ja.md                  # 日本語 (Japanese)
│   ├── zh-CN.md               # 简体中文 (Simplified Chinese)
│   ├── es.md                  # Español (Spanish)
│   ├── fr.md                  # Français (French)
│   ├── de.md                  # Deutsch (German)
│   ├── ru.md                  # Русский (Russian)
│   ├── pt-BR.md               # Português (Portuguese)
│   ├── ar.md                  # العربية (Arabic)
│   ├── hi.md                  # हिन्दी (Hindi)
│   └── id.md                  # Bahasa Indonesia (Indonesian)
└── specs/                     # 코어 엔진 세부 기술 명세서 (RFC)
    ├── 01_NETWORK_CORE_ENGINE.md              # Chrome 131 TLS BoringSSL 핸드셰이크
    ├── 02_PROXY_INFRASTRUCTURE.md             # 1:1 유저스페이스 WireGuard 터널 풀
    ├── 03_NICKNAME_GENERATION_ALGORITHMS.md   # 8대 닉네임 생성 수학적 알고리즘
    ├── 04_MONITORING_STORAGE_WEBHOOK.md       # SQLite WAL 트랜잭션 & 실시간 텔레메트리
    └── 05_SURFSHARK_INTEGRATION.md            # 142개 글로벌 클러스터 핫스왑 매핑
```

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="운영체제-환경별-공식-가이드-docsguides"></a><a id="-운영체제-환경별-공식-가이드-docsguides"></a>
## 🖥️ 운영체제 환경별 공식 가이드 (docs/guides/)

각 운영체제에 최적화된 설치 및 실행 매뉴얼입니다:

1. 🪟 [Windows 가이드 (WINDOWS_GUIDE.md)](guides/WINDOWS_GUIDE.md): 4대 `.exe` 바이너리, Defender 방화벽 예외 스크립트, Task Scheduler.
2. 🍎 [macOS 가이드 (MACOS_GUIDE.md)](guides/MACOS_GUIDE.md): Apple Silicon M1~M4 BoringSSL 가속, Homebrew, launchd.
3. 🐧 [Linux 가이드 (LINUX_GUIDE.md)](guides/LINUX_GUIDE.md): Ubuntu, Debian, Kali, systemd 24/7 서비스 등록.
4. 🤖 [Android 가이드 (ANDROID_GUIDE.md)](guides/ANDROID_GUIDE.md): 네이티브 1-Tap APK, Wake Lock, 백그라운드 배터리 최적화.
5. 🍏 [iOS 가이드 (IOS_GUIDE.md)](guides/IOS_GUIDE.md): Safari PWA 홈 화면 추가, Discord Webhook 즉각 푸시, Termius SSH.
6. 🐳 [Docker 가이드 (DOCKER_GUIDE.md)](guides/DOCKER_GUIDE.md): Multi-Arch Docker Compose 2-샤드 병렬 2배속.
7. 🍓 [Raspberry Pi 가이드 (RASPBERRY_PI_GUIDE.md)](guides/RASPBERRY_PI_GUIDE.md): 3W 초저전력 홈랩, Tailscale 원격 제어.
8. 📚 [플랫폼 가이드 전체 색인 (guides/README.md)](guides/README.md): 플랫폼 가이드 종합 인덱스.

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="11개-다국어-현지화-매뉴얼-docslocales"></a><a id="-11개-다국어-현지화-매뉴얼-docslocales"></a>
## 🌐 11개 다국어 현지화 매뉴얼 (docs/locales/)

전 세계 사용자를 위한 1:1 완벽 대응 다국어 문서입니다:

| 언어 | 문서 경로 | 상태 |
| :--- | :--- | :--- |
| **한국어 (Korean)** | [docs/locales/ko.md](locales/ko.md) | ✅ 1:1 완벽 지원 |
| **English (Master)** | [README.md](../README.md) | ✅ 1:1 완벽 지원 |
| **日本語 (Japanese)** | [docs/locales/ja.md](locales/ja.md) | ✅ 1:1 완벽 지원 |
| **简体中文 (Simplified Chinese)** | [docs/locales/zh-CN.md](locales/zh-CN.md) | ✅ 1:1 완벽 지원 |
| **Español (Spanish)** | [docs/locales/es.md](locales/es.md) | ✅ 1:1 완벽 지원 |
| **Français (French)** | [docs/locales/fr.md](locales/fr.md) | ✅ 1:1 완벽 지원 |
| **Deutsch (German)** | [docs/locales/de.md](locales/de.md) | ✅ 1:1 완벽 지원 |
| **Русский (Russian)** | [docs/locales/ru.md](locales/ru.md) | ✅ 1:1 완벽 지원 |
| **Português (Portuguese)** | [docs/locales/pt-BR.md](locales/pt-BR.md) | ✅ 1:1 완벽 지원 |
| **العربية (Arabic)** | [docs/locales/ar.md](locales/ar.md) | ✅ 1:1 완벽 지원 |
| **हिन्दी (Hindi)** | [docs/locales/hi.md](locales/hi.md) | ✅ 1:1 완벽 지원 |
| **Bahasa Indonesia (Indonesian)** | [docs/locales/id.md](locales/id.md) | ✅ 1:1 완벽 지원 |

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="엔진-내부-아키텍처-기술-명세서-docsspecs"></a><a id="-엔진-내부-아키텍처-기술-명세서-docsspecs"></a>
## 🔬 엔진 내부 아키텍처 기술 명세서 (docs/specs/)

- ⚙️ [01. 네트워크 코어 엔진 (Chrome 131 TLS BoringSSL)](specs/01_NETWORK_CORE_ENGINE.md)
- 🌐 [02. 프록시 인프라 (유저스페이스 WireGuard 1:1 터널)](specs/02_PROXY_INFRASTRUCTURE.md)
- 🔢 [03. 8대 닉네임 생성 알고리즘 및 규칙 검증](specs/03_NICKNAME_GENERATION_ALGORITHMS.md)
- 💾 [04. 모니터링, SQLite WAL 스토리지 및 Webhook](specs/04_MONITORING_STORAGE_WEBHOOK.md)
- 🛡️ [05. Surfshark 142개 글로벌 클러스터 연동](specs/05_SURFSHARK_INTEGRATION.md)

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="프로젝트-관리-및-유지보수-문서"></a><a id="-프로젝트-관리-및-유지보수-문서"></a>
## 📋 프로젝트 관리 및 유지보수 문서

- 🧭 [D4UC 프로젝트 마스터 가이드](GUIDE.md)
- 🗺️ [소스코드 아키텍처 맵 (ARCHITECTURE_MAP.md)](ARCHITECTURE_MAP.md)
- 📝 [버전별 태스크 및 백로그 (TASKS.md)](TASKS.md)

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="각주-및-기술-참고문헌"></a><a id="-각주-및-기술-참고문헌"></a>
## 📚 각주 및 기술 참고문헌

[^1]: 본 문서 허브는 D4UC v12.3.0 및 v12.4.0 릴리스의 모든 산출물과 기능을 1:1로 증명하고 상호 참조할 수 있도록 설계되었습니다. [↩](#-목차) [↩ 본문으로 돌아가기](#fnref-1) · [⬆️ 목차 맨 위로 이동](#-목차)
[⬆️ 목차 맨 위로 이동](#-목차)
