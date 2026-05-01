#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Environment checker for Parametric Computer Book Factory.

Checks external tools commonly used in the post-production pipeline:
- Python
- Pandoc
- Mermaid CLI (mmdc)
- Node.js / npm
- Java
- Git
- Puppeteer/Chrome availability for Mermaid rendering

Use --soft to report missing tools without failing. Unlike earlier versions,
--soft still performs version checks; it only changes the final exit behavior.
"""
from __future__ import annotations

import argparse
import importlib.util
import os
import signal
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ToolCheck:
    name: str
    command: str
    version_args: list[str]
    required: bool = True


TOOLS = [
    ToolCheck("python", sys.executable, ["--version"], True),
    ToolCheck("pandoc", "pandoc", ["--version"], True),
    ToolCheck("mermaid_cli", "mmdc", ["--version"], False),
    ToolCheck("node", "node", ["--version"], False),
    ToolCheck("npm", "npm", ["--version"], False),
    ToolCheck("java", "java", ["-version"], False),
    ToolCheck("git", "git", ["--version"], False),
]


def run_version(cmd: str, args: list[str]) -> str:
    timeout = int(os.environ.get("BOOKFACTORY_VERSION_CHECK_TIMEOUT_SEC", "10"))
    popen_kwargs = {
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "text": True,
    }
    if os.name == "nt":
        popen_kwargs["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    else:
        popen_kwargs["start_new_session"] = True
    proc = subprocess.Popen([cmd, *args], **popen_kwargs)
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        try:
            if os.name == "nt":
                proc.kill()
            else:
                os.killpg(proc.pid, signal.SIGKILL)
        except Exception:
            proc.kill()
        proc.communicate()
        raise RuntimeError(f"version check timed out after {timeout} seconds")
    text = (stdout or stderr or "").strip().splitlines()
    return text[0] if text else "version output unavailable"


def _load_puppeteer_helper():
    helper = Path(__file__).resolve().parent / "cloud" / "write_puppeteer_config.py"
    if not helper.exists():
        return None
    spec = importlib.util.spec_from_file_location("bookfactory_puppeteer_helper", helper)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_puppeteer_chrome() -> tuple[str, str]:
    module = _load_puppeteer_helper()
    if module is None or not hasattr(module, "find_chrome"):
        return "WARN", "helper not found"
    chrome = module.find_chrome()
    if chrome is None:
        return "WARN", "Chrome/headless shell not found; Mermaid may fail until Puppeteer installs it"
    return "OK", str(chrome)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Check local environment for Book Factory.")
    parser.add_argument("--soft", action="store_true", help="Do not fail if a required tool is missing or version check fails.")
    args = parser.parse_args(argv)

    missing_required: list[str] = []
    print("# Environment check\n")

    for tool in TOOLS:
        path = shutil.which(tool.command) if tool.command != sys.executable else sys.executable
        if not path:
            print(f"- {tool.name}: MISSING")
            if tool.required:
                missing_required.append(tool.name)
            continue

        try:
            version = run_version(path, tool.version_args)
            print(f"- {tool.name}: OK — {path} — {version}")
        except Exception as exc:
            print(f"- {tool.name}: FOUND BUT VERSION CHECK FAILED — {path} — {exc}")
            if tool.required:
                missing_required.append(tool.name)

    chrome_status, chrome_detail = check_puppeteer_chrome()
    print(f"- puppeteer_chrome: {chrome_status} — {chrome_detail}")

    if missing_required and not args.soft:
        print("\n[ERROR] Missing or invalid required tools: " + ", ".join(missing_required), file=sys.stderr)
        return 1

    if missing_required:
        print("\n[WARN] Missing or invalid required tools, but --soft was used: " + ", ".join(missing_required))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
