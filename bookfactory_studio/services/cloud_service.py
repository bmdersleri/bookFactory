# -*- coding: utf-8 -*-
"""Cloud integration and GitHub provisioning service for BookFactory Studio."""
from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from .path_service import PathService

class CloudService:
    @staticmethod
    def provision_github_configs(root: Path, manifest: dict[str, Any]) -> list[str]:
        """Copies cloud templates (Codespace, Actions) to the project root."""
        templates_root = PathService.framework_root() / "templates" / "cloud"
        book_title = manifest.get("book", {}).get("title", "BookFactory Project")
        
        provisioned = []
        
        # 1. .devcontainer
        dev_src = templates_root / ".devcontainer" / "devcontainer.json"
        dev_dest_dir = root / ".devcontainer"
        dev_dest_dir.mkdir(parents=True, exist_ok=True)
        dev_dest = dev_dest_dir / "devcontainer.json"
        
        if dev_src.exists():
            content = dev_src.read_text(encoding="utf-8")
            content = content.replace("{book_title}", book_title)
            dev_dest.write_text(content, encoding="utf-8")
            provisioned.append(".devcontainer/devcontainer.json")
            
        # 2. GitHub Workflows
        wf_src_dir = templates_root / ".github" / "workflows"
        wf_dest_dir = root / ".github" / "workflows"
        wf_dest_dir.mkdir(parents=True, exist_ok=True)
        
        if wf_src_dir.exists():
            for wf_file in wf_src_dir.glob("*.yml"):
                shutil.copy2(wf_file, wf_dest_dir / wf_file.name)
                provisioned.append(f".github/workflows/{wf_file.name}")
                
        return provisioned

    @staticmethod
    def check_cloud_status(root: Path) -> dict[str, bool]:
        """Checks which cloud configurations are present."""
        return {
            "codespace": (root / ".devcontainer" / "devcontainer.json").exists(),
            "github_actions": any((root / ".github" / "workflows").glob("*.yml")),
            "digital_twin": (root / "dist" / "web_site").exists()
        }
