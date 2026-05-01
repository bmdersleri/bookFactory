#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a QR manifest from a code manifest.

Purpose:
- Convert CODE_META/GitHub/code manifest outputs into a QR generation manifest.
- Support dual QR strategy:
  1. source QR: direct source code URL
  2. page QR: explanatory code page URL

Accepted input shapes:
  codes: [...]
  code_entries: [...]
  entries: [...]
  code_manifest:
    entries: [...]

Each code entry may include:
  id, code_id, chapter_id, title, file,
  github_source_url / source_url / raw_url,
  github_page_url / page_url / explanation_url,
  qr: dual | source | page | none

Usage:
  python build_qr_manifest_from_code_manifest.py \
    --code-manifest examples/code/code_manifest_example.yaml \
    --output build/qr_manifest.yaml
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Any

from tools.utils.yaml_utils import load_data, dump_yaml


def get_code_entries(data: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("items", "codes", "code_entries", "entries"):
        if isinstance(data.get(key), list):
            return [x for x in data[key] if isinstance(x, dict)]
    cm = data.get("code_manifest")
    if isinstance(cm, dict):
        for key in ("codes", "entries"):
            if isinstance(cm.get(key), list):
                return [x for x in cm[key] if isinstance(x, dict)]
    return []


def slug(value: str) -> str:
    value = value.strip().lower()
    trans = str.maketrans({"ı": "i", "ğ": "g", "ü": "u", "ş": "s", "ö": "o", "ç": "c",
                           "İ": "i", "Ğ": "g", "Ü": "u", "Ş": "s", "Ö": "o", "Ç": "c"})
    value = value.translate(trans)
    value = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in value)
    while "__" in value:
        value = value.replace("__", "_")
    return value.strip("_") or "item"


def first_nonempty(entry: dict[str, Any], keys: list[str]) -> str:
    for key in keys:
        value = entry.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def build_entries(codes: list[dict[str, Any]], output_prefix: str, strict_url: bool = False) -> tuple[list[dict[str, str]], list[str]]:
    qr_entries: list[dict[str, str]] = []
    warnings: list[str] = []

    for idx, code in enumerate(codes, start=1):
        code_id = first_nonempty(code, ["id", "code_id"]) or f"code_{idx:03d}"
        code_id = slug(code_id)
        title = first_nonempty(code, ["title", "file", "name"]) or code_id
        qr_policy = (first_nonempty(code, ["qr", "qr_policy"]) or "dual").lower()

        if qr_policy in {"none", "false", "no", "skip"}:
            continue

        source_url = first_nonempty(code, ["github_source_url", "source_url", "raw_url", "url_source"])
        page_url = first_nonempty(code, ["github_page_url", "page_url", "explanation_url", "url_page"])

        if qr_policy in {"dual", "source"} and not source_url:
            warnings.append(f"{code_id}: missing source URL for qr policy {qr_policy}")
        if qr_policy in {"dual", "page"} and not page_url:
            warnings.append(f"{code_id}: missing page URL for qr policy {qr_policy}")

        if qr_policy in {"dual", "source"} and source_url:
            qr_entries.append({
                "id": f"{code_id}_source",
                "title": f"{title} source",
                "url": source_url,
                "output": f"{output_prefix}/{code_id}_source.png",
                "kind": "source",
                "code_id": code_id,
            })

        if qr_policy in {"dual", "page"} and page_url:
            qr_entries.append({
                "id": f"{code_id}_page",
                "title": f"{title} page",
                "url": page_url,
                "output": f"{output_prefix}/{code_id}_page.png",
                "kind": "page",
                "code_id": code_id,
            })

    return qr_entries, warnings


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Build QR manifest from code manifest.")
    ap.add_argument("--code-manifest", required=True, help="Input code manifest YAML/JSON")
    ap.add_argument("--output", required=True, help="Output QR manifest YAML")
    ap.add_argument("--output-prefix", default="assets/auto/qr", help="Output path prefix used inside QR entries")
    ap.add_argument("--fail-on-empty", action="store_true", help="Return non-zero when no QR entries can be produced")
    ap.add_argument("--strict-url", action="store_true", help="Return non-zero if a requested source/page QR URL is missing")
    args = ap.parse_args(argv)

    input_path = Path(args.code_manifest)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"[ERROR] Code manifest not found: {input_path}", file=sys.stderr)
        return 1

    data = load_data(input_path)
    codes = get_code_entries(data)

    if not codes:
        print(f"[WARN] No code entries found in: {input_path}")

    entries, warnings = build_entries(codes, output_prefix=args.output_prefix, strict_url=args.strict_url)

    result = {
        "qr": {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "source_code_manifest": str(input_path),
            "entries": entries,
            "warnings": warnings,
        }
    }

    dump_yaml(result, output_path)

    print(f"[OK] QR manifest written: {output_path}")
    print(f"[OK] QR entries: {len(entries)}")
    if warnings:
        for warning in warnings:
            print(f"[WARN] {warning}")

    if args.strict_url and warnings:
        return 3

    if args.fail_on_empty and not entries:
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
