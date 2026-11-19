# 💻 PC Platform Deployment Guide (PC_GUIDE.md)

> **프로젝트**: D4UC (`discord-checker`) v12.3.0 / v12.4.0  
> **대상 플랫폼**: Microsoft Windows 10/11 & Apple macOS (Apple Silicon M1-M4 / Intel)  
> **최종 개정일**: 2026년 11월 19일  

---

<a id="목차"></a><a id="-목차"></a>
## 📑 목차
1. [개요 및 운영체제별 전용 가이드 안내](#-개요-및-운영체제별-전용-가이드-안내)
2. [Windows 10 / 11 환경 빠른 시작](#-windows-10--11-환경-빠른-시작)
3. [Apple macOS 환경 빠른 시작](#-apple-macos-환경-빠른-시작)
4. [프록시 및 네트워크 구성](#-프록시-및-네트워크-구성)
5. [PC 환경 문제 해결](#-pc-환경-문제-해결)
6. [각주 및 기술 참고문헌](#-각주-및-기술-참고문헌)

---

<a id="개요-및-운영체제별-전용-가이드-안내"></a><a id="-개요-및-운영체제별-전용-가이드-안내"></a>
## 🧭 개요 및 운영체제별 전용 가이드 안내

PC 환경에서의 보다 심층적인 설정, 방화벽 예외 처리, 시작 프로그램 등록 등은 아래의 전용 문서를 참조하세요:
- 🪟 **Windows 전용 심층 가이드**: [WINDOWS_GUIDE.md](WINDOWS_GUIDE.md) (4대 바이너리, 방화벽 PowerShell, 작업 스케줄러)
- 🍎 **macOS 전용 심층 가이드**: [MACOS_GUIDE.md](MACOS_GUIDE.md) (M1~M4 BoringSSL, Homebrew, launchd)

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="windows-10--11-환경-빠른-시작"></a><a id="-windows-10--11-환경-빠른-시작"></a>
## 🪟 Windows 10 / 11 환경 빠른 시작

### 1. 인터페이스 미리보기
[![D4UC Windows GUI](../assets/gui_ko_main.png)](WINDOWS_GUIDE.md)

### 2. 무설치 단독 실행 파일 (`.exe`) 사용
GitHub Releases에서 제공하는 Standalone 바이너리는 Python 3.12 런타임, `customtkinter`, `curl_cffi` BoringSSL 엔진, `wireproxy.exe`를 단일 실행 파일에 완전히 내장하고 있습니다.
- `DiscordUsernameCheckerV2_Web.exe`: 모바일 반응형 웹 GUI (포트 5000)
- `DiscordUsernameCheckerV2_KO.exe`: 한국어 <a id="fnref-1"></a><a id="fnref1"></a>데스크톱 GUI[^1]
- `DiscordUsernameCheckerV2_EN.exe`: 영어 데스크톱 GUI
- `DiscordUsernameCheckerV2_CLI.exe`: 헤드리스 콘솔 CLI 대시보드

### 3. 소스코드 가상환경 실행
```powershell
git clone https://github.com/KRCUPRO/discord-checker.git
cd discord-checker
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/gui_ko.py
```

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="apple-macos-환경-빠른-시작"></a><a id="-apple-macos-환경-빠른-시작"></a>
## 🍎 Apple macOS 환경 빠른 시작

macOS 환경에서는 Homebrew 패키지 매니저를 통해 필요한 유저스페이스 도구와 Python 3.12를 구성하여 실행합니다.

```bash
# 1. 의존성 설치
brew install python@3.12 wireproxy

# 2. 저장소 복제 및 가상환경 실행
git clone https://github.com/KRCUPRO/discord-checker.git
cd discord-checker
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. CLI 대시보드 또는 모바일 웹 GUI 실행
python3 src/web_gui.py --port 5000
```

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="프록시-및-네트워크-구성"></a><a id="-프록시-및-네트워크-구성"></a>
## 🌐 프록시 및 네트워크 구성

- **Surfshark WireGuard**: 1:1 유저스페이스 터널 풀 (`127.0.0.1:1081+`).
- **무료 공개 프록시 (`--proxy free`)**: 오픈소스 다중 소스 실시간 수집 및 검증.
- **다이렉트**: 로컬 네트워크 직통 연결.

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="pc-환경-문제-해결"></a><a id="-pc-환경-문제-해결"></a>
## 🔧 PC 환경 문제 해결

- **포트 1081 충돌**: 잔여 `wireproxy` 프로세스 종료.
- **방화벽 경고**: [WINDOWS_GUIDE.md](WINDOWS_GUIDE.md)의 원클릭 PowerShell 스크립트 실행.

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="각주-및-기술-참고문헌"></a><a id="-각주-및-기술-참고문헌"></a>
## 📚 각주 및 기술 참고문헌

[^1]: PC 플랫폼(Windows/macOS)은 데스크톱 GUI와 웹 GUI를 동시에 실행할 수 있습니다. [↩](#-목차) [↩ 본문으로 돌아가기](#fnref-1) · [⬆️ 목차 맨 위로 이동](#-목차)
[⬆️ 목차 맨 위로 이동](#-목차)
