<div align="center">

# 🛡️ Security Policy

> **D4UC Security Guidelines, Secret Protection Rules, and Responsible Disclosure**

<br />

| [KR 한국어](../ko/SECURITY.md) | [US English](./SECURITY.md) | [JP 日本語](../ja/SECURITY.md) | [CN 简体中文](../zh-CN/SECURITY.md) | [ES Español](../es/SECURITY.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/SECURITY.md) | [DE Deutsch](../de/SECURITY.md) | [RU Русский](../ru/SECURITY.md) | [BR Português](../pt-BR/SECURITY.md) | [SA العربية](../ar/SECURITY.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/SECURITY.md">HI हिन्दी</a> • <a href="../id/SECURITY.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: Nov 19, 2026](../../assets/badges/update_badge_en.svg)](./CHANGELOG.md)
[![Security Policy: Active](https://img.shields.io/badge/Security-Policy%20Active-brightgreen.svg)](https://github.com/KRCUPRO/discord-checker/security)

</div>

---

<a id="-table-of-contents"></a>
## 📑 Table of Contents
1. [1. Credentials & Private Keys Protection](#-1-credentials--private-keys-protection)
1. [2. Network Isolation & Rate-Limit Safety](#-2-network-isolation--rate-limit-safety)
1. [3. Reporting a Security Issue](#-3-reporting-a-security-issue)
1. [4. Responsible Research & Ethics](#-4-responsible-research--ethics)

---

<a id="-1-credentials--private-keys-protection"></a>
## 1. Credentials & Private Keys Protection

- **Never commit `config.yaml`, `.env`, `surfshark_credentials.json`, or `*.conf` to version control.**
- This repository includes a hardened `.gitignore` preventing accidental commits of local credentials, runtime databases (`*.db*`), scraped result files (`available*.txt`, `taken*.txt`, `results/`), and compiled binaries (`*.exe`, `*.apk`).
- Always copy and configure from provided templates: `config/.env.example`, `config/config.example.yaml`, and `data/surfshark_credentials.example.json`.
- Zero proprietary credentials, WireGuard private keys, or personal tokens are hardcoded in source code or documentation.

[⬆️ Return to Top](#-table-of-contents)

---

<a id="-2-network-isolation--rate-limit-safety"></a>
## 2. Network Isolation & Rate-Limit Safety

- All HTTP requests utilize `curl_cffi` Chrome 131 TLS stealth impersonation routed through isolated user-space HTTP/SOCKS5 tunnels (`wireproxy`).
- Host OS default network interfaces, system routing tables, and DNS configurations remain 100% untouched.
- When Discord returns HTTP 429, atomic hot-swap rotates to a fresh multi-tunnel node in under 0.3s, preventing request concentration on a single IP.

[⬆️ Return to Top](#-table-of-contents)

---

<a id="-3-reporting-a-security-issue"></a>
## 3. Reporting a Security Issue

- If you discover a security vulnerability or accidental credential exposure, please do NOT open a public GitHub issue.
- Instead, submit a report via GitHub **Private Security Advisory** or contact the repository owner (`KRCUPRO`) directly. Verified reports receive a patch within 24 hours.

[⬆️ Return to Top](#-table-of-contents)

---

<a id="-4-responsible-research--ethics"></a>
## 4. Responsible Research & Ethics

- D4UC is designed strictly for educational research into TLS fingerprinting, asynchronous proxy orchestration, and high-concurrency network architectures.
- DoS/DDoS attacks, credential stuffing, and unauthorized commercial exploitation are strictly prohibited.

[⬆️ Return to Top](#-table-of-contents)

