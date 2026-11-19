<div align="center">

# 🛡️ 安全政策 (Security Policy)

> **D4UC 安全准则、密钥凭据保护规范与漏洞披露机制**

<br />

| [KR 한국어](../ko/SECURITY.md) | [US English](../en/SECURITY.md) | [JP 日本語](../ja/SECURITY.md) | [CN 简体中文](./SECURITY.md) | [ES Español](../es/SECURITY.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/SECURITY.md) | [DE Deutsch](../de/SECURITY.md) | [RU Русский](../ru/SECURITY.md) | [BR Português](../pt-BR/SECURITY.md) | [SA العربية](../ar/SECURITY.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/SECURITY.md">HI हिन्दी</a> • <a href="../id/SECURITY.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 2026年11月19日](../../assets/badges/update_badge_zh.svg)](./CHANGELOG.md)
[![Security Policy: Active](https://img.shields.io/badge/Security-Policy%20Active-brightgreen.svg)](https://github.com/KRCUPRO/discord-checker/security)

</div>

---

<a id="目录"></a>
## 📑 目录
1. [1. 凭据与私钥保护规范](#-1-凭据与私钥保护规范)
1. [2. 网络隔离与速率限制安全](#-2-网络隔离与速率限制安全)
1. [3. 安全漏洞报告 (Reporting a Security Issue)](#-3-安全漏洞报告-reporting-a-security-issue)
1. [4. 负责任的研究与合规守则](#-4-负责任的研究与合规守则)

---

<a id="-1-凭据与私钥保护规范"></a>
## 1. 凭据与私钥保护规范

- **切勿将 `config.yaml`、`.env`、`surfshark_credentials.json` 或 `*.conf` 提交到版本控制系统中。**
- 本仓库配备了经过严格加固的 `.gitignore`，可全面拦截本地凭据、运行时数据库（`*.db*`）、扫描结果文件（`available*.txt`、`taken*.txt`、`results/`）以及编译生成的二进制文件（`*.exe`、`*.apk`）。
- 请始终通过复制 `config/.env.example`、`config/config.example.yaml` 和 `data/surfshark_credentials.example.json` 模板来进行个性化配置。
- 源代码及官方文档中绝不包含任何硬编码的私钥、令牌或敏感路径。

[⬆️ 返回目录顶部](#目录)

---

<a id="-2-网络隔离与速率限制安全"></a>
## 2. 网络隔离与速率限制安全

- 所有 HTTP 请求均采用基于 `curl_cffi` 的 Chrome 131 TLS 隐形指纹伪装，并通过独立用户空间 HTTP/SOCKS5 隧道（`wireproxy`）进行路由转发。
- 宿主机操作系统的物理网卡、默认路由表与系统 DNS 设置均完全不受影响。
- 遭遇 429 限流时，系统将在 0.3 秒内自动完成原子热切换，防止单一 IP 遭受持续封禁。

[⬆️ 返回目录顶部](#目录)

---

<a id="-3-安全漏洞报告-reporting-a-security-issue"></a>
## 3. 安全漏洞报告 (Reporting a Security Issue)

- 若您发现潜在安全漏洞或凭据泄漏事件，请切勿通过公开 Issue 发布。
- 请直接通过 GitHub **Private Security Advisory** 提交私密报告，或直接联系项目维护者（`KRCUPRO`）。我们将在 24 小时内进行响应与修复。

[⬆️ 返回目录顶部](#目录)

---

<a id="-4-负责任的研究与合规守则"></a>
## 4. 负责任的研究与合规守则

- 本工具专为学习高并发网络编程、TLS JA3/JA4 模拟、多隧道代理池编排而设计。
- 严禁将其用于 DoS/DDoS 攻击或任何侵犯第三方服务条款的行为。

[⬆️ 返回目录顶部](#目录)

