<div align="center">

# 📖 Guia Mestre do Projeto D4UC (GUIDE.md)

> **Motor de Alta Performance para Verificação de Nomes Raros no Discord baseado em Camuflagem TLS Chrome 131, Pool de Túneis Surfshark 1:1 e SQLite WAL**

<br />

| [KR 한국어](../ko/GUIDE.md) | [US English](../en/GUIDE.md) | [JP 日本語](../ja/GUIDE.md) | [CN 简体中文](../zh-CN/GUIDE.md) | [ES Español](../es/GUIDE.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/GUIDE.md) | [DE Deutsch](../de/GUIDE.md) | [RU Русский](../ru/GUIDE.md) | [BR Português](./GUIDE.md) | [SA العربية](../ar/GUIDE.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/GUIDE.md">HI हिन्दी</a> • <a href="../id/GUIDE.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 19 nov 2026](../../assets/badges/update_badge_pt.svg)](./CHANGELOG.md)
[![Guide Version](https://img.shields.io/badge/Guide-v12.5.0-blue.svg)](./GUIDE.md)

</div>

---

<a id="-índice"></a>
## 📑 Índice
1. [1. Visão Geral do Projeto & Arquitetura Central](#-1-visão-geral-do-projeto--arquitetura-central)
2. [2. Manuais Específicos por Sistema Operacional](#-2-manuais-específicos-por-sistema-operacional)
3. [3. Início Rápido por Ambiente Principal](#-3-início-rápido-por-ambiente-principal)
4. [4. 8 Modos de Geração de Nomes de Usuário](#-4-8-modos-de-geração-de-nomes-de-usuário)
5. [5. Infraestrutura de Proxies & Túneis Internacionais](#-5-infraestrutura-de-proxies--túneis-internacionais)
6. [6. Sharding Multi-Janelas e Multi-Contêineres](#-6-sharding-multi-janelas-e-multi-contêineres)
7. [7. Regras de Segurança e Publicação Sem Vazamentos no GitHub](#-7-regras-de-segurança-e-publicação-sem-vazamentos-no-github)
8. [8. Estrutura do Código & Guia de Manutenção](#-8-estrutura-do-código--guia-de-manutenção)
9. [9. Notas de Rodapé & Referências Técnicas](#-9-notas-de-rodapé--referências-técnicas)

---

<a id="-1-visão-geral-do-projeto--arquitetura-central"></a>
## 1. 1. Visão Geral do Projeto & Arquitetura Central

- **Engine Target Endpoint**: `https://discord.com/api/v9/unique-username/username-attempt-unauthed`
- **Core Technological Invariants**:
  1. <a id="fnref-1"></a><a id="fnref1"></a>**Chrome 131 TLS JA3/JA4 Stealth Impersonation** (`curl_cffi`)[^1].
  2. <a id="fnref-2"></a><a id="fnref2"></a>**Surfshark 1:1 Isolated Multi-Tunnel Pool** (`wireproxy`)[^2].
  3. **0.3s Atomic 429 Hot-Swap**: Uninterrupted continuous scanning across alternate global countries.
  4. **Free Public Proxy Scraper & Live Multi-Threaded Validator** (`src/proxy/free_proxy.py`).
  5. **SQLite WAL Concurrency**: Multi-process safe state synchronization without database locks.

[⬆️ Voltar ao Topo do Índice](#-índice)

---

<a id="-2-manuais-específicos-por-sistema-operacional"></a>
## 2. 2. Manuais Específicos por Sistema Operacional

- 🪟 [Windows Guide (WINDOWS_GUIDE.md)](../../guides/WINDOWS_GUIDE.md): 4 Standalone EXEs, Windows Firewall, Task Scheduler 24/7.
- 🍏 [macOS Guide (MACOS_GUIDE.md)](../../guides/MACOS_GUIDE.md): Apple Silicon M1-M4 & Intel, Homebrew, `launchd` automation.
- 🐧 [Linux Guide (LINUX_GUIDE.md)](../../guides/LINUX_GUIDE.md): Ubuntu, Debian, systemd service, tmux/screen background execution.
- 🤖 [Android Guide (ANDROID_GUIDE.md)](../../guides/ANDROID_GUIDE.md): 1-Tap native APK, Wake Lock management, Termux PRoot.
- 📱 [iOS Guide (IOS_GUIDE.md)](../../guides/IOS_GUIDE.md): Safari PWA Home Screen App, 0.1s Discord Webhook push notifications.
- 🐳 [Docker Guide (DOCKER_GUIDE.md)](../../guides/DOCKER_GUIDE.md): Multi-Arch Docker Compose 2-shard acceleration.
- 🍓 [Raspberry Pi Guide (RASPBERRY_PI_GUIDE.md)](../../guides/RASPBERRY_PI_GUIDE.md): 3W low-power homelab 24/7 setup.
- 🧭 [Guides Hub (docs/guides/README.md)](../../guides/README.md) & [Docs Hub (docs/README.md)](../../README.md)

[⬆️ Voltar ao Topo do Índice](#-índice)

---

<a id="-3-início-rápido-por-ambiente-principal"></a>
## 3. 3. Início Rápido por Ambiente Principal

### A. Desktop GUI (Windows & macOS)
```bash
python src/gui_ko.py   # Korean GUI
python src/gui_en.py   # English GUI
```

### B. Mobile Touch Web GUI & PWA
```bash
python src/web_gui.py --port 5000
# Open http://<LOCAL_IP>:5000 on mobile browser or tap 'Add to Home Screen'
```

### C. Android 1-Tap Standalone APK
- Install `dist/DiscordUsernameChecker_v12.3.0.apk` directly on Android 8.0+.

### D. Headless Rich CLI (Linux / Server)
```bash
python src/run.py --mode hybrid --length 4 --workers 10 --proxy free
```

### E. Multi-Arch Docker Compose
```bash
docker compose -f deploy/docker-compose.yml up -d
```

[⬆️ Voltar ao Topo do Índice](#-índice)

---

<a id="-4-8-modos-de-geração-de-nomes-de-usuário"></a>
## 4. 4. 8 Modos de Geração de Nomes de Usuário

1. **Hybrid**: Combines dictionary bases, consonant-vowel combinations, and alphanumeric affixes.
2. **Permutation**: Pure combinatorial math engine (`[a-z0-9_.]^N`).
3. **Dictionary**: Real word frequency dictionary matching.
4. **Pattern**: Custom regex pattern matching (`a*b?`, `kr_*`).
5. **Numeric**: Consecutive and rare numerical combinations (`0001`~`9999`).
6. **Custom Mask**: Precise position-by-position character masking.
7. **Combinatorial**: User-defined prefix + base + suffix combinations.
8. **Recheck**: Scans previously verified or taken database history.

[⬆️ Voltar ao Topo do Índice](#-índice)

---

<a id="-5-infraestrutura-de-proxies--túneis-internacionais"></a>
## 5. 5. Infraestrutura de Proxies & Túneis Internacionais

- **Surfshark WireGuard Multi-Tunnel**: Maps 142 global server clusters to local ports `127.0.0.1:1081~1085`.
- **Free Public Proxy Scraper**: Aggregates from 18 verified open-source endpoints with Cloudflare trace pre-validation.
- **Tor & User Proxies**: SOCKS5 and HTTP proxy list rotation support.

[⬆️ Voltar ao Topo do Índice](#-índice)

---

<a id="-6-sharding-multi-janelas-e-multi-contêineres"></a>
## 6. 6. Sharding Multi-Janelas e Multi-Contêineres

Execute 2 to 4 parallel sharded instances with zero key collisions:
```bash
# Window 1 (Shard 1/2)
python src/run.py --mode permutation --shard 2_1 --length 4

# Window 2 (Shard 2/2)
python src/run.py --mode permutation --shard 2_2 --length 4
```

[⬆️ Voltar ao Topo do Índice](#-índice)

---

<a id="-7-regras-de-segurança-e-publicação-sem-vazamentos-no-github"></a>
## 7. 7. Regras de Segurança e Publicação Sem Vazamentos no GitHub

- Never commit `config.yaml`, `.env`, or `surfshark_credentials.json`.
- All credentials must be passed via environment variables or template files.
- Refer to [SECURITY.md](./SECURITY.md) for vulnerability reporting.

[⬆️ Voltar ao Topo do Índice](#-índice)

---

<a id="-8-estrutura-do-código--guia-de-manutenção"></a>
## 8. 8. Estrutura do Código & Guia de Manutenção

```text
src/
├── network/    # DiscordApiClient & Chrome 131 TLS handshake
├── proxy/      # UnifiedProxyManager, Surfshark, FreeProxyProvider
├── generator/  # 8 candidate generation algorithms
├── storage/    # SQLite WAL database & text mirrors
└── ui/         # Desktop CustomTkinter & Mobile Web GUI
```

[⬆️ Voltar ao Topo do Índice](#-índice)

---

<a id="-9-notas-de-rodapé--referências-técnicas"></a>
## 9. 9. Notas de Rodapé & Referências Técnicas

[^1]: <a id="fn-1"></a><a id="fn1"></a>O handshake BoringSSL do Chrome 131 neutraliza totalmente as defesas de fingerprinting TLS da Cloudflare. [↩️ Voltar à Referência](#fnref-1)
[^2]: <a id="fn-2"></a><a id="fn2"></a>wireproxy é um utilitário em Go que traduz WireGuard para proxies locais SOCKS5 sem requerer privilégios de root. [↩️ Voltar à Referência](#fnref-2)

[⬆️ Voltar ao Topo do Índice](#-índice)
