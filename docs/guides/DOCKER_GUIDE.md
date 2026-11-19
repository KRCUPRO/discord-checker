# 🐳 D4UC 도커(Docker & Docker Compose) 완벽 가이드 (DOCKER_GUIDE.md)

> **프로젝트**: D4UC (`discord-checker`) v12.3.0 / v12.4.0  
> **대상 플랫폼**: Linux (Ubuntu, Debian, CentOS, Alpine), Cloud VPS (AWS, Oracle Cloud ARM/AMD, GCP), Raspberry Pi, NAS (Synology, QNAP)  
> **지원 아키텍처**: `linux/amd64` (Intel/AMD) & `linux/arm64` (ARMv8/Apple Silicon/Ampere)  
> **최종 개정일**: 2026년 11월 19일  

---

<a id="목차"></a><a id="-목차"></a>
## 📑 목차
1. [도커 환경의 핵심 장점 & 아키텍처](#-도커-환경의-핵심-장점--아키텍처)
2. [실행 화면 미리보기](#-실행-화면-미리보기)
3. [빠른 시작 (Docker Compose) - 가장 권장](#-빠른-시작-docker-compose---가장-권장)
4. [2배속 병렬 분할 (2-Shard Multi-Container) 구동](#-2배속-병렬-분할-2-shard-multi-container-구동)
5. [Docker CLI 직접 빌드 및 단독 실행](#-docker-cli-직접-빌드-및-단독-실행)
6. [볼륨 마운트 및 영구 데이터 보존](#-볼륨-마운트-및-영구-데이터-보존)
7. [환경 변수 전체 명세](#-환경-변수-전체-명세)
8. [컨테이너 모니터링 & 문제 해결](#-컨테이너-모니터링--문제-해결)
9. [각주 및 기술 참고문헌](#-각주-및-기술-참고문헌)

---

<a id="도커-환경의-핵심-장점--아키텍처"></a><a id="-도커-환경의-핵심-장점--아키텍처"></a>
## 🌟 도커 환경의 핵심 장점 & 아키텍처

D4UC(Discord Username Checker)를 도커 컨테이너로 패키징하여, 리눅스 서버나 NAS 등에서 호스트 환경에 구애받지 않고 24시간 무중단으로 안정 구동할 수 있습니다.

1. **완벽한 환경 격리 (Zero Dependency)**:
   - 호스트 머신에 Python, gcc, wireguard 도구를 따로 설치할 필요 없이 도커 엔진만 있으면 즉시 실행 가능합니다.
2. **멀티 아키텍처(Multi-Arch) 자동 감지 지원**:
   - `linux/amd64` (인텔/AMD 서버) 및 `linux/arm64` (라즈베리파이, 오라클 ARM 인스턴스, 애플 실리콘 Mac) 모두 지원하며 아키텍처에 맞는 `wireproxy` 바이너리를 자동 번들링합니다.
3. **볼륨 마운트를 통한 영구 데이터 보존**:
   - 컨테이너 내부의 `/app/data` 경로가 호스트 디렉토리(`./data`)와 1:1 바인드되어, 컨테이너를 삭제하거나 재부팅해도 SQLite WAL DB와 `available.txt`가 100% 영구 보존됩니다.
4. **멀티 컨테이너 샤딩(병렬 2배속) 원클릭 지원**:
   - Docker Compose 프로파일(`2shard`)을 활용해 단 한 줄의 명령어로 알파벳 범위를 절반씩 분할(a~m / n~_)한 2개의 독립 컨테이너를 동시 기동하여 2배 속도로 전수검사를 수행합니다.

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="실행-화면-미리보기"></a><a id="-실행-화면-미리보기"></a>
## 📸 실행 화면 미리보기

[![D4UC Docker Environment](../assets/docker_linux_capture.png)](DOCKER_GUIDE.md)

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="빠른-시작-docker-compose---가장-권장"></a><a id="-빠른-시작-docker-compose---가장-권장"></a>
## 🚀 빠른 시작 (Docker Compose) - 가장 권장

### 1단계: 저장소 이동 및 디렉터리 준비
```bash
git clone https://github.com/KRCUPRO/discord-checker.git
cd discord-checker
mkdir -p data
```

### 2단계: 환경 변수 설정 (.env)
```bash
cat << 'EOF' > .env
SURFSHARK_PRIVATE_KEYS=YOUR_SURFSHARK_KEY_HERE
D4UC_WEBHOOK=https://discord.com/api/webhooks/your/webhook/url
D4UC_WORKERS=5
D4UC_MODE=hybrid
D4UC_LENGTH=4
EOF
```

### 3단계: 기본 컨테이너 백그라운드 실행
```bash
# 백그라운드 빌드 및 기동
docker compose -f deploy/docker-compose.yml up -d

# 실시간 검사 로그 확인 (스트리밍)
docker compose -f deploy/docker-compose.yml logs -f d4uc
```

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="2배속-병렬-분할-2-shard-multi-container-구동"></a><a id="-2배속-병렬-분할-2-shard-multi-container-구동"></a>
## ⚡ 2배속 병렬 분할 (2-Shard Multi-Container) 구동

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

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="docker-cli-직접-빌드-및-단독-실행"></a><a id="-docker-cli-직접-빌드-및-단독-실행"></a>
## 🛠️ Docker CLI 직접 빌드 및 단독 실행

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
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -e D4UC_MODE=hybrid \
  -e D4UC_LENGTH=4 \
  -e D4UC_WORKERS=5 \
  -e D4UC_PROXY=surfshark \
  -e SURFSHARK_PRIVATE_KEYS="키1,키2" \
  -e D4UC_WEBHOOK="https://discord.com/api/webhooks/..." \
  d4uc:latest
```

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="볼륨-마운트-및-영구-데이터-보존"></a><a id="-볼륨-마운트-및-영구-데이터-보존"></a>
## 💾 볼륨 마운트 및 영구 데이터 보존

- 컨테이너 내부의 `/app/data` 디렉터리는 호스트의 `./data`와 동기화됩니다.
- 생성되는 파일:
  * `d4uc_results.db`: SQLite 트랜잭션 데이터베이스
  * `available.txt`: 발견된 가용 닉네임 목록
  * `taken.txt`: 선점된 닉네임 목록
  * `checked_history.txt`: 중복 검사 방지 캐시

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="환경-변수-전체-명세"></a><a id="-환경-변수-전체-명세"></a>
## 🌐 환경 변수 전체 명세

| 환경 변수 | 기본값 | 설명 및 유효값 |
| :--- | :--- | :--- |
| `D4UC_MODE` | `hybrid` | 생성 모드 (`hybrid`, `permutation`, `dictionary`, `pattern`, `numeric`, `custom_mask`, `combinatorial`, `recheck`) |
| `D4UC_LENGTH` | `4` | 닉네임 자릿수 (`3`, `4`, `5`, `6`) |
| `D4UC_WORKERS` | `5` | 동시 검사 워커 스레드 수 (`1` ~ `50`) |
| `D4UC_PROXY` | `surfshark` | 프록시 모드 (`surfshark`, `free`, `file`, `direct`) |
| `SURFSHARK_PRIVATE_KEYS` | (없음) | 콤마(,)로 구분된 Surfshark WireGuard 개인키 목록 |
| `D4UC_WEBHOOK` | (없음) | 가용 닉네임 발견 시 알림을 수신할 Discord Webhook URL |

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="컨테이너-모니터링--문제-해결"></a><a id="-컨테이너-모니터링--문제-해결"></a>
## 🔧 컨테이너 모니터링 & 문제 해결

| 증상 | 진단 및 해결책 |
| :--- | :--- |
| **컨테이너 즉시 종료** | `docker logs d4uc` 확인. `credentials.json` 또는 WireGuard 개인키 누락 여부 확인. |
| **`Permission denied: /app/data`** | 호스트 디렉터리 권한 확인 (`chmod -R 777 data`). |
| **Web GUI 접속 불가** | 포트 매핑 `-p 5000:5000` 확인 및 호스트 방화벽 점검. |

[⬆️ 목차 맨 위로 이동](#-목차)

---

<a id="각주-및-기술-참고문헌"></a><a id="-각주-및-기술-참고문헌"></a>
## 📚 각주 및 기술 참고문헌

[^1]: Multi-Arch 컨테이너는 Docker Buildx 엔진을 통해 `linux/amd64`와 `linux/arm64` 이미지를 단일 태그로 제공합니다. [↩](#-목차)

[⬆️ 목차 맨 위로 이동](#-목차)
