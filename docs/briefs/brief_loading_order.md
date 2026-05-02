# BookFactory — Yükleme Sırası ve İş Akışı

**Modül:** `brief_loading_order.md`  
**Yükleme önceliği:** 5 — Üretim aşaması planlanırken yükle  
**İlgili modüller:** [`brief_core.md`](brief_core.md), [`brief_llm_rules.md`](brief_llm_rules.md)

---

## 1. LLM'e dosyalar hangi sırayla verilmeli?

### 1.1 Yeni kitap projesi başlatma

```
1. LLM_PROJECT_BRIEF.md          ← bu index
2. brief_core.md
3. brief_llm_rules.md
4. core/00_llm_execution_contract.md
5. core/01_book_manifest_schema.md
6. core/12_project_starter_prompt.md
7. Kullanıcının kitap fikri
```

### 1.2 Bölüm girdi promptu üretme

```
1. brief_core.md
2. brief_llm_rules.md
3. core/00_llm_execution_contract.md
4. core/01_book_manifest_schema.md
5. core/05_chapter_input_generator_prompt.md
6. book_manifest.yaml veya proje manifesti
```

### 1.3 Outline üretme

```
1. brief_core.md
2. brief_llm_rules.md
3. core/00_llm_execution_contract.md
4. core/02_general_system_prompt.md
5. core/03_output_format_standard.md
6. core/04_chapter_structure_standard.md
7. İlgili chapter_input.md
```

### 1.4 Outline kontrolü

```
1. core/06_outline_review_prompt.md
2. İlgili chapter_input.md
3. Üretilen outline
```

### 1.5 Tam metin üretimi

```
1. brief_core.md
2. brief_llm_rules.md
3. brief_standards.md
4. core/00_llm_execution_contract.md
5. core/02_general_system_prompt.md
6. core/03_output_format_standard.md
7. core/04_chapter_structure_standard.md
8. core/07_full_text_generation_prompt.md
9. İlgili chapter_input.md
10. Onaylanmış outline
```

### 1.6 React kitabı bölüm kalite kontrolü

```
1. brief_core.md
2. brief_llm_rules.md
3. brief_react_context.md
4. brief_standards.md
5. İlgili bölüm dosyası
6. code_test_report.md
7. markdown_quality_report.md
```

---

## 2. Onay kapıları

Onay kapıları manifest veya proje iş akışından yönetilir.

```yaml
approval_gates:
  manifest_validation:        "required"
  chapter_input_generation:   "optional"
  outline_review:             "required"
  full_text_generation:       "required"
  code_validation:            "required"
  markdown_quality_check:     "required"
  post_production_build:      "optional"
```

**LLM şu kurala uymalıdır:**

```
Bir aşamada kritik hata varsa sonraki aşamaya geçilmez.
FAIL: 0 hedeflenir.
WARN varsa bağlamına göre kritik olup olmadığı değerlendirilir.
```

---

## 3. Tam üretim akışı

```
Kitap fikri
   ↓
Project Starter Prompt → Netleştirme soruları
   ↓
Manifest / proje standardı (ONAY GEREKİR)
   ↓
Bölüm girdi promptları
   ↓
Outline üretimi
   ↓
Outline kontrolü (ONAY GEREKİR)
   ↓
Tam bölüm Markdown metni (ONAY GEREKİR)
   ↓
CODE_META ile kod çıkarma
   ↓
Kod doğrulama ve test (Failed: 0 hedefi)
   ↓
Markdown kalite kontrol (FAIL: 0 hedefi)
   ↓
Screenshot / Mermaid / asset / QR planı
   ↓
GitHub sync / code pages
   ↓
Post-production (DOCX / HTML / EPUB / PDF / ZIP)
   ↓
Release, dashboard, arşiv
```

---

## 4. Başlangıç komutu (yeni LLM oturumu)

```
Sen Parametric Computer Book Factory projesi için çalışan bir kitap üretim
ve kalite kontrol ajanısın.

Önce `brief_core.md`, ardından `brief_llm_rules.md` dosyasını oku.
Aktif kitap projesine özgü context brief dosyası varsa onu da yükle.
Bölüm üretimi yapacaksan `brief_standards.md` ve bu dosyayı (`brief_loading_order.md`) da oku.

Aktif kitap bağlamını `book_manifest.yaml` dosyasından belirle:
- book.title → kitap adı
- cumulative_app.name → kümülatif uygulama adı
- book_root → kullanıcının belirttiği kitap proje kökü

Eksik veya muallak bilgileri tahmin ederek doldurma.
Kritik kararlar için kullanıcıya kısa ve hedefli sorular sor.

Kritik hata varsa sonraki aşamaya geçme.
Hata raporlarını kök neden ve çözüm adımıyla birlikte açıkla.
```
