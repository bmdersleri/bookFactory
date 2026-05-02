# -*- coding: utf-8 -*-
"""Java local test adapter."""
from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from .base_adapter import LanguageAdapter, normalize_args
from tools.utils.process_utils import run_command


class JavaAdapter(LanguageAdapter):
    language = "java"

    def __init__(self, *, javac: str = "javac", java: str = "java", default_timeout: int = 10) -> None:
        super().__init__(default_timeout=default_timeout)
        self.javac = javac
        self.java = java
        self.javac_path = shutil.which(javac) or javac
        self.java_path = shutil.which(java) or java

    def executable_available(self) -> bool:
        return shutil.which(self.javac) is not None and shutil.which(self.java) is not None

    def unavailable_reason(self) -> str:
        return "java_or_javac_not_found"

    def compile_step(self, item: dict[str, Any], code_path: Path, timeout: int) -> dict[str, Any]:
        return run_command([self.javac_path, "-encoding", "UTF-8", code_path.name], code_path.parent, timeout)

    def run_step(self, item: dict[str, Any], code_path: Path, timeout: int) -> dict[str, Any]:
        main_class = str(item.get("main_class") or code_path.stem)
        stdin = item.get("stdin")
        args = normalize_args(item.get("args"))
        return run_command(
            [self.java_path, "-Dfile.encoding=UTF-8", main_class, *args],
            code_path.parent,
            timeout,
            stdin=str(stdin) if stdin is not None else None,
        )
