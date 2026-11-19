<div align="center">

# 🛡️ 보안 정책 (Security Policy)

> **D4UC 보안 가이드라인, 시크릿 보호 수칙 및 취약점 제보 정책**

<br />

| [KR 한국어](./SECURITY.md) | [US English](../en/SECURITY.md) | [JP 日本語](../ja/SECURITY.md) | [CN 简体中文](../zh-CN/SECURITY.md) | [ES Español](../es/SECURITY.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/SECURITY.md) | [DE Deutsch](../de/SECURITY.md) | [RU Русский](../ru/SECURITY.md) | [BR Português](../pt-BR/SECURITY.md) | [SA العربية](../ar/SECURITY.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/SECURITY.md">HI हिन्दी</a> • <a href="../id/SECURITY.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 2026년 11월 19일](../../assets/badges/update_badge.svg)](./CHANGELOG.md)
[![Security Policy: Active](https://img.shields.io/badge/Security-Policy%20Active-brightgreen.svg)](https://github.com/KRCUPRO/discord-checker/security)

</div>

---

<a id="목차"></a>
## 📑 목차
1. [1. 자격 증명 및 프라이빗 키 보호 수칙](#-1-자격-증명-및-프라이빗-키-보호-수칙)
1. [2. 네트워크 격리 및 Rate-Limit 안전성](#-2-네트워크-격리-및-rate-limit-안전성)
1. [3. 보안 취약점 제보 (Reporting a Security Issue)](#-3-보안-취약점-제보-reporting-a-security-issue)
1. [4. 책임 있는 연구 및 보안 정책 준수](#-4-책임-있는-연구-및-보안-정책-준수)

---

<a id="-1-자격-증명-및-프라이빗-키-보호-수칙"></a>
## 1. 자격 증명 및 프라이빗 키 보호 수칙

- **`config.yaml`, `.env`, `surfshark_credentials.json`, `*.conf`는 절대 버전 관리(Git)에 커밋하지 마십시오.**
- 본 저장소는 로컬 자격 증명, 런타임 데이터베이스(`*.db*`), 탐색 결과 파일(`available*.txt`, `taken*.txt`, `results/`), 빌드 바이너리(`*.exe`, `*.apk`)를 원천 차단하는 강화된 `.gitignore`를 포함합니다.
- 항상 `config/.env.example`, `config/config.example.yaml`, `data/surfshark_credentials.example.json` 템플릿을 복사하여 사용하십시오.
- 소스 코드 및 문서 어디에도 실제 비밀번호, WireGuard 개인키, 사용자 토큰이 하드코딩되어 있지 않습니다.

[⬆️ 목차 맨 위로 이동](#목차)

---

<a id="-2-네트워크-격리-및-rate-limit-안전성"></a>
## 2. 네트워크 격리 및 Rate-Limit 안전성

- 모든 HTTP 요청은 `curl_cffi` 기반 Chrome 131 TLS 스텔스 위장을 거치며, 유저스페이스 HTTP/SOCKS5 격리 터널(`wireproxy`)을 통해 라우팅됩니다.
- 호스트 OS의 기본 네트워크 어댑터, 라우팅 테이블, DNS 설정은 일절 변경되지 않습니다.
- 429 감지 시 즉시 0.3초 원자적 핫스왑(Hot-Swap)을 수행하여 단일 IP에 과도한 트래픽이 집중되지 않도록 보호합니다.

[⬆️ 목차 맨 위로 이동](#목차)

---

<a id="-3-보안-취약점-제보-reporting-a-security-issue"></a>
## 3. 보안 취약점 제보 (Reporting a Security Issue)

- 보안 취약점이나 의도치 않은 시크릿 노출을 발견하신 경우, 공개 이슈를 생성하지 마시고 GitHub의 **Private Security Advisory**를 통해 비공개 제보해 주시기 바랍니다.
- 또는 프로젝트 관리자(`KRCUPRO`)에게 직접 연락 주시면 24시간 이내에 분석 및 패치 릴리스를 진행합니다.

[⬆️ 목차 맨 위로 이동](#목차)

---

<a id="-4-책임-있는-연구-및-보안-정책-준수"></a>
## 4. 책임 있는 연구 및 보안 정책 준수

- 본 프로그램은 프로그래밍, TLS 지문 분석, 비동기 프록시 풀 관리, 네트워크 엔지니어링 학습 목적으로 개발되었습니다.
- 서비스 거부(DoS/DDoS) 공격이나 타인의 권리를 침해하는 용도로의 사용을 엄격히 금지합니다.

[⬆️ 목차 맨 위로 이동](#목차)

