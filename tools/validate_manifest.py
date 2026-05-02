#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate a Parametric Computer Book Factory book manifest.

This is a pragmatic validator, not a full JSON Schema implementation.
It checks the required fields needed by the LLM prompt generation and
post-production pipeline.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bookfactory_studio.core import normalize_manifest  # noqa: E402
from bookfactory_studio.core import validate_manifest as validate_studio_manifest  # noqa: E402
from tools.utils.yaml_utils import load_yaml  # noqa: E402


def validate_manifest(data: dict) -> tuple[list[str], list[str]]:
    result = validate_studio_manifest(normalize_manifest(data))
    return list(result.get("errors") or []), list(result.get("warnings") or [])


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate a book_manifest.yaml file.")
    parser.add_argument("manifest", help="Path to book manifest YAML")
    parser.add_argument("--report", help="Optional Markdown report output")
    args = parser.parse_args(argv)

    path = Path(args.manifest)
    data = load_yaml(path)
    errors, warnings = validate_manifest(data)

    lines = ["# Manifest Validation Report", "", f"Manifest: `{path}`", ""]
    if errors:
        lines.append("## Errors")
        lines.extend(f"- {e}" for e in errors)
    else:
        lines.append("## Errors\n\nNo errors found.")

    lines.append("")
    if warnings:
        lines.append("## Warnings")
        lines.extend(f"- {w}" for w in warnings)
    else:
        lines.append("## Warnings\n\nNo warnings found.")

    output = "\n".join(lines) + "\n"
    print(output)

    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(output, encoding="utf-8")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
