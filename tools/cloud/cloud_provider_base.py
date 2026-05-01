#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared helpers for optional cloud IDE integrations."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json


@dataclass
class CheckItem:
    name: str
    status: str
    detail: str = ""

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def render_markdown_report(title: str, items: list[CheckItem]) -> str:
    ok_count = sum(1 for item in items if item.status == "OK")
    warn_count = sum(1 for item in items if item.status == "WARN")
    error_count = sum(1 for item in items if item.status == "ERROR")
    lines = [
        f"# {title}",
        "",
        "## Özet",
        "",
        f"- OK: {ok_count}",
        f"- WARN: {warn_count}",
        f"- ERROR: {error_count}",
        "",
        "## Kontroller",
        "",
        "| Kontrol | Durum | Açıklama |",
        "|---|---|---|",
    ]
    for item in items:
        detail = item.detail.replace("|", "\\|")
        lines.append(f"| {item.name} | {item.status} | {detail} |")
    lines.append("")
    return "\n".join(lines)
