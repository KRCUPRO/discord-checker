# deploy/scripts/locale_data/changelog.py
"""
1:1 Full Localization for CHANGELOG.md across all 12 locales.
"""

CHANGELOG_DATA = {
    "ko": {
        "title": "📋 변경 이력 (Changelog)",
        "desc": "D4UC (discord-checker) 프로젝트의 모든 버전별 변경 사항 및 기술 갱신 기록",
        "intro": "D4UC의 모든 공식 릴리스 및 주요 기능 추가, 아키텍처 개선, 버그 수정 내역을 기록합니다.",
        "versions": [
            {
                "ver": "v12.5.0",
                "date": "2026-11-19",
                "added": [
                    "**12개국어 1:1 전수 공식 문서 스위트 (`docs/locales/<lang>/`)**: 8종의 핵심 문서(`README.md`, `ARCHITECTURE_MAP.md`, `GUIDE.md`, `TASKS.md`, `CHANGELOG.md`, `LICENSE.md`, `NOTICE.md`, `SECURITY.md`)를 12개 언어(한국어, 영어, 일본어, 중국어 간체, 스페인어, 프랑스어, 독일어, 러시아어, 포르투갈어, 아랍어, 힌디어, 인도네시아어)로 1:1 전면 번역 및 구축.",
                    "**깃허브 저장소 루트 최적화 및 모듈화**: 내부 유지보수 스크립트를 `deploy/scripts/`로 이전하고 중복 스크립트를 제거하여, 저장소 방문 즉시 설명서와 UI 미리보기가 한눈에 보이도록 폴더 6개 + 파일 8개 구조로 대폭 슬림화.",
                    "**문서 상단 빠른 점프 바 (Quick Jump Navigation Bar)**: 스크롤 부담 없이 [개요 | 미리보기 | 빠른 시작 | 아키텍처 | 가이드 | 라이선스]로 즉시 점프 가능한 원터치 앵커 링크 추가."
                ],
                "changed": [
                    "모든 문서 상단에 5x2 규격의 대칭형 다국어 선택 테이블 및 SVG 실시간 업데이트 배지(`2026년 11월 19일`) 동기화."
                ]
            },
            {
                "ver": "v12.4.0",
                "date": "2026-11-19",
                "added": [
                    "**문서 양방향 내비게이션 (TOC 앵커 및 목차 복귀 링크)**: 26개 전체 마크다운 문서에 상호 점프 앵커 `<a id=\"...\">` 및 `[⬆️ 목차 맨 위로 이동]` 링크 전면 적용.",
                    "**13종 운영체제별 공식 가이드 구축 (`docs/guides/`)**: Windows, macOS, Linux, Android APK, iOS Safari PWA, Docker Compose, Raspberry Pi 등 플랫폼별 맞춤 설치 및 24/7 데몬 구동 매뉴얼 완비."
                ]
            },
            {
                "ver": "v12.3.0",
                "date": "2026-11-19",
                "added": [
                    "**무료 공개 프록시 자동 수집 및 실시간 검증 엔진 (`src/proxy/free_proxy.py`)**: 18개 글로벌 오픈소스 저장소 실시간 스크래핑, Cloudflare WAF 검증, 15초 429 쿨다운 큐.",
                    "**안드로이드 전용 1-Tap 서명 APK (`dist/DiscordUsernameChecker_v12.3.0.apk`)**: v1/v2/v3 암호화 서명, One UI / HyperOS 절전 제외 가이드."
                ]
            },
            {
                "ver": "v12.2.0",
                "date": "2026-11-19",
                "added": [
                    "**모바일 터치 최적화 Web GUI & PWA 엔진 (`src/web_gui.py`, `src/ui/web/`)**: 스마트폰 브라우저 5000 포트 반응형 UI, 0.1초 실시간 Discord Webhook 알림."
                ]
            },
            {
                "ver": "v12.0.0",
                "date": "2026-11-18",
                "added": [
                    "**크로스 플랫폼 정식 프로덕션 릴리스**: Windows 4종 단독 EXE, 8대 닉네임 생성 엔진, Chrome 131 TLS 스텔스 위장, 1:1 다중 터널 풀."
                ]
            }
        ]
    },
    "en": {
        "title": "📋 Changelog",
        "desc": "All notable changes to D4UC (discord-checker) documented across releases",
        "intro": "This log documents all official releases, major architectural improvements, and bug fixes for D4UC.",
        "versions": [
            {
                "ver": "v12.5.0",
                "date": "2026-11-19",
                "added": [
                    "**12-Language 1:1 Complete Documentation Suite (`docs/locales/<lang>/`)**: Full 1:1 translations for all 8 core documents (`README.md`, `ARCHITECTURE_MAP.md`, `GUIDE.md`, `TASKS.md`, `CHANGELOG.md`, `LICENSE.md`, `NOTICE.md`, `SECURITY.md`) across 12 languages (Korean, English, Japanese, Simplified Chinese, Spanish, French, German, Russian, Portuguese, Arabic, Hindi, Indonesian).",
                    "**GitHub Repository Root Streamlining & Modularization**: Moved internal scripts to `deploy/scripts/`, eliminated duplicate scripts, and reduced root clutter to 6 folders + 8 files so README and preview media appear above the fold.",
                    "**Above-the-Fold Quick Jump Navigation Bar**: One-click anchor bar below badge strip ([ Overview | Previews | Quick Start | Architecture | Guides | License ])."
                ],
                "changed": [
                    "Standardized 5x2 symmetrical language selector grid and synchronized live SVG date badge (`Nov 19, 2026`) across all files."
                ]
            },
            {
                "ver": "v12.4.0",
                "date": "2026-11-19",
                "added": [
                    "**Two-Way Document Navigation (TOC Anchor Links & Return-to-Top Navigation)**: Full interactive Table of Contents and return-to-top links across all 26 markdown documents.",
                    "**Dedicated OS & Platform Comprehensive Guides (`docs/guides/`)**: 13 platform manuals covering Windows, macOS, Linux, Android APK, iOS Safari PWA, Docker Compose, Raspberry Pi."
                ]
            },
            {
                "ver": "v12.3.0",
                "date": "2026-11-19",
                "added": [
                    "**Free Public Proxy Scraper & Live Multi-Threaded Validator (`src/proxy/free_proxy.py`)**: 18 public candidate sources, Cloudflare WAF validation, 15s 429 rate limit cooldown queue.",
                    "**Standalone Android 1-Tap Signed APK (`dist/DiscordUsernameChecker_v12.3.0.apk`)**: Cryptographically verified v1/v2/v3 signatures with background battery optimization guides."
                ]
            },
            {
                "ver": "v12.2.0",
                "date": "2026-11-19",
                "added": [
                    "**Mobile Touch Web GUI & PWA Engine (`src/web_gui.py`, `src/ui/web/`)**: Port 5000 responsive smartphone UI, Service Worker offline caching, 0.1s Discord Webhook push."
                ]
            },
            {
                "ver": "v12.0.0",
                "date": "2026-11-18",
                "added": [
                    "**Official Cross-Platform Production Release**: 4 standalone Windows EXEs, 8 candidate nickname engines, Chrome 131 TLS stealth, 1:1 multi-tunnel proxy pool."
                ]
            }
        ]
    },
    "ja": {
        "title": "📋 変更履歴 (Changelog)",
        "desc": "D4UC (discord-checker) のバージョン別更新履歴および技術改善記録",
        "intro": "本ファイルには、D4UCの各公式リリースにおける新機能追加、設計改善、バグ修正の全履歴を記録します。",
        "versions": [
            {
                "ver": "v12.5.0",
                "date": "2026-11-19",
                "added": [
                    "**12言語 1:1 完全対応公式ドキュメントスイート (`docs/locales/<lang>/`)**: 8大主要文書（README、ARCHITECTURE_MAP、GUIDE、TASKS、CHANGELOG、LICENSE、NOTICE、SECURITY）を12言語（日本語、韓国語、英語、簡体字中国語、スペイン語、フランス語、ドイツ語、ロシア語、ポルトガル語、アラビア語、ヒンディー語、インドネシア語）へ1:1完全翻訳・配備。",
                    "**GitHubリポジトリルートの整理とモジュール化**: 内部スクリプトを `deploy/scripts/` へ集約し、不要な重複ファイルを削除して、訪問時に概要とプレビューが即座に表示されるよう6フォルダ＋8ファイルの構造へ大幅スリム化。",
                    "**文書上部クイックジャンプバー**: スクロール不要で即座に目的の章へジャンプできるワンタッチリンクを追加。"
                ],
                "changed": [
                    "すべての文書上部に5×2規格の対称言語選択表およびリアルタイム更新SVGバッジ（`2026年11月19日`）を同期。"
                ]
            },
            {
                "ver": "v12.4.0",
                "date": "2026-11-19",
                "added": [
                    "**双方向ドキュメントナビゲーション**: 全26文書に相互ジャンプ目次と「目次の先頭へ戻る」リンクを完全適用。",
                    "**13種類のOS別公式ガイド (`docs/guides/`)**: Windows、macOS、Linux、Android APK、iOS PWA、Docker Compose等の環境別ガイド完備。"
                ]
            },
            {
                "ver": "v12.3.0",
                "date": "2026-11-19",
                "added": [
                    "**無料公開プロキシ自動収集・検証エンジン**: 18公開ソースからリアルタイム収集、Cloudflare検証、15秒クールダウンキュー機能。",
                    "**署名済みAndroid単独APK**: v1/v2/v3署名付きAPKパッケージおよびバックグラウンド省電力除外設定ガイド。"
                ]
            },
            {
                "ver": "v12.2.0",
                "date": "2026-11-19",
                "added": [
                    "**モバイルタッチ最適化Web GUI & PWA**: ポート5000対応レスポンシブUI、0.1秒Discord Webhook即時通知。"
                ]
            },
            {
                "ver": "v12.0.0",
                "date": "2026-11-18",
                "added": [
                    "**正式マルチプラットフォームリリース**: Windows単独EXE 4種、8大生成エンジン、Chrome 131 TLS ステルス偽装。"
                ]
            }
        ]
    },
    "zh-CN": {
        "title": "📋 更新日志 (Changelog)",
        "desc": "D4UC (discord-checker) 项目全版本重大更新、架构优化与修复记录",
        "intro": "本文件记录 D4UC 所有正式发布版本的核心功能新增、架构改进与故障修复细节。",
        "versions": [
            {
                "ver": "v12.5.0",
                "date": "2026-11-19",
                "added": [
                    "**12 国语言 1:1 完整官方文档套件 (`docs/locales/<lang>/`)**: 将 8 大核心文档（README、ARCHITECTURE_MAP、GUIDE、TASKS、CHANGELOG、LICENSE、NOTICE、SECURITY）全量翻译并部署至 12 种语言（中文简体、韩语、英语、日语、西班牙语、法语、德语、俄语、葡萄牙语、阿拉伯语、印地语、印尼语）。",
                    "**GitHub 仓库根目录优化与模块化**: 将内部运维脚本归档至 `deploy/scripts/`，移除冗余文件，使根目录精简为 6 文件夹 + 8 文件，确保访客第一眼即可浏览项目介绍与界面预览。",
                    "**首屏快速跳转导航栏**: 在徽章栏下方新增一键锚点栏 [ 概览 | 界面预览 | 快速启动 | 系统架构 | 平台指南 | 许可协议 ]。"
                ],
                "changed": [
                    "在所有文档顶部同步 5×2 规格的对称多语言选择器与实时 SVG 更新徽章（`2026年11月19日`）。"
                ]
            },
            {
                "ver": "v12.4.0",
                "date": "2026-11-19",
                "added": [
                    "**双向文档导航系统**: 全仓库 26 个 Markdown 文档均配备交互式目录与返回目录顶部链接。",
                    "**13 种操作系统专属指南 (`docs/guides/`)**: 覆盖 Windows、macOS、Linux、Android APK、iOS PWA、Docker Compose 等全环境。"
                ]
            },
            {
                "ver": "v12.3.0",
                "date": "2026-11-19",
                "added": [
                    "**免费公开代理自动抓取与验证引擎**: 18 个公开源实时抓取、Cloudflare WAF 验证、15 秒 429 冷却队列。",
                    "**已签名的独立 Android APK**: 经过 v1/v2/v3 完整数字签名的安装包及电池优化白名单配置教程。"
                ]
            },
            {
                "ver": "v12.2.0",
                "date": "2026-11-19",
                "added": [
                    "**移动端触控 Web GUI 与 PWA 引擎**: 5000 端口响应式触摸界面、0.1 秒 Discord Webhook 实时推送。"
                ]
            },
            {
                "ver": "v12.0.0",
                "date": "2026-11-18",
                "added": [
                    "**跨平台正式生产版本发布**: 4 种独立 Windows EXE、八大候选用户名生成引擎、Chrome 131 TLS 隐形网络栈。"
                ]
            }
        ]
    },
    "es": {
        "title": "📋 Registro de Cambios (Changelog)",
        "desc": "Todos los cambios notables y mejoras de D4UC (discord-checker)",
        "intro": "Este registro documenta todas las versiones oficiales, optimizaciones arquitectónicas y correcciones de D4UC.",
        "versions": [
            {
                "ver": "v12.5.0",
                "date": "2026-11-19",
                "added": [
                    "**Suite de Documentación Completa 1:1 en 12 Idiomas (`docs/locales/<lang>/`)**: Traducción íntegra de los 8 documentos clave en 12 idiomas.",
                    "**Optimización y Modularización de la Raíz de GitHub**: Reorganización interna en `deploy/scripts/` dejando una raíz limpia de 6 carpetas y 8 archivos.",
                    "**Barra de Salto Rápido Superior**: Enlaces de anclaje para navegar instantáneamente sin scroll innecesario."
                ],
                "changed": [
                    "Sincronización de tabla selectora simétrica 5x2 y distintivo SVG en vivo (`19 nov 2026`)."
                ]
            },
            {
                "ver": "v12.4.0",
                "date": "2026-11-19",
                "added": [
                    "**Navegación Bidireccional de Documentos**: Índices completos con enlaces de retorno en los 26 archivos markdown.",
                    "**Guías Dedicadas para 13 Sistemas Operativos (`docs/guides/`)**: Manuales detallados para Windows, macOS, Linux, Android, iOS y Docker."
                ]
            },
            {
                "ver": "v12.3.0",
                "date": "2026-11-19",
                "added": [
                    "**Scraper de Proxies Gratuitos y Validador en Vivo**: 18 fuentes públicas, validación Cloudflare y cola de enfriamiento para 429.",
                    "**APK Autónomo Firmado para Android**: Paquete con firmas v1/v2/v3 y guías de optimización de batería."
                ]
            },
            {
                "ver": "v12.2.0",
                "date": "2026-11-19",
                "added": [
                    "**Web GUI Móvil y PWA**: Interfaz táctil puerto 5000 y notificaciones Discord Webhook en 0.1s."
                ]
            },
            {
                "ver": "v12.0.0",
                "date": "2026-11-18",
                "added": [
                    "**Lanzamiento Multiplataforma**: 4 ejecutables autónomos, 8 motores de búsqueda y sigilo TLS Chrome 131."
                ]
            }
        ]
    },
    "fr": {
        "title": "📋 Journal des Modifications (Changelog)",
        "desc": "Historique des versions et évolutions architecturales de D4UC (discord-checker)",
        "intro": "Ce document répertorie l'ensemble des versions officielles, ajouts majeurs et correctifs de D4UC.",
        "versions": [
            {
                "ver": "v12.5.0",
                "date": "2026-11-19",
                "added": [
                    "**Suite Documentaire 1:1 en 12 Langues (`docs/locales/<lang>/`)**: Traduction exhaustive des 8 documents majeurs dans les 12 langues prises en charge.",
                    "**Allègement et Modularisation de la Racine GitHub**: Déplacement des scripts dans `deploy/scripts/` pour une racine épurée (6 dossiers, 8 fichiers).",
                    "**Barre de Navigation Rapide au Sommet**: Accès immédiat aux sections clés sans défilement."
                ],
                "changed": [
                    "Grille multilingue 5x2 symétrique et badge de mise à jour SVG en temps réel (`19 nov 2026`)."
                ]
            },
            {
                "ver": "v12.4.0",
                "date": "2026-11-19",
                "added": [
                    "**Navigation Bidirectionnelle**: Sommaires interactifs et liens de retour sur l'ensemble des 26 documents.",
                    "**13 Manuels d'Installation par Système d'Exploitation**: Guides complets pour Windows, macOS, Linux, Android, iOS, Docker."
                ]
            },
            {
                "ver": "v12.3.0",
                "date": "2026-11-19",
                "added": [
                    "**Moissonneur de Proxys Gratuits & Validateur en Direct**: 18 sources ouvertes avec filtrage Cloudflare.",
                    "**Paquet APK Android Signé**: Binaire autonome certifié v1/v2/v3 avec gestion du maintien d'activité (Wake Lock)."
                ]
            },
            {
                "ver": "v12.2.0",
                "date": "2026-11-19",
                "added": [
                    "**Interface Web Mobile & PWA**: Port 5000, design tactile et alertes Webhook instantanées."
                ]
            },
            {
                "ver": "v12.0.0",
                "date": "2026-11-18",
                "added": [
                    "**Version Multiplateforme Officielle**: 4 EXE Windows, 8 générateurs et TLS furtif Chrome 131."
                ]
            }
        ]
    },
    "de": {
        "title": "📋 Änderungsprotokoll (Changelog)",
        "desc": "Dokumentation aller Versionsänderungen und technischen Updates für D4UC",
        "intro": "Dieses Protokoll verzeichnet alle offiziellen Veröffentlichungen, Architekturverbesserungen und Fehlerbehebungen.",
        "versions": [
            {
                "ver": "v12.5.0",
                "date": "2026-11-19",
                "added": [
                    "**Vollständige 1:1-Dokumentations-Suite in 12 Sprachen (`docs/locales/<lang>/`)**: Übersetzung aller 8 Kern-Dokumente in 12 Sprachen.",
                    "**Vollständige Bereinigung des GitHub-Root-Verzeichnisses**: Verschiebung interner Skripte nach `deploy/scripts/`, Reduzierung auf 6 Ordner + 8 Dateien.",
                    "**Schnellzugriffsleiste am Dokumentanfang**: Direkte Sprungmarken für eine optimale Benutzererfahrung."
                ],
                "changed": [
                    "Einheitliche 5x2-Sprachauswahltabelle und synchronisiertes SVG-Update-Badge (`19. Nov 2026`)."
                ]
            },
            {
                "ver": "v12.4.0",
                "date": "2026-11-19",
                "added": [
                    "**Bidirektionale Dokumentennavigation**: Interaktive Inhaltsverzeichnisse und Rücksprunglinks in allen 26 Dateien.",
                    "**13 OS-spezifische Installationsanleitungen**: Umfassende Handbücher für Windows, macOS, Linux, Android, iOS und Docker."
                ]
            },
            {
                "ver": "v12.3.0",
                "date": "2026-11-19",
                "added": [
                    "**Automatischer Public-Proxy-Scraper**: Live-Validierung von 18 Quellen und 15s-Cooldown-Warteschlange.",
                    "**Signiertes Android-APK-Paket**: Kryptografisch validierte v1/v2/v3-Signaturen mit Energiesparanleitungen."
                ]
            },
            {
                "ver": "v12.2.0",
                "date": "2026-11-19",
                "added": [
                    "**Mobiles Web GUI & PWA**: Port 5000 Touch-Interface und 0,1s Discord-Webhook-Benachrichtigungen."
                ]
            },
            {
                "ver": "v12.0.0",
                "date": "2026-11-18",
                "added": [
                    "**Offizieller Multiplattform-Release**: 4 eigenständige EXEs, 8 Such-Engines und Chrome 131 TLS-Tarnung."
                ]
            }
        ]
    },
    "ru": {
        "title": "📋 История изменений (Changelog)",
        "desc": "Все ключевые изменения и технические обновления проекта D4UC",
        "intro": "В данном журнале фиксируются все официальные релизы, улучшения архитектуры и исправления ошибок.",
        "versions": [
            {
                "ver": "v12.5.0",
                "date": "2026-11-19",
                "added": [
                    "**Комплект документации 1:1 на 12 языках (`docs/locales/<lang>/`)**: Полный перевод всех 8 основных документов на 12 языков.",
                    "**Оптимизация корня репозитория GitHub**: Перенос служебных скриптов в `deploy/scripts/`, компактный вид (6 папок + 8 файлов).",
                    "**Панель быстрого перехода в шапке**: Кнопки моментального перехода к ключевым разделам без прокрутки."
                ],
                "changed": [
                    "Симметричная сетка переключения языков 5х2 и динамический SVG-бейдж даты (`19 ноя 2026`)."
                ]
            },
            {
                "ver": "v12.4.0",
                "date": "2026-11-19",
                "added": [
                    "**Двусторонняя навигация по документам**: Рабочее оглавление и кнопки возврата наверх во всех 26 документах.",
                    "**13 специализированных руководств по ОС**: Полные инструкции для Windows, macOS, Linux, Android, iOS и Docker."
                ]
            },
            {
                "ver": "v12.3.0",
                "date": "2026-11-19",
                "added": [
                    "**Сборщик бесплатных публичных прокси**: Парсинг 18 источников, проверка Cloudflare и очередь 429.",
                    "**Подписанный APK для Android**: Пакет с v1/v2/v3 подписями и инструкциями по фоновой работе."
                ]
            },
            {
                "ver": "v12.2.0",
                "date": "2026-11-19",
                "added": [
                    "**Мобильный Web GUI и PWA**: Сенсорный интерфейс на порту 5000 и мгновенные уведомления в Discord."
                ]
            },
            {
                "ver": "v12.0.0",
                "date": "2026-11-18",
                "added": [
                    "**Официальный кроссплатформенный релиз**: 4 автономных EXE, 8 генераторов и стелс-TLS Chrome 131."
                ]
            }
        ]
    },
    "pt-BR": {
        "title": "📋 Histórico de Alterações (Changelog)",
        "desc": "Todas as alterações notáveis e atualizações técnicas do projeto D4UC",
        "intro": "Este registro documenta todas as versões oficiais, melhorias estruturais e correções do D4UC.",
        "versions": [
            {
                "ver": "v12.5.0",
                "date": "2026-11-19",
                "added": [
                    "**Suíte de Documentação 1:1 em 12 Idiomas (`docs/locales/<lang>/`)**: Tradução completa dos 8 documentos principais em 12 idiomas.",
                    "**Modularização da Raiz do Repositório**: Transferência de scripts para `deploy/scripts/` e raiz simplificada (6 pastas + 8 arquivos).",
                    "**Barra de Salto Rápido Superior**: Links diretos para navegação ágil sem rolagem desnecessária."
                ],
                "changed": [
                    "Tabela de idiomas 5x2 simétrica e badge de atualização SVG sincronizado (`19 nov 2026`)."
                ]
            },
            {
                "ver": "v12.4.0",
                "date": "2026-11-19",
                "added": [
                    "**Navegação Bidirecional**: Sumários interativos com links de retorno ao topo em todos os 26 arquivos.",
                    "**13 Guias Completos por Sistema Operacional**: Manuais para Windows, macOS, Linux, Android, iOS e Docker."
                ]
            },
            {
                "ver": "v12.3.0",
                "date": "2026-11-19",
                "added": [
                    "**Scraper de Proxies Públicos e Validação ao Vivo**: 18 fontes com checagem Cloudflare e fila de resfriamento.",
                    "**APK Android Autônomo Assinado**: Assinaturas v1/v2/v3 e manuais de isenção de economia de bateria."
                ]
            },
            {
                "ver": "v12.2.0",
                "date": "2026-11-19",
                "added": [
                    "**Web GUI Touch & PWA Móvel**: Interface na porta 5000 e notificações Discord Webhook em 0,1s."
                ]
            },
            {
                "ver": "v12.0.0",
                "date": "2026-11-18",
                "added": [
                    "**Lançamento Oficial Multiplataforma**: 4 EXEs independentes, 8 motores e disfarce TLS Chrome 131."
                ]
            }
        ]
    },
    "ar": {
        "title": "📋 سجل التغييرات (Changelog)",
        "desc": "توثيق شامل لكافة التحديثات والتحسينات التقنية لمشروع D4UC",
        "intro": "يوثق هذا السجل جميع الإصدارات الرسمية والميزات الجديدة والتحسينات الهندسية والإصلاحات البرمجية.",
        "versions": [
            {
                "ver": "v12.5.0",
                "date": "2026-11-19",
                "added": [
                    "**حزمة التوثيق الكاملة بنسبة 1:1 بـ 12 لغة (`docs/locales/<lang>/`)**: ترجمة كاملة وشاملة لـ 8 وثائق أساسية إلى 12 لغة عالمية.",
                    "**تنظيم وتنسيق المجلد الرئيسي للمستودع**: نقل أدوات الصيانة إلى `deploy/scripts/` لتصبح الواجهة مقتصرة على 6 مجلدات و8 ملفات رئيسية.",
                    "**شريط الانتقال السريع في أعلى المستند**: روابط فورية تتيح الوصول للأقسام الرئيسية دون الحاجة للتمرير الطويل."
                ],
                "changed": [
                    "توحيد جدول اختيار اللغات المتماثل 5x2 وتحديث شارة التاريخ التفاعلية SVG (`19 نوفمبر 2026`)."
                ]
            },
            {
                "ver": "v12.4.0",
                "date": "2026-11-19",
                "added": [
                    "**التنقل ثنائي الاتجاه**: فهارس تفاعلية وروابط للعودة لأعلى الصفحة عبر جميع مستندات المشروع الـ 26.",
                    "**13 دليلاً شاملاً لكافة أنظمة التشغيل**: تغطية كاملة لـ Windows وmacOS وLinux وأندرويد وiOS وDocker."
                ]
            },
            {
                "ver": "v12.3.0",
                "date": "2026-11-19",
                "added": [
                    "**محرك جمع البروكسيات المجانية والتحقق الفوري**: سحب من 18 مصدراً مفتوحاً مع الفحص عبر Cloudflare.",
                    "**تطبيق APK مستقل وموقع بنقرة واحدة**: شهادات رقمية v1/v2/v3 ودليل لإلغاء قيود توفير الطاقة."
                ]
            },
            {
                "ver": "v12.2.0",
                "date": "2026-11-19",
                "added": [
                    "**واجهة الويب المخصصة للمس وتطبيق PWA**: تشغيل على المنفذ 5000 وتنبيهات فورية خلال 0.1 ثانية."
                ]
            },
            {
                "ver": "v12.0.0",
                "date": "2026-11-18",
                "added": [
                    "**الإصدار الإنتاجي متعدد المنصات**: 4 ملفات EXE مستقلة، 8 محركات بحث، ومحاكاة TLS Chrome 131."
                ]
            }
        ]
    },
    "hi": {
        "title": "📋 परिवर्तन लॉग (Changelog)",
        "desc": "D4UC (discord-checker) के सभी संस्करण परिवर्तनों और तकनीकी अपडेट का दस्तावेज़ीकरण",
        "intro": "यह लॉग D4UC के सभी आधिकारिक रिलीज़, प्रमुख वास्तुशिल्प सुधारों और बग फिक्स का दस्तावेजीकरण करता है।",
        "versions": [
            {
                "ver": "v12.5.0",
                "date": "2026-11-19",
                "added": [
                    "**12 भाषाओं में 1:1 पूर्ण दस्तावेज़ीकरण सुइट (`docs/locales/<lang>/`)**: 12 भाषाओं में सभी 8 मुख्य दस्तावेज़ों का पूर्ण 1:1 अनुवाद।",
                    "**GitHub रिपॉजिटरी रूट का सरलीकरण और मॉड्यूलर पुनर्गठन**: स्क्रिप्ट्स को `deploy/scripts/` में स्थानांतरित किया गया (6 फ़ोल्डर + 8 फ़ाइलें)।",
                    "**शीर्ष पर त्वरित नेविगेशन बार**: बिना स्क्रॉल किए मुख्य अनुभागों पर तुरंत जाने के लिए त्वरित लिंक।"
                ],
                "changed": [
                    "सममित 5x2 भाषा चयन तालिका और लाइव SVG दिनांक बैज (`19 नवंबर 2026`) का तुल्यकालन।"
                ]
            },
            {
                "ver": "v12.4.0",
                "date": "2026-11-19",
                "added": [
                    "**द्विदिश दस्तावेज़ नेविगेशन**: सभी 26 मार्कडाउन दस्तावेज़ों में इंटरैक्टिव सामग्री तालिका और शीर्ष पर लौटने के लिंक।",
                    "**13 समर्पित ऑपरेटिंग सिस्टम गाइड**: Windows, macOS, Linux, Android, iOS और Docker के लिए विस्तृत मैनुअल।"
                ]
            },
            {
                "ver": "v12.3.0",
                "date": "2026-11-19",
                "added": [
                    "**निःशुल्क सार्वजनिक प्रॉक्सी स्क्रैपर और सत्यापन इंजन**: 18 स्रोतों से लाइव डेटा और Cloudflare सत्यापन।",
                    "**हस्ताक्षरित स्टैंडअलोन Android APK पैकेज**: v1/v2/v3 डिजिटल हस्ताक्षर और पृष्ठभूमि बैटरी अनुकूलन गाइड।"
                ]
            },
            {
                "ver": "v12.2.0",
                "date": "2026-11-19",
                "added": [
                    "**मोबाइल टच Web GUI और PWA**: पोर्ट 5000 पर उत्तरदायी वेब और 0.1s में Discord Webhook सूचनाएं।"
                ]
            },
            {
                "ver": "v12.0.0",
                "date": "2026-11-18",
                "added": [
                    "**आधिकारिक क्रॉस-प्लेटफ़ॉर्म प्रोडक्शन रिलीज़**: 4 स्टैंडअलोन EXEs, 8 जनरेशन इंजन और Chrome 131 TLS स्टेल्थ।"
                ]
            }
        ]
    },
    "id": {
        "title": "📋 Log Perubahan (Changelog)",
        "desc": "Dokumentasi seluruh perubahan versi dan pembaruan teknis proyek D4UC",
        "intro": "Log ini mendokumentasikan seluruh rilis resmi, peningkatan arsitektur, dan perbaikan bug D4UC.",
        "versions": [
            {
                "ver": "v12.5.0",
                "date": "2026-11-19",
                "added": [
                    "**Paket Dokumentasi Lengkap 1:1 dalam 12 Bahasa (`docs/locales/<lang>/`)**: Terjemahan utuh dari 8 dokumen utama ke dalam 12 bahasa.",
                    "**Perapian & Modularisasi Direktori Root GitHub**: Pemindahan skrip internal ke `deploy/scripts/` (6 folder + 8 berkas bersih).",
                    "**Bilah Navigasi Cepat di Bagian Atas**: Tautan satu sentuhan untuk melompat ke bab utama tanpa perlu menggulir jauh."
                ],
                "changed": [
                    "Tabel pemilih bahasa simetris 5x2 dan lencana pembaruan SVG dinamis (`19 Nov 2026`)."
                ]
            },
            {
                "ver": "v12.4.0",
                "date": "2026-11-19",
                "added": [
                    "**Navigasi Dokumen Dua Arah**: Daftar isi interaktif dengan tautan kembali ke atas di seluruh 26 dokumen.",
                    "**13 Panduan Khusus Sistem Operasi**: Manual terperinci untuk Windows, macOS, Linux, Android, iOS, dan Docker."
                ]
            },
            {
                "ver": "v12.3.0",
                "date": "2026-11-19",
                "added": [
                    "**Pengumpul Proxy Publik Gratis & Validator Waktu Nyata**: 18 sumber publik tervalidasi Cloudflare.",
                    "**Paket APK Android Mandiri Bertanda Tangan**: Tanda tangan kriptografis v1/v2/v3 dengan panduan pengecualian hemat baterai."
                ]
            },
            {
                "ver": "v12.2.0",
                "date": "2026-11-19",
                "added": [
                    "**Web GUI Sentuh & PWA Seluler**: Port 5000 UI responsif dan notifikasi Discord Webhook dalam 0,1 detik."
                ]
            },
            {
                "ver": "v12.0.0",
                "date": "2026-11-18",
                "added": [
                    "**Rilis Resmi Lintas Platform**: 4 berkas EXE mandiri, 8 mesin pembuat nama, dan penyamaran TLS Chrome 131."
                ]
            }
        ]
    }
}
