#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code-Text Alignment Checker v3.7.

Analyzes markdown prose to ensure that mentioned variables and functions 
actually exist in the accompanying CODE_META blocks.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

def extract_variables_from_code(code: str, language: str) -> set[str]:
    """Simple regex-based variable extraction."""
    vars = set()
    if language in ["python", "javascript", "js"]:
        # Match assignments and function defs
        vars.update(re.findall(r"(\b[a-zA-Z_][a-zA-Z0-9_]*)\s*=", code))
        vars.update(re.findall(r"def\s+(\b[a-zA-Z_][a-zA-Z0-9_]*)", code))
        vars.update(re.findall(r"function\s+(\b[a-zA-Z_][a-zA-Z0-9_]*)", code))
        vars.update(re.findall(r"const\s+(\b[a-zA-Z_][a-zA-Z0-9_]*)", code))
        vars.update(re.findall(r"let\s+(\b[a-zA-Z_][a-zA-Z0-9_]*)", code))
    elif language == "java":
        vars.update(re.findall(r"(?:public|private|protected|static|\s)\s+[\w<>,]+\s+(\b[a-zA-Z_][a-zA-Z0-9_]*)\s*[:;=]", code))
        vars.update(re.findall(r"(\b[a-zA-Z_][a-zA-Z0-9_]*)\s*\(", code)) # methods
    return vars

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check alignment between prose and code.")
    parser.add_argument("--chapter", required=True, help="Markdown file")
    
    args = parser.parse_args(argv)
    path = Path(args.chapter)
    if not path.exists():
        print(f"Error: {path} not found")
        return 1
        
    content = path.read_text(encoding="utf-8")
    
    # 1. Extract all CODE_META and their code
    blocks = re.findall(r"<!--\s*CODE_META[\s\S]*?language:\s*([a-z]+)[\s\S]*?-->[\s\S]*?```[a-z]*\n([\s\S]*?)\n```", content)
    
    all_code_vars = set()
    for lang, code in blocks:
        all_code_vars.update(extract_variables_from_code(code, lang))
        
    # 2. Find variables mentioned in prose (within backticks)
    prose_mentions = set(re.findall(r"`(\b[a-zA-Z_][a-zA-Z0-9_]*)`", content))
    
    # 3. Compare
    # We only care about mentions that LOOK like they should be in code
    # This is a heuristic. Filter out very short ones or common words.
    potential_mismatches = []
    for mention in prose_mentions:
        if mention in ["id", "name", "email", "tr", "en"]: continue # skip common metadata
        if len(mention) < 3: continue
        
        if mention not in all_code_vars:
            potential_mismatches.append(mention)
            
    if potential_mismatches:
        print(f"WARNING: Mentions in prose not found in code blocks: {', '.join(potential_mismatches)}")
        # This tool is informational for now, doesn't fail the build
    else:
        print("ALIGNMENT: PASS")
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
