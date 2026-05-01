---
title: "Bölüm 4 Girdi Promptu: JSX ve Bileşen Anatomisi"
chapter_id: "chapter_04"
content_language: "tr-TR"
book_title: "React ile Web Uygulama Geliştirme"
author: "Prof. Dr. İsmail KIRBAŞ"
main_project: "KampüsHub"
output_target: "workspace/react/chapters/chapter_04_jsx_bilesen_anatomisi.md"
automation_profile: "parametric_computer_book_factory_v2_0"
---

# Bölüm 4 Girdi Promptu: JSX ve Bileşen Anatomisi

## Bölüm kimliği

- **Bölüm ID:** `chapter_04`
- **Bölüm no:** `4`
- **Dosya adı:** `chapter_04_jsx_bilesen_anatomisi.md`
- **Hedef yol:** `workspace/react/chapters/chapter_04_jsx_bilesen_anatomisi.md`
- **Kitap:** *React ile Web Uygulama Geliştirme*
- **Ana proje:** KampüsHub

## Bölüm başlığı

```text
Bölüm 4: JSX ve Bileşen Anatomisi
```

## Bölümün kitap içindeki yeri

Bu bölüm, ilk üç bölümde kurulan zemin üzerine inşa edilmelidir. Bölüm 1 modern web, Node.js, npm, Vite ve geliştirme ortamını tanıtmıştır. Bölüm 2 React için gerekli modern JavaScript ES6+ kavramlarını öğretmiştir. Bölüm 3 HTML/CSS sayfa düşüncesinden bileşen adaylarını belirleme yaklaşımına geçiş sağlamıştır. Bölüm 4 artık bu birikimi React’in gerçek yazım biçimi olan JSX ve fonksiyon bileşenleri üzerinde somutlaştırmalıdır.

Bölüm 4, Bölüm 5’te ayrıntılı işlenecek `props` konusuna doğrudan köprü kurmalıdır; ancak `props` ana konu yapılmamalıdır. Öğrenci bu bölümde bileşenin neye benzediğini, JSX’in ne olduğunu, `className`, `{}` ifadeleri, koşullu görünüm ve liste üretimi gibi temel kalıpları öğrenmelidir.

## Ön koşullar

Öğrencinin aşağıdaki konuları temel düzeyde bildiği varsayılmalıdır:

- HTML etiketleri ve semantik sayfa bölgeleri
- CSS sınıf mantığı ve basit responsive düzen fikri
- JavaScript `const`, `let`, arrow function, template literal, object/array destructuring, `map` ve `filter`
- Vite ile oluşturulmuş React projesinde `src/App.jsx` ve `src/main.jsx` dosyalarının rolü
- KampüsHub projesinin modül fikri: duyurular, etkinlikler, not paylaşımı ve profil alanı

## Öğrenme çıktıları

Bölüm sonunda öğrenci:

1. JSX’in HTML olmadığını, JavaScript içinde arayüz tanımlama sözdizimi olduğunu açıklar.
2. JSX ile HTML arasındaki temel farkları `className`, tek kök eleman, kapanan etiketler ve JavaScript ifadeleri üzerinden ayırt eder.
3. Fonksiyon bileşeninin anatomisini ad, parametre, dönüş değeri ve dışa aktarma açısından çözümler.
4. KampüsHub arayüzünü `Header`, `HeroSection`, `ModuleCard` ve `DashboardPreview` gibi küçük bileşenlere ayırır.
5. JSX içinde ifade kullanımı, koşullu görünüm ve liste üretimi için başlangıç düzeyinde doğru kalıplar yazar.
6. Bileşen adlandırma, dosya adlandırma ve klasör düzeni konusunda tutarlı kararlar verir.
7. Sık yapılan JSX hatalarını hata mesajı ve kod yapısı üzerinden teşhis eder.

## Ana kavramlar

- JSX
- JSX expression
- Fonksiyon bileşeni
- PascalCase bileşen adı
- `className`
- Tek kök eleman ve fragment
- Self-closing tag
- Conditional rendering hazırlığı
- Liste üretimi hazırlığı
- Bileşen ağacı
- Bileşen anatomisi
- KampüsHub statik arayüz iskeleti

## KampüsHub bağlantısı

Bu bölümde KampüsHub uygulamasının ilk gerçek React bileşen iskeleti kurulmalıdır. Öğrenci tek parça `App.jsx` içinde tüm arayüzü yazmak yerine şu bileşen sınırlarını görmelidir:

```text
App
├─ Header
├─ HeroSection
├─ DashboardPreview
│  ├─ ModuleCard
│  ├─ ModuleCard
│  ├─ ModuleCard
│  └─ ModuleCard
└─ Footer
```

Bölüm sonunda KampüsHub için statik ama bileşenlere ayrılmış bir ana ekran taslağı elde edilmelidir. Veri akışı ayrıntısı Bölüm 5’e bırakılmalıdır; ancak örneklerde modül kartlarının ileride `props` ile besleneceği sezdirilmelidir.

## Kullanılacak teknik kapsam

Bölümde şu konular işlenmelidir:

- JSX’in tanımı ve amacı
- JSX ile HTML arasındaki farklar
- JavaScript ifadelerinin `{}` içinde kullanılması
- `className` kullanımı
- Inline style konusuna kısa ve sınırlı not
- Fonksiyon bileşeni oluşturma
- Bileşenleri iç içe kullanma
- Fragment kullanımı
- JSX içinde koşullu metin/görünüm için başlangıç kalıpları
- JSX içinde dizi `map` yaklaşımına giriş
- KampüsHub bileşen ağacının kurulması
- Basit JSX hata ayıklama örnekleri

## Kapsam dışı konular

Aşağıdaki konular ana akışa alınmamalı, yalnızca ilerleyen bölümlere köprü olarak kısa biçimde anılmalıdır:

- `useState`
- `useEffect`
- React Router
- Context API
- Redux Toolkit
- Zustand
- TanStack Query
- Form yönetimi
- REST API entegrasyonu
- Server Components
- Next.js
- GraphQL
- React Native
- Backend, veritabanı ve kimlik doğrulama
- Class component yaklaşımı

## Kod örneği politikası

- Kodlar kısa, öğretici ve öğrenci tarafından elle denenebilir olmalıdır.
- Test edilebilir örnekler saf JavaScript olarak verilmelidir.
- Gerçek JSX/React bileşen örnekleri ders anlatımı amacıyla verilebilir; ancak mevcut test hattı `jsx` dilini doğrudan desteklemediği için bu bloklara `CODE_META` eklenmemelidir.
- `CODE_META` yalnızca `language: javascript` ve Node ile test edilebilir bloklarda kullanılmalıdır.
- Kod dosyası adları İngilizce, küçük harfli veya camelCase uyumlu olmalıdır.
- Bileşen adları PascalCase olmalıdır.

## CODE_META gereksinimleri

Bölümde en az 5 adet test edilebilir `CODE_META` örneği bulunmalıdır. Önerilen örnekler:

```text
react_ch04_code01
JSX ifade mantığını saf JavaScript render fonksiyonu üzerinden açıklar.

react_ch04_code02
Fonksiyon bileşeni fikrini nesne döndüren sade bir modelle açıklar.

react_ch04_code03
KampüsHub modül kartlarını veri dizisinden özet metne dönüştürür.

react_ch04_code04
className üretim mantığını koşula bağlı olarak test eder.

react_ch04_code05
Bileşen ağacı fikrini veri yapısı üzerinden özetler.
```

Her blok aşağıdaki biçimi izlemelidir:

```markdown
<!-- CODE_META
id: react_ch04_code01
chapter_id: chapter_04
language: javascript
kind: example
title_key: "jsx_expression_model"
file: "jsx_expression_model.js"
extract: true
test: compile_run_assert
expected_stdout_contains:
  - "KampüsHub"
timeout_sec: 5
github: true
qr: dual
-->
```

`CODE_META` kesinlikle kod bloğunun içine `// CODE_META` biçiminde yazılmamalıdır.

## Screenshot planı

Bölümde en az 3 screenshot marker bulunmalıdır. Önerilen marker’lar:

```text
[SCREENSHOT:b04_01_jsx_ifade_modeli]
[SCREENSHOT:b04_02_kampushub_bilesen_agaci]
[SCREENSHOT:b04_03_modul_kartlari_jsx]
```

Her screenshot için `SCREENSHOT_META` bloğu kullanılmalıdır. Route yaklaşımı:

```text
/__book__/chapter-04/jsx-ifade-modeli
/__book__/chapter-04/kampushub-bilesen-agaci
/__book__/chapter-04/modul-kartlari-jsx
```

Her `SCREENSHOT_META` alanında `id`, `chapter_id`, `title_key`, `route`, `waitFor`, `actions`, `output`, `manual_path`, `final_path` ve `manual_override` bulunmalıdır.

## Pedagojik akış

Bölüm aşağıdaki sıra ile ilerlemelidir:

1. JSX’in neden ortaya çıktığını açıklama
2. HTML’e benzerlik ve HTML’den farklar
3. Bileşen anatomisi: ad, gövde, dönüş, export
4. JSX içinde JavaScript ifadeleri
5. Bileşenleri iç içe kullanma
6. KampüsHub ekranını bileşen ağacına dönüştürme
7. Sık yapılan hatalar
8. Hata ayıklama egzersizi
9. Laboratuvar görevi
10. Bölüm 5’e props köprüsü

## Mini alıştırmalar

Bölüm içinde kısa uygulama soruları verilmelidir:

- `class` kullanılan JSX parçasını `className` ile düzeltme
- Birden fazla kök eleman döndüren bileşeni fragment ile düzeltme
- Bir KampüsHub modülünü `ModuleCard` bileşenine dönüştürme
- Verilen modül listesini `map` ile kartlara dönüştürmeye hazırlama
- Bileşen adlandırma hatalarını tespit etme

## Laboratuvar görevi

Öğrenciden KampüsHub ana ekranını aşağıdaki bileşenlere ayırması istenmelidir:

```text
src/components/Header.jsx
src/components/HeroSection.jsx
src/components/ModuleCard.jsx
src/components/DashboardPreview.jsx
src/components/Footer.jsx
src/App.jsx
src/App.css
```

Laboratuvar çıktısı statik olmalıdır; `state`, `effect`, router veya API kullanılmamalıdır.

## Kalite kontrol ölçütleri

- Dosyada yalnızca bir H1 bulunmalıdır.
- Başlık hiyerarşisi tutarlı olmalıdır.
- YAML front matter bulunmalıdır.
- En az 5 `CODE_META` bloğu bulunmalıdır.
- `CODE_META` id değerleri benzersiz olmalıdır.
- `// CODE_META` kullanılmamalıdır.
- En az 3 screenshot marker bulunmalıdır.
- Kod blokları kapanmış olmalıdır.
- Test edilebilir kodlar Node ortamında çalışmalıdır.
- Kapsam dışı ileri React konuları ana anlatımı dağıtmamalıdır.
- Metin Pandoc uyumlu Markdown olmalıdır.

## Tam metin üretim talimatı

Aşağıdaki ana başlık yapısını kullanarak tam bölüm metni üret:

```markdown
---
yaml front matter
---

# Bölüm 4: JSX ve Bileşen Anatomisi

## 4.1 Bölümün yol haritası
## 4.2 Bölümün konumu ve pedagojik rolü
## 4.3 Öğrenme çıktıları
## 4.4 Ön bilgi ve başlangıç varsayımları
## 4.5 JSX nedir?
## 4.6 JSX ile HTML arasındaki farklar
## 4.7 Fonksiyon bileşeninin anatomisi
## 4.8 JSX içinde ifade, koşul ve liste mantığı
## 4.9 KampüsHub bileşen iskeleti
## 4.10 Sık yapılan hatalar ve yanlış sezgiler
## 4.11 Hata ayıklama egzersizi
## 4.12 Bölüm özeti ve terim sözlüğü
## 4.13 Kavramsal sorular
## 4.14 Programlama alıştırmaları
## 4.15 Haftalık laboratuvar / proje görevi
## 4.16 İleri okuma ve bir sonraki bölüme geçiş
```

Tam metin akademik ama sade Türkçe ile yazılmalıdır. Kod açıklamaları kısa ve öğretici olmalıdır. Bölüm sonunda Bölüm 5’te işlenecek `props` konusuna açık köprü kurulmalıdır.
