# -*- coding: utf-8 -*-
"""Python local test adapter."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from .base_adapter import ExecutableAdapter, normalize_args
from tools.utils.process_utils import run_command


class PythonAdapter(ExecutableAdapter):
    language = "python"
    executable_name = sys.executable or "python"

    def compile_step(self, item: dict[str, Any], code_path: Path, timeout: int) -> dict[str, Any]:
        return run_command([self.executable_path, "-m", "py_compile", code_path.name], code_path.parent, timeout)

    def run_step(self, item: dict[str, Any], code_path: Path, timeout: int) -> dict[str, Any]:
        stdin = item.get("stdin")
        args = normalize_args(item.get("args"))
        return run_command(
            [self.executable_path, code_path.name, *args],
            code_path.parent,
            timeout,
            stdin=str(stdin) if stdin is not None else None,
        )
