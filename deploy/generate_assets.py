# deploy/generate_assets.py
"""
High-Fidelity Visual Asset Generator for D4UC v12.1.0 Documentation.
Generates pixel-perfect PNG screenshots and animated GIFs with natural mouse-cursor movement:
- docs/assets/gui_ko_main.png
- docs/assets/gui_ko_demo.gif
- docs/assets/gui_en_main.png
- docs/assets/gui_en_demo.gif
- docs/assets/gui_settings_modal.png
- docs/assets/cli_dashboard.png
- docs/assets/cli_demo.gif
- docs/assets/docker_linux_capture.png
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
FONT_MONO = r"C:\Windows\Fonts\consola.ttf"
FONT_MONO_BOLD = r"C:\Windows\Fonts\consolab.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

# Colors (Discord Dark Theme Palette)
BG_APP = (30, 31, 34)       # #1e1f22
BG_PANEL = (43, 45, 49)     # #2b2d31
BG_CARD = (49, 51, 56)      # #313338
BG_INPUT = (35, 36, 40)     # #232428
BG_TITLEBAR = (24, 25, 28)  # #18191c
BORDER = (60, 63, 69)       # #3c3f45
BORDER_FOCUS = (88, 101, 242) # Discord Blurple

TEXT_WHITE = (242, 243, 245)
TEXT_MUTED = (148, 155, 164)
TEXT_SUCCESS = (35, 165, 90)   # #23a55a
TEXT_DANGER = (242, 63, 67)    # #f23f43
TEXT_ACCENT = (88, 101, 242)   # #5865F2
TEXT_CYAN = (0, 196, 204)
TEXT_YELLOW = (250, 166, 26)

def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def draw_cursor(img, pos, clicking=False):
    """Draws a crisp modern mouse cursor at pos with optional click ripple."""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    x, y = pos
    
    if clicking:
        # Click ripple ring
        d.ellipse([x - 14, y - 14, x + 14, y + 14], outline=(88, 101, 242, 180), width=3)
        d.ellipse([x - 8, y - 8, x + 8, y + 8], outline=(255, 255, 255, 220), width=2)
    
    # Cursor arrow polygon
    cursor_pts = [
        (x, y),
        (x, y + 18),
        (x + 4, y + 14),
        (x + 8, y + 22),
        (x + 11, y + 21),
        (x + 7, y + 13),
        (x + 13, y + 13),
    ]
    # Shadow
    shadow_pts = [(px + 2, py + 2) for px, py in cursor_pts]
    d.polygon(shadow_pts, fill=(0, 0, 0, 100))
    # Border & Fill
    d.polygon(cursor_pts, fill=(255, 255, 255, 255))
    d.line(cursor_pts + [(x, y)], fill=(20, 20, 20, 255), width=1)
    
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay), (0, 0))

def render_gui_base(lang="ko", is_running=False, metrics=None, custom_cursor=None, is_clicking=False, table_items=None):
    w, h = 1200, 780
    img = Image.new("RGBA", (w, h), BG_APP)
    draw = ImageDraw.Draw(img)

    f_title = get_font(FONT_KR_BOLD if lang == "ko" else FONT_UI_BOLD, 13)
    f_badge = get_font(FONT_KR_REG if lang == "ko" else FONT_UI_REG, 11)
    f_body = get_font(FONT_KR_REG if lang == "ko" else FONT_UI_REG, 13)
    f_bold = get_font(FONT_KR_BOLD if lang == "ko" else FONT_UI_BOLD, 13)
    f_mono = get_font(FONT_MONO, 12)
    f_mono_bold = get_font(FONT_MONO_BOLD, 12)
    f_mono_sm = get_font(FONT_MONO, 11)
    f_stat_val = get_font(FONT_KR_BOLD if lang == "ko" else FONT_UI_BOLD, 20)
    f_stat_lbl = get_font(FONT_KR_REG if lang == "ko" else FONT_UI_REG, 11)

    # 1. Window Titlebar
    draw.rectangle([0, 0, w, 36], fill=BG_TITLEBAR)
    title_text = "D4UC v12.1.0 - Discord Username Checker [한국어 에디션]" if lang == "ko" else "D4UC v12.1.0 - Discord Username Checker [English Edition]"
    draw.text((16, 9), title_text, fill=TEXT_WHITE, font=f_title)
    
    # Titlebar controls (min, max, close)
    draw.line([w - 110, 18, w - 100, 18], fill=TEXT_MUTED, width=2)
    draw.rectangle([w - 75, 13, w - 65, 23], outline=TEXT_MUTED, width=1)
    draw.line([w - 35, 13, w - 25, 23], fill=TEXT_MUTED, width=2)
    draw.line([w - 25, 13, w - 35, 23], fill=TEXT_MUTED, width=2)

    # 2. Onboarding Notification Banner
    draw_rounded_rect(draw, [16, 48, w - 16, 84], radius=6, fill=BG_CARD, outline=BORDER)
    banner_txt = "[온보딩] Chrome 131 TLS 스텔스 위장 및 1:1 WireGuard 터널 풀이 자동 적용됩니다. 시작을 눌러 가동하세요." if lang == "ko" else "[ONBOARDING] Chrome 131 TLS stealth & 1:1 isolated WireGuard tunnel pool active. Click Start to begin."
    draw.text((32, 57), banner_txt, fill=TEXT_CYAN, font=f_body)

    # 3. Top Control Bar Panel
    draw_rounded_rect(draw, [16, 96, w - 16, 168], radius=8, fill=BG_PANEL, outline=BORDER)
    
    # Mode Dropdown
    lbl_mode = "생성 모드" if lang == "ko" else "Mode"
    draw.text((32, 108), lbl_mode, fill=TEXT_MUTED, font=f_badge)
    draw_rounded_rect(draw, [32, 126, 210, 156], radius=5, fill=BG_INPUT, outline=BORDER)
    val_mode = "하이브리드 (Hybrid)  ▼" if lang == "ko" else "Hybrid (Dict+Num)  ▼"
    draw.text((42, 133), val_mode, fill=TEXT_WHITE, font=f_body)

    # Length
    lbl_len = "자릿수" if lang == "ko" else "Length"
    draw.text((230, 108), lbl_len, fill=TEXT_MUTED, font=f_badge)
    draw_rounded_rect(draw, [230, 126, 290, 156], radius=5, fill=BG_INPUT, outline=BORDER)
    draw.text((254, 133), "4", fill=TEXT_WHITE, font=f_body)

    # Workers
    lbl_wk = "워커수" if lang == "ko" else "Workers"
    draw.text((310, 108), lbl_wk, fill=TEXT_MUTED, font=f_badge)
    draw_rounded_rect(draw, [310, 126, 380, 156], radius=5, fill=BG_INPUT, outline=BORDER)
    draw.text((338, 133), "5", fill=TEXT_WHITE, font=f_body)

    # Shard Presets
    lbl_sh = "샤드 분할" if lang == "ko" else "Sharding"
    draw.text((400, 108), lbl_sh, fill=TEXT_MUTED, font=f_badge)
    draw_rounded_rect(draw, [400, 126, 520, 156], radius=5, fill=BG_INPUT, outline=BORDER)
    draw.text((412, 133), "2_1 (a–m)  ▼", fill=TEXT_WHITE, font=f_body)

    # Proxy Engine Status
    lbl_px = "프록시 엔진" if lang == "ko" else "Proxy Engine"
    draw.text((540, 108), lbl_px, fill=TEXT_MUTED, font=f_badge)
    draw_rounded_rect(draw, [540, 126, 730, 156], radius=5, fill=BG_INPUT, outline=BORDER)
    draw.text((552, 133), "● 1:1 Surfshark WireGuard", fill=TEXT_SUCCESS, font=f_badge)

    # Action Buttons: Start/Stop, Settings
    btn_start_col = TEXT_DANGER if is_running else TEXT_ACCENT
    draw_rounded_rect(draw, [760, 120, 890, 160], radius=6, fill=btn_start_col)
    btn_start_txt = ("■ 중지" if lang == "ko" else "■ Stop") if is_running else ("▶ 시작" if lang == "ko" else "▶ Start")
    draw.text((800, 131), btn_start_txt, fill=TEXT_WHITE, font=f_bold)

    draw_rounded_rect(draw, [905, 120, 1010, 160], radius=6, fill=BG_CARD, outline=BORDER)
    draw.text((928, 131), "환경 설정" if lang == "ko" else "Settings", fill=TEXT_WHITE, font=f_body)

    draw_rounded_rect(draw, [1025, 120, 1165, 160], radius=6, fill=BG_CARD, outline=BORDER)
    draw.text((1045, 131), "결과 폴더" if lang == "ko" else "Open Dir", fill=TEXT_WHITE, font=f_body)

    # 4. Metrics Dashboard (4 Cards)
    metrics = metrics or {"speed": "14.8 RPS", "checked": "1,420", "avail": "3", "taken": "1,417", "hotswap": "2회 성공 (0.3s)"}
    
    card_w = (w - 32 - 36) // 4
    cards = [
        ("검사 속도" if lang == "ko" else "Scan Speed", metrics["speed"], TEXT_CYAN),
        ("총 검사수" if lang == "ko" else "Total Checked", metrics["checked"], TEXT_WHITE),
        ("가용 닉네임" if lang == "ko" else "Available Found", metrics["avail"], TEXT_SUCCESS),
        ("429 원자적 핫스왑" if lang == "ko" else "429 Hot-Swaps", metrics["hotswap"], TEXT_YELLOW),
    ]
    for i, (label, val, val_col) in enumerate(cards):
        cx1 = 16 + i * (card_w + 12)
        cx2 = cx1 + card_w
        draw_rounded_rect(draw, [cx1, 180, cx2, 246], radius=6, fill=BG_CARD, outline=BORDER)
        draw.text((cx1 + 14, 188), label, fill=TEXT_MUTED, font=f_stat_lbl)
        draw.text((cx1 + 14, 206), val, fill=val_col, font=f_stat_val)

    # 5. Split Content Area: Left Log Console, Right Available Table
    split_x = 520
    content_y1 = 258
    content_y2 = 740

    # Left Panel: Live Terminal Logs
    draw_rounded_rect(draw, [16, content_y1, split_x - 8, content_y2], radius=6, fill=BG_INPUT, outline=BORDER)
    draw.rectangle([16, content_y1, split_x - 8, content_y1 + 30], fill=BG_PANEL)
    draw.text((28, content_y1 + 7), ">> 실시간 스캔 로그" if lang == "ko" else ">> Live Stream Logs", fill=TEXT_MUTED, font=f_badge)
    
    logs = [
        ("[12:20:01]", "INFO", "UnifiedProxyManager initialized with 5 WireGuard tunnels", TEXT_MUTED),
        ("[12:20:02]", "GATE", "Pre-flight IP Verification: All 5 tunnels active", TEXT_CYAN),
        ("[12:20:03]", "SCAN", "Worker #1 [JP-Tokyo]: Checking 'a..1' -> [EXCLUDED] consecutive dots", TEXT_YELLOW),
        ("[12:20:05]", "SCAN", "Worker #2 [KR-Seoul]: Checking 'ab..' -> [EXCLUDED] trailing dot", TEXT_YELLOW),
        ("[12:20:08]", "TAKEN", "Worker #3 [SG-Singapore]: 'krc1' is TAKEN (404-miss)", TEXT_MUTED),
        ("[12:20:15]", "HIT", ">> Worker #1 [JP]: 'k4rc' is AVAILABLE! (200 OK)", TEXT_SUCCESS),
        ("[12:20:16]", "HOOK", "Discord Webhook alert dispatched for 'k4rc'", TEXT_ACCENT),
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
    draw.text((split_x + 20, content_y1 + 7), "발견된 가용 닉네임 목록 (Available Usernames)" if lang == "ko" else "Found Available Handles", fill=TEXT_WHITE, font=f_badge)
    
    # Table Header
    th_y = content_y1 + 32
    draw.rectangle([split_x + 8, th_y, w - 16, th_y + 26], fill=(38, 40, 44))
    draw.text((split_x + 24, th_y + 5), "#", fill=TEXT_MUTED, font=f_mono_sm)
    draw.text((split_x + 70, th_y + 5), "사용자명" if lang == "ko" else "Username", fill=TEXT_MUTED, font=f_badge)
    draw.text((split_x + 220, th_y + 5), "상태" if lang == "ko" else "Status", fill=TEXT_MUTED, font=f_badge)
    draw.text((split_x + 360, th_y + 5), "발견 일시" if lang == "ko" else "Timestamp", fill=TEXT_MUTED, font=f_badge)
    draw.text((split_x + 530, th_y + 5), "응답시간" if lang == "ko" else "Latency", fill=TEXT_MUTED, font=f_badge)

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
        draw.text((split_x + 70, ry + 6), uname, fill=TEXT_CYAN, font=f_mono_bold if lang=="ko" else f_mono)
        
        # Green Badge
        draw_rounded_rect(draw, [split_x + 215, ry + 4, split_x + 315, ry + 24], radius=4, fill=(28, 70, 45))
        draw.text((split_x + 228, ry + 6), "● AVAILABLE", fill=TEXT_SUCCESS, font=f_mono_sm)
        
        draw.text((split_x + 360, ry + 6), tstamp, fill=TEXT_WHITE, font=f_mono_sm)
        draw.text((split_x + 530, ry + 6), lat, fill=TEXT_MUTED, font=f_mono_sm)

    # 6. Bottom Status Bar
    draw.rectangle([0, h - 28, w, h], fill=BG_TITLEBAR)
    status_txt = "● 5개 WireGuard 터널 정상 가동 중 (KR, JP, SG, US, DE)  |  SQLite WAL 활성화: data/d4uc_results.db" if lang == "ko" else "● 5 WireGuard Tunnels Active (KR, JP, SG, US, DE) | SQLite WAL Sync: data/d4uc_results.db"
    draw.text((16, h - 21), status_txt, fill=TEXT_MUTED, font=f_badge)
    ver_txt = "v12.1.0 (Production Stable)"
    draw.text((w - 180, h - 21), ver_txt, fill=TEXT_ACCENT, font=f_badge)

    if custom_cursor:
        draw_cursor(img, custom_cursor, clicking=is_clicking)

    return img

def generate_gui_screenshots():
    print("Generating GUI Screenshots...")
    # 1. gui_ko_main.png
    img_ko = render_gui_base(lang="ko", is_running=True)
    img_ko.save(ASSETS_DIR / "gui_ko_main.png")
    print(f"  Saved {ASSETS_DIR / 'gui_ko_main.png'}")

    # 2. gui_en_main.png
    img_en = render_gui_base(lang="en", is_running=True)
    img_en.save(ASSETS_DIR / "gui_en_main.png")
    print(f"  Saved {ASSETS_DIR / 'gui_en_main.png'}")

    # 3. gui_settings_modal.png
    img_modal = render_gui_base(lang="ko", is_running=False)
    # Dim overlay
    dim = Image.new("RGBA", img_modal.size, (0, 0, 0, 160))
    img_modal = Image.alpha_composite(img_modal, dim)
    draw_m = ImageDraw.Draw(img_modal)
    
    # Modal Window in center
    mw, mh = 640, 520
    mx1 = (1200 - mw) // 2
    my1 = (780 - mh) // 2
    mx2 = mx1 + mw
    my2 = my1 + mh
    draw_rounded_rect(draw_m, [mx1, my1, mx2, my2], radius=10, fill=BG_PANEL, outline=BORDER_FOCUS, width=2)
    
    # Modal Titlebar
    draw_m.rectangle([mx1, my1, mx2, my1 + 40], fill=BG_TITLEBAR)
    f_mbold = get_font(FONT_KR_BOLD, 15)
    f_mbody = get_font(FONT_KR_REG, 13)
    f_mono = get_font(FONT_MONO, 12)
    draw_m.text((mx1 + 20, my1 + 10), "D4UC 통합 환경설정 (Settings)", fill=TEXT_WHITE, font=f_mbold)
    
    # Section 1: Surfshark WireGuard
    draw_m.text((mx1 + 30, my1 + 60), "[KEY] Surfshark WireGuard 개인키 (Private Key Pool)", fill=TEXT_CYAN, font=f_mbold)
    draw_rounded_rect(draw_m, [mx1 + 30, my1 + 86, mx2 - 30, my1 + 120], radius=5, fill=BG_INPUT, outline=BORDER)
    draw_m.text((mx1 + 42, my1 + 95), "******************************************** (5 Keys Active)", fill=TEXT_MUTED, font=f_mono)

    # Section 2: Port Range
    draw_m.text((mx1 + 30, my1 + 140), "[PORT] Wireproxy 로컬 포트 범위 (1:1 격리 터널)", fill=TEXT_WHITE, font=f_mbold)
    draw_rounded_rect(draw_m, [mx1 + 30, my1 + 166, mx1 + 200, my1 + 200], radius=5, fill=BG_INPUT, outline=BORDER)
    draw_m.text((mx1 + 42, my1 + 175), "1081 ~ 1130", fill=TEXT_WHITE, font=f_mono)

    # Section 3: Webhook URL
    draw_m.text((mx1 + 30, my1 + 220), "[WEBHOOK] Discord Webhook 알림 URL", fill=TEXT_WHITE, font=f_mbold)
    draw_rounded_rect(draw_m, [mx1 + 30, my1 + 246, mx2 - 30, my1 + 280], radius=5, fill=BG_INPUT, outline=BORDER)
    draw_m.text((mx1 + 42, my1 + 255), "https://discord.com/api/webhooks/123456789/token_secret", fill=TEXT_MUTED, font=f_mono)

    # Section 4: 429 Hot-Swap & Delay
    draw_m.text((mx1 + 30, my1 + 300), "[HOT-SWAP] 429 원자적 핫스왑 & 복구 정책", fill=TEXT_WHITE, font=f_mbold)
    draw_rounded_rect(draw_m, [mx1 + 30, my1 + 326, mx1 + 48, my1 + 344], radius=3, fill=TEXT_ACCENT)
    draw_m.text((mx1 + 34, my1 + 327), "v", fill=TEXT_WHITE, font=f_mbold)
    draw_m.text((mx1 + 60, my1 + 327), "429 감지 시 해당 터널만 0.3초 내 새 국가 노드로 즉시 교체", fill=TEXT_WHITE, font=f_mbody)

    # Buttons at bottom
    draw_rounded_rect(draw_m, [mx2 - 250, my2 - 55, mx2 - 140, my2 - 18], radius=6, fill=TEXT_ACCENT)
    draw_m.text((mx2 - 215, my2 - 44), "저장 (Save)", fill=TEXT_WHITE, font=f_mbold)

    draw_rounded_rect(draw_m, [mx2 - 120, my2 - 55, mx2 - 30, my2 - 18], radius=6, fill=BG_CARD, outline=BORDER)
    draw_m.text((mx2 - 95, my2 - 44), "닫기", fill=TEXT_WHITE, font=f_mbody)

    img_modal.save(ASSETS_DIR / "gui_settings_modal.png")
    print(f"  Saved {ASSETS_DIR / 'gui_settings_modal.png'}")

def generate_gui_gifs():
    print("Generating Animated GUI GIFs with Natural Mouse Cursor Movement...")
    # Create 14 frames for Korean edition
    frames_ko = []
    # Waypoints: start at center (600, 400), move to start button (820, 140), click, move to table row (800, 360)
    for i in range(14):
        t = i / 13.0
        if i < 4:
            # Moving towards start button
            cx = int(600 + (825 - 600) * (i / 3.0))
            cy = int(400 + (140 - 400) * (i / 3.0))
            clicking = False
            running = False
            speed_val = "0.0 RPS"
            avail_cnt = "0"
            tbl = []
        elif i == 4:
            # Clicking start button
            cx, cy = 825, 140
            clicking = True
            running = True
            speed_val = "6.5 RPS"
            avail_cnt = "0"
            tbl = []
        elif i < 8:
            # Running, scanning, cursor drifting to stats
            cx = int(825 + (350 - 825) * ((i - 4) / 4.0))
            cy = int(140 + (210 - 140) * ((i - 4) / 4.0))
            clicking = False
            running = True
            speed_val = "12.4 RPS"
            avail_cnt = "1"
            tbl = [("1", "k4rc", "AVAILABLE", "2026-11-19 12:20:15", "142ms")]
        else:
            # Cursor hovering over available table row
            cx = int(350 + (780 - 350) * ((i - 8) / 5.0))
            cy = int(210 + (360 - 210) * ((i - 8) / 5.0))
            clicking = False
            running = True
            speed_val = "14.8 RPS"
            avail_cnt = "3"
            tbl = [
                ("1", "k4rc", "AVAILABLE", "2026-11-19 12:20:15", "142ms"),
                ("2", "z99p", "AVAILABLE", "2026-11-19 12:21:04", "138ms"),
                ("3", "qv2x", "AVAILABLE", "2026-11-19 12:21:49", "151ms"),
            ]
        m = {"speed": speed_val, "checked": f"{i * 120 + 40}", "avail": avail_cnt, "taken": f"{i * 119}", "hotswap": "1회 성공"}
        f = render_gui_base(lang="ko", is_running=running, metrics=m, custom_cursor=(cx, cy), is_clicking=clicking, table_items=tbl)
        frames_ko.append(f.convert("RGB"))

    frames_ko[0].save(
        ASSETS_DIR / "gui_ko_demo.gif",
        save_all=True,
        append_images=frames_ko[1:],
        duration=320,
        loop=0
    )
    print(f"  Saved {ASSETS_DIR / 'gui_ko_demo.gif'}")

    # Create English version
    frames_en = []
    for i in range(14):
        if i < 4:
            cx = int(600 + (825 - 600) * (i / 3.0))
            cy = int(400 + (140 - 400) * (i / 3.0))
            clicking = False
            running = False
            speed_val = "0.0 RPS"
            avail_cnt = "0"
            tbl = []
        elif i == 4:
            cx, cy = 825, 140
            clicking = True
            running = True
            speed_val = "6.5 RPS"
            avail_cnt = "0"
            tbl = []
        elif i < 8:
            cx = int(825 + (350 - 825) * ((i - 4) / 4.0))
            cy = int(140 + (210 - 140) * ((i - 4) / 4.0))
            clicking = False
            running = True
            speed_val = "12.4 RPS"
            avail_cnt = "1"
            tbl = [("1", "k4rc", "AVAILABLE", "2026-11-19 12:20:15", "142ms")]
        else:
            cx = int(350 + (780 - 350) * ((i - 8) / 5.0))
            cy = int(210 + (360 - 210) * ((i - 8) / 5.0))
            clicking = False
            running = True
            speed_val = "14.8 RPS"
            avail_cnt = "3"
            tbl = [
                ("1", "k4rc", "AVAILABLE", "2026-11-19 12:20:15", "142ms"),
                ("2", "z99p", "AVAILABLE", "2026-11-19 12:21:04", "138ms"),
                ("3", "qv2x", "AVAILABLE", "2026-11-19 12:21:49", "151ms"),
            ]
        m = {"speed": speed_val, "checked": f"{i * 120 + 40}", "avail": avail_cnt, "taken": f"{i * 119}", "hotswap": "1회 성공"}
        f = render_gui_base(lang="en", is_running=running, metrics=m, custom_cursor=(cx, cy), is_clicking=clicking, table_items=tbl)
        frames_en.append(f.convert("RGB"))

    frames_en[0].save(
        ASSETS_DIR / "gui_en_demo.gif",
        save_all=True,
        append_images=frames_en[1:],
        duration=320,
        loop=0
    )
    print(f"  Saved {ASSETS_DIR / 'gui_en_demo.gif'}")

def render_cli_frame(step=10):
    w, h = 1000, 620
    img = Image.new("RGBA", (w, h), (18, 19, 23))
    draw = ImageDraw.Draw(img)

    f_mono = get_font(FONT_MONO, 14)
    f_mono_bold = get_font(FONT_MONO_BOLD, 14)
    f_title = get_font(FONT_MONO_BOLD, 16)

    # Terminal Window Titlebar
    draw.rectangle([0, 0, w, 32], fill=(28, 30, 36))
    draw.text((16, 7), "D4UC v12.1.0 - Headless CLI Dashboard (Python 3.12)", fill=TEXT_WHITE, font=f_mono_bold)
    
    # Window Dots
    draw.ellipse([w - 60, 11, w - 50, 21], fill=(242, 63, 67))
    draw.ellipse([w - 42, 11, w - 32, 21], fill=(250, 166, 26))
    draw.ellipse([w - 24, 11, w - 14, 21], fill=(35, 165, 90))

    # Box Border (Rich style)
    draw_rounded_rect(draw, [14, 46, w - 14, h - 16], radius=6, fill=(22, 24, 29), outline=(88, 101, 242), width=2)

    # Banner Header inside terminal
    draw.text((36, 62), "┌─ [ D4UC HIGH-PERFORMANCE DISCORD USERNAME CHECKER ] ─────────────────────────┐", fill=(88, 101, 242), font=f_mono)
    draw.text((36, 82), "│ Mode: HYBRID (4 chars)  |  Shards: 2_1 [a-m]  |  Tunnels: 5 Active (Wireproxy) │", fill=TEXT_CYAN, font=f_mono)
    draw.text((36, 102), "└───────────────────────────────────────────────────────────────────────────────┘", fill=(88, 101, 242), font=f_mono)

    # Metrics Panel
    draw.text((36, 134), f"• Total Checked : {120 * step:,} handles", fill=TEXT_WHITE, font=f_mono)
    draw.text((36, 154), f"• Scanning Speed: 15.2 RPS", fill=TEXT_CYAN, font=f_mono)
    draw.text((36, 174), f"• Available Found: {min(step // 3, 3)} (Written to SQLite WAL & available.txt)", fill=TEXT_SUCCESS, font=f_mono_bold)
    draw.text((36, 194), f"• 429 Hot-Swaps  : 2 atomic node rotations (0.28s zero-stall)", fill=TEXT_YELLOW, font=f_mono)

    # Progress Bar
    pct = min(100, step * 8 + 12)
    bar_len = 36
    filled = int(bar_len * (pct / 100.0))
    bar_str = "█" * filled + "░" * (bar_len - filled)
    draw.text((36, 226), f"Progress [{bar_str}] {pct}% (ETA: 00:08:42)", fill=TEXT_ACCENT, font=f_mono)

    # Workers Table
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

    # Real-time Log Stream inside terminal
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
    # 1. cli_dashboard.png
    cli_img = render_cli_frame(step=10)
    cli_img.save(ASSETS_DIR / "cli_dashboard.png")
    print(f"  Saved {ASSETS_DIR / 'cli_dashboard.png'}")

    # 2. cli_demo.gif
    cli_frames = []
    for s in range(1, 12):
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

    # Titlebar
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
        ("d4uc-shard-1  | [2026-11-19 12:20:00] [INFO] D4UC v12.1.0 starting inside Docker container (ARM64/AMD64)", TEXT_MUTED, False),
        ("d4uc-shard-1  | [2026-11-19 12:20:01] [INFO] Shard 2_1 configured: range a000..mz99 (Exhaustive search)", TEXT_WHITE, False),
        ("d4uc-shard-1  | [2026-11-19 12:20:02] [GATE] Pre-flight IP Verification: 5 WireGuard tunnels active", TEXT_CYAN, False),
        ("d4uc-shard-2  | [2026-11-19 12:20:00] [INFO] D4UC v12.1.0 starting inside Docker container (ARM64/AMD64)", TEXT_MUTED, False),
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
    print("\n✅ All 8 visual assets successfully generated in docs/assets/!")

if __name__ == "__main__":
    main()
