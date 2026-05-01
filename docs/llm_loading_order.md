# LLM Loading Order

Bir LLM modeline framework dosyaları yüklenirken önerilen sıra aşağıdadır.

## Manifest oluşturmadan önce

1. `core/00_llm_execution_contract.md`
2. `core/01_book_manifest_schema.md`
3. `core/12_project_starter_prompt.md`

Bu aşamada LLM’den kullanıcı fikrini analiz etmesi, eksik alanları sorması ve manifest taslağı üretmesi istenir.

## Manifestten bölüm girdi promptu üretirken

1. `core/00_llm_execution_contract.md`
2. `core/01_book_manifest_schema.md`
3. `core/05_chapter_input_generator_prompt.md`
4. `manifests/<book_manifest>.yaml`

## Outline kontrolü için

1. `core/06_outline_review_prompt.md`
2. ilgili bölüm girdi dosyası
3. üretilmiş outline

## Tam metin üretimi için

1. `core/07_full_text_generation_prompt.md`
2. `core/03_output_format_standard.md`
3. `core/04_chapter_structure_standard.md`
4. ilgili bölüm girdi dosyası
5. onaylanmış outline
