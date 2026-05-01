# Post-Production Kullanım Örneği

Aşağıdaki komut, üretilmiş bölüm Markdown dosyalarını birleştirir, Mermaid diyagramlarını PNG’ye çevirir, Pandoc ile DOCX üretir ve DOCX üzerinde güvenli biçim düzeltmelerini yapar.

```bash
python tools/postproduction/post_production_pipeline.py \
  --profile configs/post_production_profile_java_fundamentals.yaml \
  --stage all
```

Sadece denetim için:

```bash
python tools/postproduction/post_production_pipeline.py \
  --profile configs/post_production_profile_java_fundamentals.yaml \
  --stage validate
```

Sadece DOCX biçim düzeltme için:

```bash
python tools/postproduction/post_production_pipeline.py \
  --profile configs/post_production_profile_java_fundamentals.yaml \
  --stage fix-docx
```
