#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f "$PROJECT_ROOT/.venv/bin/activate" ]; then
    source "$PROJECT_ROOT/.venv/bin/activate"
else
    # Check if rich or curl_cffi is available in system python
    if ! python3 -c "import rich, curl_cffi" >/dev/null 2>&1; then
        echo -e "\033[0;31m❌ [오류] 필수 라이브러리(rich, curl_cffi)가 설치되지 않았거나 가상환경(.venv)이 없습니다.\033[0m"
        echo -e "\033[1;33m💡 먼저 설치 스크립트를 1회 실행해 주세요:\033[0m"
        echo -e "   \033[0;36mchmod +x deploy/install_debian.sh && ./deploy/install_debian.sh\033[0m\n"
        exit 1
    fi
fi

export PYTHONUNBUFFERED=1

# Run with arguments
exec python3 src/run.py "$@"
