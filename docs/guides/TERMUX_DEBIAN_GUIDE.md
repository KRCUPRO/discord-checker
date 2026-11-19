# 📱 안드로이드 모바일 Termux (데비안 환경) D4UC 완벽 가이드 (TERMUX_DEBIAN_GUIDE.md)

> **프로젝트**: D4UC (`discord-checker`) v12.3.0 / v12.4.0  
> **대상 플랫폼**: Android 10+ (Termux + proot-distro Debian ARM64)  
> **최종 개정일**: 2026년 11월 19일  

---

<a id="목차"></a><a id="-목차"></a>
## 📑 목차
1. [개요 및 안드로이드 전용 가이드 안내](#-개요-및-안드로이드-전용-가이드-안내)
2. [왜 proot-distro 데비안인가요?](#-왜-proot-distro-데비안인가요)
3. [설치 및 환경 세팅 (최초 1회, 약 2~3분)](#-설치-및-환경-세팅-최초-1회-약-23분)
4. [D4UC 소스코드 다운로드 및 원클릭 자동 설치](#-d4uc-소스코드-다운로드-및-원클릭-자동-설치)
5. [환경 변수 설정 (.env)](#-환경-변수-설정-env)
6. [실행 및 백그라운드 24시간 무중단 구동](#-실행-및-백그라운드-24시간-무중단-구동)
7. [결과 파일 확인 및 내보내기](#-결과-파일-확인-및-내보내기)
8. [자주 묻는 질문 및 트러블슈팅](#-자주-묻는-질문-및-트러블슈팅)
9. [각주 및 기술 참고문헌](#-각주-및-기술-참고문헌)

---

<a id="개요-및-안드로이드-전용-가이드-안내"></a><a id="-개요-및-안드로이드-전용-가이드-안내"></a>
## 🧭 개요 및 안드로이드 전용 가이드 안내

- 🤖 **안드로이드 네이티브 APK 가이드**: [ANDROID_GUIDE.md](ANDROID_GUIDE.md) (1-Tap 설치, Wake Lock, UI 조작)
- 🍏 **iOS / iPadOS 가이드**: [IOS_GUIDE.md](IOS_GUIDE.md)

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="왜-proot-distro-데비안인가요"></a><a id="-왜-proot-distro-데비안인가요"></a>
## 🌟 왜 proot-distro 데비안인가요?
- 안드로이드 기본 Termux 쉘은 bionic C 라이브러리를 사용하여 일부 파이썬 C-확장 모듈(BoringSSL) 컴파일에 오류가 발생할 수 있습니다.
- <a id="fnref-1"></a><a id="fnref1"></a>**proot-distro debian**[^1]은 안드로이드 위에 **100% 표준 GNU/Linux (glibc ARM64)** 환경을 구축하므로, PC 리눅스와 동일하게 `curl_cffi` 및 `wireproxy`가 네이티브 속도로 완벽히 구동됩니다.

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="설치-및-환경-세팅-최초-1회-약-23분"></a><a id="-설치-및-환경-세팅-최초-1회-약-23분"></a>
## 🚀 설치 및 환경 세팅 (최초 1회, 약 2~3분)

### 1단계: Termux 앱 설치
- 구글 플레이스토어 버전은 업데이트가 중단되었으므로, **F-Droid** 또는 **GitHub 공식 릴리즈**에서 Termux 최신 APK를 다운로드하여 설치합니다.
- Termux 실행 후 저장소 권한 설정:
```bash
termux-setup-storage
```

### 2단계: 데비안 리눅스 환경 원클릭 설치 및 진입 (1줄 복사)
```bash
pkg update -y && pkg install git proot-distro -y && proot-distro install debian && proot-distro login debian
```

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="d4uc-소스코드-다운로드-및-원클릭-자동-설치"></a><a id="-d4uc-소스코드-다운로드-및-원클릭-자동-설치"></a>
## 📦 D4UC 소스코드 다운로드 및 원클릭 자동 설치

### 1단계: D4UC 다운로드 (Git Clone)
```bash
git clone https://github.com/KRCUPRO/discord-checker.git
cd discord-checker
```

### 2단계: 자동 설치 스크립트 실행
```bash
chmod +x deploy/install_debian.sh deploy/run.sh
./deploy/install_debian.sh
```

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="환경-변수-설정-env"></a><a id="-환경-변수-설정-env"></a>
## ⚙️ 환경 변수 설정 (.env)
```bash
cp config/.env.example .env
nano .env
```
WireGuard 개인키와 웹후크 URL을 등록합니다.

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="실행-및-백그라운드-24시간-무중단-구동"></a><a id="-실행-및-백그라운드-24시간-무중단-구동"></a>
## 🏃 실행 및 백그라운드 24시간 무중단 구동

```bash
# 화면 꺼짐 방지
termux-wake-lock

# 24시간 백그라운드 구동
nohup ./deploy/run.sh --no-dashboard > output.log 2>&1 &
tail -f output.log
```

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="결과-파일-확인-및-내보내기"></a><a id="-결과-파일-확인-및-내보내기"></a>
## 💾 결과 파일 확인 및 내보내기

- `cat available.txt`: 발견된 가용 닉네임 즉시 확인
- 스마트폰 다운로드 폴더로 복사:
```bash
cp available.txt /sdcard/Download/
```

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="자주-묻는-질문-및-트러블슈팅"></a><a id="-자주-묻는-질문-및-트러블슈팅"></a>
## ❓ 자주 묻는 질문 및 트러블슈팅

| 현상 | 해결책 |
| :--- | :--- |
| **`Permission denied: ./deploy/run.sh`** | `chmod +x deploy/run.sh` 실행 |
| **화면이 꺼지면 Termux 프로세스가 종료됨** | 스마트폰 설정 ➔ 앱 ➔ Termux ➔ 배터리 '제한 없음' 설정 및 `termux-wake-lock` 실행 |

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="각주-및-기술-참고문헌"></a><a id="-각주-및-기술-참고문헌"></a>
## 📚 각주 및 기술 참고문헌

[^1]: PRoot는 ptrace 시스템 콜을 통해 루트 권한 없는 안드로이드 사용자 영역에서 격리된 파일시스템 루트를 구현합니다. [↩](#-목차) [↩ 본문으로 돌아가기](#fnref-1) · [⬆️ 목차 맨 위로 이동](#-목차)
[⬆️ 목차 맨 위로 이동](#-목차)
