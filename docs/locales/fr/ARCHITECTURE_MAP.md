<div align="center">

# 🏛️ Cartographie d'Architecture et Schémas Système D4UC (ARCHITECTURE_MAP.md)

> **Concurrence Asynchrone Sans Perte, Persistance Sans Conflit, Furtivité TLS et Tunnels Isolés 1:1**

<br />

| [KR 한국어](../ko/ARCHITECTURE_MAP.md) | [US English](../en/ARCHITECTURE_MAP.md) | [JP 日本語](../ja/ARCHITECTURE_MAP.md) | [CN 简体中文](../zh-CN/ARCHITECTURE_MAP.md) | [ES Español](../es/ARCHITECTURE_MAP.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](./ARCHITECTURE_MAP.md) | [DE Deutsch](../de/ARCHITECTURE_MAP.md) | [RU Русский](../ru/ARCHITECTURE_MAP.md) | [BR Português](../pt-BR/ARCHITECTURE_MAP.md) | [SA العربية](../ar/ARCHITECTURE_MAP.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/ARCHITECTURE_MAP.md">HI हिन्दी</a> • <a href="../id/ARCHITECTURE_MAP.md">ID Bahasa Indonesia</a></sub></p>

<br />

[![Last Updated: 19 nov 2026](../../assets/badges/update_badge_fr.svg)](./CHANGELOG.md)
[![Architecture: Lossless Multi-Tier](https://img.shields.io/badge/Architecture-Lossless%20Multi--Tier-purple.svg)](./ARCHITECTURE_MAP.md)

</div>

---

<a id="-table-des-matières"></a>
## 📑 Table des Matières
1. [1. Architecture Système en Couches](#-1-architecture-système-en-couches)
2. [2. Flux d'Exécution de Bout en Bout](#-2-flux-dexécution-de-bout-en-bout)
3. [3. Concurrence à Haut Débit & Prévention des Interblocages](#-3-concurrence-à-haut-débit--prévention-des-interblocages)
4. [4. Persistance des Données & SQLite WAL](#-4-persistance-des-données--sqlite-wal)
5. [5. Sécurité et Mécanismes d'Isolation Réseau](#-5-sécurité-et-mécanismes-disolation-réseau)

---

## 💎 Principes d'Architecture Fondamentaux
- **Concurrence Asynchrone Sans Perte**: Jusqu'à 50 workers parallèles sur la boucle d'événements `asyncio`.
- **Persistance Sans Conflit**: SQLite WAL avec `busy_timeout=5000ms` prévient tout verrouillage inter-processus.
- **Furtivité TLS Chrome 131**: `curl_cffi` réplique rigoureusement les empreintes JA3/JA4.
- **Tunnels Isolés en Espace Utilisateur**: `wireproxy` achemine le trafic sans affecter la configuration réseau de l'hôte.

---

<a id="-1-architecture-système-en-couches"></a>
## 🏛️ 1. Architecture Système en Couches

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

### Couche 1: Présentation
`src/gui_ko.py` (Coréen), `src/gui_en.py` (Anglais), `src/web_gui.py` (Web GUI Tactile / PWA), `src/run.py` (Rich CLI).

### Couche 2: Orchestration
Gestion des workers, métriques télémétriques en direct (RPS, Trouvés, 429) et coordinateur de sharding (`2_1`, `2_2`).

### Couche 3: Réseau & Furtivité TLS
`DiscordApiClient` (`curl_cffi`), simulation de Chrome 131 et en-têtes HTTP de navigateur.

### Couche 4: Infrastructure de Proxys
`UnifiedProxyManager`, `SurfsharkProxyProvider` (1:1), `FreeProxyProvider`, basculement atomique 429 en 0,3s.

### Couche 5: Moteurs de Génération
Factory `create_generator()`: Permutation, Hybride, Dictionnaire, Masque, Motif, Numérique, Combinatoire, Revérification.

### Couche 6: Stockage & Alertes
`StorageManager`, SQLite WAL (`d4uc_results.db`), miroirs fichiers txt et notifications Webhook Discord.


[⬆️ Retour au Sommaire](#-table-des-matières)

---

<a id="-2-flux-dexécution-de-bout-en-bout"></a>
## 🔄 2. Flux d'Exécution de Bout en Bout

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

[⬆️ Retour au Sommaire](#-table-des-matières)

---

<a id="-3-concurrence-à-haut-débit--prévention-des-interblocages"></a>
## ⚡ 3. Concurrence à Haut Débit & Prévention des Interblocages

- **Non-blocking Concurrency**: All network I/O operations are scheduled on Python's native `asyncio` event loop.
- **429 Atomic Hot-Swap**: When an isolated worker hits Discord's 429 rate limit, its specific Wireproxy local port is seamlessly reassigned to an available server node in under 0.3s without affecting concurrent workers.
- **Zero Lock Deadlock**: SQLite WAL journal mode coupled with Python-level queueing completely eliminates `database is locked` operational exceptions.

[⬆️ Retour au Sommaire](#-table-des-matières)

---

<a id="-4-persistance-des-données--sqlite-wal"></a>
## 💾 4. Persistance des Données & SQLite WAL

- **Primary Database**: `data/d4uc_results.db` configured with `PRAGMA journal_mode = WAL` and `PRAGMA synchronous = NORMAL`.
- **Text File Mirroring**: For maximum legacy compatibility, all newly verified rare handles are concurrently appended to `available.txt` and `checked_history.txt`.

[⬆️ Retour au Sommaire](#-table-des-matières)

---

<a id="-5-sécurité-et-mécanismes-disolation-réseau"></a>
## 🛡️ 5. Sécurité et Mécanismes d'Isolation Réseau

- **Zero-Leak Policy**: All local credentials, WireGuard configuration files, and secrets are strictly excluded from version control.
- **User-Space Network Isolation**: All proxy traffic is terminated in user space (`wireproxy`), preventing interference with system-wide DNS or routing tables.

[⬆️ Retour au Sommaire](#-table-des-matières)
