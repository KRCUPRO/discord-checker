<div align="center">

# ⚡ D4UC — Discord 4-Character Usernames Checker

[![Language](https://img.shields.io/badge/Language-10%20Languages%20Supported-58a6ff?style=for-the-badge&logo=google-translate)](./README.md)
[![Devices](https://img.shields.io/badge/Mobile-iPhone%20|%20iPad%20|%20Android%20|%20Tablet%20|%20PC-ff69b4?style=for-the-badge&logo=apple)](./docs/MOBILE_AND_IPHONE_GUIDE.md)
[![Cloud Execution](https://img.shields.io/badge/100%25%20Browser--Based-Google%20Colab%20|%20Apps%20Script%2024%2F7-blueviolet?style=for-the-badge&logo=google)](./docs/GAS_24H_CHECKER_GUIDE.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](./LICENSE)

---

### 🌐 Select Your Language / 언어 선택 / 言語を選択 / 选择语言 / Seleccionar idioma / Выберите язык / Choisir la langue / Sprache wählen / Selecionar idioma / Chọn ngôn ngữ

[ 🇰🇷 한국어 ](./README_ko.md) • [ 🇺🇸 English ](./README.md) • [ 🇯🇵 日本語 ](./README_ja.md) • [ 🇨🇳 简体中文 ](./README_zh.md) • [ 🇪🇸 Español ](./README_es.md) • [ 🇷🇺 Русский ](./README_ru.md) • [ 🇫🇷 Français ](./README_fr.md) • [ 🇩🇪 Deutsch ](./README_de.md) • [ 🇧🇷 Português ](./README_pt.md) • [ 🇻🇳 Tiếng Việt ](./README_vi.md)

---

</div>

## 📖 项目概述 (Overview)

**D4UC (Discord 4-Character Usernames Checker)** 是一款企业级高性能全自动用户名检查引擎，专为快速、安全地扫描并抢注 Discord 稀有独特用户名（3~6 字符）而设计。

系统不仅集成了 Chrome 131 TLS 指纹隐形伪装、Surfshark WireGuard 1:1 独立隧道代理、SQLite WAL 实时去重、全排列多窗口分片，更全面支持 **无需安装任何软件、支持苹果 iPhone、iPad、安卓手机、平板及电脑的 100% 浏览器全平台云端运行**（Google Colab Web GUI 与 Google Apps Script 24/7 无服务器全自动检查器）。

---

## 📱 苹果 iPhone、iPad、安卓与平板全机型通用 (Zero-Install 免安装)

> **“没有电脑？不想安装任何 APP？完全没有问题！”**  
> 只需在任何 iPhone、iPad、安卓手机或平板电脑上打开自带浏览器（Safari/Chrome），即可 1 分钟快速开启云端 24 小时检查。详细指南请参阅 [📱 移动端与 iPhone 专属使用指南](./docs/MOBILE_AND_IPHONE_GUIDE.md)。

1. **🍏 苹果 iOS (iPhone 与 iPad)**:
   - 无需越狱，无需额外安装应用，直接在系统自带的 **Safari 浏览器** 中运行 [Google Colab](./D4UC_Google_Colab.ipynb) 或配置 [Google Apps Script](./docs/GAS_24H_CHECKER_GUIDE.md)。
2. **🤖 安卓手机与平板电脑**:
   - 使用 Chrome 浏览器直接操控交互式 Web GUI，或配置 Google Apps Script 实现 24 小时后台自动巡航。
3. **🔋 0 电量消耗，手机关机依然 24 小时运行 (24/7 Cloud)**:
   - **Google Apps Script** 完全运行在谷歌云端服务器上。即使您将手机完全关机、开启飞行模式或电量耗尽，检查程序依然全天候 365 天无休运行。
4. **🔔 手机端即时消息推送**:
   - 一旦发现可用用户名，将立即向手机上的 **Discord APP** 发送带有一键抢注链接的绿色卡片提醒，并实时记录到手机 **Google 表格 APP** 中。

---

## 🚀 6 大跨平台运行环境深度对比

| 运行环境 | 支持设备 (Supported Devices) | 核心特点与架构用途 | 快速启动 / 链接 |
| :--- | :--- | :--- | :--- |
| **☁️ Google Apps Script** | 📱 **100% 全机型通用** (iPhone, iPad, 安卓, 平板, 电脑) | **关机断网照常运行**，谷歌云端 24/7/365 无服务器全自动巡检 | [GAS 24/7 指南](./docs/GAS_24H_CHECKER_GUIDE.md) |
| **⚡ Google Colab Web GUI** | 📱 **100% 全机型通用** (Safari, Chrome 等所有移动浏览器) | 单元格内直接呈现暗色交互式大屏，实时同步谷歌云端硬盘 | [`D4UC_Google_Colab.ipynb`](./D4UC_Google_Colab.ipynb) |
| **🖥️ Windows Desktop GUI** | 💻 Windows 电脑 (Win 10/11) | 赛博朋克深色主题 GUI，实时 KPI 卡片，全组件悬浮气泡提示 | `DiscordUsernameCheckerV2.exe` |
| **📱 Android Termux** | 🤖 仅限安卓系统 (无需 Root) | 手机后台 24 小时原生常驻运行 (基于 Debian proot 容器) | [Termux 指南](./docs/TERMUX_DEBIAN_GUIDE.md) |
| **🐳 Docker & Compose** | 🖥️ Linux / Mac / 服务器 / NAS | 支持 ARM64/AMD64 多架构服务器无感容器化部署 | `docker compose up -d` |
| **⚙️ Headless CLI** | 🖥️ Linux / Windows / 服务器 | 极速命令行高并发后台运行器 | `python run.py --mode Permutation` |

---

## 🌟 核心功能 (Key Features)

1. **Google Apps Script 24/7 无服务器自动化检查器 (`gas/`)**:
   - 时间驱动触发器，4.5 分钟自链接状态机突破 6 分钟超时限制。
   - 双重持久化存储：谷歌云盘文件 (`available_usernames.txt`) + 谷歌在线表格实时大屏 (`D4UC_Tracker`)。
2. **Google Colab 交互式 Web GUI (`colab_gui.py`)**:
   - 单元格内原生渲染精美暗色大屏，实时 KPI 监控与流式日志。
3. **10 国语言 1:1 完整匹配支持**: 196 个键位全量本地化映射。
4. **Surfshark WireGuard 1:1 独立多隧道代理**: 彻底免疫 Discord 429 频控封锁。
5. **Discord Webhook 实时通知**: 绿色 Embed 消息与 `@here` 提醒，一键跳转注册。

---

## 📄 开源许可证 (License)
本项目基于 [MIT License](./LICENSE) 开源。
