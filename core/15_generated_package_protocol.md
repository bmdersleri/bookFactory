# Generated Package Protocol — Üretilmiş Prompt Paketi Protokolü

Manifestten kitap özel prompt paketi üretildiğinde önerilen yapı:

```text
generated/{book_id}/
├── 00_usage_guide.md
├── 01_manifest_summary.md
├── 02_book_specific_system_prompt.md
├── 03_book_specific_output_format.md
├── 04_source_policy.md
├── 05_chapter_structure_standard.md
├── 06_outline_review_prompt.md
├── chapter_inputs/
├── manifests/
└── reports/
```

Çok dilli üretimde:

```text
generated/{book_id}/{language}/chapter_inputs/chapter_01_{chapter_id}_input.md
```
