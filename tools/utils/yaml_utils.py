#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared YAML/JSON helpers for BookFactory tools."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def parse_scalar(value: str) -> Any:
    value = value.strip()
    lowered = value.lower()
    if lowered in {"", "null", "none", "~"}:
        return None if lowered else ""
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    value = _strip_quotes(value)
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def _next_container(lines: list[str], current_index: int, indent: int) -> Any:
    for nxt in lines[current_index + 1:]:
        if not nxt.strip() or nxt.lstrip().startswith("#"):
            continue
        nxt_indent = len(nxt) - len(nxt.lstrip(" "))
        if nxt_indent <= indent:
            break
        return [] if nxt.strip().startswith("-") else {}
    return {}


def minimal_yaml_load(text: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]
    lines = text.splitlines()

    def parent_for(indent: int) -> Any:
        while stack and stack[-1][0] >= indent:
            stack.pop()
        return stack[-1][1]

    for i, raw in enumerate(lines):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()
        parent = parent_for(indent)

        if stripped.startswith("- "):
            item_text = stripped[2:].strip()
            if not isinstance(parent, list):
                continue
            if ":" in item_text:
                key, value = item_text.split(":", 1)
                item: dict[str, Any] = {}
                value = value.strip()
                if value == "":
                    item[key.strip()] = _next_container(lines, i, indent)
                    parent.append(item)
                    stack.append((indent, item))
                    stack.append((indent + 2, item[key.strip()]))
                else:
                    item[key.strip()] = parse_scalar(value)
                    parent.append(item)
                    stack.append((indent, item))
            else:
                parent.append(parse_scalar(item_text))
            continue

        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "":
            container = _next_container(lines, i, indent)
            if isinstance(parent, dict):
                parent[key] = container
                stack.append((indent, container))
            elif isinstance(parent, list):
                item = {key: container}
                parent.append(item)
                stack.append((indent, container))
        else:
            if isinstance(parent, dict):
                parent[key] = parse_scalar(value)
            elif isinstance(parent, list):
                parent.append({key: parse_scalar(value)})
    return root


def load_yaml(path: Path | str) -> dict[str, Any]:
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text) or {}
    except Exception:
        return minimal_yaml_load(text)


def load_data(path: Path | str) -> dict[str, Any]:
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return load_yaml(path)


def _yaml_scalar(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if "\n" in text:
        return "|\n" + "\n".join("  " + line for line in text.splitlines())
    return '"' + text.replace('"', '\\"') + '"'


def dump_yaml(data: dict[str, Any], path: Path | str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        import yaml  # type: ignore
        path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
        return
    except Exception:
        pass

    lines: list[str] = []

    def emit(obj: Any, indent: int = 0, key: str | None = None) -> None:
        prefix = " " * indent
        if isinstance(obj, dict):
            if key is not None:
                lines.append(f"{prefix}{key}:")
                indent += 2
            for k, v in obj.items():
                emit(v, indent, str(k))
        elif isinstance(obj, list):
            if key is not None:
                lines.append(f"{prefix}{key}:")
                indent += 2
                prefix = " " * indent
            for item in obj:
                if isinstance(item, dict):
                    lines.append(f"{prefix}-")
                    for k, v in item.items():
                        emit(v, indent + 2, str(k))
                else:
                    lines.append(f"{prefix}- {_yaml_scalar(item)}")
        else:
            if key is None:
                lines.append(_yaml_scalar(obj))
            else:
                lines.append(f"{prefix}{key}: {_yaml_scalar(obj)}")

    emit(data)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def dump_data(data: dict[str, Any], json_path: Path | str, yaml_path: Path | str | None = None) -> None:
    json_path = Path(json_path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if yaml_path is not None:
        dump_yaml(data, yaml_path)
