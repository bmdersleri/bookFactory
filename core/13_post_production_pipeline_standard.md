# Post-Production Pipeline Standardı

Bu belge, **Parametric Computer Book Factory** kapsamında bölümler üretildikten sonra çalışan yayın sonrası hattını tanımlar. Amaç, bölüm Markdown dosyalarını tek kitap dosyasına dönüştürmek, Mermaid diyagramlarını PNG olarak üretmek, Pandoc ile DOCX oluşturmak ve DOCX üzerinde güvenli biçim düzeltmeleri yapmaktır.

## Temel ilke

Post-production katmanı, bölüm üretiminden bağımsızdır. Bölümler tamamlandıktan sonra `post_production_profile.yaml` dosyası okunur ve aşağıdaki işlemler kontrollü sırayla yürütülür.

```text
chapter markdown files
  ↓
merge chapters
  ↓
extract Mermaid blocks as .mmd
  ↓
render Mermaid PNG files once
  ↓
resolve final assets / manual overrides
  ↓
Pandoc DOCX build with reference DOCX and Lua filter
  ↓
DOCX safe formatting fix
  ↓
DOCX table width optimization
  ↓
post-production report
```

## Zorunlu kalite kuralları

1. Mermaid PNG üretimi yalnızca tek aşamada yapılmalıdır.
2. `prepare_mermaid_images.py` sadece `.mmd` dosyaları üretmelidir.
3. `render_mermaid_png.py` PNG üretiminin tek sorumlusu olmalıdır.
4. Pandoc dönüşümünde reference DOCX ve Lua filter manifest/profile üzerinden seçilmelidir.
5. DOCX üzerinde resim ortalama, pedagogik kutu hizalama ve tablo başlığı düzeltmeleri ayrı post-process adımı olarak yapılmalıdır.
6. Tablo genişliği optimizasyonu ayrı ve geri alınabilir adım olmalıdır.
7. `assets/manual/` ve `assets/locked/` klasörleri hiçbir post-production temizliğinde silinmemelidir.
8. Her aşama ayrı çalıştırılabilmeli ve rapor üretmelidir.

## Araçlar

| Araç | Görev |
|---|---|
| `merge_chapters.py` | Bölüm Markdown dosyalarını manifest sırasına göre birleştirir. |
| `prepare_mermaid_images.py` | Markdown içindeki Mermaid bloklarını `.mmd` dosyalarına çıkarır. |
| `render_mermaid_png.py` | `.mmd` dosyalarını PNG’ye dönüştürür. |
| `post_production_pipeline.py` | Tüm post-production hattını sırayla çalıştırır. |
| `fix_docx_format_ooxml.py` | DOCX içinde resim, H1, bölüm sonu, kutu ve tablo başlıklarını OOXML üzerinden düzeltir. |
| `optimize_docx_tables.py` | DOCX tablolarında sütun genişliklerini içerik uzunluğuna göre optimize eder. |

## Önerilen komut

```bash
python tools/postproduction/post_production_pipeline.py \
  --profile configs/post_production_profile_java_fundamentals.yaml \
  --stage all
```

## Aşama bazlı kullanım

```bash
python tools/postproduction/post_production_pipeline.py --profile configs/post_production_profile_java_fundamentals.yaml --stage validate
python tools/postproduction/post_production_pipeline.py --profile configs/post_production_profile_java_fundamentals.yaml --stage merge
python tools/postproduction/post_production_pipeline.py --profile configs/post_production_profile_java_fundamentals.yaml --stage prepare-mermaid
python tools/postproduction/post_production_pipeline.py --profile configs/post_production_profile_java_fundamentals.yaml --stage render-mermaid
python tools/postproduction/post_production_pipeline.py --profile configs/post_production_profile_java_fundamentals.yaml --stage pandoc
python tools/postproduction/post_production_pipeline.py --profile configs/post_production_profile_java_fundamentals.yaml --stage fix-docx
python tools/postproduction/post_production_pipeline.py --profile configs/post_production_profile_java_fundamentals.yaml --stage optimize-tables
```

## LLM için yorumlama kuralı

Bir LLM bu dosyayı okuduğunda post-production işlemlerinin tam metin üretimi değil, üretilmiş içeriklerin yayın çıktısına dönüştürülmesi olduğunu anlamalıdır. LLM, bu aşamada bölüm içeriği yazmamalı; yalnızca profil, araç, kalite kapısı ve çıktı standardını üretmeli veya denetlemelidir.
