#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dual-Agent Editor Review Generator v3.7.

Generates a specialized LLM prompt for a technical editor to review 
a chapter's content and pedagogical quality.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.memory.rag_manager import BookContextMemory
from tools.utils.yaml_utils import load_yaml

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Editor Review Prompt.")
    parser.add_argument("--chapter-id", required=True)
    parser.add_argument("--chapter-file", required=True)
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", default="build/editor_review_prompt.md")
    
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    ch_path = Path(args.chapter_file)
    if not ch_path.is_absolute():
        ch_path = root / ch_path
        
    if not ch_path.exists():
        print(f"Error: Chapter file not found: {ch_path}")
        return 1
        
    try:
        manifest_path = root / "book_manifest.yaml"
        if not manifest_path.exists():
            manifest_path = root / "manifests" / "book_manifest.yaml"
            
        manifest = load_yaml(manifest_path) if manifest_path.exists() else {}
        style_profile = manifest.get("language", {}).get("style_profile", "Academic")
        
        memory = BookContextMemory(root)
        content = ch_path.read_text(encoding="utf-8")
        
        # Retrieve context relevant to the chapter
        context = memory.retrieve_context(content[:500], n_results=5)
        
        template_path = ROOT / "core" / "16_editor_review_prompt.md"
        template = template_path.read_text(encoding="utf-8")
        
        final_prompt = template.format(
            chapter_content=content,
            retrieved_context=context,
            language=manifest.get("language", {"style_profile": style_profile})
        )
        
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(final_prompt, encoding="utf-8")
        
        print(f"Success: Editor review prompt generated at {out_path}")
    except Exception as e:
        print(f"Error: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
