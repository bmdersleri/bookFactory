#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create or refresh GitHub Codespaces configuration for BookFactory.

v2.9.1 note: devcontainer content is copied from templates/codespaces so that
there is a single source of truth instead of duplicated large string literals.
"""
from __future__ import annotations

import argparse
from pathlib import Path

TEMPLATE_TARGETS = [
    ("templates/codespaces/.devcontainer/devcontainer.json", ".devcontainer/devcontainer.json"),
    ("templates/codespaces/.devcontainer/Dockerfile", ".devcontainer/Dockerfile"),
    ("templates/codespaces/.devcontainer/postCreateCommand.sh", ".devcontainer/postCreateCommand.sh"),
    ("templates/codespaces/.github/codespaces/README.md", ".github/codespaces/README.md"),
]


def write_file(path: Path, content: str, force: bool) -> tuple[str, str]:
    if path.exists() and not force:
        return ("SKIP", f"exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    if path.name.endswith(".sh"):
        path.chmod(0o755)
    return ("WRITE", str(path))


def read_template(root: Path, template_rel: str) -> str:
    template = root / template_rel
    if not template.exists():
        raise FileNotFoundError(f"Codespaces template not found: {template}")
    return template.read_text(encoding="utf-8")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Create GitHub Codespaces files for BookFactory.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root")
    parser.add_argument("--force", action="store_true", help="Overwrite existing Codespaces files")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    print("# BookFactory Codespaces Init\n")
    for template_rel, target_rel in TEMPLATE_TARGETS:
        content = read_template(root, template_rel)
        status, detail = write_file(root / target_rel, content, args.force)
        print(f"- {status}: {detail}")

    print("\nSonraki kontrol: python -m bookfactory codespaces-check --fail-on-error")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
