#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Find Puppeteer Chrome and write a Mermaid-compatible Puppeteer config."""
from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path

DEFAULT_ARGS = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-dev-shm-usage",
]


def _candidate_paths() -> list[Path]:
    candidates: list[Path] = []

    env_path = os.environ.get("PUPPETEER_EXECUTABLE_PATH")
    if env_path:
        candidates.append(Path(env_path))

    for binary in ("chrome-headless-shell", "google-chrome", "chromium", "chromium-browser"):
        found = shutil.which(binary)
        if found:
            candidates.append(Path(found))

    glob_roots = [
        Path(os.environ.get("PUPPETEER_CACHE_DIR", "")),
        Path("/usr/local/share/puppeteer"),
        Path.home() / ".cache" / "puppeteer",
        Path("/root/.cache/puppeteer"),
    ]
    patterns = [
        "chrome-headless-shell/**/chrome-headless-shell-linux64/chrome-headless-shell",
        "chrome-headless-shell/**/chrome-headless-shell",
        "chrome/**/chrome-linux64/chrome",
        "chrome/**/chrome",
    ]
    for root in glob_roots:
        if not str(root) or not root.exists():
            continue
        for pattern in patterns:
            candidates.extend(root.glob(pattern))

    # Preserve order while removing duplicates.
    unique: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate)
        if key not in seen:
            seen.add(key)
            unique.append(candidate)
    return unique


def find_chrome() -> Path | None:
    for candidate in _candidate_paths():
        try:
            if candidate.exists() and os.access(candidate, os.X_OK):
                return candidate.resolve()
        except OSError:
            continue
    return None


def write_config(output: Path, executable: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    config = {
        "executablePath": str(executable),
        "args": DEFAULT_ARGS,
    }
    output.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write Puppeteer config for Mermaid CLI.")
    parser.add_argument("--output", type=Path, default=Path("configs/puppeteer_config.json"))
    parser.add_argument("--check", action="store_true", help="Return non-zero if Chrome cannot be found.")
    args = parser.parse_args(argv)

    chrome = find_chrome()
    if chrome is None:
        print("Puppeteer Chrome executable bulunamadı.")
        return 1 if args.check else 0

    write_config(args.output, chrome)
    print(f"Puppeteer config yazıldı: {args.output} -> {chrome}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
