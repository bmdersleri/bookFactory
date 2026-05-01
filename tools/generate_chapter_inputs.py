#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate chapter input prompt files from book_manifest.yaml.

This tool creates one Markdown file per chapter in the selected target language.
It does not generate outlines or full chapter text.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

from tools.utils.yaml_utils import load_yaml



def as_lang(value, lang: str, fallback: str = "en"):
    if isinstance(value, dict):
        return value.get(lang) or value.get(fallback) or next(iter(value.values()), "")
    return value or ""


def slug_filename(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "_", value.strip().lower())
    return re.sub(r"_+", "_", value).strip("_") or "chapter"


def list_md(items) -> str:
    if not items:
        return "- Belirtilmemiş"
    return "\n".join(f"- {item}" for item in items)


def render_chapter_input(manifest: dict, chapter: dict, order: int, lang: str) -> str:
    book = manifest.get("book", {})
    language = manifest.get("language", {})
    content_scope = manifest.get("content_scope", {})
    sources = manifest.get("sources", {})

    chapter_id = chapter.get("chapter_id", f"chapter_{order:02d}")
    title = as_lang(chapter.get("title"), lang)
    part = as_lang(chapter.get("part"), lang)
    purpose = as_lang(chapter.get("purpose"), lang)

    mandatory_concepts = chapter.get("mandatory_concepts") or []
    required_code = chapter.get("required_code_examples") or []
    required_diagrams = chapter.get("required_diagrams") or chapter.get("required_visuals") or []

    lines = [
        f"# CHAPTER INPUT — {title}",
        "",
        "## 1. Manifest identity",
        "",
        f"**Book ID:** {book.get('book_id', '')}  ",
        f"**Chapter ID:** {chapter_id}  ",
        f"**Target language:** {lang}  ",
        f"**Chapter title:** {title}  ",
        f"**Part:** {part}  ",
        f"**Chapter type:** {chapter.get('chapter_type', '')}  ",
        f"**Numbering policy:** {manifest.get('automation', {}).get('numbering_policy', 'build_time')}  ",
        "",
        "## 2. Chapter purpose",
        "",
        purpose or "Bu bölümün amacı manifestte açıkça belirtilmemiştir; tam üretim öncesi netleştirilmelidir.",
        "",
        "## 3. Audience and prerequisites",
        "",
        list_md(manifest.get("audience", {}).get("primary")),
        "",
        "### Assumed background",
        "",
        list_md(manifest.get("audience", {}).get("assumed_background")),
        "",
        "## 4. Mandatory concepts",
        "",
        list_md(mandatory_concepts),
        "",
        "## 5. Required code/application assets",
        "",
    ]

    if required_code:
        for item in required_code:
            if isinstance(item, dict):
                cid = item.get("id", f"{chapter_id}_code")
                lines.extend([
                    f"### Code asset: `{cid}`",
                    "",
                    f"- Title: {as_lang(item.get('title'), lang)}",
                    f"- File: `{item.get('file', '')}`",
                    f"- Kind: `{item.get('kind', 'example')}`",
                    f"- Test policy: `{item.get('test', 'compile')}`",
                    f"- GitHub: `{item.get('github', True)}`",
                    f"- QR: `{item.get('qr', 'dual')}`",
                    "",
                ])
            else:
                lines.append(f"- {item}")
    else:
        lines.append("- Bu bölüm için zorunlu kod varlığı tanımlanmamıştır.")

    lines.extend(["", "## 6. Required diagram/visual/screenshot assets", ""])
    if required_diagrams:
        for item in required_diagrams:
            if isinstance(item, dict):
                vid = item.get("id", f"{chapter_id}_visual")
                lines.extend([
                    f"### Visual asset: `{vid}`",
                    "",
                    f"- Title: {as_lang(item.get('title'), lang)}",
                    f"- Type: `{item.get('type', 'mermaid')}`",
                    "- Manual asset override: `true`",
                    "",
                ])
            else:
                lines.append(f"- {item}")
    else:
        lines.append("- Bu bölüm için zorunlu görsel varlığı tanımlanmamıştır.")

    lines.extend([
        "",
        "## 7. Mini application / chapter task",
        "",
        as_lang(chapter.get("mini_application"), lang) or "Belirtilmemiş.",
        "",
        "## 8. Out-of-scope topics",
        "",
        list_md(content_scope.get("exclude")),
        "",
        "## 9. Source policy",
        "",
        "Bu bölümde teknik doğruluk için manifestte tanımlı kaynak önceliği izlenmelidir.",
        "",
        list_md(sources.get("priority_policy")),
        "",
        "## 10. Outline generation instruction",
        "",
        "Bu bölüm için önce yalnızca ayrıntılı outline üret. Tam metne geçme.",
        "",
        "## 11. Full-text generation note",
        "",
        "Tam metin üretiminde başlıklar manuel numaralandırılmamalıdır. Görünen bölüm, alt başlık, şekil, tablo ve kod numaraları build aşamasında atanacaktır.",
        "",
    ])

    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Generate chapter input prompts from a book manifest.")
    parser.add_argument("manifest", help="book_manifest.yaml")
    parser.add_argument("--language", help="Target language; defaults to manifest.language.primary_language")
    parser.add_argument("--out-dir", help="Output directory")
    args = parser.parse_args(argv)

    manifest_path = Path(args.manifest)
    manifest = load_yaml(manifest_path)

    lang = args.language or manifest.get("language", {}).get("primary_language") or "tr"
    book_id = manifest.get("book", {}).get("book_id", "book")
    out_dir = Path(args.out_dir or f"generated/{book_id}/{lang}/chapter_inputs")
    out_dir.mkdir(parents=True, exist_ok=True)

    chapters = manifest.get("chapters") or []
    if not chapters:
        print("[ERROR] Manifest has no chapters.", file=sys.stderr)
        return 1

    for i, chapter in enumerate(chapters, start=1):
        chapter_id = chapter.get("chapter_id", f"chapter_{i:02d}")
        filename = f"chapter_{i:02d}_{slug_filename(chapter_id)}_input.md"
        path = out_dir / filename
        path.write_text(render_chapter_input(manifest, chapter, i, lang), encoding="utf-8")
        print(f"[WRITE] {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
