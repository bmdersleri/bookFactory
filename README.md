# Parametric Computer Book Factory v2.5.0

Bu paket, bilgisayar bilimleri ve yazılım mühendisliği alanındaki kitap üretimini manifest tabanlı, çok dilli ve LLM tarafından eksiksiz anlaşılabilir hâle getirmek için hazırlanmıştır.

Temel ilke:

> Kitap konusu, hedef kitle, bölüm mimarisi, teknik kapsam, kaynak politikası, içerik dili, çok dilli üretim tercihleri, kod/görsel/QR/GitHub politikaları ve onay kapıları `book_manifest.yaml` içinde tanımlanır. LLM, bu manifesti tek doğruluk kaynağı kabul ederek kitap özel prompt paketini ve bölüm girdi promptlarını üretir.

## Kararlar

- Framework adı: **Parametric Computer Book Factory**
- Teknik dosya ve klasör adları: İngilizce
- Açıklama belgeleri: Türkçe
- İçerik dili: Parametrik
- Çok dilli üretim: Türkçe, İngilizce, Almanca vb.
- Onay kapıları: Manifestten yönetilir
- Örnek manifest: `manifests/java_fundamentals_manifest.yaml`

## Minimum LLM başlangıç komutu

```text
Aşağıdaki dosyalar Parametric Computer Book Factory v2.5.0 çerçevesine aittir.
Önce `00_llm_execution_contract.md` dosyasını oku ve çalışma protokolünü öğren.
Ardından `book_manifest.yaml` dosyasını tek doğruluk kaynağı kabul et.
Manifesti doğrula. Eksik veya çelişkili alan varsa üretime geçmeden raporla.
Manifest uygunsa kitap özel prompt paketini ve bölüm girdi promptlarını manifestteki dil politikasına göre üret.
Tam bölüm metni üretme.
```

## Paket yapısı

```text
core/
  00_llm_execution_contract.md
  01_book_manifest_schema.md
  02_general_system_prompt.md
  03_output_format_standard.md
  04_chapter_structure_standard.md
  05_chapter_input_generator_prompt.md
  06_outline_review_prompt.md
  07_full_text_generation_prompt.md
  08_quality_gate_contract.md
  09_manual_asset_override_policy.md
  10_multilingual_generation_policy.md
  11_approval_gate_policy.md
  12_generated_package_protocol.md
manifests/
  java_fundamentals_manifest.yaml
templates/
  terminology_glossary_template.yaml
  translation_memory_template.yaml
examples/
  chapter_input_example.md
  meta_block_examples.md
```

## Post-production katmanı

v2.1 ile framework’e yayın sonrası üretim hattı eklenmiştir. Bu katman, bölümler üretildikten sonra şu işlemleri yönetir:

1. Bölüm Markdown dosyalarını manifest/profil sırasına göre birleştirme
2. Mermaid bloklarını `.mmd` dosyalarına çıkarma
3. Mermaid PNG görsellerini tek aşamada üretme
4. Pandoc ile reference DOCX ve Lua filter kullanarak DOCX oluşturma
5. DOCX içinde resimleri ortalama, pedagogik kutuları iki yana yaslama ve tablo başlıklarını düzeltme
6. DOCX tablo genişliklerini optimize etme

Temel kullanım:

```bash
python tools/postproduction/post_production_pipeline.py   --profile configs/post_production_profile_java_fundamentals.yaml   --stage all
```

Ayrıntılar için `core/13_post_production_pipeline_standard.md` ve `core/14_docx_build_and_formatting_policy.md` dosyalarına bakınız.


## v2.3 Stabilization Notes

Bu sürüm, v2.1 post-production paketinin stabilize edilmiş hâlidir.

Eklenenler:

- Proje başlatıcı prompt: `core/12_project_starter_prompt.md`
- Paket üretim protokolü: `core/15_generated_package_protocol.md`
- Manifest doğrulama: `tools/validate_manifest.py`
- Bölüm girdi üretimi: `tools/generate_chapter_inputs.py`
- Manuel görsel çözümleme: `tools/postproduction/resolve_assets.py`
- Ortam kontrolü: `tools/check_environment.py`
- Paket bütünlük kontrolü: `tools/check_package_integrity.py`
- Quickstart ve LLM yükleme sırası belgeleri
- Requirements ve release checklist dosyaları

Önerilen ilk kontrol:

```bash
python tools/check_package_integrity.py .
python tools/check_environment.py --soft
```


## QR code generation

Starting with v2.3.1, the post-production layer includes `tools/postproduction/generate_qr_codes.py` and the `generate-qr` pipeline stage. QR codes are generated from a YAML/JSON QR manifest and written as PNG files, typically under `assets/auto/qr`.

Example:

```bash
python tools/postproduction/generate_qr_codes.py --manifest examples/qr/qr_manifest_example.yaml --output-dir assets/auto/qr --report build/reports/qr_generation_report.md
```


## v2.5.0 Correction Package

Bu düzeltme paketi, v2.4-improved sürümünün paket bütünlüğü korunan bakım sürümüdür. Başlıca düzeltmeler:

- Minimal demo profilindeki `project_root` yolu düzeltildi.
- Pandoc/Lua/Mermaid entegrasyonu `MERMAID_IMAGE_DIR` ortam değişkeniyle sağlamlaştırıldı.
- Windows DOCX dönüşüm batch dosyası proje kökü temelli çalışacak şekilde güncellendi.
- Java manifesti 33 ana bölüm + 3 ek bölüm iskeletini içerecek biçimde genişletildi.
- Paket manifesti, checksum dosyası ve sürüm bilgileri v2.5.0 ile eşitlendi.


## v2.4 Additions

This package includes the following practical improvements:

- `examples/assets/asset_manifest_example.yaml`: manual asset override example.
- `examples/code/code_manifest_example.yaml`: code manifest example for QR generation.
- `tools/postproduction/build_qr_manifest_from_code_manifest.py`: builds a QR manifest from a code manifest.
- `tools/postproduction/update_chapter_order.py`: updates post-production profile chapter list by scanning a chapters directory.
- `examples/numbering/numbering_test.md`: build-time numbering test document.
- `examples/minimal_book/`: minimal demo book for end-to-end workflow testing.

## v2.5.0 Code Validation + CLI Foundation

v2.5.0 ile BookFactory, bağımsız post-production araçlarına ek olarak tek noktadan yönetilebilen bir CLI ve `CODE_META` tabanlı kod doğrulama hattı kazanmıştır.

Yeni temel komutlar:

```bash
python -m bookfactory version
python -m bookfactory doctor --soft
python -m bookfactory test-minimal --fail-on-error
python -m bookfactory test-code --chapters-dir examples/minimal_book/chapters --fail-on-error
python -m bookfactory repair-prompts
```

Eklenen ana dosyalar:

- `bookfactory/cli.py`
- `bookfactory_cli.py`
- `tools/code/extract_code_blocks.py`
- `tools/code/validate_code_meta.py`
- `tools/code/run_code_tests.py`
- `tools/code/generate_llm_repair_prompt.py`
- `tools/code/run_code_tests_docker.py`
- `core/16_code_validation_and_test_policy.md`
- `docs/code_validation.md`
- `docs/cli_usage.md`
- `schemas/code_meta_schema.json`

Önerilen release öncesi kalite kapısı:

```bash
python -m bookfactory test-code --chapters-dir generated/java_fundamentals/tr/chapters --fail-on-error
```

## v2.6.0 — GitHub Sync ve QR Hardening

v2.6.0 ile testten geçen `CODE_META` kodları GitHub'a hazır bir klasör yapısına aktarılabilir ve GitHub Pages açıklama sayfaları üretilebilir.

Önerilen sıra:

```bash
python -m bookfactory test-code --chapters-dir examples/minimal_book/chapters --fail-on-error
python -m bookfactory sync-github --code-manifest build/code_manifest.json --test-report build/test_reports/code_test_report.json --require-tests-passed
python -m bookfactory qr-from-code --code-manifest build/code_manifest_github.json --fail-on-empty --strict-url
```

Gerçek `git push` varsayılan değildir; güvenlik için kullanıcı açıkça `--push` vermelidir.

## v2.7.0 Export Pipeline

v2.7.0 ile BookFactory, DOCX/PDF üretimine ek olarak EPUB, tek sayfa HTML ve bölüm bazlı statik HTML site çıktıları üretebilir.

Temel komut:

```bash
python -m bookfactory export \
  --profile examples/minimal_book/configs/post_production_profile_minimal.yaml \
  --format all \
  --merge-if-missing
```

Ayrıntılar için `docs/export_pipeline.md` ve `core/18_export_pipeline_policy.md` dosyalarına bakınız.


## v2.8.0 Glossary / Index / Dashboard

`python -m bookfactory build-index --profile examples/minimal_book/configs/post_production_profile_minimal.yaml` komutu ile terim sözlüğü ve arka dizin üretilebilir. `python -m bookfactory dashboard --check` komutu opsiyonel Streamlit dashboard bağımlılığını kontrol eder.

## GitHub Codespaces desteği

BookFactory v2.9.0 ile proje GitHub Codespaces üzerinde doğrudan açılabilecek şekilde hazırlanmıştır. Varsayılan yapılandırma `.devcontainer/` klasöründedir.

**v2.9.1 hotfix:** Mermaid CLI için Puppeteer/Chrome kurulumu, project-level `configs/puppeteer_config.json` üretimi, `doctor --soft` sürüm kontrolü ve Codespaces template senkronizasyonu güçlendirilmiştir.

```bash
python -m bookfactory codespaces-check
python -m bookfactory doctor --soft
python -m bookfactory test-minimal --fail-on-error
```

Yeni veya harici bir BookFactory projesine Codespaces dosyalarını eklemek için:

```bash
python -m bookfactory codespaces-init
```

Ayrıntılar için `docs/codespaces_integration.md` dosyasına bakınız.
