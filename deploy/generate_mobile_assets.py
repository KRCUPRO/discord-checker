# deploy/generate_mobile_assets.py
"""
Generates high-fidelity Mobile Web GUI visual assets:
1. docs/assets/mobile_web_main.png (Smartphone mockup screenshot)
2. docs/assets/mobile_web_demo.gif (Interactive animated mobile demo)
"""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "docs" / "assets"
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

def draw_rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def draw_touch_ripple(img, pos, radius=24, alpha=180):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    x, y = pos
    d.ellipse([x - radius, y - radius, x + radius, y + radius], outline=(88, 101, 242, alpha), width=3)
    d.ellipse([x - radius // 2, y - radius // 2, x + radius // 2, y + radius // 2], fill=(255, 255, 255, min(220, alpha + 40)))
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay), (0, 0))

def render_mobile_frame(step=0, touch_pos=None, is_touching=False, toast_text=None):
    w, h = 440, 880
    img = Image.new("RGBA", (w, h), BG_PHONE)
    draw = ImageDraw.Draw(img)

    f_title = get_font(FONT_KR_BOLD, 15)
    f_sub = get_font(FONT_KR_REG, 11)
    f_badge = get_font(FONT_KR_BOLD, 11)
    f_body = get_font(FONT_KR_REG, 12)
    f_bold = get_font(FONT_KR_BOLD, 12)
    f_mono = get_font(FONT_MONO, 11)
    f_mono_bold = get_font(FONT_MONO_BOLD, 12)
    f_stat_val = get_font(FONT_KR_BOLD, 18)
    f_stat_lbl = get_font(FONT_KR_REG, 10)

    # 1. Phone Bezel & Outer Shell
    draw_rounded_rect(draw, [6, 6, w - 6, h - 6], radius=38, fill=BG_APP, outline=(70, 74, 82), width=3)

    # 2. Dynamic Island / Notch
    draw_rounded_rect(draw, [w // 2 - 55, 14, w // 2 + 55, 38], radius=12, fill=(0, 0, 0), outline=(30, 30, 30))
    # Camera lens circle
    draw.ellipse([w // 2 + 25, 22, w // 2 + 37, 34], fill=(15, 20, 30))

    # Top Status Bar (Time, 5G, Battery)
    draw.text((36, 19), "13:30", fill=TEXT_WHITE, font=f_bold)
    # 5G & Battery icon representations
    draw.text((w - 74, 19), "5G  88%", fill=TEXT_WHITE, font=f_sub)

    # 3. App Header Bar
    draw.rectangle([6, 48, w - 6, 96], fill=BG_PANEL)
    draw.line([6, 96, w - 6, 96], fill=BORDER, width=1)

    # App Logo
    draw_rounded_rect(draw, [20, 56, 52, 88], radius=8, fill=TEXT_ACCENT)
    draw.text((28, 62), "⚡", fill=TEXT_WHITE, font=f_title)

    draw.text((60, 57), "D4UC Mobile Web", fill=TEXT_WHITE, font=f_title)
    draw.text((60, 75), "Discord Checker v12.2.0 (PWA)", fill=TEXT_MUTED, font=f_sub)

    # Status Pill Badge
    is_running = (step >= 2)
    pill_text = "실행 중 (15w)" if is_running else "대기 중"
    dot_color = TEXT_SUCCESS if is_running else TEXT_MUTED
    draw_rounded_rect(draw, [w - 116, 60, w - 20, 84], radius=12, fill=BG_INPUT, outline=BORDER)
    draw.ellipse([w - 106, 68, w - 98, 76], fill=dot_color)
    draw.text((w - 92, 65), pill_text, fill=TEXT_WHITE, font=f_badge)

    # 4. Telemetry 2x3 Grid
    base_checked = 12000 + step * 380
    rps_val = 45.2 + math.sin(step * 0.8) * 4.5 if is_running else 0.0
    avail_count = 14 + (step // 3)

    metrics = [
        ("속도 (RPS)", f"{rps_val:.1f}", TEXT_CYAN),
        ("가용 발견", f"{avail_count}", TEXT_SUCCESS),
        ("총 검사", f"{base_checked:,}", TEXT_WHITE),
        ("선점 (TAKEN)", f"{base_checked - avail_count:,}", TEXT_WHITE),
        ("429 노드교체", f"{3 + (step // 5)}", TEXT_YELLOW),
        ("평균 레이턴시", f"{38 + (step % 5)}ms", TEXT_WHITE),
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
    draw.text((30, graph_y + 6), "⚡ 실시간 탐색 속도 추이 (RPS Canvas)", fill=TEXT_MUTED, font=f_sub)
    draw.text((w - 110, graph_y + 6), f"최고: 49.8 req/s", fill=TEXT_CYAN, font=f_sub)

    # Canvas inner
    draw_rounded_rect(draw, [28, graph_y + 24, w - 28, graph_y + 62], radius=4, fill=BG_INPUT)
    # Simulated wave curve
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
    tabs = ["결과 목록", "탐색 조건", "프록시", "로그"]
    tw = (w - 48) // 4
    for i, t in enumerate(tabs):
        tx = 24 + i * tw
        if i == 0:
            draw_rounded_rect(draw, [tx, tab_y + 3, tx + tw - 2, tab_y + 33], radius=6, fill=TEXT_ACCENT)
            draw.text((tx + 12, tab_y + 11), t, fill=TEXT_WHITE, font=f_bold)
        else:
            draw.text((tx + 12, tab_y + 11), t, fill=TEXT_MUTED, font=f_body)

    # 7. Discovered Usernames Results List
    res_y = 356
    draw_rounded_rect(draw, [20, res_y, w - 20, h - 90], radius=12, fill=BG_PANEL, outline=BORDER)
    draw.text((32, res_y + 12), "🎉 발견된 희귀 닉네임", fill=TEXT_WHITE, font=f_title)
    draw_rounded_rect(draw, [180, res_y + 12, 210, res_y + 30], radius=9, fill=TEXT_SUCCESS)
    draw.text((188, res_y + 14), str(avail_count), fill=TEXT_WHITE, font=f_badge)

    # Results action buttons
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
        draw.text((44, iy + 8), uname, fill=TEXT_SUCCESS, font=f_title)
        draw.text((44, iy + 32), f"발견: {ts} | {lat} | {mode_str}", fill=TEXT_MUTED, font=f_mono)

        # 1-Tap Copy Button
        draw_rounded_rect(draw, [w - 95, iy + 12, w - 40, iy + 44], radius=6, fill=TEXT_ACCENT)
        draw.text((w - 82, iy + 21), "복사", fill=TEXT_WHITE, font=f_bold)

    # 8. Bottom Fixed Action Controls
    bot_y = h - 84
    draw.rectangle([6, bot_y, w - 6, h - 6], fill=BG_PANEL)
    draw.line([6, bot_y, w - 6, bot_y], fill=BORDER, width=1)

    # Big START/STOP Touch Button
    btn_col = TEXT_DANGER if is_running else TEXT_SUCCESS
    btn_lbl = "■  탐색 중지" if is_running else "▶  탐색 시작"
    draw_rounded_rect(draw, [24, bot_y + 10, w - 120, bot_y + 58], radius=10, fill=btn_col)
    draw.text((w // 2 - 80, bot_y + 24), btn_lbl, fill=TEXT_WHITE, font=f_title)

    # Restart Button
    draw_rounded_rect(draw, [w - 110, bot_y + 10, w - 24, bot_y + 58], radius=10, fill=BG_CARD, outline=BORDER)
    draw.text((w - 86, bot_y + 24), "🔄 재시작", fill=TEXT_WHITE, font=f_bold)

    # Home Bar
    draw_rounded_rect(draw, [w // 2 - 60, h - 14, w // 2 + 60, h - 9], radius=3, fill=(120, 120, 120))

    # Optional Toast Message
    if toast_text:
        tw = 180
        draw_rounded_rect(draw, [w // 2 - tw // 2, 64, w // 2 + tw // 2, 98], radius=17, fill=TEXT_SUCCESS)
        draw.text((w // 2 - tw // 2 + 16, 74), toast_text, fill=TEXT_WHITE, font=f_bold)

    # Draw touch ripple
    if touch_pos:
        draw_touch_ripple(img, touch_pos, radius=26 if is_touching else 16, alpha=220 if is_touching else 140)

    return img

def generate_mobile_assets():
    print("Generating Mobile Web GUI Assets...")
    # 1. Main Static Screenshot
    main_img = render_mobile_frame(step=8)
    main_img.save(ASSETS_DIR / "mobile_web_main.png")
    print(f"  ✅ Saved {ASSETS_DIR / 'mobile_web_main.png'}")

    # 2. Interactive Animated Demo GIF
    frames = []
    w, h = 440, 880

    # Sequence of animated mobile interactions
    # 0-3: Idle and tapping Start
    # 4-9: Running with climbing metrics
    # 10-12: Tapping copy button on 'v.vip'
    # 13-15: Showing toast '복사 완료!'
    for step in range(16):
        touch_pos = None
        is_touch = False
        toast = None

        if step == 2:
            touch_pos = (w // 2 - 50, h - 55) # Tapping Start
            is_touch = True
        elif step == 10:
            touch_pos = (w - 65, 416) # Tapping Copy button on 'v.vip'
            is_touch = True
        elif step in (11, 12, 13):
            toast = "📋 'v.vip' 복사 완료!"

        f = render_mobile_frame(step=step, touch_pos=touch_pos, is_touching=is_touch, toast_text=toast)
        frames.append(f.convert("RGB"))

    frames[0].save(
        ASSETS_DIR / "mobile_web_demo.gif",
        save_all=True,
        append_images=frames[1:],
        duration=320,
        loop=0
    )
    print(f"  ✅ Saved {ASSETS_DIR / 'mobile_web_demo.gif'}")

if __name__ == "__main__":
    generate_mobile_assets()
