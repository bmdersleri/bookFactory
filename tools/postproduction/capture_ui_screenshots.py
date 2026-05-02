#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automatic UI Screenshot Manager for BookFactory.

Scans the code manifest for 'captures_screenshot' fields, executes them 
via adapters, and validates against [SCREENSHOT:id] markers in Markdown.
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

from tools.code.language_adapters import JavaAdapter, JavaScriptAdapter, PythonAdapter
from tools.code.language_adapters.flutter_adapter import FlutterAdapter
from tools.utils.yaml_utils import load_data

SCREENSHOT_RE = re.compile(r"\[SCREENSHOT:(.*?)\]")

def load_manifest(path: Path) -> dict[str, Any]:
    try:
        return load_data(path)
    except Exception as exc:
        raise SystemExit(f"Cannot load code manifest {path}: {exc}") from exc

def scan_markdown_for_markers(chapters_dir: Path) -> set[str]:
    """Finds all [SCREENSHOT:id] markers in markdown files."""
    markers = set()
    for md_file in chapters_dir.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        for match in SCREENSHOT_RE.finditer(content):
            markers.add(match.group(1))
    return markers

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Capture UI screenshots from CODE_META blocks.")
    parser.add_argument("--manifest", type=Path, default=Path("build/code_manifest.json"))
    parser.add_argument("--package-root", type=Path, default=Path.cwd())
    parser.add_argument("--chapters-dir", type=Path, default=Path("chapters"))
    parser.add_argument("--timeout-sec", type=int, default=120)
    
    args = parser.parse_args(argv)
    
    package_root = args.package_root.resolve()
    manifest_path = package_root / args.manifest
    chapters_dir = package_root / args.chapters_dir
    
    manifest = load_manifest(manifest_path)
    items = manifest.get("items", [])
    
    # Filter items that capture screenshots
    screenshot_items = [item for item in items if item.get("captures_screenshot")]
    
    if not screenshot_items:
        print("No code blocks found with 'captures_screenshot'.")
        return 0
        
    adapters = {
        "python": PythonAdapter(default_timeout=args.timeout_sec),
        "flutter": FlutterAdapter(default_timeout=args.timeout_sec),
        "javascript": JavaScriptAdapter(default_timeout=args.timeout_sec),
        "java": JavaAdapter(default_timeout=args.timeout_sec),
    }

    print(f"Found {len(screenshot_items)} code blocks to capture screenshots.")
    
    results = []
    for item in screenshot_items:
        lang = str(item.get("language", "")).lower()
        adapter = adapters.get(lang)
        if not adapter:
            print(f"Skipping {item['id']}: No adapter for language '{lang}'")
            continue
            
        print(f"Capturing screenshot for {item['id']} ({lang})...")
        res = adapter.run(item, package_root)
        results.append(res)
        
        if res.get("status") == "passed":
            print(f"  [OK] {item['captures_screenshot']}.png")
        else:
            print(f"  [FAILED] {res.get('failure_reason')}")

    # Validation against Markdown markers
    markers = scan_markdown_for_markers(chapters_dir)
    captured = {item["captures_screenshot"] for item in screenshot_items}
    
    print("\n--- Screenshot Validation ---")
    missing_in_code = markers - captured
    unused_in_code = captured - markers
    
    if missing_in_code:
        print(f"WARNING: Markers in Markdown but not in CODE_META: {', '.join(missing_in_code)}")
    if unused_in_code:
        print(f"INFO: Captured but no marker found in Markdown: {', '.join(unused_in_code)}")
        
    if not missing_in_code:
        print("All [SCREENSHOT:id] markers are covered by CODE_META blocks.")

    failed_count = sum(1 for r in results if r.get("status") != "passed")
    return 1 if failed_count > 0 else 0

if __name__ == "__main__":
    sys.exit(main())
