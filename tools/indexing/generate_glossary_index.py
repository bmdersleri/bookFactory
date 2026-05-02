#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Glossary and Index Generator v3.4 for BookFactory.

This tool merges terms from the manifest and automatically scans chapters 
to build a cross-referenced index.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.utils.yaml_utils import load_yaml

def slugify(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def scan_chapters_for_terms(chapters: list[dict], terms: list[str], package_root: Path) -> dict[str, list[dict]]:
    """Scans chapter files for term occurrences."""
    results = {term: [] for term in terms}
    
    for ch in chapters:
        path_val = ch.get("path") or ch.get("file")
        if not path_val: continue
        
        ch_path = package_root / "chapters" / path_val
        if not ch_path.exists(): continue
        
        content = ch_path.read_text(encoding="utf-8").lower()
        for term in terms:
            count = content.count(term.lower())
            if count > 0:
                results[term].append({
                    "id": ch.get("id"),
                    "title": ch.get("title"),
                    "count": count
                })
    return results

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Glossary and Index.")
    parser.add_argument("--manifest", required=True, help="Path to book_manifest.yaml")
    parser.add_argument("--output-dir", default="exports/indexing", help="Output directory")
    
    args = parser.parse_args(argv)
    
    m_path = Path(args.manifest)
    manifest = load_yaml(m_path)
    package_root = m_path.parent.parent # Assuming manifests/book_manifest.yaml
    
    glossary = manifest.get("glossary", [])
    chapters = manifest.get("structure", {}).get("chapters", [])
    
    if not glossary:
        print("No glossary terms found in manifest.")
        return 0
        
    terms = [item["term"] for item in glossary]
    occurrences = scan_chapters_for_terms(chapters, terms, package_root)
    
    # 1. Build Glossary.md
    gloss_lines = ["# Terimler Sözlüğü", ""]
    for item in sorted(glossary, key=lambda x: x["term"]):
        gloss_lines.append(f"### {item['term']}")
        gloss_lines.append(f"{item['definition']}")
        if item.get("category"):
            gloss_lines.append(f"\n*Kategori: {item['category']}*")
        gloss_lines.append("")
        
    # 2. Build Index.md
    index_lines = ["# Dizin", "", "Bu dizin terimlerin geçtiği bölümleri listeler.", ""]
    current_letter = ""
    for term in sorted(terms):
        letter = term[0].upper()
        if letter != current_letter:
            current_letter = letter
            index_lines.append(f"## {current_letter}")
            
        refs = occurrences.get(term, [])
        ref_text = ", ".join([f"{r['title']} ({r['count']})" for r in refs]) if refs else "Referans bulunamadı"
        index_lines.append(f"- **{term}**: {ref_text}")
        
    out_dir = Path(args.output_dir)
    if not out_dir.is_absolute():
        out_dir = package_root / out_dir
        
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "Glossary.md").write_text("\n".join(gloss_lines), encoding="utf-8")
    (out_dir / "Index.md").write_text("\n".join(index_lines), encoding="utf-8")
    
    print(f"Success: Glossary and Index generated in {out_dir}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
