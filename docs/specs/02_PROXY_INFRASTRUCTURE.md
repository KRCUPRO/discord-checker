# 02. 멀티 프로바이더 프록시 인프라 명세서
## (Multi-Provider Proxy Infrastructure & Dynamic Pool Architecture)

> **문서 버전**: 1.0.0  
> **프로젝트**: Discord Username Checker V2  
> **지원 프로토콜**: HTTP, HTTPS, SOCKS5, SOCKS5H  
> **지원 공급자**: ThorData Session API, 파일 기반 프록시 풀 (`proxies.txt`), 회전형 상용 프록시

---

## 1. 개요 및 배경 (Problem Statement)

기존 레거시 `main.py`는 단일 벤더인 `ThorData`에 하드코딩되어 있습니다:
```python
# [레거시 단일 종속 코드]
PROXY_USERNAME = "프록시 이름 넣는곳"
PROXY_PASSWORD = "프록시 비번 넣는곳"
PROXY_SERVER = "프록시 서버:포트 넣는곳"

def get_thordata_proxy():
    session_id = random.randint(100000, 999999)
    proxy_url = f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_SERVER}?session_id={session_id}"
    return {"http": proxy_url, "https": proxy_url}
```

이 방식은 다음과 같은 문제점을 안고 있습니다:
1. **타 프록시 공급자 사용 불가**: Webshare, BrightData, Oxylabs, Rayobyte 등 일반 프록시나 개인 SOCKS5 프록시 목록을 사용할 수 없음.
2. **시크릿 하드코딩 위험**: 소스 코드에 자격 증명이 노출되어 깃허브 커밋 시 크리덴셜 탈취 위험.
3. **데드 프록시(Dead Proxy) 무한 재시도**: 특정 세션이나 IP가 완전히 차단되어도 쿨다운 없이 계속 시도하여 요청 지연 및 실패율 급증.
4. **회전 및 가중치 제어 부재**: 프록시별 응답 지연 시간(Latency)과 성공률을 추적하지 못함.

---

## 2. 통합 프록시 추상화 아키텍처 (Proxy Abstraction Layer)

```mermaid
classDiagram
    class BaseProxyProvider {
        <<abstract>>
        +get_proxy() ProxyEndpoint
        +report_success(endpoint)
        +report_failure(endpoint, error_type)
        +get_pool_status() PoolStats
    }

    class ThorDataProxyProvider {
        -server: str
        -username: str
        -password: str
        +generate_session_proxy()
    }

    class FileProxyProvider {
        -file_path: Path
        -proxies: List[ProxyEndpoint]
        -alive_queue: asyncio.Queue
        +load_from_file()
        +filter_dead_proxies()
    }

    class RotatingApiProxyProvider {
        -api_url: str
        -api_key: str
        +fetch_new_endpoints()
    }

    class UnifiedProxyManager {
        -providers: List[BaseProxyProvider]
        -circuit_breaker: CircuitBreaker
        +lease_proxy() ProxyEndpoint
        +release_proxy(endpoint, result)
    }

    BaseProxyProvider <|-- ThorDataProxyProvider
    BaseProxyProvider <|-- FileProxyProvider
    BaseProxyProvider <|-- RotatingApiProxyProvider
    UnifiedProxyManager o-- BaseProxyProvider
```

---

## 3. 핵심 기능 명세

### 3.1 다양한 프록시 포맷 자동 감지 및 파싱
`proxies.txt` 파일 입력 시 다음 4가지 표준 포맷을 자동 정규화합니다:
1. `host:port` (인증 없는 공개/로컬 프록시)
2. `host:port:username:password` (일반 유료 프록시 표준 포맷)
3. `username:password@host:port` (URL 인증 포맷)
4. `socks5://username:password@host:port` (SOCKS5 고속 프록시)

정규화 엔진:
```python
def normalize_proxy(raw_line: str, default_protocol: str = "http") -> str:
    raw_line = raw_line.strip()
    # protocol://user:pass@host:port 변환 로직
    ...
```

### 3.2 서킷 브레이커 & 쿨다운 매니저 (Circuit Breaker)
각 프록시 엔드포인트의 상태를 실시간으로 격리 관리합니다:

- **State 1: ALIVE**: 정상 통신 가능 상태.
- **State 2: COOLDOWN (429 Rate Limited)**: Discord 429 반환 시 `retry_after` 시간 동안 큐에서 임시 제외 후 자동 복구.
- **State 3: DEAD (Hard Failure)**: 연속 3회 타임아웃, SSL 에러, Connection Refused 발생 시 격리 큐로 이동.

```python
@dataclass
class ProxyStats:
    endpoint: str
    success_count: int = 0
    fail_count: int = 0
    last_429_timestamp: float = 0.0
    cooldown_seconds: float = 0.0
    is_active: bool = True
```

### 3.3 ThorData 세션 로테이션 풀링
ThorData 전용 모드에서는 `session_id`를 임의로 무한 생성하는 대신, 활성 비동기 워커 수에 맞춰 세션 풀(Session Pool)을 유지하여 과도한 세션 생성 핸드셰이크 오버헤드를 절감합니다.

---

## 4. 환경 변수 및 설정 파일 규격 (`config.yaml`)

소스 코드에 비밀번호를 절대 남기지 않도록 `config.yaml`과 `.env` 설정을 지원합니다:

```yaml
# config.yaml 예시
proxy:
  mode: "hybrid"  # options: "thordata", "file", "hybrid", "direct"
  
  thordata:
    enabled: true
    server: "${THORDATA_SERVER}"
    username: "${THORDATA_USERNAME}"
    password: "${THORDATA_PASSWORD}"
    rotate_interval_requests: 3
    
  file:
    enabled: true
    path: "proxies.txt"
    protocol: "http" # or "socks5"
    shuffle: true
    
  health_check:
    timeout_seconds: 5.0
    max_consecutive_fails: 3
    cooldown_on_429_seconds: 15.0
```

---

## 5. 보안 및 안전장치
1. **IP Leakage 방지**: 프록시 모드 활성화 시 프록시 연결이 실패했을 때 로컬 실제 IP로 폴백(Fallback)되어 실제 주소가 Discord 서버에 노출되는 사태를 차단(`StrictProxyOnly=True`).
2. **DPAPI / 환경변수 연동**: 윈도우 환경에서 중요 자격 증명을 로컬 DPAPI 또는 환경변수로 안전하게 취합.
