#!/usr/bin/env bash
# ==============================================================================
# D4UC (Discord Username Checker) - Google Colaboratory (Colab) Setup Script
# Architecture: Linux x86_64 (AMD64)
# ==============================================================================

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}================================================================${NC}"
echo -e "${GREEN}☁️ D4UC Google Colab 환경 자동 설정 시작${NC}"
echo -e "${CYAN}================================================================${NC}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 1. System APT Dependencies
echo -e "\n${YELLOW}[1단계] 시스템 패키지 설치 (curl, wireguard-tools)...${NC}"
apt-get update -qq > /dev/null 2>&1 || true
apt-get install -y -qq curl wireguard-tools > /dev/null 2>&1 || true
echo -e "  ✅ 시스템 패키지 준비 완료"

# 2. Python Dependencies
echo -e "\n${YELLOW}[2단계] Python 패키지 설치 (curl_cffi, rich, pyyaml 등)...${NC}"
pip install -q -r requirements.txt
echo -e "  ✅ Python 의존성 설치 완료"

# 3. Wireproxy Binary Installation
echo -e "\n${YELLOW}[3단계] Wireproxy v1.0.6 (Linux AMD64) 바이너리 설치...${NC}"
mkdir -p bin
mkdir -p data

if [ ! -f "bin/wireproxy" ]; then
    WIREPROXY_URL="https://github.com/pufferffish/wireproxy/releases/download/v1.0.6/wireproxy_linux_amd64.tar.gz"
    echo -e "  📥 다운로드 중: ${WIREPROXY_URL}"
    TMP_TGZ="/tmp/wireproxy_amd64.tar.gz"
    curl -sSL -o "$TMP_TGZ" "$WIREPROXY_URL"
    tar -xzf "$TMP_TGZ" -C bin/
    rm -f "$TMP_TGZ"
fi

chmod +x bin/wireproxy
cp bin/wireproxy /usr/local/bin/wireproxy 2>/dev/null || true
echo -e "  ✅ Wireproxy 바이너리 설치 완료: $(bin/wireproxy --version 2>&1 || echo 'wireproxy ready')"

# 4. Configuration Template Check
if [ ! -f "config.yaml" ] && [ -f "config.example.yaml" ]; then
    cp config.example.yaml config.yaml
    echo -e "  📄 config.example.yaml -> config.yaml 복사 완료"
fi

echo -e "\n${GREEN}================================================================${NC}"
echo -e "${GREEN}🎉 Google Colab 환경 설정이 성공적으로 완료되었습니다!${NC}"
echo -e "${GREEN}================================================================${NC}"
