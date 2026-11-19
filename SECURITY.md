# 🛡️ Security Policy

| [KR 한국어](./docs/locales/ko/SECURITY.md) | [US English](./SECURITY.md) | [JP 日本語](./docs/locales/ja/SECURITY.md) | [CN 简体中文](./docs/locales/zh-CN/SECURITY.md) | [ES Español](./docs/locales/es/SECURITY.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](./docs/locales/fr/SECURITY.md) | [DE Deutsch](./docs/locales/de/SECURITY.md) | [RU Русский](./docs/locales/ru/SECURITY.md) | [BR Português](./docs/locales/pt-BR/SECURITY.md) | [SA العربية](./docs/locales/ar/SECURITY.md) |

<p align="center"><sub>🌐 Also available: <a href="./docs/locales/hi/SECURITY.md">HI हिन्दी</a> • <a href="./docs/locales/id/SECURITY.md">ID Bahasa Indonesia</a></sub></p>

## Responsible Usage & Secret Protection

### 1. Credentials & Private Keys Protection
- **Never commit `config.yaml`, `.env`, `surfshark_credentials.json`, or `*.conf`** to version control.
- This repository includes a hardened `.gitignore` to block local credentials, runtime databases (`*.db*`), scraped result files (`available*.txt`, `taken*.txt`, `results/`), and compiled binaries (`*.exe`).
- Always start from `config/.env.example`, `config/config.example.yaml`, and `data/surfshark_credentials.example.json` templates.
- No proprietary credentials or environment-specific paths are hardcoded anywhere in source code or documentation.

### 2. Network Isolation & Rate-Limiting Safety
- Requests utilize `curl_cffi` TLS impersonation routed through isolated user-space HTTP/SOCKS5 tunnels (`wireproxy`), keeping host OS traffic and DNS completely unaffected.
- Avoid excessive worker concurrency without adequate multi-cluster tunnel distribution.

### 3. Reporting a Security Issue
If you discover a security vulnerability or accidental secret exposure, please open a private security advisory in GitHub Security or contact the repository owner (`KRCUPRO`) directly.
