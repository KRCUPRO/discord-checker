# 01. 네트워크 코어 엔진 & WAF 우회 아키텍처 명세서
## (Network Core Engine & Anti-Bot WAF Evasion Specification)

> **문서 버전**: 1.0.0  
> **프로젝트**: Discord Username Checker V2 (Bug Bounty & Stealth Edition)  
> **대상 엔드포인트**: `https://discord.com/api/v9/unique-username/username-attempt-unauthed`

---

## 1. 개요 및 배경 (Problem Statement)

Discord는 2023년 Pomelo(태그 시스템 폐지 및 고유 사용자명 도입) 개편 이후, 사용자명 등록 및 조회 API에 강력한 Cloudflare WAF 및 레이트리밋(Rate Limit) 방어 기제를 적용했습니다.

기존 레거시 `main.py` 코드는 표준 파이썬 라이브러리인 `requests`와 `urllib3`를 사용합니다:
```python
# [레거시 취약 코드]
response = requests.post(
    API_URL,
    json=payload,
    headers=headers,
    proxies=proxy_dict,
    timeout=10,
    verify=False
)
```

이 구조는 다음과 같은 심각한 보안 및 탐지 취약점을 내포하고 있습니다:
1. **Python TLS Fingerprint 노출 (JA3/JA4 탐지)**:
   - 파이썬 `ssl` 모듈과 `urllib3`의 TLS Client Hello 시그니처는 Chrome/Safari 등 실제 브라우저와 암호화 스위트(Cipher Suites), 확장(Extensions), 타원 곡선(Elliptic Curves) 순서가 완전히 다릅니다.
   - Cloudflare WAF는 HTTP 헤더(`User-Agent: Mozilla/5.0...`)와 실제 전송 계층의 TLS 지문이 불일치하면 즉시 403 Forbidden(Turnstile 챌린지) 또는 비정상 429를 반환합니다.
2. **HTTP/1.1 vs HTTP/2 프로토콜 식별**:
   - 실제 디스코드 모바일 앱 및 웹 클라이언트는 HTTP/2 ALPN을 필수적으로 협상합니다. `requests`는 레거시 HTTP/1.1만 지원하므로 WAF의 우선 차단 대상이 됩니다.
3. **GIL(Global Interpreter Lock)로 인한 I/O 병목**:
   - `threading.Thread` 기반 동기 I/O 모델은 스레드 컨텍스트 스위칭 비용이 높고, 수십~수백 RPS 처리에 비효율적입니다.

---

## 2. 해결 방안: `curl_cffi` 기반 차세대 비동기 스텔스 엔진

### 2.1 TLS Impersonation (JA3/JA4 완벽 위장)
`curl_cffi`는 저수준 C 라이브러리인 `curl-impersonate`를 바인딩하여, TLS 계층의 Client Hello 바이트를 실제 브라우저와 100% 동일하게 모방합니다.

- **지원 브라우저 지문**: `chrome131`, `chrome124`, `safari17_0`, `android_chrome`
- **검증 효과**:
  - Cloudflare Bot Management 우회
  - TLS 핑거프린트 점수 0점 (완전 인간 클라이언트로 인식)
  - 불필요한 429 레이트리밋 유발 80% 이상 감소

### 2.2 비동기 이벤트 루프 (`asyncio` + `AsyncSession`)
```mermaid
sequenceDiagram
    autonumber
    participant W as Async Worker Pool
    participant C as curl_cffi AsyncSession
    participant P as Proxy Manager
    participant D as Discord API Gateway

    W->>P: 가용 프록시 대여 요청
    P-->>W: 최적 프록시 반환 (ThorData / SOCKS5)
    W->>C: POST /username-attempt-unauthed (Impersonate: chrome131)
    C->>D: TLS Handshake (HTTP/2 + JA4 브라우저 일치)
    D-->>C: 200 OK (taken: true/false) or 429 RateLimit
    alt 200 OK
        C-->>W: 정상 판정 (Available / Taken)
    else 429 RateLimit
        C-->>W: retry_after 헤더 파싱 후 지능형 백오프 & 프록시 회전
    end
```

---

## 3. 핵심 아키텍처 상세 설계

### 3.1 HTTP 헤더 및 Super Properties 정렬
디스코드 API는 단순 User-Agent 외에도 특정 클라이언트 메타데이터 헤더의 정합성을 검증합니다:

```python
STANDARD_DISCORD_HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Content-Type": "application/json",
    "Origin": "https://discord.com",
    "Referer": "https://discord.com/register",
    "Sec-Ch-Ua": '"Chromium";v="131", "Not_A Brand";v="24", "Google Chrome";v="131"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "X-Discord-Locale": "ko",
    "X-Discord-Timezone": "Asia/Seoul",
}
```

### 3.2 응답 상태 코드 처리 매트릭스

| HTTP Status | 응답 본문 / 조건 | 판정 결과 | 엔진 동작 |
| :--- | :--- | :--- | :--- |
| **200 OK** | `{"taken": false}` | **Available (사용 가능)** | DB 저장 및 Discord Webhook 즉시 전송 |
| **200 OK** | `{"taken": true}` | **Taken (사용 중)** | DB 기록 후 다음 타깃 탐색 |
| **400 Bad Request** | `{"code": 50035}` | **Invalid / Reserved** | 금지 문자, 예약어, 연속 점 예외 처리 |
| **429 Too Many Requests**| `{"retry_after": float}` | **Rate Limit** | 해당 프록시 쿨다운 등록 및 세션 즉시 교체 |
| **403 Forbidden** | Cloudflare Challenge HTML | **WAF Ban** | 프록시 블랙리스트 등록 및 브라우저 프로필 전환 |
| **5xx Server Error** | Gateway Timeout / Bad Gateway | **Transient Error** | 0.5초 백오프 후 다른 프록시로 재시도 |

### 3.3 지능형 백오프(Exponential Backoff with Jitter)
Rate Limit 발생 시 `retry_after` 헤더를 읽어 정확한 대기 시간을 산출하며, 추가 지터(0.1~0.3초)를 부여하여 동시 재시도로 인한 연쇄 차단을 방지합니다:

$$T_{\text{wait}} = \text{retry\_after} + \text{uniform}(0.1, 0.3)$$

---

## 4. 모듈 인터페이스 규격

```python
class StealthNetworkEngine:
    def __init__(self, proxy_pool: ProxyPool, impersonate: str = "chrome131"):
        ...
        
    async def check_username(self, username: str) -> CheckResult:
        """
        비동기 세션을 통해 Discord 사용자명 존재 여부를 안전하게 검사합니다.
        Returns:
            CheckResult(status=CheckStatus.AVAILABLE, username=username, latency_ms=124.5)
        """
        ...
```
