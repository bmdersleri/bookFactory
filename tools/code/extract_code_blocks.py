#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract CODE_META-declared fenced code blocks from Markdown chapters.

This tool is intentionally conservative:
- It only extracts code blocks that are preceded by a CODE_META HTML comment.
- It writes each code block to a deterministic folder under the output directory.
- It produces both JSON and simple YAML manifests for downstream tools.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

META_RE = re.compile(r"<!--\s*CODE_META\s*(.*?)-->", re.DOTALL | re.IGNORECASE)
FENCE_RE = re.compile(r"```([A-Za-z0-9_+\-.#]*)\s*\n(.*?)\n```", re.DOTALL)

REQUIRED_FIELDS = ["id", "chapter_id", "language", "file"]


def strip_quotes(value: str) -> str:
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def parse_scalar(value: str) -> Any:
    value = strip_quotes(value.strip())
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none", ""}:
        return None if lowered in {"null", "none"} else ""
    try:
        return int(value)
    except ValueError:
        return value


def parse_meta_block(text: str) -> dict[str, Any]:
    """Parse a small YAML-like CODE_META block without requiring PyYAML."""
    lines = [line.rstrip("\n") for line in text.splitlines()]
    result: dict[str, Any] = {}
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        if not line or line.startswith("#"):
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "|":
            i += 1
            collected: list[str] = []
            while i < len(lines):
                probe = lines[i]
                stripped = probe.strip()
                if stripped and not probe.startswith((" ", "\t")) and ":" in stripped:
                    break
                collected.append(probe[2:] if probe.startswith("  ") else probe.strip())
                i += 1
            result[key] = "\n".join(collected).rstrip("\n")
            continue
        if value == "":
            # Support simple block lists:
            # key:
            #   - value
            j = i + 1
            items: list[Any] = []
            while j < len(lines):
                probe = lines[j]
                stripped = probe.strip()
                if not stripped:
                    j += 1
                    continue
                if stripped.startswith("-"):
                    items.append(parse_scalar(stripped[1:].strip()))
                    j += 1
                    continue
                break
            if items:
                result[key] = items
                i = j
                continue
            result[key] = ""
            i += 1
            continue
        result[key] = parse_scalar(value)
        i += 1
    return result


def yaml_quote(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if "\n" in text:
        return "|\n" + "\n".join(f"      {line}" for line in text.splitlines())
    escaped = text.replace('"', '\\"')
    return f'"{escaped}"'


def write_simple_yaml(data: dict[str, Any], path: Path) -> None:
    lines: list[str] = []
    for key, value in data.items():
        if key != "items":
            lines.append(f"{key}: {yaml_quote(value)}")
    lines.append("items:")
    for item in data.get("items", []):
        lines.append("  -")
        for k, v in item.items():
            if isinstance(v, list):
                lines.append(f"    {k}:")
                for element in v:
                    lines.append(f"      - {yaml_quote(element)}")
            elif isinstance(v, dict):
                lines.append(f"    {k}:")
                for dk, dv in v.items():
                    lines.append(f"      {dk}: {yaml_quote(dv)}")
            else:
                rendered = yaml_quote(v)
                if rendered.startswith("|\n"):
                    lines.append(f"    {k}: {rendered}")
                else:
                    lines.append(f"    {k}: {rendered}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def discover_markdown_files(chapters_dir: Path | None, files: list[Path]) -> list[Path]:
    discovered: list[Path] = []
    if chapters_dir:
        discovered.extend(sorted(chapters_dir.rglob("*.md")))
    discovered.extend(files)
    # Preserve order while removing duplicates.
    seen: set[Path] = set()
    unique: list[Path] = []
    for file in discovered:
        resolved = file.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(file)
    return unique


def next_code_block_after(text: str, offset: int) -> tuple[str, str] | None:
    match = FENCE_RE.search(text, offset)
    if not match:
        return None
    return match.group(1).strip(), match.group(2)


def safe_part(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_") or "unknown"


def extract_from_file(md_file: Path, out_dir: Path, package_root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    text = md_file.read_text(encoding="utf-8")
    items: list[dict[str, Any]] = []
    errors: list[str] = []
    for index, meta_match in enumerate(META_RE.finditer(text), start=1):
        meta = parse_meta_block(meta_match.group(1))
        for field in REQUIRED_FIELDS:
            if field not in meta or meta[field] in (None, ""):
                errors.append(f"{md_file}: CODE_META #{index} missing required field: {field}")
        fence = next_code_block_after(text, meta_match.end())
        if not fence:
            errors.append(f"{md_file}: CODE_META #{index} has no following fenced code block")
            continue
        fence_lang, code = fence
        language = str(meta.get("language") or fence_lang or "text").lower()
        chapter_id = safe_part(str(meta.get("chapter_id", "unknown_chapter")))
        code_id = safe_part(str(meta.get("id", f"code_{index:03d}")))
        file_name = safe_part(str(meta.get("file", f"{code_id}.{language}")))
        code_folder = out_dir / chapter_id / code_id
        code_folder.mkdir(parents=True, exist_ok=True)
        code_path = code_folder / file_name
        if bool(meta.get("extract", True)):
            code_path.write_text(code.rstrip() + "\n", encoding="utf-8")
        item: dict[str, Any] = {
            "id": str(meta.get("id", f"code_{index:03d}")),
            "chapter_id": str(meta.get("chapter_id", "unknown_chapter")),
            "language": language,
            "kind": str(meta.get("kind", "example")),
            "title_key": str(meta.get("title_key", "")),
            "file": file_name,
            "source_markdown": str(md_file.relative_to(package_root) if md_file.is_relative_to(package_root) else md_file),
            "code_path": str(code_path.relative_to(package_root) if code_path.is_relative_to(package_root) else code_path),
            "fence_language": fence_lang,
            "extract": bool(meta.get("extract", True)),
            "test": str(meta.get("test", "compile")),
            "github": bool(meta.get("github", False)),
            "qr": str(meta.get("qr", "none")),
        }
        optional_keys = [
            "main_class",
            "stdin",
            "expected_stdout_contains",
            "expected_stderr_contains",
            "timeout_sec",
            "sandbox",
            "args",
            "expected_plot",
            "captures_screenshot",
            "sandbox_link",
            "group_id",
            "compare_with",
        ]
        for key in optional_keys:
            if key in meta:
                item[key] = meta[key]
        if "main_class" not in item and language == "java":
            item["main_class"] = Path(file_name).stem
        items.append(item)
    return items, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract CODE_META code blocks from Markdown chapters.")
    parser.add_argument("--chapters-dir", type=Path, help="Directory containing Markdown chapter files.")
    parser.add_argument("--file", dest="files", action="append", type=Path, default=[], help="Individual Markdown file to scan. Can be repeated.")
    parser.add_argument("--out-dir", type=Path, default=Path("build/code"), help="Where extracted code files are written.")
    parser.add_argument("--manifest", type=Path, default=Path("build/code_manifest.json"), help="JSON manifest output path.")
    parser.add_argument("--yaml-manifest", type=Path, default=Path("build/code_manifest.yaml"), help="YAML manifest output path.")
    parser.add_argument("--package-root", type=Path, default=Path.cwd(), help="Project/package root for relative paths.")
    parser.add_argument("--strict", action="store_true", help="Fail on validation warnings.")
    args = parser.parse_args(argv)

    if not args.chapters_dir and not args.files:
        print("[ERROR] Provide --chapters-dir or at least one --file.", file=sys.stderr)
        return 2

    package_root = args.package_root.resolve()
    out_dir = (package_root / args.out_dir).resolve() if not args.out_dir.is_absolute() else args.out_dir.resolve()
    manifest_path = (package_root / args.manifest).resolve() if not args.manifest.is_absolute() else args.manifest.resolve()
    yaml_manifest_path = (package_root / args.yaml_manifest).resolve() if not args.yaml_manifest.is_absolute() else args.yaml_manifest.resolve()
    chapters_dir = None
    if args.chapters_dir:
        chapters_dir = (package_root / args.chapters_dir).resolve() if not args.chapters_dir.is_absolute() else args.chapters_dir.resolve()
    files = [(package_root / f).resolve() if not f.is_absolute() else f.resolve() for f in args.files]

    md_files = discover_markdown_files(chapters_dir, files)
    all_items: list[dict[str, Any]] = []
    all_errors: list[str] = []
    for md_file in md_files:
        if not md_file.exists():
            all_errors.append(f"Missing markdown file: {md_file}")
            continue
        items, errors = extract_from_file(md_file, out_dir, package_root)
        all_items.extend(items)
        all_errors.extend(errors)

    manifest = {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generator": "tools/code/extract_code_blocks.py",
        "item_count": len(all_items),
        "items": all_items,
        "warnings": all_errors,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    yaml_manifest_path.parent.mkdir(parents=True, exist_ok=True)
    write_simple_yaml(manifest, yaml_manifest_path)

    print(f"Extracted CODE_META blocks: {len(all_items)}")
    print(f"JSON manifest: {manifest_path}")
    print(f"YAML manifest: {yaml_manifest_path}")
    if all_errors:
        print("Warnings/errors:", file=sys.stderr)
        for error in all_errors:
            print(f"- {error}", file=sys.stderr)
    return 1 if (all_errors and args.strict) else 0


if __name__ == "__main__":
    raise SystemExit(main())
