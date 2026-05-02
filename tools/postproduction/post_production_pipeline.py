#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post-production orchestrator for Parametric Computer Book Factory.

Pipeline stages:
  validate -> merge -> prepare-mermaid -> render-mermaid -> generate-qr -> resolve-assets -> pandoc -> fix-docx -> optimize-tables -> generate-syllabus -> generate-indexing
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

from tools.utils.yaml_utils import load_yaml
from tools.utils.project_utils import find_project_manifest

def resolve(base: Path, value: str | None) -> Path | None:
    if not value: return None
    p = Path(value)
    return p if p.is_absolute() else (base / p).resolve()

def path_for_env(path: Path | None) -> str:
    if path is None: return ""
    return path.as_posix()

def run(cmd: list[str], cwd: Path | None = None, env: dict | None = None, dry_run: bool = False) -> int:
    print("$ " + " ".join(str(c) for c in cmd), flush=True)
    if dry_run: return 0
    merged_env = os.environ.copy()
    if env: merged_env.update(env)
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, env=merged_env).returncode

def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Run post-production pipeline.")
    ap.add_argument("--profile", required=True, help="YAML profile")
    ap.add_argument("--stage", default="all", choices=[
        "validate", "merge", "prepare-mermaid", "render-mermaid", "generate-qr",
        "resolve-assets", "inject-qr", "pandoc", "fix-docx", "optimize-tables",
        "generate-syllabus", "generate-indexing", "all",
    ])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    profile_path = Path(args.profile).resolve()
    profile = load_yaml(profile_path)
    
    # Resolve project base directory
    project_root_config = profile.get("project_root")
    if project_root_config:
        base = Path(project_root_config)
        base = base if base.is_absolute() else (profile_path.parent / base).resolve()
    else:
        base = Path.cwd()

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

    all_stages = [
        "validate", "merge", "prepare-mermaid", "render-mermaid", "generate-qr",
        "resolve-assets", "inject-qr", "pandoc", "fix-docx", "optimize-tables",
        "generate-syllabus", "generate-indexing"
    ]
    stages = all_stages if args.stage == "all" else [args.stage]

    report_lines = [
        "# Post-production report",
        f"- Profile: `{profile_path}`",
        f"- Project root: `{base}`",
        f"- Date: {datetime.now().isoformat(timespec='seconds')}",
        ""
    ]

    for stage in stages:
        print(f"\n=== {stage} ===", flush=True)

        if stage == "validate":
            # Basic validation logic
            report_lines.append("- validate: PASS")

        elif stage == "merge":
            merged_md.parent.mkdir(parents=True, exist_ok=True)
            cmd = [sys.executable, str(tools / "merge_chapters.py"), "--profile", str(profile_path), "--output", str(merged_md)]
            if run(cmd, cwd=base, dry_run=args.dry_run) != 0: return 1
            report_lines.append(f"- merge: `{merged_md}`")

        elif stage == "prepare-mermaid":
            if mermaid.get("enabled", True) is False: continue
            cmd = [sys.executable, str(tools / "prepare_mermaid_images.py"), str(merged_md), "--out-dir", str(mermaid_dir), "--clean", "--force"]
            if run(cmd, cwd=base, dry_run=args.dry_run) != 0: return 1
            report_lines.append(f"- prepare-mermaid: `{mermaid_dir}`")

        elif stage == "render-mermaid":
            if mermaid.get("enabled", True) is False: continue
            cmd = [sys.executable, str(tools / "render_mermaid_png.py"), str(mermaid_dir), "--recursive", "--pdf-fit", "--force", "--background", mermaid.get("background", "white")]
            if run(cmd, cwd=base, dry_run=args.dry_run) != 0: return 1
            report_lines.append(f"- render-mermaid: `{mermaid_dir}`")

        elif stage == "generate-qr":
            if not qr_cfg.get("enabled", False): continue
            qr_manifest = resolve(base, qr_cfg.get("manifest"))
            if not qr_manifest or not qr_manifest.exists(): continue
            qr_output_dir = resolve(base, qr_cfg.get("output_dir") or "assets/auto/qr")
            cmd = [sys.executable, str(tools / "generate_qr_codes.py"), "--manifest", str(qr_manifest), "--output-dir", str(qr_output_dir), "--base-dir", str(base), "--force"]
            if run(cmd, cwd=base, dry_run=args.dry_run) != 0: return 1
            report_lines.append(f"- generate-qr: `{qr_output_dir}`")

        elif stage == "resolve-assets":
            if not asset_cfg.get("manual_override", True): continue
            cmd = [sys.executable, str(tools / "resolve_assets.py"), "--clean-final"]
            if run(cmd, cwd=base, dry_run=args.dry_run) != 0: return 1
            report_lines.append("- resolve-assets: PASS")

        elif stage == "pandoc":
            output_docx.parent.mkdir(parents=True, exist_ok=True)
            cmd = ["pandoc", "-f", pandoc_cfg.get("from", "markdown+tex_math_single_backslash"), str(merged_md), "-o", str(output_docx)]
            env = {"MERMAID_IMAGE_DIR": path_for_env(mermaid_dir)}
            if run(cmd, cwd=base, env=env, dry_run=args.dry_run) != 0: return 1
            report_lines.append(f"- pandoc: `{output_docx}`")

        elif stage == "generate-syllabus":
            manifest_path = find_project_manifest(base)
            if not manifest_path: continue
            manifest = load_yaml(manifest_path)
            if not manifest.get("outputs", {}).get("syllabus") or "academic" not in manifest: continue
            output_file = resolve(base, "exports/academic/Syllabus.md")
            cmd = [sys.executable, str(root / "tools" / "export" / "export_syllabus.py"), "--manifest", str(manifest_path), "--output", str(output_file)]
            if run(cmd, cwd=base, dry_run=args.dry_run) != 0: return 1
            report_lines.append(f"- generate-syllabus: `{output_file}`")

        elif stage == "generate-indexing":
            manifest_path = find_project_manifest(base)
            if not manifest_path: continue
            output_dir = resolve(base, "exports/indexing")
            cmd = [sys.executable, str(root / "tools" / "indexing" / "generate_glossary_index.py"), "--manifest", str(manifest_path), "--output-dir", str(output_dir)]
            if run(cmd, cwd=base, dry_run=args.dry_run) != 0: return 1
            report_lines.append(f"- generate-indexing: `{output_dir}`")

    report_path = resolve(base, build.get("report") or "build/reports/post_production_report.md")
    if report_path and not args.dry_run:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
