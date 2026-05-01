# -*- coding: utf-8 -*-
"""JavaScript/Node.js local test adapter."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .base_adapter import ExecutableAdapter, normalize_args
from tools.utils.process_utils import run_command


class JavaScriptAdapter(ExecutableAdapter):
    language = "javascript"
    executable_name = "node"

    def compile_step(self, item: dict[str, Any], code_path: Path, timeout: int) -> dict[str, Any]:
        return run_command([self.executable_path, "--check", code_path.name], code_path.parent, timeout)

    def run_step(self, item: dict[str, Any], code_path: Path, timeout: int) -> dict[str, Any]:
        stdin = item.get("stdin")
        args = normalize_args(item.get("args"))
        return run_command(
            [self.executable_path, code_path.name, *args],
            code_path.parent,
            timeout,
            stdin=str(stdin) if stdin is not None else None,
        )
