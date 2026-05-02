# -*- coding: utf-8 -*-
"""Asset management service for BookFactory Studio."""
from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any
from datetime import datetime

class AssetService:
    @staticmethod
    def list_assets(root: Path) -> list[dict[str, Any]]:
        """Lists all files in the assets/ directory."""
        asset_root = root / "assets"
        if not asset_root.exists():
            return []
            
        assets = []
        # Support subdirectories like manual/ auto/
        for p in asset_root.rglob("*"):
            if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif", ".csv", ".json", ".sqlite", ".db"}:
                assets.append({
                    "name": p.name,
                    "rel_path": str(p.relative_to(root)).replace("\\", "/"),
                    "size": p.stat().st_size,
                    "modified": datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec="seconds"),
                    "type": p.suffix.lower().lstrip(".")
                })
        return sorted(assets, key=lambda x: x["modified"], reverse=True)

    @staticmethod
    def save_asset(root: Path, filename: str, content: bytes, category: str = "manual") -> str:
        """Saves an uploaded asset."""
        # Map extension to subfolder
        ext = Path(filename).suffix.lower()
        subfolder = "screenshots"
        if ext in {".csv", ".json", ".sqlite", ".db"}:
            subfolder = "datasets"
            
        target_dir = root / "assets" / category / subfolder
        target_dir.mkdir(parents=True, exist_ok=True)
        
        target_path = target_dir / filename
        target_path.write_bytes(content)
        
        return str(target_path.relative_to(root)).replace("\\", "/")
