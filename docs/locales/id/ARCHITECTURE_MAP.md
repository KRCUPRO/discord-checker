<div align="center">

# 🏛️ Pemetaan Arsitektur & Cetak Biru Sistem D4UC (ARCHITECTURE_MAP.md)

> **Konkurensi Asinkron Tanpa Rugi, Persistensi 0% Konflik, Penyamaran TLS, dan Isolasi Terowongan 1:1**

<br />

| [KR 한국어](../ko/ARCHITECTURE_MAP.md) | [US English](../en/ARCHITECTURE_MAP.md) | [JP 日本語](../ja/ARCHITECTURE_MAP.md) | [CN 简体中文](../zh-CN/ARCHITECTURE_MAP.md) | [ES Español](../es/ARCHITECTURE_MAP.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/ARCHITECTURE_MAP.md) | [DE Deutsch](../de/ARCHITECTURE_MAP.md) | [RU Русский](../ru/ARCHITECTURE_MAP.md) | [BR Português](../pt-BR/ARCHITECTURE_MAP.md) | [SA العربية](../ar/ARCHITECTURE_MAP.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/ARCHITECTURE_MAP.md">HI हिन्दी</a> • <a href="./ARCHITECTURE_MAP.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 19 Nov 2026](../../assets/badges/update_badge_id.svg)](./CHANGELOG.md)
[![Architecture: Lossless Multi-Tier](https://img.shields.io/badge/Architecture-Lossless%20Multi--Tier-purple.svg)](./ARCHITECTURE_MAP.md)

</div>

---

<a id="-daftar-isi"></a>
## 📑 Daftar Isi
1. [1. Arsitektur Sistem Berlapis (Layered Architecture)](#-1-arsitektur-sistem-berlapis-layered-architecture)
2. [2. Alur Eksekusi Ujung-ke-Ujung (End-to-End Execution Flow)](#-2-alur-eksekusi-ujung-ke-ujung-end-to-end-execution-flow)
3. [3. Konkurensi Throughput Tinggi & Pencegahan Kebuntuan](#-3-konkurensi-throughput-tinggi--pencegahan-kebuntuan)
4. [4. Aliran Data & Persistensi SQLite WAL](#-4-aliran-data--persistensi-sqlite-wal)
5. [5. Arsitektur Keamanan dan Isolasi Jaringan](#-5-arsitektur-keamanan-dan-isolasi-jaringan)

---

## 💎 Prinsip Utama Arsitektur
- **Konkurensi Asinkron Tanpa Rugi**: Hingga 50 worker paralel tanpa pemblokiran pada event loop `asyncio`.
- **Persistensi 0% Konflik**: SQLite WAL dengan `busy_timeout=5000ms` menghilangkan kebuntuan antar-proses (deadlock).
- **Penyamaran TLS Chrome 131**: `curl_cffi` mereplikasi jabat tangan JA3/JA4 secara presisi untuk melewati WAF.
- **Isolasi Terowongan 1:1 Ruang Pengguna**: `wireproxy` merutekan lalu lintas jaringan tanpa mengubah konfigurasi OS host.

---

<a id="-1-arsitektur-sistem-berlapis-layered-architecture"></a>
## 🏛️ 1. Arsitektur Sistem Berlapis (Layered Architecture)

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

### Lapisan 1: Presentasi
`src/gui_ko.py` (Bahasa Korea), `src/gui_en.py` (Bahasa Inggris), `src/web_gui.py` (Web GUI Sentuh / PWA), `src/run.py` (Terminal Rich CLI).

### Lapisan 2: Orkestrasi
Loop worker latar belakang, telemetri langsung (RPS, Tersedia, 429), dan koordinator sharding (`2_1`, `2_2`).

### Lapisan 3: Jaringan & Siluman TLS
`DiscordApiClient` (`curl_cffi`), sidik jari TLS Chrome 131, dan peniruan header peramban.

### Lapisan 4: Infrastruktur Proxy
`UnifiedProxyManager`, `SurfsharkProxyProvider` (1:1), `FreeProxyProvider`, dan hot-swap 429 atomik dalam 0,3 detik.

### Lapisan 5: Mesin Pembuat Kandidat
Factory `create_generator()`: Permutasi, Hibrida, Kamus, Masking, Pola, Numerik, Kombinatorial, Verifikasi Ulang.

### Lapisan 6: Penyimpanan & Notifikasi
`StorageManager`, SQLite WAL (`d4uc_results.db`), pencerminan berkas txt, dan webhook Discord.


[⬆️ Kembali ke Daftar Isi](#-daftar-isi)

---

<a id="-2-alur-eksekusi-ujung-ke-ujung-end-to-end-execution-flow"></a>
## 🔄 2. Alur Eksekusi Ujung-ke-Ujung (End-to-End Execution Flow)

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

[⬆️ Kembali ke Daftar Isi](#-daftar-isi)

---

<a id="-3-konkurensi-throughput-tinggi--pencegahan-kebuntuan"></a>
## ⚡ 3. Konkurensi Throughput Tinggi & Pencegahan Kebuntuan

- **Non-blocking Concurrency**: All network I/O operations are scheduled on Python's native `asyncio` event loop.
- **429 Atomic Hot-Swap**: When an isolated worker hits Discord's 429 rate limit, its specific Wireproxy local port is seamlessly reassigned to an available server node in under 0.3s without affecting concurrent workers.
- **Zero Lock Deadlock**: SQLite WAL journal mode coupled with Python-level queueing completely eliminates `database is locked` operational exceptions.

[⬆️ Kembali ke Daftar Isi](#-daftar-isi)

---

<a id="-4-aliran-data--persistensi-sqlite-wal"></a>
## 💾 4. Aliran Data & Persistensi SQLite WAL

- **Primary Database**: `data/d4uc_results.db` configured with `PRAGMA journal_mode = WAL` and `PRAGMA synchronous = NORMAL`.
- **Text File Mirroring**: For maximum legacy compatibility, all newly verified rare handles are concurrently appended to `available.txt` and `checked_history.txt`.

[⬆️ Kembali ke Daftar Isi](#-daftar-isi)

---

<a id="-5-arsitektur-keamanan-dan-isolasi-jaringan"></a>
## 🛡️ 5. Arsitektur Keamanan dan Isolasi Jaringan

- **Zero-Leak Policy**: All local credentials, WireGuard configuration files, and secrets are strictly excluded from version control.
- **User-Space Network Isolation**: All proxy traffic is terminated in user space (`wireproxy`), preventing interference with system-wide DNS or routing tables.

[⬆️ Kembali ke Daftar Isi](#-daftar-isi)
