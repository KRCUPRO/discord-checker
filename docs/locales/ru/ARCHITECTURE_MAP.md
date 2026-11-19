<div align="center">

# 🏛️ Архитектурная карта и схема системы D4UC (ARCHITECTURE_MAP.md)

> **Асинхронный параллелизм без потерь, бесконфликтная синхронизация, стелс-TLS и изоляция 1:1**

<br />

| [KR 한국어](../ko/ARCHITECTURE_MAP.md) | [US English](../en/ARCHITECTURE_MAP.md) | [JP 日本語](../ja/ARCHITECTURE_MAP.md) | [CN 简体中文](../zh-CN/ARCHITECTURE_MAP.md) | [ES Español](../es/ARCHITECTURE_MAP.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/ARCHITECTURE_MAP.md) | [DE Deutsch](../de/ARCHITECTURE_MAP.md) | [RU Русский](./ARCHITECTURE_MAP.md) | [BR Português](../pt-BR/ARCHITECTURE_MAP.md) | [SA العربية](../ar/ARCHITECTURE_MAP.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/ARCHITECTURE_MAP.md">HI हिन्दी</a> • <a href="../id/ARCHITECTURE_MAP.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 19 ноя 2026](../../assets/badges/update_badge_ru.svg)](./CHANGELOG.md)
[![Architecture: Lossless Multi-Tier](https://img.shields.io/badge/Architecture-Lossless%20Multi--Tier-purple.svg)](./ARCHITECTURE_MAP.md)

</div>

---

<a id="-содержание"></a>
## 📑 Содержание
1. [1. Многоуровневая архитектура системы](#-1-многоуровневая-архитектура-системы)
2. [2. Сквозной рабочий процесс (End-to-End)](#-2-сквозной-рабочий-процесс-end-to-end)
3. [3. Высокопроизводительный параллелизм и защита от взаимных блокировок](#-3-высокопроизводительный-параллелизм-и-защита-от-взаимных-блокировок)
4. [4. Потоки данных и сохранение в SQLite WAL](#-4-потоки-данных-и-сохранение-в-sqlite-wal)
5. [5. Архитектура безопасности и сетевой изоляции](#-5-архитектура-безопасности-и-сетевой-изоляции)

---

## 💎 Ключевые принципы архитектуры
- **Асинхронный параллелизм без потерь**: До 50 воркеров на цикле событий `asyncio` без блокировок.
- **Бесконфликтная синхронизация**: SQLite WAL с `busy_timeout=5000ms` предотвращает взаимные блокировки.
- **Стелс-маскировка TLS Chrome 131**: `curl_cffi` точно воспроизводит отпечатки JA3/JA4.
- **Изоляция туннелей в пространстве пользователя**: `wireproxy` маршрутизирует трафик без вмешательства в сеть ОС.

---

<a id="-1-многоуровневая-архитектура-системы"></a>
## 🏛️ 1. Многоуровневая архитектура системы

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

### Уровень 1: Представление
`src/gui_ko.py` (Корейский), `src/gui_en.py` (Английский), `src/web_gui.py` (Мобильный Web GUI / PWA), `src/run.py` (Rich CLI).

### Уровень 2: Оркестрация
Пул фоновых воркеров, телеметрия в реальном времени (RPS, Доступно, 429) и координатор шардинга (`2_1`, `2_2`).

### Уровень 3: Сеть и стелс-TLS
`DiscordApiClient` (`curl_cffi`), отпечатки Chrome 131 и эмуляция заголовков браузера.

### Уровень 4: Инфраструктура прокси
`UnifiedProxyManager`, `SurfsharkProxyProvider` (1:1), `FreeProxyProvider`, горячая замена при 429 за 0.3с.

### Уровень 5: Генераторы имен
Фабрика `create_generator()`: Перестановки, Гибридный, Словарь, Маска, Шаблон, Числовой, Комбинаторный, Перепроверка.

### Уровень 6: Хранилище и оповещения
`StorageManager`, SQLite WAL (`d4uc_results.db`), зеркалирование в txt и Discord Webhook.


[⬆️ Наверх к содержанию](#-содержание)

---

<a id="-2-сквозной-рабочий-процесс-end-to-end"></a>
## 🔄 2. Сквозной рабочий процесс (End-to-End)

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

[⬆️ Наверх к содержанию](#-содержание)

---

<a id="-3-высокопроизводительный-параллелизм-и-защита-от-взаимных-блокировок"></a>
## ⚡ 3. Высокопроизводительный параллелизм и защита от взаимных блокировок

- **Non-blocking Concurrency**: All network I/O operations are scheduled on Python's native `asyncio` event loop.
- **429 Atomic Hot-Swap**: When an isolated worker hits Discord's 429 rate limit, its specific Wireproxy local port is seamlessly reassigned to an available server node in under 0.3s without affecting concurrent workers.
- **Zero Lock Deadlock**: SQLite WAL journal mode coupled with Python-level queueing completely eliminates `database is locked` operational exceptions.

[⬆️ Наверх к содержанию](#-содержание)

---

<a id="-4-потоки-данных-и-сохранение-в-sqlite-wal"></a>
## 💾 4. Потоки данных и сохранение в SQLite WAL

- **Primary Database**: `data/d4uc_results.db` configured with `PRAGMA journal_mode = WAL` and `PRAGMA synchronous = NORMAL`.
- **Text File Mirroring**: For maximum legacy compatibility, all newly verified rare handles are concurrently appended to `available.txt` and `checked_history.txt`.

[⬆️ Наверх к содержанию](#-содержание)

---

<a id="-5-архитектура-безопасности-и-сетевой-изоляции"></a>
## 🛡️ 5. Архитектура безопасности и сетевой изоляции

- **Zero-Leak Policy**: All local credentials, WireGuard configuration files, and secrets are strictly excluded from version control.
- **User-Space Network Isolation**: All proxy traffic is terminated in user space (`wireproxy`), preventing interference with system-wide DNS or routing tables.

[⬆️ Наверх к содержанию](#-содержание)
