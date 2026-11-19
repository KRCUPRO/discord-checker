# scripts/apply_two_way_navigation.py
import re
from pathlib import Path

REPO_ROOT = Path("C:/Users/Administrator/Desktop/D4UC/github-ready")

CONFIGS = {
    "README.md": {
        "file": REPO_ROOT / "README.md",
        "toc_title": "Table of Contents",
        "toc_anchor": "-table-of-contents",
        "toc_clean": "table-of-contents",
        "return_top": "[⬆️ Back to Top](#-table-of-contents)",
        "fn_heading": "Footnotes & Technical References",
        "platform_badge_target": "docs/guides/README.md",
        "guide_prefix": "docs/guides/",
        "fn1": "[^1]: The Chrome 131 BoringSSL handshake completely neutralizes TLS fingerprinting defenses deployed by Cloudflare and modern WAFs. [↩](#-table-of-contents)",
        "fn2": "[^2]: wireproxy is a lightweight user-space Go binary translating WireGuard protocol into isolated local SOCKS5 proxies without root privileges. [↩](#-table-of-contents)",
    },
    "ko.md": {
        "file": REPO_ROOT / "docs" / "locales" / "ko.md",
        "toc_title": "목차",
        "toc_anchor": "-목차",
        "toc_clean": "목차",
        "return_top": "[⬆️ 목차 맨 위로 이동](#-목차)",
        "fn_heading": "각주 및 기술 참고문헌",
        "platform_badge_target": "../guides/README.md",
        "guide_prefix": "../guides/",
        "fn1": "[^1]: Chrome 131 BoringSSL 핸드셰이크는 WAF의 TLS 핑거프린팅 차단을 원천 무력화합니다. [↩](#-목차)",
        "fn2": "[^2]: wireproxy는 사용자 영역에서 WireGuard 프로토콜을 SOCKS5 프록시로 변환하는 경량 Go 바이너리입니다. [↩](#-목차)",
    },
    "ja.md": {
        "file": REPO_ROOT / "docs" / "locales" / "ja.md",
        "toc_title": "目次",
        "toc_anchor": "-目次",
        "toc_clean": "目次",
        "return_top": "[⬆️ 目次へ戻る](#-目次)",
        "fn_heading": "脚注および技術参考文献",
        "platform_badge_target": "../guides/README.md",
        "guide_prefix": "../guides/",
        "fn1": "[^1]: Chrome 131 BoringSSLハンドシェイクは、WAFのTLSフィンガープリントによる遮断を完全に無力化します。[↩](#-目次)",
        "fn2": "[^2]: wireproxyは、管理者権限なしにWireGuardプロトコルを独立したローカルSOCKS5プロキシに変換する軽量Goバイナリです。[↩](#-目次)",
    },
    "zh-CN.md": {
        "file": REPO_ROOT / "docs" / "locales" / "zh-CN.md",
        "toc_title": "目录",
        "toc_anchor": "-目录",
        "toc_clean": "目录",
        "return_top": "[⬆️ 返回顶部目录](#-目录)",
        "fn_heading": "脚注与技术参考文献",
        "platform_badge_target": "../guides/README.md",
        "guide_prefix": "../guides/",
        "fn1": "[^1]: Chrome 131 BoringSSL 握手彻底消除了 Cloudflare 及现代 WAF 的 TLS 指纹拦截。[↩](#-目录)",
        "fn2": "[^2]: wireproxy 是一款在用户空间运行的轻量级 Go 二进制程序，无需 Root 权限即可将 WireGuard 转换为独立的本地 SOCKS5 代理。[↩](#-目录)",
    },
    "es.md": {
        "file": REPO_ROOT / "docs" / "locales" / "es.md",
        "toc_title": "Tabla de Contenidos",
        "toc_anchor": "-tabla-de-contenidos",
        "toc_clean": "tabla-de-contenidos",
        "return_top": "[⬆️ Volver al inicio](#-tabla-de-contenidos)",
        "fn_heading": "Notas al Pie y Referencias Técnicas",
        "platform_badge_target": "../guides/README.md",
        "guide_prefix": "../guides/",
        "fn1": "[^1]: El apretón de manos BoringSSL de Chrome 131 neutraliza por completo los bloqueos por huella digital TLS de Cloudflare y WAFs modernos. [↩](#-tabla-de-contenidos)",
        "fn2": "[^2]: wireproxy es un binario ligero en Go en espacio de usuario que traduce el protocolo WireGuard en proxies locales SOCKS5 sin privilegios de root. [↩](#-tabla-de-contenidos)",
    },
    "fr.md": {
        "file": REPO_ROOT / "docs" / "locales" / "fr.md",
        "toc_title": "Table des Matières",
        "toc_anchor": "-table-des-matières",
        "toc_clean": "table-des-matières",
        "return_top": "[⬆️ Haut de page](#-table-des-matières)",
        "fn_heading": "Notes de Bas de Page et Références Techniques",
        "platform_badge_target": "../guides/README.md",
        "guide_prefix": "../guides/",
        "fn1": "[^1]: Le handshake BoringSSL de Chrome 131 neutralise entièrement les blocages d'empreintes TLS de Cloudflare et des WAF modernes. [↩](#-table-des-matières)",
        "fn2": "[^2]: wireproxy est un binaire Go léger en espace utilisateur qui convertit le protocole WireGuard en proxys SOCKS5 locaux isolés sans privilèges root. [↩](#-table-des-matières)",
    },
    "de.md": {
        "file": REPO_ROOT / "docs" / "locales" / "de.md",
        "toc_title": "Inhaltsverzeichnis",
        "toc_anchor": "-inhaltsverzeichnis",
        "toc_clean": "inhaltsverzeichnis",
        "return_top": "[⬆️ Nach oben](#-inhaltsverzeichnis)",
        "fn_heading": "Fußnoten und technische Referenzen",
        "platform_badge_target": "../guides/README.md",
        "guide_prefix": "../guides/",
        "fn1": "[^1]: Der Chrome 131 BoringSSL-Handshake neutralisiert TLS-Fingerprinting-Sperren von Cloudflare und modernen WAFs vollständig. [↩](#-inhaltsverzeichnis)",
        "fn2": "[^2]: wireproxy ist eine leichtgewichtige Go-Binärdatei im Userspace, die das WireGuard-Protokoll ohne Root-Rechte in isolierte lokale SOCKS5-Proxys übersetzt. [↩](#-inhaltsverzeichnis)",
    },
    "ru.md": {
        "file": REPO_ROOT / "docs" / "locales" / "ru.md",
        "toc_title": "Содержание",
        "toc_anchor": "-содержание",
        "toc_clean": "содержание",
        "return_top": "[⬆️ Наверх к оглавлению](#-содержание)",
        "fn_heading": "Сноски и технические примечания",
        "platform_badge_target": "../guides/README.md",
        "guide_prefix": "../guides/",
        "fn1": "[^1]: Рукопожатие Chrome 131 BoringSSL полностью нейтрализует блокировки по TLS-отпечаткам от Cloudflare и современных WAF. [↩](#-содержание)",
        "fn2": "[^2]: wireproxy — это легковесный бинарный файл на Go в пространстве пользователя, преобразующий протокол WireGuard в изолированные локальные SOCKS5-прокси без прав root. [↩](#-содержание)",
    },
    "pt-BR.md": {
        "file": REPO_ROOT / "docs" / "locales" / "pt-BR.md",
        "toc_title": "Índice",
        "toc_anchor": "-índice",
        "toc_clean": "índice",
        "return_top": "[⬆️ Voltar ao topo](#-índice)",
        "fn_heading": "Notas de Rodapé e Referências Técnicas",
        "platform_badge_target": "../guides/README.md",
        "guide_prefix": "../guides/",
        "fn1": "[^1]: O handshake BoringSSL do Chrome 131 neutraliza completamente os bloqueios de impressão digital TLS do Cloudflare e WAFs modernos. [↩](#-índice)",
        "fn2": "[^2]: O wireproxy é um binário Go leve em espaço de usuário que converte o protocolo WireGuard em proxies SOCKS5 locais isolados sem privilégios de root. [↩](#-índice)",
    },
    "ar.md": {
        "file": REPO_ROOT / "docs" / "locales" / "ar.md",
        "toc_title": "جدول المحتويات",
        "toc_anchor": "-جدول-المحتويات",
        "toc_clean": "جدول-المحتويات",
        "return_top": "[⬆️ العودة إلى أعلى الفهرس](#-جدول-المحتويات)",
        "fn_heading": "الحواشي والمراجع التقنية",
        "platform_badge_target": "../guides/README.md",
        "guide_prefix": "../guides/",
        "fn1": "[^1]: تعمل مصافحة Chrome 131 BoringSSL على تحييد حظر بصمات أصابع TLS تماماً من Cloudflare وأنظمة WAF الحديثة. [↩](#-جدول-المحتويات)",
        "fn2": "[^2]: يعتبر wireproxy برنامجاً خفيفاً بلغة Go يعمل في مساحة المستخدم لتحويل بروتوكول WireGuard إلى وكلاء SOCKS5 محليين معزولين بدون صلاحيات الجذر. [↩](#-جدول-المحتويات)",
    },
    "hi.md": {
        "file": REPO_ROOT / "docs" / "locales" / "hi.md",
        "toc_title": "सामग्री तालिका",
        "toc_anchor": "-सामग्री-तालिका",
        "toc_clean": "सामग्री-तालिका",
        "return_top": "[⬆️ सामग्री सूची पर वापस जाएं](#-सामग्री-तालिका)",
        "fn_heading": "पाद लेख और तकनीकी संदर्भ",
        "platform_badge_target": "../guides/README.md",
        "guide_prefix": "../guides/",
        "fn1": "[^1]: Chrome 131 BoringSSL हैंडशेक Cloudflare और आधुनिक WAF द्वारा लगाए गए TLS फ़िंगरप्रिंटिंग अवरोधों को पूरी तरह से निष्प्रभावी कर देता है। [↩](#-सामग्री-तालिका)",
        "fn2": "[^2]: wireproxy यूजर-स्पेस में चलने वाला एक हल्का Go बाइनरी है जो बिना रूट अनुमतियों के WireGuard प्रोटोकॉल को अलग स्थानीय SOCKS5 प्रॉक्सी में परिवर्तित करता है। [↩](#-सामग्री-तालिका)",
    },
    "id.md": {
        "file": REPO_ROOT / "docs" / "locales" / "id.md",
        "toc_title": "Daftar Isi",
        "toc_anchor": "-daftar-isi",
        "toc_clean": "daftar-isi",
        "return_top": "[⬆️ Kembali ke Daftar Isi](#-daftar-isi)",
        "fn_heading": "Catatan Kaki & Referensi Teknis",
        "platform_badge_target": "../guides/README.md",
        "guide_prefix": "../guides/",
        "fn1": "[^1]: Jabat tangan Chrome 131 BoringSSL sepenuhnya menetralkan pemblokiran sidik jari TLS dari Cloudflare dan WAF modern. [↩](#-daftar-isi)",
        "fn2": "[^2]: wireproxy adalah biner Go ringan di ruang pengguna yang mengubah protokol WireGuard menjadi proksi SOCKS5 lokal terisolasi tanpa izin root. [↩](#-daftar-isi)",
    },
}


def make_anchor(title_str: str) -> tuple[str, str]:
    clean = title_str.lower()
    clean = re.sub(r"[^\w\s\-]", "", clean, flags=re.UNICODE)
    parts = clean.split()
    joined = "-".join(parts)
    gh_anchor = "-" + joined if joined else ""
    return gh_anchor, joined


def process_document(doc_key: str, cfg: dict):
    file_path = cfg["file"]
    content = file_path.read_text(encoding="utf-8")

    # Update platform badge target
    content = re.sub(
        r"(\[!\[Platform\]\([^\)]+\)\]\()[^\)]+(\))",
        rf"\g<1>{cfg['platform_badge_target']}\2",
        content,
    )

    # Split into header and body
    assert "## 📸 " in content, f"Missing ## 📸 in {doc_key}"
    header_raw, body_raw = content.split("## 📸 ", 1)
    header = header_raw.rstrip()

    # Split body into sections
    raw_sections = re.split(r"\n(?=## )", "## 📸 " + body_raw)
    assert len(raw_sections) == 21, f"Expected 21 sections, got {len(raw_sections)} in {doc_key}"

    toc_items = []
    formatted_sections = []
    ret_top = cfg["return_top"]
    pfx = cfg["guide_prefix"]

    for idx, raw_sec in enumerate(raw_sections):
        lines = raw_sec.strip().split("\n")
        h2_line = lines[0].strip()
        h2_text = h2_line[3:].strip()

        gh_anchor, clean_anchor = make_anchor(h2_text)
        toc_items.append((h2_text, gh_anchor))

        rest_body = "\n".join(lines[1:]).strip()
        # Clean trailing hr
        rest_body = re.sub(r"\s*---\s*$", "", rest_body).strip()

        # Update preview links in Section 1
        if idx == 0:
            rest_body = re.sub(r"\(docs/guides/PC_GUIDE\.md\)", f"({pfx}WINDOWS_GUIDE.md)", rest_body)
            rest_body = re.sub(r"\(\.\./guides/PC_GUIDE\.md\)", f"({pfx}WINDOWS_GUIDE.md)", rest_body)

        # Build section block
        sec_block_lines = [
            f'<a id="{gh_anchor}"></a><a id="{clean_anchor}"></a>',
            f'## {h2_text}',
            "",
            rest_body,
            "",
            ret_top,
        ]

        # For the last section (Section 21), append footnotes
        if idx == len(raw_sections) - 1:
            sec_block_lines.extend([
                "",
                "---",
                "",
                f'### 📚 {cfg["fn_heading"]}',
                cfg["fn1"],
                cfg["fn2"],
                "",
                ret_top,
            ])
            sec_text = "\n".join(sec_block_lines)
        else:
            sec_block_lines.extend(["", "---"])
            sec_text = "\n".join(sec_block_lines)

        formatted_sections.append(sec_text)

    # Build TOC block
    toc_lines = [
        f'<a id="{cfg["toc_anchor"]}"></a><a id="{cfg["toc_clean"]}"></a>',
        f'## 📑 {cfg["toc_title"]}',
    ]
    for idx, (title, anchor) in enumerate(toc_items, 1):
        toc_lines.append(f"{idx}. [{title}](#{anchor})")
    toc_block = "\n".join(toc_lines)

    # Combine everything
    final_content = (
        header
        + "\n\n"
        + toc_block
        + "\n\n---\n\n"
        + "\n\n".join(formatted_sections)
        + "\n"
    )

    # In Section 2, ensure [^1] and [^2] are linked
    if "[^1]" not in final_content:
        final_content = re.sub(r"(Chrome 131 TLS[^\n]*?\))", r"\1[^1]", final_content, count=1)
    if "[^2]" not in final_content:
        final_content = re.sub(r"(WireGuard[^\n]*?\))", r"\1[^2]", final_content, count=1)

    file_path.write_text(final_content, encoding="utf-8")
    print(f"✅ Cleanly processed {doc_key} ({len(toc_items)} sections)")


def main():
    print("🚀 Applying pristine 1:1 Two-Way Document Navigation across all 12 docs...")
    for doc_key, cfg in CONFIGS.items():
        process_document(doc_key, cfg)
    print("🎉 All 12 documents successfully updated!")


if __name__ == "__main__":
    main()
