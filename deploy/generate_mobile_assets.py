# deploy/generate_mobile_assets.py
"""
High-Fidelity 1:1 Multilingual Mobile Web GUI & PWA Visual Asset Generator for D4UC v12.2.0.
Generates pixel-perfect smartphone mockup screenshots and interactive animated touch GIFs
for ALL 12 supported languages:
- ko (Korean)
- en (English)
- ja (Japanese)
- zh (Simplified Chinese)
- es (Spanish)
- fr (French)
- de (German)
- ru (Russian)
- pt (Portuguese)
- ar (Arabic)
- hi (Hindi)
- id (Indonesian)
"""
import math
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "docs" / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# System Fonts
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

def get_locale_fonts(lang: str):
    if lang == "ko":
        return get_font(FONT_KR_REG, 11), get_font(FONT_KR_BOLD, 14), get_font(FONT_KR_BOLD, 18), get_font(FONT_KR_REG, 10)
    elif lang == "ja":
        return get_font(FONT_JA_REG, 11), get_font(FONT_JA_REG, 13), get_font(FONT_JA_REG, 17), get_font(FONT_JA_REG, 10)
    elif lang == "zh":
        return get_font(FONT_ZH_REG, 11), get_font(FONT_ZH_REG, 14), get_font(FONT_ZH_REG, 17), get_font(FONT_ZH_REG, 10)
    elif lang == "ar":
        f_b = get_font(FONT_AR_BOLD, 13) if Path(FONT_AR_BOLD).exists() else get_font(FONT_AR_REG, 13)
        return get_font(FONT_AR_REG, 11), f_b, get_font(FONT_AR_REG, 17), get_font(FONT_AR_REG, 10)
    elif lang == "hi":
        f_b = get_font(FONT_HI_BOLD, 13) if Path(FONT_HI_BOLD).exists() else get_font(FONT_HI_REG, 13)
        return get_font(FONT_HI_REG, 11), f_b, get_font(FONT_HI_REG, 16), get_font(FONT_HI_REG, 9)
    else:  # en, es, fr, de, ru, pt, id
        return get_font(FONT_UI_REG, 11), get_font(FONT_UI_BOLD, 13), get_font(FONT_UI_BOLD, 18), get_font(FONT_UI_REG, 10)

# Colors
BG_PHONE = (18, 19, 22)
BG_APP = (30, 31, 34)       # #1e1f22
BG_PANEL = (43, 45, 49)     # #2b2d31
BG_CARD = (49, 51, 56)      # #313338
BG_INPUT = (35, 36, 40)     # #232428
BORDER = (60, 63, 69)       # #3c3f45
TEXT_WHITE = (242, 243, 245)
TEXT_MUTED = (148, 155, 164)
TEXT_SUCCESS = (35, 165, 90)   # #23a55a
TEXT_DANGER = (242, 63, 67)    # #f23f43
TEXT_ACCENT = (88, 101, 242)   # #5865F2
TEXT_CYAN = (0, 196, 204)
TEXT_YELLOW = (250, 166, 26)

MOBILE_I18N = {
    "ko": {
        "title": "D4UC 모바일 웹",
        "subtitle": "Discord Checker v12.2.0 (PWA)",
        "running": "실행 중 (15w)",
        "idle": "대기 중",
        "rps": "속도 (RPS)",
        "avail": "가용 발견",
        "checked": "총 검사",
        "taken": "선점 (TAKEN)",
        "swaps": "429 노드교체",
        "latency": "평균 레이턴시",
        "graph_title": "⚡ 실시간 탐색 속도 추이 (RPS)",
        "graph_peak": "최고: 49.8 req/s",
        "tabs": ["결과 목록", "탐색 조건", "프록시", "로그"],
        "results_title": "🎉 발견된 희귀 닉네임",
        "copy": "복사",
        "found": "발견",
        "btn_stop": "■  탐색 중지",
        "btn_start": "▶  탐색 시작",
        "btn_restart": "🔄 재시작",
        "toast": "📋 '{uname}' 복사 완료!"
    },
    "en": {
        "title": "D4UC Mobile Web",
        "subtitle": "Discord Checker v12.2.0 (PWA)",
        "running": "Running (15w)",
        "idle": "Idle",
        "rps": "Speed (RPS)",
        "avail": "Available",
        "checked": "Checked",
        "taken": "Taken",
        "swaps": "429 Swaps",
        "latency": "Avg Latency",
        "graph_title": "⚡ Real-Time Speed Trend (RPS)",
        "graph_peak": "Peak: 49.8 req/s",
        "tabs": ["Results", "Target", "Proxy", "Logs"],
        "results_title": "🎉 Rare Usernames Discovered",
        "copy": "Copy",
        "found": "Found",
        "btn_stop": "■  Stop Scan",
        "btn_start": "▶  Start Scan",
        "btn_restart": "🔄 Restart",
        "toast": "📋 '{uname}' Copied!"
    },
    "ja": {
        "title": "D4UC モバイル Web",
        "subtitle": "Discord Checker v12.2.0 (PWA)",
        "running": "実行中 (15w)",
        "idle": "待機中",
        "rps": "速度 (RPS)",
        "avail": "利用可能",
        "checked": "総検査数",
        "taken": "取得済",
        "swaps": "429 切替",
        "latency": "平均遅延",
        "graph_title": "⚡ リアルタイム探索速度 (RPS)",
        "graph_peak": "最高: 49.8 req/s",
        "tabs": ["結果一覧", "探索条件", "プロキシ", "ログ"],
        "results_title": "🎉 発見されたレアニックネーム",
        "copy": "コピー",
        "found": "発見",
        "btn_stop": "■  探索停止",
        "btn_start": "▶  探索開始",
        "btn_restart": "🔄 再起動",
        "toast": "📋 '{uname}' コピー完了!"
    },
    "zh": {
        "title": "D4UC 移动端网页",
        "subtitle": "Discord Checker v12.2.0 (PWA)",
        "running": "运行中 (15w)",
        "idle": "空闲中",
        "rps": "速度 (RPS)",
        "avail": "发现可用",
        "checked": "总检查数",
        "taken": "已占用",
        "swaps": "429 切换",
        "latency": "平均延迟",
        "graph_title": "⚡ 实时扫描速度趋势 (RPS)",
        "graph_peak": "峰值: 49.8 req/s",
        "tabs": ["结果列表", "扫描条件", "代理设置", "日志"],
        "results_title": "🎉 发现的稀有用户名",
        "copy": "复制",
        "found": "发现",
        "btn_stop": "■  停止扫描",
        "btn_start": "▶  开始扫描",
        "btn_restart": "🔄 重启",
        "toast": "📋 '{uname}' 复制成功!"
    },
    "es": {
        "title": "D4UC Web Móvil",
        "subtitle": "Discord Checker v12.2.0 (PWA)",
        "running": "Ejecutando (15w)",
        "idle": "En espera",
        "rps": "Velocidad",
        "avail": "Disponible",
        "checked": "Verificado",
        "taken": "Ocupado",
        "swaps": "429 Cambios",
        "latency": "Latencia",
        "graph_title": "⚡ Velocidad en tiempo real (RPS)",
        "graph_peak": "Máx: 49.8 req/s",
        "tabs": ["Resultados", "Objetivo", "Proxy", "Logs"],
        "results_title": "🎉 Nombres raros descubiertos",
        "copy": "Copiar",
        "found": "Hallado",
        "btn_stop": "■  Detener",
        "btn_start": "▶  Iniciar",
        "btn_restart": "🔄 Reiniciar",
        "toast": "📋 ¡'{uname}' copiado!"
    },
    "fr": {
        "title": "D4UC Web Mobile",
        "subtitle": "Discord Checker v12.2.0 (PWA)",
        "running": "En cours (15w)",
        "idle": "En attente",
        "rps": "Vitesse",
        "avail": "Disponible",
        "checked": "Vérifiés",
        "taken": "Occupé",
        "swaps": "429 Échanges",
        "latency": "Latence moy.",
        "graph_title": "⚡ Vitesse en temps réel (RPS)",
        "graph_peak": "Max: 49.8 req/s",
        "tabs": ["Résultats", "Cibles", "Proxy", "Logs"],
        "results_title": "🎉 Noms rares découverts",
        "copy": "Copier",
        "found": "Trouvé",
        "btn_stop": "■  Arrêter",
        "btn_start": "▶  Démarrer",
        "btn_restart": "🔄 Redémarrer",
        "toast": "📋 '{uname}' copié !"
    },
    "de": {
        "title": "D4UC Mobile Web",
        "subtitle": "Discord Checker v12.2.0 (PWA)",
        "running": "Aktiv (15w)",
        "idle": "Bereit",
        "rps": "Geschw.",
        "avail": "Verfügbar",
        "checked": "Geprüft",
        "taken": "Belegt",
        "swaps": "429 Tausch",
        "latency": "Ø Latenz",
        "graph_title": "⚡ Echtzeit-Geschwindigkeit (RPS)",
        "graph_peak": "Spitze: 49.8 req/s",
        "tabs": ["Ergebnisse", "Ziel", "Proxy", "Logs"],
        "results_title": "🎉 Seltene Namen entdeckt",
        "copy": "Kopie",
        "found": "Gefunden",
        "btn_stop": "■  Stoppen",
        "btn_start": "▶  Starten",
        "btn_restart": "🔄 Neustart",
        "toast": "📋 '{uname}' kopiert!"
    },
    "ru": {
        "title": "D4UC Мобильный Web",
        "subtitle": "Discord Checker v12.2.0 (PWA)",
        "running": "Работает (15w)",
        "idle": "Ожидание",
        "rps": "Скорость",
        "avail": "Доступно",
        "checked": "Проверено",
        "taken": "Занято",
        "swaps": "429 Замен",
        "latency": "Задержка",
        "graph_title": "⚡ Скорость в реальном времени (RPS)",
        "graph_peak": "Пик: 49.8 req/s",
        "tabs": ["Результаты", "Условия", "Прокси", "Логи"],
        "results_title": "🎉 Найденные редкие никнеймы",
        "copy": "Копия",
        "found": "Найдено",
        "btn_stop": "■  Остановить",
        "btn_start": "▶  Запустить",
        "btn_restart": "🔄 Перезапуск",
        "toast": "📋 '{uname}' скопирован!"
    },
    "pt": {
        "title": "D4UC Web Móvel",
        "subtitle": "Discord Checker v12.2.0 (PWA)",
        "running": "Executando (15w)",
        "idle": "Ocioso",
        "rps": "Velocidade",
        "avail": "Disponível",
        "checked": "Verificado",
        "taken": "Ocupado",
        "swaps": "429 Trocas",
        "latency": "Latência",
        "graph_title": "⚡ Velocidade em tempo real (RPS)",
        "graph_peak": "Pico: 49.8 req/s",
        "tabs": ["Resultados", "Alvo", "Proxy", "Logs"],
        "results_title": "🎉 Nomes raros descobertos",
        "copy": "Copiar",
        "found": "Achado",
        "btn_stop": "■  Parar",
        "btn_start": "▶  Iniciar",
        "btn_restart": "🔄 Reiniciar",
        "toast": "📋 '{uname}' copiado!"
    },
    "ar": {
        "title": "D4UC ويب الجوال",
        "subtitle": "Discord Checker v12.2.0 (PWA)",
        "running": "قيد التشغيل (15w)",
        "idle": "في الانتظار",
        "rps": "السرعة",
        "avail": "المتاحة",
        "checked": "المفحوص",
        "taken": "محجوز",
        "swaps": "تبديل 429",
        "latency": "التأخير",
        "graph_title": "⚡ اتجاه السرعة في الوقت الفعلي (RPS)",
        "graph_peak": "الذروة: 49.8 req/s",
        "tabs": ["النتائج", "الأهداف", "البروكسي", "السجلات"],
        "results_title": "🎉 الأسماء النادرة المكتشفة",
        "copy": "نسخ",
        "found": "تم العثور",
        "btn_stop": "■  إيقاف",
        "btn_start": "▶  بدء",
        "btn_restart": "🔄 إعادة تشغيل",
        "toast": "📋 تم نسخ '{uname}'!"
    },
    "hi": {
        "title": "D4UC मोबाइल वेब",
        "subtitle": "Discord Checker v12.2.0 (PWA)",
        "running": "सक्रिय (15w)",
        "idle": "निष्क्रिय",
        "rps": "गति (RPS)",
        "avail": "उपलब्ध",
        "checked": "जाँचे गए",
        "taken": "लिया गया",
        "swaps": "429 स्वैप",
        "latency": "विलंबता",
        "graph_title": "⚡ वास्तविक समय गति प्रवृत्ति (RPS)",
        "graph_peak": "शीर्ष: 49.8 req/s",
        "tabs": ["परिणाम", "लक्ष्य", "प्रॉक्सी", "लॉग्स"],
        "results_title": "🎉 दुर्लभ नाम खोजे गए",
        "copy": "कॉपी",
        "found": "प्राप्त",
        "btn_stop": "■  रोकें",
        "btn_start": "▶  आरंभ करें",
        "btn_restart": "🔄 पुनः आरंभ",
        "toast": "📋 '{uname}' कॉपी हुआ!"
    },
    "id": {
        "title": "D4UC Web Seluler",
        "subtitle": "Discord Checker v12.2.0 (PWA)",
        "running": "Berjalan (15w)",
        "idle": "Siaga",
        "rps": "Kecepatan",
        "avail": "Tersedia",
        "checked": "Diperiksa",
        "taken": "Digunakan",
        "swaps": "429 Ganti",
        "latency": "Latensi",
        "graph_title": "⚡ Tren Kecepatan Real-Time (RPS)",
        "graph_peak": "Puncak: 49.8 req/s",
        "tabs": ["Hasil", "Target", "Proksi", "Log"],
        "results_title": "🎉 Username Langka Ditemukan",
        "copy": "Salin",
        "found": "Ditemukan",
        "btn_stop": "■  Hentikan",
        "btn_start": "▶  Mulai",
        "btn_restart": "🔄 Mulai Ulang",
        "toast": "📋 '{uname}' Disalin!"
    }
}

def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def draw_touch_ripple(img, pos, radius=24, alpha=180):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    x, y = pos
    d.ellipse([x - radius, y - radius, x + radius, y + radius], outline=(88, 101, 242, alpha), width=3)
    d.ellipse([x - radius // 2, y - radius // 2, x + radius // 2, y + radius // 2], fill=(255, 255, 255, min(220, alpha + 40)))
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay), (0, 0))

def render_mobile_frame(lang: str = "ko", step: int = 0, touch_pos=None, is_touching=False, toast_text=None):
    i18n = MOBILE_I18N.get(lang, MOBILE_I18N["en"])
    w, h = 440, 880
    img = Image.new("RGBA", (w, h), BG_PHONE)
    draw = ImageDraw.Draw(img)

    f_sub, f_bold, f_stat_val, f_stat_lbl = get_locale_fonts(lang)
    f_mono = get_font(FONT_MONO, 11)
    f_mono_bold = get_font(FONT_MONO_BOLD, 12)

    # 1. Phone Bezel & Outer Shell
    draw_rounded_rect(draw, [6, 6, w - 6, h - 6], radius=38, fill=BG_APP, outline=(70, 74, 82), width=3)

    # 2. Dynamic Island / Notch
    draw_rounded_rect(draw, [w // 2 - 55, 14, w // 2 + 55, 38], radius=12, fill=(0, 0, 0), outline=(30, 30, 30))
    draw.ellipse([w // 2 + 25, 22, w // 2 + 37, 34], fill=(15, 20, 30))

    # Top Status Bar
    draw.text((36, 19), "13:30", fill=TEXT_WHITE, font=f_bold)
    draw.text((w - 74, 19), "5G  88%", fill=TEXT_WHITE, font=f_sub)

    # 3. App Header Bar
    draw.rectangle([6, 48, w - 6, 96], fill=BG_PANEL)
    draw.line([6, 96, w - 6, 96], fill=BORDER, width=1)

    # App Logo
    draw_rounded_rect(draw, [20, 56, 52, 88], radius=8, fill=TEXT_ACCENT)
    draw.text((28, 62), "⚡", fill=TEXT_WHITE, font=f_bold)

    draw.text((60, 57), i18n["title"], fill=TEXT_WHITE, font=f_bold)
    draw.text((60, 75), i18n["subtitle"], fill=TEXT_MUTED, font=f_sub)

    # Status Pill Badge
    is_running = (step >= 2)
    pill_text = i18n["running"] if is_running else i18n["idle"]
    dot_color = TEXT_SUCCESS if is_running else TEXT_MUTED
    draw_rounded_rect(draw, [w - 116, 60, w - 20, 84], radius=12, fill=BG_INPUT, outline=BORDER)
    draw.ellipse([w - 106, 68, w - 98, 76], fill=dot_color)
    draw.text((w - 92, 65), pill_text, fill=TEXT_WHITE, font=f_sub)

    # 4. Telemetry 2x3 Grid
    base_checked = 12000 + step * 380
    rps_val = 45.2 + math.sin(step * 0.8) * 4.5 if is_running else 0.0
    avail_count = 14 + (step // 3)

    metrics = [
        (i18n["rps"], f"{rps_val:.1f}", TEXT_CYAN),
        (i18n["avail"], f"{avail_count}", TEXT_SUCCESS),
        (i18n["checked"], f"{base_checked:,}", TEXT_WHITE),
        (i18n["taken"], f"{base_checked - avail_count:,}", TEXT_WHITE),
        (i18n["swaps"], f"{3 + (step // 5)}", TEXT_YELLOW),
        (i18n["latency"], f"{38 + (step % 5)}ms", TEXT_WHITE),
    ]

    grid_y = 108
    cw = (w - 40 - 8) // 3
    ch = 50
    for idx, (lbl, val, col) in enumerate(metrics):
        r = idx // 3
        c = idx % 3
        cx = 20 + c * (cw + 4)
        cy = grid_y + r * (ch + 6)
        draw_rounded_rect(draw, [cx, cy, cx + cw, cy + ch], radius=8, fill=BG_CARD, outline=BORDER)
        draw.text((cx + 8, cy + 5), lbl, fill=TEXT_MUTED, font=f_stat_lbl)
        draw.text((cx + 8, cy + 22), val, fill=col, font=f_stat_val)

    # 5. Real-Time Canvas Graph Card
    graph_y = 226
    draw_rounded_rect(draw, [20, graph_y, w - 20, graph_y + 70], radius=8, fill=BG_CARD, outline=BORDER)
    draw.text((30, graph_y + 6), i18n["graph_title"], fill=TEXT_MUTED, font=f_sub)
    draw.text((w - 110, graph_y + 6), i18n["graph_peak"], fill=TEXT_CYAN, font=f_sub)

    # Canvas inner
    draw_rounded_rect(draw, [28, graph_y + 24, w - 28, graph_y + 62], radius=4, fill=BG_INPUT)
    pts = []
    gw = w - 56
    for i in range(25):
        px = 28 + i * (gw // 24)
        v = math.sin((i + step * 2) * 0.45) * 12 + 18
        py = (graph_y + 62) - v
        pts.append((px, py))
    if is_running and len(pts) > 1:
        draw.line(pts, fill=TEXT_ACCENT, width=2)

    # 6. Navigation Tabs
    tab_y = 308
    draw_rounded_rect(draw, [20, tab_y, w - 20, tab_y + 36], radius=8, fill=BG_PANEL, outline=BORDER)
    tabs = i18n["tabs"]
    tw = (w - 48) // 4
    for i, t in enumerate(tabs):
        tx = 24 + i * tw
        if i == 0:
            draw_rounded_rect(draw, [tx, tab_y + 3, tx + tw - 2, tab_y + 33], radius=6, fill=TEXT_ACCENT)
            draw.text((tx + 8, tab_y + 11), t, fill=TEXT_WHITE, font=f_bold)
        else:
            draw.text((tx + 8, tab_y + 11), t, fill=TEXT_MUTED, font=f_sub)

    # 7. Discovered Usernames Results List
    res_y = 356
    draw_rounded_rect(draw, [20, res_y, w - 20, h - 90], radius=12, fill=BG_PANEL, outline=BORDER)
    draw.text((32, res_y + 12), i18n["results_title"], fill=TEXT_WHITE, font=f_bold)
    badge_x = 32 + int(len(i18n["results_title"]) * 8.5) + 10
    draw_rounded_rect(draw, [badge_x, res_y + 12, badge_x + 30, res_y + 30], radius=9, fill=TEXT_SUCCESS)
    draw.text((badge_x + 8, res_y + 14), str(avail_count), fill=TEXT_WHITE, font=f_sub)

    # Action Buttons: TXT / CSV / JSON
    draw_rounded_rect(draw, [w - 146, res_y + 10, w - 108, res_y + 32], radius=4, fill=BG_INPUT, outline=BORDER)
    draw.text((w - 138, res_y + 14), "TXT", fill=TEXT_WHITE, font=f_sub)
    draw_rounded_rect(draw, [w - 102, res_y + 10, w - 64, res_y + 32], radius=4, fill=BG_INPUT, outline=BORDER)
    draw.text((w - 94, res_y + 14), "CSV", fill=TEXT_WHITE, font=f_sub)
    draw_rounded_rect(draw, [w - 58, res_y + 10, w - 28, res_y + 32], radius=4, fill=BG_INPUT, outline=BORDER)
    draw.text((w - 52, res_y + 14), "JSON", fill=TEXT_WHITE, font=f_sub)

    # Usernames items
    items = [
        ("v.vip", "13:20:15", "42.1ms", "mask(?.vip)"),
        ("kr.99", "13:20:38", "35.8ms", "mask(kr??)"),
        ("a.vip", "13:21:02", "39.4ms", "mask(?.vip)"),
        ("z9_q",  "13:21:29", "41.0ms", "hybrid"),
        ("neo.9", "13:22:10", "36.5ms", "mask(neo?)"),
        ("777x",  "13:22:45", "37.2ms", "pattern"),
    ]

    item_start_y = res_y + 42
    for idx, (uname, ts, lat, mode_str) in enumerate(items[:5]):
        iy = item_start_y + idx * 64
        if iy > h - 160:
            break
        draw_rounded_rect(draw, [30, iy, w - 30, iy + 56], radius=8, fill=BG_CARD, outline=BORDER)
        draw.rectangle([30, iy, 34, iy + 56], fill=TEXT_SUCCESS)
        draw.text((44, iy + 8), uname, fill=TEXT_SUCCESS, font=f_bold)
        draw.text((44, iy + 32), f"{i18n['found']}: {ts} | {lat} | {mode_str}", fill=TEXT_MUTED, font=f_mono)

        # 1-Tap Copy Button
        draw_rounded_rect(draw, [w - 85, iy + 14, w - 40, iy + 42], radius=6, fill=TEXT_ACCENT)
        draw.text((w - 74, iy + 21), i18n["copy"], fill=TEXT_WHITE, font=f_sub)

    # 8. Bottom Fixed Action Controls
    bot_y = h - 84
    draw.rectangle([6, bot_y, w - 6, h - 6], fill=BG_PANEL)
    draw.line([6, bot_y, w - 6, bot_y], fill=BORDER, width=1)

    # Big START/STOP Touch Button
    btn_col = TEXT_DANGER if is_running else TEXT_SUCCESS
    btn_lbl = i18n["btn_stop"] if is_running else i18n["btn_start"]
    draw_rounded_rect(draw, [24, bot_y + 10, w - 120, bot_y + 58], radius=10, fill=btn_col)
    draw.text((w // 2 - 80, bot_y + 24), btn_lbl, fill=TEXT_WHITE, font=f_bold)

    # Restart Button
    draw_rounded_rect(draw, [w - 110, bot_y + 10, w - 24, bot_y + 58], radius=10, fill=BG_CARD, outline=BORDER)
    draw.text((w - 95, bot_y + 24), i18n["btn_restart"], fill=TEXT_WHITE, font=f_sub)

    # Home Bar
    draw_rounded_rect(draw, [w // 2 - 60, h - 14, w // 2 + 60, h - 9], radius=3, fill=(120, 120, 120))

    # Optional Toast Message
    if toast_text:
        tw = 210
        draw_rounded_rect(draw, [w // 2 - tw // 2, 64, w // 2 + tw // 2, 98], radius=17, fill=TEXT_SUCCESS)
        draw.text((w // 2 - tw // 2 + 16, 74), toast_text, fill=TEXT_WHITE, font=f_bold)

    # Touch Ripple
    if touch_pos:
        draw_touch_ripple(img, touch_pos, radius=26 if is_touching else 16, alpha=220 if is_touching else 140)

    return img

def generate_mobile_assets_for_lang(lang: str):
    i18n = MOBILE_I18N.get(lang, MOBILE_I18N["en"])
    w, h = 440, 880

    # 1. Main Static Screenshot
    main_img = render_mobile_frame(lang=lang, step=8)
    out_png = ASSETS_DIR / f"mobile_web_main_{lang}.png"
    main_img.save(out_png)

    # Also save default mobile_web_main.png if lang is ko or en
    if lang == "ko":
        main_img.save(ASSETS_DIR / "mobile_web_main.png")

    # 2. Interactive Animated Demo GIF (10 frames for fast & smooth render)
    frames = []
    toast_msg = i18n["toast"].format(uname="v.vip")
    for step in range(10):
        touch_pos = None
        is_touch = False
        toast = None

        if step == 2:
            touch_pos = (w // 2 - 50, h - 55)  # Tapping Start
            is_touch = True
        elif step == 6:
            touch_pos = (w - 65, 416)          # Tapping Copy button
            is_touch = True
        elif step in (7, 8):
            toast = toast_msg

        f = render_mobile_frame(lang=lang, step=step, touch_pos=touch_pos, is_touching=is_touch, toast_text=toast)
        frames.append(f.convert("RGB"))

    out_gif = ASSETS_DIR / f"mobile_web_demo_{lang}.gif"
    frames[0].save(
        out_gif,
        save_all=True,
        append_images=frames[1:],
        duration=320,
        loop=0
    )
    if lang == "ko":
        frames[0].save(
            ASSETS_DIR / "mobile_web_demo.gif",
            save_all=True,
            append_images=frames[1:],
            duration=320,
            loop=0
        )
    print(f"  ✅ [{lang.upper()}] Generated {out_png.name} & {out_gif.name}")

def generate_all_mobile_assets():
    print("=================================================================")
    print("📱 Generating 1:1 Multilingual Mobile Web GUI Assets (12 Locales)")
    print("=================================================================")
    for lang in MOBILE_I18N.keys():
        generate_mobile_assets_for_lang(lang)
    print("✅ All 12 localized Mobile Web assets successfully generated.")

if __name__ == "__main__":
    generate_all_mobile_assets()
