#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update post-production profile chapter order from a chapters directory.

Purpose:
- Avoid manually editing chapter_order / chapters in post-production profile.
- Scan generated/{book_id}/{language}/chapters/*.md
- Sort files by chapter_XX prefix when available.
- Update profile.chapters with order, chapter_id and source path.

Usage:
  python update_chapter_order.py \
    --profile configs/post_production_profile_java_fundamentals.yaml \
    --chapters-dir generated/java_fundamentals/tr/chapters \
    --write

Without --write, the tool performs a dry run and prints detected chapters.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

from tools.utils.yaml_utils import load_yaml, dump_yaml




def profile_base(profile_path: Path, profile: dict[str, Any]) -> Path:
    root = profile.get("project_root") or profile.get("post_production", {}).get("project_root")
    if root:
        p = Path(root)
        return p.resolve() if p.is_absolute() else (profile_path.parent / p).resolve()
    return profile_path.parent.resolve()


def slug_from_filename(path: Path) -> str:
    stem = path.stem
    stem = re.sub(r"^chapter[_-]?\d+[_-]?", "", stem, flags=re.IGNORECASE)
    stem = re.sub(r"^bolum[_-]?\d+[_-]?", "", stem, flags=re.IGNORECASE)
    return stem or path.stem


def sort_key(path: Path) -> tuple[int, str]:
    m = re.search(r"(?:chapter|bolum)[_-]?(\d+)", path.stem, flags=re.IGNORECASE)
    if m:
        return int(m.group(1)), path.name.lower()
    return 9999, path.name.lower()


def rel_to_base(path: Path, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except Exception:
        return path.as_posix()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Update post-production profile chapters from a directory.")
    ap.add_argument("--profile", required=True, help="Post-production profile YAML")
    ap.add_argument("--chapters-dir", required=True, help="Directory containing chapter Markdown files")
    ap.add_argument("--write", action="store_true", help="Write changes to profile")
    ap.add_argument("--backup", action="store_true", help="Create .bak backup before writing")
    args = ap.parse_args(argv)

    profile_path = Path(args.profile).resolve()
    if not profile_path.exists():
        print(f"[ERROR] Profile not found: {profile_path}", file=sys.stderr)
        return 1

    profile = load_yaml(profile_path)
    base = profile_base(profile_path, profile)

    chapters_dir = Path(args.chapters_dir)
    if not chapters_dir.is_absolute():
        chapters_dir = (base / chapters_dir).resolve()

    if not chapters_dir.exists() or not chapters_dir.is_dir():
        print(f"[ERROR] Chapters directory not found: {chapters_dir}", file=sys.stderr)
        return 1

    files = sorted(chapters_dir.glob("*.md"), key=sort_key)
    if not files:
        print(f"[ERROR] No Markdown chapter files found in: {chapters_dir}", file=sys.stderr)
        return 2

    chapters = []
    for order, path in enumerate(files, start=1):
        chapters.append({
            "order": order,
            "chapter_id": slug_from_filename(path),
            "source": rel_to_base(path, base),
        })

    print(f"[OK] Detected chapters: {len(chapters)}")
    for ch in chapters:
        print(f"  {ch['order']:02d}. {ch['chapter_id']} -> {ch['source']}")

    if args.write:
        if args.backup:
            backup = profile_path.with_suffix(profile_path.suffix + ".bak")
            backup.write_text(profile_path.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"[OK] Backup written: {backup}")

        profile["chapters"] = chapters
        dump_yaml(profile, profile_path)
        print(f"[OK] Profile updated: {profile_path}")
    else:
        print("[DRY-RUN] Use --write to update the profile.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
