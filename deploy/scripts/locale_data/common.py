# deploy/scripts/locale_data/common.py
"""
Common locale definitions, badge mappings, and language selector generator for D4UC.
"""
from pathlib import Path

LOCALES = [
    {
        "code": "ko",
        "tag": "KR 한국어",
        "name": "한국어",
        "badge": "update_badge.svg",
        "toc_title": "목차",
        "toc_anchor": "목차",
        "return_top": "[⬆️ 목차 맨 위로 이동](#목차)",
        "return_ref": "본문으로 돌아가기",
        "footnotes_title": "각주 및 기술 참고문헌",
        "date_str": "2026년 11월 19일",
    },
    {
        "code": "en",
        "tag": "US English",
        "name": "English",
        "badge": "update_badge_en.svg",
        "toc_title": "Table of Contents",
        "toc_anchor": "-table-of-contents",
        "return_top": "[⬆️ Return to Top](#-table-of-contents)",
        "return_ref": "Return to Reference",
        "footnotes_title": "Footnotes & Technical References",
        "date_str": "Nov 19, 2026",
    },
    {
        "code": "ja",
        "tag": "JP 日本語",
        "name": "日本語",
        "badge": "update_badge_ja.svg",
        "toc_title": "目次",
        "toc_anchor": "目次",
        "return_top": "[⬆️ 目次の先頭へ移動](#目次)",
        "return_ref": "本文に戻る",
        "footnotes_title": "脚注および技術参考文献",
        "date_str": "2026年11月19日",
    },
    {
        "code": "zh-CN",
        "tag": "CN 简体中文",
        "name": "简体中文",
        "badge": "update_badge_zh.svg",
        "toc_title": "目录",
        "toc_anchor": "目录",
        "return_top": "[⬆️ 返回目录顶部](#目录)",
        "return_ref": "返回正文",
        "footnotes_title": "脚注与技术参考文献",
        "date_str": "2026年11月19日",
    },
    {
        "code": "es",
        "tag": "ES Español",
        "name": "Español",
        "badge": "update_badge_es.svg",
        "toc_title": "Tabla de Contenidos",
        "toc_anchor": "-tabla-de-contenidos",
        "return_top": "[⬆️ Volver al Índice](#-tabla-de-contenidos)",
        "return_ref": "Volver a la Referencia",
        "footnotes_title": "Notas al pie y referencias técnicas",
        "date_str": "19 nov 2026",
    },
    {
        "code": "fr",
        "tag": "FR Français",
        "name": "Français",
        "badge": "update_badge_fr.svg",
        "toc_title": "Table des Matières",
        "toc_anchor": "-table-des-matières",
        "return_top": "[⬆️ Retour au Sommaire](#-table-des-matières)",
        "return_ref": "Retour à la référence",
        "footnotes_title": "Notes de bas de page et références techniques",
        "date_str": "19 nov 2026",
    },
    {
        "code": "de",
        "tag": "DE Deutsch",
        "name": "Deutsch",
        "badge": "update_badge_de.svg",
        "toc_title": "Inhaltsverzeichnis",
        "toc_anchor": "-inhaltsverzeichnis",
        "return_top": "[⬆️ Zurück zum Inhaltsverzeichnis](#-inhaltsverzeichnis)",
        "return_ref": "Zurück zur Referenz",
        "footnotes_title": "Fußnoten und technische Referenzen",
        "date_str": "19. Nov 2026",
    },
    {
        "code": "ru",
        "tag": "RU Русский",
        "name": "Русский",
        "badge": "update_badge_ru.svg",
        "toc_title": "Содержание",
        "toc_anchor": "-содержание",
        "return_top": "[⬆️ Наверх к содержанию](#-содержание)",
        "return_ref": "Вернуться к тексту",
        "footnotes_title": "Сноски и технические источники",
        "date_str": "19 ноя 2026",
    },
    {
        "code": "pt-BR",
        "tag": "BR Português",
        "name": "Português",
        "badge": "update_badge_pt.svg",
        "toc_title": "Índice",
        "toc_anchor": "-índice",
        "return_top": "[⬆️ Voltar ao Topo do Índice](#-índice)",
        "return_ref": "Voltar à Referência",
        "footnotes_title": "Notas de Rodapé e Referências Técnicas",
        "date_str": "19 nov 2026",
    },
    {
        "code": "ar",
        "tag": "SA العربية",
        "name": "العربية",
        "badge": "update_badge_ar.svg",
        "toc_title": "فهرس المحتويات",
        "toc_anchor": "-فهرس-المحتويات",
        "return_top": "[⬆️ العودة إلى أعلى الفهرس](#-فهرس-المحتويات)",
        "return_ref": "العودة إلى المرجع",
        "footnotes_title": "الهوامش والمراجع التقنية",
        "date_str": "19 نوفمبر 2026",
    },
    {
        "code": "hi",
        "tag": "HI हिन्दी",
        "name": "हिन्दी",
        "badge": "update_badge_hi.svg",
        "toc_title": "विषय सूची",
        "toc_anchor": "-विषय-सूची",
        "return_top": "[⬆️ विषय सूची पर वापस जाएं](#-विषय-सूची)",
        "return_ref": "संदर्भ पर वापस लौटें",
        "footnotes_title": "पाद टिप्पणियाँ और तकनीकी संदर्भ",
        "date_str": "19 नवंबर 2026",
    },
    {
        "code": "id",
        "tag": "ID Bahasa Indonesia",
        "name": "Bahasa Indonesia",
        "badge": "update_badge_id.svg",
        "toc_title": "Daftar Isi",
        "toc_anchor": "-daftar-isi",
        "return_top": "[⬆️ Kembali ke Daftar Isi](#-daftar-isi)",
        "return_ref": "Kembali ke Referensi",
        "footnotes_title": "Catatan Kaki & Referensi Teknis",
        "date_str": "19 Nov 2026",
    },
]

LOCALE_MAP = {loc["code"]: loc for loc in LOCALES}


def generate_language_table(doc_filename: str, current_locale: str, location_type: str = "locale_subdir") -> str:
    """
    Generates a 5x2 language selector table matching user specification:
    Row 1: KR 한국어 | US English | JP 日本語 | CN 简体中文 | ES Español
    Row 2: FR Français | DE Deutsch | RU Русский | BR Português | SA العربية
    Sub: HI हिन्दी • ID Bahasa Indonesia

    location_type:
      - 'locale_subdir': file is at docs/locales/<lang>/<doc_filename>
      - 'repo_root': file is at repository root (e.g., README.md, CHANGELOG.md, LICENSE, NOTICE, SECURITY.md)
      - 'docs_root': file is at docs/ (e.g., docs/README.md, docs/GUIDE.md, docs/ARCHITECTURE_MAP.md, docs/TASKS.md)
      - 'locale_flat': file is at docs/locales/<lang>.md
    """
    # 10 core languages in 5x2 grid
    row1_codes = ["ko", "en", "ja", "zh-CN", "es"]
    row2_codes = ["fr", "de", "ru", "pt-BR", "ar"]
    sub_codes = ["hi", "id"]

    def get_link(target_code: str) -> str:
        # Determine the target path relative to location_type
        if location_type == "locale_subdir":
            if target_code == current_locale:
                return f"./{doc_filename}"
            return f"../{target_code}/{doc_filename}"
        elif location_type == "repo_root":
            if doc_filename == "README.md" and target_code == "en":
                return "./README.md"
            elif doc_filename == "CHANGELOG.md" and target_code == "en":
                return "./CHANGELOG.md"
            elif doc_filename == "SECURITY.md" and target_code == "en":
                return "./SECURITY.md"
            elif doc_filename in ["LICENSE", "NOTICE"] and target_code == "en":
                return f"./{doc_filename}"
            # Otherwise point to docs/locales/<target_code>/<doc_filename> (or .md)
            ext_doc = f"{doc_filename}.md" if not doc_filename.endswith(".md") else doc_filename
            return f"./docs/locales/{target_code}/{ext_doc}"
        elif location_type == "docs_root":
            if target_code == "ko":
                return f"./{doc_filename}"
            ext_doc = f"{doc_filename}.md" if not doc_filename.endswith(".md") else doc_filename
            return f"./locales/{target_code}/{ext_doc}"
        elif location_type == "locale_flat":
            if target_code == "en":
                return "../../README.md"
            return f"./{target_code}.md"
        return f"./{doc_filename}"

    # Build cells
    r1_cells = [f"[{LOCALE_MAP[c]['tag']}]({get_link(c)})" for c in row1_codes]
    r2_cells = [f"[{LOCALE_MAP[c]['tag']}]({get_link(c)})" for c in row2_codes]
    sub_links = [f'<a href="{get_link(c)}">{LOCALE_MAP[c]["tag"]}</a>' for c in sub_codes]

    table = (
        f"| {' | '.join(r1_cells)} |\n"
        f"| :---: | :---: | :---: | :---: | :---: |\n"
        f"| {' | '.join(r2_cells)} |\n\n"
        f'<p align="center"><sub>🌐 Also available: {" • ".join(sub_links)}</sub></p>'
    )
    return table
