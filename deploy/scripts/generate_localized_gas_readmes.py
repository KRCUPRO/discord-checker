# generate_localized_gas_readmes.py
import os
from pathlib import Path

root = Path(__file__).resolve().parent.parent.parent

LANG_TABLE = """| [KR 한국어](../ko/gas/README.md) | [US English](../en/gas/README.md) | [JP 日本語](../ja/gas/README.md) | [CN 简体中文](../zh-CN/gas/README.md) | [ES Español](../es/gas/README.md) |
| :---: | :---: | :---: | :---: | :---: |
| [FR Français](../fr/gas/README.md) | [DE Deutsch](../de/gas/README.md) | [RU Русский](../ru/gas/README.md) | [BR Português](../pt-BR/gas/README.md) | [SA العربية](../ar/gas/README.md) |

<p align="center"><sub>🌐 Also available: <a href="../hi/gas/README.md">HI हिन्दी</a> • <a href="../id/gas/README.md">ID Bahasa Indonesia</a></sub></p>

---
"""

DATA = {
    "en": {
        "title": "⚡ D4UC Google Apps Script (GAS) 24/7 Serverless Checker",
        "desc": "> **Zero-Install, 100% Autonomous 24/7/365 Cloud Checker.**\n> Runs permanently on Google Cloud infrastructure via Time-driven Triggers without keeping your PC, smartphone, or Colab open.",
        "quick_start": "🚀 1-Minute Quick Start Guide",
        "step1_title": "Step 1: Create a Google Apps Script Project",
        "step1_body": "1. Open [Google Apps Script Dashboard](https://script.google.com/) in your browser.\n2. Click **[+ New project]** on the top-left.\n3. Name the project `D4UC 24/7 Checker`.",
        "step2_title": "Step 2: Copy Code & Configure",
        "step2_body": "1. Delete default code in `Code.gs` and paste the full contents of [`gas/D4UC_Checker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_Checker.js).\n2. Update the `CONFIG` block as needed:\n```javascript\nconst CONFIG = {\n  EXECUTION_MODE: 'STANDALONE', // 'STANDALONE' or 'HYBRID_WATCHDOG' (Colab sync)\n  TRIGGER_MODE: 'BALANCED',      // 'BALANCED' (5-min intervals) or 'TURBO' (1-min rapid)\n  SHARDING_MODE: 'SINGLE',       // 'SINGLE', 'INTERLEAVED', or 'FEDERATED'\n  USERNAME_LENGTH: 4,            // Target length (3-6 chars)\n  ENABLE_SPREADSHEET: true,       // Real-time Google Sheets tracking\n  DISCORD_WEBHOOK_URL: 'https://discord.com/api/webhooks/...' // Webhook URL for hits\n};\n```\n3. Save by clicking the Save icon (or Ctrl+S).",
        "step3_title": "Step 3: Initialize 24/7 Autonomous Runner",
        "step3_body": "1. Select **`initD4UCChecker`** in the function dropdown list.\n2. Click **[Run]**.\n3. When prompted, grant Google permissions (Review Permissions ➔ Select Account ➔ Advanced ➔ Go to D4UC 24/7 Checker (unsafe) ➔ Allow).\n4. When `🚀 [D4UC] 24/7 Autonomous Checker initialized` appears in Execution log, it runs around the clock even when your device is turned off.",
        "results_title": "📊 Result Verification",
        "results_body": "- **Google Drive**: Stored in `MyDrive/D4UC_Checker/available_usernames.txt` and `checker_state_w0.json`.\n- **Google Sheets**: Auto-created `D4UC_Tracker` spreadsheet logs valid hits in real-time.\n- **Discord Webhook**: Sends instant green embed alerts with `@here` mention when rare usernames are discovered.",
        "multi_title": "🌐 Multi-Account & Sharding Acceleration (100k~240k Checks/Day)",
        "multi_body": "To exceed Google's 20,000 requests/day per-account limit, scale horizontally across multiple accounts or projects:\n\n### Mode A: Single-Account Interleaved Projects\n1. In the same account, create additional Apps Script projects.\n2. Set `SHARDING_MODE: 'INTERLEAVED'` to alternate execution cycles across 24 hours.\n\n### Mode B: Multi-Account Zero-Collision Federation\n1. Log into your 2nd, 3rd, or Nth Google account.\n2. Copy & paste [`gas/D4UC_MultiAccount_Worker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_MultiAccount_Worker.js).\n3. Assign unique `WORKER_ID` (e.g. `0`, `1`, `2`, `3`) with `TOTAL_WORKERS: 4`.\n4. Enter the **same Discord Webhook URL** in all workers to aggregate discoveries into a single channel!\n5. (Optional) Run [`gas/D4UC_Master_Dashboard.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_Master_Dashboard.js) to view real-time fleet telemetry.",
        "stop_title": "🛑 Stopping the Checker",
        "stop_body": "Select **`stopD4UCChecker`** in the function dropdown and click **[Run]**. All scheduled triggers are safely removed immediately."
    },
    "ko": {
        "title": "⚡ D4UC Google Apps Script (GAS) 24/7 서버리스 체커",
        "desc": "> **PC, 스마트폰, Colab을 켜둘 필요 없이** Google 클라우드 인프라에서 시간 기반 예약 기능(Time-driven Triggers)으로 24시간 365일 무인 구동되는 닉네임 체커입니다.",
        "quick_start": "🚀 1분 초고속 시작 가이드",
        "step1_title": "1단계: Google Apps Script 프로젝트 생성",
        "step1_body": "1. 브라우저에서 [Google Apps Script 대시보드](https://script.google.com/)에 접속합니다.\n2. 좌측 상단의 **[+ 새 프로젝트]**를 클릭합니다.\n3. 프로젝트 제목을 `D4UC 24/7 Checker`로 변경합니다.",
        "step2_title": "2단계: 코드 복사 및 설정 입력",
        "step2_body": "1. 기본 `Code.gs` 내용을 모두 지우고, [`gas/D4UC_Checker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_Checker.js) 전체 내용을 복사하여 붙여넣습니다.\n2. 상단의 `CONFIG` 블록에서 원하는 옵션을 설정합니다:\n```javascript\nconst CONFIG = {\n  EXECUTION_MODE: 'STANDALONE', // 'STANDALONE' (단독) 또는 'HYBRID_WATCHDOG' (Colab 연동)\n  TRIGGER_MODE: 'BALANCED',      // 'BALANCED' (5분 예정) 또는 'TURBO' (1분 초고속)\n  SHARDING_MODE: 'SINGLE',       // 'SINGLE', 'INTERLEAVED', 'FEDERATED'\n  USERNAME_LENGTH: 4,            // 탐색할 글자수 (3~6)\n  ENABLE_SPREADSHEET: true,       // Google Sheets 실시간 대시보드 사용\n  DISCORD_WEBHOOK_URL: 'https://discord.com/api/webhooks/...' // 알림받을 웹훅 URL\n};\n```\n3. 상단 도구 모음의 **[저장 (💾)]** 버튼(또는 Ctrl+S)을 누릅니다.",
        "step3_title": "3단계: 원클릭 초기화 및 24시간 자동 가동",
        "step3_body": "1. 상단 함수 선택 드롭다운에서 **`initD4UCChecker`**를 선택합니다.\n2. **[실행 (▶)]** 버튼을 클릭합니다.\n3. 최초 실행 시 Google 권한 승인 창이 뜨면 **[권한 검토]** ➔ 계정 선택 ➔ **[고급]** ➔ **[이동 (안전하지 않음)]** ➔ **[허용]**을 순서대로 클릭합니다.\n4. 실행 로그에 `🚀 [D4UC] 24시간 자동 체커 초기화 및 트리거 등록 완료`가 출력되면 이제 컴퓨터나 스마트폰을 끄셔도 24시간 자동으로 계속 작동합니다.",
        "results_title": "📊 결과 확인 방법",
        "results_body": "1. **Google Drive**: `MyDrive/D4UC_Checker/` 폴더가 자동 생성되며, `available_usernames.txt`에 유효 닉네임이 실시간 저장됩니다.\n2. **Google Sheets**: `D4UC_Tracker` 시트에 모든 행이 자동 기록되어 모바일에서도 실시간 조회 가능합니다.\n3. **Discord Webhook**: 유효 닉네임 발견 시 초록색 임베드와 `@here` 알림이 즉시 스마트폰으로 전송됩니다.",
        "multi_title": "🌐 다중 계정 및 다중 프로젝트 가속 가이드 (일일 10만~24만 회 초고속)",
        "multi_body": "구글 계정의 일일 호출 한도(20,000회)를 넘어 **일일 10만~24만 회 이상 초고속 전수 탐색**을 원할 경우 다중 계정 분산 샤딩을 활용할 수 있습니다:\n\n### 방식 A: 단일 계정 내 다중 프로젝트 시차 가동 (Interleaved)\n1. 동일한 구글 계정에서 `D4UC Checker - Node B`를 추가 생성합니다.\n2. `CONFIG.SHARDING_MODE = 'INTERLEAVED'`로 설정 후 `initD4UCChecker`를 실행합니다.\n\n### 방식 B: 다중 구글 계정 연합 무충돌 샤딩 (Federated Multi-Account)\n1. 2번째, 3번째 구글 계정의 [Google Apps Script](https://script.google.com/)에 접속합니다.\n2. [`gas/D4UC_MultiAccount_Worker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_MultiAccount_Worker.js) 코드를 복사하여 붙여넣습니다.\n3. 각 계정별로 `WORKER_ID`를 지정합니다 (예: 4개 계정: 계정1=`0`, 계정2=`1`, 계정3=`2`, 계정4=`3`, `TOTAL_WORKERS: 4`).\n4. 모든 계정에 **동일한 Discord Webhook URL**을 입력하면 가용 닉네임이 단일 디스코드 채널로 실시간 자동 취합됩니다!\n5. (선택사항) 중앙 종합 모니터링이 필요할 경우 [`gas/D4UC_Master_Dashboard.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_Master_Dashboard.js)를 가동합니다.",
        "stop_title": "🛑 체커 중지 방법",
        "stop_body": "중단하고 싶을 때는 함수 드롭다운에서 **`stopD4UCChecker`**를 선택하고 **[실행]**을 누르면 모든 예약 트리거가 즉시 안전하게 삭제됩니다."
    },
    "ja": {
        "title": "⚡ D4UC Google Apps Script (GAS) 24/7 サーバーレスチェッカー",
        "desc": "> **PCやスマホを開いておく必要なし！** Google Cloudインフラ上で時間駆動トリガー（Time-driven Triggers）により24時間365日完全無人稼働するDiscordユーザー名チェッカーです。",
        "quick_start": "🚀 1分クイックスタートガイド",
        "step1_title": "ステップ 1: Google Apps Script プロジェクト作成",
        "step1_body": "1. ブラウザで [Google Apps Script ダッシュボード](https://script.google.com/) にアクセスします。\n2. 左上の **[+ 新しいプロジェクト]** をクリックします。\n3. プロジェクト名を `D4UC 24/7 Checker` に変更します。",
        "step2_title": "ステップ 2: コードの貼り付けと設定",
        "step2_body": "1. `Code.gs` の内容を全消去し、[`gas/D4UC_Checker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_Checker.js) の全内容を貼り付けます。\n2. `CONFIG` ブロックを設定します:\n```javascript\nconst CONFIG = {\n  EXECUTION_MODE: 'STANDALONE',\n  TRIGGER_MODE: 'BALANCED',\n  SHARDING_MODE: 'SINGLE',\n  USERNAME_LENGTH: 4,\n  ENABLE_SPREADSHEET: true,\n  DISCORD_WEBHOOK_URL: 'https://discord.com/api/webhooks/...'\n};\n```\n3. 保存アイコン（または Ctrl+S）をクリックします。",
        "step3_title": "ステップ 3: 24時間無人ランナーの初期化",
        "step3_body": "1. 関数ドロップダウンから **`initD4UCChecker`** を選択します。\n2. **[実行]** をクリックします。\n3. Google権限承認プロンプトを許可します。\n4. 実行ログに完了メッセージが表示されたら、端末の電源を切っても24時間自動で稼働し続けます。",
        "results_title": "📊 結果の確認方法",
        "results_body": "- **Google Drive**: `MyDrive/D4UC_Checker/` に結果と状態が自動保存されます。\n- **Google Sheets**: `D4UC_Tracker` スプレッドシートにリアルタイム記録されます。\n- **Discord Webhook**: 有効なユーザー名発見時に即座に通知が届きます。",
        "multi_title": "🌐 マルチアカウント分散シャーディング（1日10万〜24万回高速化）",
        "multi_body": "Googleアカウントの1日20,000回制限を超えて高速探索を行う場合、複数アカウントによる分散シャーディングをご利用いただけます:\n\n1. 2つ目以降のGoogleアカウントで [`gas/D4UC_MultiAccount_Worker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_MultiAccount_Worker.js) を開きます。\n2. `WORKER_ID`（例: `0`, `1`, `2`, `3`）と `TOTAL_WORKERS: 4` を設定します。\n3. 同一の Discord Webhook URL を登録することで、1つのチャンネルに全アカウントの結果が集約されます。",
        "stop_title": "🛑 チェッカーの停止方法",
        "stop_body": "関数ドロップダウンで **`stopD4UCChecker`** を選択し、**[実行]** をクリックすると、すべてのトリガーが安全に削除されます。"
    },
    "zh-CN": {
        "title": "⚡ D4UC Google Apps Script (GAS) 24/7 无服务器检测器",
        "desc": "> **无需保持电脑、手机或 Colab 开启！** 基于 Google Cloud 云端时间驱动触发器（Time-driven Triggers），实现 24 小时 365 天完全无人值守自动运行。",
        "quick_start": "🚀 1 分钟快速上手指南",
        "step1_title": "步骤 1: 创建 Google Apps Script 项目",
        "step1_body": "1. 在浏览器中打开 [Google Apps Script 控制台](https://script.google.com/)。\n2. 点击左上角的 **[+ 新建项目]**。\n3. 将项目名称更改为 `D4UC 24/7 Checker`。",
        "step2_title": "步骤 2: 复制代码并配置",
        "step2_body": "1. 清空 `Code.gs` 并粘贴 [`gas/D4UC_Checker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_Checker.js) 的全部内容。\n2. 修改 `CONFIG` 配置项并保存。",
        "step3_title": "步骤 3: 一键初始化与 24 小时运行",
        "step3_body": "1. 在函数下拉菜单中选择 **`initD4UCChecker`**。\n2. 点击 **[运行]** 并授权 Google 权限。\n3. 执行日志显示初始化成功后，程序会在云端持续运行。",
        "results_title": "📊 结果查看",
        "results_body": "- **Google Drive**: 结果自动保存在 `MyDrive/D4UC_Checker/` 目录中。\n- **Google Sheets**: 自动生成 `D4UC_Tracker` 电子表格实时记录可用用户名。\n- **Discord Webhook**: 发现稀有用户名时立即推送带有 `@here` 的通知消息。",
        "multi_title": "🌐 多账号与分布式分片加速（单日 10 万 ~ 24 万次）",
        "multi_body": "突破单账号每日 20,000 次限制，支持多账号无冲突分片:\n\n1. 在其他 Google 账号中粘贴 [`gas/D4UC_MultiAccount_Worker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_MultiAccount_Worker.js)。\n2. 设置 `WORKER_ID`（如 `0`, `1`, `2`, `3`）及 `TOTAL_WORKERS: 4`。\n3. 配置相同的 Discord Webhook 即可实现单频道自动汇聚结果！",
        "stop_title": "🛑 停止检测器",
        "stop_body": "在函数列表中选择 **`stopD4UCChecker`** 并点击 **[运行]**，即可立即安全删除所有定时触发器。"
    },
    "es": {
        "title": "⚡ D4UC Google Apps Script (GAS) Verificador 24/7 sin Servidor",
        "desc": "> **¡Sin necesidad de mantener tu PC, teléfono o Colab encendido!** Se ejecuta en Google Cloud las 24 horas, los 365 días del año mediante activadores programados.",
        "quick_start": "🚀 Guía de Inicio Rápido de 1 Minuto",
        "step1_title": "Paso 1: Crear proyecto de Google Apps Script",
        "step1_body": "1. Abre [Google Apps Script](https://script.google.com/).\n2. Haz clic en **[+ Nuevo proyecto]** y nombra `D4UC 24/7 Checker`.",
        "step2_title": "Paso 2: Copiar código y configurar",
        "step2_body": "1. Pega [`gas/D4UC_Checker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_Checker.js) en `Code.gs`.\n2. Configura `CONFIG` y guarda.",
        "step3_title": "Paso 3: Inicializar ejecución 24/7",
        "step3_body": "1. Selecciona **`initD4UCChecker`** y haz clic en **[Ejecutar]**.\n2. Otorga los permisos requeridos.",
        "results_title": "📊 Comprobación de Resultados",
        "results_body": "Guardado en Google Drive, Google Sheets y alertas en Discord Webhook.",
        "multi_title": "🌐 Aceleración con Múltiples Cuentas (100k~240k Diarias)",
        "multi_body": "Usa [`gas/D4UC_MultiAccount_Worker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_MultiAccount_Worker.js) en cuentas secundarias con `WORKER_ID` (0..N-1) y el mismo Discord Webhook.",
        "stop_title": "🛑 Detener el Verificador",
        "stop_body": "Ejecuta **`stopD4UCChecker`** para eliminar todos los activadores."
    },
    "fr": {
        "title": "⚡ D4UC Google Apps Script (GAS) Vérificateur Serverless 24/7",
        "desc": "> **Fonctionne 24h/24 et 365j/an sur Google Cloud sans laisser votre PC ou smartphone allumé !**",
        "quick_start": "🚀 Guide de Démarrage Rapide en 1 Minute",
        "step1_title": "Étape 1 : Créer un projet Google Apps Script",
        "step1_body": "1. Ouvrez [Google Apps Script](https://script.google.com/) et créez un projet `D4UC 24/7 Checker`.",
        "step2_title": "Étape 2 : Copier le code et configurer",
        "step2_body": "1. Collez [`gas/D4UC_Checker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_Checker.js) dans `Code.gs`.\n2. Configurez `CONFIG` et enregistrez.",
        "step3_title": "Étape 3 : Initialiser le fonctionnement 24/7",
        "step3_body": "1. Sélectionnez **`initD4UCChecker`** et cliquez sur **[Exécuter]**.\n2. Autorisez les permissions.",
        "results_title": "📊 Résultats et Notifications",
        "results_body": "Google Drive, Google Sheets et alertes webhook Discord.",
        "multi_title": "🌐 Fédération Multi-Comptes (100k~240k Requêtes/Jour)",
        "multi_body": "Déployez [`gas/D4UC_MultiAccount_Worker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_MultiAccount_Worker.js) sur vos autres comptes Google.",
        "stop_title": "🛑 Arrêter le Vérificateur",
        "stop_body": "Exécutez **`stopD4UCChecker`**."
    },
    "de": {
        "title": "⚡ D4UC Google Apps Script (GAS) 24/7 Serverless Checker",
        "desc": "> **Läuft rund um die Uhr (24/7/365) in der Google Cloud, ohne dass PC oder Smartphone laufen müssen.**",
        "quick_start": "🚀 1-Minute Schnellstartanleitung",
        "step1_title": "Schritt 1: Google Apps Script Projekt erstellen",
        "step1_body": "1. Öffnen Sie [Google Apps Script](https://script.google.com/) und erstellen Sie `D4UC 24/7 Checker`.",
        "step2_title": "Schritt 2: Code einfügen & konfigurieren",
        "step2_body": "1. Fügen Sie [`gas/D4UC_Checker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_Checker.js) ein.\n2. Konfigurieren Sie `CONFIG` und speichern Sie.",
        "step3_title": "Schritt 3: Initialisierung starten",
        "step3_body": "1. Wählen Sie **`initD4UCChecker`** und führen Sie es aus.\n2. Berechtigungen erteilen.",
        "results_title": "📊 Ergebnisse",
        "results_body": "Speicherung auf Google Drive, Google Sheets und Discord-Webhooks.",
        "multi_title": "🌐 Multi-Account Sharding (100k~240k Checks/Tag)",
        "multi_body": "Verwenden Sie [`gas/D4UC_MultiAccount_Worker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_MultiAccount_Worker.js) auf zusätzlichen Konten.",
        "stop_title": "🛑 Beenden",
        "stop_body": "Führen Sie **`stopD4UCChecker`** aus."
    },
    "ru": {
        "title": "⚡ D4UC Google Apps Script (GAS) 24/7 Серверлесс Чекер",
        "desc": "> **Работает 24 часа в сутки 365 дней в году в Google Cloud без включенного ПК или смартфона.**",
        "quick_start": "🚀 Быстрый старт за 1 минуту",
        "step1_title": "Шаг 1: Создание проекта Google Apps Script",
        "step1_body": "1. Откройте [Google Apps Script](https://script.google.com/) и создайте проект `D4UC 24/7 Checker`.",
        "step2_title": "Шаг 2: Вставка кода и настройка",
        "step2_body": "1. Вставьте [`gas/D4UC_Checker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_Checker.js).\n2. Настройте `CONFIG` и сохраните.",
        "step3_title": "Шаг 3: Запуск 24/7",
        "step3_body": "1. Выберите **`initD4UCChecker`** и нажмите **[Выполнить]**.\n2. Предоставьте разрешения.",
        "results_title": "📊 Результаты",
        "results_body": "Google Диск, Google Таблицы и Discord Webhook.",
        "multi_title": "🌐 Мульти-аккаунт шардинг (100k~240k проверок в день)",
        "multi_body": "Используйте [`gas/D4UC_MultiAccount_Worker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_MultiAccount_Worker.js) на других аккаунтах.",
        "stop_title": "🛑 Остановка",
        "stop_body": "Выполните **`stopD4UCChecker`**."
    },
    "pt-BR": {
        "title": "⚡ D4UC Google Apps Script (GAS) Verificador 24/7 Serverless",
        "desc": "> **Execução 24 horas por dia, 365 dias por ano na nuvem Google sem manter PC ou smartphone ligados.**",
        "quick_start": "🚀 Guia Rápido de 1 Minuto",
        "step1_title": "Passo 1: Criar projeto no Google Apps Script",
        "step1_body": "1. Acesse [Google Apps Script](https://script.google.com/) e crie `D4UC 24/7 Checker`.",
        "step2_title": "Passo 2: Inserir código e configurar",
        "step2_body": "1. Cole [`gas/D4UC_Checker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_Checker.js) em `Code.gs`.\n2. Configure `CONFIG` e salve.",
        "step3_title": "Passo 3: Inicializar 24/7",
        "step3_body": "1. Execute **`initD4UCChecker`** e conceda as permissões.",
        "results_title": "📊 Resultados",
        "results_body": "Google Drive, Google Sheets e alertas via Discord Webhook.",
        "multi_title": "🌐 Aceleração Multi-Contas (100k~240k Verificações/Dia)",
        "multi_body": "Utilize [`gas/D4UC_MultiAccount_Worker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_MultiAccount_Worker.js) em contas adicionais.",
        "stop_title": "🛑 Parar o Verificador",
        "stop_body": "Execute **`stopD4UCChecker`**."
    },
    "ar": {
        "title": "⚡ فاحص D4UC بدون خادم Google Apps Script على مدار 24/7",
        "desc": "> **يعمل على مدار الساعة 365 يومًا دون الحاجة لإبقاء الكمبيوتر أو الهاتف مفتوحًا.**",
        "quick_start": "🚀 دليل البدء السريع في دقيقة واحدة",
        "step1_title": "الخطوة 1: إنشاء مشروع Google Apps Script",
        "step1_body": "1. افتح [Google Apps Script](https://script.google.com/) وأنشئ مشروع `D4UC 24/7 Checker`.",
        "step2_title": "الخطوة 2: نسخ الكود والتهيئة",
        "step2_body": "1. الصق كود [`gas/D4UC_Checker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_Checker.js).\n2. اضبط `CONFIG` واحفظ.",
        "step3_title": "الخطوة 3: بدء التشغيل التلقائي",
        "step3_body": "1. اختر **`initD4UCChecker`** واضغط **[تشغيل]**.\n2. امنح الأذونات.",
        "results_title": "📊 التحقق من النتائج",
        "results_body": "Google Drive و Google Sheets مع إشعارات Discord Webhook الفورية.",
        "multi_title": "🌐 تسريع متعدد الحسابات (100 ألف ~ 240 ألف فحص يوميًا)",
        "multi_body": "استخدم [`gas/D4UC_MultiAccount_Worker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_MultiAccount_Worker.js) في حساباتك الإضافية.",
        "stop_title": "🛑 إيقاف الفاحص",
        "stop_body": "اختر **`stopD4UCChecker`** واضغط **[تشغيل]**."
    },
    "hi": {
        "title": "⚡ D4UC Google Apps Script (GAS) 24/7 सर्वरलेस चेकर",
        "desc": "> **पीसी या मोबाइल चालू रखे बिना Google क्लाउड पर 24 घंटे 365 दिन स्वचालित रूप से चलता है।**",
        "quick_start": "🚀 1-मिनट क्विक स्टार्ट गाइड",
        "step1_title": "चरण 1: Google Apps Script प्रोजेक्ट बनाएं",
        "step1_body": "1. [Google Apps Script](https://script.google.com/) खोलें और `D4UC 24/7 Checker` बनाएं।",
        "step2_title": "चरण 2: कोड कॉपी और कॉन्फ़िगर करें",
        "step2_body": "1. [`gas/D4UC_Checker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_Checker.js) पेस्ट करें।\n2. `CONFIG` सेट करें और सेव करें।",
        "step3_title": "चरण 3: स्वचालित रनर प्रारंभ करें",
        "step3_body": "1. **`initD4UCChecker`** चुनें और **[Run]** दबाएं।",
        "results_title": "📊 परिणाम जांच",
        "results_body": "Google Drive, Google Sheets और Discord Webhook पर रीयल-टाइम सूचनाएं।",
        "multi_title": "🌐 मल्टी-अकाउंट गतिवर्धन (प्रतिदिन 100k~240k जांच)",
        "multi_body": "अतिरिक्त खातों में [`gas/D4UC_MultiAccount_Worker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_MultiAccount_Worker.js) चलाएं।",
        "stop_title": "🛑 चेकर बंद करें",
        "stop_body": "**`stopD4UCChecker`** चलाकर सभी ट्रिगर हटाएं।"
    },
    "id": {
        "title": "⚡ D4UC Google Apps Script (GAS) Checker Serverless 24/7",
        "desc": "> **Berjalan 24 jam 365 hari di Google Cloud tanpa perlu menyalakan PC atau smartphone.**",
        "quick_start": "🚀 Panduan Cepat 1 Menit",
        "step1_title": "Langkah 1: Buat Proyek Google Apps Script",
        "step1_body": "1. Buka [Google Apps Script](https://script.google.com/) dan buat `D4UC 24/7 Checker`.",
        "step2_title": "Langkah 2: Salin Kode & Konfigurasi",
        "step2_body": "1. Tempel [`gas/D4UC_Checker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_Checker.js) ke `Code.gs`.\n2. Sesuaikan `CONFIG` dan simpan.",
        "step3_title": "Langkah 3: Jalankan 24/7 Otomatis",
        "step3_body": "1. Pilih **`initD4UCChecker`** lalu klik **[Jalankan]**.",
        "results_title": "📊 Verifikasi Hasil",
        "results_body": "Google Drive, Google Sheets, dan notifikasi Discord Webhook.",
        "multi_title": "🌐 Akselerasi Multi-Akun (100k~240k Pengecekan/Hari)",
        "multi_body": "Gunakan [`gas/D4UC_MultiAccount_Worker.js`](https://github.com/KRCUPRO/discord-checker/blob/main/gas/D4UC_MultiAccount_Worker.js) pada akun tambahan.",
        "stop_title": "🛑 Menghentikan Checker",
        "stop_body": "Pilih **`stopD4UCChecker`** lalu klik **[Jalankan]**."
    }
}

for loc, d in DATA.items():
    file_path = root / f"docs/locales/{loc}/gas/README.md"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    content = f"""<div align="center">

# {d['title']}

{d['desc']}

<br />

{LANG_TABLE}

</div>

## {d['quick_start']}

### {d['step1_title']}
{d['step1_body']}

---

### {d['step2_title']}
{d['step2_body']}

---

### {d['step3_title']}
{d['step3_body']}

---

## {d['results_title']}
{d['results_body']}

---

## {d['multi_title']}
{d['multi_body']}

---

## {d['stop_title']}
{d['stop_body']}
"""
    file_path.write_text(content, encoding="utf-8")
    print(f"Generated: {file_path}")

# Also update root gas/README.md in English
root_gas_readme = root / "gas/README.md"
en_d = DATA["en"]
root_content = f"""<div align="center">

# {en_d['title']}

{en_d['desc']}

<br />

{LANG_TABLE.replace('../', '../docs/locales/')}

</div>

## {en_d['quick_start']}

### {en_d['step1_title']}
{en_d['step1_body'].replace('../../../../gas/', '')}

---

### {en_d['step2_title']}
{en_d['step2_body'].replace('../../../../gas/', '')}

---

### {en_d['step3_title']}
{en_d['step3_body']}

---

## {en_d['results_title']}
{en_d['results_body']}

---

## {en_d['multi_title']}
{en_d['multi_body'].replace('../../../../gas/', '')}

---

## {en_d['stop_title']}
{en_d['stop_body']}
"""
root_gas_readme.write_text(root_content, encoding="utf-8")
print(f"Generated: {root_gas_readme}")

print("All 12 localized gas/README.md + root gas/README.md generated successfully!")
