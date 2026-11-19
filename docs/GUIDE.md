# 🧭 D4UC (Discord Username Checker) 프로젝트 마스터 가이드 (GUIDE.md)

> **D4UC (Discord 4-Character Usernames Checker)**  
> Chrome 131 TLS 스텔스 위장 + Surfshark 1:1 다중 국가 터널 풀 + SQLite WAL 멀티 인스턴스 무충돌 동기화 기반의 고성능 디스코드 닉네임 전수검사 및 가용성 탐색 엔진  
> **최종 개정일**: 2026년 11월 19일  

---

<a id="목차"></a><a id="-목차"></a>
## 📑 목차
1. [프로젝트 개요 및 핵심 아키텍처](#-1-프로젝트-개요-및-핵심-아키텍처)
2. [운영체제 및 환경별 전용 가이드 링크](#-2-운영체제-및-환경별-전용-가이드-링크)
3. [주요 실행 환경별 빠른 시작](#-3-주요-실행-환경별-빠른-시작)
   - [A. 데스크톱 GUI (Windows & macOS)](#a-데스크톱-gui-windows--macos)
   - [B. 모바일 터치 최적화 Web GUI & PWA](#b-모바일-터치-최적화-web-gui--pwa)
   - [C. 안드로이드 스마트폰 (1-Tap APK)](#c-안드로이드-스마트폰-1-tap-apk)
   - [D. 헤드리스 CLI (Terminal / Linux)](#d-헤드리스-cli-terminal--linux)
   - [E. 도커 컨테이너 (Docker & Compose)](#e-도커-컨테이너-docker--compose)
4. [8대 닉네임 생성 및 탐색 모드](#-4-8대-닉네임-생성-및-탐색-모드)
5. [프록시 인프라 및 다중 국가 터널링](#-5-프록시-인프라-및-다중-국가-터널링)
6. [다중 창/다중 컨테이너 분할 샤딩 (2배~4배 가속)](#-6-다중-창다중-컨테이너-분할-샤딩-2배4배-가속)
7. [깃허브(GitHub) 안전 배포 및 보안 수칙](#-7-깃허브github-안전-배포-및-보안-수칙)
8. [체계적 코드 구조 및 개발자 유지보수 가이드](#-8-체계적-코드-구조-및-개발자-유지보수-가이드)
9. [각주 및 기술 참고문헌](#-각주-및-기술-참고문헌)

---

<a id="1-프로젝트-개요-및-핵심-아키텍처"></a><a id="-1-프로젝트-개요-및-핵심-아키텍처"></a>
## 1. 프로젝트 개요 및 핵심 아키텍처

- **엔진 원리**: 디스코드 가입 API(`https://discord.com/api/v9/unique-username/username-attempt-unauthed`) 엔드포인트를 대상으로, Cloudflare/WAF 차단 없이 합법적인 비로그인 가용 여부를 초고속 판별합니다.
- **핵심 차별화 기술**:
  1. <a id="fnref-1"></a><a id="fnref1"></a>**Chrome 131 TLS JA3/JA4 스텔스 위장**: Python 표준 requests의 지문 차단을 극복하고 최신 크롬 브라우저와 100% 동일한 TLS 핸드셰이크 전송 (`curl_cffi`)[^1].
  2. <a id="fnref-2"></a><a id="fnref2"></a>**Surfshark 1:1 독립 국가 터널 풀 (`wireproxy`)**: OS 네트워크 카드를 건드리지 않고 유저스페이스에서 전세계 142개국 엔드포인트를 로컬 루프백(`127.0.0.1:1081~1085`)으로 1:1 매핑[^2].
  3. **429 레이트리밋 원자적 핫스왑 (Atomic Hot-Swap)**: 특정 워커가 429를 맞으면 해당 워커의 터널만 0.3초 만에 새 국가로 원자적 교체하고, 타 워커는 중단 없이 100% 풀스피드 유지.
  4. **무료 공개 프록시 자동 수집/검증기 (`--proxy free`)**: 유료 VPN 없이도 14개 이상의 글로벌 공개 프록시를 실시간 수집 및 검증하여 즉시 투입.
  5. **SQLite WAL 멀티 프로세스 동기화**: 프로그램을 여러 개 띄워도 `d4uc_results.db`를 안전하게 공유하여 중복 검사 0% 및 실시간 발견 닉네임 크로스 팝업.

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="2-운영체제-및-환경별-전용-가이드-링크"></a><a id="-2-운영체제-및-환경별-전용-가이드-링크"></a>
## 2. 운영체제 및 환경별 전용 가이드 링크

각 환경에 맞춘 세부 설치, 방화벽, 데몬화, 모바일 설정 매뉴얼을 제공합니다:

- 🪟 [Windows 심층 가이드 (WINDOWS_GUIDE.md)](guides/WINDOWS_GUIDE.md): 4종 무설치 `.exe`, Defender 방화벽 예외 스크립트, Task Scheduler.
- 🍎 [macOS 심층 가이드 (MACOS_GUIDE.md)](guides/MACOS_GUIDE.md): Apple Silicon M1-M4 BoringSSL, Homebrew, launchd 자동 기동.
- 🐧 [Linux 심층 가이드 (LINUX_GUIDE.md)](guides/LINUX_GUIDE.md): Ubuntu, Debian, Kali, systemd 24/7 서비스 등록.
- 🤖 [Android 심층 가이드 (ANDROID_GUIDE.md)](guides/ANDROID_GUIDE.md): 1-Tap APK 설치, Wake Lock, 배터리 최적화.
- 🍏 [iOS 심층 가이드 (IOS_GUIDE.md)](guides/IOS_GUIDE.md): Safari PWA 전체화면 앱, Webhook 푸시, Termius SSH.
- 🐳 [Docker 심층 가이드 (DOCKER_GUIDE.md)](guides/DOCKER_GUIDE.md): Multi-Arch Docker Compose 2-샤드 병렬 2배속.
- 🍓 [Raspberry Pi 심층 가이드 (RASPBERRY_PI_GUIDE.md)](guides/RASPBERRY_PI_GUIDE.md): 라즈베리파이 4/5 3W 저전력 홈랩 24시간 가동.
- 📚 [가이드 통합 허브 (guides/README.md)](guides/README.md) 및 [문서 전체 허브 (docs/README.md)](README.md)

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="3-주요-실행-환경별-빠른-시작"></a><a id="-3-주요-실행-환경별-빠른-시작"></a>
## 3. 주요 실행 환경별 빠른 시작

<a id="a-데스크톱-gui-windows--macos"></a><a id="a-데스크톱-gui-windows-macos"></a>
### A. 데스크톱 GUI (Windows & macOS)
```bash
# 한글 인터페이스 실행
python src/gui_ko.py

# 영문 인터페이스 실행
python src/gui_en.py
```
> Windows 사용자라면 별도 설치 없이 `DiscordUsernameCheckerV2_KO.exe` 또는 `DiscordUsernameCheckerV2_EN.exe`를 더블클릭하여 바로 실행할 수 있습니다.

<a id="b-모바일-터치-최적화-web-gui--pwa"></a><a id="b-모바일-터치-최적화-web-gui-pwa"></a>
### B. 모바일 터치 최적화 Web GUI & PWA
```bash
python src/web_gui.py --port 5000
```
> 스마트폰 브라우저에서 `http://<호스트_IP>:5000`에 접속하여 [홈 화면에 추가]를 누르면 네이티브 모바일 앱으로 실행됩니다.

<a id="c-안드로이드-스마트폰-1-tap-apk"></a>
### C. 안드로이드 스마트폰 (1-Tap APK)
- 최신 Releases에서 `DiscordUsernameChecker_v12.3.0.apk`를 스마트폰에 다운로드 후 터치하여 설치합니다.
- 내장된 반응형 웹 엔진과 클립보드 복사 기능을 지원합니다.

<a id="d-헤드리스-cli-terminal--linux"></a><a id="d-헤드리스-cli-terminal-linux"></a>
### D. 헤드리스 CLI (Terminal / Linux)
```bash
# 기본 실행 (하이브리드 모드, 4자리, 5워커)
python src/run.py

# 2분할 1번 창 (a~m 범위) 실행
python src/run.py --mode permutation --length 4 --shard 2_1 --workers 5

# 대시보드 화면 지우기 없이 한 줄 스트리밍 로그 모드 (백그라운드 nohup 권장)
python src/run.py --no-dashboard
```

<a id="e-도커-컨테이너-docker--compose"></a><a id="e-도커-컨테이너-docker-compose"></a>
### E. 도커 컨테이너 (Docker & Compose)
```bash
# 단일 컨테이너 백그라운드 구동
docker compose -f deploy/docker-compose.yml up -d

# 2배속 병렬 분할 (a~m / n~_) 2개 컨테이너 동시 기동
docker compose -f deploy/docker-compose.yml --profile 2shard up -d

# 실시간 스트리밍 로그 확인
docker compose -f deploy/docker-compose.yml logs -f
```

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="4-8대-닉네임-생성-및-탐색-모드"></a><a id="-4-8대-닉네임-생성-및-탐색-모드"></a>
## 4. 8대 닉네임 생성 및 탐색 모드

| 모드 이름 | 코드 키 (`mode`) | 특징 및 탐색 방식 | 권장 용도 |
| :--- | :--- | :--- | :--- |
| **하이브리드 (추천)** | `hybrid` | 사전 단어 변형 + 대칭/반복 패턴 복합 검사 | 일상적 가용 닉네임 신속 발굴 |
| **순열 전수조사** | `permutation` | `a~z, 0~9, _` 조합을 1개도 빠짐없이 수학적 완전 탐색 | 다중 창/다중 컨테이너 분할 필수 |
| **사전식 단어** | `dictionary` | 영단어, 3~4글자 약어, 발음 가능한 어휘 우선 검사 | 의미 있는 레어 단어 선점 |
| **패턴/대칭** | `pattern` | `aaaa`, `abba`, `abab`, `a_a` 등 시각적 대칭 패턴 | 아이디 미관 및 희귀도 중시 |
| **순수 숫자** | `numeric` | 0000 ~ 9999 등 연속/반복 숫자 조합 | 짧은 레어 숫자 닉네임 탐색 |
| **커스텀 마스크** | `custom_mask` | 접두사(`kr`), 접미사(`99`), 마스크(`??99`) 직접 지정 | 특정 브랜드/이니셜 타깃팅 |
| **조합식 음절** | `combinatorial` | CVCV, VCCV 등 발음 가능한 인공 음절 생성 | 브랜드 네이밍 및 고유명사 발굴 |
| **재검증 (Recheck)** | `recheck` | 과거 TAKEN이었던 닉네임을 주기적으로 재점검 | 계정 삭제/탈퇴로 풀린 닉네임 낚아채기 |

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="5-프록시-인프라-및-다중-국가-터널링"></a><a id="-5-프록시-인프라-및-다중-국가-터널링"></a>
## 5. 프록시 인프라 및 다중 국가 터널링

1. **Surfshark WireGuard 1:1 터널 (기본값)**:
   - `data/surfshark_clusters.json`의 142개국 엔드포인트(:51820 UDP)와 `credentials.json`의 개인키를 결합.
   - 워커 번호마다 `1081`, `1082`, `1083` 포트를 순차 배정하여 완전히 격리된 국가 IP로 요청.
2. **무료 공개 프록시 자동 수집 (`--proxy free`) [NEW]**:
   - 14개 이상의 글로벌 공개 소스에서 실시간 수집 및 Discord API 비동기 가용성 검증.
3. **ThorData 프록시**:
   - `config.yaml`에 호스트/계정 등록 시 매 N회 요청마다 세션 자동 교체.
4. **파일 기반 프록시 풀 (`proxies.txt`)**:
   - 직접 수집한 HTTP/SOCKS5 프록시 목록을 텍스트 파일로 연동하여 라운드로빈 순환.
5. **다이렉트 (Direct)**:
   - 프록시 없이 로컬 PC 인터넷 직통 연결 (테스트용).

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="6-다중-창다중-컨테이너-분할-샤딩-2배4배-가속"></a><a id="-6-다중-창다중-컨테이너-분할-샤딩-2배4배-가속"></a>
## 6. 다중 창/다중 컨테이너 분할 샤딩 (2배~4배 가속)

- **2분할**:
  - **1번 창**: `a ~ m` 시작 (전체 순열의 50%)
  - **2번 창**: `n ~ _` 시작 (전체 순열의 50%)
  - **수학적 중복 0%**: 두 창이 검사하는 대상이 정확히 절반씩 나누어져 2배 빠르게 전체 검사 완료.
- **3분할**: `a~i` / `j~r` / `s~_`
- **4분할**: `a~g` / `h~n` / `o~u` / `v~_`
- **직접 지정**: 원하는 시작 글자와 끝 글자를 직접 정의 (`--start-char`, `--end-char`).

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="7-깃허브github-안전-배포-및-보안-수칙"></a><a id="-7-깃허브github-안전-배포-및-보안-수칙"></a>
## 7. 깃허브(GitHub) 안전 배포 및 보안 수칙

> [!CAUTION]
> **공개(Public) 저장소 업로드 시 유의사항**  
> 실제 결제된 Surfshark WireGuard 개인키 및 계정 비밀번호는 절대로 공개 저장소에 푸시되어서는 안 됩니다.

### 보안 수칙 체크리스트
1. **`.gitignore` 적용 필수**:
   - `credentials.json`, `config.yaml`, `.env`, `data/*.db`, `available*.txt`가 차단되어 있는지 확인.
2. **템플릿 파일 사용**:
   - 저장소에는 `config/config.example.yaml`, `config/.env.example`, `data/surfshark_credentials.example.json` 템플릿만 포함.
3. **실행 환경 설정**:
   - 사용자는 자신의 키를 로컬 `.env` 파일에 `SURFSHARK_PRIVATE_KEYS=내_개인키` 형태로 작성하여 구동.
4. **독점 라이선스 안내**:
   - 본 프로젝트는 `KRCUPRO` 독점 라이선스([LICENSE](../LICENSE)) 하에 보호됩니다.

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="8-체계적-코드-구조-및-개발자-유지보수-가이드"></a><a id="-8-체계적-코드-구조-및-개발자-유지보수-가이드"></a>
## 8. 체계적 코드 구조 및 개발자 유지보수 가이드

- **문서 허브 인덱스**: [docs/README.md](README.md)
- **플랫폼 가이드 모음**: [docs/guides/README.md](guides/README.md)
- **프로젝트 맵**: [ARCHITECTURE_MAP.md](ARCHITECTURE_MAP.md)
- **작업 인덱스 & 백로그**: [TASKS.md](TASKS.md)
- **단위 테스트 실행**:
  ```bash
  python tests/test_deliverables_verification.py
  ```
- **빌드 스크립트 실행 (EXE 제작)**:
  ```bash
  python deploy/build_exe.py
  ```

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="각주-및-기술-참고문헌"></a><a id="-각주-및-기술-참고문헌"></a>
## 📚 각주 및 기술 참고문헌

<a id="footnote-1"></a><a id="fn-1"></a>
[^1]: Chrome 131 BoringSSL 핸드셰이크는 WAF의 TLS 핑거프린팅 차단을 원천 무력화합니다. [↩ 본문으로 돌아가기](#fnref-1) · [⬆️ 목차 맨 위로 이동](#-목차)

<a id="footnote-2"></a><a id="fn-2"></a>
[^2]: wireproxy는 사용자 영역에서 WireGuard 프로토콜을 SOCKS5 프록시로 변환하는 경량 Go 바이너리입니다. [↩ 본문으로 돌아가기](#fnref-2) · [⬆️ 목차 맨 위로 이동](#-목차)

[⬆️ 목차 맨 위로 이동](#-목차)
