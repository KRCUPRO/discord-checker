<div align="center">

# ⚡ D4UC Google Apps Script (GAS) 24/7 サーバーレスチェッカー

> **PCやスマホを開いておく必要なし！** Google Cloudインフラ上で時間駆動トリガー（Time-driven Triggers）により24時間365日完全無人稼働するDiscordユーザー名チェッカーです。

<br />

| [KR 한국어](../ko/gas/README.md) | [US English](../en/gas/README.md) | [JP 日本語](../ja/gas/README.md) | [CN 简体中文](../zh-CN/gas/README.md) | [ES Español](../es/gas/README.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/gas/README.md) | [DE Deutsch](../de/gas/README.md) | [RU Русский](../ru/gas/README.md) | [BR Português](../pt-BR/gas/README.md) | [SA العربية](../ar/gas/README.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/gas/README.md">HI हिन्दी</a> • <a href="../id/gas/README.md">ID Bahasa Indonesia</a></sub></p>

---


</div>

## 🚀 1分クイックスタートガイド

### ステップ 1: Google Apps Script プロジェクト作成
1. ブラウザで [Google Apps Script ダッシュボード](https://script.google.com/) にアクセスします。
2. 左上の **[+ 新しいプロジェクト]** をクリックします。
3. プロジェクト名を `D4UC 24/7 Checker` に変更します。

---

### ステップ 2: コードの貼り付けと設定
1. `Code.gs` の内容を全消去し、[`gas/D4UC_Checker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_Checker.js) の全内容を貼り付けます。
2. `CONFIG` ブロックを設定します:
```javascript
const CONFIG = {
  EXECUTION_MODE: 'STANDALONE',
  TRIGGER_MODE: 'BALANCED',
  SHARDING_MODE: 'SINGLE',
  USERNAME_LENGTH: 4,
  ENABLE_SPREADSHEET: true,
  DISCORD_WEBHOOK_URL: 'https://discord.com/api/webhooks/...'
};
```
3. 保存アイコン（または Ctrl+S）をクリックします。

---

### ステップ 3: 24時間無人ランナーの初期化
1. 関数ドロップダウンから **`initD4UCChecker`** を選択します。
2. **[実行]** をクリックします。
3. Google権限承認プロンプトを許可します。
4. 実行ログに完了メッセージが表示されたら、端末の電源を切っても24時間自動で稼働し続けます。

---

## 📊 結果の確認方法
- **Google Drive**: `MyDrive/D4UC_Checker/` に結果と状態が自動保存されます。
- **Google Sheets**: `D4UC_Tracker` スプレッドシートにリアルタイム記録されます。
- **Discord Webhook**: 有効なユーザー名発見時に即座に通知が届きます。

---

## 🌐 マルチアカウント分散シャーディング（1日10万〜24万回高速化）
Googleアカウントの1日20,000回制限を超えて高速探索を行う場合、複数アカウントによる分散シャーディングをご利用いただけます:

1. 2つ目以降のGoogleアカウントで [`gas/D4UC_MultiAccount_Worker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_MultiAccount_Worker.js) を開きます。
2. `WORKER_ID`（例: `0`, `1`, `2`, `3`）と `TOTAL_WORKERS: 4` を設定します。
3. 同一の Discord Webhook URL を登録することで、1つのチャンネルに全アカウントの結果が集約されます。

---

## 🛑 チェッカーの停止方法
関数ドロップダウンで **`stopD4UCChecker`** を選択し、**[実行]** をクリックすると、すべてのトリガーが安全に削除されます。
