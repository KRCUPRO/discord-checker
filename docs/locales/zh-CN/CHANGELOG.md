<div align="center">

# 📋 更新日志 (Changelog)

> **D4UC (discord-checker) 项目全版本重大更新、架构优化与修复记录**

<br />

| [KR 한국어](../ko/CHANGELOG.md) | [US English](../en/CHANGELOG.md) | [JP 日本語](../ja/CHANGELOG.md) | [CN 简体中文](./CHANGELOG.md) | [ES Español](../es/CHANGELOG.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/CHANGELOG.md) | [DE Deutsch](../de/CHANGELOG.md) | [RU Русский](../ru/CHANGELOG.md) | [BR Português](../pt-BR/CHANGELOG.md) | [SA العربية](../ar/CHANGELOG.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/CHANGELOG.md">HI हिन्दी</a> • <a href="../id/CHANGELOG.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 2026年11月19日](../../assets/badges/update_badge_zh.svg)](./CHANGELOG.md)
[![Latest Release](https://img.shields.io/badge/Release-v12.5.0-blue.svg)](https://github.com/KRCUPRO/discord-checker/releases)

</div>

---

<a id="目录"></a>
## 📑 目录
1. [[v12.5.0] — 2026-11-19](#-v1250-2026-11-19)
1. [[v12.4.0] — 2026-11-19](#-v1240-2026-11-19)
1. [[v12.3.0] — 2026-11-19](#-v1230-2026-11-19)
1. [[v12.2.0] — 2026-11-19](#-v1220-2026-11-19)
1. [[v12.0.0] — 2026-11-18](#-v1200-2026-11-18)

---

> 本文件记录 D4UC 所有正式发布版本的核心功能新增、架构改进与故障修复细节。

---

<a id="-v1250-2026-11-19"></a>
## [v12.5.0] — 2026-11-19

### Added
- **12 国语言 1:1 完整官方文档套件 (`docs/locales/<lang>/`)**: 将 8 大核心文档（README、ARCHITECTURE_MAP、GUIDE、TASKS、CHANGELOG、LICENSE、NOTICE、SECURITY）全量翻译并部署至 12 种语言（中文简体、韩语、英语、日语、西班牙语、法语、德语、俄语、葡萄牙语、阿拉伯语、印地语、印尼语）。
- **GitHub 仓库根目录优化与模块化**: 将内部运维脚本归档至 `deploy/scripts/`，移除冗余文件，使根目录精简为 6 文件夹 + 8 文件，确保访客第一眼即可浏览项目介绍与界面预览。
- **首屏快速跳转导航栏**: 在徽章栏下方新增一键锚点栏 [ 概览 | 界面预览 | 快速启动 | 系统架构 | 平台指南 | 许可协议 ]。

### Changed
- 在所有文档顶部同步 5×2 规格的对称多语言选择器与实时 SVG 更新徽章（`2026年11月19日`）。

[⬆️ 返回目录顶部](#目录)

---

<a id="-v1240-2026-11-19"></a>
## [v12.4.0] — 2026-11-19

### Added
- **双向文档导航系统**: 全仓库 26 个 Markdown 文档均配备交互式目录与返回目录顶部链接。
- **13 种操作系统专属指南 (`docs/guides/`)**: 覆盖 Windows、macOS、Linux、Android APK、iOS PWA、Docker Compose 等全环境。

[⬆️ 返回目录顶部](#目录)

---

<a id="-v1230-2026-11-19"></a>
## [v12.3.0] — 2026-11-19

### Added
- **免费公开代理自动抓取与验证引擎**: 18 个公开源实时抓取、Cloudflare WAF 验证、15 秒 429 冷却队列。
- **已签名的独立 Android APK**: 经过 v1/v2/v3 完整数字签名的安装包及电池优化白名单配置教程。

[⬆️ 返回目录顶部](#目录)

---

<a id="-v1220-2026-11-19"></a>
## [v12.2.0] — 2026-11-19

### Added
- **移动端触控 Web GUI 与 PWA 引擎**: 5000 端口响应式触摸界面、0.1 秒 Discord Webhook 实时推送。

[⬆️ 返回目录顶部](#目录)

---

<a id="-v1200-2026-11-18"></a>
## [v12.0.0] — 2026-11-18

### Added
- **跨平台正式生产版本发布**: 4 种独立 Windows EXE、八大候选用户名生成引擎、Chrome 131 TLS 隐形网络栈。

[⬆️ 返回目录顶部](#目录)

