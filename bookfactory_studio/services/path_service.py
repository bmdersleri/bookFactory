# -*- coding: utf-8 -*-
"""Path resolution service for BookFactory Studio."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .manifest_service import ManifestService

class PathService:
    @staticmethod
    def project_root(path: str | None = None) -> Path:
        """Resolves the active project root."""
        p = Path(path or ".").resolve()
        if p == Path.cwd() or (p / "book_manifest.yaml").exists() or (p / "manifests").exists():
            return p
        return p

    @staticmethod
    def framework_root() -> Path:
        """Resolves the BookFactory framework root."""
        return Path(__file__).resolve().parents[2]

    @staticmethod
    def safe_relative(path: Path | None, base: Path) -> str:
        """Returns a safe forward-slash relative path string."""
        if path is None:
            return ""
        try:
            return str(path.resolve().relative_to(base.resolve())).replace("\\", "/")
        except ValueError:
            return str(path).replace("\\", "/")

    @staticmethod
    def chapter_markdown_path(root: Path, chapter: dict[str, Any], order: int, lang: str | None = None) -> Path:
        """Resolves the full path to a chapter markdown file."""
        filename = ManifestService.chapter_file(chapter, order)
        if lang:
            return root / "chapters" / lang / filename

        # Support for legacy manifest paths
        raw = str(chapter.get("path") or chapter.get("file") or "").strip()
        if raw:
            p = Path(raw)
            if p.is_absolute():
                return p
            direct = root / p
            if direct.exists():
                return direct
            parts = p.parts
            if "chapters" in parts:
                idx = parts.index("chapters")
                return root.joinpath(*parts[idx:])
        
        return root / "chapters" / filename
