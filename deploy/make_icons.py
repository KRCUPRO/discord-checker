# deploy/make_icons.py
from PIL import Image, ImageDraw
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
icons_dir = ROOT / "src" / "ui" / "web" / "icons"
icons_dir.mkdir(parents=True, exist_ok=True)

# 1. Favicon SVG
svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <rect width="100" height="100" rx="22" fill="#5865F2"/>
  <path d="M54 18 L28 52 L48 52 L44 82 L72 46 L52 46 Z" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="2" stroke-linejoin="round"/>
</svg>"""
(icons_dir / "favicon.svg").write_text(svg_content, encoding="utf-8")

# 2. PNG Icons 192 and 512
for size in [192, 512]:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rx = int(size * 0.22)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=rx, fill=(88, 101, 242, 255))
    pts = [
        (int(size * 0.54), int(size * 0.18)),
        (int(size * 0.28), int(size * 0.52)),
        (int(size * 0.48), int(size * 0.52)),
        (int(size * 0.44), int(size * 0.82)),
        (int(size * 0.72), int(size * 0.46)),
        (int(size * 0.52), int(size * 0.46)),
    ]
    d.polygon(pts, fill=(255, 255, 255, 255))
    img.save(icons_dir / f"icon-{size}.png", "PNG")

print("Generated PWA Icons in src/ui/web/icons/ successfully!")
