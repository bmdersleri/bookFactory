#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate a BookFactory CODE_META/code_manifest JSON file."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from tools.utils.yaml_utils import load_data

REQUIRED = ["id", "chapter_id", "language", "file", "code_path", "test"]
SUPPORTED_TESTS = {"none", "compile", "compile_run", "compile_run_assert"}
SUPPORTED_LANGUAGES = {"java", "python", "javascript", "text", "bash"}


def load_manifest(path: Path) -> dict[str, Any]:
    return load_data(path)



def validate_item(item: dict[str, Any], index: int, package_root: Path) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED:
        if field not in item or item[field] in (None, ""):
            errors.append(f"items[{index}] missing required field: {field}")
    language = str(item.get("language", "")).lower()
    if language and language not in SUPPORTED_LANGUAGES:
        errors.append(f"items[{index}] unsupported language: {language}")
    test = str(item.get("test", "none"))
    if test not in SUPPORTED_TESTS:
        errors.append(f"items[{index}] unsupported test mode: {test}")
    code_path = item.get("code_path")
    if code_path:
        resolved = Path(code_path)
        if not resolved.is_absolute():
            resolved = package_root / resolved
        if not resolved.exists():
            errors.append(f"items[{index}] code_path does not exist: {code_path}")
    if language == "java" and test != "none":
        if not str(item.get("file", "")).endswith(".java"):
            errors.append(f"items[{index}] Java item file should end with .java")
        if not item.get("main_class") and test in {"compile_run", "compile_run_assert"}:
            errors.append(f"items[{index}] Java run test requires main_class")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate CODE_META/code manifest.")
    parser.add_argument("manifest", type=Path, help="code_manifest.json or YAML")
    parser.add_argument("--package-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)

    manifest = load_manifest(args.manifest)
    items = manifest.get("items", [])
    if not isinstance(items, list):
        print("[ERROR] manifest.items must be a list", file=sys.stderr)
        return 1
    errors: list[str] = []
    ids: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"items[{index}] must be an object")
            continue
        item_id = str(item.get("id", ""))
        if item_id in ids:
            errors.append(f"items[{index}] duplicate id: {item_id}")
        ids.add(item_id)
        errors.extend(validate_item(item, index, args.package_root.resolve()))

    print(f"CODE_META items checked: {len(items)}")
    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("CODE_META validation: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
