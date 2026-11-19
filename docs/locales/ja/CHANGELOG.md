<div align="center">

# 📋 変更履歴 (Changelog)

> **D4UC (discord-checker) のバージョン別更新履歴および技術改善記録**

<br />

| [KR 한국어](../ko/CHANGELOG.md) | [US English](../en/CHANGELOG.md) | [JP 日本語](./CHANGELOG.md) | [CN 简体中文](../zh-CN/CHANGELOG.md) | [ES Español](../es/CHANGELOG.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/CHANGELOG.md) | [DE Deutsch](../de/CHANGELOG.md) | [RU Русский](../ru/CHANGELOG.md) | [BR Português](../pt-BR/CHANGELOG.md) | [SA العربية](../ar/CHANGELOG.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/CHANGELOG.md">HI हिन्दी</a> • <a href="../id/CHANGELOG.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 2026年11月19日](../../assets/badges/update_badge_ja.svg)](./CHANGELOG.md)
[![Latest Release](https://img.shields.io/badge/Release-v12.5.0-blue.svg)](https://github.com/KRCUPRO/discord-checker/releases)

</div>

---

<a id="目次"></a>
## 📑 目次
1. [[v12.5.0] — 2026-11-19](#-v1250-2026-11-19)
1. [[v12.4.0] — 2026-11-19](#-v1240-2026-11-19)
1. [[v12.3.0] — 2026-11-19](#-v1230-2026-11-19)
1. [[v12.2.0] — 2026-11-19](#-v1220-2026-11-19)
1. [[v12.0.0] — 2026-11-18](#-v1200-2026-11-18)

---

> 本ファイルには、D4UCの各公式リリースにおける新機能追加、設計改善、バグ修正の全履歴を記録します。

---

<a id="-v1250-2026-11-19"></a>
## [v12.5.0] — 2026-11-19

### Added
- **12言語 1:1 完全対応公式ドキュメントスイート (`docs/locales/<lang>/`)**: 8大主要文書（README、ARCHITECTURE_MAP、GUIDE、TASKS、CHANGELOG、LICENSE、NOTICE、SECURITY）を12言語（日本語、韓国語、英語、簡体字中国語、スペイン語、フランス語、ドイツ語、ロシア語、ポルトガル語、アラビア語、ヒンディー語、インドネシア語）へ1:1完全翻訳・配備。
- **GitHubリポジトリルートの整理とモジュール化**: 内部スクリプトを `deploy/scripts/` へ集約し、不要な重複ファイルを削除して、訪問時に概要とプレビューが即座に表示されるよう6フォルダ＋8ファイルの構造へ大幅スリム化。
- **文書上部クイックジャンプバー**: スクロール不要で即座に目的の章へジャンプできるワンタッチリンクを追加。

### Changed
- すべての文書上部に5×2規格の対称言語選択表およびリアルタイム更新SVGバッジ（`2026年11月19日`）を同期。

[⬆️ 目次の先頭へ移動](#目次)

---

<a id="-v1240-2026-11-19"></a>
## [v12.4.0] — 2026-11-19

### Added
- **双方向ドキュメントナビゲーション**: 全26文書に相互ジャンプ目次と「目次の先頭へ戻る」リンクを完全適用。
- **13種類のOS別公式ガイド (`docs/guides/`)**: Windows、macOS、Linux、Android APK、iOS PWA、Docker Compose等の環境別ガイド完備。

[⬆️ 目次の先頭へ移動](#目次)

---

<a id="-v1230-2026-11-19"></a>
## [v12.3.0] — 2026-11-19

### Added
- **無料公開プロキシ自動収集・検証エンジン**: 18公開ソースからリアルタイム収集、Cloudflare検証、15秒クールダウンキュー機能。
- **署名済みAndroid単独APK**: v1/v2/v3署名付きAPKパッケージおよびバックグラウンド省電力除外設定ガイド。

[⬆️ 目次の先頭へ移動](#目次)

---

<a id="-v1220-2026-11-19"></a>
## [v12.2.0] — 2026-11-19

### Added
- **モバイルタッチ最適化Web GUI & PWA**: ポート5000対応レスポンシブUI、0.1秒Discord Webhook即時通知。

[⬆️ 目次の先頭へ移動](#目次)

---

<a id="-v1200-2026-11-18"></a>
## [v12.0.0] — 2026-11-18

### Added
- **正式マルチプラットフォームリリース**: Windows単独EXE 4種、8大生成エンジン、Chrome 131 TLS ステルス偽装。

[⬆️ 目次の先頭へ移動](#目次)

