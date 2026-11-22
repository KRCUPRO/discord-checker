# ☁️ D4UC Google Apps Script (GAS) 24/7 Serverless Checker

> **PC, 스마트폰, Colab을 전혀 켜둘 필요 없이** Google 클라우드 인프라에서 시간 기반 예약 기능(Time-driven Triggers)으로 24시간 365일 무인 구동되는 닉네임 체커입니다.

---

## 🚀 1분 초고속 시작 가이드 (Quick Start)

### 1단계: Google Apps Script 프로젝트 생성
1. 브라우저에서 [Google Apps Script 대시보드](https://script.google.com/)에 접속합니다.
2. 좌측 상단의 **[+ 새 프로젝트]**를 클릭합니다.
3. 프로젝트 제목을 `D4UC 24/7 Checker`로 변경합니다.

### 2단계: 코드 복사 및 설정 입력
1. 기본 `Code.gs` 내용을 모두 지우고, [`gas/D4UC_Checker.js`](./D4UC_Checker.js) 전체 내용을 복사하여 붙여넣습니다.
2. 상단의 `CONFIG` 블록에서 원하는 옵션을 설정합니다:
   ```javascript
   const CONFIG = {
     EXECUTION_MODE: 'STANDALONE', // 'STANDALONE' (단독) 또는 'HYBRID_WATCHDOG' (Colab 연동)
     TRIGGER_MODE: 'BALANCED',      // 'BALANCED' (5분 안정) 또는 'TURBO' (1분 초고속)
     USERNAME_LENGTH: 4,            // 탐색할 글자수 (3~6)
     ENABLE_SPREADSHEET: true,       // Google Sheets 실시간 대시보드 사용
     DISCORD_WEBHOOK_URL: 'https://discord.com/api/webhooks/...' // 알림받을 웹훅 URL
   };
   ```
3. 상단 도구 모음의 **[저장 (💾)]** 버튼(또는 Ctrl+S)을 누릅니다.

### 3단계: 원클릭 초기화 및 24시간 자동 가동
1. 상단 함수 선택 드롭다운에서 **`initD4UCChecker`**를 선택합니다.
2. **[실행 (▶)]** 버튼을 클릭합니다.
3. 최초 실행 시 Google 권한 승인 창이 뜨면 **[권한 검토]** ➔ 계정 선택 ➔ **[고급]** ➔ **[이동 (안전하지 않음)]** ➔ **[허용]**을 순서대로 클릭합니다.
4. 실행 로그에 `✅ [D4UC] 24시간 자동 체커 초기화 및 트리거 등록이 완료되었습니다!`가 출력되면 이제 컴퓨터를 끄셔도 24시간 자동으로 계속 작동합니다!

---

## 📊 결과 확인 방법

1. **Google Drive**:
   - `MyDrive/D4UC_Checker/` 폴더가 자동 생성됩니다.
   - `available_usernames.txt`: 발견된 사용 가능한 닉네임이 실시간 저장됩니다.
   - `checker_state.json`: 현재 검사 커서와 누적 통계가 기록됩니다.
2. **Google Sheets (대시보드)**:
   - `D4UC_Tracker` 스프레드시트가 자동 생성되며, 가용 닉네임이 발견될 때마다 새로운 행이 즉시 추가됩니다.
   - 모바일 Google Sheets 앱에서 실시간으로 알림과 함께 확인 가능합니다.
3. **Discord Webhook**:
   - 닉네임 발견 시 초록색 임베드와 함께 `@here` 알림이 즉시 날아옵니다.

---

## 🛑 체커 정지 방법
- 중단하고 싶을 때는 함수 드롭다운에서 **`stopD4UCChecker`**를 선택하고 **[실행]**을 누르면 모든 예약 트리거가 즉시 안전하게 삭제됩니다.
