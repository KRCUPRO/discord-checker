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

## 📖 개요 (Overview)

**D4UC (Discord 4-Character Usernames Checker)**는 Discord의 희귀 고유 닉네임(3~6자)을 가장 빠르고 안전하게 탐색하고 선점할 수 있도록 설계된 엔터프라이즈급 올인원 자동화 엔진입니다.

Chrome 131 TLS 지문 위장, Surfshark WireGuard 유저스페이스 1:1 격리 터널링, SQLite WAL 모드 실시간 동기화, 다중 창 분할(샤딩)은 물론, **아이폰(iPhone), 아이패드(iPad), 안드로이드, 태블릿, PC 등 기종에 전혀 구애받지 않는 100% 웹 브라우저 기반 클라우드 실행**을 완벽하게 지원합니다.

---

## 📱 스마트폰/아이폰/아이패드/태블릿 100% 기종 무관 지원 (Zero-Install)

> **"컴퓨터가 없어도, 앱을 설치하지 않아도 괜찮습니다!"**  
> 아이폰(Safari), 아이패드, 갤럭시, 모든 태블릿의 웹 브라우저만 열면 즉시 가동할 수 있습니다. 자세한 내용은 [📱 모바일/아이폰 전용 가이드](./docs/MOBILE_AND_IPHONE_GUIDE.md)를 확인하세요.

1. **🍏 Apple iOS (아이폰 / 아이패드)**:
   - 별도의 앱 설치, 탈옥(Jailbreak) 없이 **순정 Safari 브라우저**에서 [Google Colab](./D4UC_Google_Colab.ipynb) 및 [Google Apps Script](./docs/GAS_24H_CHECKER_GUIDE.md)를 즉시 실행할 수 있습니다.
2. **🤖 Android 스마트폰 & 태블릿**:
   - Chrome 브라우저로 Colab 인셀 반응형 Web GUI를 실행하거나, GAS로 24시간 백그라운드 구동이 가능합니다. (로컬 터미널을 원할 경우 Termux도 완벽 지원).
3. **🔋 배터리 소모 0% & 기기 꺼짐 무관 (24/7 Cloud Background)**:
   - **Google Apps Script** 방식을 가동하면 스마트폰 전원을 끄거나 비행기 모드로 전환해도 구글 클라우드 인프라에서 24시간 365일 1초도 멈추지 않고 닉네임 검사가 지속됩니다.
4. **🔔 스마트폰 실시간 알림**:
   - 가용 닉네임 발견 시 스마트폰 **Discord 앱 푸시 알림** 및 **Google Sheets 모바일 앱**으로 실시간 기록됩니다.

---

## 🚀 6대 크로스 플랫폼 실행 환경 비교

| 실행 환경 | 지원 기기 (Supported Devices) | 특징 및 핵심 용도 | 빠른 시작 명령어 / 링크 |
| :--- | :--- | :--- | :--- |
| **☁️ Google Apps Script** | 📱 **100% 전 기종** (아이폰, 아이패드, 갤럭시, 태블릿, PC) | **기기 꺼져도 작동**, 구글 클라우드 24/7 서버리스 완전 무인 체커 | [GAS 24/7 가이드](./docs/GAS_24H_CHECKER_GUIDE.md) |
| **⚡ Google Colab Web GUI** | 📱 **100% 전 기종** (Safari, Chrome 등 브라우저 지원 기기) | 인셀 반응형 모던 다크 대시보드, 구글 드라이브 영구 동기화 | [`D4UC_Google_Colab.ipynb`](./D4UC_Google_Colab.ipynb) |
| **🖥️ Windows Desktop GUI** | 💻 Windows PC (Windows 10/11) | 직관적인 Cyberpunk 다크 테마 GUI, 실시간 KPI, 전 위젯 툴팁 | `DiscordUsernameCheckerV2.exe` |
| **📱 Android Termux** | 🤖 안드로이드 전용 (루팅 불필요) | 모바일 백그라운드 24시간 무중단 네이티브 구동 (Debian proot) | [Termux 가이드](./docs/TERMUX_DEBIAN_GUIDE.md) |
| **🐳 Docker & Compose** | 🖥️ 리눅스/Mac/서버/NAS | ARM64/AMD64 멀티아키텍처 서버 무인 컨테이너화 | `docker compose up -d` |
| **⚙️ Headless CLI** | 🖥️ 리눅스/윈도우/서버 | 고속 대량 트래픽 백그라운드 콘솔 실행기 | `python run.py --mode Permutation` |

---

## 🌟 핵심 기능 (Key Features)

1. **Google Apps Script 24시간 서버리스 체커 (`gas/`)**:
   - 시간 기반 예약 트리거(Time-driven Triggers)로 24시간 무인 구동.
   - 6분 타임아웃을 돌파하는 4.5분 Self-Chaining State Machine.
   - Google Drive 파일 저장 + Google Sheets 실시간 대시보드(`D4UC_Tracker`) 듀얼 연동.
   - 단독 구동(Standalone) 및 Colab 감시 페일오버(Hybrid Watchdog) 듀얼 모드.
2. **Google Colab 대화형 Web GUI (`colab_gui.py`)**:
   - 외부 터널 없이 Colab 셀 내에 직접 렌더링되는 모던 다크 대시보드.
   - 6대 실시간 KPI 카드, 진행 상태바, 실시간 발견 닉네임 표, 실시간 로그 콘솔.
3. **10개국어 1:1 매칭 전수 지원**:
   - 한국어, 영어, 일본어, 중국어, 스페인어, 러시아어, 프랑스어, 독일어, 포르투갈어, 베트남어 196개 키 완전 매핑.
4. **Surfshark WireGuard 1:1 격리 멀티 터널링 (`surfshark-proxy-engine/`)**:
   - 각 워커마다 전용 해외 IP를 배정하여 Discord 429 Rate Limit 원천 극복.
5. **Discord Webhook 실시간 알림**:
   - 가용 닉네임("된거") 발견 즉시 초록색 임베드, `@here` 멘션 및 원클릭 등록 링크 전송.

---

## 📄 라이선스 (License)
본 프로젝트는 [MIT License](./LICENSE) 하에 배포됩니다.
