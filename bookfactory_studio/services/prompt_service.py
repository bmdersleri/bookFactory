# -*- coding: utf-8 -*-
"""Prompt generation and rendering service for BookFactory Studio."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .path_service import PathService

class PromptService:
    @staticmethod
    def render_architecture_prompt(data: dict[str, Any]) -> str:
        # Simple placeholder for rendering logic
        # In a real refactor, we'd move the full markdown template here
        return f"# Architecture Prompt for {data.get('title', 'New Book')}\n"

    @staticmethod
    def save_architecture_prompt(root: Path, prompt: str) -> dict[str, Any]:
        path = root / "prompts" / "project_architecture_prompt.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(prompt, encoding="utf-8")
        return {"prompt": prompt, "path": PathService.safe_relative(path, root)}
