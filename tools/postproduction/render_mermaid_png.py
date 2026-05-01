#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bir klasördeki .mmd Mermaid dosyalarını yüksek çözünürlüklü PNG dosyalarına dönüştürür.

Bu betik Mermaid PNG üretiminin tek sorumlusudur. Önce prepare_mermaid_images.py
ile .mmd dosyalarını üretin, sonra bu betiği bir kez çalıştırın.

Örnek:
    python render_mermaid_png.py mermaid_images --pdf-fit --force
    python render_mermaid_png.py mermaid_images --recursive --background white --width 2400 --scale 3
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bir klasördeki .mmd Mermaid dosyalarını PNG'ye dönüştürür."
    )
    parser.add_argument("input_dir", nargs="?", default="mermaid_images", help=".mmd dosyalarının bulunduğu klasör")
    parser.add_argument("--recursive", action="store_true", help="Alt klasörlerdeki .mmd dosyalarını da tara")
    parser.add_argument("--force", action="store_true", help="Mevcut PNG dosyaları varsa üzerine yaz")
    parser.add_argument("--background", default="white", help="Arka plan rengi: white veya transparent (varsayılan: white)")
    parser.add_argument("--width", type=int, default=None, help="İsteğe bağlı çıktı genişliği, piksel. Örn: 2400")
    parser.add_argument("--height", type=int, default=None, help="İsteğe bağlı çıktı yüksekliği, piksel")
    parser.add_argument("--scale", type=float, default=3.0, help="Yüksek çözünürlük katsayısı (varsayılan: 3.0)")
    parser.add_argument("--theme", choices=["default", "forest", "dark", "neutral"], default=None, help="İsteğe bağlı Mermaid tema adı")
    parser.add_argument(
        "--pdf-fit",
        action="store_true",
        help="DOCX/PDF için width=2400 ve scale en az 3 olacak şekilde ayarlar",
    )
    parser.add_argument(
        "--puppeteer-config",
        default=None,
        help="Mermaid CLI için Puppeteer config JSON dosyası. Örn: configs/puppeteer_config.json",
    )
    return parser.parse_args()


def find_mmdc() -> str | None:
    for candidate in ("mmdc", "mmdc.cmd", "mmdc.ps1"):
        found = shutil.which(candidate)
        if found:
            return found
    return None


def iter_mmd_files(base_dir: Path, recursive: bool) -> list[Path]:
    pattern = "**/*.mmd" if recursive else "*.mmd"
    return sorted(path for path in base_dir.glob(pattern) if path.is_file())


def build_command(
    mmdc_cmd: str,
    input_file: Path,
    output_file: Path,
    background: str,
    width: int | None,
    height: int | None,
    scale: float,
    theme: str | None,
    puppeteer_config: str | None,
) -> list[str]:
    cmd = [
        mmdc_cmd,
        "-i", str(input_file),
        "-o", str(output_file),
        "-e", "png",
        "-b", background,
        "-s", str(scale),
    ]
    if width is not None:
        cmd.extend(["-w", str(width)])
    if height is not None:
        cmd.extend(["-H", str(height)])
    if theme is not None:
        cmd.extend(["-t", theme])
    if puppeteer_config:
        cmd.extend(["--puppeteerConfigFile", puppeteer_config])
    return cmd


def main() -> int:
    args = parse_args()

    input_dir = Path(args.input_dir).expanduser().resolve()
    if not input_dir.exists() or not input_dir.is_dir():
        print(f"Hata: Klasör bulunamadı: {input_dir}", file=sys.stderr)
        return 1

    width = args.width
    height = args.height
    scale = args.scale

    if args.pdf_fit:
        width = 2400 if width is None else width
        scale = max(scale, 3.0)

    mmd_files = iter_mmd_files(input_dir, args.recursive)
    if not mmd_files:
        print(f".mmd dosyası bulunamadı: {input_dir}")
        return 0

    mmdc_cmd = find_mmdc()
    if not mmdc_cmd:
        print("Hata: Mermaid CLI (mmdc) PATH içinde bulunamadı.", file=sys.stderr)
        print("Kurulum örneği: npm install -g @mermaid-js/mermaid-cli", file=sys.stderr)
        return 1

    print(f"Mermaid CLI : {mmdc_cmd}")
    print(f"Girdi klasörü: {input_dir}")
    print(f"Dosya sayısı : {len(mmd_files)}")
    print(f"Background   : {args.background}")
    print(f"Scale        : {scale}")
    print(f"Width        : {width if width is not None else 'otomatik'}")
    print(f"Height       : {height if height is not None else 'otomatik'}")
    if args.puppeteer_config:
        print(f"Puppeteer cfg: {args.puppeteer_config}")
    print("-" * 60)

    success_count = 0
    skipped_count = 0
    fail_count = 0

    for mmd_file in mmd_files:
        png_file = mmd_file.with_suffix(".png")

        if png_file.exists() and not args.force:
            print(f"[ATLANDI] {mmd_file.name} -> {png_file.name} (zaten var)")
            skipped_count += 1
            continue

        cmd = build_command(
            mmdc_cmd,
            mmd_file,
            png_file,
            args.background,
            width,
            height,
            scale,
            args.theme,
            args.puppeteer_config,
        )

        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"[PNG] {mmd_file.name} -> {png_file.name}")
            if result.stdout.strip():
                print(result.stdout.strip())
            success_count += 1
        except subprocess.CalledProcessError as exc:
            print(f"[HATA] {mmd_file.name} dönüştürülemedi.", file=sys.stderr)
            if exc.stdout:
                print(exc.stdout.strip(), file=sys.stderr)
            if exc.stderr:
                print(exc.stderr.strip(), file=sys.stderr)
            fail_count += 1

    print("-" * 60)
    print("İşlem özeti:")
    print(f"  Başarılı : {success_count}")
    print(f"  Atlandı  : {skipped_count}")
    print(f"  Hatalı   : {fail_count}")

    return 0 if fail_count == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
