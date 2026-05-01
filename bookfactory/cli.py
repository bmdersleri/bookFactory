#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BookFactory command-line orchestrator."""
from __future__ import annotations

import argparse
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

from . import __version__


def _load_module_from_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _system_exit_code(exc: SystemExit) -> int:
    if isinstance(exc.code, int):
        return exc.code
    return 0 if exc.code is None else 1


def run_python(script: Path, args: list[str], root: Path) -> int:
    command = [sys.executable]
    if os.environ.get("BOOKFACTORY_PYTHON_NO_SITE") == "1":
        command.append("-S")
    command.extend([str(script), *args])
    print("$ " + " ".join(str(part) for part in command), flush=True)

    if os.environ.get("BOOKFACTORY_SUBPROCESS_MODE") == "1":
        env = os.environ.copy()
        env.setdefault("PYTHONDONTWRITEBYTECODE", "1")
        completed = subprocess.run(command, cwd=str(root), env=env)
        return int(completed.returncode)

    old_cwd = Path.cwd()
    try:
        os.chdir(root)
        module_name = "bookfactory_tool_" + script.stem + "_" + str(abs(hash(str(script))))
        module = _load_module_from_path(module_name, script)
        if not hasattr(module, "main"):
            raise RuntimeError(f"Tool has no main(argv) function: {script}")
        try:
            return int(module.main(args))
        except SystemExit as exc:
            return _system_exit_code(exc)
    finally:
        os.chdir(old_cwd)


def script(root: Path, relative: str) -> Path:
    return root / relative


def cmd_doctor(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    return run_python(script(root, "tools/check_environment.py"), ["--soft"] if args.soft else [], root)


def cmd_validate(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    return run_python(script(root, "tools/validate_manifest.py"), [str(args.manifest)], root)


def cmd_build(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    command_args = ["--profile", str(args.profile)]
    if args.dry_run:
        command_args.append("--dry-run")
    return run_python(script(root, "tools/postproduction/post_production_pipeline.py"), command_args, root)


def cmd_extract_code(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    command_args = ["--package-root", str(root), "--out-dir", str(args.out_dir), "--manifest", str(args.manifest), "--yaml-manifest", str(args.yaml_manifest)]
    if args.chapters_dir:
        command_args.extend(["--chapters-dir", str(args.chapters_dir)])
    for file in args.files or []:
        command_args.extend(["--file", str(file)])
    if args.strict:
        command_args.append("--strict")
    return run_python(script(root, "tools/code/extract_code_blocks.py"), command_args, root)


def cmd_validate_code_meta(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    return run_python(
        script(root, "tools/code/validate_code_meta.py"),
        [str(args.manifest), "--package-root", str(root)],
        root,
    )


def cmd_test_code(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    if args.chapters_dir or args.files:
        extract_args = argparse.Namespace(
            root=root,
            chapters_dir=args.chapters_dir,
            files=args.files,
            out_dir=args.out_dir,
            manifest=args.manifest,
            yaml_manifest=args.yaml_manifest,
            strict=False,
        )
        code = cmd_extract_code(extract_args)
        if code != 0:
            return code
    validate_code = cmd_validate_code_meta(argparse.Namespace(root=root, manifest=args.manifest))
    if validate_code != 0:
        return validate_code
    command_args = [
        "--manifest",
        str(args.manifest),
        "--package-root",
        str(root),
        "--report-json",
        str(args.report_json),
        "--report-md",
        str(args.report_md),
        "--timeout-sec",
        str(args.timeout_sec),
        "--javac",
        str(args.javac),
        "--java",
        str(args.java),
        "--python",
        str(getattr(args, "python", sys.executable)),
        "--node",
        str(getattr(args, "node", "node")),
    ]
    if args.fail_on_error:
        command_args.append("--fail-on-error")
    return run_python(script(root, "tools/code/run_code_tests.py"), command_args, root)


def cmd_repair_prompts(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    command_args = [
        "--test-report",
        str(args.test_report),
        "--manifest",
        str(args.manifest),
        "--out-dir",
        str(args.out_dir),
        "--package-root",
        str(root),
    ]
    return run_python(script(root, "tools/code/generate_llm_repair_prompt.py"), command_args, root)


def cmd_sync_github(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    command_args = [
        "--code-manifest", str(args.code_manifest),
        "--package-root", str(root),
        "--out-dir", str(args.out_dir),
        "--owner", str(args.owner),
        "--repo", str(args.repo),
        "--branch", str(args.branch),
        "--code-root", str(args.code_root),
        "--pages-root", str(args.pages_root),
        "--folder-style", str(args.folder_style),
        "--enriched-json", str(args.enriched_json),
        "--enriched-yaml", str(args.enriched_yaml),
        "--report-json", str(args.report_json),
        "--report-md", str(args.report_md),
    ]
    if args.test_report:
        command_args.extend(["--test-report", str(args.test_report)])
    if args.include_all:
        command_args.append("--include-all")
    if args.require_tests_passed:
        command_args.append("--require-tests-passed")
    if args.clean:
        command_args.append("--clean")
    if args.init_git:
        command_args.append("--init-git")
    if args.commit:
        command_args.append("--commit")
        command_args.extend(["--commit-message", str(args.commit_message)])
    if args.push:
        command_args.append("--push")
        command_args.extend(["--remote", str(args.remote)])
    return run_python(script(root, "tools/github/sync_code_repository.py"), command_args, root)


def cmd_qr_from_code(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    command_args = [
        "--code-manifest", str(args.code_manifest),
        "--output", str(args.output),
        "--output-prefix", str(args.output_prefix),
    ]
    if args.fail_on_empty:
        command_args.append("--fail-on-empty")
    if getattr(args, "strict_url", False):
        command_args.append("--strict-url")
    return run_python(script(root, "tools/postproduction/build_qr_manifest_from_code_manifest.py"), command_args, root)




def cmd_codespaces_init(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    command_args = ["--root", str(root)]
    if args.force:
        command_args.append("--force")
    return run_python(script(root, "tools/cloud/codespaces_init.py"), command_args, root)


def cmd_codespaces_check(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    command_args = [
        "--root", str(root),
        "--report-json", str(args.report_json),
        "--report-md", str(args.report_md),
    ]
    if args.fail_on_error:
        command_args.append("--fail-on-error")
    return run_python(script(root, "tools/cloud/codespaces_check.py"), command_args, root)


def cmd_build_index(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    module = _load_module_from_path("bookfactory_indexing", script(root, "tools/indexing/build_glossary_index.py"))
    profile = args.profile if args.profile.is_absolute() else (root / args.profile)
    return int(module.build(profile.resolve(), args.output_dir, args.fail_on_empty))


def cmd_dashboard(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    module = _load_module_from_path("bookfactory_dashboard", script(root, "tools/dashboard/local_dashboard.py"))
    argv = ["--root", str(root), "--profile", str(args.profile)]
    if args.check:
        argv.append("--check")
    return int(module.main(argv))


def cmd_render_code_pages(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    command_args = [
        "--manifest", str(args.manifest),
        "--package-root", str(root),
        "--out-dir", str(args.out_dir),
    ]
    if args.test_report:
        command_args.extend(["--test-report", str(args.test_report)])
    if args.clean:
        command_args.append("--clean")
    if args.index:
        command_args.extend(["--index", str(args.index)])
    return run_python(script(root, "tools/github/render_code_pages.py"), command_args, root)


def cmd_export(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    command_args = ["--profile", str(args.profile)]
    for fmt in args.formats or []:
        command_args.extend(["--format", str(fmt)])
    if args.merged_md:
        command_args.extend(["--merged-md", str(args.merged_md)])
    if args.output_dir:
        command_args.extend(["--output-dir", str(args.output_dir)])
    if args.merge_if_missing:
        command_args.append("--merge-if-missing")
    if args.dry_run:
        command_args.append("--dry-run")
    if args.require_pandoc:
        command_args.append("--require-pandoc")
    return run_python(script(root, "tools/export/export_book.py"), command_args, root)


def cmd_test_minimal(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    return cmd_test_code(
        argparse.Namespace(
            root=root,
            chapters_dir=Path("examples/minimal_book/chapters"),
            files=[],
            out_dir=Path("examples/minimal_book/build/code"),
            manifest=Path("examples/minimal_book/build/code_manifest.json"),
            yaml_manifest=Path("examples/minimal_book/build/code_manifest.yaml"),
            report_json=Path("examples/minimal_book/build/test_reports/code_test_report.json"),
            report_md=Path("examples/minimal_book/build/test_reports/code_test_report.md"),
            timeout_sec=args.timeout_sec,
            javac=args.javac,
            java=args.java,
            python=getattr(args, "python", sys.executable),
            node=getattr(args, "node", "node"),
            fail_on_error=args.fail_on_error,
        )
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bookfactory", description="Parametric Computer Book Factory CLI")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="BookFactory package/project root. Default: current directory.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("version", help="Show BookFactory version.")
    p.set_defaults(func=lambda args: (print(__version__) or 0))

    p = sub.add_parser("doctor", help="Check local environment.")
    p.add_argument("--soft", action="store_true", help="Do not fail on missing required tools.")
    p.set_defaults(func=cmd_doctor)

    p = sub.add_parser("validate", help="Validate book manifest.")
    p.add_argument("--manifest", type=Path, required=True)
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("build", help="Run post-production pipeline.")
    p.add_argument("--profile", type=Path, required=True)
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_build)

    p = sub.add_parser("extract-code", help="Extract CODE_META code blocks.")
    p.add_argument("--chapters-dir", type=Path)
    p.add_argument("--file", dest="files", action="append", type=Path, default=[])
    p.add_argument("--out-dir", type=Path, default=Path("build/code"))
    p.add_argument("--manifest", type=Path, default=Path("build/code_manifest.json"))
    p.add_argument("--yaml-manifest", type=Path, default=Path("build/code_manifest.yaml"))
    p.add_argument("--strict", action="store_true")
    p.set_defaults(func=cmd_extract_code)

    p = sub.add_parser("validate-code-meta", help="Validate CODE_META manifest.")
    p.add_argument("--manifest", type=Path, default=Path("build/code_manifest.json"))
    p.set_defaults(func=cmd_validate_code_meta)

    p = sub.add_parser("test-code", help="Extract and/or test CODE_META code blocks.")
    p.add_argument("--chapters-dir", type=Path)
    p.add_argument("--file", dest="files", action="append", type=Path, default=[])
    p.add_argument("--out-dir", type=Path, default=Path("build/code"))
    p.add_argument("--manifest", type=Path, default=Path("build/code_manifest.json"))
    p.add_argument("--yaml-manifest", type=Path, default=Path("build/code_manifest.yaml"))
    p.add_argument("--report-json", type=Path, default=Path("build/test_reports/code_test_report.json"))
    p.add_argument("--report-md", type=Path, default=Path("build/test_reports/code_test_report.md"))
    p.add_argument("--timeout-sec", type=int, default=10)
    p.add_argument("--javac", default="javac")
    p.add_argument("--java", default="java")
    p.add_argument("--python", default=sys.executable)
    p.add_argument("--node", default="node")
    p.add_argument("--fail-on-error", action="store_true")
    p.set_defaults(func=cmd_test_code)

    p = sub.add_parser("repair-prompts", help="Generate LLM repair prompts from failed code tests.")
    p.add_argument("--test-report", type=Path, default=Path("build/test_reports/code_test_report.json"))
    p.add_argument("--manifest", type=Path, default=Path("build/code_manifest.json"))
    p.add_argument("--out-dir", type=Path, default=Path("build/repair_prompts"))
    p.set_defaults(func=cmd_repair_prompts)

    p = sub.add_parser("sync-github", help="Stage tested code into a GitHub-ready repository layout.")
    p.add_argument("--code-manifest", type=Path, default=Path("build/code_manifest.json"))
    p.add_argument("--test-report", type=Path)
    p.add_argument("--out-dir", type=Path, default=Path("build/github_repo"))
    p.add_argument("--owner", default="example-owner")
    p.add_argument("--repo", default="example-book-repo")
    p.add_argument("--branch", default="main")
    p.add_argument("--code-root", default="kodlar")
    p.add_argument("--pages-root", default="docs/kodlar")
    p.add_argument("--folder-style", choices=["slug", "numbered"], default="numbered")
    p.add_argument("--include-all", action="store_true")
    p.add_argument("--require-tests-passed", action="store_true")
    p.add_argument("--clean", action="store_true")
    p.add_argument("--enriched-json", type=Path, default=Path("build/code_manifest_github.json"))
    p.add_argument("--enriched-yaml", type=Path, default=Path("build/code_manifest_github.yaml"))
    p.add_argument("--report-json", type=Path, default=Path("build/github_sync_report.json"))
    p.add_argument("--report-md", type=Path, default=Path("build/github_sync_report.md"))
    p.add_argument("--init-git", action="store_true")
    p.add_argument("--commit", action="store_true")
    p.add_argument("--push", action="store_true")
    p.add_argument("--remote", default="origin")
    p.add_argument("--commit-message", default="Update BookFactory generated code")
    p.set_defaults(func=cmd_sync_github)

    p = sub.add_parser("qr-from-code", help="Build QR manifest from enriched/tested code manifest.")
    p.add_argument("--code-manifest", type=Path, default=Path("build/code_manifest_github.json"))
    p.add_argument("--output", type=Path, default=Path("build/qr_manifest.yaml"))
    p.add_argument("--output-prefix", default="assets/auto/qr")
    p.add_argument("--fail-on-empty", action="store_true")
    p.add_argument("--strict-url", action="store_true")
    p.set_defaults(func=cmd_qr_from_code)

    p = sub.add_parser("render-code-pages", help="Render rich Markdown pages from enriched CODE_META manifest.")
    p.add_argument("--manifest", type=Path, default=Path("build/code_manifest_github.json"))
    p.add_argument("--test-report", type=Path)
    p.add_argument("--out-dir", type=Path, default=Path("build/code_pages"))
    p.add_argument("--index", type=Path)
    p.add_argument("--clean", action="store_true")
    p.set_defaults(func=cmd_render_code_pages)

    p = sub.add_parser("export", help="Export merged book content to Markdown, HTML, EPUB or split site outputs.")
    p.add_argument("--profile", type=Path, required=True)
    p.add_argument("--format", dest="formats", action="append", choices=["all", "markdown", "html", "epub", "site"], default=[])
    p.add_argument("--merged-md", type=Path)
    p.add_argument("--output-dir", type=Path)
    p.add_argument("--merge-if-missing", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--require-pandoc", action="store_true")
    p.set_defaults(func=cmd_export)

    p = sub.add_parser("build-index", help="Build deterministic glossary and section-referenced back index.")
    p.add_argument("--profile", type=Path, required=True)
    p.add_argument("--output-dir", type=Path)
    p.add_argument("--fail-on-empty", action="store_true")
    p.set_defaults(func=cmd_build_index)

    p = sub.add_parser("codespaces-init", help="Create or refresh GitHub Codespaces devcontainer files.")
    p.add_argument("--force", action="store_true", help="Overwrite existing Codespaces files.")
    p.set_defaults(func=cmd_codespaces_init)

    p = sub.add_parser("codespaces-check", help="Validate GitHub Codespaces devcontainer files.")
    p.add_argument("--report-json", type=Path, default=Path("build/codespaces_check_report.json"))
    p.add_argument("--report-md", type=Path, default=Path("build/codespaces_check_report.md"))
    p.add_argument("--fail-on-error", action="store_true")
    p.set_defaults(func=cmd_codespaces_check)


    p = sub.add_parser("dashboard", help="Run/check the optional local dashboard.")
    p.add_argument("--profile", type=Path, default=Path("examples/minimal_book/configs/post_production_profile_minimal.yaml"))
    p.add_argument("--check", action="store_true")
    p.set_defaults(func=cmd_dashboard)


    p = sub.add_parser("test-minimal", help="Run CODE_META tests for examples/minimal_book.")
    p.add_argument("--timeout-sec", type=int, default=10)
    p.add_argument("--javac", default="javac")
    p.add_argument("--java", default="java")
    p.add_argument("--python", default=sys.executable)
    p.add_argument("--node", default="node")
    p.add_argument("--fail-on-error", action="store_true")
    p.set_defaults(func=cmd_test_minimal)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))
