# 🧭 D4UC (Discord Username Checker) 프로젝트 마스터 가이드

> **D4UC (Discord 4-Character Usernames Checker)**  
> Chrome 131 TLS 스텔스 위장 + Surfshark 1:1 다중 국가 터널 풀 + SQLite WAL 멀티 인스턴스 무충돌 동기화 기반의 고성능 디스코드 닉네임 전수검사 및 가용성 탐색 엔진

---

## 📑 목차
1. [프로젝트 개요 및 핵심 아키텍처](#1-프로젝트-개요-및-핵심-아키텍처)
2. [4대 실행 환경별 빠른 시작](#2-4대-실행-환경별-빠른-시작)
   - [A. 데스크톱 GUI (Windows)](#a-데스크톱-gui-windows)
   - [B. 헤드리스 CLI (Terminal)](#b-헤드리스-cli-terminal)
   - [C. 안드로이드 모바일 (Termux Debian)](#c-안드로이드-모바일-termux-debian)
   - [D. 도커 컨테이너 (Docker & Compose)](#d-도커-컨테이너-docker--compose)
3. [8대 닉네임 생성 및 탐색 모드](#3-8대-닉네임-생성-및-탐색-모드)
4. [프록시 인프라 및 다중 국가 터널링](#4-프록시-인프라-및-다중-국가-터널링)
5. [다중 창/다중 컨테이너 분할 샤딩 (2배~4배 가속)](#5-다중-창다중-컨테이너-분할-샤딩-2배4배-가속)
6. [깃허브(GitHub) 안전 배포 및 보안 수칙](#6-깃허브github-안전-배포-및-보안-수칙)
7. [바이브 코딩 구조 및 개발자 유지보수 가이드](#7-바이브-코딩-구조-및-개발자-유지보수-가이드)

---

## 1. 프로젝트 개요 및 핵심 아키텍처

- **엔진 원리**: 디스코드 가입 API(`https://discord.com/api/v9/unique-username/username-attempt-unauthed`) 엔드포인트를 대상으로, Cloudflare/WAF 차단 없이 합법적인 비로그인 가용 여부를 초고속 판별합니다.
- **핵심 차별화 기술**:
  1. **Chrome 131 TLS JA3/JA4 스텔스 위장**: Python 표준 requests의 지문 차단을 극복하고 최신 크롬 브라우저와 100% 동일한 TLS 핸드셰이크 전송 (`curl_cffi`).
  2. **Surfshark 1:1 독립 국가 터널 풀 (`wireproxy`)**: OS 네트워크 카드를 건드리지 않고 유저스페이스에서 전세계 142개국 엔드포인트를 로컬 루프백(`127.0.0.1:1081~1085`)으로 1:1 매핑.
  3. **429 레이트리밋 원자적 핫스왑 (Atomic Hot-Swap)**: 특정 워커가 429를 맞으면 해당 워커의 터널만 0.3초 만에 새 국가로 원자적 교체하고, 타 워커는 중단 없이 100% 풀스피드 유지.
  4. **SQLite WAL 멀티 프로세스 동기화**: 프로그램을 여러 개 띄워도 `d4uc_results.db`를 안전하게 공유하여 중복 검사 0% 및 실시간 발견 닉네임 크로스 팝업.

---

## 2. 4대 실행 환경별 빠른 시작

### A. 데스크톱 GUI (Windows)
```bash
# 한글 인터페이스 실행
python src/gui_ko.py

# 영문 인터페이스 실행
python src/gui_en.py

# 또는 모듈 실행
python -m src.gui_ko
```

### B. 헤드리스 CLI (Terminal)
```bash
# 기본 실행 (하이브리드 모드, 4자리, 5워커)
python src/run.py

# 2분할 1번 창 (a~m 범위) 실행
python src/run.py --mode permutation --length 4 --shard 2_1 --workers 5

# 대시보드 화면 지우기 없이 한 줄 스트리밍 로그 모드 (백그라운드 nohup 권장)
python src/run.py --no-dashboard
```

### C. 안드로이드 모바일 (Termux Debian)
> PC 없이 스마트폰에서 24시간 무중단 검사를 돌리는 모바일 솔루션  
> 상세 매뉴얼: [TERMUX_DEBIAN_GUIDE.md](guides/TERMUX_DEBIAN_GUIDE.md)

```bash
# Termux 내 Debian 환경 진입 후 원클릭 설치
chmod +x deploy/install_debian.sh deploy/run.sh
./deploy/install_debian.sh

# 24시간 백그라운드 무중단 실행 (화면 꺼짐 방지)
termux-wake-lock
nohup ./deploy/run.sh --no-dashboard > output.log 2>&1 &
```

### D. 도커 컨테이너 (Docker & Compose)
> 리눅스 서버, 클라우드 VPS, 라즈베리파이, NAS 전용 패키징  
> 상세 매뉴얼: [DOCKER_GUIDE.md](guides/DOCKER_GUIDE.md)

```bash
# 단일 컨테이너 백그라운드 구동
docker compose -f deploy/docker-compose.yml up -d

# 2배속 병렬 분할 (a~m / n~_) 2개 컨테이너 동시 기동
docker compose -f deploy/docker-compose.yml --profile 2shard up -d

# 실시간 스트리밍 로그 확인
docker compose -f deploy/docker-compose.yml logs -f
```

---

## 3. 8대 닉네임 생성 및 탐색 모드

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

---

## 4. 프록시 인프라 및 다중 국가 터널링

1. **Surfshark WireGuard 1:1 터널 (기본값)**:
   - `data/surfshark_clusters.json`의 142개국 엔드포인트(:51820 UDP)와 `credentials.json`의 개인키를 결합.
   - 워커 번호마다 `1081`, `1082`, `1083` 포트를 순차 배정하여 완전히 격리된 국가 IP로 요청.
2. **ThorData 프록시**:
   - `config.yaml`에 호스트/계정 등록 시 매 N회 요청마다 세션 자동 교체.
3. **파일 기반 프록시 풀 (`proxies.txt`)**:
   - 직접 수집한 HTTP/SOCKS5 프록시 목록을 텍스트 파일로 연동하여 라운드로빈 순환.
4. **다이렉트 (Direct)**:
   - 프록시 없이 로컬 PC 인터넷 직통 연결 (테스트용).

---

## 5. 다중 창/다중 컨테이너 분할 샤딩 (2배~4배 가속)

- **2분할**:
  - **1번 창**: `a ~ m` 시작 (전체 순열의 50%)
  - **2번 창**: `n ~ _` 시작 (전체 순열의 50%)
  - **수학적 중복 0%**: 두 창이 검사하는 대상이 정확히 절반씩 나누어져 2배 빠르게 전체 검사 완료.
- **3분할**: `a~i` / `j~r` / `s~_`
- **4분할**: `a~g` / `h~n` / `o~u` / `v~_`
- **직접 지정**: 원하는 시작 글자와 끝 글자를 직접 정의 (`--start-char`, `--end-char`).

---

## 6. 깃허브(GitHub) 안전 배포 및 보안 수칙

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

---

## 7. 체계적 코드 구조 및 개발자 유지보수 가이드

- **프로젝트 맵**: [ARCHITECTURE_MAP.md](ARCHITECTURE_MAP.md)
- **작업 인덱스 & 백로그**: [TASKS.md](TASKS.md)
- **단위 테스트 실행**:
  ```bash
  python -m unittest discover -s tests
  ```
- **빌드 스크립트 실행 (EXE 제작)**:
  ```bash
  python deploy/build_exe.py
  ```
