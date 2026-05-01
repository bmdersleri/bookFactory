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
import re
import sys

from tools.utils.yaml_utils import load_yaml


SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9_/-]*[a-z0-9]$|^[a-z0-9]$")



def get(data: dict, dotted: str):
    cur = data
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def validate_manifest(data: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    required = [
        "book.book_id",
        "book.title",
        "language.primary_language",
        "language.output_languages",
        "audience.primary",
        "chapters",
    ]

    for field in required:
        value = get(data, field)
        if value in (None, "", [], {}):
            errors.append(f"Missing required field: {field}")

    book_id = get(data, "book.book_id")
    if isinstance(book_id, str) and not SLUG_RE.match(book_id):
        errors.append("book.book_id must be a stable English slug, e.g. java_fundamentals")

    chapters = data.get("chapters") or []
    if not isinstance(chapters, list):
        errors.append("chapters must be a list")
        chapters = []

    seen = set()
    for idx, chapter in enumerate(chapters, start=1):
        if not isinstance(chapter, dict):
            errors.append(f"chapters[{idx}] must be a mapping")
            continue

        chapter_id = chapter.get("chapter_id")
        title = chapter.get("title")
        if not chapter_id:
            errors.append(f"chapters[{idx}] missing chapter_id")
        elif chapter_id in seen:
            errors.append(f"Duplicate chapter_id: {chapter_id}")
        else:
            seen.add(chapter_id)
            if not SLUG_RE.match(str(chapter_id)):
                errors.append(f"chapter_id must be an English slug: {chapter_id}")

        if not title:
            errors.append(f"chapters[{idx}] missing title")

        if not chapter.get("purpose"):
            warnings.append(f"chapters[{idx}] {chapter_id or ''} missing purpose")

    approval = data.get("approval_gates", {})
    if approval:
        allowed = {"required", "optional", "disabled"}
        for key, value in approval.items():
            if isinstance(value, str):
                if value not in allowed:
                    warnings.append(f"approval_gates.{key} should be one of {sorted(allowed)}")
            elif isinstance(value, dict):
                if "required" not in value:
                    warnings.append(f"approval_gates.{key} has no 'required' field")
            else:
                warnings.append(f"approval_gates.{key} should be a string or mapping")

    return errors, warnings


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
