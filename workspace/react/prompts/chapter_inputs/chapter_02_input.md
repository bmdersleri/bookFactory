---
title: "Bölüm 2 Girdi Promptu: JavaScript ES6+ — React için Zorunlu Kavramlar"
book_title: "React ile Web Uygulama Geliştirme"
author: "Prof. Dr. İsmail KIRBAŞ"
chapter_id: "chapter_02"
chapter_no: 2
language: tr-TR
automation_profile: "parametric_computer_book_factory_v2"
---

# Bölüm 2 Girdi Promptu: JavaScript ES6+ — React için Zorunlu Kavramlar

## Bölüm kimliği

- **Kitap:** React ile Web Uygulama Geliştirme
- **Ana proje:** KampüsHub
- **Bölüm ID:** `chapter_02`
- **Bölüm No:** 2
- **Bölüm dosyası:** `workspace/react/chapters/chapter_02_javascript_es6_react.md`
- **Manifest başlığı:** Bölüm 2: JavaScript ES6+ — React için Zorunlu Kavramlar
- **Önerilen içerik dili:** Akademik ama sade Türkçe
- **Hedef okur:** HTML ve CSS bilen, React’e yeni başlayan bilgisayar/bilişim öğrencileri

## Bölüm başlığı

```text
Bölüm 2: JavaScript ES6+ — React için Zorunlu Kavramlar
```

## Bölümün kitap içindeki yeri

Bu bölüm, Bölüm 1’de kurulan modern web, SPA, React, Node.js, npm, Vite ve KampüsHub geliştirme ortamını dil temeliyle güçlendirir. React bileşenleri, JSX, props, state ve hooks konularına geçmeden önce öğrencinin modern JavaScript sözdizimini kavraması hedeflenir.

Bu bölümde amaç genel amaçlı ve kapsamlı bir JavaScript kitabı yazmak değildir. Amaç, React kodlarını okuyup yazmak için zorunlu olan ES6+ kavramlarını KampüsHub örnekleri üzerinden öğretmektir.

## Ön koşullar

Öğrencinin şu becerilere sahip olduğu varsayılır:

1. HTML ve CSS ile temel sayfa yapısı oluşturabilme.
2. Bölüm 1’deki Vite tabanlı React projesini başlatabilme.
3. Terminalde `node --version`, `npm --version`, `npm run dev` gibi komutları çalıştırabilme.
4. Basit JavaScript değişken, koşul ve döngü kavramlarını genel düzeyde tanıma.

## Öğrenme çıktıları

Bölüm sonunda öğrenci:

1. `let`, `const` ve değişmez referans kavramını React bağlamında açıklayabilir.
2. Template literal kullanarak okunabilir arayüz metinleri oluşturabilir.
3. Arrow function sözdizimini temel fonksiyon tanımlarıyla karşılaştırabilir.
4. Object ve array literal yapılarını KampüsHub veri modeli için kullanabilir.
5. Destructuring ile nesne ve dizi içinden değer çekebilir.
6. Spread/rest sözdizimiyle veriyi mutasyona uğratmadan yeni kopyalar oluşturabilir.
7. `map`, `filter`, `find`, `some`, `reduce` gibi dizi metotlarını React listeleri için hazırlık düzeyinde kullanabilir.
8. Modül sisteminde `export` ve `import` mantığını kavramsal olarak açıklayabilir.
9. `Promise`, `async` ve `await` kavramlarını API entegrasyonuna hazırlık düzeyinde yorumlayabilir.
10. KampüsHub’ın duyuru, etkinlik, not ve profil verilerini sade JavaScript veri yapılarıyla temsil edebilir.
11. BookFactory hattına uygun `CODE_META` bloklarıyla test edilebilir JavaScript örnekleri üretebilir.
12. Programatik ekran çıktısı marker’larını bölüm içinde doğru şekilde konumlandırabilir.

## Ana kavramlar

Bu bölümde ele alınacak ana kavramlar:

- ES6+ sözdizimi
- `let` ve `const`
- Template literal
- Arrow function
- Object literal
- Array literal
- Destructuring
- Spread/rest
- Immutability / veriyi mutasyona uğratmadan güncelleme
- Dizi metotları: `map`, `filter`, `find`, `some`, `reduce`
- Optional chaining ve nullish coalescing
- Modül sistemi
- Promise, async/await
- React’e hazırlık için veri dönüştürme mantığı

## KampüsHub bağlantısı

Bölüm boyunca KampüsHub projesi için şu veri parçaları hazırlanmalıdır:

1. Duyuru listesi
2. Etkinlik listesi
3. Not paylaşımı modül bilgisi
4. Kullanıcı profil özeti
5. Ana sayfada gösterilecek modül kartları

Bu veriler henüz gerçek back-end’den gelmeyecektir. Bölüm 2’de veriler düz JavaScript dizileri ve nesneleri olarak modellenir. Bu yaklaşım Bölüm 4’te JSX çıktısına, Bölüm 5’te props veri akışına ve Bölüm 13’te API entegrasyonuna temel oluşturacaktır.

## Kullanılacak teknik kapsam

Bölümde işlenecek teknik kapsam:

- Modern JavaScript değişken tanımlama yaklaşımı
- Fonksiyon tanımlama biçimleri
- Veri koleksiyonlarıyla çalışma
- React’te sık karşılaşılan veri dönüştürme kalıpları
- Mutasyon yerine kopya üretme disiplini
- Modüler dosya düşüncesi
- Asenkron veri alma fikrine giriş
- Node ile test edilebilir saf JavaScript örnekleri

## Kapsam dışı konular

Bu bölümde ana akışa alınmayacak konular:

- JSX ayrıntıları
- React bileşen anatomisi
- Props ile bileşenler arası veri aktarımı
- State yönetimi
- Hooks
- Router
- Form yönetimi
- Global state kütüphaneleri
- Gerçek back-end API entegrasyonu
- Veritabanı bağlantısı
- Kimlik doğrulama
- Üretim dağıtımı

Bu konular yalnızca sonraki bölümlere köprü kurmak amacıyla kısa şekilde anılabilir.

## Kod örneği politikası

Kodlar kısa, bağımsız ve test edilebilir olmalıdır. Ana örnekler Node.js ile çalıştırılabilir saf JavaScript olarak tasarlanmalıdır. React bileşenlerine hazırlık yapılabilir; ancak JSX ana öğretim konusu yapılmamalıdır.

Kodlarda şu kurallar izlenmelidir:

1. Değişken ve fonksiyon adları İngilizce ve camelCase olmalıdır.
2. Sınıf tabanlı bileşen yaklaşımına girilmemelidir.
3. React’e ait ileri API’ler kullanılmamalıdır.
4. Örnekler KampüsHub bağlamına bağlanmalıdır.
5. Çalıştırılabilir örneklerde beklenen çıktı açıkça tanımlanmalıdır.
6. Test hattı için `compile_run_assert` kullanılmalıdır.

## CODE_META gereksinimleri

Her çalıştırılabilir kod örneğinden önce HTML yorum bloğu biçiminde `CODE_META` bulunmalıdır.

Örnek şablon:

```markdown
<!-- CODE_META
id: react_ch02_code01
chapter_id: chapter_02
language: javascript
kind: example
title_key: js_template_literal_kampushub
file: kampushub_template_literal.js
extract: true
test: compile_run_assert
expected_stdout_contains: "KampüsHub"
timeout_sec: 10
-->
```

Bölümde en az 5 test edilebilir örnek önerilir:

1. `react_ch02_code01` — Template literal ve temel fonksiyon çıktısı.
2. `react_ch02_code02` — Object destructuring ve profil özeti.
3. `react_ch02_code03` — `map`, `filter` ve modül kartları.
4. `react_ch02_code04` — Spread ile mutasyonsuz duyuru güncelleme.
5. `react_ch02_code05` — Promise ve `async/await` ile sahte duyuru yükleme.

## Screenshot planı

Bölüm 2’de en az iki programatik ekran çıktısı marker’ı bulunmalıdır. Görsel yoğunluk orta düzeyde olduğu için 2–3 marker yeterlidir.

Önerilen marker’lar:

```text
[SCREENSHOT:b02_01_es6_console_ciktisi]
[SCREENSHOT:b02_02_kampushub_veri_modeli]
[SCREENSHOT:b02_03_modul_kartlari_onizleme]
```

Önerilen screenshot manifest alanları:

| id | chapter | figure | title | route | waitFor | output | markdownTarget |
|---|---|---|---|---|---|---|---|
| `b02_01_es6_console_ciktisi` | `chapter_02` | Şekil 2.1 | ES6 örneklerinin konsol çıktısı | `/__book__/chapter_02/es6-console` | `[data-book-shot='es6-console']` | `workspace/react/assets/screenshots/b02_01_es6_console_ciktisi.png` | `[SCREENSHOT:b02_01_es6_console_ciktisi]` |
| `b02_02_kampushub_veri_modeli` | `chapter_02` | Şekil 2.2 | KampüsHub veri modelinin görsel özeti | `/__book__/chapter_02/data-model` | `[data-book-shot='data-model']` | `workspace/react/assets/screenshots/b02_02_kampushub_veri_modeli.png` | `[SCREENSHOT:b02_02_kampushub_veri_modeli]` |
| `b02_03_modul_kartlari_onizleme` | `chapter_02` | Şekil 2.3 | Modül kartlarının statik önizlemesi | `/__book__/chapter_02/module-cards` | `[data-book-shot='module-cards']` | `workspace/react/assets/screenshots/b02_03_modul_kartlari_onizleme.png` | `[SCREENSHOT:b02_03_modul_kartlari_onizleme]` |

## Pedagojik akış

Bölüm şu sırayla ilerlemelidir:

1. Bölümün yol haritası ve React öğrenimindeki yeri.
2. ES6+ kavramlarının neden React için gerekli olduğunun açıklanması.
3. `let`, `const`, template literal ve arrow function.
4. Nesne ve dizi modelleme.
5. Destructuring ve spread/rest.
6. Dizi metotlarıyla veri dönüştürme.
7. Mutasyonsuz güncelleme mantığı.
8. Modül sistemi.
9. Asenkron JavaScript’e hazırlık.
10. KampüsHub veri modeli mini uygulaması.
11. Programatik ekran çıktısı planı.
12. Sık yapılan hatalar, hata ayıklama, özet, sözlük ve laboratuvar görevi.

## Mini alıştırmalar

Bölüm içinde kısa alıştırmalar verilmelidir:

1. Duyuru nesnesinden ders adı ve başlığı destructuring ile çekme.
2. Etkinlik listesinde yalnızca bu haftaki etkinlikleri filtreleme.
3. Modül kartlarına `isActive` alanı ekleme.
4. Profil nesnesini mutasyona uğratmadan güncelleme.
5. Sahte API fonksiyonunun döndürdüğü duyuruları okunabilir metne dönüştürme.

## Laboratuvar görevi

Öğrenci, KampüsHub için `src/data` klasörü altında şu dosyaları tasarlayacak şekilde yönlendirilmelidir:

```text
src/data/announcements.js
src/data/events.js
src/data/modules.js
src/data/profile.js
```

Bu dosyalar henüz gerçek React bileşenleri içinde kullanılmayabilir. Amaç, ilerleyen bölümlerde JSX ve props ile kullanılacak temiz veri yapısını hazırlamaktır.

## Kalite kontrol ölçütleri

Bölüm tam metni şu ölçütleri sağlamalıdır:

- Dosya YAML front matter ile başlamalıdır.
- Dosyada yalnızca bir H1 bulunmalıdır.
- H1 `Bölüm 2:` ile başlamalıdır.
- Ana bölüm başlıkları `2.1`, `2.2`, ... düzeninde verilmelidir.
- En az 5 `CODE_META` bloğu bulunmalıdır.
- `CODE_META` bloklarında `id`, `chapter_id`, `language`, `file`, `extract`, `test` alanları bulunmalıdır.
- Kod meta bilgisi kod bloğu içinde satır yorumu olarak verilmemelidir.
- En az 2 screenshot marker bulunmalıdır.
- Marker adları `b02_YY_aciklayici_ad` biçimini izlemelidir.
- Kod blokları kapalı olmalıdır.
- Türkçe karakterler UTF-8 uyumlu olmalıdır.
- Pandoc/DOCX dönüşümünde sorun çıkarabilecek ham HTML, gereksiz H1 ve bozuk fence kullanılmamalıdır.
- Bölüm sonunda özet, terim sözlüğü, kavramsal sorular, programlama alıştırmaları, haftalık laboratuvar ve bir sonraki bölüme geçiş bulunmalıdır.

## Tam metin üretim talimatı

Bu girdi promptuna göre tam metin üretirken şu dosya oluşturulmalıdır:

```text
workspace/react/chapters/chapter_02_javascript_es6_react.md
```

Tam metin, ders kitabı diliyle yazılmalı; gereksiz ileri konulara girmeden modern JavaScript kavramlarını React hazırlığı olarak açıklamalıdır. Kodlar çalıştırılabilir, kısa ve KampüsHub bağlamlı olmalıdır.

Bölüm sonunda aşağıdaki doğrulama komutları verilebilir:

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
  --chapter .\workspace\react\chapters\chapter_02_javascript_es6_react.md `
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
