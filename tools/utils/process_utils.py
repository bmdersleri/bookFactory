#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared subprocess helpers for BookFactory test adapters.

v2.11.2 hotfix:
- Force UTF-8 decoding for stdout/stderr in subprocess calls.
- This prevents mojibake such as "KampÃƒÂ¼sHub" on Windows consoles when
  Node.js/Python/other tools emit UTF-8 output.
"""
from __future__ import annotations

import os
import signal
import subprocess
from pathlib import Path
from typing import Any


def _merged_env() -> dict[str, str]:
    """Return a subprocess environment with UTF-8 friendly defaults."""
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUTF8", "1")
    return env


def run_command(
    command: list[str],
    cwd: Path,
    timeout: int,
    stdin: str | None = None,
) -> dict[str, Any]:
    popen_kwargs: dict[str, Any] = {
        "cwd": str(cwd),
        "stdin": subprocess.PIPE if stdin is not None else None,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "text": True,
        "encoding": "utf-8",
        "errors": "replace",
        "env": _merged_env(),
    }

    if os.name == "nt":
        popen_kwargs["creationflags"] = getattr(
            subprocess,
            "CREATE_NEW_PROCESS_GROUP",
            0,
        )
    else:
        popen_kwargs["start_new_session"] = True

    proc = subprocess.Popen(command, **popen_kwargs)

    try:
        stdout, stderr = proc.communicate(input=stdin, timeout=timeout)
        return {
            "command": command,
            "cwd": str(cwd),
            "returncode": proc.returncode,
            "stdout": stdout or "",
            "stderr": stderr or "",
            "timed_out": False,
        }
    except subprocess.TimeoutExpired:
        try:
            if os.name == "nt":
                proc.kill()
            else:
                os.killpg(proc.pid, signal.SIGKILL)
        except Exception:
            proc.kill()

        stdout, stderr = proc.communicate()
        return {
            "command": command,
            "cwd": str(cwd),
            "returncode": None,
            "stdout": stdout or "",
            "stderr": (stderr or "") + f"\nTimeout after {timeout} seconds",
            "timed_out": True,
        }
