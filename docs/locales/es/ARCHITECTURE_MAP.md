<div align="center">

# 🏛️ Mapeo de Arquitectura y Planos del Sistema D4UC (ARCHITECTURE_MAP.md)

> **Concurrencia Asíncrona sin Pérdidas, Persistencia con 0% Conflictos, Sigilo TLS y Túneles Aislados 1:1**

<br />

| [KR 한국어](../ko/ARCHITECTURE_MAP.md) | [US English](../en/ARCHITECTURE_MAP.md) | [JP 日本語](../ja/ARCHITECTURE_MAP.md) | [CN 简体中文](../zh-CN/ARCHITECTURE_MAP.md) | [ES Español](./ARCHITECTURE_MAP.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/ARCHITECTURE_MAP.md) | [DE Deutsch](../de/ARCHITECTURE_MAP.md) | [RU Русский](../ru/ARCHITECTURE_MAP.md) | [BR Português](../pt-BR/ARCHITECTURE_MAP.md) | [SA العربية](../ar/ARCHITECTURE_MAP.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/ARCHITECTURE_MAP.md">HI हिन्दी</a> • <a href="../id/ARCHITECTURE_MAP.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 19 nov 2026](../../assets/badges/update_badge_es.svg)](./CHANGELOG.md)
[![Architecture: Lossless Multi-Tier](https://img.shields.io/badge/Architecture-Lossless%20Multi--Tier-purple.svg)](./ARCHITECTURE_MAP.md)

</div>

---

<a id="-tabla-de-contenidos"></a>
## 📑 Tabla de Contenidos
1. [1. Arquitectura por Capas](#-1-arquitectura-por-capas)
2. [2. Flujo de Ejecución de Extremo a Extremo](#-2-flujo-de-ejecución-de-extremo-a-extremo)
3. [3. Alta Concurrencia y Prevención de Bloqueos Mutuos](#-3-alta-concurrencia-y-prevención-de-bloqueos-mutuos)
4. [4. Persistencia de Datos y Sincronización SQLite WAL](#-4-persistencia-de-datos-y-sincronización-sqlite-wal)
5. [5. Mecanismos de Seguridad y Aislamiento de Red](#-5-mecanismos-de-seguridad-y-aislamiento-de-red)

---

## 💎 Invariantes Arquitectónicos Clave
- **Concurrencia Asíncrona sin Pérdidas**: Hasta 50 workers paralelos sobre el bucle de eventos `asyncio`.
- **Persistencia con 0% Conflictos**: SQLite WAL con `busy_timeout=5000ms` elimina los bloqueos entre procesos.
- **Sigilo TLS Chrome 131**: `curl_cffi` reproduce exactamente los protocolos de negociación JA3/JA4.
- **Túneles Aislados en Espacio de Usuario**: `wireproxy` enruta el tráfico sin tocar la red del sistema operativo.

---

<a id="-1-arquitectura-por-capas"></a>
## 🏛️ 1. Arquitectura por Capas

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

### Capa 1: Presentación
`src/gui_ko.py` (Coreano), `src/gui_en.py` (Inglés), `src/web_gui.py` (Web GUI Móvil / PWA), `src/run.py` (Terminal Rich CLI).

### Capa 2: Orquestación
Bucle de workers en segundo plano, telemetría en vivo (RPS, Disponibles, 429) y sharding (`2_1`, `2_2`).

### Capa 3: Red y Sigilo TLS
`DiscordApiClient` (`curl_cffi`), huellas TLS Chrome 131 y cabeceras dinámicas.

### Capa 4: Infraestructura de Proxies
`UnifiedProxyManager`, `SurfsharkProxyProvider` (1:1), `FreeProxyProvider` y reemplazo atómico 429 en 0.3s.

### Capa 5: Motores de Generación
Factoría `create_generator()`: Permutación, Híbrido, Diccionario, Máscara, Patrón, Numérico, Combinatorio, Reverificación.

### Capa 6: Almacenamiento y Notificaciones
`StorageManager`, SQLite WAL (`d4uc_results.db`), espejos txt y notificaciones Discord Webhook.


[⬆️ Volver al Índice](#-tabla-de-contenidos)

---

<a id="-2-flujo-de-ejecución-de-extremo-a-extremo"></a>
## 🔄 2. Flujo de Ejecución de Extremo a Extremo

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

[⬆️ Volver al Índice](#-tabla-de-contenidos)

---

<a id="-3-alta-concurrencia-y-prevención-de-bloqueos-mutuos"></a>
## ⚡ 3. Alta Concurrencia y Prevención de Bloqueos Mutuos

- **Non-blocking Concurrency**: All network I/O operations are scheduled on Python's native `asyncio` event loop.
- **429 Atomic Hot-Swap**: When an isolated worker hits Discord's 429 rate limit, its specific Wireproxy local port is seamlessly reassigned to an available server node in under 0.3s without affecting concurrent workers.
- **Zero Lock Deadlock**: SQLite WAL journal mode coupled with Python-level queueing completely eliminates `database is locked` operational exceptions.

[⬆️ Volver al Índice](#-tabla-de-contenidos)

---

<a id="-4-persistencia-de-datos-y-sincronización-sqlite-wal"></a>
## 💾 4. Persistencia de Datos y Sincronización SQLite WAL

- **Primary Database**: `data/d4uc_results.db` configured with `PRAGMA journal_mode = WAL` and `PRAGMA synchronous = NORMAL`.
- **Text File Mirroring**: For maximum legacy compatibility, all newly verified rare handles are concurrently appended to `available.txt` and `checked_history.txt`.

[⬆️ Volver al Índice](#-tabla-de-contenidos)

---

<a id="-5-mecanismos-de-seguridad-y-aislamiento-de-red"></a>
## 🛡️ 5. Mecanismos de Seguridad y Aislamiento de Red

- **Zero-Leak Policy**: All local credentials, WireGuard configuration files, and secrets are strictly excluded from version control.
- **User-Space Network Isolation**: All proxy traffic is terminated in user space (`wireproxy`), preventing interference with system-wide DNS or routing tables.

[⬆️ Volver al Índice](#-tabla-de-contenidos)
