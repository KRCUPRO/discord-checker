# deploy/generate_badges.py
"""
Generates 1:1 localized update date SVG badges in docs/assets/badges/ for all 12 languages.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BADGES_DIR = ROOT / "docs" / "assets" / "badges"
BADGES_DIR.mkdir(parents=True, exist_ok=True)

BADGES_SPEC = [
    {
        "filename": "update_badge.svg",
        "lang": "ko",
        "label": "최종 업데이트",
        "date": "2026년 11월 19일",
        "left_w": 86,
        "right_w": 120,
    },
    {
        "filename": "update_badge_en.svg",
        "lang": "en",
        "label": "Last Updated",
        "date": "Nov 19, 2026",
        "left_w": 86,
        "right_w": 104,
    },
    {
        "filename": "update_badge_ja.svg",
        "lang": "ja",
        "label": "最終更新",
        "date": "2026年11月19日",
        "left_w": 68,
        "right_w": 120,
    },
    {
        "filename": "update_badge_zh.svg",
        "lang": "zh-CN",
        "label": "最后更新",
        "date": "2026年11月19日",
        "left_w": 68,
        "right_w": 120,
    },
    {
        "filename": "update_badge_es.svg",
        "lang": "es",
        "label": "Última actualización",
        "date": "19 nov 2026",
        "left_w": 126,
        "right_w": 96,
    },
    {
        "filename": "update_badge_fr.svg",
        "lang": "fr",
        "label": "Dernière mise à jour",
        "date": "19 nov 2026",
        "left_w": 126,
        "right_w": 96,
    },
    {
        "filename": "update_badge_de.svg",
        "lang": "de",
        "label": "Zuletzt aktualisiert",
        "date": "19. Nov 2026",
        "left_w": 122,
        "right_w": 98,
    },
    {
        "filename": "update_badge_ru.svg",
        "lang": "ru",
        "label": "Последнее обновление",
        "date": "19 ноя 2026",
        "left_w": 142,
        "right_w": 94,
    },
    {
        "filename": "update_badge_pt.svg",
        "lang": "pt-BR",
        "label": "Última atualização",
        "date": "19 nov 2026",
        "left_w": 124,
        "right_w": 96,
    },
    {
        "filename": "update_badge_ar.svg",
        "lang": "ar",
        "label": "آخر تحديث",
        "date": "19 نوفمبر 2026",
        "left_w": 72,
        "right_w": 118,
    },
    {
        "filename": "update_badge_hi.svg",
        "lang": "hi",
        "label": "अंतिम अद्यतन",
        "date": "19 नवंबर 2026",
        "left_w": 90,
        "right_w": 110,
    },
    {
        "filename": "update_badge_id.svg",
        "lang": "id",
        "label": "Pembaruan Terakhir",
        "date": "19 Nov 2026",
        "left_w": 124,
        "right_w": 96,
    },
]

SVG_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{total_w}" height="20" role="img" aria-label="{aria_label}">
  <title>{aria_label}</title>
  <a xlink:href="CHANGELOG.md" target="_parent">
    <linearGradient id="s" x2="0" y2="100%">
      <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
      <stop offset="1" stop-opacity=".1"/>
    </linearGradient>
    <clipPath id="r">
      <rect width="{total_w}" height="20" rx="3" fill="#fff"/>
    </clipPath>
    <g clip-path="url(#r)">
      <rect width="{left_w}" height="20" fill="#555"/>
      <rect x="{left_w}" width="{right_w}" height="20" fill="#5865F2"/>
      <rect width="{total_w}" height="20" fill="url(#s)"/>
    </g>
    <g fill="#fff" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" text-rendering="geometricPrecision" font-size="110">
      <text aria-hidden="true" x="{left_center}" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="{left_len}">{label}</text>
      <text x="{left_center}" y="140" transform="scale(.1)" fill="#fff" textLength="{left_len}">{label}</text>
      <text aria-hidden="true" x="{right_center}" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="{right_len}">{date}</text>
      <text x="{right_center}" y="140" transform="scale(.1)" fill="#fff" textLength="{right_len}">{date}</text>
    </g>
  </a>
</svg>"""

def generate():
    for item in BADGES_SPEC:
        left_w = item["left_w"]
        right_w = item["right_w"]
        total_w = left_w + right_w
        left_center = int((left_w / 2.0) * 10)
        right_center = int((left_w + (right_w / 2.0)) * 10)
        left_len = int((left_w - 12) * 10)
        right_len = int((right_w - 12) * 10)
        aria_label = f"{item['label']}: {item['date']}"

        svg_text = SVG_TEMPLATE.format(
            total_w=total_w,
            left_w=left_w,
            right_w=right_w,
            left_center=left_center,
            right_center=right_center,
            left_len=left_len,
            right_len=right_len,
            label=item["label"],
            date=item["date"],
            aria_label=aria_label,
        )

        out_path = BADGES_DIR / item["filename"]
        out_path.write_text(svg_text, encoding="utf-8")
        print(f"✅ Generated badge: {item['filename']} (Lang: {item['lang']}, Width: {total_w}px)")

    print(f"\n🎉 Successfully generated all {len(BADGES_SPEC)} 1:1 localized SVG update badges in docs/assets/badges/!")

if __name__ == "__main__":
    generate()
