# deploy/scripts/locale_data/architecture.py
"""
1:1 Full Localization for ARCHITECTURE_MAP.md across all 12 locales.
"""

ARCHITECTURE_DATA = {
    "ko": {
        "title": "🏛️ D4UC 아키텍처 매핑 및 시스템 구조도 (ARCHITECTURE_MAP.md)",
        "desc": "무결성 비동기 병렬화, 0% 충돌 영구 동기화, TLS 스텔스 위장 및 1:1 유저스페이스 터널 격리",
        "principles_title": "핵심 설계 원칙",
        "principles": [
            "**무결성 비동기 병렬화**: `asyncio` 이벤트 루프 기반으로 최대 50개 워커가 논블로킹 병렬 처리.",
            "**0% 충돌 영구 동기화**: SQLite WAL(Write-Ahead Logging) 및 `busy_timeout=5000ms`로 다중 프로세스 충돌 방지.",
            "**TLS 스텔스 위장**: `curl_cffi`를 통해 Chrome 131 JA3/JA4 핸드셰이크를 100% 동일하게 재현.",
            "**1:1 유저스페이스 터널 격리**: `wireproxy`를 활용하여 호스트 OS 네트워크 영향 없이 프로세스 격리 라우팅."
        ],
        "sec1_title": "1. 시스템 계층 아키텍처 (Layered Architecture)",
        "sec1_id": "-1-시스템-계층-아키텍처-layered-architecture",
        "sec2_title": "2. 엔드투엔드 처리 흐름 (End-to-End Execution Flow)",
        "sec2_id": "-2-엔드투엔드-처리-흐름-end-to-end-execution-flow",
        "sec3_title": "3. 고처리량 동시성 및 데드락 방지 구조",
        "sec3_id": "-3-고처리량-동시성-및-데드락-방지-구조",
        "sec4_title": "4. 데이터 영속성 및 동기화 (SQLite WAL)",
        "sec4_id": "-4-데이터-영속성-및-동기화-sqlite-wal",
        "sec5_title": "5. 보안 및 네트워크 격리 메커니즘",
        "sec5_id": "-5-보안-및-네트워크-격리-메커니즘",
        "layers": [
            ("Layer 1: 프레젠테이션 계층 (Presentation)", "`src/gui_ko.py` (한글 GUI), `src/gui_en.py` (영문 GUI), `src/web_gui.py` (모바일 Web GUI / PWA), `src/run.py` (헤드리스 Rich CLI)."),
            ("Layer 2: 오케스트레이션 계층 (Orchestration)", "백그라운드 워커 풀 루프, 대시보드 텔레메트리 메트릭스(RPS, 가용, 사용중, 429), 샤딩 분할 제어기(`2_1`, `2_2`)."),
            ("Layer 3: 네트워크 및 TLS 스텔스 위장 (Network & Stealth)", "`DiscordApiClient` (curl_cffi AsyncSession), Chrome 131 TLS 지문 및 완벽한 브라우저 헤더 에뮬레이션."),
            ("Layer 4: 프록시 인프라 및 다중 터널 (Proxy Infrastructure)", "`UnifiedProxyManager`, `SurfsharkProxyProvider` (1:1 Multi-Tunnel), `FreeProxyProvider` (공개 프록시 풀), 429 원자적 핫스왑 큐."),
            ("Layer 5: 후보 닉네임 생성 엔진 (Candidate Generator)", "`create_generator()` 팩토리: 순열(Permutation), 하이브리드, 딕셔너리, 커스텀 마스크, 패턴, 숫자, 조합형, 재검증."),
            ("Layer 6: 스토리지 및 알림 계층 (Storage & Notify)", "`StorageManager` (비동기 큐 워커), SQLite WAL(`d4uc_results.db`), 레거시 txt 미러링(`available.txt`, `taken.txt`), Discord Webhook 푸시.")
        ]
    },
    "en": {
        "title": "🏛️ D4UC Architecture Mapping & System Blueprints (ARCHITECTURE_MAP.md)",
        "desc": "Lossless Async Concurrency, 0% Conflict Persistence, TLS Stealth Impersonation, and 1:1 User-Space Tunnel Isolation",
        "principles_title": "Core Architectural Invariants",
        "principles": [
            "**Lossless Async Concurrency**: Up to 50 concurrent workers running non-blocking operations on `asyncio` event loop.",
            "**0% Conflict Persistence**: SQLite WAL (Write-Ahead Logging) with `busy_timeout=5000ms` eliminates multi-process locking collisions.",
            "**TLS Stealth Impersonation**: `curl_cffi` reproduces exact Chrome 131 JA3/JA4 TLS signatures to bypass Cloudflare / modern WAFs.",
            "**1:1 User-Space Tunnel Isolation**: `wireproxy` routes worker traffic through localized SOCKS5 endpoints without modifying host OS network state."
        ],
        "sec1_title": "1. Layered System Architecture",
        "sec1_id": "-1-layered-system-architecture",
        "sec2_title": "2. End-to-End Execution Flow",
        "sec2_id": "-2-end-to-end-execution-flow",
        "sec3_title": "3. High-Throughput Concurrency & Deadlock Prevention",
        "sec3_id": "-3-high-throughput-concurrency--deadlock-prevention",
        "sec4_title": "4. Data Flow & SQLite WAL Persistence",
        "sec4_id": "-4-data-flow--sqlite-wal-persistence",
        "sec5_title": "5. Security & Network Isolation Blueprints",
        "sec5_id": "-5-security--network-isolation-blueprints",
        "layers": [
            ("Layer 1: Presentation Layer", "`src/gui_ko.py` (Korean GUI), `src/gui_en.py` (English GUI), `src/web_gui.py` (Mobile Touch Web GUI / PWA), `src/run.py` (Headless Rich CLI)."),
            ("Layer 2: Orchestration Layer", "Background worker pool loop, live telemetry metrics (RPS, Available, Taken, 429), and mathematical sharding coordinator (`2_1`, `2_2`)."),
            ("Layer 3: Network & TLS Stealth", "`DiscordApiClient` (`curl_cffi` AsyncSession), Chrome 131 TLS fingerprinting, and dynamic browser header emulation."),
            ("Layer 4: Proxy Infrastructure", "`UnifiedProxyManager`, `SurfsharkProxyProvider` (1:1 Multi-Tunnel), `FreeProxyProvider` (Public Pool), and 0.3s atomic 429 hot-swap engine."),
            ("Layer 5: Candidate Generator Engines", "`create_generator()` factory: Permutation, Hybrid, Dictionary, Custom Mask, Pattern, Numeric, Combinatorial, Recheck."),
            ("Layer 6: Storage & Notification", "`StorageManager` (Async worker), SQLite WAL (`d4uc_results.db`), legacy txt mirroring (`available.txt`, `taken.txt`), Discord Webhook notifier.")
        ]
    },
    "ja": {
        "title": "🏛️ D4UC アーキテクチャマッピングとシステム構造図 (ARCHITECTURE_MAP.md)",
        "desc": "無損失非同期並行処理、0%衝突永続化同期、TLSステルス偽装および1:1ユーザ空間トンネル隔離",
        "principles_title": "コア設計原則",
        "principles": [
            "**無損失非同期並行処理**: `asyncio` イベントループを基盤とし、最大50ワーカがノンブロッキング並行処理を実行。",
            "**0%衝突永続化同期**: SQLite WALおよび `busy_timeout=5000ms` によりマルチプロセス間のデッドロックを完全防止。",
            "**TLSステルス偽装**: `curl_cffi` により Chrome 131 JA3/JA4 ハンドシェイクを完全に再現。",
            "**1:1ユーザ空間トンネル隔離**: `wireproxy` を通じてOSのネットワーク設定に影響を与えず隔離ルーティングを実現。"
        ],
        "sec1_title": "1. システム階層アーキテクチャ (Layered Architecture)",
        "sec1_id": "-1-システム階層アーキテクチャ-layered-architecture",
        "sec2_title": "2. エンドツーエンド実行フロー (End-to-End Execution Flow)",
        "sec2_id": "-2-エンドツーエンド実行フロー-end-to-end-execution-flow",
        "sec3_title": "3. 高スループット並行処理とデッドロック防止構造",
        "sec3_id": "-3-高スループット並行処理とデッドロック防止構造",
        "sec4_title": "4. データ永続化および同期 (SQLite WAL)",
        "sec4_id": "-4-データ永続化および同期-sqlite-wal",
        "sec5_title": "5. セキュリティとネットワーク隔離機構",
        "sec5_id": "-5-セキュリティとネットワーク隔離機構",
        "layers": [
            ("Layer 1: プレゼンテーション層 (Presentation)", "`src/gui_ko.py` (韓国語GUI), `src/gui_en.py` (英語GUI), `src/web_gui.py` (モバイルWeb GUI / PWA), `src/run.py` (Rich CLI)。"),
            ("Layer 2: オーケストレーション層 (Orchestration)", "バックグラウンドワーカループ、リアルタイムテレメトリ（RPS、発見数、使用中、429）、シャーディング調整器。"),
            ("Layer 3: ネットワークおよびTLSステルス偽装 (Network & Stealth)", "`DiscordApiClient` (curl_cffi AsyncSession), Chrome 131 TLS 指紋および完全なブラウザヘッダー模倣。"),
            ("Layer 4: プロキシ基盤および複数トンネル (Proxy Infrastructure)", "`UnifiedProxyManager`, `SurfsharkProxyProvider` (1:1 Multi-Tunnel), `FreeProxyProvider`, 0.3秒ホットスワップ。"),
            ("Layer 5: 候補生成エンジン (Candidate Generator)", "`create_generator()`: 順列、ハイブリッド、辞書、カスタムマスク、パターン、数字、組合せ、再検証。"),
            ("Layer 6: ストレージおよび通知層 (Storage & Notify)", "`StorageManager`, SQLite WAL (`d4uc_results.db`), レガシーtxt同期 (`available.txt`, `taken.txt`), Discord Webhook。")
        ]
    },
    "zh-CN": {
        "title": "🏛️ D4UC 架构映射与系统结构图 (ARCHITECTURE_MAP.md)",
        "desc": "无损异步高并发、0% 冲突持久化同步、TLS 隐形伪装与 1:1 用户空间网络隧道隔离",
        "principles_title": "核心设计原则",
        "principles": [
            "**无损异步高并发**: 基于 `asyncio` 事件循环调度，支持高达 50 个工作线程进行无阻塞并行检测。",
            "**0% 冲突持久化同步**: 采用 SQLite WAL 模式与 `busy_timeout=5000ms` 彻底消除多进程读写锁竞争。",
            "**TLS 隐形指纹伪装**: 借助 `curl_cffi` 完整还原 Chrome 131 JA3/JA4 握手特征，绕过各类 WAF 识别。",
            "**1:1 用户空间隧道隔离**: 通过 `wireproxy` 在用户态实现独立的本地代理网关，完全不干扰宿主机的网络环境。"
        ],
        "sec1_title": "1. 系统分层架构 (Layered Architecture)",
        "sec1_id": "-1-系统分层架构-layered-architecture",
        "sec2_title": "2. 端到端执行流程 (End-to-End Execution Flow)",
        "sec2_id": "-2-端到端执行流程-end-to-end-execution-flow",
        "sec3_title": "3. 高吞吐并发与防死锁设计",
        "sec3_id": "-3-高吞吐并发与防死锁设计",
        "sec4_title": "4. 数据持久化与多进程同步 (SQLite WAL)",
        "sec4_id": "-4-数据持久化与多进程同步-sqlite-wal",
        "sec5_title": "5. 安全防护与网络隔离机制",
        "sec5_id": "-5-安全防护与网络隔离机制",
        "layers": [
            ("Layer 1: 表现层 (Presentation Layer)", "`src/gui_ko.py` (韩文界面), `src/gui_en.py` (英文界面), `src/web_gui.py` (移动端 Web GUI / PWA), `src/run.py` (无头 Rich CLI)。"),
            ("Layer 2: 编排调度层 (Orchestration Layer)", "后台工作线程池循环、实时指标遥测系统（RPS、可用、已占用、429）与数学分片协调器（`2_1`, `2_2`）。"),
            ("Layer 3: 网络通信与 TLS 隐形层 (Network & Stealth)", "`DiscordApiClient` (`curl_cffi` AsyncSession)，Chrome 131 TLS 指纹仿真与浏览器标头伪装。"),
            ("Layer 4: 代理基础设施与多隧道池 (Proxy Infrastructure)", "`UnifiedProxyManager`，`SurfsharkProxyProvider` (1:1 多隧道)，`FreeProxyProvider` (公开池)，0.3 秒原子热切换。"),
            ("Layer 5: 候选用户名生成引擎 (Candidate Generator)", "`create_generator()` 工厂：排列、混合、字典、自定义掩码、模式、纯数字、组合式与复检引擎。"),
            ("Layer 6: 存储持久化与通知层 (Storage & Notify)", "`StorageManager`，SQLite WAL (`d4uc_results.db`)，文本文件实时镜像与 Discord Webhook 推送。")
        ]
    },
    "es": {
        "title": "🏛️ Mapeo de Arquitectura y Planos del Sistema D4UC (ARCHITECTURE_MAP.md)",
        "desc": "Concurrencia Asíncrona sin Pérdidas, Persistencia con 0% Conflictos, Sigilo TLS y Túneles Aislados 1:1",
        "principles_title": "Invariantes Arquitectónicos Clave",
        "principles": [
            "**Concurrencia Asíncrona sin Pérdidas**: Hasta 50 workers paralelos sobre el bucle de eventos `asyncio`.",
            "**Persistencia con 0% Conflictos**: SQLite WAL con `busy_timeout=5000ms` elimina los bloqueos entre procesos.",
            "**Sigilo TLS Chrome 131**: `curl_cffi` reproduce exactamente los protocolos de negociación JA3/JA4.",
            "**Túneles Aislados en Espacio de Usuario**: `wireproxy` enruta el tráfico sin tocar la red del sistema operativo."
        ],
        "sec1_title": "1. Arquitectura por Capas",
        "sec1_id": "-1-arquitectura-por-capas",
        "sec2_title": "2. Flujo de Ejecución de Extremo a Extremo",
        "sec2_id": "-2-flujo-de-ejecución-de-extremo-a-extremo",
        "sec3_title": "3. Alta Concurrencia y Prevención de Bloqueos Mutuos",
        "sec3_id": "-3-alta-concurrencia-y-prevención-de-bloqueos-mutuos",
        "sec4_title": "4. Persistencia de Datos y Sincronización SQLite WAL",
        "sec4_id": "-4-persistencia-de-datos-y-sincronización-sqlite-wal",
        "sec5_title": "5. Mecanismos de Seguridad y Aislamiento de Red",
        "sec5_id": "-5-mecanismos-de-seguridad-y-aislamiento-de-red",
        "layers": [
            ("Capa 1: Presentación", "`src/gui_ko.py` (Coreano), `src/gui_en.py` (Inglés), `src/web_gui.py` (Web GUI Móvil / PWA), `src/run.py` (Terminal Rich CLI)."),
            ("Capa 2: Orquestación", "Bucle de workers en segundo plano, telemetría en vivo (RPS, Disponibles, 429) y sharding (`2_1`, `2_2`)."),
            ("Capa 3: Red y Sigilo TLS", "`DiscordApiClient` (`curl_cffi`), huellas TLS Chrome 131 y cabeceras dinámicas."),
            ("Capa 4: Infraestructura de Proxies", "`UnifiedProxyManager`, `SurfsharkProxyProvider` (1:1), `FreeProxyProvider` y reemplazo atómico 429 en 0.3s."),
            ("Capa 5: Motores de Generación", "Factoría `create_generator()`: Permutación, Híbrido, Diccionario, Máscara, Patrón, Numérico, Combinatorio, Reverificación."),
            ("Capa 6: Almacenamiento y Notificaciones", "`StorageManager`, SQLite WAL (`d4uc_results.db`), espejos txt y notificaciones Discord Webhook.")
        ]
    },
    "fr": {
        "title": "🏛️ Cartographie d'Architecture et Schémas Système D4UC (ARCHITECTURE_MAP.md)",
        "desc": "Concurrence Asynchrone Sans Perte, Persistance Sans Conflit, Furtivité TLS et Tunnels Isolés 1:1",
        "principles_title": "Principes d'Architecture Fondamentaux",
        "principles": [
            "**Concurrence Asynchrone Sans Perte**: Jusqu'à 50 workers parallèles sur la boucle d'événements `asyncio`.",
            "**Persistance Sans Conflit**: SQLite WAL avec `busy_timeout=5000ms` prévient tout verrouillage inter-processus.",
            "**Furtivité TLS Chrome 131**: `curl_cffi` réplique rigoureusement les empreintes JA3/JA4.",
            "**Tunnels Isolés en Espace Utilisateur**: `wireproxy` achemine le trafic sans affecter la configuration réseau de l'hôte."
        ],
        "sec1_title": "1. Architecture Système en Couches",
        "sec1_id": "-1-architecture-système-en-couches",
        "sec2_title": "2. Flux d'Exécution de Bout en Bout",
        "sec2_id": "-2-flux-dexécution-de-bout-en-bout",
        "sec3_title": "3. Concurrence à Haut Débit & Prévention des Interblocages",
        "sec3_id": "-3-concurrence-à-haut-débit--prévention-des-interblocages",
        "sec4_title": "4. Persistance des Données & SQLite WAL",
        "sec4_id": "-4-persistance-des-données--sqlite-wal",
        "sec5_title": "5. Sécurité et Mécanismes d'Isolation Réseau",
        "sec5_id": "-5-sécurité-et-mécanismes-disolation-réseau",
        "layers": [
            ("Couche 1: Présentation", "`src/gui_ko.py` (Coréen), `src/gui_en.py` (Anglais), `src/web_gui.py` (Web GUI Tactile / PWA), `src/run.py` (Rich CLI)."),
            ("Couche 2: Orchestration", "Gestion des workers, métriques télémétriques en direct (RPS, Trouvés, 429) et coordinateur de sharding (`2_1`, `2_2`)."),
            ("Couche 3: Réseau & Furtivité TLS", "`DiscordApiClient` (`curl_cffi`), simulation de Chrome 131 et en-têtes HTTP de navigateur."),
            ("Couche 4: Infrastructure de Proxys", "`UnifiedProxyManager`, `SurfsharkProxyProvider` (1:1), `FreeProxyProvider`, basculement atomique 429 en 0,3s."),
            ("Couche 5: Moteurs de Génération", "Factory `create_generator()`: Permutation, Hybride, Dictionnaire, Masque, Motif, Numérique, Combinatoire, Revérification."),
            ("Couche 6: Stockage & Alertes", "`StorageManager`, SQLite WAL (`d4uc_results.db`), miroirs fichiers txt et notifications Webhook Discord.")
        ]
    },
    "de": {
        "title": "🏛️ D4UC Architektur-Mapping & Systemübersicht (ARCHITECTURE_MAP.md)",
        "desc": "Verlustfreie asynchrone Nebenläufigkeit, konfliktfreie SQLite-Persistenz, TLS-Tarnung & 1:1 isolierte Tunnel",
        "principles_title": "Architektonische Kernprinzipien",
        "principles": [
            "**Verlustfreie asynchrone Nebenläufigkeit**: Bis zu 50 parallele Worker auf der `asyncio`-Ereignisschleife.",
            "**Konfliktfreie SQLite-Persistenz**: SQLite WAL mit `busy_timeout=5000ms` schließt Deadlocks aus.",
            "**Chrome 131 TLS-Tarnung**: `curl_cffi` bildet die JA3/JA4-Fingerabdrücke exakt nach.",
            "**1:1 isolierte Tunnel**: `wireproxy` routet Worker-Traffic im User-Space ohne Eingriff in die Host-Netzwerkkarten."
        ],
        "sec1_title": "1. Schichtenarchitektur des Systems",
        "sec1_id": "-1-schichtenarchitektur-des-systems",
        "sec2_title": "2. End-to-End-Ausführungsfluss",
        "sec2_id": "-2-end-to-end-ausführungsfluss",
        "sec3_title": "3. Hochdurchsatz-Parallelität & Deadlock-Prävention",
        "sec3_id": "-3-hochdurchsatz-parallelität--deadlock-prävention",
        "sec4_title": "4. Datenfluss & SQLite WAL-Persistenz",
        "sec4_id": "-4-datenfluss--sqlite-wal-persistenz",
        "sec5_title": "5. Sicherheits- & Netzwerk-Isolationskonzepte",
        "sec5_id": "-5-sicherheits--netzwerk-isolationskonzepte",
        "layers": [
            ("Schicht 1: Präsentation", "`src/gui_ko.py` (Koreanisch), `src/gui_en.py` (Englisch), `src/web_gui.py` (Mobiles Web GUI / PWA), `src/run.py` (Terminal Rich CLI)."),
            ("Schicht 2: Orchestrierung", "Hintergrund-Worker-Schleife, Live-Telemetrie (RPS, Verfügbar, 429) und Sharding-Koordinator (`2_1`, `2_2`)."),
            ("Schicht 3: Netzwerk & TLS-Tarnung", "`DiscordApiClient` (`curl_cffi`), Chrome 131 TLS-Signaturen und Header-Emulation."),
            ("Schicht 4: Proxy-Infrastruktur", "`UnifiedProxyManager`, `SurfsharkProxyProvider` (1:1), `FreeProxyProvider`, atomarer 429 Hot-Swap in 0,3s."),
            ("Schicht 5: Generierungs-Engines", "`create_generator()` Factory: Permutation, Hybrid, Wörterbuch, Maske, Muster, Numerisch, Kombinatorisch, Nachprüfung."),
            ("Schicht 6: Speicherung & Benachrichtigung", "`StorageManager`, SQLite WAL (`d4uc_results.db`), TXT-Dateispiegelung und Discord-Webhook-Push.")
        ]
    },
    "ru": {
        "title": "🏛️ Архитектурная карта и схема системы D4UC (ARCHITECTURE_MAP.md)",
        "desc": "Асинхронный параллелизм без потерь, бесконфликтная синхронизация, стелс-TLS и изоляция 1:1",
        "principles_title": "Ключевые принципы архитектуры",
        "principles": [
            "**Асинхронный параллелизм без потерь**: До 50 воркеров на цикле событий `asyncio` без блокировок.",
            "**Бесконфликтная синхронизация**: SQLite WAL с `busy_timeout=5000ms` предотвращает взаимные блокировки.",
            "**Стелс-маскировка TLS Chrome 131**: `curl_cffi` точно воспроизводит отпечатки JA3/JA4.",
            "**Изоляция туннелей в пространстве пользователя**: `wireproxy` маршрутизирует трафик без вмешательства в сеть ОС."
        ],
        "sec1_title": "1. Многоуровневая архитектура системы",
        "sec1_id": "-1-многоуровневая-архитектура-системы",
        "sec2_title": "2. Сквозной рабочий процесс (End-to-End)",
        "sec2_id": "-2-сквозной-рабочий-процесс-end-to-end",
        "sec3_title": "3. Высокопроизводительный параллелизм и защита от взаимных блокировок",
        "sec3_id": "-3-высокопроизводительный-параллелизм-и-защита-от-взаимных-блокировок",
        "sec4_title": "4. Потоки данных и сохранение в SQLite WAL",
        "sec4_id": "-4-потоки-данных-и-сохранение-в-sqlite-wal",
        "sec5_title": "5. Архитектура безопасности и сетевой изоляции",
        "sec5_id": "-5-архитектура-безопасности-и-сетевой-изоляции",
        "layers": [
            ("Уровень 1: Представление", "`src/gui_ko.py` (Корейский), `src/gui_en.py` (Английский), `src/web_gui.py` (Мобильный Web GUI / PWA), `src/run.py` (Rich CLI)."),
            ("Уровень 2: Оркестрация", "Пул фоновых воркеров, телеметрия в реальном времени (RPS, Доступно, 429) и координатор шардинга (`2_1`, `2_2`)."),
            ("Уровень 3: Сеть и стелс-TLS", "`DiscordApiClient` (`curl_cffi`), отпечатки Chrome 131 и эмуляция заголовков браузера."),
            ("Уровень 4: Инфраструктура прокси", "`UnifiedProxyManager`, `SurfsharkProxyProvider` (1:1), `FreeProxyProvider`, горячая замена при 429 за 0.3с."),
            ("Уровень 5: Генераторы имен", "Фабрика `create_generator()`: Перестановки, Гибридный, Словарь, Маска, Шаблон, Числовой, Комбинаторный, Перепроверка."),
            ("Уровень 6: Хранилище и оповещения", "`StorageManager`, SQLite WAL (`d4uc_results.db`), зеркалирование в txt и Discord Webhook.")
        ]
    },
    "pt-BR": {
        "title": "🏛️ Mapeamento de Arquitetura e Diagramas D4UC (ARCHITECTURE_MAP.md)",
        "desc": "Concorrência Assíncrona Sem Perdas, Persistência Sem Conflitos, Camuflagem TLS e Túneis Isolados 1:1",
        "principles_title": "Princípios Fundamentais de Projeto",
        "principles": [
            "**Concorrência Assíncrona Sem Perdas**: Até 50 workers paralelos sem bloqueio no loop `asyncio`.",
            "**Persistência Sem Conflitos**: SQLite WAL com `busy_timeout=5000ms` impede impasses (deadlocks).",
            "**Camuflagem TLS Chrome 131**: `curl_cffi` reproduz com precisão os apertos de mão JA3/JA4.",
            "**Túneis Isolados em Espaço de Usuário**: `wireproxy` roteia dados sem alterar as configurações de rede do host."
        ],
        "sec1_title": "1. Arquitetura do Sistema em Camadas",
        "sec1_id": "-1-arquitetura-do-sistema-em-camadas",
        "sec2_title": "2. Fluxo de Execução Ponta a Ponta",
        "sec2_id": "-2-fluxo-de-execução-ponta-a-ponta",
        "sec3_title": "3. Alta Concorrência e Prevenção de Deadlocks",
        "sec3_id": "-3-alta-concorrência-e-prevenção-de-deadlocks",
        "sec4_title": "4. Fluxo de Dados e Persistência SQLite WAL",
        "sec4_id": "-4-fluxo-de-dados-e-persistência-sqlite-wal",
        "sec5_title": "5. Segurança e Isolamento de Rede",
        "sec5_id": "-5-segurança-e-isolamento-de-rede",
        "layers": [
            ("Camada 1: Apresentação", "`src/gui_ko.py` (Coreano), `src/gui_en.py` (Inglês), `src/web_gui.py` (Web GUI Móvel / PWA), `src/run.py` (Terminal Rich CLI)."),
            ("Camada 2: Orquestração", "Loop de workers em segundo plano, telemetria em tempo real (RPS, Disponíveis, 429) e sharding (`2_1`, `2_2`)."),
            ("Camada 3: Rede & Furtividade TLS", "`DiscordApiClient` (`curl_cffi`), assinaturas TLS Chrome 131 e cabeçalhos emulados."),
            ("Camada 4: Infraestrutura de Proxies", "`UnifiedProxyManager`, `SurfsharkProxyProvider` (1:1), `FreeProxyProvider` e hot-swap 429 em 0,3s."),
            ("Camada 5: Motores de Geração", "Fábrica `create_generator()`: Permutação, Híbrido, Dicionário, Máscara, Padrão, Numérico, Combinatório, Rechecagem."),
            ("Camada 6: Armazenamento & Notificações", "`StorageManager`, SQLite WAL (`d4uc_results.db`), espelhos txt e alertas via Discord Webhook.")
        ]
    },
    "ar": {
        "title": "🏛️ مخطط الهيكلية الهندسية وتصميم النظام D4UC (ARCHITECTURE_MAP.md)",
        "desc": "تزامن غير متزامن بدون فقدان، وتخزين بيانات بلا تعارض، ومحاكاة TLS الخفية وعزل الأنفاق بنسبة 1:1",
        "principles_title": "المبادئ الهندسية الأساسية",
        "principles": [
            "**تزامن غير متزامن بدون فقدان**: تشغيل ما يصل إلى 50 عاملاً متزامناً بالاعتماد على حلقة أحداث `asyncio` دون أي حظر للمهام.",
            "**تخزين بيانات بلا تعارض بنسبة 0%**: وضع SQLite WAL مع مهلة `busy_timeout=5000ms` لمنع تصادم العمليات المتعددة نهائياً.",
            "**محاكاة بصمة TLS الخفية**: استخدام `curl_cffi` لإعادة إنتاج بصمات Chrome 131 JA3/JA4 بالكامل لتخطي أنظمة الحماية.",
            "**عزل الأنفاق بنسبة 1:1 في مساحة المستخدم**: استخدام `wireproxy` لتوجيه الاتصالات محلياً دون أي تأثير على شبكة نظام التشغيل."
        ],
        "sec1_title": "1. الهيكلية المعمارية متعددة الطبقات",
        "sec1_id": "-1-الهيكلية-المعمارية-متعددة-الطبقات",
        "sec2_title": "2. مسار التنفيذ الشامل (End-to-End)",
        "sec2_id": "-2-مسار-التنفيذ-الشامل-end-to-end",
        "sec3_title": "3. التزامن عالي الإنتاجية وتفادي الاختناقات البرمجية",
        "sec3_id": "-3-التزامن-عالي-الإنتاجية-وتفادي-الاختناقات-البرمجية",
        "sec4_title": "4. تدفق البيانات والتخزين الدائم في SQLite WAL",
        "sec4_id": "-4-تدفق-البيانات-والتخزين-الدائم-في-sqlite-wal",
        "sec5_title": "5. آليات الأمان والعزل الشبكي",
        "sec5_id": "-5-آليات-الأمان-والعزل-الشبكي",
        "layers": [
            ("الطبقة 1: طبقة العرض والواجهة", "`src/gui_ko.py` (كوري)، `src/gui_en.py` (إنجليزي)، `src/web_gui.py` (واجهة الويب للموبايل / PWA)، `src/run.py` (سطر الأوامر Rich CLI)."),
            ("الطبقة 2: طبقة التنسيق والإدارة", "حلقة إدارة العمال في الخلفية، مقاييس الأداء الفورية (RPS، المتاح، المستخدم، 429)، ومقسم النطاقات (`2_1`، `2_2`)."),
            ("الطبقة 3: الشبكة والتمويه TLS", "`DiscordApiClient` عبر `curl_cffi`، محاكاة بصمات Chrome 131 TLS وترويسات المتصفح الكاملة."),
            ("الطبقة 4: بنية البروكسي والأنفاق المتعددة", "`UnifiedProxyManager`، موفر Surfshark بنسبة 1:1، وموفر البروكسيات المجانية، والتبديل السريع عند 429 في 0.3 ثانية."),
            ("الطبقة 5: محركات توليد أسماء المستخدمين", "مصنع `create_generator()`: التباديل، الهجين، القاموس، الأقنعة المخصصة، الأنماط، الأرقام، التوافيق، وإعادة الفحص."),
            ("الطبقة 6: التخزين والإشعارات", "`StorageManager`، قاعدة بيانات SQLite WAL (`d4uc_results.db`)، ملفات txt النصية، وتنبيهات Discord Webhook.")
        ]
    },
    "hi": {
        "title": "🏛️ D4UC आर्किटेक्चर मैपिंग और सिस्टम ब्लूप्रिंट (ARCHITECTURE_MAP.md)",
        "desc": "शून्य-हानि अतुल्यकालिक संगामिति, 0% टकराव डेटाबेस सिंक, TLS स्टेल्थ प्रतिरूपण और 1:1 आइसोलेटेड टनलिंग",
        "principles_title": "मुख्य वास्तुशिल्प सिद्धांत",
        "principles": [
            "**शून्य-हानि अतुल्यकालिक संगामिति**: `asyncio` इवेंट लूप पर अधिकतम 50 समवर्ती कार्यकर्ताओं द्वारा गैर-अवरोधक समानांतर निष्पादन।",
            "**0% टकराव दृढ़ता**: `busy_timeout=5000ms` के साथ SQLite WAL बहु-प्रक्रिया लॉक टकराव को पूरी तरह से समाप्त करता है।",
            "**Chrome 131 TLS स्टेल्थ**: `curl_cffi` द्वारा Chrome 131 JA3/JA4 फिंगरप्रिंट का सटीक पुनरुत्पादन।",
            "**1:1 यूजर-स्पेस टनल अलगाव**: `wireproxy` होस्ट ऑपरेटिंग सिस्टम की नेटवर्क सेटिंग्स को बदले बिना सुरक्षित रूटिंग प्रदान करता है।"
        ],
        "sec1_title": "1. स्तरित सिस्टम आर्किटेक्चर (Layered Architecture)",
        "sec1_id": "-1-स्तरित-सिस्टम-आर्किटेक्चर-layered-architecture",
        "sec2_title": "2. एंड-टू-एंड निष्पादन प्रवाह (End-to-End Execution Flow)",
        "sec2_id": "-2-एंड-टू-एंड-निष्पादन-प्रवाह-end-to-end-execution-flow",
        "sec3_title": "3. उच्च-थ्रूपुट समवर्तीता और डेडलॉक रोकथाम संरचना",
        "sec3_id": "-3-उच्च-थ्रूपुट-समवर्तीता-और-डेडलॉक-रोकथाम-संरचना",
        "sec4_title": "4. डेटा प्रवाह और SQLite WAL दृढ़ता",
        "sec4_id": "-4-डेटा-प्रवाह-और-sqlite-wal-दृढ़ता",
        "sec5_title": "5. सुरक्षा और नेटवर्क अलगाव तंत्र",
        "sec5_id": "-5-सुरक्षा-और-नेटवर्क-अलगाव-तंत्र",
        "layers": [
            ("स्तर 1: प्रस्तुति स्तर (Presentation)", "`src/gui_ko.py` (कोरियाई), `src/gui_en.py` (अंग्रेजी), `src/web_gui.py` (मोबाइल Web GUI / PWA), `src/run.py` (Rich CLI)।"),
            ("स्तर 2: ऑर्केस्ट्रेशन स्तर (Orchestration)", "बैकग्राउंड वर्कर पूल लूप, रीयल-टाइम टेलीमेट्री मेट्रिक्स (RPS, उपलब्ध, 429), और शार्डिंग कोऑर्डिनेटर (`2_1`, `2_2`)।"),
            ("स्तर 3: नेटवर्क और TLS स्टेल्थ", "`DiscordApiClient` (`curl_cffi` AsyncSession), Chrome 131 TLS फिंगरप्रिंटिंग और ब्राउज़र हेडर अनुकरण।"),
            ("स्तर 4: प्रॉक्सी इंफ्रास्ट्रक्चर", "`UnifiedProxyManager`, `SurfsharkProxyProvider` (1:1), `FreeProxyProvider`, और 0.3s में 429 हॉट-स्वैप।"),
            ("स्तर 5: जनरेशन इंजन (Candidate Generator)", "`create_generator()` फैक्ट्री: क्रमपरिवर्तन, हाइब्रिड, शब्दकोश, मास्क, पैटर्न, संख्यात्मक, संयोजन, पुनर्परीक्षण।"),
            ("स्तर 6: संग्रहण और सूचनाएं", "`StorageManager`, SQLite WAL (`d4uc_results.db`), txt फ़ाइल मिररिंग और Discord Webhook सूचनाएं।")
        ]
    },
    "id": {
        "title": "🏛️ Pemetaan Arsitektur & Cetak Biru Sistem D4UC (ARCHITECTURE_MAP.md)",
        "desc": "Konkurensi Asinkron Tanpa Rugi, Persistensi 0% Konflik, Penyamaran TLS, dan Isolasi Terowongan 1:1",
        "principles_title": "Prinsip Utama Arsitektur",
        "principles": [
            "**Konkurensi Asinkron Tanpa Rugi**: Hingga 50 worker paralel tanpa pemblokiran pada event loop `asyncio`.",
            "**Persistensi 0% Konflik**: SQLite WAL dengan `busy_timeout=5000ms` menghilangkan kebuntuan antar-proses (deadlock).",
            "**Penyamaran TLS Chrome 131**: `curl_cffi` mereplikasi jabat tangan JA3/JA4 secara presisi untuk melewati WAF.",
            "**Isolasi Terowongan 1:1 Ruang Pengguna**: `wireproxy` merutekan lalu lintas jaringan tanpa mengubah konfigurasi OS host."
        ],
        "sec1_title": "1. Arsitektur Sistem Berlapis (Layered Architecture)",
        "sec1_id": "-1-arsitektur-sistem-berlapis-layered-architecture",
        "sec2_title": "2. Alur Eksekusi Ujung-ke-Ujung (End-to-End Execution Flow)",
        "sec2_id": "-2-alur-eksekusi-ujung-ke-ujung-end-to-end-execution-flow",
        "sec3_title": "3. Konkurensi Throughput Tinggi & Pencegahan Kebuntuan",
        "sec3_id": "-3-konkurensi-throughput-tinggi--pencegahan-kebuntuan",
        "sec4_title": "4. Aliran Data & Persistensi SQLite WAL",
        "sec4_id": "-4-aliran-data--persistensi-sqlite-wal",
        "sec5_title": "5. Arsitektur Keamanan dan Isolasi Jaringan",
        "sec5_id": "-5-arsitektur-keamanan-dan-isolasi-jaringan",
        "layers": [
            ("Lapisan 1: Presentasi", "`src/gui_ko.py` (Bahasa Korea), `src/gui_en.py` (Bahasa Inggris), `src/web_gui.py` (Web GUI Sentuh / PWA), `src/run.py` (Terminal Rich CLI)."),
            ("Lapisan 2: Orkestrasi", "Loop worker latar belakang, telemetri langsung (RPS, Tersedia, 429), dan koordinator sharding (`2_1`, `2_2`)."),
            ("Lapisan 3: Jaringan & Siluman TLS", "`DiscordApiClient` (`curl_cffi`), sidik jari TLS Chrome 131, dan peniruan header peramban."),
            ("Lapisan 4: Infrastruktur Proxy", "`UnifiedProxyManager`, `SurfsharkProxyProvider` (1:1), `FreeProxyProvider`, dan hot-swap 429 atomik dalam 0,3 detik."),
            ("Lapisan 5: Mesin Pembuat Kandidat", "Factory `create_generator()`: Permutasi, Hibrida, Kamus, Masking, Pola, Numerik, Kombinatorial, Verifikasi Ulang."),
            ("Lapisan 6: Penyimpanan & Notifikasi", "`StorageManager`, SQLite WAL (`d4uc_results.db`), pencerminan berkas txt, dan webhook Discord.")
        ]
    }
}
