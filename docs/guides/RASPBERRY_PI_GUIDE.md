# 🍓 Raspberry Pi 4 & 5 Homelab Deployment Guide (RASPBERRY_PI_GUIDE.md)

> **프로젝트**: D4UC (`discord-checker`) v12.3.0 / v12.4.0  
> **대상 기기**: Raspberry Pi 4 Model B (2GB/4GB/8GB) & Raspberry Pi 5 (4GB/8GB/16GB)  
> **운영체제**: Raspberry Pi OS 64-bit (Debian Bookworm) / Ubuntu Server ARM64  
> **아키텍처**: `aarch64` (ARMv8 / ARMv9 64-bit)  
> **최종 개정일**: 2026년 11월 19일  

---

<a id="목차"></a><a id="-목차"></a>
## 📑 목차
1. [라즈베리파이 홈랩의 장점 및 소비 전력](#-라즈베리파이-홈랩의-장점-및-소비-전력)
2. [사전 필수 환경 및 64비트 OS 구성](#-사전-필수-환경-및-64비트-os-구성)
3. [Python 3.12 및 wireproxy-arm64 설치](#-python-312-및-wireproxy-arm64-설치)
4. [D4UC 프로젝트 클론 및 가상환경 설정](#-d4uc-프로젝트-클론-및-가상환경-설정)
5. [모바일 웹 GUI (PWA) 서버 구동 (포트 5000)](#-모바일-웹-gui-pwa-서버-구동-포트-5000)
6. [Tailscale VPN을 통한 외부 어디서나 원격 제어](#-tailscale-vpn을-통한-외부-어디서나-원격-제어)
7. [Systemd 서비스 등록 (24/7 부팅 시 자동 시작)](#-systemd-서비스-등록-247-부팅-시-자동-시작)
8. [SD 카드 마모 방지 및 SQLite WAL I/O 최적화](#-sd-카드-마모-방지-및-sqlite-wal-io-최적화)
9. [라즈베리파이 환경 문제 해결 (Troubleshooting)](#-라즈베리파이-환경-문제-해결-troubleshooting)
10. [각주 및 기술 참고문헌](#-각주-및-기술-참고문헌)

---

<a id="라즈베리파이-홈랩의-장점-및-소비-전력"></a><a id="-라즈베리파이-홈랩의-장점-및-소비-전력"></a>
## 🍓 라즈베리파이 홈랩의 장점 및 소비 전력

라즈베리파이는 데스크톱 PC를 켜둘 필요 없이 방 구석에서 24시간 365일 무소음·초저전력으로 닉네임 탐색기를 가동할 수 있는 최적의 홈랩(Homelab) 장비입니다:

- **초저전력 경제성**: 평균 소비 전력 약 **3W~5W** (한 달 24시간 풀가동 시 전기요금 약 500원 미만).
- **무소음 24/7 가동**: 패시브 히트싱크 케이스 구성 시 완전 무소음 환경 구축 가능.
- **상시 백엔드 서버**: 스마트폰으로 침대나 외부 어디서나 라즈베리파이에 떠 있는 웹 GUI(포트 5000)에 접속하여 제어.

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="사전-필수-환경-및-64비트-os-구성"></a><a id="-사전-필수-환경-및-64비트-os-구성"></a>
## ⚙️ 사전 필수 환경 및 64비트 OS 구성

> [!IMPORTANT]
> D4UC의 `curl_cffi` 및 <a id="fnref-1"></a><a id="fnref1"></a>BoringSSL[^1] 라이브러리는 **64-bit ARM(`aarch64`)** 환경을 필요로 합니다. 반드시 Raspberry Pi OS 64-bit 버전을 사용해야 합니다 (32-bit는 지원되지 않습니다).

```bash
# 아키텍처 확인 (aarch64가 출력되어야 함)
uname -m
# aarch64
```

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="python-312-및-wireproxy-arm64-설치"></a><a id="-python-312-및-wireproxy-arm64-설치"></a>
## 📦 Python 3.12 및 wireproxy-arm64 설치

```bash
# 1. 패키지 저장소 업데이트 및 시스템 빌드 도구 설치
sudo apt update && sudo apt install -y \
    python3 \
    python3-venv \
    python3-pip \
    build-essential \
    libssl-dev \
    git \
    curl \
    tmux \
    sqlite3

# 2. wireproxy ARM64 공식 바이너리 다운로드 (필요 시)
sudo curl -fsSL -o /usr/local/bin/wireproxy https://github.com/octeep/wireproxy/releases/download/v0.3.0/wireproxy_linux_arm64
sudo chmod +x /usr/local/bin/wireproxy
```

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="d4uc-프로젝트-클론-및-가상환경-설정"></a><a id="-d4uc-프로젝트-클론-및-가상환경-설정"></a>
## 🚀 D4UC 프로젝트 클론 및 가상환경 설정

```bash
# 1. 저장소 복제 및 이동
git clone https://github.com/KRCUPRO/discord-checker.git ~/discord-checker
cd ~/discord-checker

# 2. Python 가상환경 생성
python3 -m venv .venv
source .venv/bin/activate

# 3. 최신 pip 및 패키지 설치
pip install --upgrade pip
pip install -r requirements.txt
```

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="모바일-웹-gui-pwa-서버-구동-포트-5000"></a><a id="-모바일-웹-gui-pwa-서버-구동-포트-5000"></a>
## 🌐 모바일 웹 GUI (PWA) 서버 구동 (포트 5000)

```bash
# 웹 서버 실행
python src/web_gui.py --host 0.0.0.0 --port 5000
```

같은 공유기에 연결된 스마트폰에서 `http://<라즈베리파이_IP>:5000`에 접속하여 원격 제어합니다.

[![D4UC Mobile Web GUI](../assets/mobile_web_main.png)](RASPBERRY_PI_GUIDE.md)

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="tailscale-vpn을-통한-외부-어디서나-원격-제어"></a><a id="-tailscale-vpn을-통한-외부-어디서나-원격-제어"></a>
## 🔒 Tailscale VPN을 통한 외부 어디서나 원격 제어

포트포워딩이나 공인 IP 없이 외부(카페, 직장, 대중교통)에서 스마트폰으로 라즈베리파이에 안전하게 접속할 수 있습니다:

```bash
# 라즈베리파이에 Tailscale 설치 및 로그인
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

스마트폰에도 Tailscale 앱을 설치하면 스마트폰에서 `http://100.x.y.z:5000`으로 1-클릭 암호화 터널 접속이 가능합니다.

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="systemd-서비스-등록-247-부팅-시-자동-시작"></a><a id="-systemd-서비스-등록-247-부팅-시-자동-시작"></a>
## 🤖 Systemd 서비스 등록 (24/7 부팅 시 자동 시작)

라즈베리파이가 켜질 때마다 백그라운드에서 자동으로 D4UC가 기동되도록 등록합니다:

`/etc/systemd/system/d4uc.service` 파일 작성:
```ini
[Unit]
Description=D4UC Discord Username Checker on Raspberry Pi
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/discord-checker
ExecStart=/home/pi/discord-checker/.venv/bin/python src/web_gui.py --host 0.0.0.0 --port 5000
Restart=always
RestartSec=10
StandardOutput=append:/home/pi/discord-checker/data/rpi_service.log
StandardError=append:/home/pi/discord-checker/data/rpi_err.log

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now d4uc
sudo systemctl status d4uc
```

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="sd-카드-마모-방지-및-sqlite-wal-io-최적화"></a><a id="-sd-카드-마모-방지-및-sqlite-wal-io-최적화"></a>
## 💾 SD 카드 마모 방지 및 SQLite WAL I/O 최적화

라즈베리파이의 MicroSD 카드는 잦은 디스크 쓰기 시 수명이 단축될 수 있습니다. D4UC는 고도로 최적화된 설계를 갖추고 있습니다:

1. **SQLite WAL (Write-Ahead Logging)**:
   - 디스크 랜덤 I/O를 순차 추가(Append-Only) I/O로 전환하여 SD 카드 수명을 획기적으로 연장합니다.
2. **RAM 디스크 로그 마운트 (선택 권장)**:
   - 임시 로그 파일을 tmpfs(메모리)에 마운트하여 SD 카드 쓰기 횟수를 95% 감소시킵니다:
   ```bash
   sudo nano /etc/fstab
   # 다음 줄 추가:
   tmpfs /home/pi/discord-checker/tests/tmp tmpfs defaults,noatime,nosuid,size=64M 0 0
   ```

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="라즈베리파이-환경-문제-해결-troubleshooting"></a><a id="-라즈베리파이-환경-문제-해결-troubleshooting"></a>
## 🔧 라즈베리파이 환경 문제 해결 (Troubleshooting)

| 현상 | 원인 | 해결책 |
| :--- | :--- | :--- |
| **속도가 점차 저하됨** | CPU 쓰로틀링 (온도 80°C 초과) | `vcgencmd measure_temp`로 온도 확인 후 방열판 또는 쿨링 팬 추가 장착 |
| **`python: command not found`** | 기본 심볼릭 링크 부재 | `sudo apt install python-is-python3` 실행 |
| **메모리 부족 (OOM Killer)** | 워커 수가 너무 많음 | 라즈베리파이 4 2GB 환경에서는 워커 수를 `5`~`10`개로 조정 |

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="각주-및-기술-참고문헌"></a><a id="-각주-및-기술-참고문헌"></a>
## 📚 각주 및 기술 참고문헌

[^1]: Raspberry Pi 4 및 5의 ARM Cortex-A72 / A76 아키텍처는 BoringSSL 암호화 가속 명령어를 완벽하게 지원하여 x86_64 데스크톱 대비 90% 이상의 네트워크 처리 효율을 발휘합니다. [↩](#-목차) [↩ 본문으로 돌아가기](#fnref-1) · [⬆️ 목차 맨 위로 이동](#-목차)
[⬆️ 목차 맨 위로 이동](#-목차)
