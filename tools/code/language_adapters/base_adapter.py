# -*- coding: utf-8 -*-
"""Language adapter base classes for BookFactory code tests."""
from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from tools.utils.process_utils import run_command


SUPPORTED_TEST_MODES = {"compile", "compile_run", "compile_run_assert"}


def resolve_path(path_value: str, package_root: Path) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else package_root / path


def normalize_contains(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]


def normalize_args(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return value.split()
    if isinstance(value, list):
        return [str(v) for v in value]
    return []


class LanguageAdapter:
    """Base adapter. Subclasses implement compile_step and run_step."""

    language = "base"

    def __init__(self, *, default_timeout: int = 10) -> None:
        self.default_timeout = default_timeout

    def supports(self, item: dict[str, Any]) -> bool:
        return str(item.get("language", "")).lower() == self.language

    def executable_available(self) -> bool:
        return True

    def unavailable_reason(self) -> str:
        return f"{self.language}_runtime_not_found"

    def result_base(self, item: dict[str, Any], code_path: Path, test_mode: str) -> dict[str, Any]:
        return {
            "id": item.get("id"),
            "chapter_id": item.get("chapter_id"),
            "language": self.language,
            "test": test_mode,
            "file": item.get("file"),
            "code_path": str(code_path),
            "status": "passed",
            "steps": [],
            "assertions": [],
        }

    def compile_step(self, item: dict[str, Any], code_path: Path, timeout: int) -> dict[str, Any]:
        raise NotImplementedError

    def run_step(self, item: dict[str, Any], code_path: Path, timeout: int) -> dict[str, Any]:
        raise NotImplementedError

    def assert_outputs(self, item: dict[str, Any], step: dict[str, Any], result: dict[str, Any]) -> None:
        stdout = str(step.get("stdout", ""))
        stderr = str(step.get("stderr", ""))
        for expected in normalize_contains(item.get("expected_stdout_contains")):
            ok = expected in stdout
            result["assertions"].append({"stream": "stdout", "contains": expected, "passed": ok})
            if not ok:
                result["status"] = "failed"
                result["failure_reason"] = "stdout_assertion_failed"
        for expected in normalize_contains(item.get("expected_stderr_contains")):
            ok = expected in stderr
            result["assertions"].append({"stream": "stderr", "contains": expected, "passed": ok})
            if not ok:
                result["status"] = "failed"
                result["failure_reason"] = "stderr_assertion_failed"

    def run(self, item: dict[str, Any], package_root: Path) -> dict[str, Any]:
        code_path = resolve_path(str(item["code_path"]), package_root)
        timeout = int(item.get("timeout_sec") or self.default_timeout)
        test_mode = str(item.get("test", "compile"))
        result = self.result_base(item, code_path, test_mode)

        if test_mode not in SUPPORTED_TEST_MODES:
            result["status"] = "skipped"
            result["failure_reason"] = f"unsupported_test_mode_{test_mode}"
            return result
        if not self.executable_available():
            result["status"] = "skipped"
            result["failure_reason"] = self.unavailable_reason()
            return result
        if not code_path.exists():
            result["status"] = "failed"
            result["failure_reason"] = "code_file_not_found"
            return result

        compile_result = self.compile_step(item, code_path, timeout)
        result["steps"].append({"name": "compile", **compile_result})
        if compile_result.get("returncode") != 0 or compile_result.get("timed_out"):
            result["status"] = "failed"
            result["failure_reason"] = "compile_failed"
            return result
        if test_mode == "compile":
            return result

        run_result = self.run_step(item, code_path, timeout)
        result["steps"].append({"name": "run", **run_result})
        if run_result.get("returncode") != 0 or run_result.get("timed_out"):
            result["status"] = "failed"
            result["failure_reason"] = "runtime_failed"
            return result
        if test_mode == "compile_run_assert":
            self.assert_outputs(item, run_result, result)
        return result


class ExecutableAdapter(LanguageAdapter):
    executable_name = ""

    def __init__(self, *, executable: str | None = None, default_timeout: int = 10) -> None:
        super().__init__(default_timeout=default_timeout)
        self.executable = executable or self.executable_name
        self.executable_path = shutil.which(self.executable) or self.executable

    def executable_available(self) -> bool:
        return shutil.which(self.executable) is not None or Path(self.executable).exists()
