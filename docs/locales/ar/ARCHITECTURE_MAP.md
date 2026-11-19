<div align="center">

# 🏛️ مخطط الهيكلية الهندسية وتصميم النظام D4UC (ARCHITECTURE_MAP.md)

> **تزامن غير متزامن بدون فقدان، وتخزين بيانات بلا تعارض، ومحاكاة TLS الخفية وعزل الأنفاق بنسبة 1:1**

<br />

| [KR 한국어](../ko/ARCHITECTURE_MAP.md) | [US English](../en/ARCHITECTURE_MAP.md) | [JP 日本語](../ja/ARCHITECTURE_MAP.md) | [CN 简体中文](../zh-CN/ARCHITECTURE_MAP.md) | [ES Español](../es/ARCHITECTURE_MAP.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/ARCHITECTURE_MAP.md) | [DE Deutsch](../de/ARCHITECTURE_MAP.md) | [RU Русский](../ru/ARCHITECTURE_MAP.md) | [BR Português](../pt-BR/ARCHITECTURE_MAP.md) | [SA العربية](./ARCHITECTURE_MAP.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/ARCHITECTURE_MAP.md">HI हिन्दी</a> • <a href="../id/ARCHITECTURE_MAP.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 19 نوفمبر 2026](../../assets/badges/update_badge_ar.svg)](./CHANGELOG.md)
[![Architecture: Lossless Multi-Tier](https://img.shields.io/badge/Architecture-Lossless%20Multi--Tier-purple.svg)](./ARCHITECTURE_MAP.md)

</div>

---

<a id="-فهرس-المحتويات"></a>
## 📑 فهرس المحتويات
1. [1. الهيكلية المعمارية متعددة الطبقات](#-1-الهيكلية-المعمارية-متعددة-الطبقات)
2. [2. مسار التنفيذ الشامل (End-to-End)](#-2-مسار-التنفيذ-الشامل-end-to-end)
3. [3. التزامن عالي الإنتاجية وتفادي الاختناقات البرمجية](#-3-التزامن-عالي-الإنتاجية-وتفادي-الاختناقات-البرمجية)
4. [4. تدفق البيانات والتخزين الدائم في SQLite WAL](#-4-تدفق-البيانات-والتخزين-الدائم-في-sqlite-wal)
5. [5. آليات الأمان والعزل الشبكي](#-5-آليات-الأمان-والعزل-الشبكي)

---

## 💎 المبادئ الهندسية الأساسية
- **تزامن غير متزامن بدون فقدان**: تشغيل ما يصل إلى 50 عاملاً متزامناً بالاعتماد على حلقة أحداث `asyncio` دون أي حظر للمهام.
- **تخزين بيانات بلا تعارض بنسبة 0%**: وضع SQLite WAL مع مهلة `busy_timeout=5000ms` لمنع تصادم العمليات المتعددة نهائياً.
- **محاكاة بصمة TLS الخفية**: استخدام `curl_cffi` لإعادة إنتاج بصمات Chrome 131 JA3/JA4 بالكامل لتخطي أنظمة الحماية.
- **عزل الأنفاق بنسبة 1:1 في مساحة المستخدم**: استخدام `wireproxy` لتوجيه الاتصالات محلياً دون أي تأثير على شبكة نظام التشغيل.

---

<a id="-1-الهيكلية-المعمارية-متعددة-الطبقات"></a>
## 🏛️ 1. الهيكلية المعمارية متعددة الطبقات

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

### الطبقة 1: طبقة العرض والواجهة
`src/gui_ko.py` (كوري)، `src/gui_en.py` (إنجليزي)، `src/web_gui.py` (واجهة الويب للموبايل / PWA)، `src/run.py` (سطر الأوامر Rich CLI).

### الطبقة 2: طبقة التنسيق والإدارة
حلقة إدارة العمال في الخلفية، مقاييس الأداء الفورية (RPS، المتاح، المستخدم، 429)، ومقسم النطاقات (`2_1`، `2_2`).

### الطبقة 3: الشبكة والتمويه TLS
`DiscordApiClient` عبر `curl_cffi`، محاكاة بصمات Chrome 131 TLS وترويسات المتصفح الكاملة.

### الطبقة 4: بنية البروكسي والأنفاق المتعددة
`UnifiedProxyManager`، موفر Surfshark بنسبة 1:1، وموفر البروكسيات المجانية، والتبديل السريع عند 429 في 0.3 ثانية.

### الطبقة 5: محركات توليد أسماء المستخدمين
مصنع `create_generator()`: التباديل، الهجين، القاموس، الأقنعة المخصصة، الأنماط، الأرقام، التوافيق، وإعادة الفحص.

### الطبقة 6: التخزين والإشعارات
`StorageManager`، قاعدة بيانات SQLite WAL (`d4uc_results.db`)، ملفات txt النصية، وتنبيهات Discord Webhook.


[⬆️ العودة إلى أعلى الفهرس](#-فهرس-المحتويات)

---

<a id="-2-مسار-التنفيذ-الشامل-end-to-end"></a>
## 🔄 2. مسار التنفيذ الشامل (End-to-End)

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

[⬆️ العودة إلى أعلى الفهرس](#-فهرس-المحتويات)

---

<a id="-3-التزامن-عالي-الإنتاجية-وتفادي-الاختناقات-البرمجية"></a>
## ⚡ 3. التزامن عالي الإنتاجية وتفادي الاختناقات البرمجية

- **Non-blocking Concurrency**: All network I/O operations are scheduled on Python's native `asyncio` event loop.
- **429 Atomic Hot-Swap**: When an isolated worker hits Discord's 429 rate limit, its specific Wireproxy local port is seamlessly reassigned to an available server node in under 0.3s without affecting concurrent workers.
- **Zero Lock Deadlock**: SQLite WAL journal mode coupled with Python-level queueing completely eliminates `database is locked` operational exceptions.

[⬆️ العودة إلى أعلى الفهرس](#-فهرس-المحتويات)

---

<a id="-4-تدفق-البيانات-والتخزين-الدائم-في-sqlite-wal"></a>
## 💾 4. تدفق البيانات والتخزين الدائم في SQLite WAL

- **Primary Database**: `data/d4uc_results.db` configured with `PRAGMA journal_mode = WAL` and `PRAGMA synchronous = NORMAL`.
- **Text File Mirroring**: For maximum legacy compatibility, all newly verified rare handles are concurrently appended to `available.txt` and `checked_history.txt`.

[⬆️ العودة إلى أعلى الفهرس](#-فهرس-المحتويات)

---

<a id="-5-آليات-الأمان-والعزل-الشبكي"></a>
## 🛡️ 5. آليات الأمان والعزل الشبكي

- **Zero-Leak Policy**: All local credentials, WireGuard configuration files, and secrets are strictly excluded from version control.
- **User-Space Network Isolation**: All proxy traffic is terminated in user space (`wireproxy`), preventing interference with system-wide DNS or routing tables.

[⬆️ العودة إلى أعلى الفهرس](#-فهرس-المحتويات)
