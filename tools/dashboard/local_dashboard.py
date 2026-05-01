#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Local Streamlit dashboard for BookFactory.

v2.11.0 converts the dashboard from a stub into a read-only control panel
that summarizes build artifacts, code-test reports, export outputs, indexing
outputs, GitHub sync outputs and Codespaces validation reports.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def _is_running_in_streamlit() -> bool:
    """Return True when this file is executed by Streamlit's script runner."""
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        return get_script_run_ctx() is not None
    except Exception:
        return False


def _load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _file_info(path: Path, root: Path) -> dict[str, Any]:
    try:
        stat = path.stat()
        rel = path.relative_to(root)
    except Exception:
        stat = path.stat()
        rel = path
    return {
        "path": str(rel).replace("\\", "/"),
        "size_kb": round(stat.st_size / 1024, 2),
        "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
    }


def discover_reports(root: Path) -> dict[str, list[Path]]:
    build = root / "build"
    examples = root / "examples"
    candidates = {
        "test_reports": [
            build / "test_reports",
            examples / "minimal_book" / "build" / "test_reports",
        ],
        "codespaces_reports": [build],
        "github_reports": [build],
        "index_reports": [build / "index", build / "indexing", build],
        "export_outputs": [build / "export", build / "exports", root / "exports"],
        "code_pages": [build / "code_pages", build / "github_repo" / "docs" / "kodlar"],
    }
    result: dict[str, list[Path]] = {key: [] for key in candidates}
    for key, dirs in candidates.items():
        seen: set[Path] = set()
        for directory in dirs:
            if not directory.exists():
                continue
            patterns = {
                "test_reports": ["*.json", "*.md"],
                "codespaces_reports": ["codespaces*_report*.json", "codespaces*_report*.md"],
                "github_reports": ["github*_report*.json", "github*_report*.md", "code_manifest_github.*"],
                "index_reports": ["*glossary*", "*index*", "*.json", "*.md"],
                "export_outputs": ["*.md", "*.html", "*.epub"],
                "code_pages": ["*.md"],
            }[key]
            for pattern in patterns:
                for path in directory.rglob(pattern):
                    if path.is_file() and path not in seen:
                        result[key].append(path)
                        seen.add(path)
    for key in result:
        result[key].sort(key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True)
    return result


def summarize_test_report(path: Path) -> dict[str, Any]:
    data = _load_json(path)
    summary = data.get("summary", {}) if isinstance(data, dict) else {}
    return {
        "file": path.name,
        "total": summary.get("total", 0),
        "passed": summary.get("passed", 0),
        "failed": summary.get("failed", 0),
        "skipped": summary.get("skipped", 0),
    }


def render_cli_hint(root: Path, profile: Path) -> str:
    return "\n".join([
        "python -m bookfactory doctor --soft",
        "python -m bookfactory codespaces-check --fail-on-error",
        "python -m bookfactory test-minimal --fail-on-error",
        f"python -m bookfactory build-index --profile {profile}",
        f"python -m bookfactory export --profile {profile} --format html --merge-if-missing",
        "python -m bookfactory render-code-pages --manifest build/code_manifest_github.json --test-report build/test_reports/code_test_report.json",
    ])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run/check optional local BookFactory dashboard.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--profile", type=Path, default=Path("examples/minimal_book/configs/post_production_profile_minimal.yaml"))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    try:
        import streamlit as st  # type: ignore
    except Exception:
        print("Streamlit is not installed. Install optional dashboard dependencies with:")
        print('  pip install -e ".[dashboard]"')
        return 0 if args.check else 2

    root = args.root.resolve()
    profile = args.profile if args.profile.is_absolute() else (root / args.profile)

    if args.check:
        print("Streamlit is available. Dashboard can be launched with:")
        print("  python -m streamlit run tools/dashboard/local_dashboard.py -- --root " + str(root) + " --profile " + str(profile))
        return 0

    # When invoked through `python -m bookfactory dashboard`, print the canonical
    # Streamlit command instead of trying to start a nested server. When Streamlit
    # itself runs this file, render the dashboard.
    if not _is_running_in_streamlit():
        print("Launch the dashboard with:")
        print("  python -m streamlit run tools/dashboard/local_dashboard.py -- --root " + str(root) + " --profile " + str(profile))
        return 0

    reports = discover_reports(root)

    st.set_page_config(page_title="BookFactory Dashboard", layout="wide")
    st.title("BookFactory Local Control Panel")
    st.caption("v2.11.0 — read-only project status dashboard")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Test report files", len(reports["test_reports"]))
    c2.metric("Export outputs", len(reports["export_outputs"]))
    c3.metric("Code pages", len(reports["code_pages"]))
    c4.metric("GitHub artifacts", len(reports["github_reports"]))

    with st.expander("Project paths", expanded=True):
        st.write("**Root:**", str(root))
        st.write("**Profile:**", str(profile))
        st.code(render_cli_hint(root, profile), language="bash")

    tab_tests, tab_exports, tab_index, tab_github, tab_codespaces = st.tabs([
        "Code tests", "Exports", "Glossary / Index", "GitHub / Code pages", "Codespaces"
    ])

    with tab_tests:
        json_reports = [p for p in reports["test_reports"] if p.suffix == ".json"]
        if json_reports:
            rows = [summarize_test_report(p) for p in json_reports]
            st.dataframe(rows, use_container_width=True)
            selected = st.selectbox("Inspect test report", json_reports, format_func=lambda p: str(p.relative_to(root)))
            data = _load_json(selected)
            st.json(data)
        else:
            st.info("No JSON test report found yet. Run `python -m bookfactory test-minimal --fail-on-error`.")

    with tab_exports:
        if reports["export_outputs"]:
            st.dataframe([_file_info(p, root) for p in reports["export_outputs"]], use_container_width=True)
        else:
            st.info("No export output found yet. Run the export command shown above.")

    with tab_index:
        index_files = reports["index_reports"][:50]
        if index_files:
            st.dataframe([_file_info(p, root) for p in index_files], use_container_width=True)
        else:
            st.info("No glossary/index artifact found yet. Run `bookfactory build-index`.")

    with tab_github:
        github_files = reports["github_reports"][:50]
        code_pages = reports["code_pages"][:100]
        if github_files:
            st.subheader("GitHub sync artifacts")
            st.dataframe([_file_info(p, root) for p in github_files], use_container_width=True)
        if code_pages:
            st.subheader("Rendered code pages")
            st.dataframe([_file_info(p, root) for p in code_pages], use_container_width=True)
        if not github_files and not code_pages:
            st.info("No GitHub/code page artifact found yet.")

    with tab_codespaces:
        cs_files = reports["codespaces_reports"][:50]
        if cs_files:
            st.dataframe([_file_info(p, root) for p in cs_files], use_container_width=True)
        else:
            st.info("No Codespaces report found yet. Run `bookfactory codespaces-check --fail-on-error`.")

    st.warning("Dashboard is read-only. It does not display secrets and does not push to remote repositories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
