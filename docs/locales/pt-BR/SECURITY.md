<div align="center">

# 🛡️ Política de Segurança (Security Policy)

> **Diretrizes de Segurança D4UC, Proteção de Segredos e Divulgação Responsável**

<br />

| [KR 한국어](../ko/SECURITY.md) | [US English](../en/SECURITY.md) | [JP 日本語](../ja/SECURITY.md) | [CN 简体中文](../zh-CN/SECURITY.md) | [ES Español](../es/SECURITY.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/SECURITY.md) | [DE Deutsch](../de/SECURITY.md) | [RU Русский](../ru/SECURITY.md) | [BR Português](./SECURITY.md) | [SA العربية](../ar/SECURITY.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/SECURITY.md">HI हिन्दी</a> • <a href="../id/SECURITY.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 19 nov 2026](../../assets/badges/update_badge_pt.svg)](./CHANGELOG.md)
[![Security Policy: Active](https://img.shields.io/badge/Security-Policy%20Active-brightgreen.svg)](https://github.com/KRCUPRO/discord-checker/security)

</div>

---

<a id="-índice"></a>
## 📑 Índice
1. [1. Proteção de Credenciais e Chaves Privadas](#-1-proteção-de-credenciais-e-chaves-privadas)
1. [2. Isolamento de Rede e Segurança Contra Rate-Limit](#-2-isolamento-de-rede-e-segurança-contra-rate-limit)
1. [3. Notificação de Vulnerabilidades](#-3-notificação-de-vulnerabilidades)
1. [4. Pesquisa Ética e Uso Responsável](#-4-pesquisa-ética-e-uso-responsável)

---

<a id="-1-proteção-de-credenciais-e-chaves-privadas"></a>
## 1. Proteção de Credenciais e Chaves Privadas

- **Nunca envie `config.yaml`, `.env`, `surfshark_credentials.json` ou `*.conf` para o controle de versão (Git).**
- Este repositório inclui um `.gitignore` reforçado que bloqueia credenciais locais, bancos de dados em execução (`*.db*`), arquivos de resultados (`available*.txt`, `taken*.txt`, `results/`) e binários compilados (`*.exe`, `*.apk`).
- Configure seu ambiente copiando os modelos oficiais: `config/.env.example`, `config/config.example.yaml` e `data/surfshark_credentials.example.json`.
- Nenhum segredo ou chave privada está inserido de forma fixa no código-fonte ou na documentação.

[⬆️ Voltar ao Topo do Índice](#-índice)

---

<a id="-2-isolamento-de-rede-e-segurança-contra-rate-limit"></a>
## 2. Isolamento de Rede e Segurança Contra Rate-Limit

- Todas as requisições HTTP utilizam camuflagem TLS Chrome 131 (`curl_cffi`) roteadas por túneis isolados em espaço de usuário (`wireproxy`).
- As interfaces de rede do sistema operacional host, tabelas de roteamento e servidores DNS permanecem 100% inalterados.
- Ao identificar um código 429, o sistema efetua um hot-swap atômico em menos de 0,3s, garantindo rotação contínua e segura.

[⬆️ Voltar ao Topo do Índice](#-índice)

---

<a id="-3-notificação-de-vulnerabilidades"></a>
## 3. Notificação de Vulnerabilidades

- Ao encontrar falhas de segurança ou vazamento involuntário de credenciais, evite abrir problemas públicos.
- Envie um relatório sigiloso através do GitHub **Private Security Advisory** ou fale diretamente com o mantenedor (`KRCUPRO`). Resposta e correção em até 24 horas.

[⬆️ Voltar ao Topo do Índice](#-índice)

---

<a id="-4-pesquisa-ética-e-uso-responsável"></a>
## 4. Pesquisa Ética e Uso Responsável

- O D4UC é desenvolvido exclusivamente para estudo acadêmico de impressões digitais TLS, gestão de proxies assíncronos e arquiteturas concorrentes.
- É expressamente proibida sua utilização em ataques de negação de serviço (DoS/DDoS) ou em desacordo com termos de serviço de terceiros.

[⬆️ Voltar ao Topo do Índice](#-índice)

