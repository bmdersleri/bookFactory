# BookFactory — Klasör ve Dosya Yapısı

**Modül:** `brief_structure.md`  
**Yükleme önceliği:** 3 — Dosya/klasör işlemi yapılacaksa yükle  
**İlgili modüller:** [`brief_core.md`](brief_core.md), [`brief_standards.md`](brief_standards.md)

---

## 1. Güncel proje kök yapısı

```
BookFactory/
├── .devcontainer/
├── .github/
│   ├── codespaces/
│   └── workflows/
├── assets/
│   ├── auto/
│   ├── final/
│   ├── locked/
│   └── manual/
├── bookfactory/
├── build/
├── configs/
├── core/
├── docs/
├── examples/
├── manifests/
├── schemas/
├── templates/
├── tests/
├── tools/
├── workspace/
│   └── react/
├── README.md
├── SETUP.md
├── KULLANIM_KILAVUZU.md
├── LLM_PROJECT_BRIEF.md
├── RELEASE_CHECKLIST.md
├── CHANGELOG.md
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── checksums.sha256
```

> Not: Bazı klasörler proje sürümüne veya kullanıcının yerel arşivleme işlemlerine göre bulunmayabilir. LLM, bir dosyanın varlığından emin değilse kullanıcıdan çıktı istemeli veya dosya listesini temel almalıdır.

---

## 2. `core/` klasörü

`core/` klasörü LLM'in çalışma kurallarını ve üretim standartlarını içerir.

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

### Çekirdek belgeler özeti

| Dosya | Amaç |
|---|---|
| `00_llm_execution_contract.md` | LLM'in genel çalışma sözleşmesi |
| `01_book_manifest_schema.md` | Manifest alanları ve anlamları |
| `02_general_system_prompt.md` | Genel kitap üretim sistemi promptu |
| `03_output_format_standard.md` | Markdown çıktı, tablo, kod ve kutu standartları |
| `04_chapter_structure_standard.md` | Bölüm içi pedagojik yapı |
| `05_chapter_input_generator_prompt.md` | Manifestten bölüm girdi promptu üretimi |
| `06_outline_review_prompt.md` | Outline kontrol ve karar standardı |
| `07_full_text_generation_prompt.md` | Onaylı outline'dan tam metin üretimi |
| `08_quality_gate_contract.md` | Kalite kapıları ve karar türleri |
| `09_manual_asset_override_policy.md` | Manuel görsel önceliği |
| `10_multilingual_generation_policy.md` | Çok dilli üretim politikası |
| `11_approval_gate_policy.md` | Onay kapıları |
| `12_project_starter_prompt.md` | Yeni kitap projesi başlatma |
| `13_post_production_pipeline_standard.md` | Post-production hattı |
| `14_docx_build_and_formatting_policy.md` | DOCX üretim ve biçimlendirme |
| `15_generated_package_protocol.md` | Paket üretim protokolü |
| `16_code_validation_and_test_policy.md` | Kod çıkarma, manifest doğrulama ve test hattı |
| `17_github_sync_and_qr_policy.md` | GitHub senkronizasyonu, QR ve code page standardı |
| `18_export_pipeline_policy.md` | HTML/EPUB/PDF/export akışı |
| `19_indexing_dashboard_policy.md` | Dashboard, indeksleme ve raporlama |
| `20_cloud_ide_codespaces_policy.md` | Dev Container ve GitHub Codespaces entegrasyonu |

---

## 3. `workspace/react/` klasörü

React kitabı üretimi için aktif çalışma alanı:

```
workspace/react/
├── chapters/
├── chapter_inputs/
├── build/
│   ├── code/
│   └── test_reports/
├── assets/
├── screenshots/
├── manifests/
└── dist/
```

**Önemli yollar:**

```
workspace/react/chapters/chapter_01_modern_web_giris.md
workspace/react/build/code_manifest.json
workspace/react/build/code_manifest.yaml
workspace/react/build/test_reports/code_test_report.json
workspace/react/build/test_reports/code_test_report.md
workspace/react/build/test_reports/chapter_01_markdown_quality_report.md
```

Bölüm dosyası adları küçük harfli, İngilizce slug veya açık ASCII karakterlerle tutulmalıdır:

```
chapter_02_javascript_temelleri.md
chapter_03_html_css_bilesen_dusuncesi.md
```

---

## 4. `docs/` klasörü

```
docs/
├── cli_usage.md
├── codespaces_integration.md
├── code_pages.md
├── code_validation.md
├── dashboard.md
├── export_pipeline.md
├── github_sync.md
├── indexing_glossary.md
├── llm_loading_order.md
├── postproduction_troubleshooting.md
├── project_starter_prompt_usage.md
├── quickstart.md
├── usage.md
└── windows_setup.md
```

Eski sürüm notları, geçici raporlar ve kısa süreli Markdown açıklamaları `docs/archive/` altına taşınabilir.

---

## 5. `tools/` klasörü

```
tools/
├── check_environment.py
├── check_package_integrity.py
├── validate_manifest.py
├── generate_chapter_inputs.py
├── code/
│   ├── extract_code_blocks.py
│   ├── validate_code_meta.py
│   ├── run_code_tests.py
│   ├── generate_llm_repair_prompt.py
│   └── run_code_tests_docker.py
├── quality/
│   └── check_chapter_markdown.py
└── postproduction/
    ├── post_production_pipeline.py
    ├── generate_qr_codes.py
    ├── resolve_assets.py
    ├── build_qr_manifest_from_code_manifest.py
    └── update_chapter_order.py
```

### Kod doğrulama zinciri

```
tools.code.extract_code_blocks   → CODE_META bloklarını bulur, kodları çıkarır
tools.code.validate_code_meta    → Metadata doğrulaması yapar
tools.code.run_code_tests        → Node.js veya ilgili runtime ile test eder
```

### Markdown kalite aracı

```
tools/quality/check_chapter_markdown.py
```

Bu araç şu sorunları yakalar: birden fazla H1, yanlış CODE_META yerleşimi, eksik screenshot marker, standart bölüm başlıklarından sapma, kapsam dışı konu uyarıları.

### Temizlik betikleri — güvenli yaklaşım

```
1. Önce rapor üret.
2. Dosyaları doğrudan silme.
3. Gerekirse docs/archive altına taşı.
4. Kalıcı silme için açık parametre kullan.
```

---

## 6. `assets/` klasörü ve görsel önceliği

```
assets/
├── auto/      ← Araçlar tarafından otomatik üretilen
├── manual/    ← İnsan editörün düzenlediği — KORUNUR
├── locked/    ← Onaylanmış, değiştirilmeyecek — KORUNUR
└── final/     ← Yayın çıktısına hazır
```

**Öncelik sırası:** `manual > locked > auto`

```
assets/manual/ ve assets/locked/ otomatik silinmez.
Otomatik üretilen görsel, manuel düzenlenmiş görselin üzerine yazmaz.
```
