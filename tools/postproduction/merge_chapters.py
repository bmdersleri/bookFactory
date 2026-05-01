#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Merge chapter Markdown files for Parametric Computer Book Factory.

The tool reads either:
  1) a YAML post-production profile containing chapters[].source, or
  2) explicit Markdown paths passed with --chapters.

Visible numbering is not applied here. Numbering is expected to be handled
by the build/post-production layer.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from datetime import datetime

from tools.utils.yaml_utils import load_yaml

FRONT_MATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.DOTALL)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def strip_front_matter(text: str) -> str:
    return FRONT_MATTER_RE.sub("", text, count=1).lstrip()


def load_profile(profile_path: Path) -> dict:
    return load_yaml(profile_path)


def profile_base(profile_path: Path, profile: dict) -> Path:
    project_root = profile.get("project_root") or profile.get("post_production", {}).get("project_root")
    if project_root:
        p = Path(project_root)
        return p.resolve() if p.is_absolute() else (profile_path.parent / p).resolve()
    # fallback: profile directory for backward compatibility
    return profile_path.parent


def profile_chapter_paths(profile: dict, base_dir: Path) -> list[Path]:
    chapters = profile.get("chapters") or profile.get("post_production", {}).get("chapters") or []
    paths: list[Path] = []
    for ch in chapters:
        src = ch.get("source") or ch.get("path")
        if not src:
            raise ValueError(f"Chapter entry is missing source/path: {ch}")
        p = Path(src)
        if not p.is_absolute():
            p = base_dir / p
        paths.append(p.resolve())
    return paths


def scalar(v, default=""):
    if isinstance(v, dict):
        return v.get("tr") or v.get("en") or next(iter(v.values()), default)
    return v or default


def build_front_matter(profile: dict | None, explicit_front_matter: Path | None) -> str:
    if explicit_front_matter:
        txt = explicit_front_matter.read_text(encoding="utf-8").strip()
        if not txt.startswith("---"):
            txt = "---\n" + txt + "\n---"
        return txt.rstrip() + "\n\n"

    if not profile:
        return ""

    book = profile.get("book") or {}
    lang = profile.get("language", {}).get("content_language") or profile.get("language", {}).get("primary_language") or "tr-TR"

    fm = {
        "title": scalar(book.get("title"), "Book"),
        "subtitle": scalar(book.get("subtitle"), ""),
        "author": scalar(book.get("author"), ""),
        "date": str(book.get("year") or datetime.now().year),
        "lang": lang,
        "documentclass": "report",
        "toc": True,
        "toc-depth": 3,
        "numbersections": True,
    }

    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, bool):
            lines.append(f"{k}: {str(v).lower()}")
        else:
            lines.append(f'{k}: "{str(v).replace(chr(34), chr(39))}"')
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def merge(
    chapter_paths: list[Path],
    output: Path,
    profile: dict | None,
    book_front_matter: Path | None,
    keep_chapter_front_matter: bool,
    pagebreak: str,
) -> dict:
    output.parent.mkdir(parents=True, exist_ok=True)
    missing = [str(p) for p in chapter_paths if not p.exists()]
    if missing:
        raise FileNotFoundError("Missing chapter files:\n" + "\n".join(missing))

    parts: list[str] = []
    fm = build_front_matter(profile, book_front_matter)
    if fm:
        parts.append(fm.rstrip() + "\n")

    for idx, path in enumerate(chapter_paths, start=1):
        text = read_text(path)
        if not keep_chapter_front_matter:
            text = strip_front_matter(text)
        parts.append(f"\n<!-- SOURCE_FILE: {path.as_posix()} -->\n\n")
        parts.append(text.strip() + "\n")
        if idx != len(chapter_paths):
            parts.append(f"\n{pagebreak}\n")

    output.write_text("\n".join(parts).strip() + "\n", encoding="utf-8")
    return {"chapters": len(chapter_paths), "output": str(output)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Merge chapter Markdown files into one Pandoc-compatible Markdown file.")
    ap.add_argument("--profile", help="YAML post-production profile")
    ap.add_argument("--chapters", nargs="*", help="Explicit chapter Markdown files")
    ap.add_argument("--output", required=True, help="Merged output Markdown file")
    ap.add_argument("--book-front-matter", help="Optional YAML front matter file")
    ap.add_argument("--keep-chapter-front-matter", action="store_true", help="Do not strip per-chapter YAML front matter")
    ap.add_argument("--pagebreak", default="\\newpage", help="Page break marker between chapters")
    args = ap.parse_args(argv)

    profile = None
    profile_path = Path(args.profile).resolve() if args.profile else None

    if profile_path:
        profile = load_profile(profile_path)
        base_dir = profile_base(profile_path, profile)
        chapter_paths = profile_chapter_paths(profile, base_dir)
    else:
        chapter_paths = [Path(p).resolve() for p in (args.chapters or [])]

    if not chapter_paths:
        print("[ERROR] No chapters were provided.", file=sys.stderr)
        return 1

    stats = merge(
        chapter_paths=chapter_paths,
        output=Path(args.output).resolve(),
        profile=profile,
        book_front_matter=Path(args.book_front_matter).resolve() if args.book_front_matter else None,
        keep_chapter_front_matter=args.keep_chapter_front_matter,
        pagebreak=args.pagebreak,
    )
    print("Merge completed.")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
