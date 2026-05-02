# BookFactory — Klasör ve Dosya Yapısı

**Modül:** `brief_structure.md`
**Yükleme önceliği:** 3 — Dosya/klasör işlemi yapılacaksa yükle
**İlgili modüller:** [`brief_core.md`](brief_core.md), [`brief_standards.md`](brief_standards.md)

---

## 1. Framework kök yapısı

```
BookFactory/                        ← Framework kökü (sabit, değişmez)
├── bookfactory/                    ← Ana Python paketi (CLI)
├── bookfactory_studio/             ← FastAPI GUI uygulaması
│   ├── app.py
│   ├── core.py
│   ├── jobs.py
│   └── static/
├── bookfactory-gui/                ← VS Code extension
├── core/                           ← LLM kontrat ve standartlar (00–20)
├── docs/                           ← Framework dokümantasyonu
│   ├── briefs/                     ← LLM oturum brief modülleri
│   └── studio/
├── examples/
├── schemas/
├── templates/
├── tools/                          ← Üretim araçları
├── configs/
├── scripts/                        ← Yönetim betikleri
├── tests/
├── build/                          ← Framework raporları (.gitkeep)
├── .devcontainer/
├── .github/
├── README.md, SETUP.md, CHANGELOG.md, RELEASE_CHECKLIST.md
├── pyproject.toml, requirements.txt, requirements-dev.txt
├── run_studio.ps1, run_studio.bat
└── .studio_config.json             ← Aktif kitap yolu (yerel, gitignore'da)
```

> **Önemli:** Kitap projeleri (`react-web`, vb.) framework'ten **tamamen ayrı** bağımsız Git depolarıdır.
> Studio GUI `Aktif Kitap` alanıyla bunları açar; framework dizinine dahil değildirler.

---

## 2. `core/` — LLM kontrat ve standartlar

```
core/
├── 00_llm_execution_contract.md
├── 01_book_manifest_schema.md
├── 02_general_system_prompt.md
├── 03_output_format_standard.md
├── 04_chapter_structure_standard.md
├── 05_chapter_input_generator_prompt.md
├── 06_outline_review_prompt.md
├── 07_full_text_generation_prompt.md
├── 08_quality_gate_contract.md
├── 09_manual_asset_override_policy.md
├── 10_multilingual_generation_policy.md
├── 11_approval_gate_policy.md
├── 12_project_starter_prompt.md
├── 13_post_production_pipeline_standard.md
├── 14_docx_build_and_formatting_policy.md
├── 15_generated_package_protocol.md
├── 16_code_validation_and_test_policy.md
├── 17_github_sync_and_qr_policy.md
├── 18_export_pipeline_policy.md
├── 19_indexing_dashboard_policy.md
└── 20_cloud_ide_codespaces_policy.md
```

| Dosya | Amaç |
|---|---|
| `00_llm_execution_contract.md` | LLM genel çalışma sözleşmesi |
| `01_book_manifest_schema.md` | Manifest alanları ve anlamları |
| `05_chapter_input_generator_prompt.md` | Manifestten bölüm girdi promptu üretimi |
| `12_project_starter_prompt.md` | Yeni kitap projesi başlatma |
| `16_code_validation_and_test_policy.md` | Kod çıkarma, doğrulama ve test |

---

## 3. Kitap projesi yapısı (ayrı repo)

Her kitap projesi framework'ten bağımsız bir Git deposudur.

```
{book_root}/                        ← Kitap proje kökü (örn. react-web/)
├── chapters/                       ← Bölüm Markdown dosyaları
│   └── chapter_{nn}_{slug}.md
├── prompts/
│   └── chapter_inputs/
│       └── chapter_{nn}_input.md
├── assets/
│   ├── auto/       ← Araç üretimi (üzerine yazılabilir)
│   ├── manual/     ← İnsan editörü — KORUNUR
│   ├── locked/     ← Onaylanmış — KORUNUR
│   └── final/
├── build/
│   ├── code/
│   ├── reports/
│   ├── test_reports/
│   └── quality_reports/
├── chapter_backups/
├── configs/
├── exports/
│   └── docx/ | html/ | epub/ | site/
├── book_manifest.yaml              ← Tek doğruluk kaynağı
└── manifests/
    └── book_manifest.yaml
```

**Kritik yollar:**

```
{book_root}/book_manifest.yaml
{book_root}/chapters/chapter_{nn}_{slug}.md
{book_root}/build/code_manifest.json
{book_root}/build/test_reports/code_test_report.md
{book_root}/prompts/chapter_inputs/chapter_{nn}_input.md
```

---

## 4. `docs/briefs/` — LLM oturum modülleri

```
docs/briefs/
├── LLM_PROJECT_BRIEF.md       ← Router/index — her oturumda başlangıç noktası
├── brief_core.md              ← Proje özeti ve temel ilkeler
├── brief_llm_rules.md         ← LLM davranış kuralları ve rolleri
├── brief_structure.md         ← Bu dosya
├── brief_standards.md         ← CODE_META, screenshot, Mermaid, QR standartları
├── brief_react_context.md     ← React kitabı bağlamı (kitaba özgü)
├── brief_environment.md       ← PowerShell 7, UTF-8, Codespaces
└── brief_loading_order.md     ← Yükleme sırası ve iş akışı
```

---

## 5. `tools/` — Üretim araçları

```
tools/
├── check_environment.py
├── check_package_integrity.py
├── validate_manifest.py
├── generate_chapter_inputs.py
├── scaffold_book_project.py
├── cloud/
│   ├── codespaces_check.py
│   ├── codespaces_init.py
│   └── write_puppeteer_config.py
├── code/
│   ├── extract_code_blocks.py
│   ├── validate_code_meta.py
│   ├── run_code_tests.py
│   ├── run_code_tests_docker.py
│   └── language_adapters/
│       ├── base_adapter.py, java_adapter.py
│       ├── javascript_adapter.py, python_adapter.py
├── dashboard/local_dashboard.py
├── export/export_book.py
├── github/
│   ├── sync_code_repository.py
│   ├── render_code_pages.py
│   └── setup_github_pages.py
├── indexing/build_glossary_index.py
├── postproduction/
│   ├── post_production_pipeline.py
│   ├── merge_chapters.py
│   ├── generate_qr_codes.py
│   ├── prepare_mermaid_images.py
│   ├── render_mermaid_png.py
│   └── resolve_assets.py (+ diğerleri)
├── quality/check_chapter_markdown.py
└── utils/
    ├── process_utils.py
    └── yaml_utils.py
```

### Kod doğrulama zinciri

```
extract_code_blocks → validate_code_meta → run_code_tests
```

---

## 6. Assets — Görsel öncelik politikası

**Öncelik:** `manual > locked > auto`

`assets/manual/` ve `assets/locked/` hiçbir araç tarafından silinmez veya üzerine yazılmaz.

---

## 7. Studio GUI

```powershell
cd "C:\...\BookFactory"
python -m bookfactory_studio.app   # veya: .\run_studio.ps1
```

Tarayıcı: `http://127.0.0.1:8765`

Studio, aktif kitap yolunu `.studio_config.json`'da kalıcı saklar — sayfa yenilenince otomatik yüklenir.
