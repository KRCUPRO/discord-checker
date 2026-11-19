# 🤖 Android Mobile Ecosystem Guide (ANDROID_GUIDE.md)

> **프로젝트**: D4UC (`discord-checker`) v12.3.0 / v12.4.0  
> **대상 플랫폼**: Android 10, 11, 12, 13, 14, 15 (Samsung One UI, Google Pixel, Xiaomi HyperOS, OnePlus, Nothing OS)  
> **최종 개정일**: 2026년 11월 19일  

---

<a id="목차"></a><a id="-목차"></a>
## 📑 목차
1. [안드로이드 3대 실행 옵션 개요](#-안드로이드-3대-실행-옵션-개요)
2. [방법 1: 1-Tap 네이티브 APK 설치 (DiscordUsernameChecker.apk)](#-방법-1-1-tap-네이티브-apk-설치-discordusernamecheckerapk)
3. [배터리 최적화 예외 및 화면 꺼짐 방지 (Wake Lock)](#-배터리-최적화-예외-및-화면-꺼짐-방지-wake-lock)
4. [방법 2: Chrome 모바일 브라우저 PWA 홈 화면 추가](#-방법-2-chrome-모바일-브라우저-pwa-홈-화면-추가)
5. [방법 3: Termux + PRoot Debian 파워유저 단독 구동](#-방법-3-termux--proot-debian-파워유저-단독-구동)
6. [모바일 네트워크 및 무료 공개 프록시 라우팅](#-모바일-네트워크-및-무료-공개-프록시-라우팅)
7. [안드로이드 환경 문제 해결 (Troubleshooting)](#-안드로이드-환경-문제-해결-troubleshooting)
8. [각주 및 기술 참고문헌](#-각주-및-기술-참고문헌)

---

<a id="안드로이드-3대-실행-옵션-개요"></a><a id="-안드로이드-3대-실행-옵션-개요"></a>
## 📱 안드로이드 3대 실행 옵션 개요

D4UC는 모바일 환경에서 사용자의 기호와 기기 성능에 맞춰 3가지 실행 방식을 지원합니다:

| 실행 방식 | 사용자 편의성 | 배터리 소모 | 필요 준비물 | 권장 대상 |
| :--- | :--- | :--- | :--- | :--- |
| **1. 네이티브 `.apk` 앱** | ⭐⭐⭐⭐⭐ (최고) | 매우 낮음 | 안드로이드 스마트폰 | 일반 사용자 및 가장 간편한 모바일 제어 |
| **2. Chrome 모바일 PWA** | ⭐⭐⭐⭐⭐ (설치 불필요) | 낮음 | 모바일 크롬 브라우저 | 앱 설치 없이 즉시 웹으로 제어하려는 사용자 |
| **3. Termux + Debian** | ⭐⭐⭐ (터미널) | 중간 | Termux 앱 | PC 없이 스마트폰 단독으로 24시간 검사기 구동 |

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="방법-1-1-tap-네이티브-apk-설치-discordusernamecheckerapk"></a><a id="-방법-1-1-tap-네이티브-apk-설치-discordusernamecheckerapk"></a>
## 📲 방법 1: 1-Tap 네이티브 APK 설치 (DiscordUsernameChecker.apk)

최신 [GitHub Releases v12.3.0](https://github.com/KRCUPRO/discord-checker/releases/tag/v12.3.0)에서 제공되는 암호학적 서명이 완료된 독립형 안드로이드 패키지입니다.

[![D4UC Mobile Web GUI](../assets/mobile_web_main.png)](ANDROID_GUIDE.md)

### 1. 다운로드 및 설치 절차
1. 스마트폰에서 [<a id="fnref-1"></a><a id="fnref1"></a>`DiscordUsernameChecker_v12.3.0.apk`[^1]](https://github.com/KRCUPRO/discord-checker/releases/download/v12.3.0/DiscordUsernameChecker_v12.3.0.apk)를 다운로드합니다.
2. 다운로드 알림 또는 **[내 파일 / 다운로드]** 폴더에서 `.apk` 파일을 터치합니다.
3. **"출처를 알 수 없는 앱 설치"** 팝업이 나타나면 **[설정] ➔ [이 출처의 앱 허용]**을 켭니다.
4. **[설치]**를 눌러 완료한 후 홈 화면의 **`D4UC Discord Checker`** 앱을 실행합니다.

### 2. 주요 내장 기능
- **오프라인 내장 웹 엔진**: 앱 내부에 12개 언어를 지원하는 모바일 반응형 프론트엔드가 포함되어 있어 즉시 로드됩니다.
- **1-Tap 네이티브 클립보드 복사**: 발견된 희귀 닉네임을 원터치하면 안드로이드 시스템 클립보드로 복사되며 진동 토스트가 뜹니다.
- **원터치 호스트 연결**: PC나 리눅스 VPS에서 구동 중인 D4UC 백엔드 IP(`http://192.168.0.x:5000`)에 접속하여 실시간 제어할 수 있습니다.

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="배터리-최적화-예외-및-화면-꺼짐-방지-wake-lock"></a><a id="-배터리-최적화-예외-및-화면-꺼짐-방지-wake-lock"></a>
## 🔋 배터리 최적화 예외 및 화면 꺼짐 방지 (Wake Lock)

안드로이드 OS가 화면이 꺼진 후 D4UC를 강제 절전(Doze Mode)시키지 않도록 설정합니다:

### 1. 삼성 갤럭시 (One UI)
- **[설정]** ➔ **[애플리케이션]** ➔ **[D4UC Discord Checker]** ➔ **[배터리]** ➔ **`제한 없음(Unrestricted)`** 선택.

### 2. 구글 픽셀 / 샤오미 (HyperOS)
- 샤오미: 앱 정보 ➔ **[배터리 절약기]** ➔ **`제한 없음`** 설정 및 **[자동 시작]** 허용.
- 픽셀: 앱 설정 ➔ **[배터리 사용량]** ➔ **`최적화 안 함`** 설정.

### 3. 인앱 Wake Lock 토글
앱 상단 우측의 **`⚡ 화면 유지 (Wake Lock)`** 버튼을 활성화하면 백그라운드 스캔 도중에도 CPU 슬립을 방지합니다.

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="방법-2-chrome-모바일-브라우저-pwa-홈-화면-추가"></a><a id="-방법-2-chrome-모바일-브라우저-pwa-홈-화면-추가"></a>
## 🌐 방법 2: Chrome 모바일 브라우저 PWA 홈 화면 추가

APK를 설치하지 않고 웹 브라우저만으로 네이티브 앱과 동일한 전체화면 인터페이스를 구성할 수 있습니다:

1. 안드로이드 Chrome 브라우저를 열고 `http://<호스트 IP>:5000`에 접속합니다.
2. 브라우저 우측 상단 더보기 버튼(점 3개 `⋮`)을 터치합니다.
3. 메뉴에서 **`[홈 화면에 추가]`** 또는 **`[앱 설치]`**를 선택합니다.
4. 홈 화면에 생성된 보라색 D4UC 아이콘을 누르면 주소 표시줄이 없는 풀스크린 PWA 앱으로 기동됩니다.

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="방법-3-termux--proot-debian-파워유저-단독-구동"></a><a id="-방법-3-termux--proot-debian-파워유저-단독-구동"></a>
## 💻 방법 3: Termux + PRoot Debian 파워유저 단독 구동

PC나 외부 서버 없이 스마트폰 자체 CPU로 24시간 상시 탐색 엔진을 돌리는 파워유저용 방법입니다.

```bash
# 1. F-Droid에서 Termux 최신 버전 설치 후 실행
# 2. Termux 화면 꺼짐 방지
termux-wake-lock

# 3. 자동 설치 스크립트 실행
curl -fsSL https://raw.githubusercontent.com/KRCUPRO/discord-checker/main/deploy/install_debian.sh -o install_debian.sh
chmod +x install_debian.sh
./install_debian.sh

# 4. 백그라운드 nohup 실행
nohup python3 src/run.py --mode hybrid --length 4 --workers 5 --no-dashboard > checker.log 2>&1 &
```

> 상세 튜토리얼은 [TERMUX_DEBIAN_GUIDE.md](TERMUX_DEBIAN_GUIDE.md)를 참조하세요.

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="모바일-네트워크-및-무료-공개-프록시-라우팅"></a><a id="-모바일-네트워크-및-무료-공개-프록시-라우팅"></a>
## 🌐 모바일 네트워크 및 무료 공개 프록시 라우팅

- **LTE / 5G 셀룰러 데이터 환경**: 통신사 IP가 비주기적으로 변경되므로 일반 환경보다 429 차단 내성이 우수합니다.
- **무료 공개 프록시 연동**: 모바일 UI의 프록시 설정 탭에서 `🌐 무료 프록시 자동 수집`을 터치하면 14개 이상의 글로벌 공개 프록시 소스에서 수천 개의 노드를 실시간 비동기 검증하여 탐색에 투입합니다.

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="안드로이드-환경-문제-해결-troubleshooting"></a><a id="-안드로이드-환경-문제-해결-troubleshooting"></a>
## 🔧 안드로이드 환경 문제 해결 (Troubleshooting)

| 현상 | 원인 | 조치 사항 |
| :--- | :--- | :--- |
| **화면을 끄면 스캔이 멈춤** | 안드로이드 배터리 최적화 Doze 모드 | 배터리 최적화에서 D4UC를 **'제한 없음'**으로 등록하고 Wake Lock을 켭니다. |
| **PC 호스트 서버에 연결 실패 (`ERR_CONNECTION_REFUSED`)** | 스마트폰과 PC가 서로 다른 Wi-Fi 망에 연결됨 | PC와 스마트폰이 동일한 공유기 Wi-Fi(2.4G/5G)에 연결되었는지 확인하고, PC 방화벽에서 5000 포트를 허용합니다. |
| **다운로드한 APK 설치 거부** | Google Play 프로텍트 경고 | [세부정보 보기] ➔ [무시하고 설치]를 누릅니다. |

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="각주-및-기술-참고문헌"></a><a id="-각주-및-기술-참고문헌"></a>
## 📚 각주 및 기술 참고문헌

[^1]: 안드로이드 네이티브 APK는 `com.krcupro.discordchecker` 패키지 식별자와 v1/v2/v3 보안 서명 체계가 완비되어 있습니다. [↩](#-목차) [↩ 본문으로 돌아가기](#fnref-1) · [⬆️ 목차 맨 위로 이동](#-목차) [↩ 본문으로 돌아가기](#fnref-1) · [⬆️ 목차 맨 위로 이동](#-목차)
[⬆️ 목차 맨 위로 이동](#-목차)
