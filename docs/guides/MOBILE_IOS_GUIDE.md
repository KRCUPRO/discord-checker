# 📱 iOS & Mobile Environment Deployment Guide (MOBILE_IOS_GUIDE.md)

> **프로젝트**: D4UC (`discord-checker`)  
> **대상 플랫폼**: Apple iOS (iPhone / iPad), iPadOS, Mobile Remote Bridges  
> **최종 개정일**: 2026년 11월 19일  

---

## 🧭 1. iOS 샌드박스 보안 아키텍처 및 기술적 한계

iOS는 애플의 강력한 앱 샌드박스(App Sandbox) 보안 모델을 적용하고 있어, 데스크톱이나 안드로이드(Termux) 환경과 다른 기술적 제약이 존재합니다:

1. **JIT (Just-In-Time) 컴파일 및 네이티브 라이브러리 제약**:
   - `curl_cffi`는 BoringSSL C 라이브러리를 동적 링크하여 Chrome 131 JA3/JA4 지문을 에뮬레이트합니다.
   - iOS의 일반 앱(a-Shell 등)은 커스텀 C 바이너리의 동적 로딩 및 임의 네이티브 C 확장 실행에 엄격한 제한을 둡니다.
2. **유저스페이스 네트워크 어댑터(`wireproxy`) 소켓 권한**:
   - iOS에서는 루트 권한이나 VPN Network Extension 권한 없이 유저스페이스에서 WireGuard UDP 터널을 1:1로 다중 바인딩하는 것이 제한됩니다.
3. **iSH (x86 Linux 에뮬레이터) 성능 한계**:
   - iSH는 x86 명령어를 사용자 레벨에서 소프트웨어 에뮬레이션하므로, 대량의 비동기 동시성 네트워크 요청 시 심각한 CPU 병목과 지연이 발생합니다.

---

## 🚀 2. 실전 권장 아키텍처: 모바일 원격 제어 & 웹훅 브리지

현업 엔지니어가 모바일(아이폰/아이패드) 환경에서 D4UC를 24시간 가동하고 제어하는 **가장 안정적인 3대 실전 구성**입니다:

### 권장 구성 A: Discord Webhook 모바일 즉시 푸시 (가장 간편)
- D4UC 코어는 PC, 홈 서버, 또는 클라우드 VPS(Ubuntu/Debian)에서 백그라운드로 24시간 가동합니다.
- `.env`에 `D4UC_WEBHOOK`을 등록해두면 희귀 닉네임이 발견되는 즉시 **아이폰의 Discord 모바일 앱으로 0.1초 만에 푸시 알림**이 전송됩니다.

### 권장 구성 B: iOS SSH 터미널 클라이언트 연동 (Termius, Blink, Prompt)
1. 데스크톱 PC 또는 클라우드 서버에서 D4UC를 `tmux` 또는 `screen` 세션으로 실행합니다:
   ```bash
   tmux new -s d4uc
   python src/run.py --mode hybrid --length 4 --workers 5
   # Ctrl+B, D를 눌러 세션 분리(Detach)
   ```
2. 아이폰/아이패드에서 **Termius** 또는 **Blink Shell** 앱을 실행합니다.
3. SSH로 서버에 접속한 후 세션에 다시 연결합니다:
   ```bash
   tmux attach -t d4uc
   ```
4. 모바일 화면에서 실시간 Rich CLI 대시보드(RPS, 가용 닉네임, 워커 상태)를 완벽하게 모니터링하고 제어할 수 있습니다.

### 권장 구성 C: 안드로이드 기기 병행 사용 (Termux 완벽 지원)
- 안드로이드 환경에서는 [TERMUX_DEBIAN_GUIDE.md](./TERMUX_DEBIAN_GUIDE.md)를 참조하여 기기 자체에서 무제한 백그라운드 스캔이 가능합니다.

---

## 📋 요약 비교표

| 환경 | 설치 난이도 | 24시간 가동성 | 실시간 제어 | 권장도 |
| :--- | :---: | :---: | :---: | :---: |
| **iOS Discord Webhook** | 초급 (1분) | ⭐⭐⭐⭐⭐ (완벽) | 푸시 수신 | **최우선 권장** |
| **iOS SSH + tmux** | 중급 (5분) | ⭐⭐⭐⭐⭐ (완벽) | 실시간 양방향 제어 | **고급 사용자 권장** |
| **iOS a-Shell / iSH** | 고급 (난해) | ⭐ (백그라운드 킬) | 매우 느림 | 비권장 (테스트용) |
