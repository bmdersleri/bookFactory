# -*- coding: utf-8 -*-
"""Code management service for BookFactory Studio."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .path_service import PathService

class CodeService:
    @staticmethod
    def get_code_block(root: Path, chapter_id: str, code_id: str) -> dict[str, Any]:
        """Extracts a specific code block and its metadata from markdown."""
        from .manifest_service import ManifestService
        manifest_path = ManifestService.find(root)
        if not manifest_path:
            return {"error": "Manifest not found"}
            
        manifest = ManifestService.load(manifest_path)
        # Find chapter entry to get file path
        chapter = None
        idx = -1
        for i, ch in enumerate(ManifestService.chapters_from_manifest(manifest), 1):
            if ManifestService.chapter_id(ch, i) == chapter_id:
                chapter = ch
                idx = i
                break
        
        if not chapter:
            return {"error": f"Chapter {chapter_id} not found"}
            
        md_path = PathService.chapter_markdown_path(root, chapter, idx)
        if not md_path.exists():
            return {"error": f"Chapter file {md_path.name} not found"}
            
        content = md_path.read_text(encoding="utf-8")
        
        # Regex to find the specific CODE_META block and its code
        pattern = re.compile(
            rf"(<!--\s*CODE_META[\s\S]*?id:\s*{re.escape(code_id)}[\s\S]*?-->[\s\S]*?```[a-z]*\n([\s\S]*?)\n```)",
            re.MULTILINE
        )
        
        match = pattern.search(content)
        if not match:
            return {"error": f"Code block {code_id} not found in {md_path.name}"}
            
        return {
            "id": code_id,
            "full_match": match.group(1),
            "code": match.group(2),
            "path": str(md_path)
        }

    @staticmethod
    def update_code_block(root: Path, chapter_id: str, code_id: str, new_code: str) -> bool:
        """Surgically replaces a code block in the chapter markdown."""
        data = CodeService.get_code_block(root, chapter_id, code_id)
        if "error" in data:
            return False
            
        md_path = Path(data["path"])
        content = md_path.read_text(encoding="utf-8")
        
        # We need to replace the content within the code fences
        # Re-searching to get exact replacement range
        pattern = re.compile(
            rf"(<!--\s*CODE_META[\s\S]*?id:\s*{re.escape(code_id)}[\s\S]*?-->[\s\S]*?```[a-z]*\n)([\s\S]*?)(\n```)",
            re.MULTILINE
        )
        
        new_content = pattern.sub(rf"\1{new_code}\3", content)
        md_path.write_text(new_content, encoding="utf-8")
        return True
