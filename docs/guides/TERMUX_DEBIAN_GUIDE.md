# 📱 안드로이드 모바일 Termux (데비안 환경) D4UC 완벽 가이드

안드로이드 스마트폰의 **Termux**와 **proot-distro (Debian)** 환경을 활용하여, PC를 켜두지 않고도 휴대폰에서 24시간 무중단으로 디스코드 닉네임 전수검사를 돌리는 방법입니다.

---

## 🌟 왜 proot-distro 데비안인가요?
- 안드로이드 기본 Termux 쉘은 bionic C 라이브러리를 사용하여 일부 파이썬 C-확장 모듈(BoringSSL) 컴파일에 오류가 발생할 수 있습니다.
- **proot-distro debian**은 안드로이드 위에 **100% 표준 GNU/Linux (glibc ARM64)** 환경을 구축하므로, PC 리눅스와 동일하게 `curl_cffi` 및 `wireproxy`가 네이티브 속도로 완벽히 구동됩니다.

---

## 🚀 1. 설치 및 환경 세팅 (최초 1회, 약 2~3분)

### 1단계: Termux 앱 설치
- 구글 플레이스토어 버전은 업데이트가 중단되었으므로, **F-Droid** 또는 **GitHub 공식 릴리즈**에서 Termux 최신 APK를 다운로드하여 설치합니다.
- Termux 실행 후 저장소 권한 설정:
```bash
termux-setup-storage
```
*(화면에 사진/미디어 접근 권한 팝업이 뜨면 **허용**을 누르세요)*

### 2단계: 데비안 리눅스 환경 원클릭 설치 및 진입 (1줄 복사)
```bash
pkg update -y && pkg install git proot-distro -y && proot-distro install debian && proot-distro login debian
```
*(다운로드와 설치가 완료되면 프롬프트가 `root@localhost:~#` 로 바뀌며 데비안 진입에 성공합니다)*

---

## 📦 2. D4UC 소스코드 다운로드 및 원클릭 자동 설치

### 1단계: D4UC 다운로드 (Git Clone)
*(반드시 `root@localhost:~#` 상태에서 입력하세요)*
```bash
git clone https://github.com/KRCUPRO/discord-checker.git
cd discord-checker
```

### 2단계: 자동 설치 스크립트 실행
```bash
chmod +x deploy/install_debian.sh deploy/run.sh
./deploy/install_debian.sh
```
> **자동 수행 작업**:
> 1. ARM64(aarch64) 아키텍처 자동 감지
> 2. `python3`, `pip`, `venv`, `curl`, `wireguard-tools` 설치
> 3. `.venv` 가상환경 및 `requirements.txt` (`curl_cffi`, `rich`, `pyyaml`, `customtkinter`) 설치
> 4. Linux ARM64 네이티브 `wireproxy` 바이너리 자동 다운로드 및 `bin/wireproxy` 배치

---

## ⚡ 3. 실행 방법 (Usage)

### 1) 기본 대화형 터미널 대시보드 실행
```bash
./deploy/run.sh
```
*(터미널에 실시간 RPS, 검사 완료 수, 발견 닉네임 등이 미려한 Rich 콘솔 UI로 출력됩니다)*

### 2) 다중 창 2배 속도 분할 샤딩 실행
- **1번 작업 (a ~ m 시작 닉네임 전담)**:
```bash
./deploy/run.sh --mode permutation --shard 2_1 --workers 5
```
- **2번 작업 (n ~ _ 시작 닉네임 전담)**:
```bash
./deploy/run.sh --mode permutation --shard 2_2 --workers 5
```
*(PC와 휴대폰을 각각 2_1, 2_2로 나눠 돌리시면 집 밖에서도 PC와 함께 2배 속도로 전수검사를 끝냅니다!)*

### 3) Surfshark VPN 개인키 즉시 주입 실행
```bash
SURFSHARK_PRIVATE_KEYS="내_와이어가드_개인키" ./deploy/run.sh --workers 5
```

---

## 🌙 4. 휴대폰 화면 끄고 24시간 백그라운드 무중단 실행 (절전 방지)

안드로이드 OS가 화면이 꺼졌을 때 Termux 프로세스를 강제 종료(Doze Mode)하지 않도록 설정합니다:

### 1. Termux 절전 방지 활성화 (Termux 기본 쉘에서)
```bash
termux-wake-lock
```
*(알림창에 `Termux (wake lock held)` 고정 알림이 표시됩니다)*

### 2. 데비안 로그인 후 백그라운드 무중단 데몬 실행 (`nohup`)
```bash
proot-distro login debian
cd discord-checker
nohup ./deploy/run.sh --no-dashboard --mode permutation --shard 2_1 --workers 5 > d4uc.log 2>&1 &
```

### 3. 실시간 로그 모니터링
```bash
tail -f d4uc.log
```

### 4. 검사기 종료 시
```bash
pkill -f "python3 src/run.py"
```

### 5. 발견된 가용 닉네임 확인
```bash
cat available.txt
```
*(디스코드 웹훅을 등록해두셨다면 레어 닉네임 발견 즉시 모바일 디스코드 앱으로 실시간 핑 알림이 옵니다!)*

---

## 🔧 5. 자주 묻는 질문 및 문제 해결 (FAQ & Troubleshooting)

### Q1. `./deploy/install_debian.sh: line 52: sudo: command not found` 오류가 발생해요.
- **원인**: 데비안 환경(`proot-distro login debian`)에 들어가지 않고 안드로이드 Termux 기본 쉘에서 스크립트를 실행했을 때 발생합니다.
- **해결책**:
  1. `proot-distro login debian` 명령어를 실행하여 데비안으로 먼저 로그인하세요.
  2. 프롬프트가 `root@localhost:~#`로 바뀌었는지 확인한 후, `cd discord-checker && ./deploy/install_debian.sh`를 실행하세요.
  *(v12.1.0 최신 스크립트에서는 Termux 쉘에서 실행하더라도 자동으로 감지하여 Debian 패키지를 준비해 줍니다)*

### Q2. `ModuleNotFoundError: No module named 'rich'` 오류가 떠요.
- **원인**: 라이브러리 설치 단계(`install_debian.sh`)를 건너뛰고 바로 `run.sh`를 실행했거나 설치가 중간에 중단된 경우입니다.
- **해결책**:
  ```bash
  cd discord-checker
  ./deploy/install_debian.sh
  ```
  설치가 정상 완료된 후 `./deploy/run.sh`를 실행하면 정상 구동됩니다.

### Q3. 스마트폰을 재부팅한 후 다시 체커를 켤 때는 어떻게 하나요?
다음 2줄만 입력하시면 즉시 다시 실행됩니다:
```bash
proot-distro login debian
cd discord-checker && ./deploy/run.sh
```
