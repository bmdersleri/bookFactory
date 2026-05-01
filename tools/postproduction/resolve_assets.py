#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Resolve final assets with manual override policy.

Selection priority:
1. manual asset
2. locked asset
3. auto asset

The selected asset is copied to the final asset directory, preserving relative paths.
This tool protects `assets/manual` and `assets/locked`; it never deletes them.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from datetime import datetime

from tools.utils.yaml_utils import load_yaml


ASSET_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".svg"}



def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_assets(base: Path) -> list[Path]:
    if not base.exists():
        return []
    return sorted(p for p in base.rglob("*") if p.is_file() and p.suffix.lower() in ASSET_EXTENSIONS)


def rel_candidates(paths: list[Path], base: Path) -> dict[str, Path]:
    out = {}
    for p in paths:
        out[p.relative_to(base).as_posix()] = p
    return out


def resolve_assets(auto_dir: Path, manual_dir: Path, locked_dir: Path, final_dir: Path, clean_final: bool) -> list[dict]:
    auto = rel_candidates(iter_assets(auto_dir), auto_dir)
    manual = rel_candidates(iter_assets(manual_dir), manual_dir)
    locked = rel_candidates(iter_assets(locked_dir), locked_dir)

    keys = sorted(set(auto) | set(manual) | set(locked))
    if clean_final and final_dir.exists():
        shutil.rmtree(final_dir)
    final_dir.mkdir(parents=True, exist_ok=True)

    records: list[dict] = []
    for key in keys:
        selected_source = None
        selected_path = None

        if key in manual:
            selected_source = "manual"
            selected_path = manual[key]
        elif key in locked:
            selected_source = "locked"
            selected_path = locked[key]
        elif key in auto:
            selected_source = "auto"
            selected_path = auto[key]

        if selected_path is None:
            continue

        final_path = final_dir / key
        final_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(selected_path, final_path)

        records.append({
            "asset_id": Path(key).stem,
            "relative_path": key,
            "selected_source": selected_source,
            "source_path": selected_path.as_posix(),
            "final_path": final_path.as_posix(),
            "sha256": sha256(final_path),
        })

    return records


def write_markdown_report(records: list[dict], path: Path) -> None:
    lines = [
        "# Asset Resolution Report",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "| Asset | Source | Final path |",
        "|---|---|---|",
    ]
    for rec in records:
        lines.append(f"| `{rec['relative_path']}` | {rec['selected_source']} | `{rec['final_path']}` |")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Resolve final assets using manual override policy.")
    parser.add_argument("--profile", help="Post-production profile YAML")
    parser.add_argument("--auto-dir")
    parser.add_argument("--manual-dir")
    parser.add_argument("--locked-dir")
    parser.add_argument("--final-dir")
    parser.add_argument("--report", default="build/reports/asset_resolution_report.md")
    parser.add_argument("--json-report", default="build/reports/asset_resolution_report.json")
    parser.add_argument("--clean-final", action="store_true", help="Clean final asset directory before copying")
    args = parser.parse_args(argv)

    base = Path.cwd()
    cfg = {}
    if args.profile:
        profile_path = Path(args.profile).resolve()
        profile = load_yaml(profile_path)
        project_root = profile.get("project_root") or profile.get("post_production", {}).get("project_root") or "."
        base = (profile_path.parent / project_root).resolve() if not Path(project_root).is_absolute() else Path(project_root)
        cfg = profile.get("post_production", {}).get("assets", {})

    def resolve(value: str | None, default: str) -> Path:
        raw = value or default
        p = Path(raw)
        return p if p.is_absolute() else (base / p).resolve()

    auto_dir = resolve(args.auto_dir, cfg.get("auto_dir", "assets/auto"))
    manual_dir = resolve(args.manual_dir, cfg.get("manual_dir", "assets/manual"))
    locked_dir = resolve(args.locked_dir, cfg.get("locked_dir", "assets/locked"))
    final_dir = resolve(args.final_dir, cfg.get("final_dir", "assets/final"))
    report = resolve(args.report, args.report)
    json_report = resolve(args.json_report, args.json_report)

    records = resolve_assets(auto_dir, manual_dir, locked_dir, final_dir, args.clean_final)

    write_markdown_report(records, report)
    json_report.parent.mkdir(parents=True, exist_ok=True)
    json_report.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Resolved assets: {len(records)}")
    print(f"Markdown report: {report}")
    print(f"JSON report: {json_report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
