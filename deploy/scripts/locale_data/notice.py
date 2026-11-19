# deploy/scripts/locale_data/notice.py
"""
1:1 Full Localization for NOTICE.md across all 12 locales.
"""

NOTICE_DATA = {
    "ko": {
        "title": "📜 오픈소스 고지 및 라이선스 안내 (NOTICE)",
        "desc": "D4UC 프로젝트에 활용 및 참조된 제3자 오픈소스 패키지 및 라이선스 고지사항",
        "intro": "본 프로젝트는 다음의 오픈소스 라이브러리 및 도구를 사용하거나 참조하며, 각 패키지는 고유한 라이선스 조건에 따라 배포됩니다.",
        "packages": [
            {
                "name": "1. curl_cffi",
                "id": "-1-curl_cffi",
                "license": "MIT License",
                "desc": "BoringSSL 및 curl-impersonate 기반 Chrome 131 TLS/JA3/JA4 브라우저 스텔스 위장 네트워킹 스택."
            },
            {
                "name": "2. wireproxy",
                "id": "-2-wireproxy",
                "license": "ISC License",
                "desc": "OS 네트워크 설정 변경 없이 유저스페이스에서 WireGuard 프로토콜을 로컬 HTTP/SOCKS5 프록시로 변환하는 독립 바이너리 (https://github.com/pufferffish/wireproxy)."
            },
            {
                "name": "3. CustomTkinter",
                "id": "-3-customtkinter",
                "license": "MIT License",
                "desc": "모던 다크 테마 및 반응형 UI 컴포넌트를 제공하는 Python GUI 라이브러리."
            },
            {
                "name": "4. Rich",
                "id": "-4-rich",
                "license": "MIT License",
                "desc": "터미널 헤드리스 대시보드, 다중 프로그레스 바 및 텔레메트리 로그 렌더링 라이브러리."
            },
            {
                "name": "5. PyYAML",
                "id": "-5-pyyaml",
                "license": "MIT License",
                "desc": "YAML 포맷 설정 파일 파싱 및 덤프 엔진."
            },
            {
                "name": "6. 업스트림 영감 및 개념 참조 (Upstream Inspiration Reference)",
                "id": "-6-업스트림-영감-및-개념-참조-upstream-inspiration-reference",
                "license": "Reference Only",
                "desc": "초기 개념 프로토타입 단계에서 `camt4372/Discord-4Character-Usernames-Checker`를 참고하였으며, 이후 비동기 오케스트레이션, TLS 스텔스 위장, 1:1 다중 터널 프록시 풀 격리, SQLite WAL 다중 프로세스 동기화 및 크로스 플랫폼 패키징을 통해 전면 신규 설계·재구축되었습니다."
            }
        ]
    },
    "en": {
        "title": "📜 Third-Party Open-Source & Upstream Notices",
        "desc": "Attributions, Licenses, and Upstream References for D4UC Dependencies",
        "intro": "This project references or depends on the following third-party open-source packages and tools, each governed by its own respective license:",
        "packages": [
            {
                "name": "1. curl_cffi",
                "id": "-1-curl_cffi",
                "license": "MIT License",
                "desc": "TLS/JA3/JA4 browser impersonation networking stack built on BoringSSL / curl-impersonate."
            },
            {
                "name": "2. wireproxy",
                "id": "-2-wireproxy",
                "license": "ISC License",
                "desc": "User-space WireGuard client exposing isolated local HTTP/SOCKS5 proxies without root privileges (https://github.com/pufferffish/wireproxy)."
            },
            {
                "name": "3. CustomTkinter",
                "id": "-3-customtkinter",
                "license": "MIT License",
                "desc": "Modern themed Tkinter wrapper for Python desktop GUI."
            },
            {
                "name": "4. Rich",
                "id": "-4-rich",
                "license": "MIT License",
                "desc": "Terminal UI dashboard, progress rendering, and formatted telemetry logs."
            },
            {
                "name": "5. PyYAML",
                "id": "-5-pyyaml",
                "license": "MIT License",
                "desc": "YAML configuration parser and emitter."
            },
            {
                "name": "6. Upstream Inspiration Reference",
                "id": "-6-upstream-inspiration-reference",
                "license": "Reference Only",
                "desc": "Initial concept exploration referenced `camt4372/Discord-4Character-Usernames-Checker`, later rebuilt from the ground up with asynchronous orchestration, TLS impersonation, isolated multi-tunnel proxy rotation, SQLite WAL synchronization, and cross-platform packaging."
            }
        ]
    },
    "ja": {
        "title": "📜 オープンソース告知およびライセンス案内 (NOTICE)",
        "desc": "D4UCプロジェクトで使用および参照されているサードパーティ製オープンソース告知",
        "intro": "本プロジェクトは以下のサードパーティ製オープンソースソフトウェアを利用または参照しており、各パッケージはそれぞれのライセンス条件に従います。",
        "packages": [
            {
                "name": "1. curl_cffi",
                "id": "-1-curl_cffi",
                "license": "MIT License",
                "desc": "BoringSSL / curl-impersonate をベースとした Chrome 131 TLS/JA3/JA4 ステルス偽装ネットワークスタック。"
            },
            {
                "name": "2. wireproxy",
                "id": "-2-wireproxy",
                "license": "ISC License",
                "desc": "管理者権限なしでユーザ空間において WireGuard 通信をローカル HTTP/SOCKS5 に変換する軽量バイナリ (https://github.com/pufferffish/wireproxy)。"
            },
            {
                "name": "3. CustomTkinter",
                "id": "-3-customtkinter",
                "license": "MIT License",
                "desc": "モダンなダークテーマとウィジェットを提供する Python デスクトップ GUI ライブラリ。"
            },
            {
                "name": "4. Rich",
                "id": "-4-rich",
                "license": "MIT License",
                "desc": "ターミナルダッシュボード、進捗状況の描画およびログ出力ライブラリ。"
            },
            {
                "name": "5. PyYAML",
                "id": "-5-pyyaml",
                "license": "MIT License",
                "desc": "YAML 設定ファイルの解析および出力エンジン。"
            },
            {
                "name": "6. アップストリーム参照およびインスピレーション",
                "id": "-6-アップストリーム参照およびインスピレーション",
                "license": "Reference Only",
                "desc": "初期プロトタイプ検討時に `camt4372/Discord-4Character-Usernames-Checker` を参照し、その後、非同期オーケストレーション、TLSステルス偽装、複数国トンネル隔離、SQLite WAL同期およびクロスプラットフォーム対応に伴いゼロから全面再構築されました。"
            }
        ]
    },
    "zh-CN": {
        "title": "📜 开源声明与第三方许可说明 (NOTICE)",
        "desc": "D4UC 项目中所引用和依赖的第三方开源软件包归属声明",
        "intro": "本项目依赖或参考了以下第三方开源组件及工具，每个组件均受其各自官方开源许可协议的管辖：",
        "packages": [
            {
                "name": "1. curl_cffi",
                "id": "-1-curl_cffi",
                "license": "MIT License",
                "desc": "基于 BoringSSL / curl-impersonate 构建的 Chrome 131 TLS/JA3/JA4 浏览器隐形网络栈。"
            },
            {
                "name": "2. wireproxy",
                "id": "-2-wireproxy",
                "license": "ISC License",
                "desc": "无需 Root 权限即可在用户空间将 WireGuard 流量暴露为本地 HTTP/SOCKS5 代理的独立工具 (https://github.com/pufferffish/wireproxy)。"
            },
            {
                "name": "3. CustomTkinter",
                "id": "-3-customtkinter",
                "license": "MIT License",
                "desc": "专为 Python 桌面图形界面打造的现代主题 Tkinter UI 封装库。"
            },
            {
                "name": "4. Rich",
                "id": "-4-rich",
                "license": "MIT License",
                "desc": "用于终端无头仪表盘渲染、进度条展示与结构化遥测日志的高性能库。"
            },
            {
                "name": "5. PyYAML",
                "id": "-5-pyyaml",
                "license": "MIT License",
                "desc": "YAML 配置文件解析与序列化组件。"
            },
            {
                "name": "6. 上游灵感与概念参考 (Upstream Inspiration Reference)",
                "id": "-6-上游灵感与概念参考-upstream-inspiration-reference",
                "license": "Reference Only",
                "desc": "在早期概念验证阶段曾参考 `camt4372/Discord-4Character-Usernames-Checker`，后通过完全异步编排、TLS 隐形伪装、独立多隧道隔离轮询、SQLite WAL 多进程安全同步以及跨平台打包进行了彻底的重新构架与研发。"
            }
        ]
    },
    "es": {
        "title": "📜 Avisos de Terceros y Código Abierto (NOTICE)",
        "desc": "Atribuciones, Licencias y Referencias Upstream para las dependencias de D4UC",
        "intro": "Este proyecto hace uso o referencia de los siguientes paquetes y utilidades de código abierto de terceros, gobernados por sus respectivas licencias:",
        "packages": [
            {
                "name": "1. curl_cffi",
                "id": "-1-curl_cffi",
                "license": "MIT License",
                "desc": "Pila de red con suplantación de huella TLS/JA3/JA4 basada en BoringSSL y curl-impersonate."
            },
            {
                "name": "2. wireproxy",
                "id": "-2-wireproxy",
                "license": "ISC License",
                "desc": "Cliente WireGuard en espacio de usuario que expone proxies locales HTTP/SOCKS5 sin privilegios de root (https://github.com/pufferffish/wireproxy)."
            },
            {
                "name": "3. CustomTkinter",
                "id": "-3-customtkinter",
                "license": "MIT License",
                "desc": "Envoltorio moderno para Tkinter con soporte de temas oscuros en Python."
            },
            {
                "name": "4. Rich",
                "id": "-4-rich",
                "license": "MIT License",
                "desc": "Panel de control en terminal, barras de progreso y registro telemétrico enriquecido."
            },
            {
                "name": "5. PyYAML",
                "id": "-5-pyyaml",
                "license": "MIT License",
                "desc": "Analizador y emisor de archivos de configuración en formato YAML."
            },
            {
                "name": "6. Referencia de Inspiración Upstream",
                "id": "-6-referencia-de-inspiración-upstream",
                "license": "Reference Only",
                "desc": "La exploración conceptual inicial tomó como referencia `camt4372/Discord-4Character-Usernames-Checker`, habiendo sido reconstruida íntegramente desde cero con orquestación asíncrona, sigilo TLS, rotación multicanal aislada, sincronización SQLite WAL y empaquetado multiplataforma."
            }
        ]
    },
    "fr": {
        "title": "📜 Mentions Légales et Logiciels Tiers (NOTICE)",
        "desc": "Attributions, licences et références upstream des composants intégrés à D4UC",
        "intro": "Ce projet intègre ou s'appuie sur les bibliothèques logicielles open-source tierces suivantes, chacune étant soumise à ses propres termes de licence :",
        "packages": [
            {
                "name": "1. curl_cffi",
                "id": "-1-curl_cffi",
                "license": "MIT License",
                "desc": "Couche réseau furtive simulant l'empreinte TLS/JA3/JA4 de Chrome 131 basée sur BoringSSL."
            },
            {
                "name": "2. wireproxy",
                "id": "-2-wireproxy",
                "license": "ISC License",
                "desc": "Client WireGuard en espace utilisateur créant des proxys locaux HTTP/SOCKS5 sans droits administrateur (https://github.com/pufferffish/wireproxy)."
            },
            {
                "name": "3. CustomTkinter",
                "id": "-3-customtkinter",
                "license": "MIT License",
                "desc": "Interface graphique Python moderne avec thèmes sombres et design contemporain."
            },
            {
                "name": "4. Rich",
                "id": "-4-rich",
                "license": "MIT License",
                "desc": "Tableau de bord console, barres de défilement et affichage télémétrique formaté."
            },
            {
                "name": "5. PyYAML",
                "id": "-5-pyyaml",
                "license": "MIT License",
                "desc": "Moteur d'analyse et d'écriture pour fichiers de configuration YAML."
            },
            {
                "name": "6. Référence d'Inspiration Amont",
                "id": "-6-référence-dinspiration-amont",
                "license": "Reference Only",
                "desc": "La phase initiale a examiné `camt4372/Discord-4Character-Usernames-Checker`, avant une refonte totale et exclusive axée sur l'asynchronisme, la furtivité TLS, les tunnels isolés, la persistance SQLite WAL et la distribution multiplateforme."
            }
        ]
    },
    "de": {
        "title": "📜 Drittanbieter-Lizenzen und Hinweise (NOTICE)",
        "desc": "Zuordnungen, Lizenzen und Upstream-Referenzen für D4UC-Abhängigkeiten",
        "intro": "Dieses Projekt referenziert oder verwendet die folgenden Open-Source-Pakete und -Tools von Drittanbietern, die jeweils ihren eigenen Lizenzbedingungen unterliegen:",
        "packages": [
            {
                "name": "1. curl_cffi",
                "id": "-1-curl_cffi",
                "license": "MIT License",
                "desc": "Netzwerk-Stack zur Nachbildung von Chrome 131 TLS/JA3/JA4-Fingerabdrücken basierend auf BoringSSL."
            },
            {
                "name": "2. wireproxy",
                "id": "-2-wireproxy",
                "license": "ISC License",
                "desc": "User-Space-WireGuard-Client, der lokale HTTP/SOCKS5-Proxys ohne Root-Rechte bereitstellt (https://github.com/pufferffish/wireproxy)."
            },
            {
                "name": "3. CustomTkinter",
                "id": "-3-customtkinter",
                "license": "MIT License",
                "desc": "Moderne Tkinter-Oberfläche mit ansprechendem Dark-Mode für Python-Desktop-Anwendungen."
            },
            {
                "name": "4. Rich",
                "id": "-4-rich",
                "license": "MIT License",
                "desc": "Terminal-Dashboard, Fortschrittsanzeigen und strukturierte Telemetrieprotokolle."
            },
            {
                "name": "5. PyYAML",
                "id": "-5-pyyaml",
                "license": "MIT License",
                "desc": "Parser und Emitter für YAML-Konfigurationsdateien."
            },
            {
                "name": "6. Upstream-Inspirationsreferenz",
                "id": "-6-upstream-inspirationsreferenz",
                "license": "Reference Only",
                "desc": "Die ursprüngliche Konzeptstudie bezog sich auf `camt4372/Discord-4Character-Usernames-Checker` und wurde anschließend mit asynchroner Architektur, TLS-Tarnung, isolierten Multitunnel-Proxys, SQLite WAL und Multi-Plattform-Distribution von Grund auf neu entwickelt."
            }
        ]
    },
    "ru": {
        "title": "📜 Уведомления об открытом ПО и лицензиях (NOTICE)",
        "desc": "Авторские права, лицензии и апстрим-источники сторонних компонентов D4UC",
        "intro": "Данный проект использует или ссылается на следующие сторонние пакеты с открытым исходным кодом, каждый из которых регулируется собственной лицензией:",
        "packages": [
            {
                "name": "1. curl_cffi",
                "id": "-1-curl_cffi",
                "license": "MIT License",
                "desc": "Сетевой стек с поддержкой маскировки отпечатков TLS/JA3/JA4 Chrome 131 на базе BoringSSL."
            },
            {
                "name": "2. wireproxy",
                "id": "-2-wireproxy",
                "license": "ISC License",
                "desc": "Клиент WireGuard в пользовательском пространстве, предоставляющий локальные HTTP/SOCKS5 прокси без root-прав (https://github.com/pufferffish/wireproxy)."
            },
            {
                "name": "3. CustomTkinter",
                "id": "-3-customtkinter",
                "license": "MIT License",
                "desc": "Библиотека современного графического интерфейса Tkinter с темной темой для Python."
            },
            {
                "name": "4. Rich",
                "id": "-4-rich",
                "license": "MIT License",
                "desc": "Инструмент отрисовки консольной панели управления, прогресс-баров и форматированных логов."
            },
            {
                "name": "5. PyYAML",
                "id": "-5-pyyaml",
                "license": "MIT License",
                "desc": "Парсер и генератор конфигурационных файлов в формате YAML."
            },
            {
                "name": "6. Апстрим-источник вдохновения (Upstream Inspiration Reference)",
                "id": "-6-апстрим-источник-вдохновения-upstream-inspiration-reference",
                "license": "Reference Only",
                "desc": "Первоначальное знакомство с концепцией базировалось на репозитории `camt4372/Discord-4Character-Usernames-Checker`, после чего проект был полностью переписан с нуля с использованием асинхронности, стелс-TLS, изолированных туннелей, SQLite WAL и кроссплатформенной сборки."
            }
        ]
    },
    "pt-BR": {
        "title": "📜 Notificações de Código Aberto e Licenças (NOTICE)",
        "desc": "Atribuições, Licenças e Referências Upstream para dependências do D4UC",
        "intro": "Este projeto utiliza ou faz referência aos seguintes pacotes e ferramentas de código aberto de terceiros, governados por seus respectivos termos de licença:",
        "packages": [
            {
                "name": "1. curl_cffi",
                "id": "-1-curl_cffi",
                "license": "MIT License",
                "desc": "Pilha de rede com camuflagem de impressão digital TLS/JA3/JA4 do Chrome 131 baseada em BoringSSL."
            },
            {
                "name": "2. wireproxy",
                "id": "-2-wireproxy",
                "license": "ISC License",
                "desc": "Cliente WireGuard em espaço de usuário que expõe proxies locais HTTP/SOCKS5 sem privilégios de root (https://github.com/pufferffish/wireproxy)."
            },
            {
                "name": "3. CustomTkinter",
                "id": "-3-customtkinter",
                "license": "MIT License",
                "desc": "Biblioteca para criação de interfaces gráficas modernas e responsivas em Python."
            },
            {
                "name": "4. Rich",
                "id": "-4-rich",
                "license": "MIT License",
                "desc": "Painel de controle em terminal, barras de progresso e renderização de telemetria."
            },
            {
                "name": "5. PyYAML",
                "id": "-5-pyyaml",
                "license": "MIT License",
                "desc": "Mecanismo de análise e geração de arquivos de configuração YAML."
            },
            {
                "name": "6. Referência de Inspiração Upstream",
                "id": "-6-referência-de-inspiração-upstream",
                "license": "Reference Only",
                "desc": "A exploração conceitual inicial tomou como referência `camt4372/Discord-4Character-Usernames-Checker`, sendo posteriormente redesenhada e reconstruída do zero com arquitetura assíncrona, TLS furtivo, túneis isolados, SQLite WAL e empacotamento multiplataforma."
            }
        ]
    },
    "ar": {
        "title": "📜 إشعارات المصادر المفتوحة والجهات الخارجية (NOTICE)",
        "desc": "الإسناد والترخيص والمراجع الأولية للمكتبات البرمجية المستخدمة في D4UC",
        "intro": "يعتمد هذا المشروع على حزم وأدوات برمجية مفتوحة المصدر تابعة لجهات خارجية، ويخضع كل منها لشروط ترخيصه الخاصة:",
        "packages": [
            {
                "name": "1. curl_cffi",
                "id": "-1-curl_cffi",
                "license": "MIT License",
                "desc": "حزمة شبكية لمحاكاة بصمة Chrome 131 TLS/JA3/JA4 الخفية مبنية على BoringSSL و curl-impersonate."
            },
            {
                "name": "2. wireproxy",
                "id": "-2-wireproxy",
                "license": "ISC License",
                "desc": "عميل WireGuard في مساحة المستخدم لتوفير بروكسي محلي HTTP/SOCKS5 دون الحاجة لصلاحيات المسؤول (https://github.com/pufferffish/wireproxy)."
            },
            {
                "name": "3. CustomTkinter",
                "id": "-3-customtkinter",
                "license": "MIT License",
                "desc": "مكتبة واجهة مستخدم رسومية عصرية تدعم الوضع الداكن لتطبيقات بايثون المكتبية."
            },
            {
                "name": "4. Rich",
                "id": "-4-rich",
                "license": "MIT License",
                "desc": "لوحة تحكم تفاعلية في سطر الأوامر وأشرطة تقدم وسجلات قياس أداء منسقة."
            },
            {
                "name": "5. PyYAML",
                "id": "-5-pyyaml",
                "license": "MIT License",
                "desc": "محرك قراءة وكتابة ملفات التكوين والإعدادات بصيغة YAML."
            },
            {
                "name": "6. مرجع الإلهام الأولي (Upstream Inspiration Reference)",
                "id": "-6-مرجع-الإلهام-الأولي-upstream-inspiration-reference",
                "license": "Reference Only",
                "desc": "استند النموذج الأولي للمشروع إلى `camt4372/Discord-4Character-Usernames-Checker`، ثم أُعيدت كتابة وبناء النظام بالكامل من الصفر بدعم التزامن غير المتزامن ومحاكاة TLS وأنفاق البروكسي وقواعد بيانات SQLite WAL ودعم مختلف أنظمة التشغيل."
            }
        ]
    },
    "hi": {
        "title": "📜 ओपन-सोर्स नोटिस और लाइसेंस सूचना (NOTICE)",
        "desc": "D4UC निर्भरताओं के लिए ओपन-सोर्स पैकेज एट्रिब्यूशन और संदर्भ",
        "intro": "यह प्रोजेक्ट निम्नलिखित तृतीय-पक्ष ओपन-सोर्स पैकेजों और उपकरणों का उपयोग या संदर्भ लेता है, जिनमें से प्रत्येक अपने संबंधित लाइसेंस द्वारा शासित है:",
        "packages": [
            {
                "name": "1. curl_cffi",
                "id": "-1-curl_cffi",
                "license": "MIT License",
                "desc": "BoringSSL पर निर्मित Chrome 131 TLS/JA3/JA4 ब्राउज़र प्रतिरूपण नेटवर्किंग स्टैक।"
            },
            {
                "name": "2. wireproxy",
                "id": "-2-wireproxy",
                "license": "ISC License",
                "desc": "रूट विशेषाधिकारों के बिना स्थानीय HTTP/SOCKS5 प्रॉक्सी प्रदान करने वाला यूजर-स्पेस WireGuard क्लाइंट (https://github.com/pufferffish/wireproxy)।"
            },
            {
                "name": "3. CustomTkinter",
                "id": "-3-customtkinter",
                "license": "MIT License",
                "desc": "पायथन डेस्कटॉप जीयूआई के लिए आधुनिक डार्क थीम आधारित Tkinter रैपर लाइब्रेरी।"
            },
            {
                "name": "4. Rich",
                "id": "-4-rich",
                "license": "MIT License",
                "desc": "टर्मिनल डैशबोर्ड, प्रगति बार और स्वरूपित टेलीमेट्री लॉग लाइब्रेरी।"
            },
            {
                "name": "5. PyYAML",
                "id": "-5-pyyaml",
                "license": "MIT License",
                "desc": "YAML कॉन्फ़िगरेशन फ़ाइल पार्सर और एमिटर इंजन।"
            },
            {
                "name": "6. अपस्ट्रीम प्रेरणा संदर्भ (Upstream Inspiration Reference)",
                "id": "-6-अपस्ट्रीम-प्रेरणा-संदर्भ-upstream-inspiration-reference",
                "license": "Reference Only",
                "desc": "प्रारंभिक अवधारणा अन्वेषण ने `camt4372/Discord-4Character-Usernames-Checker` को संदर्भित किया, जिसके बाद अतुल्यकालिक ऑर्केस्ट्रेशन, TLS स्टेल्थ, बहु-सुरंग अलगाव, SQLite WAL और क्रॉस-प्लेटफ़ॉर्म पैकेजिंग के साथ इसे पूरी तरह से फिर से बनाया गया।"
            }
        ]
    },
    "id": {
        "title": "📜 Pemberitahuan Sumber Terbuka & Lisensi Pihak Ketiga (NOTICE)",
        "desc": "Atribusi, Lisensi, dan Referensi Upstream untuk dependensi paket D4UC",
        "intro": "Proyek ini menggunakan dan merujuk pada paket perangkat lunak sumber terbuka (open-source) pihak ketiga berikut, yang masing-masing diatur oleh lisensi resminya sendiri:",
        "packages": [
            {
                "name": "1. curl_cffi",
                "id": "-1-curl_cffi",
                "license": "MIT License",
                "desc": "Tumpukan jaringan peniruan sidik jari TLS/JA3/JA4 Chrome 131 yang dibangun di atas BoringSSL."
            },
            {
                "name": "2. wireproxy",
                "id": "-2-wireproxy",
                "license": "ISC License",
                "desc": "Klien WireGuard ruang pengguna yang mengekspos proxy lokal HTTP/SOCKS5 tanpa hak akses root (https://github.com/pufferffish/wireproxy)."
            },
            {
                "name": "3. CustomTkinter",
                "id": "-3-customtkinter",
                "license": "MIT License",
                "desc": "Pembungkus Tkinter bertema modern untuk antarmuka grafis desktop Python."
            },
            {
                "name": "4. Rich",
                "id": "-4-rich",
                "license": "MIT License",
                "desc": "Pustaka visualisasi terminal, bilah kemajuan, dan log telemetri berformat kaya."
            },
            {
                "name": "5. PyYAML",
                "id": "-5-pyyaml",
                "license": "MIT License",
                "desc": "Mesin pembaca dan penulis berkas konfigurasi format YAML."
            },
            {
                "name": "6. Referensi Inspirasi Upstream",
                "id": "-6-referensi-inspirasi-upstream",
                "license": "Reference Only",
                "desc": "Eksplorasi konsep awal merujuk pada `camt4372/Discord-4Character-Usernames-Checker`, yang kemudian dirancang ulang dan dibangun kembali secara total dari nol dengan arsitektur asinkron, penyamaran TLS, isolasi multi-terowongan, SQLite WAL, dan distribusi lintas platform."
            }
        ]
    }
}
