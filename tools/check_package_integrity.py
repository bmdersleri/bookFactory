#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check release package integrity for Parametric Computer Book Factory.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    tomllib = None


FORBIDDEN_PARTS = {"__pycache__", ".git"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo", ".bak", ".tmp"}
FORBIDDEN_NAMES = {".DS_Store", "Thumbs.db"}
EXCLUDED_DIRS = {
    ".eggs",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "build",
    "dist",
    "node_modules",
    "venv",
}
EXCLUDED_SUFFIXES = {".egg-info"}


def is_excluded_dir_name(name: str) -> bool:
    return (
        name in EXCLUDED_DIRS
        or name.startswith("pytest-cache-files-")
        or name.endswith(tuple(EXCLUDED_SUFFIXES))
    )


def iter_project_files(root: Path):
    for current, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            dirname for dirname in dirnames
            if not is_excluded_dir_name(dirname)
        ]
        current_path = Path(current)
        for filename in filenames:
            yield current_path / filename


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Check Book Factory package integrity.")
    parser.add_argument("root", nargs="?", default=".", help="Package root")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not (root / "README.md").exists():
        errors.append("Missing README.md")
    if not (root / "package_manifest.json").exists():
        errors.append("Missing package_manifest.json")
    if not (root / "core").is_dir():
        errors.append("Missing core/ directory")
    if not (root / "tools").is_dir():
        errors.append("Missing tools/ directory")

    # duplicate numeric prefixes in core
    prefix_map: dict[str, list[Path]] = {}
    core = root / "core"
    if core.exists():
        for path in core.glob("*.md"):
            prefix = path.name.split("_", 1)[0]
            if prefix.isdigit():
                prefix_map.setdefault(prefix, []).append(path)
        for prefix, paths in prefix_map.items():
            if len(paths) > 1:
                errors.append(f"Duplicate core numeric prefix {prefix}: {', '.join(p.name for p in paths)}")

    # forbidden files
    for path in iter_project_files(root):
        rel = path.relative_to(root)
        if any(part in FORBIDDEN_PARTS for part in rel.parts):
            errors.append(f"Forbidden path in release: {rel}")
        if path.name in FORBIDDEN_NAMES:
            errors.append(f"Forbidden OS file in release: {rel}")
        if path.suffix in FORBIDDEN_SUFFIXES:
            errors.append(f"Forbidden temporary/compiled file in release: {rel}")

    # JSON parse
    for path in iter_project_files(root):
        if path.suffix != ".json":
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"Invalid JSON: {path.relative_to(root)} — {exc}")

    # YAML parse
    try:
        import yaml  # type: ignore
        for path in iter_project_files(root):
            if path.suffix not in {".yaml", ".yml"}:
                continue
            try:
                yaml.safe_load(path.read_text(encoding="utf-8"))
            except Exception as exc:
                errors.append(f"Invalid YAML: {path.relative_to(root)} — {exc}")
    except Exception:
        warnings.append("PyYAML unavailable; YAML parse checks skipped.")

    # Python syntax without writing __pycache__
    for path in iter_project_files(root):
        if path.suffix != ".py":
            continue
        try:
            source = path.read_text(encoding="utf-8")
            compile(source, str(path), "exec")
        except Exception as exc:
            errors.append(f"Python syntax error: {path.relative_to(root)} — {exc}")

    pyproject = root / "pyproject.toml"
    package_init = root / "bookfactory" / "__init__.py"
    if pyproject.exists() and package_init.exists():
        try:
            if tomllib is None:
                warnings.append("tomllib unavailable; package metadata consistency check skipped.")
                project = None
            else:
                project = tomllib.loads(pyproject.read_text(encoding="utf-8"))["project"]
            init_text = package_init.read_text(encoding="utf-8")
            version_line = next(
                line for line in init_text.splitlines()
                if line.startswith("__version__")
            )
            package_version = version_line.split("=", 1)[1].strip().strip('"')
            if project is not None:
                if project["version"] != package_version:
                    errors.append(
                        "Version mismatch: "
                        f"pyproject.toml={project['version']} "
                        f"bookfactory.__version__={package_version}"
                    )
                scripts = project.get("scripts", {})
                if scripts.get("bookfactory") != "bookfactory.cli:main":
                    errors.append("Invalid bookfactory console script entry point")
                if scripts.get("bookfactory-studio") != "bookfactory_studio.app:main":
                    errors.append("Invalid bookfactory-studio console script entry point")
        except Exception as exc:
            errors.append(f"Package metadata consistency check failed: {exc}")

    print("# Package Integrity Report\n")
    if errors:
        print("## Errors")
        for e in errors:
            print(f"- {e}")
    else:
        print("## Errors\n\nNo errors found.")

    print()
    if warnings:
        print("## Warnings")
        for w in warnings:
            print(f"- {w}")
    else:
        print("## Warnings\n\nNo warnings found.")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
