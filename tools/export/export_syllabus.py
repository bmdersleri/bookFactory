#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Syllabus and ECTS Information Package Generator for BookFactory.

This tool extracts book metadata and 'academic' block from book_manifest.yaml
to generate a professional Markdown syllabus.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

# Ensure we can import from tools.utils if needed, but let's stick to core yaml loading
# In BookFactory, usually we have a shared yaml utility. 
# Looking at previous turns, I see tools.utils.yaml_utils is used.

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.utils.yaml_utils import load_yaml

def generate_syllabus_markdown(manifest: dict[str, Any]) -> str:
    """Generate Markdown content for the syllabus."""
    book = manifest.get("book", {})
    academic = manifest.get("academic", {})
    structure = manifest.get("structure", {})
    chapters = structure.get("chapters", [])
    
    # Create a mapping for quick lookup
    chapter_map = {ch.get("id"): ch.get("title") for ch in chapters if ch.get("id")}
    
    lines = [
        f"# {academic.get('course_name', book.get('title'))} — Ders İzlence Formu (Syllabus)",
        "",
        "## 1. Dersin Künyesi",
        "",
        f"- **Ders Kodu:** {academic.get('course_code', '—')}",
        f"- **Ders Adı:** {academic.get('course_name', '—')}",
        f"- **AKTS Kredisi:** {academic.get('ects_credits', '—')}",
        f"- **Kitap Referansı:** {book.get('title', '—')} ({book.get('author', '—')})",
        f"- **Yıl:** {book.get('year', '—')}",
        "",
        "## 2. Dersin Amacı ve Öğrenme Çıktıları",
        "",
        "### Dersin Amacı",
        "Bu ders, teknik ders kitabında sunulan kavramların teorik ve uygulamalı olarak kavranmasını hedefler.",
        "",
        "### Öğrenme Çıktıları",
    ]
    
    outcomes = academic.get("learning_outcomes", [])
    if outcomes:
        for outcome in outcomes:
            lines.append(f"- {outcome}")
    else:
        lines.append("- Henüz tanımlanmamış.")
        
    lines.extend([
        "",
        "## 3. Haftalık Ders Planı",
        "",
        "| Hafta | Konu / Bölüm |",
        "|---|---|",
    ])
    
    mapping = academic.get("weekly_schedule_mapping", {})
    if mapping:
        # Sort by key if possible (e.g. "Hafta 01", "Hafta 02" or "1", "2")
        # For simplicity, we'll iterate through items
        for week, chapter_id in sorted(mapping.items()):
            title = chapter_map.get(chapter_id, "—")
            lines.append(f"| {week} | {title} (`{chapter_id}`) |")
    else:
        # Fallback to chapter list if no mapping
        for i, ch in enumerate(chapters, 1):
            lines.append(f"| Hafta {i:02d} | {ch.get('title')} (`{ch.get('id')}`) |")
            
    lines.extend([
        "",
        "## 4. Değerlendirme Sistemi",
        "",
        "| Etkinlik | Ağırlık (%) |",
        "|---|---:|",
        "| Ara Sınav (Vize) | 40 |",
        "| Genel Sınav (Final) | 60 |",
        "| **Toplam** | **100** |",
        "",
        "---",
        f"*Bu belge Parametric Computer Book Factory tarafından otomatik olarak üretilmiştir.*"
    ])
    
    return "\n".join(lines)

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Academic Syllabus from BookFactory manifest.")
    parser.add_argument("--manifest", required=True, help="Path to book_manifest.yaml")
    parser.add_argument("--output", required=True, help="Output Markdown file path (e.g. Syllabus.md)")
    
    args = parser.parse_args(argv)
    
    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"Error: Manifest not found at {manifest_path}", file=sys.stderr)
        return 1
        
    try:
        manifest = load_yaml(manifest_path)
    except Exception as e:
        print(f"Error loading manifest: {e}", file=sys.stderr)
        return 1
        
    if "academic" not in manifest:
        print("Warning: 'academic' block missing in manifest. Using defaults.", file=sys.stderr)
        
    content = generate_syllabus_markdown(manifest)
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    
    print(f"Success: Syllabus generated at {output_path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
