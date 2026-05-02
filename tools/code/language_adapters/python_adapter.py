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
        
        expected_plot = item.get("expected_plot")
        if expected_plot:
            # Step 1: Prepare plot directory
            # We need to find package root to save to assets/auto/plots
            # Assuming current working directory is package root as per typical run_code_tests usage
            package_root = Path.cwd()
            plot_dir = package_root / "assets" / "auto" / "plots"
            plot_dir.mkdir(parents=True, exist_ok=True)
            plot_path = plot_dir / expected_plot

            # Step 2: Create wrapper script
            original_code = code_path.read_text(encoding="utf-8")
            wrapper_code = [
                "import matplotlib",
                "matplotlib.use('Agg')",
                "import matplotlib.pyplot as plt",
                "",
                original_code,
                "",
                f"plt.savefig(r'{plot_path}')",
            ]
            wrapper_path = code_path.parent / (code_path.stem + "_plot_wrapper.py")
            wrapper_path.write_text("\n".join(wrapper_code), encoding="utf-8")
            
            # Step 3: Run wrapper
            return run_command(
                [self.executable_path, wrapper_path.name, *args],
                wrapper_path.parent,
                timeout,
                stdin=str(stdin) if stdin is not None else None,
            )

        return run_command(
            [self.executable_path, code_path.name, *args],
            code_path.parent,
            timeout,
            stdin=str(stdin) if stdin is not None else None,
        )
