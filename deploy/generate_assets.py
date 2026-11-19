# deploy/generate_assets.py
"""
High-Fidelity Visual Asset Generator for D4UC v12.2.0 Documentation.
Generates pixel-perfect PNG screenshots and animated GIFs with natural mouse-cursor movement
for ALL 12 supported languages:
- ko, en, ja, zh, es, fr, de, ru, pt, ar, hi, id
"""
import math
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT_DIR / "docs" / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Fonts
FONT_UI_REG = r"C:\Windows\Fonts\segoeui.ttf"
FONT_UI_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_KR_REG = r"C:\Windows\Fonts\malgun.ttf"
FONT_KR_BOLD = r"C:\Windows\Fonts\malgunbd.ttf"
FONT_JA_REG = r"C:\Windows\Fonts\msgothic.ttc"
FONT_ZH_REG = r"C:\Windows\Fonts\msyh.ttc"
FONT_AR_REG = r"C:\Windows\Fonts\tahoma.ttf"
FONT_AR_BOLD = r"C:\Windows\Fonts\tahomabd.ttf"
FONT_HI_REG = r"C:\Windows\Fonts\Nirmala.ttc"
FONT_HI_BOLD = r"C:\Windows\Fonts\NirmalaB.ttf"
FONT_MONO = r"C:\Windows\Fonts\consola.ttf"
FONT_MONO_BOLD = r"C:\Windows\Fonts\consolab.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def get_gui_fonts(lang: str):
    if lang == "ko":
        return (
            get_font(FONT_KR_BOLD, 13),
            get_font(FONT_KR_REG, 11),
            get_font(FONT_KR_REG, 13),
            get_font(FONT_KR_BOLD, 13),
            get_font(FONT_KR_BOLD, 20),
            get_font(FONT_KR_REG, 11),
        )
    elif lang == "ja":
        return (
            get_font(FONT_JA_REG, 13),
            get_font(FONT_JA_REG, 11),
            get_font(FONT_JA_REG, 12),
            get_font(FONT_JA_REG, 13),
            get_font(FONT_JA_REG, 18),
            get_font(FONT_JA_REG, 10),
        )
    elif lang == "zh":
        return (
            get_font(FONT_ZH_REG, 13),
            get_font(FONT_ZH_REG, 11),
            get_font(FONT_ZH_REG, 12),
            get_font(FONT_ZH_REG, 13),
            get_font(FONT_ZH_REG, 18),
            get_font(FONT_ZH_REG, 10),
        )
    elif lang == "ar":
        f_b = get_font(FONT_AR_BOLD, 13) if Path(FONT_AR_BOLD).exists() else get_font(FONT_AR_REG, 13)
        return (
            f_b,
            get_font(FONT_AR_REG, 11),
            get_font(FONT_AR_REG, 12),
            f_b,
            get_font(FONT_AR_REG, 18),
            get_font(FONT_AR_REG, 10),
        )
    elif lang == "hi":
        f_b = get_font(FONT_HI_BOLD, 13) if Path(FONT_HI_BOLD).exists() else get_font(FONT_HI_REG, 13)
        return (
            f_b,
            get_font(FONT_HI_REG, 11),
            get_font(FONT_HI_REG, 12),
            f_b,
            get_font(FONT_HI_REG, 18),
            get_font(FONT_HI_REG, 10),
        )
    else:  # en, es, fr, de, ru, pt, id
        return (
            get_font(FONT_UI_BOLD, 13),
            get_font(FONT_UI_REG, 11),
            get_font(FONT_UI_REG, 13),
            get_font(FONT_UI_BOLD, 13),
            get_font(FONT_UI_BOLD, 20),
            get_font(FONT_UI_REG, 11),
        )

# Colors (Discord Dark Theme Palette)
BG_APP = (30, 31, 34)       # #1e1f22
BG_PANEL = (43, 45, 49)     # #2b2d31
BG_CARD = (49, 51, 56)      # #313338
BG_INPUT = (35, 36, 40)     # #232428
BG_TITLEBAR = (24, 25, 28)  # #18191c
BORDER = (60, 63, 69)       # #3c3f45
BORDER_FOCUS = (88, 101, 242)  # Discord Blurple

TEXT_WHITE = (242, 243, 245)
TEXT_MUTED = (148, 155, 164)
TEXT_SUCCESS = (35, 165, 90)   # #23a55a
TEXT_DANGER = (242, 63, 67)    # #f23f43
TEXT_ACCENT = (88, 101, 242)   # #5865F2
TEXT_CYAN = (0, 196, 204)
TEXT_YELLOW = (250, 166, 26)

GUI_I18N = {
    "ko": {
        "title": "D4UC v12.2.0 - Discord Username Checker [한국어 에디션]",
        "banner": "[온보딩] Chrome 131 TLS 스텔스 위장 및 1:1 WireGuard 터널 풀이 자동 적용됩니다. 시작을 눌러 가동하세요.",
        "lbl_mode": "생성 모드",
        "val_mode": "하이브리드 (Hybrid)  ▼",
        "lbl_len": "자릿수",
        "lbl_wk": "워커수",
        "lbl_sh": "샤드 분할",
        "lbl_px": "프록시 엔진",
        "val_px": "● 1:1 Surfshark WireGuard",
        "btn_stop": "■ 중지",
        "btn_start": "▶ 시작",
        "btn_settings": "환경 설정",
        "stat_total": "총 검사",
        "stat_avail": "가용 발견",
        "stat_taken": "선점 완료",
        "stat_429": "429 교체 회수",
        "stat_speed": "현재 속도",
        "stat_lat": "평균 레이턴시",
        "tbl_avail": "발견된 가용 닉네임 목록",
        "tbl_log": "실시간 엔진 로그",
        "status_bar": "● 5개 WireGuard 터널 정상 가동 중 (KR, JP, SG, US, DE)  |  SQLite WAL 활성화: data/d4uc_results.db",
    },
    "en": {
        "title": "D4UC v12.2.0 - Discord Username Checker [English Edition]",
        "banner": "[ONBOARDING] Chrome 131 TLS stealth & 1:1 isolated WireGuard tunnel pool active. Click Start to begin.",
        "lbl_mode": "Mode",
        "val_mode": "Hybrid (Dict+Num)  ▼",
        "lbl_len": "Length",
        "lbl_wk": "Workers",
        "lbl_sh": "Sharding",
        "lbl_px": "Proxy Engine",
        "val_px": "● 1:1 Surfshark WireGuard",
        "btn_stop": "■ Stop",
        "btn_start": "▶ Start",
        "btn_settings": "Settings",
        "stat_total": "Total Checked",
        "stat_avail": "Available Found",
        "stat_taken": "Taken (404/200)",
        "stat_429": "429 Hot-Swaps",
        "stat_speed": "Current Speed",
        "stat_lat": "Avg Latency",
        "tbl_avail": "Found Available Handles",
        "tbl_log": "Live Engine Logs",
        "status_bar": "● 5 WireGuard Tunnels Active (KR, JP, SG, US, DE) | SQLite WAL Sync: data/d4uc_results.db",
    },
    "ja": {
        "title": "D4UC v12.2.0 - Discord Username Checker [日本語エディション]",
        "banner": "[オンボーディング] Chrome 131 TLSステルス偽装および1:1 WireGuardトンネルプールが有効です。[開始]をクリックして起動してください。",
        "lbl_mode": "生成モード",
        "val_mode": "ハイブリッド (Hybrid)  ▼",
        "lbl_len": "桁数",
        "lbl_wk": "ワーカー数",
        "lbl_sh": "シャード分割",
        "lbl_px": "プロキシエンジン",
        "val_px": "● 1:1 Surfshark WireGuard",
        "btn_stop": "■ 停止",
        "btn_start": "▶ 開始",
        "btn_settings": "環境設定",
        "stat_total": "総検査数",
        "stat_avail": "利用可能発見",
        "stat_taken": "取得済 (TAKEN)",
        "stat_429": "429 切替回数",
        "stat_speed": "現在の速度",
        "stat_lat": "平均遅延",
        "tbl_avail": "発見された利用可能ニックネーム",
        "tbl_log": "リアルタイムエンジンログ",
        "status_bar": "● 5つのWireGuardトンネル正常稼働中 (KR, JP, SG, US, DE) | SQLite WAL 同期中",
    },
    "zh": {
        "title": "D4UC v12.2.0 - Discord Username Checker [简体中文版]",
        "banner": "[引导] Chrome 131 TLS 隐身伪装和 1:1 WireGuard 隧道池已启用。点击开始以启动。",
        "lbl_mode": "生成模式",
        "val_mode": "混合模式 (Hybrid)  ▼",
        "lbl_len": "长度",
        "lbl_wk": "工作线程",
        "lbl_sh": "分片预设",
        "lbl_px": "代理引擎",
        "val_px": "● 1:1 Surfshark WireGuard",
        "btn_stop": "■ 停止",
        "btn_start": "▶ 开始",
        "btn_settings": "系统设置",
        "stat_total": "总检查数",
        "stat_avail": "发现可用",
        "stat_taken": "已占用 (TAKEN)",
        "stat_429": "429 节点切换",
        "stat_speed": "当前速度",
        "stat_lat": "平均延迟",
        "tbl_avail": "发现的可用用户名",
        "tbl_log": "实时引擎日志",
        "status_bar": "● 5个WireGuard隧道正常运行中 (KR, JP, SG, US, DE) | SQLite WAL 同步激活",
    },
    "es": {
        "title": "D4UC v12.2.0 - Discord Username Checker [Edición en Español]",
        "banner": "[INTEGRACIÓN] Sigilo Chrome 131 TLS y túnel WireGuard 1:1 activos. Haga clic en Iniciar para comenzar.",
        "lbl_mode": "Modo",
        "val_mode": "Híbrido (Dict+Num)  ▼",
        "lbl_len": "Longitud",
        "lbl_wk": "Hilos",
        "lbl_sh": "Fragmentación",
        "lbl_px": "Motor Proxy",
        "val_px": "● 1:1 Surfshark WireGuard",
        "btn_stop": "■ Detener",
        "btn_start": "▶ Iniciar",
        "btn_settings": "Ajustes",
        "stat_total": "Total Verif.",
        "stat_avail": "Disponibles",
        "stat_taken": "Ocupados",
        "stat_429": "429 Reemplazos",
        "stat_speed": "Velocidad actual",
        "stat_lat": "Latencia media",
        "tbl_avail": "Nombres disponibles descubiertos",
        "tbl_log": "Registros del motor en vivo",
        "status_bar": "● 5 túneles WireGuard activos (KR, JP, SG, US, DE) | Sincronización SQLite WAL",
    },
    "fr": {
        "title": "D4UC v12.2.0 - Discord Username Checker [Édition Française]",
        "banner": "[INTÉGRATION] Furtivité Chrome 131 TLS et tunnel WireGuard 1:1 actifs. Cliquez sur Démarrer pour lancer.",
        "lbl_mode": "Mode",
        "val_mode": "Hybride (Dict+Num)  ▼",
        "lbl_len": "Longueur",
        "lbl_wk": "Workers",
        "lbl_sh": "Sharding",
        "lbl_px": "Moteur Proxy",
        "val_px": "● 1:1 Surfshark WireGuard",
        "btn_stop": "■ Arrêter",
        "btn_start": "▶ Démarrer",
        "btn_settings": "Paramètres",
        "stat_total": "Total Vérif.",
        "stat_avail": "Disponibles",
        "stat_taken": "Occupés",
        "stat_429": "429 Échanges",
        "stat_speed": "Vitesse actuelle",
        "stat_lat": "Latence moy.",
        "tbl_avail": "Noms d'utilisateur disponibles",
        "tbl_log": "Journaux du moteur en direct",
        "status_bar": "● 5 tunnels WireGuard actifs (KR, JP, SG, US, DE) | Synchronisation SQLite WAL",
    },
    "de": {
        "title": "D4UC v12.2.0 - Discord Username Checker [Deutsche Ausgabe]",
        "banner": "[ONBOARDING] Chrome 131 TLS-Stealth & 1:1 WireGuard-Tunnelpool aktiv. Klicken Sie auf Start, um zu beginnen.",
        "lbl_mode": "Modus",
        "val_mode": "Hybrid (Wörter+Zahl)  ▼",
        "lbl_len": "Länge",
        "lbl_wk": "Worker",
        "lbl_sh": "Sharding",
        "lbl_px": "Proxy-Engine",
        "val_px": "● 1:1 Surfshark WireGuard",
        "btn_stop": "■ Stopp",
        "btn_start": "▶ Start",
        "btn_settings": "Einstellungen",
        "stat_total": "Gesamt geprüft",
        "stat_avail": "Verfügbar",
        "stat_taken": "Belegt",
        "stat_429": "429 Tausch",
        "stat_speed": "Aktuelle Geschw.",
        "stat_lat": "Ø Latenz",
        "tbl_avail": "Entdeckte verfügbare Namen",
        "tbl_log": "Live-Engine-Protokolle",
        "status_bar": "● 5 WireGuard-Tunnel aktiv (KR, JP, SG, US, DE) | SQLite WAL Sync aktiv",
    },
    "ru": {
        "title": "D4UC v12.2.0 - Discord Username Checker [Русское издание]",
        "banner": "[ОНБОРДИНГ] Стелс-маскировка Chrome 131 TLS и туннели WireGuard 1:1 активны. Нажмите Запуск для старта.",
        "lbl_mode": "Режим",
        "val_mode": "Гибридный (Dict+Num)  ▼",
        "lbl_len": "Длина",
        "lbl_wk": "Потоки",
        "lbl_sh": "Шардинг",
        "lbl_px": "Прокси-движок",
        "val_px": "● 1:1 Surfshark WireGuard",
        "btn_stop": "■ Стоп",
        "btn_start": "▶ Старт",
        "btn_settings": "Настройки",
        "stat_total": "Всего проверено",
        "stat_avail": "Доступно",
        "stat_taken": "Занято",
        "stat_429": "429 Замен узлов",
        "stat_speed": "Текущая скорость",
        "stat_lat": "Сред. задержка",
        "tbl_avail": "Найденные доступные никнеймы",
        "tbl_log": "Логи движка в реальном времени",
        "status_bar": "● 5 туннелей WireGuard активны (KR, JP, SG, US, DE) | Синхронизация SQLite WAL",
    },
    "pt": {
        "title": "D4UC v12.2.0 - Discord Username Checker [Edição Portuguesa]",
        "banner": "[INTEGRAÇÃO] Furtividade Chrome 131 TLS e túnel WireGuard 1:1 ativos. Clique em Iniciar para começar.",
        "lbl_mode": "Modo",
        "val_mode": "Híbrido (Dict+Num)  ▼",
        "lbl_len": "Tamanho",
        "lbl_wk": "Workers",
        "lbl_sh": "Fragmentação",
        "lbl_px": "Motor Proxy",
        "val_px": "● 1:1 Surfshark WireGuard",
        "btn_stop": "■ Parar",
        "btn_start": "▶ Iniciar",
        "btn_settings": "Configurações",
        "stat_total": "Total Verif.",
        "stat_avail": "Disponíveis",
        "stat_taken": "Ocupados",
        "stat_429": "429 Trocas IP",
        "stat_speed": "Velocidade Atual",
        "stat_lat": "Latência Média",
        "tbl_avail": "Nomes de usuário disponíveis",
        "tbl_log": "Logs do Motor em Tempo Real",
        "status_bar": "● 5 túneis WireGuard ativos (KR, JP, SG, US, DE) | Sincronização SQLite WAL",
    },
    "ar": {
        "title": "D4UC v12.2.0 - Discord Username Checker [النسخة العربية]",
        "banner": "[تهيئة] تخفي Chrome 131 TLS ونفق WireGuard 1:1 نشط. انقر فوق بدء للتشغيل.",
        "lbl_mode": "الوضع",
        "val_mode": "هجين (Hybrid)  ▼",
        "lbl_len": "الطول",
        "lbl_wk": "العمال",
        "lbl_sh": "تجزئة",
        "lbl_px": "محرك البروكسي",
        "val_px": "● 1:1 Surfshark WireGuard",
        "btn_stop": "■ إيقاف",
        "btn_start": "▶ بدء",
        "btn_settings": "الإعدادات",
        "stat_total": "إجمالي الفحص",
        "stat_avail": "المتاحة المكتشفة",
        "stat_taken": "محجوزة",
        "stat_429": "تبديلات 429",
        "stat_speed": "السرعة الحالية",
        "stat_lat": "متوسط التأخير",
        "tbl_avail": "أسماء المستخدمين المتاحة",
        "tbl_log": "سجلات المحرك المباشرة",
        "status_bar": "● 5 أنفاق WireGuard نشطة (KR, JP, SG, US, DE) | مزامنة SQLite WAL",
    },
    "hi": {
        "title": "D4UC v12.2.0 - Discord Username Checker [हिन्दी संस्करण]",
        "banner": "[ऑनबोर्डिंग] Chrome 131 TLS स्टील्थ और 1:1 WireGuard टनल सक्रिय है। आरंभ करने के लिए स्टार्ट दबाएं।",
        "lbl_mode": "मोड",
        "val_mode": "हाइब्रिड (Hybrid)  ▼",
        "lbl_len": "लंबाई",
        "lbl_wk": "वर्कर्स",
        "lbl_sh": "शार्डिंग",
        "lbl_px": "प्रॉक्सी इंजन",
        "val_px": "● 1:1 Surfshark WireGuard",
        "btn_stop": "■ रोकें",
        "btn_start": "▶ शुरू",
        "btn_settings": "सेटिंग्स",
        "stat_total": "कुल जाँचे गए",
        "stat_avail": "उपलब्ध पाए गए",
        "stat_taken": "लिए गए",
        "stat_429": "429 हॉट-स्वैप",
        "stat_speed": "वर्तमान गति",
        "stat_lat": "औसत विलंबता",
        "tbl_avail": "खोजे गए उपलब्ध नाम",
        "tbl_log": "लाइव इंजन लॉग्स",
        "status_bar": "● 5 WireGuard टनल सक्रिय हैं (KR, JP, SG, US, DE) | SQLite WAL सिंक",
    },
    "id": {
        "title": "D4UC v12.2.0 - Discord Username Checker [Edisi Bahasa Indonesia]",
        "banner": "[ONBOARDING] Penyamaran Chrome 131 TLS & terowongan WireGuard 1:1 aktif. Klik Mulai untuk menjalankan.",
        "lbl_mode": "Mode",
        "val_mode": "Hibrida (Hybrid)  ▼",
        "lbl_len": "Panjang",
        "lbl_wk": "Pekerja",
        "lbl_sh": "Sharding",
        "lbl_px": "Mesin Proksi",
        "val_px": "● 1:1 Surfshark WireGuard",
        "btn_stop": "■ Berhenti",
        "btn_start": "▶ Mulai",
        "btn_settings": "Pengaturan",
        "stat_total": "Total Diperiksa",
        "stat_avail": "Tersedia Ditemukan",
        "stat_taken": "Digunakan",
        "stat_429": "429 Pergantian",
        "stat_speed": "Kecepatan Saat Ini",
        "stat_lat": "Rata-rata Latensi",
        "tbl_avail": "Username Tersedia Ditemukan",
        "tbl_log": "Log Mesin Real-time",
        "status_bar": "● 5 Terowongan WireGuard Aktif (KR, JP, SG, US, DE) | Sinkronisasi SQLite WAL",
    }
}

def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def draw_cursor(img, pos, clicking=False):
    """Draws a crisp modern mouse cursor at pos with optional click ripple."""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    x, y = pos

    if clicking:
        d.ellipse([x - 14, y - 14, x + 14, y + 14], fill=(88, 101, 242, 100), outline=(88, 101, 242, 220), width=2)

    cursor_pts = [
        (x, y),
        (x, y + 18),
        (x + 4, y + 14),
        (x + 8, y + 23),
        (x + 12, y + 21),
        (x + 8, y + 12),
        (x + 14, y + 12),
    ]
    shadow_pts = [(px + 2, py + 2) for px, py in cursor_pts]
    d.polygon(shadow_pts, fill=(0, 0, 0, 100))
    d.polygon(cursor_pts, fill=(255, 255, 255, 255))
    d.line(cursor_pts + [(x, y)], fill=(20, 20, 20, 255), width=1)
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay), (0, 0))

def render_gui_base(lang="ko", is_running=False, metrics=None, custom_cursor=None, is_clicking=False, table_items=None):
    i18n = GUI_I18N.get(lang, GUI_I18N["en"])
    w, h = 1200, 780
    img = Image.new("RGBA", (w, h), BG_APP)
    draw = ImageDraw.Draw(img)

    f_title, f_badge, f_body, f_bold, f_stat_val, f_stat_lbl = get_gui_fonts(lang)
    f_mono = get_font(FONT_MONO, 12)
    f_mono_bold = get_font(FONT_MONO_BOLD, 12)
    f_mono_sm = get_font(FONT_MONO, 11)

    # 1. Window Titlebar
    draw.rectangle([0, 0, w, 36], fill=BG_TITLEBAR)
    draw.text((16, 9), i18n["title"], fill=TEXT_WHITE, font=f_title)
    
    # Titlebar controls (min, max, close)
    draw.line([w - 110, 18, w - 100, 18], fill=TEXT_MUTED, width=2)
    draw.rectangle([w - 75, 13, w - 65, 23], outline=TEXT_MUTED, width=1)
    draw.line([w - 35, 13, w - 25, 23], fill=TEXT_MUTED, width=2)
    draw.line([w - 25, 13, w - 35, 23], fill=TEXT_MUTED, width=2)

    # 2. Onboarding Notification Banner
    draw_rounded_rect(draw, [16, 48, w - 16, 84], radius=6, fill=BG_CARD, outline=BORDER)
    draw.text((32, 57), i18n["banner"], fill=TEXT_CYAN, font=f_body)

    # 3. Top Control Bar Panel
    draw_rounded_rect(draw, [16, 96, w - 16, 168], radius=8, fill=BG_PANEL, outline=BORDER)
    
    # Mode Dropdown
    draw.text((32, 108), i18n["lbl_mode"], fill=TEXT_MUTED, font=f_badge)
    draw_rounded_rect(draw, [32, 126, 210, 156], radius=5, fill=BG_INPUT, outline=BORDER)
    draw.text((42, 133), i18n["val_mode"], fill=TEXT_WHITE, font=f_body)

    # Length
    draw.text((230, 108), i18n["lbl_len"], fill=TEXT_MUTED, font=f_badge)
    draw_rounded_rect(draw, [230, 126, 290, 156], radius=5, fill=BG_INPUT, outline=BORDER)
    draw.text((254, 133), "4", fill=TEXT_WHITE, font=f_body)

    # Workers
    draw.text((310, 108), i18n["lbl_wk"], fill=TEXT_MUTED, font=f_badge)
    draw_rounded_rect(draw, [310, 126, 380, 156], radius=5, fill=BG_INPUT, outline=BORDER)
    draw.text((338, 133), "5", fill=TEXT_WHITE, font=f_body)

    # Shard Presets
    draw.text((400, 108), i18n["lbl_sh"], fill=TEXT_MUTED, font=f_badge)
    draw_rounded_rect(draw, [400, 126, 520, 156], radius=5, fill=BG_INPUT, outline=BORDER)
    draw.text((412, 133), "2_1 (a–m)  ▼", fill=TEXT_WHITE, font=f_body)

    # Proxy Engine Status
    draw.text((540, 108), i18n["lbl_px"], fill=TEXT_MUTED, font=f_badge)
    draw_rounded_rect(draw, [540, 126, 730, 156], radius=5, fill=BG_INPUT, outline=BORDER)
    draw.text((552, 133), i18n["val_px"], fill=TEXT_SUCCESS, font=f_badge)

    # Action Buttons: Start/Stop, Settings
    btn_start_col = TEXT_DANGER if is_running else TEXT_ACCENT
    draw_rounded_rect(draw, [760, 120, 890, 160], radius=6, fill=btn_start_col)
    btn_start_txt = i18n["btn_stop"] if is_running else i18n["btn_start"]
    draw.text((800, 131), btn_start_txt, fill=TEXT_WHITE, font=f_bold)

    draw_rounded_rect(draw, [905, 120, 1010, 160], radius=6, fill=BG_CARD, outline=BORDER)
    draw.text((924, 131), i18n["btn_settings"], fill=TEXT_WHITE, font=f_body)

    # 4. Telemetry Metric Cards (6 cards in horizontal row)
    card_y = 180
    card_h = 72
    card_w = (w - 32 - 50) // 6
    
    m = metrics or {}
    speed_txt = m.get("speed", "14.8 RPS" if is_running else "0.0 RPS")
    checked_txt = m.get("checked", "1,240" if is_running else "0")
    avail_txt = m.get("avail", "3" if is_running else "0")
    taken_txt = m.get("taken", "1,237" if is_running else "0")
    hotswap_txt = m.get("hotswap", "1" if is_running else "0")
    lat_txt = "38ms" if is_running else "--"

    stat_cards = [
        (i18n["stat_total"], checked_txt, TEXT_WHITE),
        (i18n["stat_avail"], avail_txt, TEXT_SUCCESS),
        (i18n["stat_taken"], taken_txt, TEXT_WHITE),
        (i18n["stat_429"], hotswap_txt, TEXT_YELLOW),
        (i18n["stat_speed"], speed_txt, TEXT_CYAN),
        (i18n["stat_lat"], lat_txt, TEXT_WHITE),
    ]

    for idx, (label, val, col) in enumerate(stat_cards):
        cx = 16 + idx * (card_w + 10)
        draw_rounded_rect(draw, [cx, card_y, cx + card_w, card_y + card_h], radius=6, fill=BG_CARD, outline=BORDER)
        draw.text((cx + 12, card_y + 10), label, fill=TEXT_MUTED, font=f_stat_lbl)
        draw.text((cx + 12, card_y + 32), val, fill=col, font=f_stat_val)

    # 5. Dual Content Area: Real-Time Live Logs (Left) and Available Usernames Table (Right)
    content_y1 = 264
    content_y2 = h - 40
    split_x = int(w * 0.44)

    # Left Panel: Live Engine Logs
    draw_rounded_rect(draw, [16, content_y1, split_x, content_y2], radius=6, fill=BG_CARD, outline=BORDER)
    draw.rectangle([16, content_y1, split_x, content_y1 + 30], fill=BG_PANEL)
    draw.text((28, content_y1 + 7), i18n["tbl_log"], fill=TEXT_WHITE, font=f_badge)
    
    logs = [
        ("[12:20:00]", "INIT", "D4UC Engine initialized with 5 workers", TEXT_MUTED),
        ("[12:20:01]", "TUNL", "5 Surfshark WireGuard tunnels verified active", TEXT_CYAN),
        ("[12:20:15]", "HIT", ">> Worker #3 [SG]: 'k4rc' is AVAILABLE! (200 OK)", TEXT_SUCCESS),
        ("[12:20:16]", "ALERT", "Dispatched Discord Webhook alert to #rare-names", TEXT_ACCENT),
        ("[12:20:45]", "INFO", "Batch 50 checked. Speed: 14.2 req/s", TEXT_MUTED),
        ("[12:21:04]", "HIT", ">> Worker #4 [US]: 'z99p' is AVAILABLE! (200 OK)", TEXT_SUCCESS),
        ("[12:21:28]", "SWAP", "Worker #5 [DE] hit 429 -> Hot-swap to DE-Frankfurt-2 (0.28s)", TEXT_YELLOW),
        ("[12:21:49]", "HIT", ">> Worker #2 [KR]: 'qv2x' is AVAILABLE! (200 OK)", TEXT_SUCCESS),
    ]
    for idx, (ts, tag, msg, color) in enumerate(logs):
        ly = content_y1 + 38 + idx * 22
        if ly > content_y2 - 25:
            break
        draw.text((26, ly), ts, fill=TEXT_MUTED, font=f_mono_sm)
        draw.text((95, ly), f"[{tag}]", fill=color, font=f_mono_sm)
        disp_msg = msg[:48] + "..." if len(msg) > 50 else msg
        draw.text((150, ly), disp_msg, fill=TEXT_WHITE if color != TEXT_SUCCESS else TEXT_SUCCESS, font=f_mono_sm)

    # Right Panel: Available Usernames Table
    draw_rounded_rect(draw, [split_x + 8, content_y1, w - 16, content_y2], radius=6, fill=BG_CARD, outline=BORDER)
    draw.rectangle([split_x + 8, content_y1, w - 16, content_y1 + 30], fill=BG_PANEL)
    draw.text((split_x + 20, content_y1 + 7), i18n["tbl_avail"], fill=TEXT_WHITE, font=f_badge)
    
    # Table Header
    th_y = content_y1 + 32
    draw.rectangle([split_x + 8, th_y, w - 16, th_y + 26], fill=(38, 40, 44))
    draw.text((split_x + 24, th_y + 5), "#", fill=TEXT_MUTED, font=f_mono_sm)
    draw.text((split_x + 70, th_y + 5), "Username", fill=TEXT_MUTED, font=f_badge)
    draw.text((split_x + 220, th_y + 5), "Status", fill=TEXT_MUTED, font=f_badge)
    draw.text((split_x + 360, th_y + 5), "Timestamp", fill=TEXT_MUTED, font=f_badge)
    draw.text((split_x + 530, th_y + 5), "Latency", fill=TEXT_MUTED, font=f_badge)

    table_items = table_items or [
        ("1", "k4rc", "AVAILABLE", "2026-11-19 12:20:15", "142ms"),
        ("2", "z99p", "AVAILABLE", "2026-11-19 12:21:04", "138ms"),
        ("3", "qv2x", "AVAILABLE", "2026-11-19 12:21:49", "151ms"),
    ]
    for idx, (num, uname, status, tstamp, lat) in enumerate(table_items):
        ry = th_y + 30 + idx * 32
        row_bg = (44, 46, 51) if idx % 2 == 0 else (40, 42, 46)
        draw.rectangle([split_x + 10, ry, w - 18, ry + 28], fill=row_bg)
        draw.text((split_x + 24, ry + 6), num, fill=TEXT_MUTED, font=f_mono)
        draw.text((split_x + 70, ry + 6), uname, fill=TEXT_CYAN, font=f_mono)
        
        # Green Badge
        draw_rounded_rect(draw, [split_x + 215, ry + 4, split_x + 315, ry + 24], radius=4, fill=(28, 70, 45))
        draw.text((split_x + 228, ry + 6), "● AVAILABLE", fill=TEXT_SUCCESS, font=f_mono_sm)
        
        draw.text((split_x + 360, ry + 6), tstamp, fill=TEXT_WHITE, font=f_mono_sm)
        draw.text((split_x + 530, ry + 6), lat, fill=TEXT_MUTED, font=f_mono_sm)

    # 6. Bottom Status Bar
    draw.rectangle([0, h - 28, w, h], fill=BG_TITLEBAR)
    draw.text((16, h - 21), i18n["status_bar"], fill=TEXT_MUTED, font=f_badge)
    ver_txt = "v12.2.0 (Production Stable)"
    draw.text((w - 180, h - 21), ver_txt, fill=TEXT_ACCENT, font=f_badge)

    if custom_cursor:
        draw_cursor(img, custom_cursor, clicking=is_clicking)

    return img

def generate_gui_screenshots():
    print("Generating Multilingual GUI Screenshots (12 Locales)...")
    for lang in GUI_I18N.keys():
        img = render_gui_base(lang=lang, is_running=True)
        img.save(ASSETS_DIR / f"gui_{lang}_main.png")
        if lang == "ko":
            img.save(ASSETS_DIR / "gui_ko_main.png")
        elif lang == "en":
            img.save(ASSETS_DIR / "gui_en_main.png")
        print(f"  ✅ Saved gui_{lang}_main.png")

    # Settings Modal
    img_modal = render_gui_base(lang="ko", is_running=False)
    dim = Image.new("RGBA", img_modal.size, (0, 0, 0, 160))
    img_modal = Image.alpha_composite(img_modal, dim)
    draw_m = ImageDraw.Draw(img_modal)
    
    mw, mh = 640, 520
    mx1 = (1200 - mw) // 2
    my1 = (780 - mh) // 2
    mx2 = mx1 + mw
    my2 = my1 + mh
    draw_rounded_rect(draw_m, [mx1, my1, mx2, my2], radius=10, fill=BG_PANEL, outline=BORDER_FOCUS, width=2)
    
    draw_m.rectangle([mx1, my1, mx2, my1 + 40], fill=BG_TITLEBAR)
    f_mbold = get_font(FONT_KR_BOLD, 15)
    f_mono = get_font(FONT_MONO, 12)
    draw_m.text((mx1 + 20, my1 + 10), "D4UC 통합 환경설정 (Settings)", fill=TEXT_WHITE, font=f_mbold)
    
    draw_m.text((mx1 + 30, my1 + 60), "[KEY] Surfshark WireGuard 개인키 (Private Key Pool)", fill=TEXT_CYAN, font=f_mbold)
    draw_rounded_rect(draw_m, [mx1 + 30, my1 + 86, mx2 - 30, my1 + 120], radius=5, fill=BG_INPUT, outline=BORDER)
    draw_m.text((mx1 + 42, my1 + 95), "******************************************** (5 Keys Active)", fill=TEXT_MUTED, font=f_mono)

    draw_m.text((mx1 + 30, my1 + 140), "[PORT] Wireproxy 로컬 포트 범위 (1:1 격리 터널)", fill=TEXT_WHITE, font=f_mbold)
    draw_rounded_rect(draw_m, [mx1 + 30, my1 + 166, mx1 + 200, my1 + 200], radius=5, fill=BG_INPUT, outline=BORDER)
    draw_m.text((mx1 + 42, my1 + 175), "1081 ~ 1130", fill=TEXT_WHITE, font=f_mono)

    img_modal.save(ASSETS_DIR / "gui_settings_modal.png")
    print(f"  ✅ Saved gui_settings_modal.png")

def generate_gui_gifs():
    print("Generating Multilingual GUI GIFs (12 Locales)...")
    for lang in GUI_I18N.keys():
        frames = []
        for i in range(10):
            if i < 3:
                cx = int(600 + (825 - 600) * (i / 2.0))
                cy = int(400 + (140 - 400) * (i / 2.0))
                clicking = False
                running = False
                speed_val = "0.0 RPS"
                avail_cnt = "0"
                tbl = []
            elif i == 3:
                cx, cy = 825, 140
                clicking = True
                running = True
                speed_val = "6.5 RPS"
                avail_cnt = "0"
                tbl = []
            elif i < 6:
                cx = int(825 + (350 - 825) * ((i - 3) / 3.0))
                cy = int(140 + (210 - 140) * ((i - 3) / 3.0))
                clicking = False
                running = True
                speed_val = "12.4 RPS"
                avail_cnt = "1"
                tbl = [("1", "k4rc", "AVAILABLE", "2026-11-19 12:20:15", "142ms")]
            else:
                cx = int(350 + (780 - 350) * ((i - 6) / 3.0))
                cy = int(210 + (360 - 210) * ((i - 6) / 3.0))
                clicking = False
                running = True
                speed_val = "14.8 RPS"
                avail_cnt = "3"
                tbl = [
                    ("1", "k4rc", "AVAILABLE", "2026-11-19 12:20:15", "142ms"),
                    ("2", "z99p", "AVAILABLE", "2026-11-19 12:21:04", "138ms"),
                    ("3", "qv2x", "AVAILABLE", "2026-11-19 12:21:49", "151ms"),
                ]
            m = {"speed": speed_val, "checked": f"{i * 120 + 40}", "avail": avail_cnt, "taken": f"{i * 119}", "hotswap": "1"}
            f = render_gui_base(lang=lang, is_running=running, metrics=m, custom_cursor=(cx, cy), is_clicking=clicking, table_items=tbl)
            frames.append(f.convert("RGB"))

        out_gif = ASSETS_DIR / f"gui_{lang}_demo.gif"
        frames[0].save(
            out_gif,
            save_all=True,
            append_images=frames[1:],
            duration=320,
            loop=0
        )
        if lang == "ko":
            frames[0].save(ASSETS_DIR / "gui_ko_demo.gif", save_all=True, append_images=frames[1:], duration=320, loop=0)
        elif lang == "en":
            frames[0].save(ASSETS_DIR / "gui_en_demo.gif", save_all=True, append_images=frames[1:], duration=320, loop=0)
        print(f"  ✅ Saved gui_{lang}_demo.gif")

def render_cli_frame(step=1):
    w, h = 960, 600
    img = Image.new("RGBA", (w, h), (18, 20, 24))
    draw = ImageDraw.Draw(img)

    f_mono = get_font(FONT_MONO, 12)
    f_mono_bold = get_font(FONT_MONO_BOLD, 12)

    draw.rectangle([0, 0, w, 32], fill=(26, 29, 34))
    draw.text((16, 7), "root@d4uc-vps-edge-01: ~/discord-checker# python src/run.py --shards 2_1", fill=TEXT_WHITE, font=f_mono_bold)
    draw.ellipse([w - 60, 11, w - 50, 21], fill=(242, 63, 67))
    draw.ellipse([w - 42, 11, w - 32, 21], fill=(250, 166, 26))
    draw.ellipse([w - 24, 11, w - 14, 21], fill=(35, 165, 90))

    banner = [
        "╔══════════════════════════════════════════════════════════════════════════════╗",
        "║  D4UC v12.2.0 - Discord Username Checker & Claim Engine                      ║",
        "║  [TLS: Chrome 131 JA3/JA4]  [Engine: BoringSSL]  [Tunnels: WireGuard 1:1]    ║",
        "╚══════════════════════════════════════════════════════════════════════════════╝",
    ]
    for idx, line in enumerate(banner):
        draw.text((36, 48 + idx * 18), line, fill=TEXT_ACCENT, font=f_mono)

    stats_y = 130
    draw.rectangle([36, stats_y, w - 36, stats_y + 80], fill=(28, 31, 38), outline=BORDER)
    draw.text((50, stats_y + 10), "TELEMETRY METRICS", fill=TEXT_MUTED, font=f_mono_bold)
    
    checked = 3200 + step * 450
    rps = 42.5 + (step % 4) * 2.1
    avail = 4 + (step // 3)
    draw.text((50, stats_y + 36), f"Checked: {checked:,}   Available: {avail}   Taken: {checked - avail:,}", fill=TEXT_WHITE, font=f_mono)
    draw.text((50, stats_y + 56), f"Speed: {rps:.1f} RPS   429 Hot-Swaps: 2   Avg Latency: 42ms   ETA: 00:08:42", fill=TEXT_CYAN, font=f_mono)

    pct = min(100, 20 + step * 6)
    bar_len = 35
    filled = int(bar_len * (pct / 100.0))
    bar_str = "█" * filled + "░" * (bar_len - filled)
    draw.text((36, 226), f"Progress [{bar_str}] {pct}% (ETA: 00:08:42)", fill=TEXT_ACCENT, font=f_mono)

    draw.text((36, 260), "── Active Worker Tunnel Pool ───────────────────────────────────────────────────", fill=BORDER, font=f_mono)
    draw.text((36, 280), "  ID   Tunnel Endpoint    Port    Status      Latency    Current Handle", fill=TEXT_MUTED, font=f_mono)
    
    workers = [
        ("W#1", "JP - Tokyo (142.1)", "1081", "OK (Active)", "132ms", "a_39", TEXT_SUCCESS),
        ("W#2", "KR - Seoul (121.8)", "1082", "EXCLUDED   ", "  -- ", "a..1 (consec dot)", TEXT_YELLOW),
        ("W#3", "SG - Sing (103.4) ", "1083", "AVAILABLE! ", "145ms", "k4rc [FOUND]", TEXT_CYAN),
        ("W#4", "US - Ashburn (64.2)", "1084", "OK (Active)", "158ms", "m99x", TEXT_SUCCESS),
        ("W#5", "DE - Frank (185.3)", "1085", "HOT-SWAPPED", " 310ms", "b20z", TEXT_YELLOW),
    ]
    for idx, (wid, ep, port, stat, lat, hndl, col) in enumerate(workers):
        wy = 304 + idx * 20
        draw.text((36, wy), f"  {wid}  {ep}   {port}    ", fill=TEXT_WHITE, font=f_mono)
        draw.text((380, wy), stat, fill=col, font=f_mono_bold)
        draw.text((500, wy), lat, fill=TEXT_MUTED, font=f_mono)
        draw.text((610, wy), hndl, fill=TEXT_WHITE if col != TEXT_CYAN else TEXT_SUCCESS, font=f_mono)

    draw.text((36, 424), "── Recent Events & Audit Feed ─────────────────────────────────────────────────", fill=BORDER, font=f_mono)
    logs = [
        ("[12:20:15]", "[FOUND]", "Username 'k4rc' is AVAILABLE! (HTTP 200 via BoringSSL)", TEXT_SUCCESS),
        ("[12:20:16]", "[ALERT]", "Dispatched Discord Webhook alert to configured channel", TEXT_ACCENT),
        ("[12:21:04]", "[FOUND]", "Username 'z99p' is AVAILABLE! (HTTP 200 via BoringSSL)", TEXT_SUCCESS),
        ("[12:21:28]", "[SWAP] ", "Worker 5 received HTTP 429 -> Atomic hot-swap executed in 282ms", TEXT_YELLOW),
        ("[12:21:49]", "[FOUND]", "Username 'qv2x' is AVAILABLE! (HTTP 200 via BoringSSL)", TEXT_SUCCESS),
    ]
    for idx, (ts, tag, msg, col) in enumerate(logs):
        ey = 448 + idx * 20
        if ey > h - 40:
            break
        draw.text((36, ey), f"{ts} ", fill=TEXT_MUTED, font=f_mono)
        draw.text((140, ey), f"{tag} ", fill=col, font=f_mono_bold)
        draw.text((220, ey), msg, fill=TEXT_WHITE if col != TEXT_SUCCESS else TEXT_SUCCESS, font=f_mono)

    return img

def generate_cli_assets():
    print("Generating CLI Assets...")
    cli_img = render_cli_frame(step=10)
    cli_img.save(ASSETS_DIR / "cli_dashboard.png")
    print(f"  Saved {ASSETS_DIR / 'cli_dashboard.png'}")

    cli_frames = []
    for s in range(1, 10):
        cf = render_cli_frame(step=s)
        cli_frames.append(cf.convert("RGB"))
    cli_frames[0].save(
        ASSETS_DIR / "cli_demo.gif",
        save_all=True,
        append_images=cli_frames[1:],
        duration=350,
        loop=0
    )
    print(f"  Saved {ASSETS_DIR / 'cli_demo.gif'}")

def generate_docker_linux_asset():
    print("Generating Docker / Linux Screenshot...")
    w, h = 1000, 580
    img = Image.new("RGBA", (w, h), (15, 17, 21))
    draw = ImageDraw.Draw(img)

    f_mono = get_font(FONT_MONO, 13)
    f_mono_bold = get_font(FONT_MONO_BOLD, 13)

    draw.rectangle([0, 0, w, 32], fill=(25, 27, 33))
    draw.text((16, 7), "root@debian-linux: ~/discord-checker# docker compose up", fill=TEXT_WHITE, font=f_mono_bold)
    draw.ellipse([w - 60, 11, w - 50, 21], fill=(242, 63, 67))
    draw.ellipse([w - 42, 11, w - 32, 21], fill=(250, 166, 26))
    draw.ellipse([w - 24, 11, w - 14, 21], fill=(35, 165, 90))

    lines = [
        ("$ docker compose -f deploy/docker-compose.yml --profile 2shard up -d", TEXT_CYAN, True),
        ("[+] Running 3/3", TEXT_MUTED, False),
        (" [+] Network deploy_d4uc-net       Created                                                   0.1s", TEXT_WHITE, False),
        (" [+] Container d4uc-shard-1       Started (healthy)                                         0.4s", TEXT_SUCCESS, False),
        (" [+] Container d4uc-shard-2       Started (healthy)                                         0.4s", TEXT_SUCCESS, False),
        ("", TEXT_WHITE, False),
        ("$ docker compose -f deploy/docker-compose.yml logs -f --tail=20", TEXT_CYAN, True),
        ("d4uc-shard-1  | [2026-11-19 12:20:00] [INFO] D4UC v12.2.0 starting inside Docker container (ARM64/AMD64)", TEXT_MUTED, False),
        ("d4uc-shard-1  | [2026-11-19 12:20:01] [INFO] Shard 2_1 configured: range a000..mz99 (Exhaustive search)", TEXT_WHITE, False),
        ("d4uc-shard-1  | [2026-11-19 12:20:02] [GATE] Pre-flight IP Verification: 5 WireGuard tunnels active", TEXT_CYAN, False),
        ("d4uc-shard-2  | [2026-11-19 12:20:00] [INFO] D4UC v12.2.0 starting inside Docker container (ARM64/AMD64)", TEXT_MUTED, False),
        ("d4uc-shard-2  | [2026-11-19 12:20:01] [INFO] Shard 2_2 configured: range n000..zzzz (Exhaustive search)", TEXT_WHITE, False),
        ("d4uc-shard-2  | [2026-11-19 12:20:02] [GATE] Pre-flight IP Verification: 5 WireGuard tunnels active", TEXT_CYAN, False),
        ("d4uc-shard-1  | [2026-11-19 12:20:15] [HIT]  >> AVAILABLE: 'k4rc' (Latency: 142ms) -> Saved to SQLite WAL", TEXT_SUCCESS, True),
        ("d4uc-shard-2  | [2026-11-19 12:20:45] [INFO] Shard 2_2 scanned 600 handles (Speed: 14.2 RPS)", TEXT_MUTED, False),
        ("d4uc-shard-2  | [2026-11-19 12:21:04] [HIT]  >> AVAILABLE: 'z99p' (Latency: 138ms) -> Saved to SQLite WAL", TEXT_SUCCESS, True),
        ("d4uc-shard-1  | [2026-11-19 12:21:28] [WARN] Worker 5 hit 429 rate limit. Initiating 0.3s atomic hot-swap...", TEXT_YELLOW, False),
        ("d4uc-shard-1  | [2026-11-19 12:21:29] [INFO] Atomic hot-swap complete: Switched to JP-Osaka-1. Zero stall.", TEXT_CYAN, False),
        ("d4uc-shard-1  | [2026-11-19 12:21:49] [HIT]  >> AVAILABLE: 'qv2x' (Latency: 151ms) -> Saved to SQLite WAL", TEXT_SUCCESS, True),
    ]

    for idx, (text, col, is_bold) in enumerate(lines):
        ly = 48 + idx * 25
        font_to_use = f_mono_bold if is_bold else f_mono
        draw.text((24, ly), text, fill=col, font=font_to_use)

    img.save(ASSETS_DIR / "docker_linux_capture.png")
    print(f"  Saved {ASSETS_DIR / 'docker_linux_capture.png'}")

def main():
    generate_gui_screenshots()
    generate_gui_gifs()
    generate_cli_assets()
    generate_docker_linux_asset()
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import generate_mobile_assets
        generate_mobile_assets.generate_all_mobile_assets()
    except Exception as e:
        print(f"Mobile assets generator hook: {e}")
    print("\n✅ All visual assets successfully generated in docs/assets/!")

if __name__ == "__main__":
    main()
