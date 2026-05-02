#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLI interface for BookFactory RAG Context Memory."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow importing from tools/memory/rag_manager.py
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.memory.rag_manager import BookContextMemory

def main():
    parser = argparse.ArgumentParser(description="BookFactory RAG CLI")
    parser.add_argument("--root", default=".", help="Project root directory")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Index command
    index_parser = subparsers.add_parser("index", help="Index a chapter file")
    index_parser.add_argument("--chapter-id", required=True, help="ID of the chapter")
    index_parser.add_argument("--file", required=True, help="Path to the markdown file")

    # Prompt command
    prompt_parser = subparsers.add_parser("prompt", help="Generate prompt with context")
    prompt_parser.add_argument("--query", required=True, help="Search query for context")
    prompt_parser.add_argument("--base-prompt", required=True, help="Path to the base prompt file")
    prompt_parser.add_argument("--output", required=True, help="Output file path")
    prompt_parser.add_argument("--results", type=int, default=3, help="Number of context results")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    try:
        memory = BookContextMemory(args.root)

        if args.command == "index":
            print(f"Indexing chapter {args.chapter_id} from {args.file}...")
            memory.index_chapter(args.chapter_id, args.file)
            print("Indexing complete.")

        elif args.command == "prompt":
            print(f"Retrieving context for: {args.query}...")
            context = memory.retrieve_context(args.query, n_results=args.results)
            
            base_prompt_path = Path(args.base_prompt)
            if not base_prompt_path.exists():
                print(f"Error: Base prompt file not found: {base_prompt_path}")
                return 1
            
            base_content = base_prompt_path.read_text(encoding="utf-8")
            
            final_prompt = (
                f"{base_content}\n\n"
                "LLM İÇİN ÖNCEKİ BÖLÜMLERDEN HATIRLATMA (CONTEXT):\n"
                "--------------------------------------------------\n"
                f"{context}\n"
                "--------------------------------------------------\n"
            )
            
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(final_prompt, encoding="utf-8")
            print(f"Final prompt written to: {output_path}")

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
