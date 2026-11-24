<div align="center">

# ⚡ D4UC Google Apps Script (GAS) 24/7 无服务器检测器

> **无需保持电脑、手机或 Colab 开启！** 基于 Google Cloud 云端时间驱动触发器（Time-driven Triggers），实现 24 小时 365 天完全无人值守自动运行。

<br />

| [KR 한국어](../ko/gas/README.md) | [US English](../en/gas/README.md) | [JP 日本語](../ja/gas/README.md) | [CN 简体中文](../zh-CN/gas/README.md) | [ES Español](../es/gas/README.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/gas/README.md) | [DE Deutsch](../de/gas/README.md) | [RU Русский](../ru/gas/README.md) | [BR Português](../pt-BR/gas/README.md) | [SA العربية](../ar/gas/README.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/gas/README.md">HI हिन्दी</a> • <a href="../id/gas/README.md">ID Bahasa Indonesia</a></sub></p>

---


</div>

## 🚀 1 分钟快速上手指南

### 步骤 1: 创建 Google Apps Script 项目
1. 在浏览器中打开 [Google Apps Script 控制台](https://script.google.com/)。
2. 点击左上角的 **[+ 新建项目]**。
3. 将项目名称更改为 `D4UC 24/7 Checker`。

---

### 步骤 2: 复制代码并配置
1. 清空 `Code.gs` 并粘贴 [`gas/D4UC_Checker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_Checker.js) 的全部内容。
2. 修改 `CONFIG` 配置项并保存。

---

### 步骤 3: 一键初始化与 24 小时运行
1. 在函数下拉菜单中选择 **`initD4UCChecker`**。
2. 点击 **[运行]** 并授权 Google 权限。
3. 执行日志显示初始化成功后，程序会在云端持续运行。

---

## 📊 结果查看
- **Google Drive**: 结果自动保存在 `MyDrive/D4UC_Checker/` 目录中。
- **Google Sheets**: 自动生成 `D4UC_Tracker` 电子表格实时记录可用用户名。
- **Discord Webhook**: 发现稀有用户名时立即推送带有 `@here` 的通知消息。

---

## 🌐 多账号与分布式分片加速（单日 10 万 ~ 24 万次）
突破单账号每日 20,000 次限制，支持多账号无冲突分片:

1. 在其他 Google 账号中粘贴 [`gas/D4UC_MultiAccount_Worker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_MultiAccount_Worker.js)。
2. 设置 `WORKER_ID`（如 `0`, `1`, `2`, `3`）及 `TOTAL_WORKERS: 4`。
3. 配置相同的 Discord Webhook 即可实现单频道自动汇聚结果！

---

## 🛑 停止检测器
在函数列表中选择 **`stopD4UCChecker`** 并点击 **[运行]**，即可立即安全删除所有定时触发器。
