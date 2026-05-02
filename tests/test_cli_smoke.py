from __future__ import annotations

import importlib.metadata as metadata
import re
import subprocess
import sys
from pathlib import Path

from bookfactory import __version__
from bookfactory import _cli
from bookfactory import cli as public_cli


ROOT = Path(__file__).resolve().parents[1]


def read_pyproject_value(key: str) -> str:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(rf'^{re.escape(key)}\s*=\s*"([^"]+)"$', text, re.MULTILINE)
    assert match is not None
    return match.group(1)


def test_parser_exposes_core_commands() -> None:
    parser = _cli.build_parser()
    commands_action = next(
        action for action in parser._actions if action.dest == "command"
    )

    assert {"version", "doctor", "test-minimal"} <= set(
        commands_action.choices
    )


def test_python_module_version_smoke() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "bookfactory", "version"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=10,
        check=False,
    )

    assert completed.returncode == 0
    assert completed.stdout.strip() == __version__


def test_package_version_metadata_is_consistent() -> None:
    assert read_pyproject_value("version") == __version__
    assert metadata.version("bookfactory") == __version__


def test_console_script_entry_points_are_consistent() -> None:
    scripts = {
        entry_point.name: entry_point.value
        for entry_point in metadata.entry_points(group="console_scripts")
        if entry_point.name.startswith("bookfactory")
    }

    assert scripts["bookfactory"] == "bookfactory.cli:main"
    assert scripts["bookfactory-studio"] == "bookfactory_studio.app:main"


def test_public_cli_delegates_non_init_commands(monkeypatch) -> None:
    captured: dict[str, list[str]] = {}

    def fake_orchestrator(argv: list[str]) -> int:
        captured["argv"] = argv
        return 0

    monkeypatch.setattr(_cli, "main", fake_orchestrator)

    assert public_cli.main(["doctor", "--soft"]) == 0
    assert captured["argv"] == ["doctor", "--soft"]


def test_doctor_soft_dispatch_uses_check_environment(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_run_python(script: Path, args: list[str], root: Path) -> int:
        captured["script"] = script
        captured["args"] = args
        captured["root"] = root
        return 0

    monkeypatch.setattr(_cli, "run_python", fake_run_python)

    assert _cli.main(["--root", str(ROOT), "doctor", "--soft"]) == 0
    assert captured["script"] == ROOT / "tools/check_environment.py"
    assert captured["args"] == ["--soft"]
    assert captured["root"] == ROOT


def test_test_minimal_dispatch_builds_deterministic_args(
    monkeypatch,
) -> None:
    captured: dict[str, object] = {}

    def fake_test_code(args) -> int:
        captured["args"] = args
        return 0

    monkeypatch.setattr(_cli, "cmd_test_code", fake_test_code)

    assert (
        _cli.main(
            [
                "--root",
                str(ROOT),
                "test-minimal",
                "--timeout-sec",
                "3",
                "--javac",
                "JAVAC",
                "--java",
                "JAVA",
                "--python",
                "PYTHON",
                "--node",
                "NODE",
                "--fail-on-error",
            ]
        )
        == 0
    )

    args = captured["args"]
    assert args.root == ROOT
    assert args.chapters_dir == Path("examples/minimal_book/chapters")
    assert args.manifest == Path("examples/minimal_book/build/code_manifest.json")
    assert args.timeout_sec == 3
    assert args.javac == "JAVAC"
    assert args.java == "JAVA"
    assert args.python == "PYTHON"
    assert args.node == "NODE"
    assert args.fail_on_error is True
