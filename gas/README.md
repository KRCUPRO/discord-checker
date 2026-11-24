<div align="center">

# ⚡ D4UC Google Apps Script (GAS) 24/7 Serverless Checker

> **Zero-Install, 100% Autonomous 24/7/365 Cloud Checker.**
> Runs permanently on Google Cloud infrastructure via Time-driven Triggers without keeping your PC, smartphone, or Colab open.

<br />

| [KR 한국어](../docs/locales/ko/gas/README.md) | [US English](../docs/locales/en/gas/README.md) | [JP 日本語](../docs/locales/ja/gas/README.md) | [CN 简体中文](../docs/locales/zh-CN/gas/README.md) | [ES Español](../docs/locales/es/gas/README.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../docs/locales/fr/gas/README.md) | [DE Deutsch](../docs/locales/de/gas/README.md) | [RU Русский](../docs/locales/ru/gas/README.md) | [BR Português](../docs/locales/pt-BR/gas/README.md) | [SA العربية](../docs/locales/ar/gas/README.md) |

<p align="center"><sub>🌐 Also available: <a href="../docs/locales/hi/gas/README.md">HI हिन्दी</a> • <a href="../docs/locales/id/gas/README.md">ID Bahasa Indonesia</a></sub></p>

---


</div>

## 🚀 1-Minute Quick Start Guide

### Step 1: Create a Google Apps Script Project
1. Open [Google Apps Script Dashboard](https://script.google.com/) in your browser.
2. Click **[+ New project]** on the top-left.
3. Name the project `D4UC 24/7 Checker`.

---

### Step 2: Copy Code & Configure
1. Delete default code in `Code.gs` and paste the full contents of [`gas/D4UC_Checker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_Checker.js).
2. Update the `CONFIG` block as needed:
```javascript
const CONFIG = {
  EXECUTION_MODE: 'STANDALONE', // 'STANDALONE' or 'HYBRID_WATCHDOG' (Colab sync)
  TRIGGER_MODE: 'BALANCED',      // 'BALANCED' (5-min intervals) or 'TURBO' (1-min rapid)
  SHARDING_MODE: 'SINGLE',       // 'SINGLE', 'INTERLEAVED', or 'FEDERATED'
  USERNAME_LENGTH: 4,            // Target length (3-6 chars)
  ENABLE_SPREADSHEET: true,       // Real-time Google Sheets tracking
  DISCORD_WEBHOOK_URL: 'https://discord.com/api/webhooks/...' // Webhook URL for hits
};
```
3. Save by clicking the Save icon (or Ctrl+S).

---

### Step 3: Initialize 24/7 Autonomous Runner
1. Select **`initD4UCChecker`** in the function dropdown list.
2. Click **[Run]**.
3. When prompted, grant Google permissions (Review Permissions ➔ Select Account ➔ Advanced ➔ Go to D4UC 24/7 Checker (unsafe) ➔ Allow).
4. When `🚀 [D4UC] 24/7 Autonomous Checker initialized` appears in Execution log, it runs around the clock even when your device is turned off.

---

## 📊 Result Verification
- **Google Drive**: Stored in `MyDrive/D4UC_Checker/available_usernames.txt` and `checker_state_w0.json`.
- **Google Sheets**: Auto-created `D4UC_Tracker` spreadsheet logs valid hits in real-time.
- **Discord Webhook**: Sends instant green embed alerts with `@here` mention when rare usernames are discovered.

---

## 🌐 Multi-Account & Sharding Acceleration (100k~240k Checks/Day)
To exceed Google's 20,000 requests/day per-account limit, scale horizontally across multiple accounts or projects:

### Mode A: Single-Account Interleaved Projects
1. In the same account, create additional Apps Script projects.
2. Set `SHARDING_MODE: 'INTERLEAVED'` to alternate execution cycles across 24 hours.

### Mode B: Multi-Account Zero-Collision Federation
1. Log into your 2nd, 3rd, or Nth Google account.
2. Copy & paste [`gas/D4UC_MultiAccount_Worker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_MultiAccount_Worker.js).
3. Assign unique `WORKER_ID` (e.g. `0`, `1`, `2`, `3`) with `TOTAL_WORKERS: 4`.
4. Enter the **same Discord Webhook URL** in all workers to aggregate discoveries into a single channel!
5. (Optional) Run [`gas/D4UC_Master_Dashboard.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_Master_Dashboard.js) to view real-time fleet telemetry.

---

## 🛑 Stopping the Checker
Select **`stopD4UCChecker`** in the function dropdown and click **[Run]**. All scheduled triggers are safely removed immediately.
