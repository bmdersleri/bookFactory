# -*- coding: utf-8 -*-
"""Centralized project utilities for BookFactory."""
from __future__ import annotations

from pathlib import Path

def find_project_manifest(root: Path) -> Path | None:
    """
    Locates the book_manifest.yaml file for a given project root.
    Checks the root directory and the 'manifests/' subdirectory.
    """
    candidates = [
        root / "book_manifest.yaml",
        root / "manifests" / "book_manifest.yaml"
    ]
    for cand in candidates:
        if cand.exists():
            return cand
    return None
