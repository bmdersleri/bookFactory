# Book Manifest Schema — Kitap Manifest Şeması

Bu belge, `book_manifest.yaml` dosyasının alanlarını ve anlamlarını tanımlar.

## Zorunlu üst seviye alanlar

```yaml
book:
language:
audience:
pedagogy:
technical_profile:
content_scope:
sources:
capabilities:
automation:
approval_gates:
chapters:
```

## `book`

```yaml
book:
  book_id: "java_fundamentals"
  title:
    tr: "Java'nın Temelleri"
    en: "Java Fundamentals"
    de: "Grundlagen von Java"
  subtitle:
    tr: "..."
    en: "..."
    de: "..."
  author: "Author Name"
  year: "2026"
  version: "1.0"
  book_type: "applied_textbook"
  domain: "programming"
  primary_technology: "Java"
```

`book_id` İngilizce, küçük harfli, boşluksuz ve slug uyumlu olmalıdır.

## `language`

```yaml
language:
  primary_language: "tr"
  output_languages: ["tr", "en", "de"]
  generation_mode: "parallel"
  file_naming_language: "en"
  manifest_language: "en"
  automation_language: "en"
  content_language_policy:
    headings: "target_language"
    body_text: "target_language"
    exercises: "target_language"
    glossary: "target_language_with_english_terms"
    code_comments: "target_language"
    code_identifiers: "en"
    console_outputs: "target_language"
  terminology:
    use_controlled_glossary: true
    glossary_file: "terminology_glossary.yaml"
    first_use_policy: "target_term_with_english_in_parentheses"
  fallback:
    fallback_language: "tr"
    missing_translation_policy: "report_missing_do_not_invent"
```

`generation_mode` değerleri: `single`, `parallel`, `bilingual`, `multilingual_inline`.

## `approval_gates`

Onay kapıları parametriktir.

```yaml
approval_gates:
  manifest_validation:
    required: true
    actor: "human_or_llm"
    stop_on_failure: true
  outline_review:
    required: true
    actor: "human_or_llm"
    allowed_decisions: ["PASS", "REVISION_REQUIRED", "BLOCKED"]
  full_text_generation:
    required: true
    actor: "human"
    requires_previous_gate: "outline_review:PASS"
```

## `chapters`

`chapter_id` kalıcıdır ve dil değişse bile değişmez.

```yaml
chapters:
  - chapter_id: "decision_structures"
    title:
      tr: "Karar Yapıları"
      en: "Decision Structures"
      de: "Entscheidungsstrukturen"
    chapter_type: "core_topic"
    purpose:
      tr: "Koşullara göre program akışını yönlendirmeyi öğretmek."
      en: "To teach how to control program flow based on conditions."
      de: "Zu vermitteln, wie der Programmablauf anhand von Bedingungen gesteuert wird."
```
