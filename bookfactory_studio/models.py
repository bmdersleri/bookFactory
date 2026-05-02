# -*- coding: utf-8 -*-
"""Pydantic models for BookFactory Studio API."""
from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field

class ManifestRequest(BaseModel):
    root: str = "."
    manifest: dict[str, Any]
    force: bool = False

class WizardInitRequest(BaseModel):
    root: str = "."
    data: dict[str, Any]

class WizardPromptRequest(BaseModel):
    root: str = "."
    data: dict[str, Any]
    save: bool = True
    use_rag: bool = False
    rag_query: str | None = None

class ManifestYamlRequest(BaseModel):
    root: str = "."
    yaml_text: str
    force: bool = False

class ProjectInitRequest(BaseModel):
    root: str = "."
    manifest: dict[str, Any]

class ChapterImportRequest(BaseModel):
    root: str = "."
    chapter_id: str
    content: str = Field(min_length=1)
    lang: str | None = None

class JobRequest(BaseModel):
    root: str = "."
    step: str
    options: dict[str, Any] = Field(default_factory=dict)

class StudioConfigRequest(BaseModel):
    active_book: str
