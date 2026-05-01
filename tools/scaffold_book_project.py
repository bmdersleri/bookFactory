"""
scaffold_book_project.py
Parametric Computer Book Factory — Kitap Projesi Başlatıcı

Kullanım:
    python tools/scaffold_book_project.py --name react-web --title "React ile Web Uygulama Geliştirme" --lang tr --output ../

Çıktı:
    ../react-web/
    ├── .bookfactory
    ├── README.md
    ├── .gitignore
    ├── chapters/
    ├── chapter_inputs/
    ├── manifests/
    │   └── book_manifest.yaml
    ├── configs/
    │   └── post_production_profile.yaml
    ├── assets/
    │   ├── auto/
    │   ├── manual/
    │   ├── locked/
    │   └── final/
    ├── build/
    │   ├── code/
    │   └── test_reports/
    ├── screenshots/
    └── dist/
"""

import argparse
import os
import sys
import textwrap
from datetime import datetime
from pathlib import Path

BOOKFACTORY_VERSION = "v2.11.x"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Yeni BookFactory kitap projesi oluşturur."
    )
    parser.add_argument("--name", required=True, help="Proje klasörü adı (örn: react-web)")
    parser.add_argument("--title", required=True, help="Kitap başlığı (örn: 'React ile Web Uygulama Geliştirme')")
    parser.add_argument("--author", default="", help="Yazar adı")
    parser.add_argument("--lang", default="tr", help="Birincil içerik dili (varsayılan: tr)")
    parser.add_argument("--output", default=".", help="Projenin oluşturulacağı üst dizin (varsayılan: .)")
    parser.add_argument("--framework-path", default="../bookFactory", help="BookFactory framework repo yolu")
    parser.add_argument("--dry-run", action="store_true", help="Dosya oluşturmadan yapıyı göster")
    return parser.parse_args()


def make_dir(path: Path, dry_run: bool):
    if dry_run:
        print(f"  [DIR]  {path}")
    else:
        path.mkdir(parents=True, exist_ok=True)


def make_file(path: Path, content: str, dry_run: bool):
    if dry_run:
        print(f"  [FILE] {path}")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def scaffold(args):
    output_root = Path(args.output).resolve() / args.name
    now = datetime.now().strftime("%Y-%m-%d")

    if output_root.exists() and not args.dry_run:
        print(f"HATA: '{output_root}' zaten mevcut. Farklı bir --name veya --output belirtin.")
        sys.exit(1)

    print(f"\nBookFactory Kitap Projesi Başlatıcı")
    print(f"{'=' * 50}")
    print(f"Proje adı   : {args.name}")
    print(f"Kitap başlığı: {args.title}")
    print(f"Dil         : {args.lang}")
    print(f"Çıktı yolu  : {output_root}")
    if args.dry_run:
        print(f"[DRY RUN — dosya oluşturulmayacak]\n")
    print()

    # --- Dizinler ---
    dirs = [
        "chapters",
        "chapter_inputs",
        "manifests",
        "configs",
        "assets/auto/diagrams",
        "assets/auto/qr",
        "assets/manual",
        "assets/locked",
        "assets/final",
        "build/code",
        "build/test_reports",
        "screenshots",
        "dist",
    ]
    for d in dirs:
        make_dir(output_root / d, args.dry_run)

    # --- .bookfactory ---
    make_file(output_root / ".bookfactory", textwrap.dedent(f"""\
        # BookFactory Bağlantı Dosyası
        # Bu dosya, kitap projesinin hangi BookFactory sürümünü
        # kullandığını ve framework konumunu tanımlar.

        framework_version: "{BOOKFACTORY_VERSION}"
        framework_path: "{args.framework_path}"
        created: "{now}"
        book_title: "{args.title}"
        primary_language: "{args.lang}"
    """), args.dry_run)

    # --- .gitignore ---
    make_file(output_root / ".gitignore", textwrap.dedent("""\
        # Build çıktıları
        build/
        dist/

        # Otomatik üretilen görseller (QR, PNG)
        assets/auto/

        # Geçici dosyalar
        *.bak
        *.tmp
        *.old
        __pycache__/
        *.pyc
        .DS_Store
        Thumbs.db
        .env
    """), args.dry_run)

    # --- README.md ---
    make_file(output_root / "README.md", textwrap.dedent(f"""\
        # {args.title}

        **Framework:** Parametric Computer Book Factory {BOOKFACTORY_VERSION}  
        **Dil:** {args.lang.upper()}  
        **Yazar:** {args.author or "[Yazar adı]"}  
        **Başlangıç tarihi:** {now}

        ---

        ## Proje yapısı

        ```
        {args.name}/
        ├── chapters/          ← Bölüm Markdown dosyaları
        ├── chapter_inputs/    ← Bölüm girdi promptları
        ├── manifests/         ← book_manifest.yaml
        ├── configs/           ← Post-production profilleri
        ├── assets/            ← Görseller (auto/manual/locked/final)
        ├── build/             ← Üretilen kod ve test raporları
        ├── screenshots/       ← Bölüm ekran görüntüleri
        └── dist/              ← Final çıktılar (DOCX, EPUB, PDF)
        ```

        ## Kurulum

        ```powershell
        # BookFactory framework'ü klonla (eğer yoksa)
        git clone https://github.com/bmdersleri/bookFactory {args.framework_path}

        # Bu projeyi klonla
        git clone <bu-repo-url> {args.name}
        cd {args.name}

        # Python bağımlılıklarını kur
        pip install -r {args.framework_path}/requirements.txt
        ```

        ## Kullanım

        ```powershell
        # Ortam kontrolü
        python {args.framework_path}/tools/check_environment.py --soft

        # Bölüm kod doğrulama
        python -m tools.code.extract_code_blocks `
          --package-root {args.framework_path} `
          --out-dir ./build/code `
          --manifest ./build/code_manifest.json `
          --chapters-dir ./chapters

        # Markdown kalite kontrolü
        python -m tools.quality.check_chapter_markdown `
          --chapter ./chapters/chapter_01.md `
          --chapter-id chapter_01 --chapter-no 1
        ```

        ## Framework bağlantısı

        Bu proje `.bookfactory` dosyasında tanımlı framework sürümünü kullanır.  
        Framework reposu: `{args.framework_path}`
    """), args.dry_run)

    # --- manifests/book_manifest.yaml ---
    make_file(output_root / "manifests" / "book_manifest.yaml", textwrap.dedent(f"""\
        # BookFactory Kitap Manifesti
        # Tek doğruluk kaynağı — tüm üretim bu dosyadan yönetilir.

        book:
          title: "{args.title}"
          subtitle: ""
          author: "{args.author or 'Yazar Adı'}"
          edition: "1"
          year: "{now[:4]}"

        language:
          primary_language: "{args.lang}"
          output_languages:
            - "{args.lang}"
          file_naming_language: "en"
          manifest_language: "en"
          automation_language: "en"

        structure:
          chapters: []  # chapter_id listesi buraya eklenecek

        approval_gates:
          manifest_validation: "required"
          chapter_input_generation: "optional"
          outline_review: "required"
          full_text_generation: "required"
          code_validation: "required"
          markdown_quality_check: "required"
          post_production_build: "optional"

        code:
          extract: true
          test: true
          github_sync: false
          qr_generation: false

        assets:
          screenshot_automation: false
          mermaid_generation: true
          manual_override: true
    """), args.dry_run)

    # --- configs/post_production_profile.yaml ---
    slug = args.name.lower().replace(" ", "_").replace("-", "_")
    make_file(output_root / "configs" / "post_production_profile.yaml", textwrap.dedent(f"""\
        # Post-Production Profili

        project_root: "."
        book_slug: "{slug}"
        chapters_dir: "chapters"
        output_dir: "dist"
        assets_dir: "assets"
        build_dir: "build"

        pandoc:
          reference_docx: ""   # Varsa referans DOCX yolunu girin
          lua_filter: ""       # Varsa Lua filter yolunu girin

        mermaid:
          enabled: true
          output_dir: "assets/auto/diagrams"

        stages:
          - merge_chapters
          - extract_mermaid
          - render_mermaid
          - build_docx
          - build_html
          - build_epub
    """), args.dry_run)

    # --- chapters/.gitkeep ---
    make_file(output_root / "chapters" / ".gitkeep", "", args.dry_run)
    make_file(output_root / "chapter_inputs" / ".gitkeep", "", args.dry_run)
    make_file(output_root / "screenshots" / ".gitkeep", "", args.dry_run)
    make_file(output_root / "assets" / "manual" / ".gitkeep", "", args.dry_run)
    make_file(output_root / "assets" / "locked" / ".gitkeep", "", args.dry_run)

    print(f"\n✓ Proje başarıyla oluşturuldu: {output_root}")
    print(f"\nSonraki adımlar:")
    print(f"  1. cd {output_root}")
    print(f"  2. git init && git add . && git commit -m 'init: {args.title}'")
    print(f"  3. manifests/book_manifest.yaml dosyasını doldurun")
    print(f"  4. Mevcut bölüm dosyalarını chapters/ klasörüne taşıyın")


if __name__ == "__main__":
    args = parse_args()
    scaffold(args)
