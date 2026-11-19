<div align="center">

# 🛡️ セキュリティポリシー (Security Policy)

> **D4UC セキュリティガイドライン、シークレット保護規則および脆弱性報告方針**

<br />

| [KR 한국어](../ko/SECURITY.md) | [US English](../en/SECURITY.md) | [JP 日本語](./SECURITY.md) | [CN 简体中文](../zh-CN/SECURITY.md) | [ES Español](../es/SECURITY.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/SECURITY.md) | [DE Deutsch](../de/SECURITY.md) | [RU Русский](../ru/SECURITY.md) | [BR Português](../pt-BR/SECURITY.md) | [SA العربية](../ar/SECURITY.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/SECURITY.md">HI हिन्दी</a> • <a href="../id/SECURITY.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 2026年11月19日](../../assets/badges/update_badge_ja.svg)](./CHANGELOG.md)
[![Security Policy: Active](https://img.shields.io/badge/Security-Policy%20Active-brightgreen.svg)](https://github.com/KRCUPRO/discord-checker/security)

</div>

---

<a id="目次"></a>
## 📑 目次
1. [1. 認証情報および秘密鍵の保護規則](#-1-認証情報および秘密鍵の保護規則)
1. [2. ネットワーク分離とレート制限の安全性](#-2-ネットワーク分離とレート制限の安全性)
1. [3. セキュリティ脆弱性の報告 (Reporting a Security Issue)](#-3-セキュリティ脆弱性の報告-reporting-a-security-issue)
1. [4. 責任ある研究と倫理規定](#-4-責任ある研究と倫理規定)

---

<a id="-1-認証情報および秘密鍵の保護規則"></a>
## 1. 認証情報および秘密鍵の保護規則

- **`config.yaml`、`.env`、`surfshark_credentials.json`、`*.conf` を Git 等のバージョン管理にコミットしないでください。**
- 本リポジトリには、ローカル認証情報、ランタイムデータベース（`*.db*`）、取得結果ファイル（`available*.txt`、`taken*.txt`、`results/`）、コンパイル済みバイナリ（`*.exe`、`*.apk`）のコミットを未然に遮断する強固な `.gitignore` が設定されています。
- 常に `config/.env.example`、`config/config.example.yaml`、`data/surfshark_credentials.example.json` テンプレートを複製して利用してください。
- ソースコードおよび公式文書のいかなる場所にも、秘密鍵やパスワードはハードコードされていません。

[⬆️ 目次の先頭へ移動](#目次)

---

<a id="-2-ネットワーク分離とレート制限の安全性"></a>
## 2. ネットワーク分離とレート制限の安全性

- 全てのHTTPリクエストは `curl_cffi` による Chrome 131 TLS ステルス偽装を経由し、ユーザ空間 HTTP/SOCKS5 分離トンネル（`wireproxy`）を通じてルーティングされます。
- ホストOSの標準ネットワークインターフェース、ルーティングテーブル、DNS設定は一切変更されません。
- 429検出時は0.3秒未満で自動ホットスワップが実行され、特定IPへの過度な負荷集中を防ぎます。

[⬆️ 目次の先頭へ移動](#目次)

---

<a id="-3-セキュリティ脆弱性の報告-reporting-a-security-issue"></a>
## 3. セキュリティ脆弱性の報告 (Reporting a Security Issue)

- セキュリティ脆弱性や誤ったシークレット公開を発見した場合は、公開イシューを作成せず、GitHub の **Private Security Advisory** 経由で非公開にてご報告ください。
- またはリポジトリ所有者（`KRCUPRO`）へ直接ご連絡いただければ、24時間以内に調査および修正パッチを発行します。

[⬆️ 目次の先頭へ移動](#目次)

---

<a id="-4-責任ある研究と倫理規定"></a>
## 4. 責任ある研究と倫理規定

- 本プログラムは、TLSフィンガープリント、非同期プロキシプール管理、並行ネットワークプログラミングの学習および学術研究目的でのみ提供されます。
- DoS/DDoS攻撃や第三者サービスの規約を侵害する不正使用を固く禁止します。

[⬆️ 目次の先頭へ移動](#目次)

