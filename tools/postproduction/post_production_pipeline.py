#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post-production orchestrator for Parametric Computer Book Factory.

Pipeline stages:
  validate -> merge -> prepare-mermaid -> render-mermaid -> generate-qr -> resolve-assets -> pandoc -> fix-docx -> optimize-tables

Design notes:
- Paths are resolved relative to project_root, not relative to the profile directory.
- `assets/manual` and `assets/locked` are protected by design.
- Each stage can be run separately.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from tools.utils.yaml_utils import load_yaml
from datetime import datetime


def resolve(base: Path, value: str | None) -> Path | None:
    if not value:
        return None
    p = Path(value)
    return p if p.is_absolute() else (base / p).resolve()


def path_for_env(path: Path | None) -> str:
    """Return a path representation that Lua/Pandoc can read on all platforms."""
    if path is None:
        return ""
    return path.as_posix()


def run(cmd: list[str], cwd: Path | None = None, env: dict | None = None, dry_run: bool = False) -> int:
    print("$ " + " ".join(str(c) for c in cmd))
    if dry_run:
        return 0
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, env=merged_env).returncode


def require_file(path: Path, label: str) -> None:
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"{label} not found: {path}")


def validate(profile: dict, base: Path) -> list[str]:
    errors: list[str] = []
    pp = profile.get("post_production", {})
    chapters = profile.get("chapters") or pp.get("chapters") or []

    if not chapters:
        errors.append("No chapters listed in profile.chapters or post_production.chapters")

    for ch in chapters:
        src = ch.get("source") or ch.get("path")
        if not src:
            errors.append(f"Chapter without source/path: {ch}")
        else:
            p = resolve(base, src)
            if not p or not p.exists():
                errors.append(f"Chapter source not found: {src} -> {p}")

    for key in ["reference_docx", "lua_filter"]:
        value = pp.get("pandoc", {}).get(key)
        if value:
            p = resolve(base, value)
            if not p or not p.exists():
                errors.append(f"Pandoc {key} not found: {value} -> {p}")

    return errors


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Run post-production pipeline for a generated book.")
    ap.add_argument("--profile", required=True, help="YAML post-production profile")
    ap.add_argument("--stage", default="all", choices=[
        "validate",
        "merge",
        "prepare-mermaid",
        "render-mermaid",
        "generate-qr",
        "resolve-assets",
        "pandoc",
        "fix-docx",
        "optimize-tables",
        "all",
    ])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    profile_path = Path(args.profile).resolve()
    profile = load_yaml(profile_path)
    base = profile_base(profile_path, profile)
    root = repo_root()
    tools = root / "tools" / "postproduction"

    pp = profile.get("post_production", {})
    build = pp.get("build", {})
    mermaid = pp.get("mermaid", {})
    pandoc_cfg = pp.get("pandoc", {})
    docx_cfg = pp.get("docx_postprocess", {})
    asset_cfg = pp.get("assets", {})
    qr_cfg = pp.get("qr", {})

    merged_md = resolve(base, build.get("merged_markdown") or "build/merged/book_merged.md")
    output_docx = resolve(base, build.get("output_docx") or "dist/book.docx")
    mermaid_dir = resolve(base, mermaid.get("output_dir") or "build/mermaid")

    stages = [
        "validate",
        "merge",
        "prepare-mermaid",
        "render-mermaid",
        "generate-qr",
        "resolve-assets",
        "pandoc",
        "fix-docx",
        "optimize-tables",
    ] if args.stage == "all" else [args.stage]

    report_lines = [
        "# Post-production report",
        "",
        f"Profile: `{profile_path}`",
        f"Project root: `{base}`",
        f"Date: {datetime.now().isoformat(timespec='seconds')}",
        "",
    ]

    for stage in stages:
        print(f"\n=== {stage} ===")

        if stage == "validate":
            errors = validate(profile, base)
            if errors:
                for e in errors:
                    print(f"[ERROR] {e}", file=sys.stderr)
                return 1
            print("Validation passed.")
            report_lines.append("- validate: PASS")

        elif stage == "merge":
            assert merged_md is not None
            merged_md.parent.mkdir(parents=True, exist_ok=True)
            cmd = [sys.executable, str(tools / "merge_chapters.py"), "--profile", str(profile_path), "--output", str(merged_md)]
            rc = run(cmd, cwd=base, dry_run=args.dry_run)
            if rc:
                return rc
            report_lines.append(f"- merge: `{merged_md}`")

        elif stage == "prepare-mermaid":
            if mermaid.get("enabled", True) is False:
                print("Mermaid preparation skipped; mermaid.enabled is false.")
                report_lines.append("- prepare-mermaid: SKIPPED")
                continue
            assert merged_md is not None and mermaid_dir is not None
            cmd = [
                sys.executable,
                str(tools / "prepare_mermaid_images.py"),
                str(merged_md),
                "--out-dir",
                str(mermaid_dir),
                "--clean",
                "--force",
            ]
            rc = run(cmd, cwd=base, dry_run=args.dry_run)
            if rc:
                return rc
            report_lines.append(f"- prepare-mermaid: `{mermaid_dir}`")

        elif stage == "render-mermaid":
            if mermaid.get("enabled", True) is False:
                print("Mermaid rendering skipped; mermaid.enabled is false.")
                report_lines.append("- render-mermaid: SKIPPED")
                continue
            assert mermaid_dir is not None
            cmd = [
                sys.executable,
                str(tools / "render_mermaid_png.py"),
                str(mermaid_dir),
                "--recursive",
                "--pdf-fit",
                "--force",
                "--background",
                mermaid.get("background", "white"),
            ]
            puppeteer_config = mermaid.get("puppeteer_config")
            if puppeteer_config:
                puppeteer_config_path = resolve(base, puppeteer_config)
                if puppeteer_config_path and puppeteer_config_path.exists():
                    cmd.extend(["--puppeteer-config", path_for_env(puppeteer_config_path)])
                else:
                    print(f"Puppeteer config not found, continuing without it: {puppeteer_config_path}")
            rc = run(cmd, cwd=base, dry_run=args.dry_run)
            if rc:
                return rc
            report_lines.append(f"- render-mermaid: `{mermaid_dir}`")

        elif stage == "generate-qr":
            if not qr_cfg.get("enabled", False):
                print("QR generation skipped; qr.enabled is false or missing.")
                report_lines.append("- generate-qr: SKIPPED")
                continue

            qr_manifest = resolve(base, qr_cfg.get("manifest"))
            if not qr_manifest or not qr_manifest.exists():
                if qr_cfg.get("allow_missing_manifest", True):
                    print(f"QR manifest not found, skipping: {qr_manifest}")
                    report_lines.append("- generate-qr: SKIPPED missing manifest")
                    continue
                raise FileNotFoundError(f"QR manifest not found: {qr_manifest}")

            qr_output_dir = resolve(base, qr_cfg.get("output_dir") or "assets/auto/qr")
            qr_report = resolve(base, qr_cfg.get("report") or "build/reports/qr_generation_report.md")

            cmd = [
                sys.executable,
                str(tools / "generate_qr_codes.py"),
                "--manifest",
                str(qr_manifest),
                "--output-dir",
                str(qr_output_dir),
                "--report",
                str(qr_report),
                "--base-dir",
                str(base),
                "--force",
            ]
            if qr_cfg.get("dry_run", False):
                cmd.append("--dry-run")

            rc = run(cmd, cwd=base, dry_run=args.dry_run)
            if rc:
                return rc
            report_lines.append(f"- generate-qr: `{qr_output_dir}`")

        elif stage == "resolve-assets":
            if not asset_cfg.get("manual_override", True):
                print("Asset resolving skipped; manual_override is disabled.")
                continue
            cmd = [
                sys.executable,
                str(tools / "resolve_assets.py"),
                "--profile",
                str(profile_path),
                "--clean-final",
            ]
            rc = run(cmd, cwd=base, dry_run=args.dry_run)
            if rc:
                return rc
            report_lines.append("- resolve-assets: PASS")

        elif stage == "pandoc":
            assert merged_md is not None and output_docx is not None
            output_docx.parent.mkdir(parents=True, exist_ok=True)
            reference_docx = resolve(base, pandoc_cfg.get("reference_docx"))
            lua_filter = resolve(base, pandoc_cfg.get("lua_filter"))
            if reference_docx:
                require_file(reference_docx, "reference_docx")
            if lua_filter:
                require_file(lua_filter, "lua_filter")

            cmd = [
                "pandoc",
                "-f",
                pandoc_cfg.get("from", "markdown+tex_math_single_backslash"),
                str(merged_md),
                "-o",
                str(output_docx),
            ]
            if reference_docx:
                cmd.append(f"--reference-doc={reference_docx}")
            if lua_filter:
                cmd.append(f"--lua-filter={lua_filter}")
            if pandoc_cfg.get("toc", True):
                cmd.append("--toc")
            cmd.append(f"--toc-depth={pandoc_cfg.get('toc_depth', 2)}")
            for meta_key, meta_value in (pandoc_cfg.get("metadata") or {}).items():
                cmd.append(f"--metadata={meta_key}:{meta_value}")

            # The Lua filter resolves Mermaid images by MERMAID_IMAGE_DIR first.
            # Running Pandoc from merged_md.parent also preserves backward compatibility
            # with filters that expect a local mermaid_images/ directory.
            env = {
                "MERMAID_IMAGE_WIDTH": str(mermaid.get("docx_width", "4.90in")),
                "MERMAID_IMAGE_DIR": path_for_env(mermaid_dir),
            }
            pandoc_cwd = merged_md.parent if merged_md.parent.exists() else base
            rc = run(cmd, cwd=pandoc_cwd, env=env, dry_run=args.dry_run)
            if rc:
                return rc
            report_lines.append(f"- pandoc: `{output_docx}`")

        elif stage == "fix-docx":
            if docx_cfg.get("enabled", True) is False:
                print("DOCX format fixing skipped; docx_postprocess.enabled is false.")
                report_lines.append("- fix-docx: SKIPPED")
                continue
            assert output_docx is not None
            tool = tools / docx_cfg.get("format_fix_tool", "fix_docx_format_ooxml.py")
            cmd = [sys.executable, str(tool), str(output_docx), "--in-place"]
            if not docx_cfg.get("fix_table_headers", True):
                cmd.append("--no-table-header-fix")
            rc = run(cmd, cwd=base, dry_run=args.dry_run)
            if rc:
                return rc
            report_lines.append("- fix-docx: PASS")

        elif stage == "optimize-tables":
            if docx_cfg.get("enabled", True) is False:
                print("Table optimization skipped; docx_postprocess.enabled is false.")
                report_lines.append("- optimize-tables: SKIPPED")
                continue
            assert output_docx is not None
            if not docx_cfg.get("optimize_tables", True):
                print("Table optimization disabled by profile.")
                report_lines.append("- optimize-tables: SKIPPED")
                continue
            cmd = [
                sys.executable,
                str(tools / "optimize_docx_tables.py"),
                str(output_docx),
                "--in-place",
                "--mode",
                docx_cfg.get("table_mode", "proportional"),
            ]
            rc = run(cmd, cwd=base, dry_run=args.dry_run)
            if rc:
                return rc
            report_lines.append("- optimize-tables: PASS")

    report_path = resolve(base, build.get("report") or "build/reports/post_production_report.md")
    if report_path and not args.dry_run:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
        print(f"Report: {report_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
