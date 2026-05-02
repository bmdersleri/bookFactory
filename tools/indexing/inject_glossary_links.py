#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart Glossary Linker v3.7.

Automatically finds glossary terms in markdown files and adds 
reference links or markers.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.utils.yaml_utils import load_yaml

def inject_links(content: str, terms: list[str]) -> str:
    """Injects markdown links for glossary terms."""
    # We only want to link the FIRST occurrence of each term per chapter 
    # to avoid clutter.
    new_content = content
    for term in sorted(terms, key=len, reverse=True): # reverse by length to avoid partial matches
        # Skip if already linked
        if f"[{term}]" in new_content: continue
        
        # Regex for term not inside another link or backticks
        pattern = re.compile(rf"(?<![`\[])\b({re.escape(term)})\b(?![`\]])", re.IGNORECASE)
        
        # Replace only the first occurrence
        new_content = pattern.sub(rf"[\1](../indexing/Glossary.md#slugify(\1))", new_content, count=1)
    
    return new_content

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inject glossary links into markdown.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--chapter", required=True)
    
    args = parser.parse_args(argv)
    m_path = Path(args.manifest)
    ch_path = Path(args.chapter)
    
    if not m_path.exists() or not ch_path.exists():
        return 1
        
    manifest = load_yaml(m_path)
    glossary = manifest.get("glossary", [])
    if not glossary:
        return 0
        
    terms = [item["term"] for item in glossary]
    content = ch_path.read_text(encoding="utf-8")
    
    # In a real implementation, 'slugify' would be a real function call
    # For now, let's just mark them
    new_content = content
    for term in terms:
        # Match word boundaries, not inside backticks
        # Simple placeholder injection
        pattern = re.compile(rf"(?<![`])\b({re.escape(term)})\b(?![`])", re.IGNORECASE)
        # Marking with a specific syntax for later Pandoc filtering or similar
        new_content = pattern.sub(rf"{\1}*", new_content, count=1)
        
    ch_path.write_text(new_content, encoding="utf-8")
    print(f"Success: Glossary markers injected into {ch_path.name}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
