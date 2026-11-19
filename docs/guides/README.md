# 📚 D4UC OS & Platform Deployment Guides Index (docs/guides/README.md)

> **프로젝트**: D4UC (`discord-checker`) v12.3.0 / <a id="fnref-1"></a><a id="fnref1"></a>v12.4.0[^1]  
> **설명**: 데스크톱, 서버, 클라우드, 모바일, 임베디드 등 모든 운영체제 환경별 공식 매뉴얼 모음  
> **최종 개정일**: 2026년 11월 19일  

---

<a id="목차"></a><a id="-목차"></a>
## 📑 목차
1. [운영체제 및 환경별 전용 가이드 매트릭스](#-운영체제-및-환경별-전용-가이드-매트릭스)
2. [데스크톱 운영체제 가이드](#-데스크톱-운영체제-가이드)
3. [모바일 생태계 가이드](#-모바일-생태계-가이드)
4. [서버, 클라우드 및 컨테이너 가이드](#-서버-클라우드-및-컨테이너-가이드)
5. [개발자 및 깃 배포 가이드](#-개발자-및-깃-배포-가이드)
6. [각주 및 기술 참고문헌](#-각주-및-기술-참고문헌)

---

<a id="운영체제-및-환경별-전용-가이드-매트릭스"></a><a id="-운영체제-및-환경별-전용-가이드-매트릭스"></a>
## 🧭 운영체제 및 환경별 전용 가이드 매트릭스

| 환경 / OS | 주요 지원 형태 | 가이드 문서 | 권장 용도 |
| :--- | :--- | :--- | :--- |
| **Microsoft Windows** | 4대 무설치 `.exe` + Python 소스 | [WINDOWS_GUIDE.md](WINDOWS_GUIDE.md) | Windows 10/11 데스크톱 사용자 |
| **Apple macOS** | ARM64 (M1~M4) & Intel, Web App | [MACOS_GUIDE.md](MACOS_GUIDE.md) | Mac 사용자 및 Homebrew 개발 환경 |
| **Linux (Server/VPS)** | Systemd 데몬, Headless CLI, Web | [LINUX_GUIDE.md](LINUX_GUIDE.md) | Ubuntu/Debian 24/7 상시 운영 서버 |
| **Android Mobile** | 1-Tap 네이티브 `.apk` + Termux | [ANDROID_GUIDE.md](ANDROID_GUIDE.md) | 안드로이드 스마트폰 휴대용 검사 |
| **Apple iOS / iPadOS** | Safari PWA 풀스크린 앱 + Webhook | [IOS_GUIDE.md](IOS_GUIDE.md) | iPhone & iPad 원격 제어 및 알림 |
| **Docker & Compose** | Multi-Arch (`amd64`, `arm64`) | [DOCKER_GUIDE.md](DOCKER_GUIDE.md) | 클라우드 VPS, NAS, 컨테이너 환경 |
| **Raspberry Pi** | ARM64 저전력 3W 24/7 홈랩 | [RASPBERRY_PI_GUIDE.md](RASPBERRY_PI_GUIDE.md) | 홈 서버 및 저비용 상시 구동 |
| **PC 통합 가이드** | Windows + macOS 통합 | [PC_GUIDE.md](PC_GUIDE.md) | PC 환경 종합 안내 |
| **모바일 통합 가이드** | iOS + Android 통합 | [MOBILE_IOS_GUIDE.md](MOBILE_IOS_GUIDE.md) | 스마트폰 모바일 종합 안내 |
| **Termux Debian** | 안드로이드 PRoot glibc 리눅스 | [TERMUX_DEBIAN_GUIDE.md](TERMUX_DEBIAN_GUIDE.md) | PC 없는 스마트폰 단독 전수 검사 |
| **GitHub Push** | 깃허브 배포 및 보안 검증 | [GITHUB_PUSH_GUIDE.md](GITHUB_PUSH_GUIDE.md) | 릴리스 및 커밋 보안 수칙 |

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="데스크톱-운영체제-가이드"></a><a id="-데스크톱-운영체제-가이드"></a>
## 💻 데스크톱 운영체제 가이드

- 🪟 [WINDOWS_GUIDE.md](WINDOWS_GUIDE.md): Windows 10/11 전용 4종 실행 파일, Defender 방화벽 포트 5000/1081+ 허용 스크립트, Task Scheduler 백그라운드 등록.
- 🍎 [MACOS_GUIDE.md](MACOS_GUIDE.md): Apple Silicon M1-M4 네이티브 BoringSSL 가속, Homebrew 세팅, Safari Dock 앱 등록.
- 💻 [PC_GUIDE.md](PC_GUIDE.md): PC 환경 빠른 시작 및 공통 트러블슈팅.

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="모바일-생태계-가이드"></a><a id="-모바일-생태계-가이드"></a>
## 📱 모바일 생태계 가이드

- 🤖 [ANDROID_GUIDE.md](ANDROID_GUIDE.md): 안드로이드 1-Tap APK (`DiscordUsernameChecker_v12.3.0.apk`) 설치 및 Wake Lock, 배터리 최적화 예외.
- 🍏 [IOS_GUIDE.md](IOS_GUIDE.md): iPhone Safari PWA 홈 화면 추가, Discord Webhook 즉각 알림, Termius SSH 연동.
- 📲 [TERMUX_DEBIAN_GUIDE.md](TERMUX_DEBIAN_GUIDE.md): 모바일 기기 자체에서 구동하는 proot-distro 데비안 24시간 스캔.
- 📱 [MOBILE_IOS_GUIDE.md](MOBILE_IOS_GUIDE.md): 모바일 터치 최적화 웹 애플리케이션 및 PWA 종합 안내.

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="서버-클라우드-및-컨테이너-가이드"></a><a id="-서버-클라우드-및-컨테이너-가이드"></a>
## ☁️ 서버, 클라우드 및 컨테이너 가이드

- 🐧 [LINUX_GUIDE.md](LINUX_GUIDE.md): Ubuntu, Debian, Kali, Arch 리눅스 배포판 패키징 및 systemd 데몬화.
- 🐳 [DOCKER_GUIDE.md](DOCKER_GUIDE.md): Multi-Arch Docker Compose 2-샤드 병렬 2배속 스캔.
- 🍓 [RASPBERRY_PI_GUIDE.md](RASPBERRY_PI_GUIDE.md): 라즈베리파이 4/5 ARM64 3W 저전력 홈랩 및 Tailscale 원격 제어.

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="개발자-및-깃-배포-가이드"></a><a id="-개발자-및-깃-배포-가이드"></a>
## 🛠️ 개발자 및 깃 배포 가이드

- 🚀 [GITHUB_PUSH_GUIDE.md](GITHUB_PUSH_GUIDE.md): 시크릿 키 누출 방지(Zero-Leak) 및 깃허브 원격 동기화.
- 🧭 [프로젝트 마스터 가이드](../GUIDE.md): 전체 아키텍처 및 8대 생성 알고리즘.
- 📐 [아키텍처 맵](../ARCHITECTURE_MAP.md): 소스 코드 심층 모듈 구조.

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="각주-및-기술-참고문헌"></a><a id="-각주-및-기술-참고문헌"></a>
## 📚 각주 및 기술 참고문헌

[^1]: 모든 가이드는 2026년 11월 19일 기준 D4UC v12.3.0 및 v12.4.0 최신 아키텍처를 기준으로 작성되었습니다. [↩](#-목차) [↩ 본문으로 돌아가기](#fnref-1) · [⬆️ 목차 맨 위로 이동](#-목차)
[⬆️ 목차 맨 위로 이동](#-목차)
