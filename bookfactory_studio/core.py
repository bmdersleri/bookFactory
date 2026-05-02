from __future__ import annotations

import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


MANIFEST_CANDIDATES = (
    "book_manifest.yaml",
    "manifests/book_manifest.yaml",
)

SAFE_DIRS = [
    "prompts/chapter_inputs",
    "chapters",
    "chapter_backups",
    "assets/auto/mermaid",
    "assets/auto/qr",
    "assets/auto/screenshots",
    "assets/manual",
    "assets/final",
    "build/code",
    "build/reports",
    "build/quality_reports",
    "build/test_reports",
    "build/studio_jobs",
    "exports/docx",
    "exports/html",
    "exports/epub",
    "exports/site",
    "configs",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def project_root(path: str | None = None) -> Path:
    base = Path(path or ".").expanduser()
    if not base.is_absolute():
        base = Path.cwd() / base
    return base.resolve()


def framework_root() -> Path:
    """Return the BookFactory framework root that contains tools/, schemas/ and bookfactory_studio/.

    Book projects are intentionally independent from this framework root.  A user can
    point the Studio to `react-web`, `workspace/react`, `javanin-temelleri`, etc.;
    the production commands are still executed with the framework tools from here.
    """
    return Path(__file__).resolve().parents[1]


def safe_relative(path: Path | None, base: Path) -> str:
    if path is None:
        return ""
    try:
        return str(path.resolve().relative_to(base.resolve())).replace("\\", "/")
    except Exception:
        return str(path)


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"YAML dosyası bulunamadı: {path}")
    text = path.read_text(encoding="utf-8")
    if yaml is None:
        raise RuntimeError("PyYAML yüklü değil. `pip install pyyaml` komutunu çalıştırın.")
    data = yaml.safe_load(text) or {}
    if not isinstance(data, dict):
        raise ValueError("Manifest kök yapısı object/dict olmalıdır.")
    return data


def parse_yaml_text(text: str) -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML yüklü değil. `pip install pyyaml` komutunu çalıştırın.")
    data = yaml.safe_load(text) or {}
    if not isinstance(data, dict):
        raise ValueError("YAML kök yapısı object/dict olmalıdır.")
    return data


def dump_yaml(data: dict[str, Any]) -> str:
    if yaml is None:
        raise RuntimeError("PyYAML yüklü değil. `pip install pyyaml` komutunu çalıştırın.")
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=110)


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_yaml(data), encoding="utf-8")


def find_manifest(root: Path) -> Path | None:
    """Find the manifest that belongs to the selected book root.

    This deliberately does NOT recurse into arbitrary subdirectories.  Earlier
    versions searched `**/book_manifest.yaml`; when the user selected the
    BookFactory framework root, Studio found `workspace/react/book_manifest.yaml`
    but still looked for chapters under `BookFactory/chapters`.  The selected root
    must therefore be the book root itself, for example `react-web` or
    `workspace/react`.
    """
    framework_like = (root / "bookfactory_studio").exists() and (root / "tools").exists()
    for candidate in MANIFEST_CANDIDATES:
        # A framework root may contain manifests/book_manifest.yaml for examples or
        # templates.  It should not be treated as the active book workspace.
        if framework_like and candidate.startswith("manifests/"):
            continue
        path = root / candidate
        if path.exists():
            return path
    return None


def discover_book_roots(base: Path, max_depth: int = 3) -> list[dict[str, Any]]:
    """Discover independent book workspaces below a directory.

    Used only as a navigation aid; it never changes the active root implicitly.
    """
    base = base.resolve()
    ignore_parts = {".git", ".venv", "venv", "node_modules", "__pycache__", ".cleanup_quarantine"}
    rows: list[dict[str, Any]] = []
    if not base.exists():
        return rows
    for path in sorted(base.rglob("book_manifest.yaml")):
        rel_parts = path.relative_to(base).parts
        if len(rel_parts) > max_depth + 1:
            continue
        if any(part in ignore_parts for part in rel_parts):
            continue
        book_root = path.parent if path.parent.name != "manifests" else path.parent.parent
        if (book_root / "bookfactory_studio").exists() and (book_root / "tools").exists() and path.parent.name == "manifests":
            continue
        try:
            manifest = load_yaml(path)
            title = (manifest.get("book") or {}).get("title", "")
            chapters = len(chapters_from_manifest(manifest))
        except Exception:
            title = ""
            chapters = 0
        rows.append({
            "root": str(book_root),
            "path": safe_relative(book_root, base),
            "manifest": safe_relative(path, book_root),
            "title": title,
            "chapters": chapters,
        })
    # De-duplicate book roots while preserving order.
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for row in rows:
        key = row["root"]
        if key not in seen:
            unique.append(row)
            seen.add(key)
    return unique


def chapters_from_manifest(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    chapters = manifest.get("structure", {}).get("chapters")
    if chapters is None:
        chapters = manifest.get("chapters")
    if not isinstance(chapters, list):
        return []
    return [c for c in chapters if isinstance(c, dict)]


def chapter_id(chapter: dict[str, Any], order: int) -> str:
    return str(chapter.get("id") or chapter.get("chapter_id") or f"chapter_{order:02d}")


def chapter_file(chapter: dict[str, Any], order: int) -> str:
    cid = chapter_id(chapter, order)
    title = str(chapter.get("title") or chapter.get("name") or cid)
    if chapter.get("file"):
        return Path(str(chapter["file"])).name
    if chapter.get("path"):
        return Path(str(chapter["path"])).name
    return f"{cid}_{slugify_ascii(title)}.md"


def chapter_markdown_path(root: Path, chapter: dict[str, Any], order: int) -> Path:
    """Resolve a chapter markdown file for an independent book root.

    Older manifests may contain paths such as
    `workspace/react/chapters/chapter_01_...md`, which were meaningful when the
    BookFactory framework root was the working directory.  When the active root is
    the independent book folder (`workspace/react` or `react-web`), the correct
    location is `root/chapters/<filename>`.  This resolver handles both styles.
    """
    raw = str(chapter.get("path") or chapter.get("file") or "").strip()
    if raw:
        p = Path(raw)
        if p.is_absolute():
            return p
        direct = root / p
        if direct.exists():
            return direct
        parts = p.parts
        if "chapters" in parts:
            idx = parts.index("chapters")
            return root.joinpath(*parts[idx:])
    return root / "chapters" / chapter_file(chapter, order)


def slugify_ascii(text: str) -> str:
    tr = str.maketrans({
        "ç": "c", "Ç": "c", "ğ": "g", "Ğ": "g", "ı": "i", "I": "i", "İ": "i",
        "ö": "o", "Ö": "o", "ş": "s", "Ş": "s", "ü": "u", "Ü": "u",
    })
    text = text.translate(tr).lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return re.sub(r"_+", "_", text).strip("_") or "book"


def normalize_manifest(raw: dict[str, Any]) -> dict[str, Any]:
    manifest = dict(raw)
    manifest.setdefault("book", {})
    manifest.setdefault("language", {})
    manifest.setdefault("structure", {})
    if "chapters" in manifest and "chapters" not in manifest["structure"]:
        manifest["structure"]["chapters"] = manifest.pop("chapters")
    manifest.setdefault("approval_gates", {})
    manifest.setdefault("code", {})
    manifest.setdefault("assets", {})
    manifest.setdefault("project", {})
    manifest["project"].setdefault("status", "in_progress")
    manifest["project"].setdefault("paths", {
        "chapters": "chapters",
        "chapter_prompts": "prompts/chapter_inputs",
        "chapter_backups": "chapter_backups",
        "build": "build",
        "assets": "assets",
        "exports": "exports",
    })
    manifest["project"]["updated_at"] = utc_now()
    return manifest


def validate_manifest(manifest: dict[str, Any], root: Path | None = None) -> dict[str, Any]:
    """Validate a book manifest for GUI editing and production safety.

    The validator separates blocking errors from warnings.  Errors prevent saving
    from the form/YAML editor unless the API is explicitly called with force.
    Warnings are shown to the user but do not block saving.
    """
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(manifest, dict):
        return {"valid": False, "errors": ["Manifest object/dict olmalıdır."], "warnings": []}

    book = manifest.get("book") or {}
    if not isinstance(book, dict):
        errors.append("book alanı object/dict olmalıdır.")
        book = {}
    if not str(book.get("title") or "").strip():
        errors.append("book.title eksik.")
    if not str(book.get("author") or "").strip():
        errors.append("book.author eksik.")
    year = str(book.get("year") or "").strip()
    if year and not re.match(r"^[0-9]{4}$", year):
        errors.append("book.year dört haneli yıl biçiminde olmalıdır.")

    language = manifest.get("language") or {}
    if not isinstance(language, dict):
        errors.append("language alanı object/dict olmalıdır.")
        language = {}
    book_language = book.get("language") or book.get("lang")
    if not language.get("primary_language") and not book_language:
        errors.append("language.primary_language eksik veya book.language tanımlı değil.")
    out_langs = language.get("output_languages")
    if out_langs is not None and not isinstance(out_langs, list):
        warnings.append("language.output_languages liste olmalıdır; örnek: ['tr']")

    project = manifest.get("project") or {}
    if project and not isinstance(project, dict):
        errors.append("project alanı object/dict olmalıdır.")
        project = {}
    paths = project.get("paths") or {}
    if paths and not isinstance(paths, dict):
        errors.append("project.paths alanı object/dict olmalıdır.")
        paths = {}
    for key, value in paths.items():
        rel = str(value or "").strip()
        if not rel:
            warnings.append(f"project.paths.{key} boş görünüyor.")
            continue
        p = Path(rel)
        if p.is_absolute():
            errors.append(f"project.paths.{key} mutlak yol olmamalıdır: {rel}")
        if ".." in p.parts:
            errors.append(f"project.paths.{key} üst klasöre çıkmamalıdır: {rel}")

    chapters = chapters_from_manifest(manifest)
    if not chapters:
        errors.append("structure.chapters listesi eksik veya boş.")

    seen_ids: set[str] = set()
    seen_files: set[str] = set()
    allowed_status = {"planned", "prompt_ready", "in_progress", "draft", "review", "done", "skipped", "archived"}
    unsafe_name_re = re.compile(r"^[A-Za-z0-9_./-]+\.md$")

    for i, ch in enumerate(chapters, start=1):
        cid = chapter_id(ch, i).strip()
        cfile = chapter_file(ch, i).strip()
        raw_file = str(ch.get("file") or ch.get("path") or cfile).strip()

        if not re.match(r"^chapter_[0-9]{2}$", cid):
            warnings.append(f"{cid}: id önerilen chapter_XX biçiminde değil.")
        expected_id = f"chapter_{i:02d}"
        if cid != expected_id:
            warnings.append(f"{cid}: sıra numarasına göre beklenen id {expected_id}.")
        if cid in seen_ids:
            errors.append(f"Tekrarlanan bölüm id: {cid}")
        seen_ids.add(cid)

        if not str(ch.get("title") or "").strip():
            errors.append(f"{cid}: title eksik.")

        if not cfile.endswith(".md"):
            errors.append(f"{cid}: file .md ile bitmeli.")
        if any(part == ".." for part in Path(raw_file).parts):
            errors.append(f"{cid}: file/path üst klasöre çıkmamalıdır: {raw_file}")
        if Path(raw_file).is_absolute():
            errors.append(f"{cid}: file/path mutlak yol olmamalıdır: {raw_file}")
        if " " in cfile:
            errors.append(f"{cid}: dosya adında boşluk olmamalıdır: {cfile}")
        if not unsafe_name_re.match(cfile):
            errors.append(f"{cid}: dosya adı güvenli ASCII biçiminde olmalıdır: {cfile}")
        if cfile in seen_files:
            errors.append(f"Tekrarlanan bölüm dosyası: {cfile}")
        seen_files.add(cfile)

        status = str(ch.get("status") or "planned")
        if status not in allowed_status:
            warnings.append(f"{cid}: status alışılmış değerlerden biri değil: {status}")

        if root is not None:
            chapter_path = chapter_markdown_path(root, ch, i)
            if status in {"done", "draft", "review", "in_progress"} and not chapter_path.exists():
                warnings.append(f"{cid}: status '{status}' ancak dosya bulunamadı: {safe_relative(chapter_path, root)}")

    return {"valid": not errors, "errors": errors, "warnings": warnings}


def match_chapter_files(root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Match manifest chapter file names against files in root/chapters.

    For each chapter, the function first checks the current resolved file.  If it
    does not exist, it looks for markdown files that start with the chapter id,
    such as `chapter_02_*.md`, and updates `chapter.file` to that real filename.
    """
    manifest = normalize_manifest(manifest)
    chapters_dir = root / "chapters"
    changes: list[dict[str, Any]] = []
    unmatched: list[dict[str, Any]] = []
    chapters_dir.mkdir(parents=True, exist_ok=True)
    all_md = sorted(chapters_dir.glob("*.md"))

    for i, ch in enumerate(chapters_from_manifest(manifest), start=1):
        cid = chapter_id(ch, i)
        current = chapter_markdown_path(root, ch, i)
        old_file = chapter_file(ch, i)
        if current.exists():
            ch["file"] = current.name
            continue
        candidates = sorted(chapters_dir.glob(f"{cid}_*.md"))
        if not candidates:
            # Secondary heuristic: use order if a file starts with chapter number.
            candidates = [p for p in all_md if p.name.startswith(f"chapter_{i:02d}_")]
        if candidates:
            new_file = candidates[0].name
            ch["file"] = new_file
            if old_file != new_file:
                changes.append({"id": cid, "old_file": old_file, "new_file": new_file})
        else:
            unmatched.append({"id": cid, "expected_file": old_file, "title": ch.get("title", "")})

    manifest.setdefault("project", {})["updated_at"] = utc_now()
    return {
        "manifest": manifest,
        "changes": changes,
        "unmatched": unmatched,
        "validation": validate_manifest(manifest, root=root),
    }


def ensure_workspace(root: Path) -> None:
    for rel in SAFE_DIRS:
        (root / rel).mkdir(parents=True, exist_ok=True)


def write_minimal_profile(root: Path) -> Path:
    profile = root / "configs" / "post_production_profile_studio.yaml"
    if profile.exists():
        return profile
    profile.write_text(
        """# BookFactory Studio varsayılan post-production profili
project_root: .

post_production:
  project_root: .
  chapters_dir: chapters
  build:
    merged_markdown: build/merged/book_merged.md
  assets:
    mermaid_dir: assets/auto/mermaid
    qr_dir: assets/auto/qr
exports:
  output_dir: exports
  formats:
    - docx
    - html
""",
        encoding="utf-8",
    )
    return profile


def initialize_project(root: Path, manifest: dict[str, Any], copy_manifest_to_manifests: bool = True) -> dict[str, Any]:
    ensure_workspace(root)
    manifest = normalize_manifest(manifest)
    write_yaml(root / "book_manifest.yaml", manifest)
    if copy_manifest_to_manifests:
        write_yaml(root / "manifests" / "book_manifest.yaml", manifest)
    write_minimal_profile(root)
    return project_snapshot(root)


def project_snapshot(root: Path) -> dict[str, Any]:
    manifest_path = find_manifest(root)
    manifest: dict[str, Any] = {}
    discovered = discover_book_roots(root) if root.exists() else []
    framework_like = (root / "bookfactory_studio").exists() and (root / "tools").exists()
    base_errors = ["Manifest bulunamadı. Proje kökü olarak BookFactory framework klasörünü değil, ilgili kitap klasörünü seçin."] if framework_like else ["Manifest bulunamadı."]
    validation = {"valid": False, "errors": base_errors, "warnings": []}
    if manifest_path:
        manifest = load_yaml(manifest_path)
        validation = validate_manifest(manifest, root=root)
    chapters = chapters_from_manifest(manifest)
    chapter_rows = []
    for i, ch in enumerate(chapters, start=1):
        cid = chapter_id(ch, i)
        cfile = chapter_file(ch, i)
        chapter_path = chapter_markdown_path(root, ch, i)
        prompt_path = root / "prompts" / "chapter_inputs" / f"{cid}_input.md"
        chapter_rows.append({
            "order": i,
            "id": cid,
            "title": ch.get("title", ""),
            "file": cfile,
            "status": ch.get("status", "planned"),
            "chapter_exists": chapter_path.exists(),
            "chapter_path": safe_relative(chapter_path, root),
            "prompt_exists": prompt_path.exists(),
            "prompt_path": safe_relative(prompt_path, root),
            "size": chapter_path.stat().st_size if chapter_path.exists() else 0,
        })
    counts: dict[str, int] = {}
    for row in chapter_rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    return {
        "root": str(root),
        "framework_root": str(framework_root()),
        "is_framework_root": framework_like,
        "manifest_path": safe_relative(manifest_path, root) if manifest_path else None,
        "manifest": manifest,
        "validation": validation,
        "chapters": chapter_rows,
        "chapter_status_counts": counts,
        "reports": list_reports(root, include_content=False),
        "discovered_book_roots": discovered,
    }


def render_architecture_prompt(data: dict[str, Any]) -> str:
    book = data.get("book", {})
    language = data.get("language", {})
    cumulative_app = data.get("cumulative_app", {})
    scope = data.get("scope", {})
    chapter_count = data.get("chapter_count") or len(data.get("chapters", [])) or 12
    subject = data.get("subject") or book.get("description") or "Belirtilmemiş"
    audience = data.get("target_audience") or data.get("audience") or "Belirtilmemiş"
    prerequisites = data.get("prerequisites") or "Belirtilmemiş"
    teaching = data.get("teaching_pattern") or "kavram → örnek → uygulama → mini görev → kontrol listesi"
    stack = scope.get("stack") or []
    out_scope = scope.get("out_of_scope") or []

    def bullet(items: Any) -> str:
        if isinstance(items, str):
            return f"- {items}"
        if not items:
            return "- Belirtilmemiş"
        return "\n".join(f"- {x}" for x in items)

    return f"""# Kitap Yapısı ve Manifest Tasarımı Üretim Promptu

Sen kıdemli bir bilgisayar mühendisliği akademisyeni, teknik kitap editörü ve öğretim tasarım uzmanısın.
Aşağıdaki bilgilerden hareketle uygulamalı, bölüm bölüm ilerleyen, tutarlı ve üretime hazır bir teknik kitap kurgusu tasarla.

## 1. Temel kitap bilgileri

- Kitap adı: {book.get('title', '')}
- Alt başlık: {book.get('subtitle', '')}
- Yazar: {book.get('author', '')}
- Yıl: {book.get('year', '')}
- Ana dil: {language.get('primary_language', 'tr')}
- Hedef çıktı dilleri: {', '.join(language.get('output_languages', ['tr']))}
- Kitap konusu: {subject}
- Hedef kitle: {audience}
- Ön koşullar: {prerequisites}
- Tahmini bölüm sayısı: {chapter_count}
- Öğretim yaklaşımı: {teaching}
- Kitabın genel uygulama projesi: {cumulative_app.get('name', '')}
- Uygulama açıklaması: {cumulative_app.get('description', '')}

## 2. Teknoloji kapsamı

Kitapta yer alması istenen teknolojiler:

{bullet(stack)}

Kitap kapsamı dışında tutulacak konular:

{bullet(out_scope)}

## 3. Üretilecek çıktı

Aşağıdaki YAML şemasına uygun, doğrudan `book_manifest.yaml` dosyasına dönüştürülebilecek bir çıktı üret.
Tam metin yazma. Yalnızca kitap yapısı, bölüm planı, kapsam ve üretim metaverisi üret.

## 4. Beklenen YAML alanları

```yaml
book:
  title:
  subtitle:
  author:
  edition:
  year:
  framework_version:
  description:
  target_audience:
  prerequisites:
  learning_goals:

language:
  primary_language:
  output_languages:
  file_naming_language: en
  manifest_language: en
  automation_language: en

cumulative_app:
  name:
  description:
  pedagogical_role:
  final_capabilities:

scope:
  stack:
  out_of_scope:
  assumptions:
  constraints:

structure:
  chapters:
    - id: chapter_01
      title:
      file: chapter_01_example.md
      status: planned
      summary:
      learning_outcomes:
      key_concepts:
      cumulative_app_increment:
      expected_code_outputs:
      expected_visual_outputs:
      screenshot_plan:
        - id:
          title:
          route:
          caption:

approval_gates:
  manifest_validation: required
  chapter_input_generation: optional
  outline_review: required
  full_text_generation: required
  code_validation: required
  markdown_quality_check: required
  post_production_build: optional

code:
  extract: true
  test: true
  github_sync: false
  qr_generation: false

assets:
  screenshot_automation: false
  mermaid_generation: true
  manual_override: true

github:
  enabled: false
  owner:
  repo:
  branch: main
  pages:
    enabled: false
    source: docs
  codespaces:
    enabled: false
    check_required: true
```

## 5. Kalite kuralları

- Bölüm başlıkları pedagojik olarak basitten karmaşığa ilerlemeli.
- Her bölüm önceki bölümler üzerine inşa edilmeli.
- Kitap genelinde tek bir kümülatif uygulama gelişmeli.
- Kapsam dışı konular bölüm planına sızmamalı.
- Her bölüm için en az bir somut uygulama çıktısı tanımlanmalı.
- Görsel ağırlıklı bölümlerde ekran görüntüsü planı olmalı.
- Kod üretilecek bölümlerde test edilebilir çıktı beklentisi belirtilmeli.
- Dosya adları küçük harfli, İngilizce ve güvenli olmalı.
- Çıktı yalnızca YAML olmalı.
"""


def save_architecture_prompt(root: Path, data: dict[str, Any]) -> dict[str, Any]:
    prompt = render_architecture_prompt(data)
    path = root / "prompts" / "project_architecture_prompt.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(prompt, encoding="utf-8")
    return {"prompt": prompt, "path": safe_relative(path, root)}


def render_chapter_input_prompt(manifest: dict[str, Any], chapter: dict[str, Any], order: int) -> str:
    book = manifest.get("book", {})
    language = manifest.get("language", {})
    scope = manifest.get("scope", {})
    app = manifest.get("cumulative_app", {})
    cid = chapter_id(chapter, order)
    title = str(chapter.get("title") or cid)
    cfile = chapter_file(chapter, order)
    stack = scope.get("stack") or []
    out_scope = scope.get("out_of_scope") or []

    def bullet(items: Any) -> str:
        if isinstance(items, str):
            return f"- {items}"
        if not items:
            return "- Belirtilmemiş"
        return "\n".join(f"- {x}" for x in items)

    return f"""# BÖLÜM GİRDİ PROMPTU — {title}

Sen teknik kitap yazımı, React tabanlı web programlama eğitimi ve LLM destekli içerik üretimi konusunda uzman bir akademik editörsün.
Aşağıdaki manifest bilgilerine göre yalnızca bu bölüm için önce ayrıntılı ve üretime hazır bir tam metin üret.

## 1. Kitap bağlamı

- Kitap adı: {book.get('title', '')}
- Alt başlık: {book.get('subtitle', '')}
- Yazar: {book.get('author', '')}
- Ana dil: {language.get('primary_language', 'tr')}
- Bölüm kimliği: {cid}
- Bölüm dosyası: `{cfile}`
- Bölüm başlığı: {title}
- Bölüm durumu: {chapter.get('status', 'planned')}

## 2. Kitap boyunca geliştirilen uygulama

- Uygulama adı: {app.get('name', '')}
- Açıklama: {app.get('description', '')}

Bu bölümde uygulamaya eklenecek katkı:

{chapter.get('cumulative_app_increment') or chapter.get('summary') or 'Manifestte açıkça belirtilmemiştir; bölüm içeriğiyle uyumlu, küçük ve test edilebilir bir katkı tasarla.'}

## 3. Teknoloji kapsamı

Kapsam içi teknolojiler:

{bullet(stack)}

Kapsam dışı konular:

{bullet(out_scope)}

## 4. Beklenen bölüm yapısı

Bölüm aşağıdaki yapıyı izlemelidir:

1. Bölümün amacı ve öğrenme çıktıları
2. Temel kavramlar
3. Kavramları açıklayan kısa örnekler
4. KampüsHub uygulamasına bölüm katkısı
5. Test edilebilir kod örnekleri
6. Mermaid diyagramları gerektiğinde `mermaid` kod bloğu olarak
7. Programatik ekran çıktısı planı gerektiğinde `[SCREENSHOT:{cid}_01_aciklayici_ad]` standardıyla
8. Mini uygulama görevi
9. Sık yapılan hatalar
10. Bölüm sonu kontrol listesi
11. Kısa özet

## 5. Kod üretim kuralları

Kod blokları test edilebilir olmalıdır. Her çalıştırılabilir kod bloğunun hemen önünde aşağıdaki biçimde CODE_META bulunmalıdır:

```html
<!-- CODE_META
id: {cid}_code01
chapter_id: {cid}
language: javascript
file: src/example.js
test: syntax
-->
```

Ardından uygun dil etiketiyle kod bloğu verilmelidir.

## 6. Görsel ve ekran çıktısı kuralları

- Mermaid diyagramları geçerli sözdizimiyle yazılmalıdır.
- Screenshot gerekiyorsa Markdown içinde açık hedef etiketi kullanılmalıdır.
- Görsel başlıkları ve açıklamaları akademik kitap üslubunda verilmelidir.

## 7. Üslup

- Dil: Türkçe
- Üslup: akıcı, öğretici, uygulamalı ve akademik doğruluğa sahip
- Başlıklar manuel bölüm numarası içermemelidir; numaralandırma build aşamasında yapılacaktır.
- Kapsam dışı teknolojiler ana öğretim içeriğine sokulmamalıdır.
"""


def generate_chapter_prompts(root: Path) -> dict[str, Any]:
    manifest_path = find_manifest(root)
    if not manifest_path:
        raise FileNotFoundError("Manifest bulunamadı.")
    manifest = load_yaml(manifest_path)
    out_dir = root / "prompts" / "chapter_inputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    generated = []
    for i, ch in enumerate(chapters_from_manifest(manifest), start=1):
        cid = chapter_id(ch, i)
        path = out_dir / f"{cid}_input.md"
        path.write_text(render_chapter_input_prompt(manifest, ch, i), encoding="utf-8")
        generated.append({"id": cid, "path": safe_relative(path, root)})
    return {"count": len(generated), "generated": generated}


def import_chapter_markdown(root: Path, cid: str, content: str) -> dict[str, Any]:
    manifest_path = find_manifest(root)
    if not manifest_path:
        raise FileNotFoundError("Manifest bulunamadı.")
    manifest = load_yaml(manifest_path)
    target_file: str | None = None
    for i, ch in enumerate(chapters_from_manifest(manifest), start=1):
        if chapter_id(ch, i) == cid:
            target_file = chapter_file(ch, i)
            ch["status"] = "draft"
            break
    if not target_file:
        raise ValueError(f"Bölüm bulunamadı: {cid}")
    target = chapter_markdown_path(root, ch, i) if 'ch' in locals() else root / "chapters" / target_file
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        backup = root / "chapter_backups" / f"{target.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, backup)
    target.write_text(content, encoding="utf-8")
    write_yaml(manifest_path, manifest)
    return {"id": cid, "path": safe_relative(target, root), "bytes": target.stat().st_size}


def list_reports(root: Path, include_content: bool = False) -> list[dict[str, Any]]:
    report_roots = [root / "build", root / "exports"]
    rows: list[dict[str, Any]] = []
    for base in report_roots:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".md", ".json", ".yaml", ".yml", ".log", ".txt"}:
                continue
            item = {
                "path": safe_relative(path, root),
                "name": path.name,
                "type": path.suffix.lower().lstrip("."),
                "size": path.stat().st_size,
                "modified": datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
            }
            if include_content:
                try:
                    item["content"] = path.read_text(encoding="utf-8", errors="replace")[:20000]
                except Exception as exc:
                    item["content"] = f"[Okunamadı: {exc}]"
            rows.append(item)
    return rows


def read_text_report(root: Path, rel_path: str) -> dict[str, Any]:
    path = (root / rel_path).resolve()
    if not str(path).startswith(str(root.resolve())):
        raise ValueError("Proje kökü dışındaki dosyalar okunamaz.")
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(rel_path)
    return {"path": safe_relative(path, root), "content": path.read_text(encoding="utf-8", errors="replace")}


def pipeline_steps() -> list[dict[str, Any]]:
    return [
        {"id": "validate_manifest", "title": "Manifest doğrulama", "group": "Hazırlık"},
        {"id": "generate_chapter_prompts", "title": "Bölüm girdi promptlarını üret", "group": "Hazırlık"},
        {"id": "outline_check", "title": "Bölüm Markdown kalite / outline kontrolü", "group": "Kalite"},
        {"id": "extract_code", "title": "CODE_META kod bloklarını çıkar", "group": "Kod"},
        {"id": "validate_code", "title": "Kod manifestini doğrula", "group": "Kod"},
        {"id": "test_code", "title": "Kodları test et", "group": "Kod"},
        {"id": "mermaid_extract", "title": "Mermaid bloklarını çıkar", "group": "Görsel"},
        {"id": "mermaid_render", "title": "Mermaid PNG üret", "group": "Görsel"},
        {"id": "qr_manifest", "title": "QR manifest üret", "group": "QR"},
        {"id": "qr_generate", "title": "QR PNG üret", "group": "QR"},
        {"id": "github_sync", "title": "GitHub kod senkronizasyonu", "group": "GitHub"},
        {"id": "pages_setup", "title": "GitHub Pages dosyalarını hazırla", "group": "GitHub"},
        {"id": "codespaces_check", "title": "Codespaces kontrolü", "group": "GitHub"},
        {"id": "export", "title": "DOCX/HTML/EPUB export", "group": "Çıktı"},
        {"id": "full_production", "title": "Tam üretim hattı", "group": "Çıktı"},
    ]
