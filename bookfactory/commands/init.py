"""
bookfactory/commands/init.py

İnteraktif BookFactory kitap projesi başlatıcı.

Kullanım:
    python -m bookfactory init
    python -m bookfactory init --output ../projects
    python -m bookfactory init --non-interactive --config init_config.yaml
"""

from __future__ import annotations

import os
import sys
import textwrap
from datetime import datetime
from pathlib import Path

import yaml  # pyyaml

FRAMEWORK_VERSION = "v2.11.x"

# ─────────────────────────────────────────────
# Renk ve terminal yardımcıları
# ─────────────────────────────────────────────

USE_COLOR = sys.stdout.isatty() and os.name != "nt" or os.environ.get("FORCE_COLOR")

def c(text: str, code: str) -> str:
    if not USE_COLOR:
        return text
    codes = {"bold": "1", "dim": "2", "green": "32", "yellow": "33",
             "blue": "34", "cyan": "36", "red": "31", "reset": "0"}
    return f"\033[{codes.get(code, '0')}m{text}\033[0m"

def header(text: str) -> None:
    print()
    print(c("  " + text, "bold"))
    print(c("  " + "─" * len(text), "dim"))

def ok(text: str) -> None:
    print(c("  ✓ ", "green") + text)

def warn(text: str) -> None:
    print(c("  ⚠ ", "yellow") + text)

def err(text: str) -> None:
    print(c("  ✗ ", "red") + text, file=sys.stderr)

def ask(prompt: str, default: str = "", choices: list[str] | None = None) -> str:
    """Kullanıcıdan girdi al. Enter = default."""
    choice_str = f" [{'/'.join(choices)}]" if choices else ""
    default_str = f" (varsayılan: {c(default, 'cyan')})" if default else ""
    line = f"\n  {c('?', 'blue')} {prompt}{choice_str}{default_str}: "
    while True:
        val = input(line).strip()
        if not val and default:
            return default
        if choices and val not in choices:
            print(c(f"    Lütfen şunlardan birini girin: {', '.join(choices)}", "yellow"))
            continue
        if val:
            return val
        if not default:
            print(c("    Bu alan zorunlu.", "yellow"))

def ask_yn(prompt: str, default: bool = True) -> bool:
    """Evet/Hayır sorusu."""
    hint = "(E/h)" if default else "(e/H)"
    line = f"\n  {c('?', 'blue')} {prompt} {c(hint, 'dim')}: "
    val = input(line).strip().lower()
    if not val:
        return default
    return val in ("e", "evet", "y", "yes")

# ─────────────────────────────────────────────
# Stack şablonları
# ─────────────────────────────────────────────

STACKS: dict[str, dict] = {
    "web-react": {
        "label": "Web — React",
        "technologies": [
            "React 19", "Vite", "React Router v7", "TanStack Query",
            "Redux Toolkit", "Zustand", "React Hook Form",
            "Vitest + React Testing Library", "MSW",
        ],
        "out_of_scope": ["Next.js", "SSR/SSG", "React Native", "GraphQL"],
        "chapter_template": [
            "Modern Web'e Giriş", "JavaScript Temelleri", "Bileşen Düşüncesi",
            "JSX ve Render", "Props", "State ve Event", "useEffect",
            "Hook Kuralları", "Custom Hooks", "React Router",
            "Form Yönetimi", "State Yönetimi", "REST API",
            "Performans ve Test", "Dağıtım",
        ],
    },
    "web-vue": {
        "label": "Web — Vue",
        "technologies": ["Vue 3", "Vite", "Vue Router", "Pinia", "Vitest"],
        "out_of_scope": ["Nuxt.js", "SSR", "React"],
        "chapter_template": [
            "Vue'ya Giriş", "Bileşenler", "Composition API",
            "State Yönetimi (Pinia)", "Vue Router", "Test",
        ],
    },
    "java": {
        "label": "Java — Nesne Yönelimli Programlama",
        "technologies": ["Java 21", "Maven", "JUnit 5", "Spring Boot (giriş)"],
        "out_of_scope": ["Kotlin", "Scala", "Android"],
        "chapter_template": [
            "Java'ya Giriş", "Veri Tipleri", "Kontrol Yapıları",
            "Sınıflar ve Nesneler", "Kalıtım", "Arayüzler",
            "Koleksiyonlar", "Generic'ler", "Hata Yönetimi",
            "Dosya İşlemleri", "Çok İş Parçacığı", "Test",
        ],
    },
    "python": {
        "label": "Python — Programlamaya Giriş",
        "technologies": ["Python 3.12", "pytest", "pip", "venv"],
        "out_of_scope": ["Django", "FastAPI", "ML/AI"],
        "chapter_template": [
            "Python'a Giriş", "Değişkenler ve Tipler", "Kontrol Akışı",
            "Fonksiyonlar", "Listeler ve Sözlükler", "Dosya İşlemleri",
            "Nesne Yönelimli Programlama", "Modüller", "Test",
        ],
    },
    "data-science": {
        "label": "Veri Bilimi — Python",
        "technologies": ["Python 3.12", "NumPy", "Pandas", "Matplotlib",
                         "Scikit-learn", "Jupyter"],
        "out_of_scope": ["Deep Learning", "TensorFlow", "PyTorch"],
        "chapter_template": [
            "Veri Bilimine Giriş", "Python Temelleri", "NumPy",
            "Pandas", "Veri Görselleştirme", "İstatistik",
            "Makine Öğrenmesi Temelleri", "Sınıflandırma",
            "Regresyon", "Kümeleme", "Model Değerlendirme",
        ],
    },
    "mobile-flutter": {
        "label": "Mobil — Flutter",
        "technologies": ["Flutter 3", "Dart", "Riverpod", "go_router"],
        "out_of_scope": ["React Native", "Kotlin", "Swift"],
        "chapter_template": [
            "Flutter'a Giriş", "Dart Temelleri", "Widget Sistemi",
            "Layout", "State Yönetimi", "Navigasyon",
            "API Entegrasyonu", "Test ve Dağıtım",
        ],
    },
    "custom": {
        "label": "Özel stack (kendiniz tanımlayın)",
        "technologies": [],
        "out_of_scope": [],
        "chapter_template": [],
    },
}

LANGUAGES = {"tr": "Türkçe", "en": "English", "de": "Deutsch", "fr": "Français"}

# ─────────────────────────────────────────────
# Soru akışı
# ─────────────────────────────────────────────

def collect_answers(output_dir: Path) -> dict:
    print()
    print(c("  ╔══════════════════════════════════════════╗", "cyan"))
    print(c("  ║   BookFactory — Yeni Kitap Projesi       ║", "cyan"))
    print(c(f"  ║   Framework: {FRAMEWORK_VERSION:<28}║", "cyan"))
    print(c("  ╚══════════════════════════════════════════╝", "cyan"))

    answers: dict = {}

    # ── 1. Proje adı ──────────────────────────
    header("1/7  Proje kimliği")
    print(c("  Proje adı repo ve klasör adı olur. Küçük harf, tire kullanın.", "dim"))
    name = ask("Proje adı", default="my-book")
    slug = name.lower().replace(" ", "-")
    if slug != name:
        warn(f"Proje adı '{slug}' olarak normalleştirildi.")
    answers["name"] = slug

    # ── 2. Kitap başlığı ──────────────────────
    header("2/7  Kitap bilgileri")
    answers["title"] = ask("Kitap başlığı", default="Yazılım Geliştirme Kitabı")
    answers["subtitle"] = ask("Alt başlık (boş bırakılabilir)", default="")
    answers["author"] = ask("Yazar adı", default="Prof. Dr. İsmail KIRBAŞ")
    answers["edition"] = ask("Baskı", default="1")
    answers["year"] = ask("Yıl", default=str(datetime.now().year))

    # ── 3. Dil ───────────────────────────────
    header("3/7  Dil")
    for code, label in LANGUAGES.items():
        print(c(f"    {code}", "cyan") + f"  {label}")
    print(c("    (diğer)", "dim") + "  Başka bir kod girebilirsiniz")
    answers["lang"] = ask("Birincil içerik dili", default="tr")

    # ── 4. Stack seçimi ──────────────────────
    header("4/7  Teknoloji yığını")
    for key, val in STACKS.items():
        print(c(f"    {key:<20}", "cyan") + val["label"])
    stack_key = ask("Stack seçin", default="web-react", choices=list(STACKS.keys()))
    stack = STACKS[stack_key]
    answers["stack_key"] = stack_key
    answers["stack"] = stack

    if stack_key == "custom":
        print(c("\n  Teknolojileri virgülle ayırarak girin:", "dim"))
        tech_str = ask("Teknolojiler", default="Python, pytest")
        stack["technologies"] = [t.strip() for t in tech_str.split(",")]
        ooscope_str = ask("Kapsam dışı konular (virgülle, boş bırakılabilir)", default="")
        stack["out_of_scope"] = [t.strip() for t in ooscope_str.split(",") if t.strip()]

    ok(f"Seçilen stack: {stack['label']}")
    print(c("  Teknolojiler: ", "dim") + ", ".join(stack["technologies"][:5]) +
          (f" +{len(stack['technologies'])-5} daha" if len(stack["technologies"]) > 5 else ""))

    # ── 5. Kümülatif uygulama ─────────────────
    header("5/7  Kümülatif uygulama")
    print(c("  Kitap boyunca geliştirilen ana örnek uygulamanın adı.", "dim"))
    answers["app_name"] = ask("Uygulama adı (boş = yok)", default="")
    answers["app_desc"] = ""
    if answers["app_name"]:
        answers["app_desc"] = ask("Kısa açıklama", default="Öğretim amaçlı örnek uygulama")

    # ── 6. Çıktı dizini ve framework yolu ────
    header("6/7  Dizinler")
    default_output = str(output_dir)
    answers["output"] = ask("Projenin oluşturulacağı üst dizin", default=default_output)
    answers["framework_path"] = ask(
        "BookFactory framework yolu", default="../bookFactory"
    )

    # ── 7. Ek seçenekler ─────────────────────
    header("7/7  Ek seçenekler")
    answers["github_sync"] = ask_yn("GitHub sync ve QR üretimi etkin olsun mu?", default=False)
    answers["screenshot"] = ask_yn("Screenshot otomasyonu planlanıyor mu?", default=False)
    answers["multilang"] = ask_yn("Çok dilli üretim (ör. tr + en) istiyor musunuz?", default=False)
    if answers["multilang"]:
        lang_str = ask("Çıktı dilleri (virgülle)", default=f"{answers['lang']}, en")
        answers["output_languages"] = [lang.strip() for lang in lang_str.split(",")]
    else:
        answers["output_languages"] = [answers["lang"]]

    return answers


def show_summary(answers: dict) -> None:
    header("Özet — oluşturulacak proje")
    fields = [
        ("Proje adı",     answers["name"]),
        ("Kitap başlığı", answers["title"]),
        ("Yazar",         answers["author"]),
        ("Dil",           answers["lang"]),
        ("Stack",         answers["stack"]["label"]),
        ("Uygulama",      answers["app_name"] or "—"),
        ("Çıktı dizini",  answers["output"] + "/" + answers["name"]),
    ]
    for label, val in fields:
        print(f"    {c(label+':', 'dim'):<28} {val}")
    print()


# ─────────────────────────────────────────────
# Dosya üretimi
# ─────────────────────────────────────────────

def make(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def generate_manifest(a: dict) -> str:
    stack = a["stack"]
    chapters = []
    for i, title in enumerate(stack["chapter_template"], 1):
        num = str(i).zfill(2)
        slug = title.lower()
        for tr, en in [(" ", "_"), ("'", ""), ("ı", "i"), ("ğ", "g"),
                       ("ü", "u"), ("ş", "s"), ("ö", "o"), ("ç", "c"),
                       ("İ", "i"), ("ğ", "g")]:
            slug = slug.replace(tr, en)
        slug = "".join(c for c in slug if c.isalnum() or c == "_")
        chapters.append({
            "id": f"chapter_{num}",
            "title": title,
            "file": f"chapter_{num}_{slug}.md",
            "status": "planned",
        })

    data = {
        "schema": {
            "manifest_version": "1.0",
            "bookfactory_min_version": "2.11.0",
            "studio_min_version": "3.1.3",
        },
        "book": {
            "title": a["title"],
            "subtitle": a.get("subtitle", ""),
            "author": a["author"],
            "edition": a["edition"],
            "year": a["year"],
            "framework_version": FRAMEWORK_VERSION,
        },
        "language": {
            "primary_language": a["lang"],
            "output_languages": a["output_languages"],
            "file_naming_language": "en",
            "manifest_language": "en",
            "automation_language": "en",
        },
        "scope": {
            "stack": stack["technologies"],
            "out_of_scope": stack["out_of_scope"],
        },
        "structure": {"chapters": chapters},
        "approval_gates": {
            "manifest_validation": "required",
            "chapter_input_generation": "optional",
            "outline_review": "required",
            "full_text_generation": "required",
            "code_validation": "required",
            "markdown_quality_check": "required",
            "post_production_build": "optional",
        },
        "quality_gates": {
            "require_code_meta": True,
            "require_code_tests_passed": True,
            "require_screenshot_plan": True,
            "require_references": True,
            "require_outline_compliance": True,
        },
        "outputs": {
            "docx": True,
            "pdf": True,
            "epub": True,
            "html_site": True,
        },
        "ci": {
            "enabled": True,
            "fail_on_code_error": True,
            "fail_on_missing_screenshot": False,
        },
        "code": {
            "extract": True,
            "test": True,
            "github_sync": a["github_sync"],
            "qr_generation": a["github_sync"],
        },
        "assets": {
            "screenshot_automation": a["screenshot"],
            "mermaid_generation": True,
            "manual_override": True,
        },
    }

    if a["app_name"]:
        data["cumulative_app"] = {
            "name": a["app_name"],
            "description": a.get("app_desc", ""),
        }

    return yaml.dump(data, allow_unicode=True, sort_keys=False,
                     default_flow_style=False)


def generate_post_production_profile(a: dict) -> str:
    slug = a["name"].replace("-", "_")
    return textwrap.dedent(f"""\
        project_root: "."
        book_slug: "{slug}"
        chapters_dir: "chapters"
        output_dir: "dist"
        assets_dir: "assets"
        build_dir: "build"

        pandoc:
          reference_docx: ""
          lua_filter: ""

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
    """)


def generate_readme(a: dict) -> str:
    stack = a["stack"]
    tech_list = "\n".join(f"- {t}" for t in stack["technologies"])
    oos_list = "\n".join(f"- {t}" for t in stack["out_of_scope"]) or "—"
    app_section = ""
    if a["app_name"]:
        app_section = textwrap.dedent(f"""
            ## Kümülatif uygulama

            **{a['app_name']}** — {a.get('app_desc', '')}

            Kitap boyunca bu uygulama adım adım geliştirilir.
        """)

    return textwrap.dedent(f"""\
        # {a['title']}

        {a.get('subtitle', '')}

        **Framework:** Parametric Computer Book Factory {FRAMEWORK_VERSION}
        **Dil:** {LANGUAGES.get(a['lang'], a['lang'])}
        **Yazar:** {a['author']}
        **Başlangıç:** {a['year']}

        ---

        ## Teknoloji yığını

        {tech_list}

        **Kapsam dışı:**

        {oos_list}
        {app_section}
        ## Proje yapısı

        ```
        {a['name']}/
        ├── .bookfactory
        ├── chapters/
        ├── chapter_inputs/
        ├── manifests/book_manifest.yaml
        ├── configs/post_production_profile.yaml
        ├── assets/  auto/ manual/ locked/ final/
        ├── build/   code/ test_reports/
        ├── screenshots/
        └── dist/
        ```

        ## Kurulum

        ```powershell
        $env:PYTHONPATH = "{a['framework_path']}"

        python {a['framework_path']}/tools/check_environment.py --soft
        ```

        ## Kod doğrulama

        ```powershell
        python -m tools.code.extract_code_blocks `
          --package-root . `
          --out-dir ./build/code `
          --manifest ./build/code_manifest.json `
          --chapters-dir ./chapters

        python -m tools.code.run_code_tests `
          --manifest ./build/code_manifest.json `
          --package-root . `
          --report-json ./build/test_reports/code_test_report.json `
          --report-md ./build/test_reports/code_test_report.md `
          --node node --fail-on-error
        ```

        ## LLM başlangıç komutu

        ```
        Önce şu dosyaları oku:
        1. {a['framework_path']}/brief_core.md
        2. {a['framework_path']}/brief_llm_rules.md
        3. {a['framework_path']}/brief_standards.md
        4. manifests/book_manifest.yaml

        Kitap bağlamı: {a['title']}
        {f"Kümülatif uygulama: {a['app_name']}" if a['app_name'] else ""}
        Bölüm dosyaları: chapters/

        Eksik bilgiyi tahmin etme — sor. Kritik hata varsa dur.
        ```
    """)


def scaffold(a: dict) -> Path:
    root = Path(a["output"]).resolve() / a["name"]

    if root.exists():
        err(f"'{root}' zaten mevcut. Farklı bir proje adı veya dizin seçin.")
        sys.exit(1)

    dirs = [
        "chapters", "chapter_inputs", "manifests", "configs",
        "assets/auto/diagrams", "assets/auto/qr",
        "assets/manual", "assets/locked", "assets/final",
        "build/code", "build/test_reports",
        "screenshots", "dist",
    ]
    for d in dirs:
        (root / d).mkdir(parents=True, exist_ok=True)

    # .bookfactory
    make(root / ".bookfactory", textwrap.dedent(f"""\
        framework_version: "{FRAMEWORK_VERSION}"
        framework_path: "{a['framework_path']}"
        created: "{datetime.now().strftime('%Y-%m-%d')}"
        book_title: "{a['title']}"
        primary_language: "{a['lang']}"
        stack: "{a['stack_key']}"
        {f'cumulative_app: "{a["app_name"]}"' if a['app_name'] else ''}
    """))

    # .gitignore
    make(root / ".gitignore", textwrap.dedent("""\
        build/
        dist/
        assets/auto/
        *.bak
        *.tmp
        *.old
        __pycache__/
        *.pyc
        .DS_Store
        Thumbs.db
        .env
        node_modules/
    """))

    # manifests/book_manifest.yaml
    make(root / "manifests" / "book_manifest.yaml", generate_manifest(a))

    # configs/post_production_profile.yaml
    make(root / "configs" / "post_production_profile.yaml",
         generate_post_production_profile(a))

    # README.md
    make(root / "README.md", generate_readme(a))

    # .gitkeep — boş ama izlenen klasörler
    for d in ["chapters", "chapter_inputs", "screenshots",
              "assets/manual", "assets/locked"]:
        make(root / d / ".gitkeep", "")

    return root


# ─────────────────────────────────────────────
# Ana giriş noktası
# ─────────────────────────────────────────────

def run(output: str = ".", non_interactive: bool = False,
        config: str | None = None, dry_run: bool = False) -> None:
    output_dir = Path(output).resolve()

    if non_interactive and config:
        # YAML config dosyasından oku
        answers = yaml.safe_load(Path(config).read_text(encoding="utf-8"))
        answers.setdefault("stack", STACKS.get(answers.get("stack_key", "custom"),
                                                STACKS["custom"]))
    else:
        answers = collect_answers(output_dir)

    show_summary(answers)

    if not non_interactive:
        if not ask_yn("Proje oluşturulsun mu?", default=True):
            print(c("\n  İptal edildi.\n", "dim"))
            sys.exit(0)

    if dry_run:
        print(c("\n  [DRY RUN] Dosya oluşturulmadı.\n", "yellow"))
        return 0

    print()
    root = scaffold(answers)

    print()
    ok(f"Proje oluşturuldu: {c(str(root), 'cyan')}")
    print()
    print(c("  Sonraki adımlar:", "bold"))
    print(f"    1. cd {root}")
    print(f"    2. git init && git add . && git commit -m 'init: {answers['title']}'")
    print("    3. git remote add origin <repo-url> && git push -u origin main")
    print("    4. manifests/book_manifest.yaml dosyasını gözden geçirin")
    print()
