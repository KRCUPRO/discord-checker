#!/usr/bin/env bash
# ==============================================================================
# D4UC (Discord Username Checker) - Debian / Termux proot-distro Installer
# Supports: Android Termux (proot-distro debian), Debian 11/12, Ubuntu 20.04/22.04/24.04
# Architecture: ARM64 (aarch64) & AMD64 (x86_64)
# ==============================================================================

set -e

# ANSI Color codes
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}================================================================${NC}"
echo -e "${GREEN}🚀 D4UC Mobile & Linux Debian 자동 설치 및 환경 설정 시작${NC}"
echo -e "${CYAN}================================================================${NC}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# 1. Architecture Detection
ARCH=$(uname -m)
echo -e "\n${YELLOW}[1단계] 시스템 아키텍처 감지...${NC}"
case "$ARCH" in
    aarch64|arm64)
        WIREPROXY_ARCH="arm64"
        echo -e "  ✅ 감지된 아키텍처: ${GREEN}ARM64 (aarch64) - 모바일 Termux / 라즈베리파이 / Apple Silicon${NC}"
        ;;
    x86_64|amd64)
        WIREPROXY_ARCH="amd64"
        echo -e "  ✅ 감지된 아키텍처: ${GREEN}AMD64 (x86_64) - 인텔/AMD PC 및 클라우드 VPS${NC}"
        ;;
    *)
        echo -e "  ${RED}❌ 지원되지 않는 아키텍처입니다: $ARCH${NC}"
        echo -e "  D4UC는 aarch64(ARM64) 및 x86_64(AMD64)를 공식 지원합니다."
        exit 1
        ;;
esac

# 2. Package Manager & System Dependencies
echo -e "\n${YELLOW}[2단계] 시스템 필수 패키지 설치...${NC}"
if command -v apt-get >/dev/null 2>&1; then
    echo "  -> apt-get 패키지 업데이트 및 필수 패키지 설치 중..."
    if [ "$(id -u)" -eq 0 ]; then
        apt-get update -y
        apt-get install -y python3 python3-pip python3-venv git curl wget tar gzip ca-certificates
    else
        sudo apt-get update -y
        sudo apt-get install -y python3 python3-pip python3-venv git curl wget tar gzip ca-certificates
    fi
else
    echo -e "  ${YELLOW}⚠️ apt 패키지 관리자를 찾을 수 없습니다. python3 및 curl이 설치되어 있는지 확인하세요.${NC}"
fi

# 3. Python Virtual Environment
echo -e "\n${YELLOW}[3단계] Python 3 가상환경(.venv) 생성 및 라이브러리 설치...${NC}"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "  ✅ .venv 가상환경 생성 완료"
fi

# Activate venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel

echo "  -> requirements.txt 라이브러리 설치 중 (curl_cffi BoringSSL, rich, pyyaml)..."
pip install -r requirements.txt

# 4. Wireproxy Linux Native Binary Setup
echo -e "\n${YELLOW}[4단계] Linux 네이티브 wireproxy 바이너리 점검 및 다운로드...${NC}"
mkdir -p bin

if [ ! -f "bin/wireproxy" ]; then
    echo "  -> ${WIREPROXY_ARCH}용 wireproxy v1.0.6 다운로드 중..."
    WIREPROXY_URL="https://github.com/pufferffish/wireproxy/releases/download/v1.0.6/wireproxy_linux_${WIREPROXY_ARCH}.tar.gz"
    
    TMP_TGZ="/tmp/wireproxy_${WIREPROXY_ARCH}.tar.gz"
    if curl -sSL -f -o "$TMP_TGZ" "$WIREPROXY_URL"; then
        tar -xzf "$TMP_TGZ" -C bin wireproxy
        rm -f "$TMP_TGZ"
        chmod +x bin/wireproxy
        echo -e "  ✅ bin/wireproxy 설치 및 실행 권한 부여 완료"
    else
        echo -e "  ${YELLOW}⚠️ GitHub 다운로드 실패. 시스템 PATH에서 wireproxy 확인 중...${NC}"
        if command -v wireproxy >/dev/null 2>&1; then
            cp "$(command -v wireproxy)" bin/wireproxy
            chmod +x bin/wireproxy
            echo "  ✅ 시스템 wireproxy를 bin/wireproxy로 복사 완료"
        else
            echo -e "  ${YELLOW}⚠️ wireproxy 자동 다운로드에 실패했습니다. (Surfshark 터널 사용 시 go install github.com/pufferffish/wireproxy/cmd/wireproxy@latest 로 설치 가능)${NC}"
        fi
    fi
else
    chmod +x bin/wireproxy
    echo "  ✅ bin/wireproxy가 이미 존재합니다."
fi

# 5. Ensure Easy Launcher Script permissions (deploy/run.sh)
echo -e "\n${YELLOW}[5단계] 원터치 실행 런처(deploy/run.sh) 권한 설정...${NC}"
chmod +x deploy/run.sh
echo "  ✅ ./deploy/run.sh 실행 런처 준비 완료"

# 6. Ensure data directory exists
mkdir -p data results

echo -e "\n${CYAN}================================================================${NC}"
echo -e "${GREEN}🎉 D4UC 데비안 / Termux 설치가 성공적으로 완료되었습니다!${NC}"
echo -e "${CYAN}================================================================${NC}"
echo -e "\n${YELLOW}💡 [실행 방법 안내]${NC}"
echo -e "  1. 기본 실행 (설정 파일 기반):"
echo -e "     ${CYAN}./deploy/run.sh${NC}"
echo -e "\n  2. 다중 창 2배 속도 분할 샤딩 실행 (1번 창):"
echo -e "     ${CYAN}./deploy/run.sh --mode permutation --shard 2_1 --workers 5${NC}"
echo -e "\n  3. 다중 창 2배 속도 분할 샤딩 실행 (2번 창):"
echo -e "     ${CYAN}./deploy/run.sh --mode permutation --shard 2_2 --workers 5${NC}"
echo -e "\n  4. Surfshark WireGuard 개인키 즉시 주입 실행:"
echo -e "     ${CYAN}SURFSHARK_PRIVATE_KEY=\"내_개인키\" ./deploy/run.sh --workers 5${NC}"
echo -e "\n  5. 백그라운드 무중단 실행 (화면 끄고 계속 돌리기):"
echo -e "     ${CYAN}nohup ./deploy/run.sh --no-dashboard > d4uc.log 2>&1 &${NC}"
echo -e "${CYAN}================================================================${NC}\n"
