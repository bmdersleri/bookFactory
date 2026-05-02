# Quickstart — Parametric Computer Book Factory v3.4.0

Bu belge, framework’ün en kısa kullanım akışını özetler.

## 1. Ortamı hazırlayın

```bash
pip install -r requirements.txt
python tools/check_environment.py --soft
```

Harici araçlar:

- Pandoc
- Node.js
- Mermaid CLI: `npm install -g @mermaid-js/mermaid-cli`
- Java/JDK
- Git

## 2. Manifesti doğrulayın

```bash
python tools/validate_manifest.py manifests/java_fundamentals_manifest.yaml
```

## 3. Bölüm girdi promptlarını üretin

```bash
python tools/generate_chapter_inputs.py manifests/java_fundamentals_manifest.yaml --language tr
```

## 4. Bölümler üretildikten sonra post-production çalıştırın

```bash
python tools/postproduction/post_production_pipeline.py   --profile configs/post_production_profile_java_fundamentals.yaml   --stage all
```

## Minimal demo testi

Paketi kurduktan sonra, gerçek kitap bölümlerini üretmeden önce minimal demo akışını kontrol edebilirsiniz:

```bash
python tools/postproduction/post_production_pipeline.py \
  --profile examples/minimal_book/configs/post_production_profile_minimal.yaml \
  --stage all \
  --dry-run
```

Gerçek DOCX üretimi için Mermaid CLI (`mmdc`) kurulu olmalıdır.

## 5. Paket bütünlüğünü kontrol edin

```bash
python tools/check_package_integrity.py .
```


## QR code generation

v2.3.1 adds a manifest-driven QR generation stage.

Run only QR generation:

```bash
python tools/postproduction/post_production_pipeline.py ^
  --profile configs/post_production_profile_java_fundamentals.yaml ^
  --stage generate-qr
```

The QR stage reads `post_production.qr.manifest`. If `allow_missing_manifest: true`, the stage is skipped when the QR manifest has not been generated yet.

Example QR manifest:

```text
examples/qr/qr_manifest_example.yaml
```

QR matrix images should not be manually edited because this may break scan reliability. Use captions, labels or page layout for visual customization.

## v2.5.0 hızlı kod testi

Minimal demo kitabındaki `CODE_META` bloklarını çıkarmak ve Java kodlarını test etmek için:

```bash
python -m bookfactory test-minimal --fail-on-error
```

Bu komut şu çıktıları üretir:

- `examples/minimal_book/build/code_manifest.json`
- `examples/minimal_book/build/code_manifest.yaml`
- `examples/minimal_book/build/code/`
- `examples/minimal_book/build/test_reports/code_test_report.md`

Eğer bir kod başarısız olursa:

```bash
python -m bookfactory repair-prompts \
  --test-report examples/minimal_book/build/test_reports/code_test_report.json \
  --manifest examples/minimal_book/build/code_manifest.json \
  --out-dir examples/minimal_book/build/repair_prompts
```

## EPUB / HTML hızlı test

```bash
python -m bookfactory export \
  --profile examples/minimal_book/configs/post_production_profile_minimal.yaml \
  --format all \
  --merge-if-missing
```

Çıktılar `examples/minimal_book/dist/` altında oluşur.
