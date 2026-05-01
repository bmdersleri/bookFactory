#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render rich Markdown code pages from an enriched BookFactory code manifest.

The renderer is intentionally static-site friendly. Each page contains metadata,
links, source code, test status, optional test details and a short usage block.
"""
from __future__ import annotations

import argparse
import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tools.utils.yaml_utils import load_data


LANGUAGE_HINTS = {
    "java": "java",
    "python": "python",
    "javascript": "javascript",
    "js": "javascript",
}


def get_items(data: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("items", "codes", "code_entries", "entries"):
        if isinstance(data.get(key), list):
            return [item for item in data[key] if isinstance(item, dict)]
    nested = data.get("code_manifest")
    if isinstance(nested, dict):
        return get_items(nested)
    return []


def load_test_results(path: Path | None) -> dict[str, dict[str, Any]]:
    if not path or not path.exists():
        return {}
    data = load_data(path)
    results: dict[str, dict[str, Any]] = {}
    for result in data.get("results", []):
        if isinstance(result, dict) and result.get("id"):
            results[str(result["id"])] = result
    return results


def read_code(item: dict[str, Any], package_root: Path) -> str:
    candidates = []
    for key in ("code_path", "repo_code_path", "source_path", "path"):
        value = item.get(key)
        if value:
            path = Path(str(value))
            candidates.append(path if path.is_absolute() else package_root / path)
    file_name = item.get("file")
    if file_name:
        candidates.append(package_root / str(file_name))
    for path in candidates:
        if path.exists() and path.is_file():
            return path.read_text(encoding="utf-8", errors="replace")
    return ""


def safe_title(item: dict[str, Any]) -> str:
    return str(item.get("title") or item.get("title_key") or item.get("file") or item.get("id") or "Code")


def page_path_for(item: dict[str, Any], out_dir: Path) -> Path:
    chapter_folder = str(item.get("chapter_folder") or item.get("chapter_id") or "chapter")
    code_folder = str(item.get("code_folder") or item.get("id") or item.get("file") or "code")
    return out_dir / chapter_folder / code_folder / "index.md"


def status_badge(status: str) -> str:
    status = status or "unknown"
    label = status.upper()
    return f"`{label}`"


def command_hint(item: dict[str, Any]) -> str:
    language = str(item.get("language", "")).lower()
    file_name = str(item.get("file") or "")
    class_name = Path(file_name).stem
    if language == "java":
        return f"javac {file_name}\njava {class_name}"
    if language == "python":
        return f"python {file_name}"
    if language in {"javascript", "js"}:
        return f"node {file_name}"
    return "# Run command is language-specific."


def render_page(item: dict[str, Any], test_result: dict[str, Any] | None, code: str) -> str:
    generated_at = datetime.now(timezone.utc).isoformat()
    title = safe_title(item)
    language = str(item.get("language") or "text").lower()
    fence_lang = LANGUAGE_HINTS.get(language, language or "text")
    status = str(item.get("test_status") or (test_result or {}).get("status") or "unknown")
    source_url = str(item.get("github_source_url") or item.get("source_url") or "")
    page_url = str(item.get("github_page_url") or "")

    lines = [
        "---",
        f'title: "{title.replace(chr(34), chr(92)+chr(34))}"',
        f'code_id: "{item.get("id", "")}"',
        f'language: "{language}"',
        f'test_status: "{status}"',
        "---",
        "",
        f"# {title}",
        "",
        f"Generated at: `{generated_at}`",
        "",
        "## Metadata",
        "",
        f"- Code ID: `{item.get('id', '')}`",
        f"- Chapter ID: `{item.get('chapter_id', '')}`",
        f"- File: `{item.get('file', '')}`",
        f"- Language: `{language}`",
        f"- Test mode: `{item.get('test', 'none')}`",
        f"- Test status: {status_badge(status)}",
    ]
    if source_url:
        lines.append(f"- GitHub source: {source_url}")
    if page_url:
        lines.append(f"- Public page: {page_url}")
    if item.get("source_markdown"):
        lines.append(f"- Source markdown: `{item.get('source_markdown')}`")
    lines.extend([
        "",
        "## How to run",
        "",
        "```bash",
        command_hint(item),
        "```",
        "",
        "## Source code",
        "",
        f"```{fence_lang}",
        code.rstrip() if code else "// Source code could not be located from the manifest.",
        "```",
        "",
    ])

    if test_result:
        lines.extend(["## Test result", ""])
        lines.append(f"- Status: `{test_result.get('status', 'unknown')}`")
        assertions = test_result.get("assertions") or []
        if assertions:
            lines.extend(["", "### Assertions", "", "| Stream | Contains | Passed |", "|---|---|---:|"])
            for assertion in assertions:
                if not isinstance(assertion, dict):
                    continue
                lines.append(
                    f"| `{assertion.get('stream', '')}` | `{assertion.get('contains', '')}` | `{assertion.get('passed', '')}` |"
                )
        steps = test_result.get("steps") or []
        if steps:
            lines.extend(["", "### Steps", "", "| Step | Return code | Timed out |", "|---|---:|---:|"])
            for step in steps:
                if not isinstance(step, dict):
                    continue
                lines.append(
                    f"| `{step.get('name', '')}` | `{step.get('returncode', '')}` | `{step.get('timed_out', '')}` |"
                )
    else:
        lines.extend(["## Test result", "", "No matching test report entry was provided."])

    lines.extend([
        "",
        "## Notes",
        "",
        "This page was generated by BookFactory from CODE_META metadata.",
        "",
    ])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Render rich Markdown code pages from enriched code manifest.")
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--test-report", type=Path)
    ap.add_argument("--package-root", type=Path, default=Path.cwd())
    ap.add_argument("--out-dir", type=Path, default=Path("build/code_pages"))
    ap.add_argument("--clean", action="store_true")
    ap.add_argument("--index", type=Path, default=None, help="Optional index.md path. Defaults to OUT_DIR/index.md.")
    args = ap.parse_args(argv)

    package_root = args.package_root.resolve()
    manifest_path = args.manifest if args.manifest.is_absolute() else package_root / args.manifest
    out_dir = args.out_dir if args.out_dir.is_absolute() else package_root / args.out_dir
    test_report = args.test_report if not args.test_report or args.test_report.is_absolute() else package_root / args.test_report

    if args.clean and out_dir.exists():
        import shutil
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    data = load_data(manifest_path)
    items = get_items(data)
    test_results = load_test_results(test_report)
    rendered: list[dict[str, Any]] = []

    for item in items:
        code_id = str(item.get("id", ""))
        code = read_code(item, package_root)
        test_result = test_results.get(code_id)
        page_path = page_path_for(item, out_dir)
        page_path.parent.mkdir(parents=True, exist_ok=True)
        page_path.write_text(render_page(item, test_result, code) + "\n", encoding="utf-8")
        rendered.append({"id": code_id, "page": str(page_path.relative_to(package_root)).replace("\\", "/")})

    index_path = args.index or (out_dir / "index.md")
    if not index_path.is_absolute():
        index_path = package_root / index_path
    index_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# BookFactory Code Pages",
        "",
        f"Generated at: `{datetime.now(timezone.utc).isoformat()}`",
        "",
        "| Code ID | Page |",
        "|---|---|",
    ]
    for item in rendered:
        lines.append(f"| `{item['id']}` | [{item['page']}]({item['page']}) |")
    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"[OK] Rendered code pages: {len(rendered)}")
    print(f"[OK] Index: {index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
