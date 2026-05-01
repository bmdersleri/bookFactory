#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate GitHub Codespaces configuration for BookFactory."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys

try:
    from cloud_provider_base import CheckItem, render_markdown_report, write_json
except Exception:  # pragma: no cover - supports direct and imported execution
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from cloud_provider_base import CheckItem, render_markdown_report, write_json


REQUIRED_FILES = [
    ".devcontainer/devcontainer.json",
    ".devcontainer/Dockerfile",
    ".devcontainer/postCreateCommand.sh",
]

REQUIRED_TEMPLATES = [
    "templates/codespaces/.devcontainer/devcontainer.json",
    "templates/codespaces/.devcontainer/Dockerfile",
    "templates/codespaces/.devcontainer/postCreateCommand.sh",
    "templates/codespaces/.github/codespaces/README.md",
]


def _same_text(root: Path, left: str, right: str) -> bool:
    lpath = root / left
    rpath = root / right
    if not lpath.exists() or not rpath.exists():
        return False
    return lpath.read_text(encoding="utf-8", errors="replace") == rpath.read_text(encoding="utf-8", errors="replace")


def check(root: Path) -> list[CheckItem]:
    items: list[CheckItem] = []

    for rel in REQUIRED_FILES:
        path = root / rel
        if path.exists():
            items.append(CheckItem(rel, "OK", "found"))
        else:
            items.append(CheckItem(rel, "ERROR", "missing"))

    for rel in REQUIRED_TEMPLATES:
        path = root / rel
        if path.exists():
            items.append(CheckItem(rel, "OK", "template found"))
        else:
            items.append(CheckItem(rel, "ERROR", "template missing"))

    sync_pairs = [
        ("templates/codespaces/.devcontainer/devcontainer.json", ".devcontainer/devcontainer.json"),
        ("templates/codespaces/.devcontainer/Dockerfile", ".devcontainer/Dockerfile"),
        ("templates/codespaces/.devcontainer/postCreateCommand.sh", ".devcontainer/postCreateCommand.sh"),
        ("templates/codespaces/.github/codespaces/README.md", ".github/codespaces/README.md"),
    ]
    for template_rel, target_rel in sync_pairs:
        if _same_text(root, template_rel, target_rel):
            items.append(CheckItem(f"template sync: {target_rel}", "OK", "matches template"))
        else:
            items.append(CheckItem(f"template sync: {target_rel}", "WARN", "differs from template or missing"))

    config_path = root / ".devcontainer" / "devcontainer.json"
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
            items.append(CheckItem("devcontainer.json syntax", "OK", "valid JSON"))
            if "postCreateCommand" in config:
                items.append(CheckItem("postCreateCommand", "OK", str(config["postCreateCommand"])))
            else:
                items.append(CheckItem("postCreateCommand", "WARN", "not configured"))
            ports = config.get("forwardPorts", [])
            if 8501 in ports:
                items.append(CheckItem("dashboard port 8501", "OK", "forwarded"))
            else:
                items.append(CheckItem("dashboard port 8501", "WARN", "not forwarded"))
            env = config.get("containerEnv", {})
            if env.get("PUPPETEER_CACHE_DIR"):
                items.append(CheckItem("PUPPETEER_CACHE_DIR", "OK", str(env.get("PUPPETEER_CACHE_DIR"))))
            else:
                items.append(CheckItem("PUPPETEER_CACHE_DIR", "WARN", "not configured"))
        except Exception as exc:
            items.append(CheckItem("devcontainer.json syntax", "ERROR", str(exc)))

    script_path = root / ".devcontainer" / "postCreateCommand.sh"
    if script_path.exists():
        text = script_path.read_text(encoding="utf-8", errors="replace")
        if "python -m bookfactory doctor --soft" in text:
            items.append(CheckItem("doctor command", "OK", "postCreateCommand includes doctor --soft"))
        else:
            items.append(CheckItem("doctor command", "WARN", "postCreateCommand does not run doctor --soft"))
        if "pip install -e" in text:
            items.append(CheckItem("editable install", "OK", "postCreateCommand installs package"))
        else:
            items.append(CheckItem("editable install", "WARN", "package install not detected"))
        if "write_puppeteer_config.py" in text:
            items.append(CheckItem("Puppeteer config bootstrap", "OK", "postCreateCommand writes config"))
        else:
            items.append(CheckItem("Puppeteer config bootstrap", "ERROR", "postCreateCommand does not write Puppeteer config"))

    dockerfile = root / ".devcontainer" / "Dockerfile"
    if dockerfile.exists():
        docker_text = dockerfile.read_text(encoding="utf-8", errors="replace")
        for token in ["openjdk-17-jdk", "pandoc", "@mermaid-js/mermaid-cli", "git"]:
            status = "OK" if token in docker_text else "WARN"
            detail = "configured" if token in docker_text else "not detected"
            items.append(CheckItem(f"Dockerfile dependency: {token}", status, detail))
        if "@mermaid-js/mermaid-cli@" in docker_text:
            items.append(CheckItem("Mermaid CLI version pin", "OK", "version pinned"))
        else:
            items.append(CheckItem("Mermaid CLI version pin", "WARN", "not pinned"))
        if "chrome-headless-shell" in docker_text and "puppeteer" in docker_text:
            items.append(CheckItem("Dockerfile Puppeteer Chrome", "OK", "chrome-headless-shell install configured"))
        else:
            items.append(CheckItem("Dockerfile Puppeteer Chrome", "ERROR", "Puppeteer Chrome install not configured"))

    if (root / "tools" / "cloud" / "write_puppeteer_config.py").exists():
        items.append(CheckItem("Puppeteer helper", "OK", "tools/cloud/write_puppeteer_config.py found"))
    else:
        items.append(CheckItem("Puppeteer helper", "ERROR", "tools/cloud/write_puppeteer_config.py missing"))

    if shutil.which("git"):
        items.append(CheckItem("local git", "OK", shutil.which("git") or ""))
    else:
        items.append(CheckItem("local git", "WARN", "not found in current environment"))

    if (root / "pyproject.toml").exists():
        items.append(CheckItem("pyproject.toml", "OK", "found"))
    else:
        items.append(CheckItem("pyproject.toml", "WARN", "missing; editable install may fail"))

    return items


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Check BookFactory GitHub Codespaces configuration.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root")
    parser.add_argument("--report-json", type=Path, default=Path("build/codespaces_check_report.json"))
    parser.add_argument("--report-md", type=Path, default=Path("build/codespaces_check_report.md"))
    parser.add_argument("--fail-on-error", action="store_true", help="Return non-zero if errors are found")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    items = check(root)
    errors = [item for item in items if item.status == "ERROR"]

    data = {
        "provider": "github_codespaces",
        "root": str(root),
        "ok": not errors,
        "items": [item.to_dict() for item in items],
    }
    report_json = args.report_json if args.report_json.is_absolute() else root / args.report_json
    report_md = args.report_md if args.report_md.is_absolute() else root / args.report_md
    write_json(report_json, data)
    report_md.parent.mkdir(parents=True, exist_ok=True)
    report_md.write_text(render_markdown_report("BookFactory GitHub Codespaces Kontrol Raporu", items), encoding="utf-8")

    print(report_md.read_text(encoding="utf-8"))
    if errors and args.fail_on_error:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
