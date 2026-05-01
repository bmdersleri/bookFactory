#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown içindeki ```mermaid bloklarını mermaid_images/diagram_001.mmd,
diagram_002.mmd ... dosyalarına çıkarır.

Bu sürüm bilinçli olarak PNG üretmez. PNG üretimi yalnızca
render_mermaid_png.py tarafından yapılır. Böylece batch akışında
aynı .mmd dosyalarından iki kez PNG oluşturma sorunu ortadan kalkar.

Örnek:
    python prepare_mermaid_images.py Bolum_08_GPT_pilot.md
    python prepare_mermaid_images.py Bolum_08_GPT_pilot.md --out-dir mermaid_images --clean
    python prepare_mermaid_images.py Bolum_08_GPT_pilot.md --out-dir mermaid_images --force
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


MERMAID_BLOCK_RE = re.compile(
    r"```mermaid\s*\n(.*?)\n```",
    re.DOTALL | re.IGNORECASE,
)


def extract_mermaid_blocks(md_text: str) -> list[str]:
    """Markdown içindeki Mermaid kod bloklarını sırayla döndürür."""
    return [m.group(1).strip() + "\n" for m in MERMAID_BLOCK_RE.finditer(md_text)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Markdown dosyasındaki Mermaid bloklarını yalnızca .mmd dosyalarına çıkarır."
    )
    parser.add_argument("markdown_file", help="Mermaid blokları içeren Markdown dosyası")
    parser.add_argument("--out-dir", default="mermaid_images", help="Çıktı klasörü (varsayılan: mermaid_images)")
    parser.add_argument("--force", action="store_true", help="Var olan .mmd dosyalarının üzerine yaz")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Önce bu betiğin ürettiği diagram_*.mmd ve diagram_*.png dosyalarını temizle",
    )
    parser.add_argument("--prefix", default="diagram", help="Çıktı dosya adı ön eki (varsayılan: diagram)")
    return parser.parse_args()


def clean_generated_files(out_dir: Path, prefix: str) -> int:
    """Yalnızca bu pipeline'ın ürettiği dosyaları temizler."""
    deleted = 0
    for pattern in (f"{prefix}_*.mmd", f"{prefix}_*.png"):
        for path in out_dir.glob(pattern):
            if path.is_file():
                path.unlink()
                deleted += 1
    return deleted


def main() -> int:
    args = parse_args()

    md_path = Path(args.markdown_file).expanduser().resolve()
    if not md_path.exists() or not md_path.is_file():
        print(f"Hata: Markdown dosyası bulunamadı: {md_path}", file=sys.stderr)
        return 1

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.clean:
        deleted = clean_generated_files(out_dir, args.prefix)
        print(f"Temizlenen eski Mermaid dosyası: {deleted}")

    md_text = md_path.read_text(encoding="utf-8")
    blocks = extract_mermaid_blocks(md_text)

    print(f"Markdown dosyası : {md_path}")
    print(f"Çıktı klasörü    : {out_dir}")
    print(f"Mermaid bloğu    : {len(blocks)}")

    if not blocks:
        print("Mermaid bloğu bulunamadı. .mmd dosyası üretilmedi.")
        return 0

    skipped_count = 0
    written_count = 0

    for i, code in enumerate(blocks, start=1):
        mmd_path = out_dir / f"{args.prefix}_{i:03d}.mmd"

        if mmd_path.exists() and not args.force:
            print(f"[ATLANDI] {mmd_path.name} zaten var. --force veya --clean kullanabilirsiniz.")
            skipped_count += 1
            continue

        mmd_path.write_text(code, encoding="utf-8")
        print(f"[MMD] {mmd_path.name}")
        written_count += 1

    print("-" * 60)
    print("İşlem özeti:")
    print(f"  Yazılan : {written_count}")
    print(f"  Atlanan : {skipped_count}")
    print("  PNG     : Bu betikte üretilmez; render_mermaid_png.py kullanılır.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
