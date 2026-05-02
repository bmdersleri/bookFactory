# -*- coding: utf-8 -*-
"""Manifest management service for BookFactory Studio."""
from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from tools.utils.project_utils import find_project_manifest
from tools.utils.yaml_utils import load_yaml as _load_yaml

# Constants from previous core.py logic
QUALITY_GATE_DEFAULTS = {
    "manifest_validation": "required",
    "chapter_input_generation": "optional",
    "outline_review": "required",
    "full_text_generation": "required",
    "code_validation": "required",
    "markdown_quality_check": "required",
    "post_production_build": "optional",
}

class ManifestService:
    @staticmethod
    def load(path: Path) -> dict[str, Any]:
        return _load_yaml(path)

    @staticmethod
    def save(path: Path, data: dict[str, Any]) -> None:
        path.write_text(yaml.dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")

    @staticmethod
    def find(root: Path) -> Path | None:
        return find_project_manifest(root)

    @staticmethod
    def normalize(raw: dict[str, Any]) -> dict[str, Any]:
        """Ensures manifest has all required blocks and default values."""
        m = raw.copy()
        
        # Schema versioning
        m.setdefault("schema", {})
        m["schema"].setdefault("manifest_version", "1.0")
        
        # Language
        m.setdefault("language", {
            "primary_language": "tr", 
            "output_languages": ["tr"],
            "style_profile": "Academic",
            "pedagogical_model": "Bloom"
        })
        
        # Quality Gates
        m.setdefault("quality_gates", QUALITY_GATE_DEFAULTS.copy())
        
        # Structure
        m.setdefault("structure", {})
        if "chapters" in m and not m["structure"].get("chapters"):
            m["structure"]["chapters"] = m.pop("chapters")
        m["structure"].setdefault("chapters", [])
        
        # Project metadata
        m.setdefault("project", {})
        m["project"]["updated_at"] = datetime.now().isoformat()
        
        return m

    @staticmethod
    def validate(manifest: dict[str, Any], root: Path | None = None) -> dict[str, Any]:
        """Validates the manifest structure and content."""
        errors = []
        warnings = []
        
        # Basic checks
        book = manifest.get("book", {})
        if not book.get("title"): errors.append("Kitap başlığı (book.title) eksik.")
        if not book.get("author"): errors.append("Yazar (book.author) eksik.")
        
        # Chapter checks
        chapters = manifest.get("structure", {}).get("chapters", [])
        ids = set()
        for i, ch in enumerate(chapters, 1):
            cid = ch.get("id")
            if not cid:
                errors.append(f"{i}. bölümün ID'si eksik.")
            elif cid in ids:
                errors.append(f"Mükerrer bölüm ID: {cid}")
            else:
                ids.add(cid)
            
            if root:
                from .path_service import PathService # Circular import prevention
                path = PathService.chapter_markdown_path(root, ch, i)
                if not path.exists():
                    warnings.append(f"Bölüm dosyası bulunamadı: {path.name}")

        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}

    @staticmethod
    def chapters_from_manifest(manifest: dict[str, Any]) -> list[dict[str, Any]]:
        return manifest.get("structure", {}).get("chapters", [])

    @staticmethod
    def chapter_id(chapter: dict[str, Any], order: int) -> str:
        return str(chapter.get("id") or f"chapter_{order:02d}")

    @staticmethod
    def chapter_file(chapter: dict[str, Any], order: int) -> str:
        cid = ManifestService.chapter_id(chapter, order)
        raw = chapter.get("file") or chapter.get("path") or ""
        if raw:
            p = Path(raw)
            return p.name
        return f"{cid}.md"
