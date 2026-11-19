# deploy/scripts/verify_anchor_links.py
import pathlib
import re

root = pathlib.Path(__file__).resolve().parent.parent.parent


def verify_all_document_links():
    docs = [root / "README.md"] + sorted(list((root / "docs/locales").glob("*.md")))
    print("=== 12 LOCALE DOCUMENTS AUDIT ===")
    for d in docs:
        txt = d.read_text(encoding="utf-8")
        toc_links = re.findall(r"^\d+\.\s+\[([^\]]+)\]\(#([^\)]+)\)", txt, re.M)
        return_links = re.findall(r"\[⬆️[^\]]+\]\(#([^\)]+)\)", txt)
        fn_def_1 = txt.count("[^1]:")
        fn_def_2 = txt.count("[^2]:")
        fn_ref_1 = len(re.findall(r"\[\^1\](?!:)", txt))
        fn_ref_2 = len(re.findall(r"\[\^2\](?!:)", txt))
        print(f"{d.name:10s} | TOC: {len(toc_links):2d} | RetTop: {len(return_links):2d} | fn1 def/ref: {fn_def_1}/{fn_ref_1} | fn2 def/ref: {fn_def_2}/{fn_ref_2}")
        assert len(toc_items := toc_links) == 21, f"Expected 21 TOC items in {d.name}, got {len(toc_items)}"
        assert fn_def_1 == 1 and fn_ref_1 == 1, f"fn1 mismatch in {d.name}"
        assert fn_def_2 == 1 and fn_ref_2 == 1, f"fn2 mismatch in {d.name}"
        assert len(return_links) >= 21, f"Insufficient return links in {d.name}"

    print("\n=== OS GUIDES AUDIT ===")
    guides = sorted(list((root / "docs/guides").glob("*.md"))) + [root / "docs/README.md", root / "docs/GUIDE.md"]
    for g in guides:
        txt = g.read_text(encoding="utf-8")
        toc_links = re.findall(r"^\d+\.\s+\[([^\]]+)\]\(#([^\)]+)\)", txt, re.M)
        return_links = re.findall(r"\[⬆️[^\]]+\]\(#([^\)]+)\)", txt)
        print(f"{g.relative_to(root).as_posix():35s} | TOC: {len(toc_links):2d} | RetTop: {len(return_links):2d}")
        assert len(toc_links) >= 3, f"Expected TOC in {g.name}"
        assert len(return_links) >= 3, f"Expected return links in {g.name}"
        if "[^1]:" in txt:
            fn_refs = len(re.findall(r"\[\^1\](?!:)", txt))
            assert fn_refs >= 1, f"Missing fn1 ref in {g.name}"

    print("\n=== INTERNAL ANCHOR & FILE LINK INTEGRITY ===")
    all_files = (
        [root / "README.md", root / "CHANGELOG.md", root / "SECURITY.md", root / "docs/README.md", root / "docs/GUIDE.md", root / "docs/ARCHITECTURE_MAP.md", root / "docs/TASKS.md"]
        + list((root / "docs/locales").glob("*.md"))
        + list((root / "docs/locales").glob("*/*.md"))
        + list((root / "docs/guides").glob("*.md"))
    )
    broken_internal = []
    missing_files = []

    for f in all_files:
        text = f.read_text(encoding="utf-8")
        explicit_ids = set(re.findall(r'id="([^"]+)"', text))
        headers = re.findall(r'^(#{1,6})\s+(.+)$', text, re.M)
        gh_slugs = set()
        for _, h in headers:
            clean = re.sub(r"[^\w\s\-]", "", h.lower(), flags=re.UNICODE)
            slug = "-".join(clean.split())
            gh_slugs.add(slug)
            gh_slugs.add("-" + slug)
        all_targets = explicit_ids | gh_slugs

        # Check internal anchors
        links = re.findall(r'\[([^\]]+)\]\(#([^\)]+)\)', text)
        for lbl, tgt in links:
            if tgt not in all_targets:
                broken_internal.append((f.relative_to(root).as_posix(), lbl, tgt))

        # Check relative file links
        file_links = re.findall(r'\[([^\]]+)\]\(([^#\)\s]+)(?:#[^\)]*)?\)', text)
        img_links = re.findall(r'!\[([^\]]*)\]\(([^#\)\s]+)\)', text)
        for lbl, tgt in file_links + img_links:
            if tgt.startswith(("http://", "https://", "mailto:")):
                continue
            if not (f.parent / tgt).resolve().exists():
                missing_files.append((f.relative_to(root).as_posix(), lbl, tgt))

    print(f"Total files audited: {len(all_files)}")
    print(f"Broken internal links: {len(broken_internal)}")
    print(f"Missing relative files: {len(missing_files)}")
    assert len(broken_internal) == 0, f"Found broken internal links: {broken_internal}"
    assert len(missing_files) == 0, f"Found missing relative file targets: {missing_files}"
    print("🎉 ZERO BROKEN LINKS: 100% PERFECT NAVIGATION INTEGRITY!")

if __name__ == "__main__":
    verify_all_document_links()
