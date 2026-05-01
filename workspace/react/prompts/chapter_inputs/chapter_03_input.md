---
title: "Bölüm 3 Girdi Promptu: HTML ve CSS’ten Bileşen Düşüncesine"
book_title: "React ile Web Uygulama Geliştirme"
author: "Prof. Dr. İsmail KIRBAŞ"
chapter_id: "chapter_03"
chapter_no: 3
language: tr-TR
automation_profile: "parametric_computer_book_factory_v2"
---

# Bölüm 3 Girdi Promptu: HTML ve CSS’ten Bileşen Düşüncesine

## Bölüm kimliği

- **Kitap:** React ile Web Uygulama Geliştirme
- **Ana proje:** KampüsHub
- **Bölüm ID:** `chapter_03`
- **Bölüm No:** 3
- **Bölüm dosyası:** `workspace/react/chapters/chapter_03_html_css_bilesen_dusuncesi.md`
- **Manifest başlığı:** Bölüm 3: HTML ve CSS’ten Bileşen Düşüncesine
- **Önerilen içerik dili:** Akademik ama sade Türkçe
- **Hedef okur:** HTML ve CSS bilen, Bölüm 1 ve Bölüm 2’yi tamamlamış React başlangıç öğrencileri

## Bölüm başlığı

```text
Bölüm 3: HTML ve CSS’ten Bileşen Düşüncesine
```

## Bölümün kitap içindeki yeri

Bu bölüm, Bölüm 1’de kurulan modern web, SPA, React, Node.js, npm, Vite ve KampüsHub geliştirme ortamı ile Bölüm 2’de öğrenilen modern JavaScript ES6+ kavramları üzerine inşa edilir. Bölüm 4’te JSX ve bileşen anatomisine geçmeden önce öğrencinin klasik HTML/CSS sayfa düşüncesinden React’in bileşen tabanlı arayüz modeline zihinsel geçiş yapması hedeflenir.

Bölümün ana amacı React kodu yazdırmaktan önce, var olan bir HTML/CSS arayüzünü anlamlı arayüz parçalarına ayırma, semantik HTML kullanma, CSS sınıflarını sürdürülebilir biçimde adlandırma, tekrar eden görsel örüntüleri bileşen adayı olarak belirleme ve KampüsHub uygulamasının bileşen haritasını çıkarmaktır.

## Ön koşullar

Öğrencinin şu becerilere sahip olduğu varsayılır:

1. Temel HTML etiketlerini kullanabilme.
2. Temel CSS seçicilerini, sınıf adlarını ve kutu modelini tanıma.
3. Bölüm 1’deki Vite tabanlı KampüsHub projesini çalıştırabilme.
4. Bölüm 2’deki JavaScript dizi, nesne, fonksiyon ve veri dönüştürme örneklerini okuyabilme.
5. Tarayıcı geliştirici araçlarında Elements ve Console panellerini başlangıç düzeyinde kullanabilme.

## Öğrenme çıktıları

Bölüm sonunda öğrenci:

1. Klasik HTML/CSS sayfa yapısı ile React bileşen düşüncesi arasındaki farkı açıklayabilir.
2. Bir arayüzü `header`, `main`, `section`, `article`, `nav`, `aside` ve `footer` gibi semantik bölümlere ayırabilir.
3. Tekrar eden HTML örüntülerinden bileşen adayı çıkarabilir.
4. Görsel tasarım parçalarını `Header`, `ModuleCard`, `AnnouncementList`, `EventPreview` gibi bileşen adlarıyla eşleştirebilir.
5. CSS sınıf adlarını bileşen sınırlarını yansıtacak biçimde düzenleyebilir.
6. Responsive tasarım gereksinimlerini bileşen sorumluluklarıyla ilişkilendirebilir.
7. Erişilebilirlik açısından başlık hiyerarşisi, bağlantı metni, buton, form etiketi ve renk kontrastı gibi temel unsurları kontrol edebilir.
8. KampüsHub ana ekranının bileşen envanterini çıkarabilir.
9. Bölüm 4’te JSX’e dönüştürülebilecek düzenli bir HTML/CSS iskeleti hazırlayabilir.
10. BookFactory standardına uygun `CODE_META` bloklarıyla test edilebilir JavaScript örnekleri üretebilir.
11. Programatik ekran çıktısı marker’larını bölüm içinde doğru biçimde konumlandırabilir.

## Ana kavramlar

Bu bölümde ele alınacak ana kavramlar:

- Semantik HTML
- Başlık hiyerarşisi
- Arayüz bölgelendirme
- Bileşen adayı
- Bileşen sınırı
- Sorumluluk ayrımı
- CSS sınıf adlandırma
- Kapsayıcı ve sunum sınıfları
- Tekrar eden kart yapıları
- Responsive düzen
- Erişilebilirlik kontrolü
- KampüsHub bileşen envanteri
- JSX’e hazırlık

## KampüsHub bağlantısı

Bölüm boyunca KampüsHub ana ekranı klasik HTML/CSS açısından incelenmeli ve şu bileşen adayları belirlenmelidir:

1. `AppShell`
2. `Header`
3. `MainNavigation`
4. `HeroPanel`
5. `ModuleCard`
6. `ModuleGrid`
7. `AnnouncementList`
8. `AnnouncementItem`
9. `EventPreview`
10. `UserSummary`
11. `Footer`

Bu bileşenler henüz JSX dosyaları olarak uygulanmayacaktır. Bölüm 3’te amaç, bileşen düşüncesini oluşturmak ve Bölüm 4’te JSX’e dönüştürülecek düzenli arayüz planını hazırlamaktır.

## Kullanılacak teknik kapsam

Bölümde işlenecek teknik kapsam:

- HTML sayfa iskeletinden bileşen adayları çıkarma
- Semantik HTML bölgelerini React bileşenleriyle eşleştirme
- CSS sınıf adlandırma ilkeleri
- Kart tabanlı arayüzlerin bileşenleştirilmesi
- Tekrarlı HTML yapılarının veri + bileşen yaklaşımına hazırlanması
- Responsive düzen için grid/flex mantığı
- Erişilebilirlik kontrol listesi
- Node ile test edilebilir saf JavaScript örnekleri

## Kapsam dışı konular

Bu bölümde ana akışa alınmayacak konular:

- JSX ayrıntılı sözdizimi
- Props ile bileşenler arası veri aktarımı
- State yönetimi
- Hooks
- React Router
- Form yönetimi
- Global state yönetimi
- Gerçek API entegrasyonu
- Veritabanı bağlantısı
- Kimlik doğrulama
- Build/deployment ayrıntıları
- CSS-in-JS kütüphaneleri
- Tasarım sistemi kütüphanesi kurulumu

Bu konular yalnızca ilerleyen bölümlere köprü kurmak amacıyla kısa biçimde anılabilir.

## Kod örneği politikası

1. Çalıştırılabilir kod örnekleri saf JavaScript olmalı ve Node ortamında test edilebilmelidir.
2. HTML ve CSS blokları açıklayıcı örnek olarak verilebilir; ancak test hattında çalıştırılması beklenmeyen bloklar `CODE_META` ile işaretlenmemelidir.
3. React JSX kodu bu bölümde ana akışa alınmamalı; JSX Bölüm 4’e bırakılmalıdır.
4. Kodlarda `camelCase` değişken/fonksiyon adları ve `PascalCase` bileşen adları kullanılmalıdır.
5. Kod blokları kısa, öğretici ve tek amaca odaklı olmalıdır.

## CODE_META gereksinimleri

Bölüm 3’te en az 4 adet `CODE_META` bloğu bulunmalıdır. Önerilen örnekler:

```text
react_ch03_code01
Klasik menü bağlantılarını veri listesine dönüştürme.
Node ortamında test edilebilir.

react_ch03_code02
Semantik HTML bölgelerinden bileşen adayı üretme.
Node ortamında test edilebilir.

react_ch03_code03
KampüsHub ana ekran bileşen envanteri çıkarma.
Node ortamında test edilebilir.

react_ch03_code04
CSS sınıf adı üretme ve durum sınıfı ekleme.
Node ortamında test edilebilir.

react_ch03_code05
Erişilebilirlik kontrol listesi üzerinden uyarı sayma.
Node ortamında test edilebilir.
```

Her çalıştırılabilir kod örneğinde metadata kod bloğundan önce HTML yorum bloğu olarak verilmelidir:

```markdown
<!-- CODE_META
id: react_ch03_code01
chapter_id: chapter_03
language: javascript
kind: example
title_key: html_nav_to_data_model
file: html_nav_to_data_model.js
extract: true
test: compile_run_assert
expected_stdout_contains: "Duyurular | Etkinlikler | Not Paylaşımı | Profil"
timeout_sec: 10
-->
```

`CODE_META` kesinlikle kod bloğu içine yorum satırı olarak yazılmamalıdır.

## Screenshot planı

Bölüm 3’te en az 3 screenshot marker bulunmalıdır:

```text
[SCREENSHOT:b03_01_semantik_html_bolgeleri]
[SCREENSHOT:b03_02_kampushub_bilesen_haritasi]
[SCREENSHOT:b03_03_responsive_kart_duzeni]
```

Her screenshot için şu manifest alanları tanımlanmalıdır:

```text
id
chapter_id
figure
title
route
waitFor
actions
output
caption
markdownTarget
```

Önerilen route yaklaşımı:

```text
/__book__/chapter_03/semantic-layout
/__book__/chapter_03/component-map
/__book__/chapter_03/responsive-cards
```

## Pedagojik akış

Bölüm şu akışla ilerlemelidir:

1. Klasik HTML/CSS sayfa düşüncesinin sınırları.
2. Semantik HTML ile arayüz bölgelendirme.
3. Tekrar eden görsel örüntüleri fark etme.
4. Bileşen adayı, bileşen sınırı ve sorumluluk ayrımı.
5. CSS sınıflarını bileşen düşüncesine uygun düzenleme.
6. Responsive düzen ve erişilebilirlik ilkeleri.
7. KampüsHub ana ekranını bileşen haritasına dönüştürme.
8. Bölüm 4’te JSX’e geçiş için hazırlık.

## Mini alıştırmalar

Bölüm içinde kısa alıştırmalar bulunmalıdır:

1. Verilen HTML parçalarında semantik bölge adlarını işaretleme.
2. Tekrar eden kart yapılarını bileşen adayı olarak sınıflandırma.
3. CSS sınıf adlarını daha okunabilir hâle getirme.
4. KampüsHub ana ekranı için bileşen ağacı tasarlama.
5. Erişilebilirlik açısından başlık sırası ve bağlantı metinlerini kontrol etme.

## Laboratuvar görevi

Öğrenci, KampüsHub ana ekranını HTML/CSS düzeyinde planlamalı ve en az şu çıktıları üretmelidir:

1. Semantik HTML iskeleti.
2. Bileşen adayı listesi.
3. CSS sınıf adlandırma tablosu.
4. Responsive davranış notları.
5. Erişilebilirlik kontrol listesi.
6. Bölüm 4’te JSX’e dönüştürülmek üzere kısa açıklamalı bileşen haritası.

## Kalite kontrol ölçütleri

Tam metin üretildiğinde şu ölçütler sağlanmalıdır:

1. Dosyada yalnızca bir H1 olmalıdır.
2. YAML front matter dosyanın başında bulunmalıdır.
3. Başlık hiyerarşisi tutarlı olmalıdır.
4. Standart bölüm sonu bileşenleri bulunmalıdır.
5. En az 4 `CODE_META` bloğu bulunmalıdır.
6. `CODE_META` id’leri benzersiz olmalıdır.
7. Kod bloğu içinde `// CODE_META` bulunmamalıdır.
8. Kod örnekleri Node ile çalıştırılabilir olmalıdır.
9. En az 3 screenshot marker korunmalıdır.
10. Pandoc uyumlu Markdown kullanılmalıdır.
11. Bölüm 3, JSX ayrıntılarını Bölüm 4’e bırakmalıdır.
12. KampüsHub bileşen haritası açık biçimde yer almalıdır.

## Tam metin üretim talimatı

Bu girdi promptuna dayanarak `workspace/react/chapters/chapter_03_html_css_bilesen_dusuncesi.md` dosyası için tam bölüm metni üret. Metin akademik ama sade Türkçe ile yazılsın. Bölüm, React’e yeni başlayan bilgisayar/bilişim öğrencilerine yönelik ders kitabı formatında olsun.

Tam metin şu ana yapıyı izlemelidir:

```markdown
---
yaml front matter
---

# Bölüm 3: HTML ve CSS’ten Bileşen Düşüncesine

## 3.1 Bölümün yol haritası
## 3.2 Bölümün konumu ve pedagojik rolü
## 3.3 Öğrenme çıktıları
## 3.4 Ön bilgi ve başlangıç varsayımları
## 3.5 HTML/CSS sayfa düşüncesinin sınırları
## 3.6 Semantik HTML ile arayüz bölgelendirme
## 3.7 Tekrar eden örüntülerden bileşen adaylarına
## 3.8 CSS sınıfları, düzen ve erişilebilirlik
## 3.9 KampüsHub bileşen haritası
## 3.10 Sık yapılan hatalar ve yanlış sezgiler
## 3.11 Hata ayıklama egzersizi
## 3.12 Bölüm özeti ve terim sözlüğü
## 3.13 Kavramsal sorular
## 3.14 Programlama alıştırmaları
## 3.15 Haftalık laboratuvar / proje görevi
## 3.16 İleri okuma ve bir sonraki bölüme geçiş
```

Bölüm sonunda programatik ekran çıktısı planı, `SCREENSHOT_META` blokları ve kontrol listesi bulunmalıdır.
