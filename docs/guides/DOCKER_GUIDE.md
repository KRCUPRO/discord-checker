# 🐳 D4UC 도커(Docker & Docker Compose) 완벽 가이드

D4UC(Discord Username Checker)를 도커 컨테이너로 패키징하여, 리눅스 서버(Ubuntu, Debian, CentOS), 클라우드 VPS(AWS, Oracle Cloud ARM/AMD, GCP), 라즈베리파이, NAS(Synology, QNAP) 등에서 호스트 환경에 구애받지 않고 24시간 무중단으로 안정 구동하는 방법입니다.

---

## 🌟 도커 환경의 핵심 장점
1. **완벽한 환경 격리 (Zero Dependency)**:
   - 호스트 머신에 Python, gcc, wireguard 도구를 따로 설치할 필요 없이 도커 엔진만 있으면 즉시 실행 가능합니다.
2. **멀티 아키텍처(Multi-Arch) 자동 감지 지원**:
   - `linux/amd64` (인텔/AMD 서버) 및 `linux/arm64` (라즈베리파이, 오라클 ARM 인스턴스, 애플 실리콘 Mac) 모두 지원하며 아키텍처에 맞는 `wireproxy` 바이너리를 자동 번들링합니다.
3. **볼륨 마운트를 통한 영구 데이터 보존**:
   - 컨테이너 내부의 `/app/data` 경로가 호스트 디렉토리(`./data`)와 1:1 바인드되어, 컨테이너를 삭제하거나 재부팅해도 SQLite WAL DB와 `found.txt`가 100% 영구 보존됩니다.
4. **멀티 컨테이너 샤딩(병렬 2배속) 원클릭 지원**:
   - Docker Compose 프로파일(`2shard`)을 활용해 단 한 줄의 명령어로 알파벳 범위를 절반씩 분할(a~m / n~_)한 2개의 독립 컨테이너를 동시 기동하여 2배 속도로 전수검사를 수행합니다.

---

## 📸 실행 화면 미리보기
[![D4UC Docker Environment](../assets/docker_linux_capture.png)](DOCKER_GUIDE.md)

---

## 🚀 1. 빠른 시작 (Docker Compose) - 가장 권장

### 1단계: 저장소 이동 및 권한 확인
```bash
cd discord-checker
mkdir -p data
```

### 2단계: 환경 변수 설정 (.env 또는 직접 지정)
Surfshark 와이어가드 키 또는 웹훅 URL을 사용하려면 `.env` 파일을 생성하거나 실행 시 환경 변수를 전달합니다:
```bash
# .env 파일 생성 예시
cat << 'EOF' > .env
SURFSHARK_PRIVATE_KEYS=YOUR_SURFSHARK_KEY_HERE
D4UC_WEBHOOK=https://discord.com/api/webhooks/your/webhook/url
D4UC_WORKERS=5
D4UC_MODE=hybrid
D4UC_LENGTH=4
EOF
```

### 3단계: 기본 단일 컨테이너 백그라운드 실행
```bash
# 백그라운드 빌드 및 기동
docker compose -f deploy/docker-compose.yml up -d

# 실시간 검사 로그 확인 (스트리밍)
docker compose -f deploy/docker-compose.yml logs -f d4uc
```

---

## ⚡ 2. 2배속 병렬 분할 (2-Shard Multi-Container) 구동

단일 인스턴스 대비 2배의 속도로 검사를 완료하고 싶을 때, Docker Compose 프로파일 기능을 사용합니다:
- **Shard 1 (`d4uc-shard-1`)**: `a ~ m` 범위 담당
- **Shard 2 (`d4uc-shard-2`)**: `n ~ _` 범위 담당

```bash
# 2개 분할 컨테이너 동시 기동 (빌드 포함)
docker compose -f deploy/docker-compose.yml --profile 2shard up -d

# 두 컨테이너의 실시간 로그 동시 모니터링
docker compose -f deploy/docker-compose.yml --profile 2shard logs -f

# 1번 샤드 로그만 보기
docker logs -f d4uc-shard-1

# 2번 샤드 로그만 보기
docker logs -f d4uc-shard-2
```
> **팁**: 두 컨테이너 모두 호스트의 `./data/d4uc_results.db` SQLite 데이터베이스를 WAL 모드로 안전하게 공유하므로, 발견된 닉네임과 검사 완료 이력이 충돌 없이 실시간 동기화됩니다.

---

## 🛠️ 3. Docker CLI 직접 빌드 및 단독 실행

Docker Compose 없이 일반 `docker run` 명령어로 실행하는 방법:

### 1단계: 도커 이미지 빌드
```bash
docker build -f deploy/Dockerfile -t d4uc:latest .
```

### 2단계: 컨테이너 실행
```bash
docker run -d \
  --name d4uc-checker \
  --restart unless-stopped \
  -v $(pwd)/data:/app/data \
  -e D4UC_MODE=hybrid \
  -e D4UC_LENGTH=4 \
  -e D4UC_WORKERS=5 \
  -e D4UC_PROXY=surfshark \
  -e SURFSHARK_PRIVATE_KEYS="키1,키2" \
  -e D4UC_WEBHOOK="https://discord.com/api/webhooks/..." \
  d4uc:latest
```

### 3단계: 샤딩(범위 분할)으로 실행할 경우
```bash
# 1번 창 (a ~ m)
docker run -d --name d4uc-p1 -v $(pwd)/data:/app/data \
  -e D4UC_MODE=permutation -e D4UC_SHARD=2_1 d4uc:latest

# 2번 창 (n ~ _)
docker run -d --name d4uc-p2 -v $(pwd)/data:/app/data \
  -e D4UC_MODE=permutation -e D4UC_SHARD=2_2 d4uc:latest
```

---

## 📋 4. 지원 환경 변수 (Environment Variables Reference)

| 환경 변수 | 기본값 | 허용 값 / 설명 |
| :--- | :--- | :--- |
| `D4UC_MODE` | `hybrid` | `hybrid`(하이브리드 추천), `permutation`(순열 전수조사), `random`(무작위) |
| `D4UC_LENGTH` | `4` | 닉네임 글자 수 (`3`, `4`, `5` 등) |
| `D4UC_WORKERS` | `5` | 동시 검사 워커 수 (`1` ~ `10`) |
| `D4UC_PROXY` | `surfshark` | `surfshark` (1:1 국가 터널) 또는 `off` (호스트 직접 연결) |
| `D4UC_SHARD` | 없음 | 분할 샤딩 (`2_1`, `2_2`, `3_1`, `3_2`, `3_3`, `4_1` 등) |
| `SURFSHARK_PRIVATE_KEYS` | 없음 | Surfshark 와이어가드 개인키 (여러 개인 경우 쉼표로 구분) |
| `D4UC_WEBHOOK` | 없음 | 닉네임 발견 시 알림을 보낼 디스코드 웹훅 URL |
| `D4UC_NO_DASHBOARD` | `1` | 터미널 대시보드 화면 지우기 대신 실시간 한 줄 로그 모드 활성화 |

---

## 📊 5. 컨테이너 관리 및 점검 명령어 요약

```bash
# 실행 중인 컨테이너 상태 확인
docker ps

# 실시간 리소스(CPU, 메모리) 사용량 확인
docker stats

# 실행 중인 컨테이너 일시 중지 및 재개
docker pause d4uc-checker
docker unpause d4uc-checker

# 컨테이너 중단 및 삭제
docker compose down
# 2shard 프로파일까지 완전히 중단
docker compose --profile 2shard down

# 호스트에 저장된 결과 파일 확인
cat ./data/found.txt
ls -lh ./data/d4uc.db
```
