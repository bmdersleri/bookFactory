# Chapter Input Generator Prompt — Bölüm Girdi Promptu Üretici

## Görev

Verilen `book_manifest.yaml` dosyasını okuyarak her bölüm için ayrı bir Markdown bölüm-girdi promptu üret.
Bu promptlar, bir sonraki aşamada LLM'in tam bölüm metnini oluşturmasında tek giriş kaynağı olacaktır.

---

## İşlem sırası

1. Manifesti oku; `book`, `language`, `cumulative_app`, `scope`, `structure.chapters` alanlarını çıkar.
2. Zorunlu alanları kontrol et: `book.title`, `book.author`, `language.primary_language`, `structure.chapters` listesi.
3. Eksik veya çelişkili alan varsa üretimi durdur ve hangi alanın eksik olduğunu raporla.
4. `language.primary_language` değerini belirle; içerik bu dilde üretilecektir.
5. `structure.chapters` listesindeki her bölüm için ayrı bir girdi dosyası üret.
6. `chapter_id` değerlerini değiştirme; manifest ile bire bir eşleşmeli.
7. `cumulative_app` bilgisini her bölüm girdisine taşı; hangi kümülatif katkının bu bölümde yapılacağını belirt.
8. `scope.stack` (kapsam içi) ve `scope.out_of_scope` (kapsam dışı) listelerini her bölüm girdisine ekle.
9. Her bölüm için `approval_gates` özetini ekle.
10. Tam bölüm metni **üretme**; yalnızca girdi promptunu üret.

---

## Çıktı konumu

Dosyalar kitap proje kökünde şu yola yazılır:

```text
{book_root}/prompts/chapter_inputs/chapter_{nn}_input.md
```

Örnek: `C:\...\react-web\prompts\chapter_inputs\chapter_03_input.md`

---

## Bölüm-girdi dosyası şablonu

```markdown
# BÖLÜM GİRDİ PROMPTU — {chapter_title}

## 1. Kitap ve bölüm kimliği

| Alan | Değer |
|---|---|
| Kitap adı | {book.title} |
| Yazar | {book.author} |
| Bölüm ID | {chapter_id} |
| Bölüm başlığı | {chapter_title} |
| İçerik dili | {language.primary_language} |
| Bölüm dosyası | `{chapter_file}` |
| Bölüm durumu | {chapter_status} |
| Numaralandırma politikası | build_time (başlıklara elle numara yazma) |

## 2. Kitap boyunca geliştirilen uygulama

- **Uygulama adı:** {cumulative_app.name}
- **Açıklama:** {cumulative_app.description}
- **Bu bölümün katkısı:** {chapter.cumulative_app_increment veya chapter.summary}

## 3. Teknoloji kapsamı

### Kapsam içi teknolojiler

{scope.stack — madde madde}

### Kapsam dışı konular

{scope.out_of_scope — madde madde}

## 4. Öğrenme çıktıları

{chapter.learning_outcomes — varsa manifestten, yoksa bölüm başlığından türet}

## 5. Temel kavramlar

{chapter.key_concepts — varsa manifestten}

## 6. Beklenen bölüm yapısı (Bloom Taksonomisi Uyumlu)

Bölüm aşağıdaki eğitsel akışı (pedagogical flow) izlemelidir:

1. **Hatırlama ve Giriş:** Bölümün amacı, öğrenme çıktıları ve önceki bölümlerle bağlantı.
2. **Kavrama (Teorik Temel):** Temel kavramlar, tanımlar ve "neden" sorularına cevaplar.
3. **Uygulama (Pratik Uygulama):** 
    - Kavramları açıklayan kısa, çalıştırılabilir kod örnekleri.
    - {cumulative_app.name} uygulamasına bu bölümün katkısı.
    - Adım adım uygulama geliştirme süreci.
4. **Analiz ve Derinleşme:** 
    - Kodun nasıl çalıştığının analizi.
    - Mermaid diyagramları ile mimari görselleştirme.
    - Sık yapılan hatalar ve çözümleri.
5. **Sentez ve Değerlendirme:**
    - Mini uygulama görevi veya alıştırmalar.
    - Bölüm sonu kontrol listesi.
    - Özet.

## 7. Kod üretim kuralları

### CODE_META standardı

Her çalıştırılabilir kod bloğunun **hemen önüne** şu biçimde `CODE_META` yazılmalıdır:

````html
<!-- CODE_META
id: {chapter_id}_code_01
chapter_id: {chapter_id}
language: javascript
file: src/example.js
test: syntax
-->
````

Ardından uygun dil etiketiyle kod bloğu verilir:

````javascript
// kod içeriği
````

**Kurallar:**
- `CODE_META` HTML yorum bloğu olarak kod bloğunun ÖNÜNDE yer alır; içine **yazmaz**.
- `id` değeri bölüm ve sıra ile benzersiz olmalıdır: `{chapter_id}_code_01`, `{chapter_id}_code_02`, …
- `language` alanı çalışma ortamıyla (Node.js, Python, JVM) eşleşmeli.
- Kod bloğu tablo, blockquote veya liste içine gömülmemeli.
- `test: syntax` → sözdizimi kontrolü; `test: run` → çalıştırılabilir.

## 8. Görsel ve screenshot kuralları

- Mermaid diyagramları geçerli sözdizimiyle, `mermaid` etiketiyle yazılmalı.
- Screenshot gerekiyorsa: `[SCREENSHOT:{chapter_id}_01_aciklayici_ad]`
- Görsel başlıklar akademik kitap üslubuyla verilmeli.
- Screenshot planı manifestteki `screenshot_plan` alanından alınmalı.

## 9. Onay kapıları özeti

```yaml
approval_gates:
  outline_review: {approval_gates.outline_review}
  full_text_generation: {approval_gates.full_text_generation}
  code_validation: {approval_gates.code_validation}
  markdown_quality_check: {approval_gates.markdown_quality_check}
```

**LLM bu bölüm için şunu üretecek:** önce ayrıntılı outline, onay sonrası tam metin.

## 10. Üslup ve dil

- **İçerik dili:** {language.primary_language}
- **Üslup Profili:** {language.style_profile} (Bu profile sıkı sıkıya uyun)
- **Eğitsel Model:** {language.pedagogical_model}
- **Ton:** akıcı, öğretici, uygulamalı, akademik doğruluğa sahip
- **Başlıklar:** manuel numara içerme; numaralandırma build aşamasında yapılacak
- **Dosya/kimlik adları:** küçük harfli, ASCII, boşluk ve Türkçe karakter içermez
- **Kapsam dışı konular** ana öğretim akışına sızmamalı
```

---

## Zorunlu alanlar ve hata durumları

| Alan | Zorunlu | Hata Davranışı |
|---|---|---|
| `book.title` | Evet | Üretimi durdur |
| `book.author` | Evet | Üretimi durdur |
| `language.primary_language` | Evet | Üretimi durdur |
| `structure.chapters` (liste) | Evet | Üretimi durdur |
| `cumulative_app.name` | Hayır | Şablon değerini "kümülatif uygulama" olarak bırak |
| `scope.stack` | Hayır | "Manifestte belirtilmemiş" yaz |
| `scope.out_of_scope` | Hayır | "Manifestte belirtilmemiş" yaz |
| `chapter.learning_outcomes` | Hayır | Bölüm başlığından türet |

---

## Yasak davranışlar

1. Tam bölüm metni **yazma** — yalnızca girdi promptu üretilir.
2. Bölüm outline'ı şu aşamada **üretme**.
3. `chapter_id` değerlerini **değiştirme**.
4. Kapsam dışı teknolojileri bölüm girdisine **ekleme**.
5. Dosya adlarında boşluk, Türkçe karakter veya özel karakter **kullanma**.
6. `CODE_META`'yı kod bloğunun içine `//` yorum olarak **yazma**.
7. Manifestte olmayan kaynak veya API **uydurma**.
