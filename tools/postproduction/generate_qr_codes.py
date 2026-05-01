#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR Code Generator for Parametric Computer Book Factory.

Purpose:
- Generate QR PNG files from a manifest-driven URL list.
- Keep QR generation separate from Markdown/DOCX formatting.
- Produce a reproducible QR report for post-production audits.

Supported manifest formats: YAML or JSON.

Example YAML:

qr:
  entries:
    - id: "decision_structures_code01_source"
      title: "Decision Structures Code 01 Source"
      url: "https://github.com/example/book/code/decision_structures/code01/BasicIfExample.java"
      output: "assets/auto/qr/decision_structures_code01_source.png"
    - id: "decision_structures_code01_page"
      title: "Decision Structures Code 01 Page"
      url: "https://example.github.io/book/tr/decision_structures/code01.html"
      output: "assets/auto/qr/decision_structures_code01_page.png"

Alternative top-level shape:

entries:
  - id: "..."
    url: "..."
    output: "..."

Usage:
    python generate_qr_codes.py --manifest build/qr_manifest.yaml --output-dir assets/auto/qr
    python generate_qr_codes.py --manifest build/qr_manifest.yaml --report build/reports/qr_generation_report.md
    python generate_qr_codes.py --manifest build/qr_manifest.yaml --dry-run

Notes:
- Manual editing of QR matrix images is not recommended because it may break scan reliability.
- QR labels, captions and page placement should be handled outside the QR matrix image.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Any

from tools.utils.yaml_utils import load_data


def load_manifest(path: Path) -> dict[str, Any]:
    return load_data(path)


def get_entries(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    if isinstance(manifest.get("entries"), list):
        return manifest["entries"]
    qr = manifest.get("qr") or {}
    if isinstance(qr.get("entries"), list):
        return qr["entries"]
    if isinstance(qr.get("codes"), list):
        return qr["codes"]
    if isinstance(manifest.get("qr_codes"), list):
        return manifest["qr_codes"]
    return []


def sanitize_filename(value: str) -> str:
    value = value.strip().lower()
    value = value.replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")
    value = value.replace("İ", "i").replace("Ğ", "g").replace("Ü", "u").replace("Ş", "s").replace("Ö", "o").replace("Ç", "c")
    value = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in value)
    while "__" in value:
        value = value.replace("__", "_")
    return value.strip("_") or "qr_code"


def resolve_path(base: Path, value: str | None) -> Path | None:
    if not value:
        return None
    p = Path(value)
    return p if p.is_absolute() else (base / p).resolve()


def make_qr(url: str, output: Path, box_size: int, border: int, fill_color: str, back_color: str) -> None:
    try:
        import qrcode  # type: ignore
    except Exception as exc:
        raise RuntimeError("qrcode[pil] is required. Install with: pip install qrcode[pil]") from exc

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    output.parent.mkdir(parents=True, exist_ok=True)
    img.save(output)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate QR PNG files from a QR manifest.")
    ap.add_argument("--manifest", required=True, help="QR manifest YAML/JSON file")
    ap.add_argument("--output-dir", default=None, help="Default output directory for QR PNG files")
    ap.add_argument("--report", default=None, help="Markdown report path")
    ap.add_argument("--base-dir", default=".", help="Base directory for relative paths")
    ap.add_argument("--force", action="store_true", help="Overwrite existing QR PNG files")
    ap.add_argument("--dry-run", action="store_true", help="Report actions without writing files")
    ap.add_argument("--box-size", type=int, default=10, help="QR box size in pixels")
    ap.add_argument("--border", type=int, default=4, help="QR border size")
    ap.add_argument("--fill-color", default="black", help="QR fill color")
    ap.add_argument("--back-color", default="white", help="QR background color")
    args = ap.parse_args(argv)

    base = Path(args.base_dir).resolve()
    manifest_path = resolve_path(base, args.manifest)
    if not manifest_path or not manifest_path.exists():
        print(f"[ERROR] QR manifest not found: {args.manifest} -> {manifest_path}", file=sys.stderr)
        return 1

    manifest = load_manifest(manifest_path)
    entries = get_entries(manifest)

    if not entries:
        print(f"[WARN] No QR entries found in manifest: {manifest_path}")
        if args.report and not args.dry_run:
            report_path = resolve_path(base, args.report)
            if report_path:
                report_path.parent.mkdir(parents=True, exist_ok=True)
                report_path.write_text(
                    "# QR Generation Report\n\n"
                    f"Date: {datetime.now().isoformat(timespec='seconds')}\n\n"
                    f"Manifest: `{manifest_path}`\n\n"
                    "No QR entries found.\n",
                    encoding="utf-8",
                )
        return 0

    default_output_dir = resolve_path(base, args.output_dir) if args.output_dir else None

    rows: list[dict[str, Any]] = []
    errors = 0
    written = 0
    skipped = 0

    for idx, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            rows.append({"id": f"entry_{idx}", "status": "ERROR", "url": "", "output": "", "note": "Entry is not an object"})
            errors += 1
            continue

        qid = str(entry.get("id") or entry.get("qr_id") or f"qr_{idx:03d}")
        url = str(entry.get("url") or entry.get("target") or "").strip()
        if not url:
            rows.append({"id": qid, "status": "ERROR", "url": "", "output": "", "note": "Missing URL"})
            errors += 1
            continue

        output_value = entry.get("output") or entry.get("path")
        if output_value:
            output = resolve_path(base, str(output_value))
        elif default_output_dir:
            output = default_output_dir / f"{sanitize_filename(qid)}.png"
        else:
            output = base / "assets" / "auto" / "qr" / f"{sanitize_filename(qid)}.png"

        assert output is not None

        if output.exists() and not args.force:
            skipped += 1
            status = "SKIPPED"
            note = "Already exists"
        else:
            status = "DRY-RUN" if args.dry_run else "WRITTEN"
            note = ""
            if not args.dry_run:
                try:
                    make_qr(
                        url=url,
                        output=output,
                        box_size=int(entry.get("box_size", args.box_size)),
                        border=int(entry.get("border", args.border)),
                        fill_color=str(entry.get("fill_color", args.fill_color)),
                        back_color=str(entry.get("back_color", args.back_color)),
                    )
                    written += 1
                except Exception as exc:
                    status = "ERROR"
                    note = str(exc)
                    errors += 1

        rows.append({"id": qid, "status": status, "url": url, "output": str(output), "note": note})
        print(f"[{status}] {qid} -> {output}")

    report_path = resolve_path(base, args.report) if args.report else None
    if report_path and not args.dry_run:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# QR Generation Report",
            "",
            f"Date: {datetime.now().isoformat(timespec='seconds')}",
            f"Manifest: `{manifest_path}`",
            "",
            "## Summary",
            "",
            f"- Entries: {len(entries)}",
            f"- Written: {written}",
            f"- Skipped: {skipped}",
            f"- Errors: {errors}",
            "",
            "## Details",
            "",
            "| ID | Status | Output | URL | Note |",
            "|---|---|---|---|---|",
        ]
        for row in rows:
            lines.append(
                f"| `{row['id']}` | {row['status']} | `{row['output']}` | {row['url']} | {row['note']} |"
            )
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Report: {report_path}")

    return 0 if errors == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
