<div align="center">

# 🏛️ D4UC アーキテクチャマッピングとシステム構造図 (ARCHITECTURE_MAP.md)

> **無損失非同期並行処理、0%衝突永続化同期、TLSステルス偽装および1:1ユーザ空間トンネル隔離**

<br />

| [KR 한국어](../ko/ARCHITECTURE_MAP.md) | [US English](../en/ARCHITECTURE_MAP.md) | [JP 日本語](./ARCHITECTURE_MAP.md) | [CN 简体中文](../zh-CN/ARCHITECTURE_MAP.md) | [ES Español](../es/ARCHITECTURE_MAP.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/ARCHITECTURE_MAP.md) | [DE Deutsch](../de/ARCHITECTURE_MAP.md) | [RU Русский](../ru/ARCHITECTURE_MAP.md) | [BR Português](../pt-BR/ARCHITECTURE_MAP.md) | [SA العربية](../ar/ARCHITECTURE_MAP.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/ARCHITECTURE_MAP.md">HI हिन्दी</a> • <a href="../id/ARCHITECTURE_MAP.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 2026年11月19日](../../assets/badges/update_badge_ja.svg)](./CHANGELOG.md)
[![Architecture: Lossless Multi-Tier](https://img.shields.io/badge/Architecture-Lossless%20Multi--Tier-purple.svg)](./ARCHITECTURE_MAP.md)

</div>

---

<a id="目次"></a>
## 📑 目次
1. [1. システム階層アーキテクチャ (Layered Architecture)](#-1-システム階層アーキテクチャ-layered-architecture)
2. [2. エンドツーエンド実行フロー (End-to-End Execution Flow)](#-2-エンドツーエンド実行フロー-end-to-end-execution-flow)
3. [3. 高スループット並行処理とデッドロック防止構造](#-3-高スループット並行処理とデッドロック防止構造)
4. [4. データ永続化および同期 (SQLite WAL)](#-4-データ永続化および同期-sqlite-wal)
5. [5. セキュリティとネットワーク隔離機構](#-5-セキュリティとネットワーク隔離機構)

---

## 💎 コア設計原則
- **無損失非同期並行処理**: `asyncio` イベントループを基盤とし、最大50ワーカがノンブロッキング並行処理を実行。
- **0%衝突永続化同期**: SQLite WALおよび `busy_timeout=5000ms` によりマルチプロセス間のデッドロックを完全防止。
- **TLSステルス偽装**: `curl_cffi` により Chrome 131 JA3/JA4 ハンドシェイクを完全に再現。
- **1:1ユーザ空間トンネル隔離**: `wireproxy` を通じてOSのネットワーク設定に影響を与えず隔離ルーティングを実現。

---

<a id="-1-システム階層アーキテクチャ-layered-architecture"></a>
## 🏛️ 1. システム階層アーキテクチャ (Layered Architecture)

```mermaid
graph TD
    subgraph Layer 1: Presentation ["1. Presentation Layer (UI / CLI)"]
        GUI_KO["src/gui_ko.py (Korean GUI)"]
        GUI_EN["src/gui_en.py (English GUI)"]
        GUI_WEB["src/web_gui.py (Mobile Touch Web GUI / PWA)"]
        CLI["src/run.py (Headless CLI + Rich Dashboard)"]
    end

    subgraph Layer 2: Orchestration ["2. Orchestration & Worker Loop"]
        ORCH["Orchestrator / Async Worker Loop"]
        METRICS["DashboardMetrics (RPS, Available, Taken, 429)"]
        SHARD["Sharding Coordinator (2_1, 2_2, 3_1...)"]
    end

    subgraph Layer 3: Network & Stealth ["3. Network & TLS Stealth"]
        CLIENT["DiscordApiClient (curl_cffi AsyncSession)"]
        TLS["Chrome 131 TLS JA3/JA4 Fingerprint"]
        HEADERS["Browser Headers (sec-ch-ua, Referer, Accept)"]
    end

    subgraph Layer 4: Proxy Infrastructure ["4. Proxy Infrastructure & Multi-Tunnel"]
        UPM["UnifiedProxyManager"]
        SURF["SurfsharkProxyProvider (1:1 Multi-Tunnel)"]
        FREE["FreeProxyProvider (18 Open-Source Pools)"]
        WIRE["Wireproxy Process Daemon (User-Space Netstack)"]
        COOLDOWN["429 Cooldown Queue & 0.3s Atomic Hot-Swap Engine"]
    end

    subgraph Layer 5: Candidate Generator ["5. Candidate Username Generator Engine"]
        GEN_FACT["create_generator() Factory"]
        HYBRID["HybridGenerator"]
        PERM["PermutationGenerator (Sharded Math Engine)"]
        DICT["DictionaryGenerator"]
        MASK["CustomMaskGenerator"]
        OTHER_GEN["Pattern / Numeric / Combinatorial / Recheck"]
    end

    subgraph Layer 6: Storage & Notify ["6. Persistent Storage & Notifications"]
        STORAGE["StorageManager (Async Queue Worker)"]
        SQLITE["SQLite WAL (d4uc_results.db, busy_timeout=5s)"]
        MIRROR["Legacy Mirror (available.txt, taken.txt)"]
        WEBHOOK["DiscordWebhookNotifier (0.1s Dispatch)"]
    end

    GUI_KO & GUI_EN & GUI_WEB & CLI --> ORCH
    ORCH --> GEN_FACT
    GEN_FACT --> HYBRID & PERM & DICT & MASK & OTHER_GEN
    ORCH --> CLIENT
    CLIENT --> TLS & HEADERS
    ORCH --> UPM
    UPM --> SURF & FREE & WIRE & COOLDOWN
    ORCH --> STORAGE
    STORAGE --> SQLITE & MIRROR & WEBHOOK
```

### Layer 1: プレゼンテーション層 (Presentation)
`src/gui_ko.py` (韓国語GUI), `src/gui_en.py` (英語GUI), `src/web_gui.py` (モバイルWeb GUI / PWA), `src/run.py` (Rich CLI)。

### Layer 2: オーケストレーション層 (Orchestration)
バックグラウンドワーカループ、リアルタイムテレメトリ（RPS、発見数、使用中、429）、シャーディング調整器。

### Layer 3: ネットワークおよびTLSステルス偽装 (Network & Stealth)
`DiscordApiClient` (curl_cffi AsyncSession), Chrome 131 TLS 指紋および完全なブラウザヘッダー模倣。

### Layer 4: プロキシ基盤および複数トンネル (Proxy Infrastructure)
`UnifiedProxyManager`, `SurfsharkProxyProvider` (1:1 Multi-Tunnel), `FreeProxyProvider`, 0.3秒ホットスワップ。

### Layer 5: 候補生成エンジン (Candidate Generator)
`create_generator()`: 順列、ハイブリッド、辞書、カスタムマスク、パターン、数字、組合せ、再検証。

### Layer 6: ストレージおよび通知層 (Storage & Notify)
`StorageManager`, SQLite WAL (`d4uc_results.db`), レガシーtxt同期 (`available.txt`, `taken.txt`), Discord Webhook。


[⬆️ 目次の先頭へ移動](#目次)

---

<a id="-2-エンドツーエンド実行フロー-end-to-end-execution-flow"></a>
## 🔄 2. エンドツーエンド実行フロー (End-to-End Execution Flow)

```text
[Candidate Generator] ──(Next Batch)──> [Orchestrator Worker Pool]
                                                    │
                                            (Lease Isolated SOCKS5)
                                                    ▼
                                        [Unified Proxy Manager]
                                                    │
                                          (Chrome 131 TLS Impersonation)
                                                    ▼
                                        [Discord API Endpoint]
                                                    │
                                         (Response Dispatch)
                        ┌───────────────────────────┴───────────────────────────┐
                        ▼                                                       ▼
               HTTP 200 / Taken                                         HTTP 429 Rate Limit
                        │                                                       │
        ┌───────────────┴───────────────┐                             (0.3s Atomic Hot-Swap)
        ▼                               ▼                                       ▼
 [SQLite WAL Storage]       [Discord Webhook Push]                  [Rotate to Fresh Country]
```

[⬆️ 目次の先頭へ移動](#目次)

---

<a id="-3-高スループット並行処理とデッドロック防止構造"></a>
## ⚡ 3. 高スループット並行処理とデッドロック防止構造

- **Non-blocking Concurrency**: All network I/O operations are scheduled on Python's native `asyncio` event loop.
- **429 Atomic Hot-Swap**: When an isolated worker hits Discord's 429 rate limit, its specific Wireproxy local port is seamlessly reassigned to an available server node in under 0.3s without affecting concurrent workers.
- **Zero Lock Deadlock**: SQLite WAL journal mode coupled with Python-level queueing completely eliminates `database is locked` operational exceptions.

[⬆️ 目次の先頭へ移動](#目次)

---

<a id="-4-データ永続化および同期-sqlite-wal"></a>
## 💾 4. データ永続化および同期 (SQLite WAL)

- **Primary Database**: `data/d4uc_results.db` configured with `PRAGMA journal_mode = WAL` and `PRAGMA synchronous = NORMAL`.
- **Text File Mirroring**: For maximum legacy compatibility, all newly verified rare handles are concurrently appended to `available.txt` and `checked_history.txt`.

[⬆️ 目次の先頭へ移動](#目次)

---

<a id="-5-セキュリティとネットワーク隔離機構"></a>
## 🛡️ 5. セキュリティとネットワーク隔離機構

- **Zero-Leak Policy**: All local credentials, WireGuard configuration files, and secrets are strictly excluded from version control.
- **User-Space Network Isolation**: All proxy traffic is terminated in user space (`wireproxy`), preventing interference with system-wide DNS or routing tables.

[⬆️ 目次の先頭へ移動](#目次)
