#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup GitHub Pages with Just-the-Docs theme for a BookFactory code repository.

Generates:
- docs/_config.yml        (Just-the-Docs Jekyll config)
- docs/index.md           (landing page)
- docs/kodlar/index.md    (code index with chapter grid)
- docs/kodlar/bolumXX/index.md  (chapter parent pages × 16)
- Updates all existing docs/kodlar/bolumXX/kodYY/index.md with parent frontmatter
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CHAPTERS = {
    "chapter_01": ("bolum01",  1, "Modern Web'e Giriş"),
    "chapter_02": ("bolum02",  2, "JavaScript ES6+ ve React"),
    "chapter_03": ("bolum03",  3, "HTML/CSS ve Bileşen"),
    "chapter_04": ("bolum04",  4, "JSX ve Bileşen Anatomisi"),
    "chapter_05": ("bolum05",  5, "Props ve Veri Akışı"),
    "chapter_06": ("bolum06",  6, "State Yönetimi"),
    "chapter_07": ("bolum07",  7, "useEffect ve Yan Etkiler"),
    "chapter_08": ("bolum08",  8, "İleri Hooks"),
    "chapter_09": ("bolum09",  9, "Custom Hooks"),
    "chapter_10": ("bolum10", 10, "React Router"),
    "chapter_11": ("bolum11", 11, "Form Yönetimi"),
    "chapter_12": ("bolum12", 12, "Redux Toolkit"),
    "chapter_13": ("bolum13", 13, "REST API"),
    "chapter_14": ("bolum14", 14, "Zustand"),
    "chapter_15": ("bolum15", 15, "Performans ve Test"),
    "chapter_16": ("bolum16", 16, "KampüsHub Final"),
}

CHAPTER_NAV_TITLE = {ch: f"Bölüm {n}: {label}" for ch, (_, n, label) in CHAPTERS.items()}


def chapter_nav_title(chapter_id: str) -> str:
    return CHAPTER_NAV_TITLE.get(chapter_id, chapter_id)


def update_frontmatter(text: str, updates: dict[str, str]) -> str:
    """Add or replace keys in YAML frontmatter. Keeps existing keys."""
    fm_re = re.compile(r'\A(---\s*\n)(.*?)(---\s*\n)', re.DOTALL)
    m = fm_re.match(text)
    if not m:
        fm_lines = ["---"]
        for k, v in updates.items():
            fm_lines.append(f'{k}: "{v}"')
        fm_lines.append("---\n\n")
        return "\n".join(fm_lines) + text

    body = m.group(2)
    # Remove existing keys that we'll override
    for key in updates:
        body = re.sub(rf'^{re.escape(key)}:.*\n', '', body, flags=re.MULTILINE)
    # Append new keys
    for k, v in updates.items():
        body += f'{k}: "{v}"\n'

    return m.group(1) + body + m.group(3) + text[m.end():]


def write_config(docs_dir: Path, owner: str, repo: str) -> None:
    config = f"""\
title: "React ile Web Uygulama Geliştirme"
description: "Kitap kod örnekleri — 88 JavaScript bloğu, 16 bölüm, tümü test geçti"
baseurl: "/{repo}"
url: "https://{owner}.github.io"

remote_theme: just-the-docs/just-the-docs@v0.10.0

plugins:
  - jekyll-remote-theme
  - jekyll-seo-tag

# ── Just-the-Docs ──────────────────────────────────────────────────────
search_enabled: true
search:
  heading_level: 2
  previews: 3
  preview_words_before: 5
  preview_words_after: 10
  tokenizer_separator: /[\\s/]+/

heading_anchors: true
back_to_top: true
back_to_top_text: "Başa dön"
footer_content: >
  <b>React ile Web Uygulama Geliştirme</b> — BookFactory ile üretilmiştir.
  <a href="https://github.com/{owner}/{repo}">GitHub</a>

color_scheme: default

aux_links:
  "GitHub →":
    - "https://github.com/{owner}/{repo}"
aux_links_new_tab: true

# ── Dil / encoding ──────────────────────────────────────────────────────
lang: tr
encoding: utf-8
markdown: kramdown
highlighter: rouge
kramdown:
  input: GFM
  syntax_highlighter: rouge
  syntax_highlighter_opts:
    css_class: highlight
    span:
      line_numbers: false
    block:
      line_numbers: true
      start_line: 1
"""
    (docs_dir / "_config.yml").write_text(config, encoding="utf-8")
    print("[OK] docs/_config.yml")


def write_index(docs_dir: Path, owner: str, repo: str, code_counts: dict[str, int]) -> None:
    total = sum(code_counts.values())
    rows = []
    for ch_id, (folder, n, label) in sorted(CHAPTERS.items(), key=lambda x: x[1][1]):
        count = code_counts.get(ch_id, 0)
        url = f"/{repo}/kodlar/{folder}/"
        rows.append(f"| [{n}. {label}]({url}) | {count} |")

    index = f"""\
---
title: Ana Sayfa
nav_order: 1
---

# React ile Web Uygulama Geliştirme
{{: .fs-9 }}

Kitabın tüm kod örneklerine buradan ulaşabilirsiniz.
{{: .fs-6 .fw-300 }}

[Kod Örnekleri →](/{repo}/kodlar/){{: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }}
[GitHub →](https://github.com/{owner}/{repo}){{: .btn .fs-5 .mb-4 .mb-md-0 }}

---

## Hakkında

Bu site, **{total} JavaScript kod bloğunu** içeren kitabın eşlik eden kod deposudur.
Her bölümde yer alan kod örneklerini inceleyebilir, GitHub üzerinden kaynaklara erişebilir,
kitaptaki QR kodlarını okuyarak doğrudan ilgili sayfaya ulaşabilirsiniz.

| Özellik | Değer |
|---|---|
| Toplam kod bloğu | **{total}** |
| Bölüm sayısı | **16** |
| Dil | JavaScript |
| Test durumu | ✅ 88/88 geçti |

---

## Bölümler

| Bölüm | Kod sayısı |
|---|---|
{chr(10).join(rows)}
"""
    (docs_dir / "index.md").write_text(index, encoding="utf-8")
    print("[OK] docs/index.md")


def write_kodlar_index(docs_dir: Path, repo: str, code_counts: dict[str, int]) -> None:
    kodlar_dir = docs_dir / "kodlar"
    kodlar_dir.mkdir(parents=True, exist_ok=True)
    cards = []
    for ch_id, (folder, n, label) in sorted(CHAPTERS.items(), key=lambda x: x[1][1]):
        count = code_counts.get(ch_id, 0)
        cards.append(f"- **[Bölüm {n}: {label}](/{repo}/kodlar/{folder}/)** — {count} kod")

    content = f"""\
---
title: Kod Örnekleri
nav_order: 2
has_children: true
---

# Kod Örnekleri

Kitabın 16 bölümünde yer alan tüm JavaScript kod örnekleri.

{chr(10).join(cards)}
"""
    (kodlar_dir / "index.md").write_text(content, encoding="utf-8")
    print("[OK] docs/kodlar/index.md")


def write_chapter_pages(docs_dir: Path, repo: str, items: list[dict]) -> None:
    from collections import defaultdict
    chapter_items: dict[str, list[dict]] = defaultdict(list)
    for item in items:
        chapter_items[item["chapter_id"]].append(item)

    for ch_id, (folder, n, label) in sorted(CHAPTERS.items(), key=lambda x: x[1][1]):
        ch_dir = docs_dir / "kodlar" / folder
        ch_dir.mkdir(parents=True, exist_ok=True)
        nav_title = f"Bölüm {n}: {label}"
        codes = chapter_items.get(ch_id, [])

        rows = []
        for item in codes:
            title = item.get("title") or item.get("title_key") or item.get("id")
            code_folder = item.get("code_folder", "")
            src_url = item.get("github_source_url", "")
            page_url = f"/{repo}/kodlar/{folder}/{code_folder}/"
            rows.append(f"| [{title}]({page_url}) | `{item.get('file','')}` | [GitHub]({src_url}) |")

        content = f"""\
---
title: "{nav_title}"
parent: Kod Örnekleri
nav_order: {n}
has_children: true
---

# {n}. {label}

Bu bölümde **{len(codes)} kod örneği** bulunmaktadır.

| Örnek | Dosya | Kaynak |
|---|---|---|
{chr(10).join(rows) if rows else "| — | — | — |"}
"""
        (ch_dir / "index.md").write_text(content, encoding="utf-8")

    print(f"[OK] docs/kodlar/bolumXX/index.md (16 bölüm)")


def update_code_pages(docs_dir: Path, items: list[dict]) -> int:
    updated = 0
    for item in items:
        ch_id = item.get("chapter_id", "")
        code_folder = item.get("code_folder", "")
        _, n, label = CHAPTERS.get(ch_id, ("", 0, ch_id))
        chapter_folder = item.get("chapter_folder", "")
        if not (chapter_folder and code_folder):
            continue
        page = docs_dir / "kodlar" / chapter_folder / code_folder / "index.md"
        if not page.exists():
            continue
        text = page.read_text(encoding="utf-8")
        nav_title = f"Bölüm {n}: {label}"
        code_title = item.get("title") or item.get("title_key") or item.get("id") or code_folder
        new_text = update_frontmatter(text, {
            "title": code_title,
            "parent": nav_title,
            "grand_parent": "Kod Örnekleri",
        })
        if new_text != text:
            page.write_text(new_text, encoding="utf-8")
            updated += 1
    print(f"[OK] {updated} kod sayfası güncellendi (parent/grand_parent)")
    return updated


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs-dir", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--owner", default="bmdersleri")
    ap.add_argument("--repo", default="react-web")
    args = ap.parse_args(argv)

    docs_dir = args.docs_dir.resolve()
    with open(args.manifest, encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("items", [])

    from collections import Counter
    code_counts = Counter(i["chapter_id"] for i in items)

    write_config(docs_dir, args.owner, args.repo)
    write_index(docs_dir, args.owner, args.repo, code_counts)
    write_kodlar_index(docs_dir, args.repo, code_counts)
    write_chapter_pages(docs_dir, args.repo, items)
    update_code_pages(docs_dir, items)

    print(f"\n[DONE] GitHub Pages setup tamamlandı: {docs_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
