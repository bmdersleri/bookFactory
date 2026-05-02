#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Semantic Consistency Checker v3.5.

Generates a specialized LLM prompt to identify contradictions 
between the current chapter and previously indexed book context.
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

def generate_consistency_audit_prompt(chapter_path: Path, context: str, target_lang: str = "tr") -> str:
    content = chapter_path.read_text(encoding="utf-8")
    
    prompt = f"""You are an expert Technical Editor. Your task is to perform a SEMANTIC CONSISTENCY AUDIT.
You must compare the [NEW CHAPTER] below against the [COLLECTED CONTEXT] from previous chapters.

GOAL: Identify any contradictions in terminology, technical definitions, code styles, or data models.

--- COLLECTED CONTEXT (FROM PREVIOUS CHAPTERS) ---
{context}

--- NEW CHAPTER TO AUDIT ---
{content}

--- AUDIT REQUIREMENTS ---
Please report the following in {target_lang}:
1. Terminology Conflicts: (e.g., Calling a concept 'X' when it was previously 'Y')
2. Technical Contradictions: (e.g., A class attribute that changed its name or type)
3. Stylistic Drift: (e.g., Changing from functional to class-based examples without explanation)

If no conflicts are found, state "CONSISTENCY: PASS".
"""
    return prompt

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Semantic Consistency Audit Prompt.")
    parser.add_argument("--chapter-id", required=True)
    parser.add_argument("--chapter-file", required=True)
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", default="build/consistency_audit_prompt.md")
    
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    ch_path = Path(args.chapter_file)
    if not ch_path.is_absolute():
        ch_path = root / ch_path
        
    if not ch_path.exists():
        print(f"Error: Chapter file not found: {ch_path}")
        return 1
        
    try:
        memory = BookContextMemory(root)
        # Search for context using the chapter's own content as query
        # Using first 500 chars as a summary query
        content_preview = ch_path.read_text(encoding="utf-8")[:500]
        context = memory.retrieve_context(content_preview, n_results=5)
        
        prompt = generate_consistency_audit_prompt(ch_path, context)
        
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(prompt, encoding="utf-8")
        
        print(f"Success: Consistency audit prompt generated at {out_path}")
    except Exception as e:
        print(f"Error: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
