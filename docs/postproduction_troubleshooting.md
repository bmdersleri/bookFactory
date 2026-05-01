# Post-production Troubleshooting

## Pandoc reference DOCX bulunamıyor

`configs/post_production_profile_*.yaml` içinde `project_root` alanını kontrol edin.

Önerilen yapı:

```yaml
project_root: ".."
```

## Mermaid PNG üretilmiyor

`mmdc` PATH içinde mi?

```bash
mmdc --version
```

## Manuel görsel kullanılmıyor

Manuel görselin göreli yolu otomatik görselle aynı olmalıdır.

Örnek:

```text
assets/auto/diagrams/decision_structures_diagram01.png
assets/manual/diagrams/decision_structures_diagram01.png
```

`resolve_assets.py` bu durumda manuel görseli seçer.

## Tablo genişlikleri bozuk

Önce güvenli biçim düzeltme, sonra tablo optimizasyonu çalıştırılmalıdır:

```bash
--stage fix-docx
--stage optimize-tables
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
