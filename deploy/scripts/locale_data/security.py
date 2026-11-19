# deploy/scripts/locale_data/security.py
"""
1:1 Full Localization for SECURITY.md across all 12 locales.
"""

SECURITY_DATA = {
    "ko": {
        "title": "🛡️ 보안 정책 (Security Policy)",
        "desc": "D4UC 보안 가이드라인, 시크릿 보호 수칙 및 취약점 제보 정책",
        "sections": [
            {
                "title": "1. 자격 증명 및 프라이빗 키 보호 수칙",
                "id": "-1-자격-증명-및-프라이빗-키-보호-수칙",
                "content": """- **`config.yaml`, `.env`, `surfshark_credentials.json`, `*.conf`는 절대 버전 관리(Git)에 커밋하지 마십시오.**
- 본 저장소는 로컬 자격 증명, 런타임 데이터베이스(`*.db*`), 탐색 결과 파일(`available*.txt`, `taken*.txt`, `results/`), 빌드 바이너리(`*.exe`, `*.apk`)를 원천 차단하는 강화된 `.gitignore`를 포함합니다.
- 항상 `config/.env.example`, `config/config.example.yaml`, `data/surfshark_credentials.example.json` 템플릿을 복사하여 사용하십시오.
- 소스 코드 및 문서 어디에도 실제 비밀번호, WireGuard 개인키, 사용자 토큰이 하드코딩되어 있지 않습니다."""
            },
            {
                "title": "2. 네트워크 격리 및 Rate-Limit 안전성",
                "id": "-2-네트워크-격리-및-rate-limit-안전성",
                "content": """- 모든 HTTP 요청은 `curl_cffi` 기반 Chrome 131 TLS 스텔스 위장을 거치며, 유저스페이스 HTTP/SOCKS5 격리 터널(`wireproxy`)을 통해 라우팅됩니다.
- 호스트 OS의 기본 네트워크 어댑터, 라우팅 테이블, DNS 설정은 일절 변경되지 않습니다.
- 429 감지 시 즉시 0.3초 원자적 핫스왑(Hot-Swap)을 수행하여 단일 IP에 과도한 트래픽이 집중되지 않도록 보호합니다."""
            },
            {
                "title": "3. 보안 취약점 제보 (Reporting a Security Issue)",
                "id": "-3-보안-취약점-제보-reporting-a-security-issue",
                "content": """- 보안 취약점이나 의도치 않은 시크릿 노출을 발견하신 경우, 공개 이슈를 생성하지 마시고 GitHub의 **Private Security Advisory**를 통해 비공개 제보해 주시기 바랍니다.
- 또는 프로젝트 관리자(`KRCUPRO`)에게 직접 연락 주시면 24시간 이내에 분석 및 패치 릴리스를 진행합니다."""
            },
            {
                "title": "4. 책임 있는 연구 및 보안 정책 준수",
                "id": "-4-책임-있는-연구-및-보안-정책-준수",
                "content": """- 본 프로그램은 프로그래밍, TLS 지문 분석, 비동기 프록시 풀 관리, 네트워크 엔지니어링 학습 목적으로 개발되었습니다.
- 서비스 거부(DoS/DDoS) 공격이나 타인의 권리를 침해하는 용도로의 사용을 엄격히 금지합니다."""
            }
        ]
    },
    "en": {
        "title": "🛡️ Security Policy",
        "desc": "D4UC Security Guidelines, Secret Protection Rules, and Responsible Disclosure",
        "sections": [
            {
                "title": "1. Credentials & Private Keys Protection",
                "id": "-1-credentials--private-keys-protection",
                "content": """- **Never commit `config.yaml`, `.env`, `surfshark_credentials.json`, or `*.conf` to version control.**
- This repository includes a hardened `.gitignore` preventing accidental commits of local credentials, runtime databases (`*.db*`), scraped result files (`available*.txt`, `taken*.txt`, `results/`), and compiled binaries (`*.exe`, `*.apk`).
- Always copy and configure from provided templates: `config/.env.example`, `config/config.example.yaml`, and `data/surfshark_credentials.example.json`.
- Zero proprietary credentials, WireGuard private keys, or personal tokens are hardcoded in source code or documentation."""
            },
            {
                "title": "2. Network Isolation & Rate-Limit Safety",
                "id": "-2-network-isolation--rate-limit-safety",
                "content": """- All HTTP requests utilize `curl_cffi` Chrome 131 TLS stealth impersonation routed through isolated user-space HTTP/SOCKS5 tunnels (`wireproxy`).
- Host OS default network interfaces, system routing tables, and DNS configurations remain 100% untouched.
- When Discord returns HTTP 429, atomic hot-swap rotates to a fresh multi-tunnel node in under 0.3s, preventing request concentration on a single IP."""
            },
            {
                "title": "3. Reporting a Security Issue",
                "id": "-3-reporting-a-security-issue",
                "content": """- If you discover a security vulnerability or accidental credential exposure, please do NOT open a public GitHub issue.
- Instead, submit a report via GitHub **Private Security Advisory** or contact the repository owner (`KRCUPRO`) directly. Verified reports receive a patch within 24 hours."""
            },
            {
                "title": "4. Responsible Research & Ethics",
                "id": "-4-responsible-research--ethics",
                "content": """- D4UC is designed strictly for educational research into TLS fingerprinting, asynchronous proxy orchestration, and high-concurrency network architectures.
- DoS/DDoS attacks, credential stuffing, and unauthorized commercial exploitation are strictly prohibited."""
            }
        ]
    },
    "ja": {
        "title": "🛡️ セキュリティポリシー (Security Policy)",
        "desc": "D4UC セキュリティガイドライン、シークレット保護規則および脆弱性報告方針",
        "sections": [
            {
                "title": "1. 認証情報および秘密鍵の保護規則",
                "id": "-1-認証情報および秘密鍵の保護規則",
                "content": """- **`config.yaml`、`.env`、`surfshark_credentials.json`、`*.conf` を Git 等のバージョン管理にコミットしないでください。**
- 本リポジトリには、ローカル認証情報、ランタイムデータベース（`*.db*`）、取得結果ファイル（`available*.txt`、`taken*.txt`、`results/`）、コンパイル済みバイナリ（`*.exe`、`*.apk`）のコミットを未然に遮断する強固な `.gitignore` が設定されています。
- 常に `config/.env.example`、`config/config.example.yaml`、`data/surfshark_credentials.example.json` テンプレートを複製して利用してください。
- ソースコードおよび公式文書のいかなる場所にも、秘密鍵やパスワードはハードコードされていません。"""
            },
            {
                "title": "2. ネットワーク分離とレート制限の安全性",
                "id": "-2-ネットワーク分離とレート制限の安全性",
                "content": """- 全てのHTTPリクエストは `curl_cffi` による Chrome 131 TLS ステルス偽装を経由し、ユーザ空間 HTTP/SOCKS5 分離トンネル（`wireproxy`）を通じてルーティングされます。
- ホストOSの標準ネットワークインターフェース、ルーティングテーブル、DNS設定は一切変更されません。
- 429検出時は0.3秒未満で自動ホットスワップが実行され、特定IPへの過度な負荷集中を防ぎます。"""
            },
            {
                "title": "3. セキュリティ脆弱性の報告 (Reporting a Security Issue)",
                "id": "-3-セキュリティ脆弱性の報告-reporting-a-security-issue",
                "content": """- セキュリティ脆弱性や誤ったシークレット公開を発見した場合は、公開イシューを作成せず、GitHub の **Private Security Advisory** 経由で非公開にてご報告ください。
- またはリポジトリ所有者（`KRCUPRO`）へ直接ご連絡いただければ、24時間以内に調査および修正パッチを発行します。"""
            },
            {
                "title": "4. 責任ある研究と倫理規定",
                "id": "-4-責任ある研究と倫理規定",
                "content": """- 本プログラムは、TLSフィンガープリント、非同期プロキシプール管理、並行ネットワークプログラミングの学習および学術研究目的でのみ提供されます。
- DoS/DDoS攻撃や第三者サービスの規約を侵害する不正使用を固く禁止します。"""
            }
        ]
    },
    "zh-CN": {
        "title": "🛡️ 安全政策 (Security Policy)",
        "desc": "D4UC 安全准则、密钥凭据保护规范与漏洞披露机制",
        "sections": [
            {
                "title": "1. 凭据与私钥保护规范",
                "id": "-1-凭据与私钥保护规范",
                "content": """- **切勿将 `config.yaml`、`.env`、`surfshark_credentials.json` 或 `*.conf` 提交到版本控制系统中。**
- 本仓库配备了经过严格加固的 `.gitignore`，可全面拦截本地凭据、运行时数据库（`*.db*`）、扫描结果文件（`available*.txt`、`taken*.txt`、`results/`）以及编译生成的二进制文件（`*.exe`、`*.apk`）。
- 请始终通过复制 `config/.env.example`、`config/config.example.yaml` 和 `data/surfshark_credentials.example.json` 模板来进行个性化配置。
- 源代码及官方文档中绝不包含任何硬编码的私钥、令牌或敏感路径。"""
            },
            {
                "title": "2. 网络隔离与速率限制安全",
                "id": "-2-网络隔离与速率限制安全",
                "content": """- 所有 HTTP 请求均采用基于 `curl_cffi` 的 Chrome 131 TLS 隐形指纹伪装，并通过独立用户空间 HTTP/SOCKS5 隧道（`wireproxy`）进行路由转发。
- 宿主机操作系统的物理网卡、默认路由表与系统 DNS 设置均完全不受影响。
- 遭遇 429 限流时，系统将在 0.3 秒内自动完成原子热切换，防止单一 IP 遭受持续封禁。"""
            },
            {
                "title": "3. 安全漏洞报告 (Reporting a Security Issue)",
                "id": "-3-安全漏洞报告-reporting-a-security-issue",
                "content": """- 若您发现潜在安全漏洞或凭据泄漏事件，请切勿通过公开 Issue 发布。
- 请直接通过 GitHub **Private Security Advisory** 提交私密报告，或直接联系项目维护者（`KRCUPRO`）。我们将在 24 小时内进行响应与修复。"""
            },
            {
                "title": "4. 负责任的研究与合规守则",
                "id": "-4-负责任的研究与合规守则",
                "content": """- 本工具专为学习高并发网络编程、TLS JA3/JA4 模拟、多隧道代理池编排而设计。
- 严禁将其用于 DoS/DDoS 攻击或任何侵犯第三方服务条款的行为。"""
            }
        ]
    },
    "es": {
        "title": "🛡️ Política de Seguridad (Security Policy)",
        "desc": "Directrices de Seguridad de D4UC, Protección de Secretos y Divulgación Responsable",
        "sections": [
            {
                "title": "1. Protección de Credenciales y Claves Privadas",
                "id": "-1-protección-de-credenciales-y-claves-privadas",
                "content": """- **Nunca subas `config.yaml`, `.env`, `surfshark_credentials.json` o `*.conf` al control de versiones (Git).**
- Este repositorio incluye un `.gitignore` blindado para bloquear credenciales locales, bases de datos en tiempo de ejecución (`*.db*`), resultados de escaneo (`available*.txt`, `taken*.txt`, `results/`) y binarios compilados (`*.exe`, `*.apk`).
- Comienza siempre duplicando las plantillas oficiales: `config/.env.example`, `config/config.example.yaml` y `data/surfshark_credentials.example.json`.
- Ninguna clave privada, token personal ni credencial propietaria está incrustada en el código fuente o documentación."""
            },
            {
                "title": "2. Aislamiento de Red y Seguridad ante Límites de Tasa",
                "id": "-2-aislamiento-de-red-y-seguridad-ante-límites-de-tasa",
                "content": """- Todas las peticiones HTTP implementan suplantación TLS sigilosa Chrome 131 mediante `curl_cffi`, enrutadas a través de túneles aislados en espacio de usuario (`wireproxy`).
- Las interfaces de red del sistema operativo anfitrión, tablas de enrutamiento y servidores DNS no sufren ninguna alteración.
- Al detectar un código 429, el motor ejecuta un reemplazo atómico en caliente en menos de 0.3 segundos, distribuyendo la carga de manera segura."""
            },
            {
                "title": "3. Notificación de Incidentes de Seguridad",
                "id": "-3-notificación-de-incidentes-de-seguridad",
                "content": """- Si detectas una vulnerabilidad o exposición accidental de credenciales, por favor NO abras una incidencia pública.
- Emplea la herramienta **Private Security Advisory** de GitHub o contacta al propietario del repositorio (`KRCUPRO`). Los reportes verificados reciben un parche en menos de 24 horas."""
            },
            {
                "title": "4. Investigación Responsable y Ética",
                "id": "-4-investigación-responsable-y-ética",
                "content": """- D4UC ha sido desarrollado exclusivamente con fines educativos para el estudio de huellas TLS, orquestación asíncrona de proxies y arquitectura distribuida.
- Queda terminantemente prohibido el uso para ataques DoS/DDoS o vulneración de términos de servicio de terceros."""
            }
        ]
    },
    "fr": {
        "title": "🛡️ Politique de Sécurité (Security Policy)",
        "desc": "Directives de sécurité D4UC, protection des secrets et divulgation responsable",
        "sections": [
            {
                "title": "1. Protection des Identifiants et des Clés Privées",
                "id": "-1-protection-des-identifiants-et-des-clés-privées",
                "content": """- **Ne committez jamais `config.yaml`, `.env`, `surfshark_credentials.json` ou `*.conf` dans le dépôt Git.**
- Ce dépôt intègre un fichier `.gitignore` renforcé interdisant les identifiants locaux, bases de données de session (`*.db*`), fichiers de résultats (`available*.txt`, `taken*.txt`, `results/`) et binaires (`*.exe`, `*.apk`).
- Utilisez systématiquement les fichiers modèles fournis : `config/.env.example`, `config/config.example.yaml` et `data/surfshark_credentials.example.json`.
- Aucun secret, jeton d'authentification ou clé WireGuard n'est codé en dur dans le code source ou la documentation."""
            },
            {
                "title": "2. Isolation Réseau et Maîtrise du Rate-Limiting",
                "id": "-2-isolation-réseau-et-maîtrise-du-rate-limiting",
                "content": """- L'intégralité des requêtes HTTP exploite l'empreinte TLS furtive Chrome 131 (`curl_cffi`) acheminée via des tunnels en espace utilisateur (`wireproxy`).
- Les cartes réseau, la table de routage principale et les paramètres DNS de votre machine hôte restent totalement préservés.
- Dès détection d'un statut 429, un basculement atomique immédiat s'effectue en moins de 0,3 s sans interrompre les autres flux de travail."""
            },
            {
                "title": "3. Signalement d'une Vulnérabilité",
                "id": "-3-signalement-dune-vulnérabilité",
                "content": """- En cas de découverte d'une faille de sécurité ou d'une fuite de données, n'ouvrez pas d'issue publique.
- Transmettez un rapport confidentiel via l'outil **Private Security Advisory** de GitHub ou joignez directement l'auteur (`KRCUPRO`). Une correction sera déployée sous 24h."""
            },
            {
                "title": "4. Démarche Éthique et Recherche Responsable",
                "id": "-4-démarche-éthique-et-recherche-responsable",
                "content": """- D4UC est conçu à des fins d'apprentissage technique et de recherche sur les protocoles TLS, la gestion asynchrone de proxies et les architectures concurrentes.
- Toute utilisation abusive, attaque par déni de service (DDoS) ou contournement illicite est rigoureusement interdite."""
            }
        ]
    },
    "de": {
        "title": "🛡️ Sicherheitsrichtlinie (Security Policy)",
        "desc": "D4UC Sicherheitsrichtlinien, Schutz von Geheimnissen und koordinierte Offenlegung",
        "sections": [
            {
                "title": "1. Schutz von Zugangsdaten und privaten Schlüsseln",
                "id": "-1-schutz-von-zugangsdaten-und-privaten-schlüsseln",
                "content": """- **Übertragen Sie `config.yaml`, `.env`, `surfshark_credentials.json` oder `*.conf` niemals in die Versionsverwaltung (Git).**
- Dieses Repository enthält eine gehärtete `.gitignore`-Datei, die lokale Anmeldedaten, Datenbanken (`*.db*`), Ergebnisdateien (`available*.txt`, `taken*.txt`, `results/`) und kompilierte Binärdateien (`*.exe`, `*.apk`) zuverlässig ausschließt.
- Nutzen Sie stets die Vorlagendateien: `config/.env.example`, `config/config.example.yaml` und `data/surfshark_credentials.example.json`.
- Im gesamten Quellcode und in der Dokumentation sind keinerlei private Schlüssel oder Passwörter fest einprogrammiert."""
            },
            {
                "title": "2. Netzwerkisolation und Rate-Limit-Sicherheit",
                "id": "-2-netzwerkisolation-und-rate-limit-sicherheit",
                "content": """- Alle HTTP-Anfragen nutzen Chrome 131 TLS-Tarnung über `curl_cffi`, geroutet durch isolierte User-Space-Tunnel (`wireproxy`).
- Netzwerkkarten, Routing-Tabellen und DNS-Konfigurationen des Host-Betriebssystems bleiben zu 100 % unverändert.
- Bei Erreichen eines HTTP 429 führt die Engine innerhalb von 0,3 Sekunden einen atomaren Hot-Swap zu einem alternativen Tunnel durch."""
            },
            {
                "title": "3. Meldung von Sicherheitslücken",
                "id": "-3-meldung-von-sicherheitslücken",
                "content": """- Falls Sie eine Schwachstelle oder versehentlich exponierte Schlüssel entdecken, eröffnen Sie bitte kein öffentliches Ticket.
- Erstellen Sie stattdessen einen vertraulichen Bericht über GitHub **Private Security Advisory** oder wenden Sie sich direkt an den Repository-Inhaber (`KRCUPRO`). Verifizierte Meldungen werden innerhalb von 24 Stunden behoben."""
            },
            {
                "title": "4. Verantwortungsbewusste Forschung & Ethik",
                "id": "-4-verantwortungsbewusste-forschung--ethik",
                "content": """- D4UC dient ausschließlich Bildungs- und Forschungszwecken in den Bereichen TLS-Fingerprinting, asynchrone Proxy-Pools und Hochleistungsnetzwerke.
- Angriffe zur Dienstverweigerung (DoS/DDoS) oder unautorisierte Aktivitäten sind ausdrücklich untersagt."""
            }
        ]
    },
    "ru": {
        "title": "🛡️ Политика безопасности (Security Policy)",
        "desc": "Правила безопасности D4UC, защита секретов и ответственное раскрытие уязвимостей",
        "sections": [
            {
                "title": "1. Защита учетных данных и приватных ключей",
                "id": "-1-защита-учетных-данных-и-приватных-ключей",
                "content": """- **Никогда не фиксируйте `config.yaml`, `.env`, `surfshark_credentials.json` или `*.conf` в репозитории Git.**
- Репозиторий содержит строгую конфигурацию `.gitignore`, предотвращающую коммит локальных ключей, баз данных (`*.db*`), файлов результатов (`available*.txt`, `taken*.txt`, `results/`) и бинарных сборок (`*.exe`, `*.apk`).
- Всегда создавайте рабочие конфигурации из шаблонов: `config/.env.example`, `config/config.example.yaml` и `data/surfshark_credentials.example.json`.
- В исходном коде и документации отсутствуют жестко закодированные пароли, ключи WireGuard или приватные токены."""
            },
            {
                "title": "2. Сетевая изоляция и безопасность от Rate-Limit",
                "id": "-2-сетевая-изоляция-и-безопасность-от-rate-limit",
                "content": """- Все HTTP-запросы используют маскировку TLS Chrome 131 (`curl_cffi`), маршрутизируемую через изолированные туннели в пространстве пользователя (`wireproxy`).
- Сетевые интерфейсы операционной системы хоста, системная таблица маршрутизации и параметры DNS не затрагиваются.
- При получении статуса 429 движок производит атомарную горячую замену узла менее чем за 0.3 секунды, исключая перегрузку IP-адресов."""
            },
            {
                "title": "3. Сообщение об уязвимости",
                "id": "-3-сообщение-об-уязвимости",
                "content": """- При обнаружении уязвимости безопасности или утечки ключей убедительно просим не открывать публичные Issues.
- Отправьте отчет через GitHub **Private Security Advisory** или свяжитесь с владельцем репозитория (`KRCUPRO`) напрямую. Исправление выпускается в течение 24 часов."""
            },
            {
                "title": "4. Ответственные исследования и этика",
                "id": "-4-ответственные-исследования-и-этика",
                "content": """- Программа D4UC разработана исключительно для изучения технологий TLS-маскировки, асинхронного управления пулами прокси и параллельного программирования.
- Использование в деструктивных целях, атаках типа DoS/DDoS или нарушение правил сторонних сервисов строго запрещено."""
            }
        ]
    },
    "pt-BR": {
        "title": "🛡️ Política de Segurança (Security Policy)",
        "desc": "Diretrizes de Segurança D4UC, Proteção de Segredos e Divulgação Responsável",
        "sections": [
            {
                "title": "1. Proteção de Credenciais e Chaves Privadas",
                "id": "-1-proteção-de-credenciais-e-chaves-privadas",
                "content": """- **Nunca envie `config.yaml`, `.env`, `surfshark_credentials.json` ou `*.conf` para o controle de versão (Git).**
- Este repositório inclui um `.gitignore` reforçado que bloqueia credenciais locais, bancos de dados em execução (`*.db*`), arquivos de resultados (`available*.txt`, `taken*.txt`, `results/`) e binários compilados (`*.exe`, `*.apk`).
- Configure seu ambiente copiando os modelos oficiais: `config/.env.example`, `config/config.example.yaml` e `data/surfshark_credentials.example.json`.
- Nenhum segredo ou chave privada está inserido de forma fixa no código-fonte ou na documentação."""
            },
            {
                "title": "2. Isolamento de Rede e Segurança Contra Rate-Limit",
                "id": "-2-isolamento-de-rede-e-segurança-contra-rate-limit",
                "content": """- Todas as requisições HTTP utilizam camuflagem TLS Chrome 131 (`curl_cffi`) roteadas por túneis isolados em espaço de usuário (`wireproxy`).
- As interfaces de rede do sistema operacional host, tabelas de roteamento e servidores DNS permanecem 100% inalterados.
- Ao identificar um código 429, o sistema efetua um hot-swap atômico em menos de 0,3s, garantindo rotação contínua e segura."""
            },
            {
                "title": "3. Notificação de Vulnerabilidades",
                "id": "-3-notificação-de-vulnerabilidades",
                "content": """- Ao encontrar falhas de segurança ou vazamento involuntário de credenciais, evite abrir problemas públicos.
- Envie um relatório sigiloso através do GitHub **Private Security Advisory** ou fale diretamente com o mantenedor (`KRCUPRO`). Resposta e correção em até 24 horas."""
            },
            {
                "title": "4. Pesquisa Ética e Uso Responsável",
                "id": "-4-pesquisa-ética-e-uso-responsável",
                "content": """- O D4UC é desenvolvido exclusivamente para estudo acadêmico de impressões digitais TLS, gestão de proxies assíncronos e arquiteturas concorrentes.
- É expressamente proibida sua utilização em ataques de negação de serviço (DoS/DDoS) ou em desacordo com termos de serviço de terceiros."""
            }
        ]
    },
    "ar": {
        "title": "🛡️ سياسة الأمان (Security Policy)",
        "desc": "إرشادات الأمان لمشروع D4UC، وحماية البيانات السرية والإبلاغ المسؤول عن الثغرات",
        "sections": [
            {
                "title": "1. حماية بيانات الاعتماد والمفاتيح الخاصة",
                "id": "-1-حماية-بيانات-الاعتماد-والمفاتيح-الخاصة",
                "content": """- **يُحظر تماماً إرسال أو تضمين ملفات `config.yaml` أو `.env` أو `surfshark_credentials.json` أو `*.conf` في مستودع Git.**
- يتضمن هذا المستودع ملف `.gitignore` صارم يمنع حفظ بيانات الاعتماد المحلية وقواعد البيانات (`*.db*`) ونتائج الفحص والملفات التنفيذية (`*.exe`، `*.apk`).
- ابدأ دائماً بنسخ قوالب التهيئة الرسمية المتوفرة في `config/.env.example` و `config/config.example.yaml` و `data/surfshark_credentials.example.json`.
- لا توجد أي مفاتيح خاصة أو كلمات مرور مضمنة داخل الكود البرمجي أو التوثيق الرسمي."""
            },
            {
                "title": "2. العزل الشبكي وأمان حدود الطلبات (Rate-Limit)",
                "id": "-2-العزل-الشبكي-وأمان-حدود-الطلبات-rate-limit",
                "content": """- تعتمد جميع طلبات HTTP على محاكاة بصمة Chrome 131 TLS الخفية عبر `curl_cffi` الموجهة من خلال أنفاق معزولة في مساحة المستخدم (`wireproxy`).
- تظل بطاقات الشبكة وجداول التوجيه وإعدادات DNS لنظام التشغيل المضيف سليمة وغير معدلة بنسبة 100%.
- عند تلقي الرمز 429، يقوم المحرك بالتبديل الفوري التلقائي (Hot-Swap) خلال أقل من 0.3 ثانية لمنع تراكم الطلبات على عنوان IP واحد."""
            },
            {
                "title": "3. الإبلاغ عن الثغرات الأمنية",
                "id": "-3-الإبلاغ-عن-الثغرات-الأمنية",
                "content": """- إذا اكتشفت ثغرة أمنية أو تسريباً غير مقصود للبيانات، يُرجى عدم فتح مشكلة عامة على المستودع.
- بدلاً من ذلك، يُرجى إرسال تقرير خاص عبر **Private Security Advisory** على GitHub أو التواصل مباشرة مع مالك المشروع (`KRCUPRO`). نلتزم بتقديم الحلول خلال 24 ساعة."""
            },
            {
                "title": "4. البحث المسؤول والممارسات الأخلاقية",
                "id": "-4-البحث-المسؤول-والممارسات-الأخلاقية",
                "content": """- تم تطوير D4UC لأغراض تعليمية وبحثية تتعلق بدراسة بصمات TLS وهندسة الشبكات غير المتزامنة وبرمجة التزامن العالي.
- يُحظر استخدام البرنامج في شن هجمات حجب الخدمة (DoS/DDoS) أو انتهاك شروط استخدام أي منصات أخرى."""
            }
        ]
    },
    "hi": {
        "title": "🛡️ सुरक्षा नीति (Security Policy)",
        "desc": "D4UC सुरक्षा दिशानिर्देश, क्रेडेंशियल सुरक्षा नियम और उत्तरदायी प्रकटीकरण नीति",
        "sections": [
            {
                "title": "1. क्रेडेंशियल और निजी कुंजी सुरक्षा नियम",
                "id": "-1-क्रेडेंशियल-और-निजी-कुंजी-सुरक्षा-नियम",
                "content": """- **`config.yaml`, `.env`, `surfshark_credentials.json`, या `*.conf` को कभी भी Git रिपॉजिटरी में कमिट न करें।**
- इस रिपॉजिटरी में एक सख्त `.gitignore` शामिल है जो स्थानीय क्रेडेंशियल, डेटाबेस (`*.db*`), परिणाम फ़ाइलें (`available*.txt`, `taken*.txt`) और बाइनरी (`*.exe`, `*.apk`) को स्वचालित रूप से ब्लॉक करता है।
- हमेशा दिए गए टेम्प्लेट से शुरुआत करें: `config/.env.example`, `config/config.example.yaml`, और `data/surfshark_credentials.example.json`।
- स्रोत कोड या आधिकारिक दस्तावेज़ों में कोई भी संवेदनशील निजी कुंजी या टोकन हार्डकोड नहीं किया गया है।"""
            },
            {
                "title": "2. नेटवर्क अलगाव और दर-सीमा (Rate-Limit) सुरक्षा",
                "id": "-2-नेटवर्क-अलगाव-और-दर-सीमा-rate-limit-सुरक्षा",
                "content": """- सभी HTTP अनुरोध Chrome 131 TLS स्टेल्थ फिंगरप्रिंट (`curl_cffi`) के माध्यम से यूजर-स्पेस आइसोलेटेड टनल (`wireproxy`) द्वारा रूट किए जाते हैं।
- होस्ट ऑपरेटिंग सिस्टम के भौतिक नेटवर्क एडेप्टर, रूटिंग टेबल और DNS सेटिंग्स पूरी तरह से अपरिवर्तित रहते हैं।
- 429 त्रुटि का पता चलने पर, इंजन 0.3 सेकंड के भीतर स्वचालित हॉट-स्वैप निष्पादित करता है ताकि किसी एक आईपी पर अत्यधिक ट्रैफ़िक केंद्रित न हो।"""
            },
            {
                "title": "3. सुरक्षा भेद्यता रिपोर्टिंग (Reporting a Security Issue)",
                "id": "-3-सुरक्षा-भेद्यता-रिपोर्टिंग-reporting-a-security-issue",
                "content": """- यदि आपको कोई सुरक्षा भेद्यता या अनपेक्षित क्रेडेंशियल रिसाव मिलता है, तो कृपया सार्वजनिक समस्या (Issue) न खोलें।
- इसके बजाय, GitHub के **Private Security Advisory** के माध्यम से निजी तौर पर रिपोर्ट सबमिट करें या रिपॉजिटरी स्वामी (`KRCUPRO`) से सीधे संपर्क करें। 24 घंटे के भीतर पैच जारी किया जाएगा।"""
            },
            {
                "title": "4. उत्तरदायी अनुसंधान और नैतिक दिशानिर्देश",
                "id": "-4-उत्तरदायी-अनुसंधान-और-नैतिक-दिशानिर्देश",
                "content": """- D4UC विशुद्ध रूप से TLS फिंगरप्रिंटिंग, अतुल्यकालिक प्रॉक्सी ऑर्केस्ट्रेशन और उच्च-समवर्ती नेटवर्क आर्किटेक्चर के अध्ययन के लिए विकसित किया गया है।
- सेवा से वंचित करने वाले हमलों (DoS/DDoS) या तीसरे पक्ष की सेवा शर्तों के उल्लंघन के लिए इसका उपयोग सख्त वर्जित है।"""
            }
        ]
    },
    "id": {
        "title": "🛡️ Kebijakan Keamanan (Security Policy)",
        "desc": "Panduan Keamanan D4UC, Perlindungan Kredensial, dan Pengungkapan Bertanggung Jawab",
        "sections": [
            {
                "title": "1. Perlindungan Kredensial & Kunci Privat",
                "id": "-1-perlindungan-kredensial--kunci-privat",
                "content": """- **Jangan pernah melakukan commit file `config.yaml`, `.env`, `surfshark_credentials.json`, atau `*.conf` ke dalam Git.**
- Repositori ini dilengkapi dengan konfigurasi `.gitignore` yang ketat untuk mencegah terunggahnya kredensial lokal, database sesi (`*.db*`), hasil pemindaian (`available*.txt`, `taken*.txt`, `results/`), serta biner hasil kompilasi (`*.exe`, `*.apk`).
- Selalu salin konfigurasi awal dari templat yang disediakan: `config/.env.example`, `config/config.example.yaml`, dan `data/surfshark_credentials.example.json`.
- Tidak ada kredensial pribadi, kunci WireGuard, atau token akses yang disematkan secara langsung di dalam kode sumber."""
            },
            {
                "title": "2. Isolasi Jaringan dan Keamanan Batas Kecepatan (Rate-Limit)",
                "id": "-2-isolasi-jaringan-dan-keamanan-batas-kecepatan-rate-limit",
                "content": """- Seluruh permintaan HTTP memanfaatkan peniruan TLS siluman Chrome 131 (`curl_cffi`) yang dirutekan melalui terowongan terisolasi ruang pengguna (`wireproxy`).
- Pengaturan adaptor jaringan fisik, tabel perutean utama, dan DNS pada sistem operasi host tetap 100% utuh tanpa perubahan.
- Saat kode respons 429 terdeteksi, mesin segera menjalankan hot-swap atomik dalam kurun waktu kurang dari 0,3 detik untuk mengalihkan rute secara mulus."""
            },
            {
                "title": "3. Pelaporan Kerentanan Keamanan",
                "id": "-3-pelaporan-kerentanan-keamanan",
                "content": """- Jika Anda menemukan celah keamanan atau paparan kredensial secara tidak sengaja, mohon TIDAK membuka issue publik.
- Kirimkan laporan rahasia melalui GitHub **Private Security Advisory** atau hubungi pengelola proyek (`KRCUPRO`) secara langsung. Laporan valid akan ditangani dalam waktu 24 jam."""
            },
            {
                "title": "4. Riset Bertanggung Jawab & Etika",
                "id": "-4-riset-bertanggung-jawab--etika",
                "content": """- D4UC dirancang khusus untuk pembelajaran teknis mengenai TLS fingerprinting, orkestrasi proxy asinkron, dan arsitektur konkurensi tinggi.
- Dilarang keras menggunakan program ini untuk serangan penolakan layanan (DoS/DDoS) atau pelanggaran ketentuan layanan pihak ketiga."""
            }
        ]
    }
}
