#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Experimental Docker-based Java code test runner.

This script is intentionally marked experimental. It runs each Java code folder in
an isolated container with network disabled and a bounded timeout. For ordinary
local workflows, use run_code_tests.py first.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_path(path_value: str, root: Path) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else root / path


def run_docker_java(item: dict[str, Any], package_root: Path, image: str, timeout: int) -> dict[str, Any]:
    code_path = resolve_path(str(item["code_path"]), package_root)
    cwd = code_path.parent
    file_name = code_path.name
    main_class = str(item.get("main_class") or code_path.stem)
    test_mode = str(item.get("test", "compile"))
    run_part = ""
    if test_mode in {"compile_run", "compile_run_assert"}:
        run_part = f" && java {main_class}"
    shell_cmd = f"javac {file_name}{run_part}"
    command = [
        "docker",
        "run",
        "--rm",
        "--network",
        "none",
        "--memory",
        "512m",
        "--cpus",
        "1",
        "--pids-limit",
        "128",
        "-v",
        f"{cwd}:/work:rw",
        "-w",
        "/work",
        image,
        "bash",
        "-lc",
        shell_cmd,
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        status = "passed" if result.returncode == 0 else "failed"
        reason = "" if status == "passed" else "docker_test_failed"
        if status == "passed" and test_mode == "compile_run_assert":
            expected = item.get("expected_stdout_contains") or []
            if isinstance(expected, str):
                expected = [expected]
            for token in expected:
                if str(token) not in result.stdout:
                    status = "failed"
                    reason = "stdout_assertion_failed"
                    break
        return {
            "id": item.get("id"),
            "chapter_id": item.get("chapter_id"),
            "language": "java",
            "test": test_mode,
            "file": item.get("file"),
            "status": status,
            "failure_reason": reason,
            "steps": [{
                "name": "docker_java_test",
                "command": command,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "timed_out": False,
            }],
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "id": item.get("id"),
            "chapter_id": item.get("chapter_id"),
            "language": "java",
            "test": test_mode,
            "file": item.get("file"),
            "status": "failed",
            "failure_reason": "timeout",
            "steps": [{
                "name": "docker_java_test",
                "command": command,
                "returncode": None,
                "stdout": exc.stdout or "",
                "stderr": exc.stderr or "Timeout",
                "timed_out": True,
            }],
        }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run CODE_META tests in Docker.")
    parser.add_argument("--manifest", type=Path, default=Path("build/code_manifest.json"))
    parser.add_argument("--package-root", type=Path, default=Path.cwd())
    parser.add_argument("--image", default="eclipse-temurin:21-jdk")
    parser.add_argument("--timeout-sec", type=int, default=20)
    parser.add_argument("--report-json", type=Path, default=Path("build/test_reports/code_test_report_docker.json"))
    args = parser.parse_args(argv)

    if shutil.which("docker") is None:
        print("[ERROR] Docker not found.", file=sys.stderr)
        return 2
    package_root = args.package_root.resolve()
    manifest = load_json(resolve_path(str(args.manifest), package_root))
    results: list[dict[str, Any]] = []
    for item in manifest.get("items", []):
        if str(item.get("language", "")).lower() == "java" and str(item.get("test", "none")) != "none":
            results.append(run_docker_java(item, package_root, args.image, args.timeout_sec))
    summary = {
        "total": len(results),
        "passed": sum(1 for r in results if r.get("status") == "passed"),
        "failed": sum(1 for r in results if r.get("status") == "failed"),
    }
    report = {
        "schema_version": "1.0-experimental",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "image": args.image,
        "summary": summary,
        "results": results,
    }
    out = resolve_path(str(args.report_json), package_root)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Docker code tests: total={summary['total']} passed={summary['passed']} failed={summary['failed']}")
    print(f"Report: {out}")
    return 1 if summary["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
