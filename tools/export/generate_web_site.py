#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Digital Twin Web Site Generator for BookFactory.

Converts the manifest and markdown chapters into a structured MkDocs documentation site.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.utils.yaml_utils import load_yaml, dump_yaml

def generate_mkdocs_config(manifest: dict[str, Any], docs_dir: str) -> dict[str, Any]:
    book = manifest.get("book", {})
    chapters = manifest.get("structure", {}).get("chapters", [])
    
    nav = []
    nav.append({"Giriş": "index.md"})
    
    chapter_nav = []
    for i, ch in enumerate(chapters, 1):
        title = ch.get("title", f"Bölüm {i}")
        file = ch.get("file") or ch.get("path")
        if file:
            chapter_nav.append({f"{i}. {title}": f"chapters/{file}"})
    
    if chapter_nav:
        nav.append({"Bölümler": chapter_nav})
        
    # Add Academic/Indexing if they exist in output
    nav.append({"Syllabus": "academic/Syllabus.md"})
    nav.append({"Terimler Sözlüğü": "indexing/Glossary.md"})
    nav.append({"Dizin": "indexing/Index.md"})

    config = {
        "site_name": book.get("title", "BookFactory Kitabı"),
        "site_author": book.get("author", ""),
        "theme": {
            "name": "material",
            "language": "tr",
            "palette": {
                "primary": "indigo",
                "accent": "indigo"
            },
            "features": [
                "navigation.tabs",
                "navigation.sections",
                "toc.integrate"
            ]
        },
        "nav": nav,
        "markdown_extensions": [
            "admonition",
            "codehilite",
            "extra",
            "pymdownx.superfences"
        ]
    }
    return config

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate MkDocs site for the book.")
    parser.add_argument("--manifest", required=True, help="Path to book_manifest.yaml")
    parser.add_argument("--output-dir", default="dist/web_site", help="Output directory")
    
    args = parser.parse_args(argv)
    m_path = Path(args.manifest).resolve()
    package_root = m_path.parent.parent
    manifest = load_yaml(m_path)
    
    out_dir = Path(args.output_dir)
    if not out_dir.is_absolute():
        out_dir = package_root / out_dir
        
    docs_dir = out_dir / "docs"
    
    # 1. Prepare directory
    if out_dir.exists():
        shutil.rmtree(out_dir)
    docs_dir.mkdir(parents=True)
    
    # 2. Copy Chapters
    chapters_src = package_root / "chapters"
    if chapters_src.exists():
        shutil.copytree(chapters_src, docs_dir / "chapters", dirs_exist_ok=True)
        
    # 3. Copy Assets
    assets_src = package_root / "assets"
    if assets_src.exists():
        shutil.copytree(assets_src, docs_dir / "assets", dirs_exist_ok=True)

    # 4. Copy Syllabus and Indexing if they exist
    for sub in ["academic", "indexing"]:
        src = package_root / "exports" / sub
        if src.exists():
            shutil.copytree(src, docs_dir / sub, dirs_exist_ok=True)
            
    # 5. Create landing page (index.md)
    book = manifest.get("book", {})
    index_md = f"""# {book.get('title', 'Kitap')}
## {book.get('subtitle', '')}

**Yazar:** {book.get('author', '')}
**Yıl:** {book.get('year', '')}

Bu web sitesi, kitabın dijital ikizi (Digital Twin) olarak BookFactory tarafından otomatik olarak üretilmiştir.
"""
    (docs_dir / "index.md").write_text(index_md, encoding="utf-8")
    
    # 6. Generate mkdocs.yml
    mkdocs_cfg = generate_mkdocs_config(manifest, "docs")
    dump_yaml(mkdocs_cfg, out_dir / "mkdocs.yml")
    
    print(f"Success: Web site source generated in {out_dir}")
    print(f"Run 'mkdocs serve' in {out_dir} to preview or 'mkdocs build' to generate static HTML.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
