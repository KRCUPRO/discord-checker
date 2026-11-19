<div align="center">

# 📋 변경 이력 (Changelog)

> **D4UC (discord-checker) 프로젝트의 모든 버전별 변경 사항 및 기술 갱신 기록**

<br />

| [KR 한국어](./CHANGELOG.md) | [US English](../en/CHANGELOG.md) | [JP 日本語](../ja/CHANGELOG.md) | [CN 简体中文](../zh-CN/CHANGELOG.md) | [ES Español](../es/CHANGELOG.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/CHANGELOG.md) | [DE Deutsch](../de/CHANGELOG.md) | [RU Русский](../ru/CHANGELOG.md) | [BR Português](../pt-BR/CHANGELOG.md) | [SA العربية](../ar/CHANGELOG.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/CHANGELOG.md">HI हिन्दी</a> • <a href="../id/CHANGELOG.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 2026년 11월 19일](../../assets/badges/update_badge.svg)](./CHANGELOG.md)
[![Latest Release](https://img.shields.io/badge/Release-v12.5.0-blue.svg)](https://github.com/KRCUPRO/discord-checker/releases)

</div>

---

<a id="목차"></a>
## 📑 목차
1. [[v12.5.0] — 2026-11-19](#-v1250-2026-11-19)
1. [[v12.4.0] — 2026-11-19](#-v1240-2026-11-19)
1. [[v12.3.0] — 2026-11-19](#-v1230-2026-11-19)
1. [[v12.2.0] — 2026-11-19](#-v1220-2026-11-19)
1. [[v12.0.0] — 2026-11-18](#-v1200-2026-11-18)

---

> D4UC의 모든 공식 릴리스 및 주요 기능 추가, 아키텍처 개선, 버그 수정 내역을 기록합니다.

---

<a id="-v1250-2026-11-19"></a>
## [v12.5.0] — 2026-11-19

### Added
- **모바일 APK 및 터치 웹 GUI UX 전면 개편**:
  - 삼성 갤럭시 One UI 상단 노치/상태바(`SKT 6:24`, 펀치홀 카메라) 및 하단 제스처 내비게이션 바와의 시각적 겹침을 방지하는 반응형 안전 여백(`env(safe-area-inset-top/bottom)`) 완벽 적용.
  - 상단 상태 뱃지를 간결하고 명확한 4상태 실시간 알약 배지(`🟢 34ms`, `🟡 확인 중...`, `🔴 미연결`, `🟣 시연 모드`)로 전면 재설계.
  - 기존의 검은 빈 캔버스를 격자 가이드선, 기준선, 탐색 대기 안내 문구 및 실시간 네온 스플라인 차트로 고도화.
- **스마트 네트워크 멀티 프로브 및 서버 연결 마법사 (Connection Assistant)**:
  - PC 호스트의 활성 LAN IPv4 자동 탐지(`GET /api/network_info`) 및 원클릭 핑 테스트(`GET /api/ping`).
  - 안드로이드 APK 브리지(`AndroidBridge.isEmulator()`, `getDeviceLocalIp()`)를 통해 실물 기기와 에뮬레이터를 판별하여 잘못된 `10.0.2.2` 루프백 장애 원천 차단.
  - PC 미연결 환경에서도 UI 인터랙션, RPS 파형, 희귀 닉네임 감지, 클립보드 복사를 시뮬레이션할 수 있는 **독립 시연 모드 (Standalone Mock Mode)** 탑재.
  - 상세 가이드 문서 `docs/MOBILE_AND_APK_UX_GUIDE.md` 신설 및 `docs/guides/ANDROID_GUIDE.md` 반영.
- **12개국어 1:1 전수 공식 문서 스위트 (`docs/locales/<lang>/`)**: 8종의 핵심 문서(`README.md`, `ARCHITECTURE_MAP.md`, `GUIDE.md`, `TASKS.md`, `CHANGELOG.md`, `LICENSE.md`, `NOTICE.md`, `SECURITY.md`)를 12개 언어(한국어, 영어, 일본어, 중국어 간체, 스페인어, 프랑스어, 독일어, 러시아어, 포르투갈어, 아랍어, 힌디어, 인도네시아어)로 1:1 전면 번역 및 구축.
- **깃허브 저장소 루트 최적화 및 모듈화**: 내부 유지보수 스크립트를 `deploy/scripts/`로 이전하고 중복 스크립트를 제거하여, 저장소 방문 즉시 설명서와 UI 미리보기가 한눈에 보이도록 폴더 6개 + 파일 8개 구조로 대폭 슬림화.
- **문서 상단 빠른 점프 바 (Quick Jump Navigation Bar)**: 스크롤 부담 없이 [개요 | 미리보기 | 빠른 시작 | 아키텍처 | 가이드 | 라이선스]로 즉시 점프 가능한 원터치 앵커 링크 추가.

### Changed
- 모든 문서 상단에 5x2 규격의 대칭형 다국어 선택 테이블 및 SVG 실시간 업데이트 배지(`2026년 11월 19일`) 동기화.

[⬆️ 목차 맨 위로 이동](#목차)

---

<a id="-v1240-2026-11-19"></a>
## [v12.4.0] — 2026-11-19

### Added
- **문서 양방향 내비게이션 (TOC 앵커 및 목차 복귀 링크)**: 26개 전체 마크다운 문서에 상호 점프 앵커 `<a id="...">` 및 `[⬆️ 목차 맨 위로 이동]` 링크 전면 적용.
- **13종 운영체제별 공식 가이드 구축 (`docs/guides/`)**: Windows, macOS, Linux, Android APK, iOS Safari PWA, Docker Compose, Raspberry Pi 등 플랫폼별 맞춤 설치 및 24/7 데몬 구동 매뉴얼 완비.

[⬆️ 목차 맨 위로 이동](#목차)

---

<a id="-v1230-2026-11-19"></a>
## [v12.3.0] — 2026-11-19

### Added
- **무료 공개 프록시 자동 수집 및 실시간 검증 엔진 (`src/proxy/free_proxy.py`)**: 18개 글로벌 오픈소스 저장소 실시간 스크래핑, Cloudflare WAF 검증, 15초 429 쿨다운 큐.
- **안드로이드 전용 1-Tap 서명 APK (`dist/DiscordUsernameChecker_v12.3.0.apk`)**: v1/v2/v3 암호화 서명, One UI / HyperOS 절전 제외 가이드.

[⬆️ 목차 맨 위로 이동](#목차)

---

<a id="-v1220-2026-11-19"></a>
## [v12.2.0] — 2026-11-19

### Added
- **모바일 터치 최적화 Web GUI & PWA 엔진 (`src/web_gui.py`, `src/ui/web/`)**: 스마트폰 브라우저 5000 포트 반응형 UI, 0.1초 실시간 Discord Webhook 알림.

[⬆️ 목차 맨 위로 이동](#목차)

---

<a id="-v1200-2026-11-18"></a>
## [v12.0.0] — 2026-11-18

### Added
- **크로스 플랫폼 정식 프로덕션 릴리스**: Windows 4종 단독 EXE, 8대 닉네임 생성 엔진, Chrome 131 TLS 스텔스 위장, 1:1 다중 터널 풀.

[⬆️ 목차 맨 위로 이동](#목차)

