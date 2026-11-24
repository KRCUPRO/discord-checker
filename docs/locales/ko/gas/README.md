<div align="center">

# ⚡ D4UC Google Apps Script (GAS) 24/7 서버리스 체커

> **PC, 스마트폰, Colab을 켜둘 필요 없이** Google 클라우드 인프라에서 시간 기반 예약 기능(Time-driven Triggers)으로 24시간 365일 무인 구동되는 닉네임 체커입니다.

<br />

| [KR 한국어](../ko/gas/README.md) | [US English](../en/gas/README.md) | [JP 日本語](../ja/gas/README.md) | [CN 简体中文](../zh-CN/gas/README.md) | [ES Español](../es/gas/README.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/gas/README.md) | [DE Deutsch](../de/gas/README.md) | [RU Русский](../ru/gas/README.md) | [BR Português](../pt-BR/gas/README.md) | [SA العربية](../ar/gas/README.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/gas/README.md">HI हिन्दी</a> • <a href="../id/gas/README.md">ID Bahasa Indonesia</a></sub></p>

---


</div>

## 🚀 1분 초고속 시작 가이드

### 1단계: Google Apps Script 프로젝트 생성
1. 브라우저에서 [Google Apps Script 대시보드](https://script.google.com/)에 접속합니다.
2. 좌측 상단의 **[+ 새 프로젝트]**를 클릭합니다.
3. 프로젝트 제목을 `D4UC 24/7 Checker`로 변경합니다.

---

### 2단계: 코드 복사 및 설정 입력
1. 기본 `Code.gs` 내용을 모두 지우고, [`gas/D4UC_Checker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_Checker.js) 전체 내용을 복사하여 붙여넣습니다.
2. 상단의 `CONFIG` 블록에서 원하는 옵션을 설정합니다:
```javascript
const CONFIG = {
  EXECUTION_MODE: 'STANDALONE', // 'STANDALONE' (단독) 또는 'HYBRID_WATCHDOG' (Colab 연동)
  TRIGGER_MODE: 'BALANCED',      // 'BALANCED' (5분 예정) 또는 'TURBO' (1분 초고속)
  SHARDING_MODE: 'SINGLE',       // 'SINGLE', 'INTERLEAVED', 'FEDERATED'
  USERNAME_LENGTH: 4,            // 탐색할 글자수 (3~6)
  ENABLE_SPREADSHEET: true,       // Google Sheets 실시간 대시보드 사용
  DISCORD_WEBHOOK_URL: 'https://discord.com/api/webhooks/...' // 알림받을 웹훅 URL
};
```
3. 상단 도구 모음의 **[저장 (💾)]** 버튼(또는 Ctrl+S)을 누릅니다.

---

### 3단계: 원클릭 초기화 및 24시간 자동 가동
1. 상단 함수 선택 드롭다운에서 **`initD4UCChecker`**를 선택합니다.
2. **[실행 (▶)]** 버튼을 클릭합니다.
3. 최초 실행 시 Google 권한 승인 창이 뜨면 **[권한 검토]** ➔ 계정 선택 ➔ **[고급]** ➔ **[이동 (안전하지 않음)]** ➔ **[허용]**을 순서대로 클릭합니다.
4. 실행 로그에 `🚀 [D4UC] 24시간 자동 체커 초기화 및 트리거 등록 완료`가 출력되면 이제 컴퓨터나 스마트폰을 끄셔도 24시간 자동으로 계속 작동합니다.

---

## 📊 결과 확인 방법
1. **Google Drive**: `MyDrive/D4UC_Checker/` 폴더가 자동 생성되며, `available_usernames.txt`에 유효 닉네임이 실시간 저장됩니다.
2. **Google Sheets**: `D4UC_Tracker` 시트에 모든 행이 자동 기록되어 모바일에서도 실시간 조회 가능합니다.
3. **Discord Webhook**: 유효 닉네임 발견 시 초록색 임베드와 `@here` 알림이 즉시 스마트폰으로 전송됩니다.

---

## 🌐 다중 계정 및 다중 프로젝트 가속 가이드 (일일 10만~24만 회 초고속)
구글 계정의 일일 호출 한도(20,000회)를 넘어 **일일 10만~24만 회 이상 초고속 전수 탐색**을 원할 경우 다중 계정 분산 샤딩을 활용할 수 있습니다:

### 방식 A: 단일 계정 내 다중 프로젝트 시차 가동 (Interleaved)
1. 동일한 구글 계정에서 `D4UC Checker - Node B`를 추가 생성합니다.
2. `CONFIG.SHARDING_MODE = 'INTERLEAVED'`로 설정 후 `initD4UCChecker`를 실행합니다.

### 방식 B: 다중 구글 계정 연합 무충돌 샤딩 (Federated Multi-Account)
1. 2번째, 3번째 구글 계정의 [Google Apps Script](https://script.google.com/)에 접속합니다.
2. [`gas/D4UC_MultiAccount_Worker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_MultiAccount_Worker.js) 코드를 복사하여 붙여넣습니다.
3. 각 계정별로 `WORKER_ID`를 지정합니다 (예: 4개 계정: 계정1=`0`, 계정2=`1`, 계정3=`2`, 계정4=`3`, `TOTAL_WORKERS: 4`).
4. 모든 계정에 **동일한 Discord Webhook URL**을 입력하면 가용 닉네임이 단일 디스코드 채널로 실시간 자동 취합됩니다!
5. (선택사항) 중앙 종합 모니터링이 필요할 경우 [`gas/D4UC_Master_Dashboard.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_Master_Dashboard.js)를 가동합니다.

---

## 🛑 체커 중지 방법
중단하고 싶을 때는 함수 드롭다운에서 **`stopD4UCChecker`**를 선택하고 **[실행]**을 누르면 모든 예약 트리거가 즉시 안전하게 삭제됩니다.
