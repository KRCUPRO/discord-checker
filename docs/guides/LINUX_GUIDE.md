# 🐧 Linux Server & VPS Deployment Guide (LINUX_GUIDE.md)

> **프로젝트**: D4UC (`discord-checker`) v12.3.0 / v12.4.0  
> **대상 배포판**: Ubuntu (20.04/22.04/24.04 LTS), Debian (11/12), Kali Linux, Fedora, Arch Linux, Rocky/RHEL 9, Alpine  
> **지원 아키텍처**: `x86_64` (AMD64) & `aarch64` (ARM64)  
> **최종 개정일**: 2026년 11월 19일  

---

<a id="목차"></a><a id="-목차"></a>
## 📑 목차
1. [지원 배포판 및 하드웨어 권장 사양](#-지원-배포판-및-하드웨어-권장-사양)
2. [배포판별 필수 시스템 패키지 설치](#-배포판별-필수-시스템-패키지-설치)
3. [Python 3.12 가상환경 및 의존성 구성](#-python-312-가상환경-및-의존성-구성)
4. [헤드리스 CLI 대시보드 및 백그라운드 구동](#-헤드리스-cli-대시보드-및-백그라운드-구동)
5. [모바일 반응형 Web GUI & PWA 백엔드 기동](#-모바일-반응형-web-gui--pwa-백엔드-기동)
6. [Systemd 서비스 등록 (d4uc.service) 24/7 데몬화](#-systemd-서비스-등록-d4ucservice-247-데몬화)
7. [UFW 및 iptables 방화벽 포트 설정](#-ufw-및-iptables-방화벽-포트-설정)
8. [다중 샤딩 병렬 분할 실행 (2배속~4배속 가속)](#-다중-샤딩-병렬-분할-실행-2배속4배속-가속)
9. [Linux 환경 문제 해결 (Troubleshooting)](#-linux-환경-문제-해결-troubleshooting)
10. [각주 및 기술 참고문헌](#-각주-및-기술-참고문헌)

---

<a id="지원-배포판-및-하드웨어-권장-사양"></a><a id="-지원-배포판-및-하드웨어-권장-사양"></a>
## 🐧 지원 배포판 및 하드웨어 권장 사양

D4UC는 리눅스 서버 환경에서 최소의 시스템 자원으로 24시간 365일 무중단 스캔을 수행할 수 있도록 설계되었습니다.

| 사양 항목 | 최소 사양 (VPS 1코어) | 권장 사양 (클라우드/전용 서버) |
| :--- | :--- | :--- |
| **CPU** | 1 vCPU (x86_64 또는 ARM64) | 2~4 vCPU |
| **메모리 (RAM)** | 512 MB (스왑 1GB 권장) | 2 GB 이상 |
| **스토리지** | 10 GB SSD | 30 GB NVMe |
| **대역폭** | 10 Mbps 무제한 | 100 Mbps 이상 (초당 20~30 요청 처리) |
| **OS 릴리스** | Ubuntu 22.04 LTS / Debian 12 Bookworm | Ubuntu 24.04 LTS / Debian 12 |

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="배포판별-필수-시스템-패키지-설치"></a><a id="-배포판별-필수-시스템-패키지-설치"></a>
## 📦 배포판별 필수 시스템 패키지 설치

### 1. Ubuntu / Debian / Kali Linux
```bash
sudo apt update && sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    libssl-dev \
    git \
    curl \
    tmux \
    sqlite3
```

### 2. Fedora / Rocky Linux / RHEL 9
```bash
sudo dnf update -y && sudo dnf install -y \
    python3 \
    python3-pip \
    gcc \
    openssl-devel \
    git \
    curl \
    tmux \
    sqlite
```

### 3. Arch Linux
```bash
sudo pacman -Syu --noconfirm \
    python \
    python-pip \
    base-devel \
    openssl \
    git \
    curl \
    tmux \
    sqlite
```

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="python-312-가상환경-및-의존성-구성"></a><a id="-python-312-가상환경-및-의존성-구성"></a>
## 🐍 Python 3.12 가상환경 및 의존성 구성

```bash
# 1. 저장소 클론
git clone https://github.com/KRCUPRO/discord-checker.git
cd discord-checker

# 2. 격리된 가상환경 구성
python3 -m venv .venv
source .venv/bin/activate

# 3. 의존성 패키지 설치
pip install --upgrade pip
pip install -r requirements.txt
```

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="헤드리스-cli-대시보드-및-백그라운드-구동"></a><a id="-헤드리스-cli-대시보드-및-백그라운드-구동"></a>
## 💻 헤드리스 CLI 대시보드 및 백그라운드 구동

### 1. tmux 기반 대화형 모니터링
```bash
tmux new -s d4uc
source .venv/bin/activate
python src/run.py --mode hybrid --length 4 --workers 10
# 백그라운드 전환: Ctrl + B 누른 후 D
```

### 2. nohup 기반 무인 스트리밍 로그 실행
```bash
nohup python src/run.py --no-dashboard > data/checker.log 2>&1 &
tail -f data/checker.log
```

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="모바일-반응형-web-gui--pwa-백엔드-기동"></a><a id="-모바일-반응형-web-gui--pwa-백엔드-기동"></a>
## 🌐 모바일 반응형 Web GUI & PWA 백엔드 기동

리눅스 서버에서 포트 5000을 열어 외부 어디서나 스마트폰이나 노트북으로 탐색을 제어합니다.

```bash
python src/web_gui.py --host 0.0.0.0 --port 5000
```

[![D4UC Docker Linux Capture](../assets/docker_linux_capture.png)](LINUX_GUIDE.md)

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="systemd-서비스-등록-d4ucservice-247-데몬화"></a><a id="-systemd-서비스-등록-d4ucservice-247-데몬화"></a>
## 🤖 Systemd 서비스 등록 (d4uc.service) 24/7 데몬화

서버가 재부팅되어도 자동으로 시작되는 프로덕션 레벨 서비스 구성입니다:

`/etc/systemd/system/d4uc.service` 파일 작성:
```ini
[Unit]
Description=D4UC Discord Username Checker Background Daemon
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/discord-checker
ExecStart=/root/discord-checker/.venv/bin/python src/web_gui.py --host 0.0.0.0 --port 5000
Restart=always
RestartSec=5
StandardOutput=append:/root/discord-checker/data/systemd_stdout.log
StandardError=append:/root/discord-checker/data/systemd_stderr.log
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
```

```bash
# 서비스 활성화 및 기동
sudo systemctl daemon-reload
sudo systemctl enable --now d4uc

# 실시간 동작 상태 확인
sudo systemctl status d4uc
sudo journalctl -u d4uc -f
```

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="ufw-및-iptables-방화벽-포트-설정"></a><a id="-ufw-및-iptables-방화벽-포트-설정"></a>
## 🛡️ UFW 및 iptables 방화벽 포트 설정

```bash
# UFW 방화벽 사용 시
sudo ufw allow 5000/tcp comment 'D4UC Web GUI'
sudo ufw allow 51820/udp comment 'WireGuard Outbound'
sudo ufw reload
```

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="다중-샤딩-병렬-분할-실행-2배속4배속-가속"></a><a id="-다중-샤딩-병렬-분할-실행-2배속4배속-가속"></a>
## 🔀 다중 샤딩 병렬 분할 실행 (2배속~4배속 가속)

2대 이상의 서버나 컨테이너에서 중복 없이 나누어 스캔하려면 샤딩 옵션을 전달합니다:

```bash
# 서버 A (샤드 1: a ~ m)
python src/run.py --mode permutation --length 4 --shard 2_1 --workers 10

# 서버 B (샤드 2: n ~ _)
python src/run.py --mode permutation --length 4 --shard 2_2 --workers 10
```

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="linux-환경-문제-해결-troubleshooting"></a><a id="-linux-환경-문제-해결-troubleshooting"></a>
## 🔧 Linux 환경 문제 해결 (Troubleshooting)

| 현상 | 원인 | 해결 방법 |
| :--- | :--- | :--- |
| **`ImportError: libssl.so`** | OpenSSL 개발 라이브러리 부재 | `sudo apt install libssl-dev` (Ubuntu/Debian) 실행 |
| **`Too many open files`** | 파일 디스크립터 한도 도달 | `ulimit -n 65535` 설정 및 `/etc/security/limits.conf` 수정 |
| **`sqlite3.OperationalError: database is locked`** | WAL 모드 미적용 | DB 연결 시 `PRAGMA journal_mode = WAL;`이 자동 적용되므로 최신 소스 확인 |

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="각주-및-기술-참고문헌"></a><a id="-각주-및-기술-참고문헌"></a>
## 📚 각주 및 기술 참고문헌

[^1]: Linux 환경에서 wireproxy 유저스페이스 바이너리는 루트(CAP_NET_ADMIN) 권한 없이 완전한 비권한 모드로 SOCKS5 프록시를 바인딩합니다. [↩](#-목차)

[⬆️ 목차 맨 위로 이동](#-목차)
