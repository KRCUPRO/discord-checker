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

## 📖 概要 (Overview)

**D4UC (Discord 4-Character Usernames Checker)** は、Discordの希少な固有ユーザー名（3〜6文字）を最速かつ安全に探索・先取りするために設計された高機能自動化チェッカーです。

Chrome 131 TLS擬装、Surfshark WireGuard 1:1隔離トンネリング、SQLite WAL重複排除に加え、**iPhone、iPad、Android、タブレット、PCなど機種不問で100%ブラウザ完結するクラウド実行**（Google Colab Web GUI ＆ Google Apps Script 24時間無人チェッカー）を完全サポートしています。

---

## 📱 iPhone・iPad・Android・タブレット機種不問サポート (Zero-Install)

> **「PCがなくても、アプリをインストールしなくても大丈夫！」**  
> iPhoneのSafariや各種タブレットのブラウザを開くだけで、即座に24時間クラウド検査を開始できます。詳細は [📱 モバイル/iPhone専用ガイド](./docs/MOBILE_AND_IPHONE_GUIDE.md) をご覧ください。

1. **🍏 Apple iOS (iPhone / iPad)**:
   - 脱獄不要、追加アプリ不要で純正 **Safari ブラウザ** から [Google Colab](./D4UC_Google_Colab.ipynb) や [Google Apps Script](./docs/GAS_24H_CHECKER_GUIDE.md) を1クリック起動可能。
2. **🤖 Android スマートフォン ＆ タブレット**:
   - Chromeブラウザで対話型Web GUIを操作するか、GASで24時間バックグラウンド自動実行が可能。
3. **🔋 バッテリー消費0%・端末の電源OFFでも継続稼働 (24/7 Cloud)**:
   - **Google Apps Script** を起動すれば、スマホの電源を切ってもGoogleのクラウドサーバー上で24時間365日無人で稼働し続けます。
4. **🔔 スマホへのリアルタイム通知**:
   - 利用可能な名前を発見すると、スマホの **Discord アプリ** および **Google スプレッドシート アプリ** に即時プッシュ通知されます。

---

## 🚀 6大クロスプラットフォーム実行環境の比較

| 実行環境 | 対応機器 (Supported Devices) | 特徴と主な用途 | クイックスタート / リンク |
| :--- | :--- | :--- | :--- |
| **☁️ Google Apps Script** | 📱 **全機種 100% 対応** (iPhone, iPad, Android, タブレット, PC) | **端末の電源OFFでも稼働**、Googleクラウド24/7無人チェッカー | [GAS 24/7 ガイド](./docs/GAS_24H_CHECKER_GUIDE.md) |
| **⚡ Google Colab Web GUI** | 📱 **全機種 100% 対応** (Safari, Chrome等のブラウザ搭載端末) | セル内対話型ダークダッシュボード、Googleドライブ完全同期 | [`D4UC_Google_Colab.ipynb`](./D4UC_Google_Colab.ipynb) |
| **🖥️ Windows Desktop GUI** | 💻 Windows PC (Windows 10/11) | 直感的なダークテーマGUI、リアルタイムKPI、ツールチップ完備 | `DiscordUsernameCheckerV2.exe` |
| **📱 Android Termux** | 🤖 Android 専用 (ルート化不要) | モバイル端末バックグラウンド24時間ネイティブ実行 (Debian proot) | [Termux ガイド](./docs/TERMUX_DEBIAN_GUIDE.md) |
| **🐳 Docker & Compose** | 🖥️ Linux / Mac / サーバー / NAS | ARM64/AMD64 マルチアーキテクチャサーバーコンテナ | `docker compose up -d` |
| **⚙️ Headless CLI** | 🖥️ Linux / Windows / サーバー | 高速コンソールバックグラウンド実行エンジン | `python run.py --mode Permutation` |

---

## 🌟 主な機能 (Key Features)

1. **Google Apps Script 24/7 サーバーレスチェッカー (`gas/`)**:
   - 予約トリガーによる24時間自動巡回＆6分制限を突破する4.5分 Self-Chaining。
   - Google Drive ファイル保存 ＋ Google Sheets リアルタイム同期(`D4UC_Tracker`)。
2. **Google Colab インタラクティブ Web GUI (`colab_gui.py`)**:
   - 外部トンネル不要でColabセル内に描画されるモダンダークダッシュボード。
3. **10言語1:1完全対応**: 全196キー完全マッピング。
4. **Surfshark WireGuard 1:1 隔離マルチトンネル**: Discord 429 制限を根本的に回避。
5. **Discord Webhook リアルタイム通知**: 発見時に即座に通知を送信。

---

## 📄 ライセンス (License)
本プロジェクトは [MIT License](./LICENSE) の下で配布されます。
