# -*- coding: utf-8 -*-
"""Flutter code test and screenshot adapter."""
from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from .base_adapter import ExecutableAdapter, normalize_args
from tools.utils.process_utils import run_command


class FlutterAdapter(ExecutableAdapter):
    language = "flutter"
    executable_name = "flutter"

    def compile_step(self, item: dict[str, Any], code_path: Path, timeout: int) -> dict[str, Any]:
        # For Flutter, 'compile' often means 'flutter pub get' or 'flutter analyze'
        # in the context of an extracted code block, it's tricky since it's usually just a snippet.
        # However, if it's a full file, we can run analyze.
        return run_command([self.executable_path, "analyze"], code_path.parent, timeout)

    def run_step(self, item: dict[str, Any], code_path: Path, timeout: int) -> dict[str, Any]:
        screenshot_id = item.get("captures_screenshot")
        
        if screenshot_id:
            return self._capture_screenshot(item, code_path, screenshot_id, timeout)

        # Standard flutter run (usually not useful for snippets unless it's a test)
        args = normalize_args(item.get("args"))
        return run_command(
            [self.executable_path, "test", code_path.name, *args],
            code_path.parent,
            timeout
        )

    def _capture_screenshot(self, item: dict[str, Any], code_path: Path, screenshot_id: str, timeout: int) -> dict[str, Any]:
        """Runs a flutter integration test to capture a screenshot."""
        package_root = Path.cwd()
        output_dir = package_root / "assets" / "auto" / "screenshots"
        output_dir.mkdir(parents=True, exist_ok=True)
        final_path = output_dir / f"{screenshot_id}.png"

        # Note: In a real v3.2 production, we would have a template Flutter project
        # and inject the code into it. For this adapter, we assume the code_path 
        # is already inside a valid Flutter project structure (e.g. build/code/...)
        # OR we run it as an integration test.
        
        # This is a simplified implementation of the capture logic
        cmd = [
            self.executable_path, "test",
            "--dart-define", f"SCREENSHOT_ID={screenshot_id}",
            code_path.name
        ]
        
        # UI tests are slow, increase default timeout if not specified
        ui_timeout = max(timeout, 120) 
        
        res = run_command(cmd, code_path.parent, ui_timeout)
        
        # After test, look for screenshot. 
        # Integration tests usually save screenshots to a specific folder.
        # We assume the test code uses a utility to save to a known temp location.
        temp_screenshot = code_path.parent / "screenshots" / f"{screenshot_id}.png"
        
        if temp_screenshot.exists():
            shutil.move(str(temp_screenshot), str(final_path))
            res["stdout"] = (res.get("stdout") or "") + f"\nScreenshot captured: {final_path}"
        else:
            if res.get("returncode") == 0:
                res["returncode"] = 1
                res["stderr"] = (res.get("stderr") or "") + f"\nError: Screenshot not found at {temp_screenshot}"

        return res
