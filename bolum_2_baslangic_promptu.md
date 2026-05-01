Aşağıdaki metni yeni sohbete doğrudan yapıştırabilirsiniz.

````markdown
# Devam Promptu — React Kitabı Bölüm 2 Girdi Promptu ve Tam Metin Üretimi

Bu sohbet, **BookFactory / Parametric Computer Book Factory** projesi kapsamında yürütülen **React ile Web Uygulama Geliştirme** kitabı çalışmasının devamıdır.

GitHub repo:

```text
https://github.com/bmdersleri/bookFactory
````

Branch:

```text
main
```

Son bilinen commit:

```text
c80c7d6 Remove chapter backup file from tracked sources
```

Proje klasörü yerelde şu şekildedir:

```text
C:\OneDrive\OneDrive - mehmetakif.edu.tr\BookFactory
```

Çalışma alanı:

```text
workspace/react/
```

Kitap adı:

```text
React ile Web Uygulama Geliştirme
```

Yazar:

```text
Prof. Dr. İsmail KIRBAŞ
```

Ana proje:

```text
KampüsHub
```

KampüsHub; üniversite öğrencileri için ders duyuruları, etkinlik takvimi, not paylaşımı ve kullanıcı profili modüllerini içeren kümülatif React web uygulamasıdır. Kitap boyunca her bölümde bu uygulama geliştirilecektir.

---

## 1. Mevcut durum

Bölüm 1 tamamlandı.

Bölüm 1 dosyası:

```text
workspace/react/chapters/chapter_01_modern_web_giris.md
```

Bölüm 1 başlığı:

```text
Bölüm 1: Modern Web’e Giriş ve Geliştirme Ortamı
```

Bölüm 1 için yapılanlar:

```text
CODE_META blokları çıkarıldı.
CODE_META validasyonu geçti.
Kod testleri geçti.
Markdown kalite kontrolünde FAIL: 0 seviyesine ulaşıldı.
Gereksiz chapter backup dosyası repodan çıkarıldı.
Repo GitHub’a temiz şekilde yüklendi.
```

Bölüm 1 test sonucu:

```text
Extracted CODE_META blocks: 3
CODE_META items checked: 3
CODE_META validation: OK
Total: 3 | Passed: 3 | Failed: 0 | Skipped: 0
```

Bölüm 1 kalite kontrol hedefi:

```text
FAIL: 0
```

Bu hedef sağlandı.

---

## 2. Bu sohbette yapılacak görev

Bu sohbette Bölüm 2’ye geçilecek.

Öncelikli görev sırası:

```text
1. Repodaki mevcut BookFactory yapısını ve React kitabı dosyalarını incele.
2. Manifest, core standartları ve Bölüm 1 yapısını dikkate al.
3. Bölüm 2 için ayrıntılı “bölüm girdi promptu” üret.
4. Bölüm 2 girdi promptunu Markdown dosyası olarak tasarla.
5. Ardından bu girdi promptuna dayanarak Bölüm 2 tam metnini üret.
6. Bölüm 2 tam metni Pandoc uyumlu, CODE_META uyumlu ve kalite kontrol dostu olsun.
```

Eğer GitHub reposuna doğrudan erişilemiyorsa kullanıcıdan şu dosyaları yüklemesi istenebilir:

```text
LLM_PROJECT_BRIEF.md
README.md
SETUP.md veya KULLANIM_KILAVUZU.md
core/03_output_format_standard.md
core/04_chapter_structure_standard.md
core/07_full_text_generation_prompt.md
workspace/react/chapters/chapter_01_modern_web_giris.md
tools/quality/check_chapter_markdown.py
manifests/ veya workspace/react içindeki React manifest/prompt dosyaları
```

Ancak repo okunabiliyorsa öncelikle repo esas alınmalıdır.

---

## 3. Bölüm 2 için önerilen konu

Manifest veya mevcut prompt dosyalarında farklı bir başlık varsa onu esas al.

Eğer Bölüm 2 başlığı açıkça tanımlı değilse şu öneriyi kullan:

```text
Bölüm 2: React Temelleri, JSX ve Bileşen Mantığı
```

Bölümün ana amacı:

```text
Öğrencinin React’in bileşen tabanlı düşünme biçimini kavraması, JSX sözdizimini öğrenmesi, ilk basit bileşenleri oluşturması ve KampüsHub uygulamasının ilk görsel iskeletini React bileşenleriyle kurması.
```

Bölüm 2 sonunda KampüsHub tarafında beklenen ilerleme:

```text
KampüsHub için temel App bileşeni,
Header bileşeni,
ana içerik alanı,
basit modül kartları
ve ilk statik arayüz iskeleti oluşturulmalıdır.
```

---

## 4. Bölüm 2 girdi promptunda mutlaka bulunacak alanlar

Bölüm 2 girdi promptu şu başlıkları içermelidir:

```text
Bölüm kimliği
Bölüm başlığı
Bölümün kitap içindeki yeri
Ön koşullar
Öğrenme çıktıları
Ana kavramlar
KampüsHub bağlantısı
Kullanılacak teknik kapsam
Kapsam dışı konular
Kod örneği politikası
CODE_META gereksinimleri
Screenshot planı
Pedagojik akış
Mini alıştırmalar
Laboratuvar görevi
Kalite kontrol ölçütleri
Tam metin üretim talimatı
```

---

## 5. Bölüm 2 teknik kapsamı

Bölüm 2’de işlenecek temel konular:

```text
React’in bileşen tabanlı yaklaşımı
JSX nedir?
JSX ile HTML arasındaki farklar
className kullanımı
JavaScript ifadelerinin JSX içinde kullanımı
Basit fonksiyon bileşeni
Bileşenleri iç içe kullanma
Props kavramına hazırlık düzeyi
KampüsHub arayüzünü bileşenlere ayırma
```

Bölüm 2’de ana akışa alınmayacak konular:

```text
useState
useEffect
React Router
Context API
Redux
Server Components
Next.js
GraphQL
React Native
Backend API entegrasyonu
Veritabanı bağlantısı
Kimlik doğrulama
```

Bu konular sadece “ilerleyen bölümlerde ele alınacak” bağlamında kısa şekilde anılabilir.

---

## 6. CODE_META kuralları

Kod örneklerinde `CODE_META` şu biçimde kullanılmalıdır:

```markdown
<!-- CODE_META
id: react_ch02_code01
chapter_id: chapter_02
language: javascript
kind: example
title: "..."
file: "..."
extract: true
test: node
expected_stdout: "..."
-->
```

CODE_META kesinlikle çalıştırılabilir kod bloğunun içine şu şekilde yazılmamalıdır:

```javascript
// CODE_META: ...
```

Her çalıştırılabilir kod örneği için metadata, kod bloğundan önce HTML yorum bloğu olarak verilmelidir.

Bölüm 2’de en az 3 CODE_META örneği bulunmalıdır.

Önerilen örnekler:

```text
react_ch02_code01
JSX ifade mantığını gösteren basit örnek.
Node ortamında test edilebilir.

react_ch02_code02
KampüsHub modül listesini JavaScript dizisiyle temsil eden örnek.
Node ortamında test edilebilir.

react_ch02_code03
Bileşen mantığını fonksiyon çıktısı üzerinden açıklayan sade test edilebilir örnek.
Node ortamında test edilebilir.
```

Not:

Gerçek React JSX dosyaları doğrudan Node ile test edilemiyorsa, test edilebilir örnekler saf JavaScript mantığıyla kurulmalı; React bileşen kodları ise `test: skip` veya uygun test türüyle işaretlenmelidir. Mevcut test hattının nasıl çalıştığı repodan kontrol edilmelidir.

---

## 7. Screenshot planı

Bölüm 2’de en az 2 screenshot marker bulunmalıdır.

Önerilen marker’lar:

```text
[SCREENSHOT:b02_01_jsx_ilk_bilesen]
[SCREENSHOT:b02_02_kampushub_bilesen_iskeleti]
[SCREENSHOT:b02_03_modul_kartlari]
```

Her screenshot için şu manifest mantığı gözetilmelidir:

```text
id
chapter
figure
title
route
waitFor
actions
output
caption
markdownTarget
```

Route yaklaşımı:

```text
/__book__/chapter-02/jsx-ilk-bilesen
/__book__/chapter-02/kampushub-bilesen-iskeleti
/__book__/chapter-02/modul-kartlari
```

---

## 8. Tam metin üretim kuralları

Bölüm 2 tam metni üretildiğinde dosya adı şu olmalıdır:

```text
workspace/react/chapters/chapter_02_react_temelleri_jsx_bilesenler.md
```

Tam metin şu yapıda olmalıdır:

```markdown
---
yaml front matter
---

# Bölüm 2: React Temelleri, JSX ve Bileşen Mantığı

## Bölüm yol haritası
## Öğrenme çıktıları
## Ön bilgiler
## React’te bileşen tabanlı düşünme
## JSX nedir?
## JSX ve HTML arasındaki farklar
## İlk bileşen mantığı
## KampüsHub arayüzünü bileşenlere ayırma
## Programatik ekran çıktısı planı
## CODE_META ve test edilebilir kod örnekleri
## Sık yapılan hatalar ve yanlış sezgiler
## Hata ayıklama egzersizi
## Bölüm özeti ve terim sözlüğü
## Kavramsal sorular
## Programlama alıştırmaları
## Haftalık laboratuvar / proje görevi
## İleri okuma ve bir sonraki bölüme köprü
```

Kalite kontrol açısından dikkat:

```text
Dosyada yalnızca bir H1 olmalıdır.
README taslağı veya kod içinde ikinci H1 oluşturulmamalıdır.
Kod bloğu içinde // CODE_META bulunmamalıdır.
Screenshot marker’ları korunmalıdır.
CODE_META id’leri benzersiz olmalıdır.
Markdown Pandoc uyumlu olmalıdır.
Başlık hiyerarşisi tutarlı olmalıdır.
```

---

## 9. Üslup ve pedagojik beklenti

Dil:

```text
Akademik ama sade Türkçe
```

Hedef kitle:

```text
React’e yeni başlayan bilgisayar / bilişim öğrencileri
```

Üslup:

```text
Ders kitabı dili
Adım adım öğretim
KampüsHub üzerinden kümülatif örnekleme
Gereksiz ileri konu yüklemesi yapmayan açıklama
```

Kod açıklamaları:

```text
Kodlar kısa, test edilebilir ve öğretici olmalıdır.
Değişken ve dosya adları İngilizce/camelCase veya PascalCase olmalıdır.
Açıklama metinleri Türkçe olabilir.
```

---

## 10. Bu sohbetin ilk çıktısı

Önce yalnızca Bölüm 2 girdi promptunu üret.

Çıktı dosyası önerisi:

```text
workspace/react/prompts/chapter_02_input_prompt.md
```

Girdi promptu tamamlandıktan sonra kısa bir kontrol özeti ver.

Ardından kullanıcının “devam” demesini beklemeden, eğer bağlam yeterliyse Bölüm 2 tam metnini üretmeye geç.

Tam metin çıktı dosyası önerisi:

```text
workspace/react/chapters/chapter_02_react_temelleri_jsx_bilesenler.md
```

Tam metinden sonra şu kontrol komutlarını ver:

```powershell
python -m tools.code.extract_code_blocks `
  --package-root . `
  --out-dir .\workspace\react\build\code `
  --manifest .\workspace\react\build\code_manifest.json `
  --yaml-manifest .\workspace\react\build\code_manifest.yaml `
  --chapters-dir .\workspace\react\chapters

python -m tools.code.validate_code_meta `
  .\workspace\react\build\code_manifest.json `
  --package-root .

python -m tools.code.run_code_tests `
  --manifest .\workspace\react\build\code_manifest.json `
  --package-root . `
  --report-json .\workspace\react\build\test_reports\code_test_report.json `
  --report-md .\workspace\react\build\test_reports\code_test_report.md `
  --node node `
  --fail-on-error

python -m tools.quality.check_chapter_markdown `
  --chapter .\workspace\react\chapters\chapter_02_react_temelleri_jsx_bilesenler.md `
  --chapter-id chapter_02 `
  --chapter-no 2 `
  --report .\workspace\react\build\test_reports\chapter_02_markdown_quality_report.md
```

Başarı ölçütü:

```text
CODE_META validation: OK
Kod testlerinde Failed: 0
Markdown kalite kontrolünde FAIL: 0
Bölüm dosyasında yalnızca bir H1
Screenshot marker’ları mevcut
```

```

Yeni sohbete bunu yapıştırdıktan sonra doğrudan Bölüm 2 girdi promptu üretimiyle başlayabilirsiniz.
```
