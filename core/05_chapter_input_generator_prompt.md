# Chapter Input Generator Prompt — Bölüm Girdi Promptu Üretici

## Görev

Sana verilen manifesti okuyarak her bölüm için ayrı bir Markdown bölüm-girdi promptu üret.

## İşlem

1. Manifesti oku.
2. Zorunlu alanları kontrol et.
3. Eksik veya çelişkili alan varsa raporla ve üretimi durdur.
4. `language.generation_mode` değerini belirle.
5. Her hedef dil için bölüm-girdi promptlarını üret.
6. `chapter_id` değerlerini koru.
7. Kod, diyagram, screenshot ve asset planlarını manifestten türet.
8. Onay kapısı politikasını bölüm girdisine ekle.
9. Tam bölüm metni üretme.

## Çıktı klasörü

```text
generated/{book_id}/{language}/chapter_inputs/chapter_{order}_{chapter_id}_input.md
```

## Bölüm-girdi dosyası şablonu

```markdown
# CHAPTER INPUT — {chapter_title}

## 1. Manifest identity

**Book ID:** {book_id}  
**Chapter ID:** {chapter_id}  
**Content language:** {target_language}  
**Part:** {part}  
**Chapter type:** {chapter_type}  
**Numbering policy:** build_time  

## 2. Chapter purpose

{purpose}

## 3. Target audience and prerequisites

{audience_and_prerequisites}

## 4. Learning outcomes

{learning_outcomes}

## 5. Mandatory concepts

{mandatory_concepts}

## 6. Required code/application assets

{required_code_examples}

## 7. Required diagram/screenshot/visual assets

{required_visuals}

## 8. Approval gates

{approval_gate_summary}

## 9. Outline generation instruction

Generate only a detailed outline for this chapter. Do not generate the full chapter text.
```
