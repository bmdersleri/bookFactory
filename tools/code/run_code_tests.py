#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run local code tests for CODE_META code manifests.

v2.10.0 dispatches test execution through language adapters.  Java remains the
primary production path; Python and JavaScript now support basic local syntax,
run and stdout/stderr assertion checks.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Allow direct execution as: python tools/code/run_code_tests.py
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.code.language_adapters import JavaAdapter, JavaScriptAdapter, PythonAdapter
from tools.utils.yaml_utils import load_data


def resolve_path(path_value: str, package_root: Path) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else package_root / path


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        return load_data(path)
    except Exception as exc:
        raise SystemExit(f"Cannot load code manifest {path}: {exc}") from exc


def skipped_item(item: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "id": item.get("id"),
        "chapter_id": item.get("chapter_id"),
        "language": item.get("language"),
        "test": item.get("test"),
        "file": item.get("file"),
        "status": "skipped",
        "failure_reason": reason,
        "steps": [],
        "assertions": [],
    }


def inject_plot_reference(item: dict[str, Any], package_root: Path) -> None:
    """Injects a markdown image reference after a code block if a plot was generated."""
    expected_plot = item.get("expected_plot")
    source_md_rel = item.get("source_markdown")
    if not expected_plot or not source_md_rel:
        return

    md_path = package_root / source_md_rel
    if not md_path.exists():
        return

    content = md_path.read_text(encoding="utf-8")

    # Check if already injected
    plot_ref = f"../assets/auto/plots/{expected_plot}"
    if plot_ref in content:
        return

    # Find the specific CODE_META block for this code ID and the following code block
    meta_id = item.get("id")
    pattern = re.compile(
        rf"(<!--\s*CODE_META[\s\S]*?id:\s*{re.escape(meta_id)}[\s\S]*?-->[\s\S]*?```[\s\S]*?```)",
        re.MULTILINE
    )

    match = pattern.search(content)
    if not match:
        return

    insertion_point = match.end()
    injection = f"\n\n![Otomatik Üretilen Grafik - {meta_id}]({plot_ref})\n"

    new_content = content[:insertion_point] + injection + content[insertion_point:]
    md_path.write_text(new_content, encoding="utf-8")


def write_markdown_report(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# BookFactory Code Test Report",
        "",
        f"Generated at: `{report['generated_at']}`",
        "",
        "## Summary",
        "",
        f"- Total: {report['summary']['total']}",
        f"- Passed: {report['summary']['passed']}",
        f"- Failed: {report['summary']['failed']}",
        f"- Skipped: {report['summary']['skipped']}",
        "",
        "## Adapter Summary",
        "",
        "| Language | Total | Passed | Failed | Skipped |",
        "|---|---:|---:|---:|---:|",
    ]
    for lang, stats in sorted(report.get("adapter_summary", {}).items()):
        lines.append(
            f"| `{lang}` | {stats.get('total', 0)} | {stats.get('passed', 0)} | "
            f"{stats.get('failed', 0)} | {stats.get('skipped', 0)} |"
        )
    lines.extend([
        "",
        "## Results",
        "",
        "| Status | Language | ID | Chapter | File | Test | Reason |",
        "|---|---|---|---|---|---|---|",
    ])
    for item in report["results"]:
        lines.append(
            f"| {item.get('status')} | `{item.get('language')}` | `{item.get('id')}` | "
            f"`{item.get('chapter_id')}` | `{item.get('file')}` | `{item.get('test')}` | "
            f"{item.get('failure_reason', '')} |"
        )
    failed = [r for r in report["results"] if r.get("status") == "failed"]
    if failed:
        lines.extend(["", "## Failed test details", ""])
        for item in failed:
            lines.append(f"### `{item.get('id')}`")
            lines.append("")
            lines.append(f"- Language: `{item.get('language')}`")
            lines.append(f"- Reason: `{item.get('failure_reason', '')}`")
            lines.append("")
            for step in item.get("steps", []):
                lines.append(f"**Step:** {step.get('name')}")
                lines.append("")
                lines.append("```text")
                lines.append("Command: " + " ".join(step.get("command", [])))
                lines.append(f"Return code: {step.get('returncode')}")
                if step.get("stdout"):
                    lines.append("\nSTDOUT:\n" + str(step.get("stdout")))
                if step.get("stderr"):
                    lines.append("\nSTDERR:\n" + str(step.get("stderr")))
                lines.append("```")
                lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def summarize_by_language(results: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for result in results:
        lang = str(result.get("language") or "unknown")
        stats = out.setdefault(lang, {"total": 0, "passed": 0, "failed": 0, "skipped": 0})
        stats["total"] += 1
        status = str(result.get("status") or "skipped")
        if status in stats:
            stats[status] += 1
        else:
            stats["skipped"] += 1
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run CODE_META code tests locally.")
    parser.add_argument("--manifest", type=Path, default=Path("build/code_manifest.json"))
    parser.add_argument("--package-root", type=Path, default=Path.cwd())
    parser.add_argument("--report-json", type=Path, default=Path("build/test_reports/code_test_report.json"))
    parser.add_argument("--report-md", type=Path, default=Path("build/test_reports/code_test_report.md"))
    parser.add_argument("--timeout-sec", type=int, default=10)
    parser.add_argument("--javac", default="javac")
    parser.add_argument("--java", default="java")
    parser.add_argument("--python", default=sys.executable or "python")
    parser.add_argument("--node", default="node")
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args(argv)

    package_root = args.package_root.resolve()
    manifest_path = resolve_path(str(args.manifest), package_root)
    report_json_path = resolve_path(str(args.report_json), package_root)
    report_md_path = resolve_path(str(args.report_md), package_root)
    manifest = load_manifest(manifest_path)
    items = manifest.get("items", [])

    adapters = {
        "java": JavaAdapter(javac=args.javac, java=args.java, default_timeout=args.timeout_sec),
        "python": PythonAdapter(executable=args.python, default_timeout=args.timeout_sec),
        "javascript": JavaScriptAdapter(executable=args.node, default_timeout=args.timeout_sec),
    }

    results: list[dict[str, Any]] = []
    for item in items:
        language = str(item.get("language", "")).lower()
        test_mode = str(item.get("test", "none"))
        if test_mode == "none":
            results.append(skipped_item(item, "test_mode_none"))
            continue
        adapter = adapters.get(language)
        if adapter is None:
            results.append(skipped_item(item, f"unsupported_language_{language}"))
            continue
        results.append(adapter.run(item, package_root))

    summary = {
        "total": len(results),
        "passed": sum(1 for r in results if r.get("status") == "passed"),
        "failed": sum(1 for r in results if r.get("status") == "failed"),
        "skipped": sum(1 for r in results if r.get("status") == "skipped"),
    }
    report = {
        "schema_version": "1.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "manifest": str(manifest_path),
        "summary": summary,
        "adapter_summary": summarize_by_language(results),
        "results": results,
    }
    report_json_path.parent.mkdir(parents=True, exist_ok=True)
    report_json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown_report(report, report_md_path)

    print(
        f"Total: {summary['total']} | Passed: {summary['passed']} | "
        f"Failed: {summary['failed']} | Skipped: {summary['skipped']}"
    )
    print(f"JSON report: {report_json_path}")
    print(f"Markdown report: {report_md_path}")
    if summary["failed"] and args.fail_on_error:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
