# deploy/scripts/locale_data/tasks.py
"""
1:1 Full Localization for TASKS.md across all 12 locales.
"""

TASKS_DATA = {
    "ko": {
        "title": "📋 D4UC 통합 작업 인덱스 및 개발 백로그 (TASKS.md)",
        "desc": "버전별 마일스톤 달성 내역, 시스템 배포 자산 현황 및 개발 작업 관리",
        "sec1_title": "1. 마일스톤 완료 내역 (Completed Milestones)",
        "sec1_id": "-1-마일스톤-완료-내역-completed-milestones",
        "milestones_header": "| 버전 | 마일스톤 명칭 | 주요 달성 내용 및 기술적 성과 | 상태 |\n| :---: | :--- | :--- | :---: |",
        "milestones": [
            ("v1~v3", "비동기 코어 및 SQLite 구축", "`curl_cffi` 기반 Chrome 131 TLS 스텔스 위장, SQLite 결과 저장, 레거시 txt 동시 미러링", "✅ 완료"),
            ("v4~v5", "8대 닉네임 생성 엔진 완성", "순열, 하이브리드, 딕셔너리, 패턴, 숫자, 커스텀 마스크, 조합형, 재검증 엔진 완성", "✅ 완료"),
            ("v6~v7", "서프샤크 1:1 다중 터널 풀", "Wireproxy 유저스페이스 터널링 연동, 최대 50워커 동시 가동, 142개 글로벌 클러스터 매핑", "✅ 완료"),
            ("v8", "429 무중단 원자적 핫스왑", "특정 워커 429 감지 시 해당 터널만 0.3초 내 타 국가로 교체, 타 워커 중단 0% 달성", "✅ 완료"),
            ("v9", "다중 창 분할 샤딩 및 DB 동기화", "수학적 2~4분할 샤딩(`2_1`, `2_2` 등), SQLite WAL 멀티프로세스 실시간 새로고침 팝업", "✅ 완료"),
            ("v10", "GUI/UX 온보딩 및 성능 고도화", "상단 온보딩 가이드 배너, 전 컨트롤 툴팁 적용, 30ms 로그 디바운스 배치 큐 (60 FPS 보증)", "✅ 완료"),
            ("v11", "모바일 Termux 및 도커 배포", "안드로이드 `proot-distro debian` 원클릭 스크립트, Multi-Arch ARM64/AMD64 Dockerfile", "✅ 완료"),
            ("v12.0", "크로스 플랫폼 프로덕션 릴리스", "Windows 4종 독립 EXE, macOS/Linux 원클릭 스크립트, 안전 배포 수칙 수립", "✅ 완료"),
            ("v12.1", "깃허브 안전 배포 & 바이브 코딩", "철통 `.gitignore`, 더미 템플릿(`.env.example`), 시크릿 하드코딩 영구 제거", "✅ 완료"),
            ("v12.2", "모바일 터치 Web GUI & PWA", "모바일 브라우저 전용 반응형 Web UI, 서비스워커 PWA, 0.1s Webhook 푸시", "✅ 완료"),
            ("v12.3", "무료 프록시 자동 수집 & APK", "18개 공개 소스 실시간 수집 및 Cloudflare 검증, 단독 서명 안드로이드 APK 빌드", "✅ 완료"),
            ("v12.4", "양방향 내비게이션 & OS 가이드", "전 문서 상호 점프 목차/상단 복귀 링크, 13종 OS별 완벽 가이드 구축", "✅ 완료"),
            ("v12.5", "12개국어 1:1 전수 현지화 & 루트 정돈", "8종 핵심 문서 12개국어 1:1 번역, 깃허브 루트 구조화 및 UX 최적화", "✅ 완료")
        ],
        "sec2_title": "2. 현재 배포 자산 상태 (Current System Assets)",
        "sec2_id": "-2-현재-배포-자산-상태-current-system-assets",
        "sec2_items": [
            "**데스크톱 실행 (GUI / CLI)**: `python src/gui_ko.py` (한국어) / `python src/gui_en.py` (영어) / `python src/run.py` (Rich CLI) / 4종 단독 배포 EXE (`dist/`)",
            "**모바일 Web GUI & 안드로이드 APK**: 포트 5000 반응형 터치 웹 / PWA 오프라인 캐시 / `DiscordUsernameChecker_v12.3.0.apk`",
            "**도커 및 리눅스 컨테이너**: `deploy/Dockerfile` (Multi-Arch Python 3.12 slim), `deploy/docker-compose.yml` (2-샤드 가속 프로파일)",
            "**12개국어 문서 허브**: `README.md` 및 `docs/locales/<lang>/` (12개 언어 1:1 완전 매칭)"
        ],
        "sec3_title": "3. 품질 보증 및 아키텍처 불변식",
        "sec3_id": "-3-품질-보증-및-아키텍처-불변식",
        "sec3_items": [
            "**시크릿 누출 0% 불변식**: 실제 WireGuard 키, 계정 비밀번호, 로컬 절대경로의 깃허브 업로드 영구 원천 차단.",
            "**기계적 무결성 100% 검증**: 단위 테스트 103건 및 13개 검증 단계 전부 종료 코드 0 (`exit 0`) 통과 필수.",
            "**양방향 내비게이션 보증**: 모든 문서의 목차 앵커 및 상단 이동 링크 100% 동작 (깨진 링크 0건)."
        ]
    },
    "en": {
        "title": "📋 D4UC Task Index & Development Backlog (TASKS.md)",
        "desc": "Version Milestone History, System Deployment Assets, and Development Task Backlog",
        "sec1_title": "1. Completed Milestones",
        "sec1_id": "-1-completed-milestones",
        "milestones_header": "| Version | Milestone Title | Key Accomplishments & Technical Achievements | Status |\n| :---: | :--- | :--- | :---: |",
        "milestones": [
            ("v1~v3", "Async Core & SQLite Architecture", "`curl_cffi` Chrome 131 TLS stealth, SQLite results persistence, legacy txt mirroring", "✅ Completed"),
            ("v4~v5", "8 Nickname Generation Engines", "Permutation, Hybrid, Dictionary, Pattern, Numeric, Custom Mask, Combinatorial, Recheck", "✅ Completed"),
            ("v6~v7", "Surfshark 1:1 Multi-Tunnel Pool", "Wireproxy user-space netstack, up to 50 concurrent workers, 142 global cluster nodes", "✅ Completed"),
            ("v8", "Zero-Downtime Atomic Hot-Swap", "Individual worker 429 triggers 0.3s hot-swap to fresh country without stopping other workers", "✅ Completed"),
            ("v9", "Multi-Window Sharding & DB Sync", "Mathematical 2~4 shard splitting (`2_1`, `2_2`), SQLite WAL real-time refresh popup", "✅ Completed"),
            ("v10", "GUI/UX Onboarding & Performance", "Top onboarding guide banner, full control tooltips, 30ms batch debounce queue (60 FPS)", "✅ Completed"),
            ("v11", "Mobile Termux & Docker Deploy", "Android `proot-distro debian` 1-click script, Multi-Arch ARM64/AMD64 Dockerfile", "✅ Completed"),
            ("v12.0", "Cross-Platform Production Release", "4 standalone Windows EXEs, macOS/Linux automated scripts, safe deployment rules", "✅ Completed"),
            ("v12.1", "GitHub Zero-Leak & Vibe Coding", "Hardened `.gitignore`, dummy templates (`.env.example`), zero hardcoded credentials", "✅ Completed"),
            ("v12.2", "Mobile Touch Web GUI & PWA", "Mobile-responsive Web UI, Service Worker PWA, 0.1s Discord Webhook push notifications", "✅ Completed"),
            ("v12.3", "Free Public Proxy & Android APK", "18 public sources scraped & Cloudflare verified, signed standalone Android APK package", "✅ Completed"),
            ("v12.4", "Two-Way Navigation & OS Guides", "Full bidirectional TOC/return links across all docs, 13 platform manuals in docs/guides/", "✅ Completed"),
            ("v12.5", "12-Language 1:1 Suite & Root Clean", "Complete 1:1 translation for 8 core docs across 12 languages, root reorganization & UX polish", "✅ Completed")
        ],
        "sec2_title": "2. Current System Assets",
        "sec2_id": "-2-current-system-assets",
        "sec2_items": [
            "**Desktop Execution (GUI / CLI)**: `python src/gui_ko.py` / `python src/gui_en.py` / `python src/run.py` / 4 Standalone EXEs (`dist/`)",
            "**Mobile Web GUI & Android APK**: Port 5000 touch web interface / PWA offline cache / `DiscordUsernameChecker_v12.3.0.apk`",
            "**Docker & Container Stacks**: `deploy/Dockerfile` (Multi-Arch Python 3.12 slim), `deploy/docker-compose.yml` (2-shard acceleration profile)",
            "**12-Language Documentation Suite**: `README.md` and `docs/locales/<lang>/` (1:1 full fidelity across 12 languages)"
        ],
        "sec3_title": "3. Quality Assurance & Architectural Invariants",
        "sec3_id": "-3-quality-assurance--architectural-invariants",
        "sec3_items": [
            "**Zero-Leak Invariant**: Real WireGuard keys, private credentials, and local machine paths permanently blocked from Git.",
            "**100% Mechanical Verification**: All 103 unit tests and 13 verification deliverables must pass with exit code 0.",
            "**Bidirectional Navigation Guarantee**: All TOC anchors and return-to-top links must resolve without broken links."
        ]
    },
    "ja": {
        "title": "📋 D4UC 統合タスクインデックスおよび開発バックログ (TASKS.md)",
        "desc": "バージョン別マイルストーン達成履歴、システム配布資産の現況および開発タスク管理",
        "sec1_title": "1. マイルストーン完了履歴 (Completed Milestones)",
        "sec1_id": "-1-マイルストーン完了履歴-completed-milestones",
        "milestones_header": "| バージョン | マイルストーン名称 | 主な達成内容および技術的成果 | 状態 |\n| :---: | :--- | :--- | :---: |",
        "milestones": [
            ("v1~v3", "非同期コアおよびSQLite構築", "`curl_cffi` による Chrome 131 TLS ステルス偽装、SQLite 永続化、レガシーtxtミラーリング", "✅ 完了"),
            ("v4~v5", "8大ユーザー名生成エンジンの完成", "順列、ハイブリッド、辞書、パターン、数字、カスタムマスク、組合せ、再検証", "✅ 完了"),
            ("v6~v7", "Surfshark 1:1 複数トンネルプール", "Wireproxy ユーザ空間連携、最大50ワーカ同時稼働、142グローバルノード対応", "✅ 完了"),
            ("v8", "429 無停止アトミックホットスワップ", "429検知時に該当トンネルのみ0.3秒以内に別国へ自動切替、他ワーカ停止ゼロ", "✅ 完了"),
            ("v9", "複数ウィンドウ分割シャーディングと同期", "数学的2〜4分割シャーディング（`2_1`、`2_2`等）、SQLite WAL リアルタイム同期", "✅ 完了"),
            ("v10", "GUI/UX オンボーディングと高速化", "上部ガイドバナー、全項目ツールチップ、30ms バッチデバウンスキュー（60 FPS保証）", "✅ 完了"),
            ("v11", "モバイル Termux および Docker 配布", "Android `proot-distro debian` 1クリック導入、Multi-Arch Dockerfile", "✅ 完了"),
            ("v12.0", "マルチプラットフォーム正式リリース", "Windows単独実行EXE 4種、macOS/Linux 自動化スクリプト、安全配布規則", "✅ 完了"),
            ("v12.1", "GitHub 安全配布 & バイブコーディング", "堅牢な `.gitignore`、ダミーテンプレート、シークレット漏洩の完全排除", "✅ 完了"),
            ("v12.2", "モバイル最適化 Web GUI & PWA", "レスポンシブ Web UI、Service Worker PWA、0.1秒 Discord Webhook 通知", "✅ 完了"),
            ("v12.3", "無料プロキシ自動収集 & APKビルド", "18公開ソース自動収集とCloudflare検証、署名済みAndroid単独APK", "✅ 完了"),
            ("v12.4", "双方向ナビゲーション & OS別ガイド", "全文書の相互ジャンプ目次・戻るリンク、13種類のOS別詳細マニュアル", "✅ 完了"),
            ("v12.5", "12言語 1:1 完全ローカライズ & ルート整理", "8大主要文書の12言語完全翻訳、ルートディレクトリ整理とUX最適化", "✅ 完了")
        ],
        "sec2_title": "2. 現在のシステム配布資産 (Current System Assets)",
        "sec2_id": "-2-現在のシステム配布資産-current-system-assets",
        "sec2_items": [
            "**デスクトップ実行 (GUI / CLI)**: `python src/gui_ko.py` / `python src/gui_en.py` / `python src/run.py` / 単独EXE 4種 (`dist/`)",
            "**モバイル Web GUI & Android APK**: ポート5000 Web UI / PWA オフラインキャッシュ / `DiscordUsernameChecker_v12.3.0.apk`",
            "**Docker & コンテナスタック**: `deploy/Dockerfile` (Multi-Arch Python 3.12 slim)、`deploy/docker-compose.yml` (2シャード加速)",
            "**12言語ドキュメントスイート**: `README.md` および `docs/locales/<lang>/` (12言語 1:1 完全対応)"
        ],
        "sec3_title": "3. 品質保証とアーキテクチャ不変条件",
        "sec3_id": "-3-品質保証とアーキテクチャ不変条件",
        "sec3_items": [
            "**シークレット流出ゼロ不変条件**: WireGuard秘密鍵、パスワード、環境固有パスのGitコミットを永久遮断。",
            "**100% 機械的検証の保証**: 103件の単体テストおよび13件の検証フェーズすべてで終了コード0（exit 0）を必須確認。",
            "**双方向リンク整合性の維持**: 全文書の目次アンカーおよびトップへ戻るリンクが破損なく正常動作。"
        ]
    },
    "zh-CN": {
        "title": "📋 D4UC 综合任务索引与开发日志 (TASKS.md)",
        "desc": "各版本里程碑达成记录、系统交付资产清单与开发待办任务管理",
        "sec1_title": "1. 里程碑达成记录 (Completed Milestones)",
        "sec1_id": "-1-里程碑达成记录-completed-milestones",
        "milestones_header": "| 版本 | 里程碑名称 | 主要成果与技术突破 | 状态 |\n| :---: | :--- | :--- | :---: |",
        "milestones": [
            ("v1~v3", "异步核心与 SQLite 架构构建", "基于 `curl_cffi` 的 Chrome 131 TLS 隐形伪装、SQLite 结果持久化与文本镜像", "✅ 已完成"),
            ("v4~v5", "八大候选用户名生成引擎", "排列、混合、字典、模式、数字、自定义掩码、组合式与复检引擎", "✅ 已完成"),
            ("v6~v7", "Surfshark 1:1 多隧道代理池", "Wireproxy 用户空间隧道接入，支持多达 50 个并发 Worker 与 142 个全球节点", "✅ 已完成"),
            ("v8", "429 无停机原子热切换", "单个 Worker 遭遇 429 时仅对该隧道在 0.3 秒内秒切至新国家，其他 Worker 零中断", "✅ 已完成"),
            ("v9", "多窗口分片扫描与 DB 同步", "数学分片（`2_1`、`2_2` 等）、SQLite WAL 多进程安全互斥与实时刷新弹窗", "✅ 已完成"),
            ("v10", "GUI/UX 新手指引与性能调优", "顶部引导横幅、全控件悬停提示、30ms 日志批量防抖队列（稳定 60 FPS）", "✅ 已完成"),
            ("v11", "移动端 Termux 与 Docker 交付", "安卓 `proot-distro debian` 一键脚本、Multi-Arch ARM64/AMD64 Dockerfile", "✅ 已完成"),
            ("v12.0", "跨平台生产环境正式发布", "Windows 4 种独立 EXE、macOS/Linux 一键安装脚本与安全合规守则", "✅ 已完成"),
            ("v12.1", "GitHub 零泄漏安全交付", "极严 `.gitignore`、示例配置模板（`.env.example`）、彻底杜绝密钥硬编码", "✅ 已完成"),
            ("v12.2", "触控移动端 Web GUI & PWA", "响应式触摸网页 UI、Service Worker PWA 支持、0.1 秒 Discord Webhook 推送", "✅ 已完成"),
            ("v12.3", "免费公开代理抓取与 APK 构建", "18 个公开源实时收集与 Cloudflare 验证、已签名的独立 Android APK", "✅ 已完成"),
            ("v12.4", "双向导航与操作系统指南", "全文档双向跳转目录与返回顶部链接、13 种系统专属指南文档", "✅ 已完成"),
            ("v12.5", "12 国语言 1:1 完整文档与根目录优化", "8 大核心文档 12 种语言 1:1 翻译、精简根目录并优化 GitHub UX", "✅ 已完成")
        ],
        "sec2_title": "2. 当前系统交付资产 (Current System Assets)",
        "sec2_id": "-2-当前系统交付资产-current-system-assets",
        "sec2_items": [
            "**桌面端运行 (GUI / CLI)**: `python src/gui_ko.py` / `python src/gui_en.py` / `python src/run.py` / 4 种独立 EXE (`dist/`)",
            "**移动端 Web GUI & 安卓 APK**: 5000 端口响应式触控 Web / PWA 离线缓存 / `DiscordUsernameChecker_v12.3.0.apk`",
            "**Docker 容器堆栈**: `deploy/Dockerfile` (Multi-Arch Python 3.12 slim)、`deploy/docker-compose.yml` (双分片加速模式)",
            "**12 国语言完整文档集**: `README.md` 与 `docs/locales/<lang>/` (12 种语言 1:1 逐字对齐)"
        ],
        "sec3_title": "3. 质量保证与架构不变量",
        "sec3_id": "-3-质量保证与架构不变量",
        "sec3_items": [
            "**零密钥泄漏不变量**: 严禁将真实 WireGuard 私钥、密码或本机绝对路径提交至 Git 仓库。",
            "**100% 机械化验证达标**: 必须保证全部 103 项单元测试与 13 项交付验证以退出码 0 (`exit 0`) 通过。",
            "**双向导航完整性保证**: 所有文档内的目录锚点和返回顶部链接均须正常运作（零失效链接）。"
        ]
    },
    "es": {
        "title": "📋 Índice de Tareas y Backlog de Desarrollo de D4UC (TASKS.md)",
        "desc": "Historial de hitos por versión, inventario de activos del sistema y backlog de tareas",
        "sec1_title": "1. Hitos Completados (Completed Milestones)",
        "sec1_id": "-1-hitos-completados-completed-milestones",
        "milestones_header": "| Versión | Hito | Logros Clave e Innovaciones Técnicas | Estado |\n| :---: | :--- | :--- | :---: |",
        "milestones": [
            ("v1~v3", "Núcleo Asíncrono y SQLite", "Impersonación TLS Chrome 131 con `curl_cffi`, persistencia SQLite y archivos txt espejo", "✅ Completado"),
            ("v4~v5", "8 Motores de Generación", "Permutación, Híbrido, Diccionario, Patrón, Numérico, Máscara, Combinatorio y Reverificación", "✅ Completado"),
            ("v6~v7", "Pool Multitúnel 1:1 Surfshark", "Túneles en espacio de usuario con Wireproxy, hasta 50 workers concurrentes, 142 clústeres", "✅ Completado"),
            ("v8", "Hot-Swap Atómico ante 429", "Reemplazo atómico de nodo en 0.3s ante límite 429 sin afectar al resto de workers", "✅ Completado"),
            ("v9", "Fragmentación Sharding y BD", "División matemática de rangos (`2_1`, `2_2`), sincronización en tiempo real con SQLite WAL", "✅ Completado"),
            ("v10", "GUI/UX y Optimización", "Banner informativo, tooltips interactivos, cola debounced de 30ms para garantizar 60 FPS", "✅ Completado"),
            ("v11", "Termux Móvil y Docker", "Script automático para Android `proot-distro debian`, Dockerfile Multi-Arch ARM64/AMD64", "✅ Completado"),
            ("v12.0", "Lanzamiento Multiplataforma", "4 ejecutables EXE autónomos, scripts para macOS/Linux, protocolos de despliegue seguro", "✅ Completado"),
            ("v12.1", "Despliegue Cero Fugas GitHub", "`.gitignore` blindado, plantillas de ejemplo, eliminación permanente de claves embebidas", "✅ Completado"),
            ("v12.2", "Web GUI Móvil y PWA", "Interfaz táctil responsive, Service Worker PWA, notificaciones Webhook en 0.1s", "✅ Completado"),
            ("v12.3", "Proxies Gratuitos y APK", "Scraper de 18 fuentes públicas con validación Cloudflare, APK nativo para Android", "✅ Completado"),
            ("v12.4", "Navegación Bidireccional y Guías", "Índices interactivos con enlaces de retorno, 13 manuales completos por sistema operativo", "✅ Completado"),
            ("v12.5", "Suite de 12 Idiomas y Limpieza", "Traducción completa 1:1 de 8 documentos en 12 idiomas, reorganización de la raíz y UX", "✅ Completado")
        ],
        "sec2_title": "2. Activos Actuales del Sistema",
        "sec2_id": "-2-activos-actuales-del-sistema",
        "sec2_items": [
            "**Ejecución de Escritorio**: `python src/gui_ko.py` / `python src/gui_en.py` / `python src/run.py` / 4 EXEs autónomos (`dist/`)",
            "**Web GUI Móvil y APK**: Interfaz táctil puerto 5000 / PWA offline / `DiscordUsernameChecker_v12.3.0.apk`",
            "**Contenedores Docker**: `deploy/Dockerfile` (Multi-Arch), `deploy/docker-compose.yml` (perfil 2-shard)",
            "**Suite de Documentación en 12 Idiomas**: `README.md` y `docs/locales/<lang>/` (1:1 en los 12 idiomas)"
        ],
        "sec3_title": "3. Aseguramiento de Calidad e Invariantes",
        "sec3_id": "-3-aseguramiento-de-calidad-e-invariantes",
        "sec3_items": [
            "**Invariante Cero Fugas**: Claves WireGuard reales y contraseñas bloqueadas permanentemente de Git.",
            "**Verificación Mecánica al 100%**: 103 pruebas unitarias y 13 entregables verificados con código de salida 0.",
            "**Navegación Bidireccional Garantizada**: Enlaces de tabla de contenidos y retornos funcionando sin errores."
        ]
    },
    "fr": {
        "title": "📋 Index des Tâches et Backlog de Développement D4UC (TASKS.md)",
        "desc": "Historique des jalons par version, état des livrables du système et gestion du backlog",
        "sec1_title": "1. Historique des Jalons Achevés (Completed Milestones)",
        "sec1_id": "-1-historique-des-jalons-achevés-completed-milestones",
        "milestones_header": "| Version | Jalon | Réalisations Clés & Avancées Techniques | Statut |\n| :---: | :--- | :--- | :---: |",
        "milestones": [
            ("v1~v3", "Cœur Asynchrone & Architecture SQLite", "Furtivité TLS Chrome 131 via `curl_cffi`, persistance SQLite et fichiers miroirs txt", "✅ Terminé"),
            ("v4~v5", "8 Moteurs de Génération de Noms", "Permutation, Hybride, Dictionnaire, Motif, Numérique, Masque, Combinatoire, Revérification", "✅ Terminé"),
            ("v6~v7", "Pool Multi-Tunnels 1:1 Surfshark", "Wireproxy en espace utilisateur, jusqu'à 50 workers simultanés, 142 nœuds mondiaux", "✅ Terminé"),
            ("v8", "Hot-Swap Atomique Sans Interruption", "Bascule en 0,3s d'un tunnel ciblé par un 429 vers un nouveau pays sans bloquer les autres", "✅ Terminé"),
            ("v9", "Sharding Multi-Fenêtres & Sync BD", "Découpage mathématique (`2_1`, `2_2`), synchronisation SQLite WAL en temps réel", "✅ Terminé"),
            ("v10", "GUI/UX et Amélioration des Débits", "Bandeau d'accueil, infobulles complètes, file d'attente debounced de 30ms (60 FPS)", "✅ Terminé"),
            ("v11", "Termux Mobile & Déploiement Docker", "Script 1-clic pour Android `proot-distro debian`, Dockerfile Multi-Arch ARM64/AMD64", "✅ Terminé"),
            ("v12.0", "Livraison Multiplateforme Finale", "4 exécutables Windows EXE autonomes, scripts macOS/Linux, règles de sécurité strictes", "✅ Terminé"),
            ("v12.1", "Publication Sécurisée Zéro Fuite", "`.gitignore` renforcé, modèles de configuration, suppression définitive des secrets en dur", "✅ Terminé"),
            ("v12.2", "Web GUI Tactile & PWA Mobile", "Interface Web responsive, PWA avec Service Worker, alertes Webhook en 0,1s", "✅ Terminé"),
            ("v12.3", "Proxys Publics Gratuits & APK", "Collecte depuis 18 sources et validation Cloudflare, APK Android autonome signé", "✅ Terminé"),
            ("v12.4", "Navigation Bidirectionnelle & Guides", "Tables des matières interactives avec retour au sommaire, 13 manuels dédiés par OS", "✅ Terminé"),
            ("v12.5", "Suite Complète 12 Langues & Nettoyage", "Traduction 1:1 de 8 documents en 12 langues, arborescence racine allégée et UX bonifiée", "✅ Terminé")
        ],
        "sec2_title": "2. État des Actifs du Système",
        "sec2_id": "-2-état-des-actifs-du-système",
        "sec2_items": [
            "**Exécution Desktop**: `python src/gui_ko.py` / `python src/gui_en.py` / `python src/run.py` / 4 EXE autonomes (`dist/`)",
            "**Web GUI Mobile & APK**: Interface tactile port 5000 / cache PWA / `DiscordUsernameChecker_v12.3.0.apk`",
            "**Conteneurs Docker**: `deploy/Dockerfile` (Multi-Arch), `deploy/docker-compose.yml` (profil 2-shard)",
            "**Suite Documentaire 12 Langues**: `README.md` et `docs/locales/<lang>/` (alignement 1:1 pour les 12 langues)"
        ],
        "sec3_title": "3. Assurance Qualité et Invariants d'Architecture",
        "sec3_id": "-3-assurance-qualité-et-invariants-darchitecture",
        "sec3_items": [
            "**Invariant Zéro Fuite**: Interdiction permanente de tout commit contenant des clés WireGuard ou des identifiants réels.",
            "**Vérification Mécanique à 100%**: 103 tests unitaires et 13 validations de livrables doivent réussir avec le code de sortie 0.",
            "**Garantie de Navigation Bidirectionnelle**: Aucun lien rompu parmi l'ensemble des ancres et liens de retour."
        ]
    },
    "de": {
        "title": "📋 D4UC Aufgabenindex und Entwicklungs-Backlog (TASKS.md)",
        "desc": "Meilensteinverlauf nach Versionen, Status der System-Assets und Aufgabenverwaltung",
        "sec1_title": "1. Abgeschlossene Meilensteine (Completed Milestones)",
        "sec1_id": "-1-abgeschlossene-meilensteine-completed-milestones",
        "milestones_header": "| Version | Meilenstein | Wichtigste Erfolge & Technische Innovationen | Status |\n| :---: | :--- | :--- | :---: |",
        "milestones": [
            ("v1~v3", "Asynchroner Kern & SQLite-Architektur", "`curl_cffi` Chrome 131 TLS-Tarnung, SQLite-Ergebnisspeicherung, TXT-Dateispiegelung", "✅ Abgeschlossen"),
            ("v4~v5", "8 Nickname-Generierungs-Engines", "Permutation, Hybrid, Wörterbuch, Muster, Numerisch, Maske, Kombinatorisch, Nachprüfung", "✅ Abgeschlossen"),
            ("v6~v7", "Surfshark 1:1 Multitunnel-Pool", "Wireproxy-User-Space-Netstack, bis zu 50 gleichzeitige Worker, 142 globale Cluster-Knoten", "✅ Abgeschlossen"),
            ("v8", "Unterbrechungsfreier Atomarer Hot-Swap", "429-Erkennung löst innerhalb von 0,3s Hot-Swap auf neuen Tunnel aus, andere Worker ungestört", "✅ Abgeschlossen"),
            ("v9", "Mehrfenster-Sharding & DB-Sync", "Mathematische Bereichsaufteilung (`2_1`, `2_2`), SQLite WAL Echtzeit-Aktualisierung", "✅ Abgeschlossen"),
            ("v10", "GUI/UX-Onboarding & Performance", "Onboarding-Leiste, vollständige Tooltips, 30ms Batch-Debounce-Warteschlange (60 FPS)", "✅ Abgeschlossen"),
            ("v11", "Mobiles Termux & Docker-Deployment", "Android `proot-distro debian` 1-Klick-Skript, Multi-Arch ARM64/AMD64 Dockerfile", "✅ Abgeschlossen"),
            ("v12.0", "Plattformübergreifendes Release", "4 eigenständige Windows-EXEs, automatisierte macOS/Linux-Skripte, Sicherheitsrichtlinien", "✅ Abgeschlossen"),
            ("v12.1", "GitHub Zero-Leak-Bereitstellung", "Gehärtete `.gitignore`, Konfigurationsmuster, vollständiger Verzicht auf feste Schlüssel", "✅ Abgeschlossen"),
            ("v12.2", "Mobiles Touch-Web-GUI & PWA", "Responsive Touch-Weboberfläche, Service Worker PWA, 0,1s Discord-Webhook-Push", "✅ Abgeschlossen"),
            ("v12.3", "Kostenlose Proxys & Android APK", "Scraping aus 18 Quellen mit Cloudflare-Check, signiertes eigenständiges Android-APK", "✅ Abgeschlossen"),
            ("v12.4", "Bidirektionale Navigation & Guides", "Interaktives Inhaltsverzeichnis mit Rücksprunglinks, 13 umfassende OS-Handbücher", "✅ Abgeschlossen"),
            ("v12.5", "12-Sprachen-Suite & Root-Optimierung", "1:1-Übersetzung von 8 Dokumenten in 12 Sprachen, aufgeräumtes Root-Verzeichnis & UX-Politur", "✅ Abgeschlossen")
        ],
        "sec2_title": "2. Aktueller Bestand an System-Assets",
        "sec2_id": "-2-aktueller-bestand-an-system-assets",
        "sec2_items": [
            "**Desktop-Ausführung**: `python src/gui_ko.py` / `python src/gui_en.py` / `python src/run.py` / 4 eigenständige EXEs (`dist/`)",
            "**Mobiles Web GUI & APK**: Port 5000 Touch-UI / PWA-Offline-Cache / `DiscordUsernameChecker_v12.3.0.apk`",
            "**Docker-Stacks**: `deploy/Dockerfile` (Multi-Arch), `deploy/docker-compose.yml` (2-Shard-Beschleunigung)",
            "**12-Sprachen-Dokumentations-Suite**: `README.md` und `docs/locales/<lang>/` (1:1-Übereinstimmung für alle 12 Sprachen)"
        ],
        "sec3_title": "3. Qualitätssicherung & Architektur-Invarianten",
        "sec3_id": "-3-qualitätssicherung--architektur-invarianten",
        "sec3_items": [
            "**Zero-Leak-Invariante**: Keine echten WireGuard-Schlüssel, Passwörter oder Hostpfade in Git.",
            "**100% mechanische Verifikation**: Alle 103 Unit-Tests und 13 Prüfungen müssen mit Exit-Code 0 abschließen.",
            "**Garantierte bidirektionale Navigation**: Vollständig funktionierende Inhaltsverzeichnis- und Zurück-Links."
        ]
    },
    "ru": {
        "title": "📋 Сводный индекс задач и журнал разработки D4UC (TASKS.md)",
        "desc": "История ключевых этапов по версиям, состав артефактов и управление бэклогом разработки",
        "sec1_title": "1. Завершенные этапы (Completed Milestones)",
        "sec1_id": "-1-завершенные-этапы-completed-milestones",
        "milestones_header": "| Версия | Название этапа | Основные достижения и технические результаты | Статус |\n| :---: | :--- | :--- | :---: |",
        "milestones": [
            ("v1~v3", "Асинхронное ядро и архитектура SQLite", "Маскировка TLS Chrome 131 через `curl_cffi`, сохранение в SQLite и зеркальные txt-файлы", "✅ Завершено"),
            ("v4~v5", "8 генераторов имен пользователей", "Перестановки, гибридный, словарный, шаблонный, числовой, маски, комбинаторный, перепроверка", "✅ Завершено"),
            ("v6~v7", "Surfshark 1:1 пул мульти-туннелей", "Wireproxy в пользовательском пространстве, до 50 параллельных воркеров, 142 локации", "✅ Завершено"),
            ("v8", "Атомарная горячая замена при 429", "При получении 429 узел меняется за 0.3с без остановки остальных воркеров", "✅ Завершено"),
            ("v9", "Шардинг и синхронизация БД", "Математическое разбиение диапазона (`2_1`, `2_2`), обновление SQLite WAL в реальном времени", "✅ Завершено"),
            ("v10", "GUI/UX онбординг и оптимизация", "Информационный баннер, подсказки к элементам, буферизация логов с задержкой 30мс (60 FPS)", "✅ Завершено"),
            ("v11", "Мобильный Termux и Docker", "Скрипт развертывания для Android `proot-distro debian`, Multi-Arch Dockerfile", "✅ Завершено"),
            ("v12.0", "Мультиплатформенный релиз", "4 автономных EXE для Windows, скрипты для macOS/Linux, правила безопасной публикации", "✅ Завершено"),
            ("v12.1", "Публикация без утечек на GitHub", "Строгий `.gitignore`, шаблоны конфигураций, полное исключение приватных ключей из кода", "✅ Завершено"),
            ("v12.2", "Сенсорный Web GUI и PWA", "Адаптивный мобильный интерфейс, поддержка PWA, уведомления через Discord Webhook за 0.1с", "✅ Завершено"),
            ("v12.3", "Бесплатные прокси и Android APK", "Сбор из 18 источников с проверкой Cloudflare, подписанный независимый APK для Android", "✅ Завершено"),
            ("v12.4", "Двусторонняя навигация и гайды", "Интерактивное оглавление со ссылками возврата, 13 подробных руководств для разных ОС", "✅ Завершено"),
            ("v12.5", "Полный комплект на 12 языках и чистка", "Перевод 8 основных документов на 12 языков 1:1, очистка корня репозитория и полировка UX", "✅ Завершено")
        ],
        "sec2_title": "2. Текущие артефакты системы",
        "sec2_id": "-2-текущие-артефакты-системы",
        "sec2_items": [
            "**Десктопные сборки**: `python src/gui_ko.py` / `python src/gui_en.py` / `python src/run.py` / 4 автономных EXE (`dist/`)",
            "**Мобильный Web GUI и APK**: Сенсорный интерфейс на порту 5000 / PWA кэш / `DiscordUsernameChecker_v12.3.0.apk`",
            "**Стек Docker**: `deploy/Dockerfile` (Multi-Arch), `deploy/docker-compose.yml` (профиль с 2 шардами)",
            "**Комплект документации на 12 языках**: `README.md` и `docs/locales/<lang>/` (полное 1:1 соответствие)"
        ],
        "sec3_title": "3. Гарантии качества и архитектурные инварианты",
        "sec3_id": "-3-гарантии-качества-и-архитектурные-инварианты",
        "sec3_items": [
            "**Инвариант нулевых утечек**: Реальные ключи WireGuard, пароли и локальные пути навсегда заблокированы в Git.",
            "**100% механическая верификация**: Все 103 модульных теста и 13 этапов проверки обязаны завершаться с кодом 0.",
            "**Двусторонняя навигация**: Отсутствие битых ссылок в оглавлениях и кнопках возврата наверх."
        ]
    },
    "pt-BR": {
        "title": "📋 Índice de Tarefas e Backlog de Desenvolvimento D4UC (TASKS.md)",
        "desc": "Histórico de marcos por versão, ativos do sistema e gerenciamento de tarefas",
        "sec1_title": "1. Marcos Concluídos (Completed Milestones)",
        "sec1_id": "-1-marcos-concluídos-completed-milestones",
        "milestones_header": "| Versão | Título do Marco | Principais Conquistas & Inovações Técnicas | Status |\n| :---: | :--- | :--- | :---: |",
        "milestones": [
            ("v1~v3", "Núcleo Assíncrono & SQLite", "Disfarce TLS Chrome 131 via `curl_cffi`, persistência em SQLite e espelhamento txt", "✅ Concluído"),
            ("v4~v5", "8 Motores de Geração de Nomes", "Permutação, Híbrido, Dicionário, Padrão, Numérico, Máscara, Combinatório, Rechecagem", "✅ Concluído"),
            ("v6~v7", "Pool Multitúnel 1:1 Surfshark", "Wireproxy em espaço de usuário, até 50 workers concorrentes, 142 clusters globais", "✅ Concluído"),
            ("v8", "Hot-Swap Atômico sem Interrupção", "Troca imediata de túnel em 0,3s ao detectar 429 sem interromper os demais workers", "✅ Concluído"),
            ("v9", "Sharding Multi-Janelas & Sincronização", "Divisão matemática de intervalos (`2_1`, `2_2`), sincronização em tempo real via SQLite WAL", "✅ Concluído"),
            ("v10", "GUI/UX & Alta Performance", "Banner explicativo, dicas em todos os botões, fila com debounce de 30ms para 60 FPS estáveis", "✅ Concluído"),
            ("v11", "Termux Móvel & Docker", "Script automatizado para Android `proot-distro debian`, Dockerfile Multi-Arch ARM64/AMD64", "✅ Concluído"),
            ("v12.0", "Lançamento Multiplataforma", "4 executáveis independentes para Windows, scripts para macOS/Linux, regras de segurança", "✅ Concluído"),
            ("v12.1", "Publicação Segura no GitHub", "`.gitignore` reforçado, modelos de configuração, ausência de senhas no código-fonte", "✅ Concluído"),
            ("v12.2", "Web GUI Touch & PWA Móvel", "Interface Web responsiva, PWA com Service Worker, notificações Webhook em 0,1s", "✅ Concluído"),
            ("v12.3", "Proxies Gratuitos & APK Android", "Coleta de 18 fontes públicas com validação Cloudflare, APK nativo assinado", "✅ Concluído"),
            ("v12.4", "Navegação Bidirecional & Guias", "Sumários interativos com links de retorno, 13 manuais completos por sistema operacional", "✅ Concluído"),
            ("v12.5", "Suíte Completa em 12 Idiomas & Limpeza", "Tradução 1:1 de 8 documentos em 12 idiomas, reorganização da raiz e polimento de UX", "✅ Concluído")
        ],
        "sec2_title": "2. Ativos Atuais do Sistema",
        "sec2_id": "-2-ativos-atuais-do-sistema",
        "sec2_items": [
            "**Execução Desktop**: `python src/gui_ko.py` / `python src/gui_en.py` / `python src/run.py` / 4 EXEs independentes (`dist/`)",
            "**Web GUI Móvel & APK**: Interface de toque na porta 5000 / cache PWA / `DiscordUsernameChecker_v12.3.0.apk`",
            "**Pilhas Docker**: `deploy/Dockerfile` (Multi-Arch), `deploy/docker-compose.yml` (perfil 2-shard)",
            "**Suíte de Documentação em 12 Idiomas**: `README.md` e `docs/locales/<lang>/` (1:1 nos 12 idiomas)"
        ],
        "sec3_title": "3. Garantia de Qualidade e Invariantes",
        "sec3_id": "-3-garantia-de-qualidade-e-invariantes",
        "sec3_items": [
            "**Invariante de Zero Vazamentos**: Chaves WireGuard reais e senhas terminantemente bloqueadas no Git.",
            "**100% de Verificação Mecânica**: Todos os 103 testes unitários e 13 verificações com código de saída 0.",
            "**Navegação Bidirecional Íntegra**: Todos os links de sumário e retorno ao topo funcionando perfeitamente."
        ]
    },
    "ar": {
        "title": "📋 فهرس مهام D4UC وسجل التطوير المتراكم (TASKS.md)",
        "desc": "سجل إنجاز المراحل الرئيسية للمشروع وقائمة الأصول المنشورة وإدارة خطة التطوير",
        "sec1_title": "1. سجل المراحل المنجزة (Completed Milestones)",
        "sec1_id": "-1-سجل-المراحل-المنجزة-completed-milestones",
        "milestones_header": "| الإصدار | اسم المرحلة | أبرز الإنجازات والحلول التقنية | الحالة |\n| :---: | :--- | :--- | :---: |",
        "milestones": [
            ("v1~v3", "النواة غير المتزامنة وقواعد بيانات SQLite", "محاكاة بصمة Chrome 131 TLS عبر `curl_cffi`، وتخزين النتائج في SQLite مع ملفات txt", "✅ مكتمل"),
            ("v4~v5", "محركات توليد أسماء المستخدمين الثمانية", "التباديل، الهجين، القاموس، الأنماط، الأرقام، الأقنعة المخصصة، التوافيق، وإعادة الفحص", "✅ مكتمل"),
            ("v6~v7", "مجمع أنفاق Surfshark المتعددة بنسبة 1:1", "ربط أنفاق Wireproxy في مساحة المستخدم، تشغيل حتى 50 عاملاً متزامناً، 142 خادماً عالمياً", "✅ مكتمل"),
            ("v8", "التبديل الفوري التلقائي عند مواجهة 429", "تبديل النفق المتأثر خلال 0.3 ثانية إلى دولة جديدة دون إيقاف بقية العمال بنسبة 0% انقطاع", "✅ مكتمل"),
            ("v9", "تقسيم النطاقات متعدد النوافذ وتزامن البيانات", "تجزئة النطاق رياضياً (`2_1`، `2_2`) وتزامن SQLite WAL الفوري مع النوافذ المنبثقة", "✅ مكتمل"),
            ("v10", "واجهة المستخدم الرسومية وتحسين الأداء", "شريط إرشادي علوي، تلميحات لكافة العناصر، وتجميع السجلات كل 30 مللي ثانية (60 FPS)", "✅ مكتمل"),
            ("v11", "دعم تطبيق Termux وحاويات Docker", "سكربت تثبيت بنقرة واحدة لـ `proot-distro debian` على أندرويد وملف Dockerfile متعدد المعماريات", "✅ مكتمل"),
            ("v12.0", "الإصدار الإنتاجي متعدد المنصات", "4 ملفات تنفيذية مستقلة لـ Windows، سكربتات macOS وLinux، وتطبيق قواعد الأمان الصارمة", "✅ مكتمل"),
            ("v12.1", "النشر الآمن على GitHub دون أي تسريب", "ملف `.gitignore` محكم، نماذج تكوين تجريبية، وحذف كافة المفاتيح الخاصة من الكود تماماً", "✅ مكتمل"),
            ("v12.2", "واجهة الويب المخصصة للهواتف وتطبيق PWA", "واجهة لمس متجاوبة للهواتف، دعم PWA للتخزين دون اتصال، وتنبيهات Webhook خلال 0.1 ثانية", "✅ مكتمل"),
            ("v12.3", "جمع البروكسيات المجانية وتطبيق أندرويد APK", "جمع البروكسيات من 18 مصدراً عالمياً والتحقق منها عبر Cloudflare، وتطبيق APK مستقل وموقع", "✅ مكتمل"),
            ("v12.4", "التنقل ثنائي الاتجاه ودلائل أنظمة التشغيل", "فهارس تفاعلية مع روابط للعودة للأعلى، و13 دليلاً شاملاً لكافة أنظمة التشغيل", "✅ مكتمل"),
            ("v12.5", "حزمة الـ 12 لغة كاملة 1:1 وتنظيم المستودع", "ترجمة 8 وثائق أساسية إلى 12 لغة بنسبة 1:1، وتنظيم المجلد الرئيسي وتحسين تجربة المستخدم", "✅ مكتمل")
        ],
        "sec2_title": "2. أصول النظام الحالية",
        "sec2_id": "-2-أصول-النظام-الحالية",
        "sec2_items": [
            "**تشغيل أجهزة سطح المكتب**: `python src/gui_ko.py` / `python src/gui_en.py` / `python src/run.py` / 4 ملفات EXE مستقلة (`dist/`)",
            "**واجهة الويب للهاتف وتطبيق أندرويد APK**: واجهة لمس على المنفذ 5000 / ذاكرة PWA / `DiscordUsernameChecker_v12.3.0.apk`",
            "**حاويات Docker**: `deploy/Dockerfile` (متعدد المعماريات)، `deploy/docker-compose.yml` (ملف تسريع التجزئة الثنائية)",
            "**حزمة التوثيق بـ 12 لغة**: `README.md` ومجلدات `docs/locales/<lang>/` (مطابقة بنسبة 1:1 لجميع اللغات الـ 12)"
        ],
        "sec3_title": "3. ضمان الجودة والثوابت الهندسية",
        "sec3_id": "-3-ضمان-الجودة-والثوابت-الهندسية",
        "sec3_items": [
            "**ثابت انعدام التسريب 0%**: حظر دائم لأي مفاتيح WireGuard حقيقية أو كلمات مرور أو مسارات محلية في Git.",
            "**التحقق الآلي بنسبة 100%**: اجتياز 103 اختبارات وحدة و13 مرحلة تحقق برمز خروج 0 بنجاح تام.",
            "**ضمان سلامة الروابط الثنائية**: التحقق من خلو جميع الفهارس وروابط العودة للأعلى من أي روابط معطلة."
        ]
    },
    "hi": {
        "title": "📋 D4UC कार्य सूचकांक और विकास बैकलॉग (TASKS.md)",
        "desc": "संस्करण मील का पत्थर इतिहास, सिस्टम परिनियोजन संपत्ति और विकास कार्य प्रबंधन",
        "sec1_title": "1. पूर्ण किए गए मील के पत्थर (Completed Milestones)",
        "sec1_id": "-1-पूर्ण-किए-गए-मील-के-पत्थर-completed-milestones",
        "milestones_header": "| संस्करण | मील का पत्थर | मुख्य उपलब्धियां और तकनीकी नवाचार | स्थिति |\n| :---: | :--- | :--- | :---: |",
        "milestones": [
            ("v1~v3", "अतुल्यकालिक कोर और SQLite आर्किटेक्चर", "`curl_cffi` के साथ Chrome 131 TLS स्टेल्थ, SQLite परिणाम भंडारण और txt फ़ाइल मिररिंग", "✅ पूर्ण"),
            ("v4~v5", "8 उपयोगकर्ता नाम निर्माण इंजन", "क्रमपरिवर्तन, हाइब्रिड, शब्दकोश, पैटर्न, संख्यात्मक, कस्टम मास्क, संयोजन, और पुनर्परीक्षण", "✅ पूर्ण"),
            ("v6~v7", "Surfshark 1:1 मल्टी-टनल पूल", "Wireproxy यूजर-स्पेस नेटस्टैक, 50 समवर्ती कार्यकर्ता, 142 वैश्विक क्लस्टर नोड्स", "✅ पूर्ण"),
            ("v8", "429 त्रुटि पर निर्बाध हॉट-स्वैप", "429 मिलने पर प्रभावित टनल को 0.3s में नए देश में बदलना, अन्य कार्यकर्ता निर्बाध रूप से चालू", "✅ पूर्ण"),
            ("v9", "मल्टी-विंडो शार्डिंग और DB सिंक", "गणितीय शार्डिंग (`2_1`, `2_2`), SQLite WAL रीयल-टाइम रिफ्रेश पॉपअप", "✅ पूर्ण"),
            ("v10", "GUI/UX ऑनबोर्डिंग और प्रदर्शन संवर्द्धन", "ऑनबोर्डिंग बैनर, सभी नियंत्रणों के लिए टूलटिप्स, 30ms बैच डिबाउंस कतार (60 FPS)", "✅ पूर्ण"),
            ("v11", "मोबाइल Termux और Docker परिनियोजन", "Android `proot-distro debian` 1-क्लिक स्क्रिप्ट, Multi-Arch ARM64/AMD64 Dockerfile", "✅ पूर्ण"),
            ("v12.0", "क्रॉस-प्लेटफ़ॉर्म प्रोडक्शन रिलीज़", "4 स्टैंडअलोन Windows EXEs, macOS/Linux स्वचालित स्क्रिप्ट, सुरक्षित परिनियोजन नियम", "✅ पूर्ण"),
            ("v12.1", "GitHub शून्य-रिसाव सुरक्षित परिनियोजन", "कठोर `.gitignore`, डमी कॉन्फ़िगरेशन टेम्प्लेट, कोई भी हार्डकोडेड क्रेडेंशियल नहीं", "✅ पूर्ण"),
            ("v12.2", "मोबाइल टच Web GUI और PWA", "उत्तरदायी मोबाइल टच वेब यूआई, सर्विस वर्कर PWA, 0.1s में Discord Webhook सूचनाएं", "✅ पूर्ण"),
            ("v12.3", "मुफ़्त सार्वजनिक प्रॉक्सी और Android APK", "18 सार्वजनिक स्रोतों से संग्रह और Cloudflare सत्यापन, हस्ताक्षरित Android APK पैकेज", "✅ पूर्ण"),
            ("v12.4", "द्विदिश नेविगेशन और OS गाइड", "सभी दस्तावेज़ों में इंटरएक्टिव सामग्री तालिका और शीर्ष पर लौटने के लिंक, 13 OS मैनुअल", "✅ पूर्ण"),
            ("v12.5", "12-भाषा 1:1 सुइट और रूट अनुकूलन", "8 प्रमुख दस्तावेज़ों का 12 भाषाओं में 1:1 अनुवाद, रूट डायरेक्टरी की सफाई और UX सुधार", "✅ पूर्ण")
        ],
        "sec2_title": "2. वर्तमान सिस्टम संपत्तियां",
        "sec2_id": "-2-वर्तमान-सिस्टम-संपत्तियां",
        "sec2_items": [
            "**डेस्कटॉप निष्पादन**: `python src/gui_ko.py` / `python src/gui_en.py` / `python src/run.py` / 4 स्टैंडअलोन EXEs (`dist/`)",
            "**मोबाइल Web GUI और Android APK**: पोर्ट 5000 टच वेब / PWA ऑफ़लाइन कैश / `DiscordUsernameChecker_v12.3.0.apk`",
            "**Docker स्टैक**: `deploy/Dockerfile` (Multi-Arch), `deploy/docker-compose.yml` (2-शार्ड त्वरण प्रोफ़ाइल)",
            "**12-भाषा दस्तावेज़ीकरण सुइट**: `README.md` और `docs/locales/<lang>/` (12 भाषाओं में 1:1 संरेखण)"
        ],
        "sec3_title": "3. गुणवत्ता आश्वासन और वास्तुकला अपरिवर्तनीय",
        "sec3_id": "-3-गुणवत्ता-आश्वासन-और-वास्तुकला-अपरिवर्तनीय",
        "sec3_items": [
            "**शून्य-रिसाव अपरिवर्तनीय**: वास्तविक WireGuard कुंजियाँ, पासवर्ड और स्थानीय पथ Git में पूरी तरह से अवरुद्ध हैं।",
            "**100% यांत्रिक सत्यापन**: सभी 103 यूनिट परीक्षणों और 13 सत्यापन चरणों को निकास कोड 0 के साथ उत्तीर्ण होना अनिवार्य है।",
            "**द्विदिश नेविगेशन अखंडता**: सामग्री तालिका और शीर्ष पर लौटने के सभी लिंक बिना किसी त्रुटि के कार्य करते हैं।"
        ]
    },
    "id": {
        "title": "📋 Indeks Tugas & Backlog Pengembangan D4UC (TASKS.md)",
        "desc": "Riwayat pencapaian tonggak per versi, inventaris aset sistem, dan manajemen tugas",
        "sec1_title": "1. Tonggak Pencapaian yang Selesai (Completed Milestones)",
        "sec1_id": "-1-tonggak-pencapaian-yang-selesai-completed-milestones",
        "milestones_header": "| Versi | Nama Tonggak | Pencapaian Kunci & Inovasi Teknis | Status |\n| :---: | :--- | :--- | :---: |",
        "milestones": [
            ("v1~v3", "Inti Asinkron & Arsitektur SQLite", "Penyamaran TLS Chrome 131 via `curl_cffi`, penyimpanan SQLite dan pencerminan berkas txt", "✅ Selesai"),
            ("v4~v5", "8 Mesin Pembuat Nama Pengguna", "Permutasi, Hibrida, Kamus, Pola, Numerik, Masking Kustom, Kombinatorial, dan Verifikasi Ulang", "✅ Selesai"),
            ("v6~v7", "Pool Multi-Terowongan 1:1 Surfshark", "Wireproxy ruang pengguna, hingga 50 worker konkuren, 142 node kluster global", "✅ Selesai"),
            ("v8", "Hot-Swap Atomik Tanpa Henti Saat 429", "Pengalihan otomatis dalam 0,3 detik saat terbentur batas 429 tanpa menghentikan worker lain", "✅ Selesai"),
            ("v9", "Sharding Multi-Jendela & Sinkronisasi DB", "Pembagian rentang matematis (`2_1`, `2_2`), pembaruan SQLite WAL waktu nyata", "✅ Selesai"),
            ("v10", "Panduan GUI/UX & Peningkatan Kinerja", "Spanduk panduan awal, tooltip pada setiap tombol, antrean debounce 30ms (stabil 60 FPS)", "✅ Selesai"),
            ("v11", "Termux Seluler & Kontainer Docker", "Skrip 1-klik Android `proot-distro debian`, Dockerfile Multi-Arch ARM64/AMD64", "✅ Selesai"),
            ("v12.0", "Rilis Produksi Lintas Platform", "4 berkas EXE mandiri Windows, skrip otomatis macOS/Linux, aturan keamanan terstandarisasi", "✅ Selesai"),
            ("v12.1", "Penyebaran Aman Bebas Bocor di GitHub", "`.gitignore` yang diperkuat, templat konfigurasi dummy, penghapusan mutlak kunci tertanam", "✅ Selesai"),
            ("v12.2", "Web GUI Sentuh & PWA Seluler", "Antarmuka Web responsif, PWA dengan Service Worker, notifikasi Discord Webhook dalam 0,1 detik", "✅ Selesai"),
            ("v12.3", "Proxy Publik Gratis & APK Android", "Pengumpulan dari 18 sumber publik tervalidasi Cloudflare, paket APK Android mandiri bertanda tangan", "✅ Selesai"),
            ("v12.4", "Navigasi Dua Arah & Panduan OS", "Daftar isi interaktif dengan tautan kembali ke atas, 13 manual lengkap per sistem operasi", "✅ Selesai"),
            ("v12.5", "Paket 12 Bahasa Lengkap 1:1 & Pembersihan", "Terjemahan 1:1 dari 8 dokumen utama ke dalam 12 bahasa, perapian direktori root & polesan UX", "✅ Selesai")
        ],
        "sec2_title": "2. Aset Sistem yang Tersedia Saat Ini",
        "sec2_id": "-2-aset-sistem-yang-tersedia-saat-ini",
        "sec2_items": [
            "**Eksekusi Desktop**: `python src/gui_ko.py` / `python src/gui_en.py` / `python src/run.py` / 4 berkas EXE mandiri (`dist/`)",
            "**Web GUI Seluler & APK Android**: Antarmuka sentuh port 5000 / cache PWA / `DiscordUsernameChecker_v12.3.0.apk`",
            "**Tumpukan Kontainer Docker**: `deploy/Dockerfile` (Multi-Arch), `deploy/docker-compose.yml` (profil akselerasi 2-shard)",
            "**Paket Dokumentasi 12 Bahasa**: `README.md` dan direktori `docs/locales/<lang>/` (keselarasan 1:1 di seluruh 12 bahasa)"
        ],
        "sec3_title": "3. Jaminan Kualitas & Invarian Arsitektur",
        "sec3_id": "-3-jaminan-kualitas--invarian-arsitektur",
        "sec3_items": [
            "**Invarian Bebas Kebocoran**: Kunci WireGuard riil, kata sandi, dan jalur lokal diblokir secara permanen dari Git.",
            "**Verifikasi Mekanis 100%**: Seluruh 103 pengujian unit dan 13 tahap verifikasi wajib lulus dengan kode keluar 0.",
            "**Integritas Navigasi Dua Arah**: Seluruh tautan jangkar daftar isi dan tombol kembali ke atas berfungsi tanpa tautan rusak."
        ]
    }
}
