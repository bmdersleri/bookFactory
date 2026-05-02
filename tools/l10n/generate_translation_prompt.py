#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BookFactory Localization (L10n) Prompt Generator.

This tool prepares a specialized prompt for an LLM to translate a technical 
markdown chapter while strictly preserving CODE_META and code syntax.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

def generate_prompt(source_file: Path, target_lang: str) -> str:
    """Wraps the source markdown in a strict translation instruction prompt."""
    if not source_file.exists():
        raise FileNotFoundError(f"Source chapter file not found: {source_file}")
        
    content = source_file.read_text(encoding="utf-8")
    
    prompt_template = f"""You are an expert technical translator specializing in Computer Engineering textbooks.
Your task is to translate the following Markdown chapter into {target_lang}.

CRITICAL RULES (STRICT STRICT STRICT):
1. DO NOT translate or modify ANY content inside `<!-- CODE_META ... -->` blocks. Keep them exactly as they are.
2. DO NOT translate variable names, class names, method names, or any logical syntax inside code blocks (```python, ```java, etc.).
3. ONLY translate the standard Markdown text, headings, list items, and code comments (e.g., lines starting with # or //).
4. Preserve all Markdown formatting, links, and image markers (e.g., [SCREENSHOT:...]).
5. Maintain an academic, pedagogical, and highly professional tone suitable for university-level engineering students.

--- SOURCE MARKDOWN TO TRANSLATE ---
{content}
"""
    return prompt_template

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate an LLM translation prompt for a BookFactory chapter.")
    parser.add_argument("--chapter-file", required=True, help="Path to the source markdown chapter file")
    parser.add_argument("--target-lang", required=True, help="Target language code (e.g., en, fr, ar)")
    parser.add_argument("--output", default="build/l10n_ready_prompt.md", help="Output path for the generated prompt")
    
    args = parser.parse_args(argv)
    
    try:
        source_path = Path(args.chapter_file)
        prompt_content = generate_prompt(source_path, args.target_lang)
        
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(prompt_content, encoding="utf-8")
        
        print(f"Success: Translation prompt for '{args.target_lang}' generated at {output_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
