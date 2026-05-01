---
title: "Bölüm 3: HTML ve CSS’ten Bileşen Düşüncesine"
subtitle: "React ile Web Uygulama Geliştirme"
author: "Prof. Dr. İsmail KIRBAŞ"
date: "2026"
lang: tr-TR
documentclass: report
toc: true
toc-depth: 3
numbersections: true
chapter_id: chapter_03
automation_profile: "parametric_computer_book_factory_v2"
---

# Bölüm 3: HTML ve CSS’ten Bileşen Düşüncesine

## 3.1 Bölümün yol haritası

React öğrenmeye başlayan öğrenciler çoğu zaman ilk olarak JSX sözdizimine odaklanır. Oysa JSX’e geçmeden önce daha temel bir zihinsel dönüşüm gerekir: Bir web sayfasını tek parça HTML dosyası olarak değil, anlamlı ve yeniden kullanılabilir arayüz parçalarının birleşimi olarak görmek. Bu bölümün ana hedefi bu dönüşümü sağlamaktır.

Bölüm 1’de modern web, SPA, React, Node.js, npm, Vite, HMR, React DevTools, `package.json`, `index.html`, `main.jsx`, `App.jsx`, `npm create vite@latest`, `npm install` ve `npm run dev` gibi kavramlarla KampüsHub geliştirme ortamını kurduk. Bölüm 2’de React kodlarını anlayabilmek için gerekli modern JavaScript ES6+ altyapısını inceledik. Bu bölümde ise HTML ve CSS bilgisini React’in bileşen tabanlı yaklaşımına bağlayacağız.

Bu bölümde şu sorulara yanıt arayacağız:

1. Klasik HTML/CSS sayfa düşüncesi büyüyen arayüzlerde neden zorlaşır?
2. Semantik HTML, bileşen tasarımı için nasıl bir başlangıç haritası sunar?
3. Bir arayüzde bileşen adayı nasıl belirlenir?
4. Bileşen sınırı ve bileşen sorumluluğu ne anlama gelir?
5. CSS sınıf adları bileşen düşüncesini nasıl destekleyebilir?
6. Tekrar eden kart yapıları veri + bileşen yaklaşımına nasıl hazırlanır?
7. Responsive düzen ve erişilebilirlik, bileşen tasarımında neden erken düşünülmelidir?
8. KampüsHub ana ekranı hangi bileşen adaylarından oluşabilir?
9. Bölüm 4’te JSX’e geçerken bu plan nasıl kullanılacaktır?

> **🎯 Bölüm Hedefi:** Bu bölümün sonunda öğrenci, klasik HTML/CSS arayüzünü semantik bölgelere ayırabilecek, tekrar eden örüntülerden bileşen adayları çıkarabilecek ve KampüsHub ana ekranı için JSX’e hazır bir bileşen haritası hazırlayabilecektir.

> **⚠️ Dikkat:** Bu bölüm React bileşenlerinin JSX ile yazıldığı bölüm değildir. JSX ayrıntıları Bölüm 4’te ele alınacaktır. Buradaki amaç, JSX yazmadan önce doğru arayüz parçalarını ve sorumluluk sınırlarını tasarlamaktır.

[SCREENSHOT:b03_01_semantik_html_bolgeleri]

## 3.2 Bölümün konumu ve pedagojik rolü

Bu bölüm, kitabın ilk kavramsal köprü bölümlerinden biridir. Önceki iki bölümde araç zinciri ve JavaScript temeli kuruldu. Ancak React’i doğru öğrenmek için yalnızca `const`, `map` veya `npm run dev` bilmek yeterli değildir. Öğrenci aynı zamanda bir arayüzü nasıl parçalara ayıracağını, hangi parçanın hangi sorumluluğu taşıdığını ve bu parçaların hangi sırayla birleşeceğini de düşünmelidir.

Klasik HTML/CSS öğretiminde öğrenci çoğu zaman sayfanın tamamını tek bir dosya içinde yazar. Başlık, menü, ana içerik, kartlar, duyurular, bağlantılar ve footer aynı dosyada yan yana durur. Küçük örneklerde bu yaklaşım anlaşılırdır. Fakat KampüsHub gibi ders duyuruları, etkinlik takvimi, not paylaşımı ve kullanıcı profili modüllerini barındıran bir uygulamada tek parça düşünmek hızla karmaşaya yol açar.

React’in bileşen tabanlı yaklaşımı, bu karmaşayı yönetmek için güçlü bir model sunar. Ancak bileşen düşüncesi yalnızca dosya açıp `Header.jsx` yazmak değildir. Önce arayüzün hangi bölümlerden oluştuğunu görmek, bu bölümlerin anlamını belirlemek, tekrar eden yapıların farkına varmak ve her parçaya açık bir görev atamak gerekir.

Bu bölüm, Bölüm 4’teki JSX ve bileşen anatomisine doğrudan hazırlık yapar. Bölüm 4’te `className`, süslü parantez kullanımı, fonksiyon bileşeni ve JSX dönüşü gibi konuları öğrenirken bu bölümde oluşturulan bileşen haritasını kullanacağız. Bölüm 5’te props konusuna geçildiğinde ise burada belirlenen `ModuleCard`, `AnnouncementItem` ve `UserSummary` gibi bileşenlerin hangi verileri alacağı daha net görülecektir.

> **React İdiomu:** React’te arayüz tasarlarken “sayfaya ne ekleyeceğim?” sorusu kadar “bu arayüz hangi küçük sorumluluklara ayrılabilir?” sorusu da önemlidir.

## 3.3 Öğrenme çıktıları

Bu bölümün sonunda öğrenci:

1. Klasik HTML/CSS sayfa yapısı ile React bileşen düşüncesi arasındaki temel farkı açıklayabilir.
2. `header`, `nav`, `main`, `section`, `article`, `aside` ve `footer` gibi semantik HTML bölgelerinin görevlerini ayırt edebilir.
3. Bir arayüzde tekrar eden örüntüleri bileşen adayı olarak belirleyebilir.
4. Bileşen adayı, bileşen sınırı ve bileşen sorumluluğu kavramlarını örneklerle açıklayabilir.
5. HTML sınıf adlarını bileşen sınırlarını yansıtacak biçimde yeniden düzenleyebilir.
6. Kart tabanlı arayüzlerde ortak yapı ile değişen içeriği ayırt edebilir.
7. Responsive düzen kararlarını bileşen düzeyindeki sorumluluklarla ilişkilendirebilir.
8. Erişilebilirlik açısından başlık hiyerarşisi, bağlantı metni, buton anlamı ve alternatif metin gibi temel unsurları kontrol edebilir.
9. KampüsHub ana ekranı için bir bileşen envanteri hazırlayabilir.
10. Bölüm 4’te JSX’e dönüştürülebilecek düzenli bir HTML/CSS planı oluşturabilir.
11. BookFactory standardına uygun `CODE_META` bloklarıyla test edilebilir JavaScript örnekleri yazabilir.
12. Programatik ekran çıktısı üretimi için `[SCREENSHOT:...]` marker’larını doğru bağlamda konumlandırabilir.

## 3.4 Ön bilgi ve başlangıç varsayımları

Bu bölüm, öğrencinin temel HTML ve CSS bilgisine sahip olduğunu varsayar. Öğrenci başlık, paragraf, liste, bağlantı, görsel, form elemanı, sınıf adı ve temel CSS düzenlemelerini tanımalıdır. Flexbox veya CSS Grid konusunda derin uzmanlık beklenmez; ancak kutu modeli, boşluklandırma, renk, font ve basit hizalama kavramlarına aşinalık yararlıdır.

Bölüm 1’de oluşturulan Vite projesinin çalıştırılabilir durumda olduğu kabul edilir. Öğrenci terminalde proje klasörüne gidip `npm run dev` komutunu çalıştırabilmeli, tarayıcıda uygulamayı görebilmeli ve React DevTools ile bileşen ağacına bakabileceğini bilmelidir. Bölüm 2’deki JavaScript örnekleri sayesinde dizi, nesne, fonksiyon, `map` ve `filter` gibi kavramların temel mantığı da tanınmış olmalıdır.

Bu bölümde gerçek JSX kodları ana akışa alınmayacaktır. Bunun yerine öğrenciden, HTML/CSS parçasını React bileşenlerine dönüştürmeden önce analiz etmesi beklenir. Bu yaklaşım, kod yazmadan önce tasarım kararlarını görünür hâle getirir ve ilerleyen bölümlerde yanlış bileşen bölme alışkanlıklarını azaltır.

> **İpucu:** Bir HTML bloğunu hemen React bileşenine çevirmeden önce, o bloğun “tek bir sorumluluğu” olup olmadığını sorun. Cevap belirsizse, arayüz parçası muhtemelen daha küçük parçalara ayrılmalıdır.

## 3.5 HTML/CSS sayfa düşüncesinin sınırları

Klasik HTML/CSS yaklaşımı öğrenme açısından çok değerlidir. Bir sayfanın iskeletini görmek, hangi etiketin ne işe yaradığını anlamak ve CSS ile görünümü düzenlemek web programlamanın temelidir. Fakat uygulama büyüdüğünde aynı yaklaşımı tek başına sürdürmek zorlaşır.

Aşağıdaki basit HTML parçasını düşünelim:

```html
<div class="topbar">
  <h1>KampüsHub</h1>
  <a href="/announcements">Duyurular</a>
  <a href="/events">Etkinlikler</a>
</div>
<div class="content">
  <div class="card">
    <h2>Duyurular</h2>
    <p>3 aktif duyuru var.</p>
  </div>
  <div class="card">
    <h2>Etkinlikler</h2>
    <p>2 yaklaşan etkinlik var.</p>
  </div>
</div>
```

Bu örnek küçük olduğu için yönetilebilir görünür. Ancak aynı sayfaya not paylaşımı, kullanıcı özeti, arama alanı, filtreler, hata mesajları, boş durum ekranları ve responsive düzen kuralları eklendiğinde HTML yapısı hızla uzar. Her kartın benzer ama biraz farklı olduğu durumlarda tekrarlar artar. Aynı sınıf adının hangi parçaya ait olduğu belirsizleşebilir. Bir değişiklik yapıldığında başka bir bölümün görünümü beklenmedik biçimde etkilenebilir.

React bu sorunu, arayüzü bileşenlere ayırarak yönetmeyi önerir. Örneğin yukarıdaki parçada üst bölüm `Header`, bağlantılar `MainNavigation`, kartlar `ModuleCard`, kartların kapsayıcısı `ModuleGrid` olarak düşünülebilir. Bu ayrım, yalnızca kod dosyalarını düzenlemek için değil, arayüz sorumluluklarını zihinde netleştirmek için de önemlidir.

### 3.5.1 Tek parça HTML’den sorumluluklara geçiş

Tek parça HTML dosyasında geliştirici çoğu zaman sayfayı yukarıdan aşağıya yazar. React düşüncesinde ise önce sayfanın hangi sorumluluklardan oluştuğu belirlenir. Bir sorumluluk, arayüzün belirli ve anlaşılır bir görevidir. Örneğin uygulama adını göstermek, ana menüyü sunmak, duyuru listesini göstermek veya kullanıcı profil özetini vermek ayrı sorumluluklardır.

Aşağıdaki tablo bu geçişi özetler:

| Klasik düşünce | Bileşen düşüncesi |
|---|---|
| Sayfanın tamamını tek dosyada yaz | Sayfayı anlamlı parçalara ayır |
| Aynı kart HTML’ini tekrar et | Ortak kart yapısını bileşen adayı olarak belirle |
| CSS sınıflarını görünüşe göre adlandır | CSS sınıflarını bileşen ve durumla ilişkilendir |
| DOM elemanını bulup değiştir | Veriyi değiştir, arayüzün yeniden oluşmasını bekle |
| Başlıkları yalnız görsel büyüklüğe göre seç | Başlık hiyerarşisini anlam ve erişilebilirliğe göre kur |

### 3.5.2 Tekrar eden örüntü problemi

KampüsHub ana ekranında duyurular, etkinlikler, not paylaşımı ve profil gibi modüller kartlar hâlinde gösterilebilir. Her kartın başlığı, açıklaması, durum etiketi ve bağlantısı olabilir. Bu durumda aynı HTML yapısını dört kez kopyalamak başlangıçta kolay görünür. Ancak beşinci kart eklendiğinde veya kart görünümü değiştiğinde tüm kopyaları güncellemek gerekir.

Bileşen düşüncesi bu noktada devreye girer. Aynı yapının tekrar ettiği yerde, değişmeyen iskelet ile değişen veriyi ayırırız. İskelet ileride `ModuleCard` bileşeni olabilir; değişen veriler ise başlık, açıklama, durum ve bağlantı gibi alanlardır. Bölüm 2’de öğrendiğimiz nesne ve dizi yapıları bu nedenle önemlidir.

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
```javascript
const navigationLinks = [
  { label: "Duyurular", href: "/announcements" },
  { label: "Etkinlikler", href: "/events" },
  { label: "Not Paylaşımı", href: "/notes" },
  { label: "Profil", href: "/profile" }
];

function createNavigationLabelList(links) {
  return links.map((link) => link.label).join(" | ");
}

console.log(createNavigationLabelList(navigationLinks));
```

**Kodun amacı:** Menü bağlantılarını tek tek HTML kopyaları olarak düşünmek yerine veri listesi olarak temsil etmek.

**Kritik satır:** `map` metodu her bağlantı nesnesinden yalnızca `label` alanını çıkarır.

**Beklenen terminal davranışı:** Kod çalıştırıldığında `Duyurular | Etkinlikler | Not Paylaşımı | Profil` metni görünür.

Bu örnek henüz React kodu değildir; ancak React’e hazırlık açısından çok önemlidir. Çünkü ileride JSX içinde benzer bir veri listesi `map` ile bağlantı elemanlarına dönüştürülecektir.

## 3.6 Semantik HTML ile arayüz bölgelendirme

Semantik HTML, etiketlerin yalnız görünüm için değil, anlam için de seçilmesini ifade eder. Örneğin her kapsayıcıyı `div` yapmak yerine üst bilgi için `header`, ana gezinme için `nav`, ana içerik için `main`, bağımsız içerik parçası için `article`, bölüm için `section` ve alt bilgi için `footer` kullanmak daha açıklayıcıdır.

Semantik etiketler üç açıdan yararlıdır. Birincisi, kodu okuyan geliştirici arayüzün yapısını daha kolay anlar. İkincisi, ekran okuyucular ve yardımcı teknolojiler sayfanın bölgelerini daha iyi yorumlayabilir. Üçüncüsü, React bileşenlerine geçerken bu bölgeler doğal bileşen sınırları hakkında ipucu verir.

Aşağıdaki HTML iskeleti KampüsHub ana ekranını semantik bölgelerle düşünmeye yardımcı olur:

```html
<header class="app-header">
  <h1>KampüsHub</h1>
  <nav aria-label="Ana menü">
    <a href="/announcements">Duyurular</a>
    <a href="/events">Etkinlikler</a>
    <a href="/notes">Not Paylaşımı</a>
  </nav>
</header>

<main class="app-main">
  <section class="hero-panel" aria-labelledby="hero-title">
    <h2 id="hero-title">Kampüs yaşamını tek ekranda takip edin</h2>
    <p>Ders duyuruları, etkinlikler ve not paylaşımları burada birleşir.</p>
  </section>

  <section class="module-grid" aria-labelledby="modules-title">
    <h2 id="modules-title">Modüller</h2>
    <article class="module-card">
      <h3>Duyurular</h3>
      <p>Güncel ders duyurularını görüntüleyin.</p>
    </article>
  </section>
</main>

<footer class="app-footer">
  <p>© 2026 KampüsHub</p>
</footer>
```

Bu iskelette amaç görsel mükemmellik değildir. Amaç, sayfanın anlamlı bölgelerini görünür kılmaktır. `header`, `nav`, `main`, `section`, `article` ve `footer` etiketleri ileride React bileşenleri için doğal adaylar sunar.

### 3.6.1 Semantik bölgeden bileşen adayına

Her semantik bölge otomatik olarak ayrı React bileşeni olmak zorunda değildir. Küçük ve tek sefer kullanılan bir `section`, doğrudan üst bileşen içinde kalabilir. Ancak tekrar eden, bağımsız sorumluluğu olan veya başka sayfalarda da kullanılabilecek bir yapı bileşen adayıdır.

Örneğin `header` bölgesi uygulamanın birçok ekranında görünecekse `Header` bileşeni güçlü bir adaydır. `nav` içinde bağlantı listesi değişebiliyorsa `MainNavigation` bileşeni ayrı düşünülebilir. `article.module-card` birden fazla kez kullanılacağı için `ModuleCard` bileşeni neredeyse kesin bir adaydır.

<!-- CODE_META
id: react_ch03_code02
chapter_id: chapter_03
language: javascript
kind: example
title_key: semantic_regions_to_component_candidates
file: semantic_regions_to_component_candidates.js
extract: true
test: compile_run_assert
expected_stdout_contains: "Header, MainNavigation, MainContent, ModuleCard, Footer"
timeout_sec: 10
-->
```javascript
const semanticRegions = [
  { tag: "header", role: "application header", repeatable: true },
  { tag: "nav", role: "main navigation", repeatable: true },
  { tag: "main", role: "main content", repeatable: false },
  { tag: "article", role: "module card", repeatable: true },
  { tag: "footer", role: "application footer", repeatable: true }
];

const componentNameByRole = {
  "application header": "Header",
  "main navigation": "MainNavigation",
  "main content": "MainContent",
  "module card": "ModuleCard",
  "application footer": "Footer"
};

function createComponentCandidateList(regions) {
  return regions
    .filter((region) => region.repeatable || region.tag === "main")
    .map((region) => componentNameByRole[region.role])
    .join(", ");
}

console.log(createComponentCandidateList(semanticRegions));
```

**Kodun amacı:** Semantik HTML bölgelerini bileşen adaylarıyla eşleştirmek.

**Kritik satır:** `filter` ve `map` birlikte kullanılarak anlamlı bölgeler bileşen adlarına dönüştürülür.

**Beklenen terminal davranışı:** Kod çalıştırıldığında `Header, MainNavigation, MainContent, ModuleCard, Footer` metni görünür.

### 3.6.2 Başlık hiyerarşisi

Semantik HTML yalnızca etiket adlarından ibaret değildir. Başlık hiyerarşisi de önemlidir. Bir sayfada genellikle bir ana `h1` bulunur. Bölüm başlıkları `h2`, alt başlıklar `h3` ile ilerler. Görsel olarak küçük görünmesi istenen bir başlığı sırf küçük olsun diye `h5` yapmak doğru değildir; görsel boyut CSS ile, anlamsal seviye ise başlık etiketiyle yönetilmelidir.

KampüsHub ana ekranında `h1` uygulama adını veya ekranın ana başlığını temsil edebilir. Modüller bölümü `h2`, her modül kartının başlığı ise `h3` olabilir. Bu düzen, hem kullanıcı hem ekran okuyucu hem de geliştirici açısından daha anlaşılırdır.

> **Dikkat:** Başlık düzeylerini görsel boyutlandırma aracı olarak kullanmayın. Başlık etiketi anlamı, CSS ise görünümü belirlemelidir.

## 3.7 Tekrar eden örüntülerden bileşen adaylarına

Bileşen adayı belirlemenin en etkili yollarından biri tekrar eden örüntüleri gözlemlemektir. Aynı HTML yapısı farklı içeriklerle birden fazla kez kullanılıyorsa, bu yapı büyük olasılıkla bileşen adayıdır. Ancak yalnız tekrar etmesi yeterli değildir; o parçanın açık bir görevi de olmalıdır.

KampüsHub ana ekranındaki modül kartlarını düşünelim. Duyurular, etkinlikler, not paylaşımı ve profil kartlarının hepsi benzer görsel iskelete sahip olabilir. Her kartta başlık, açıklama, durum, bağlantı ve belki ikon bulunur. Bu durumda şu ayrımı yapabiliriz:

- **Ortak yapı:** Kart kapsayıcısı, başlık alanı, açıklama, alt bağlantı.
- **Değişen veri:** Kart başlığı, açıklama metni, bağlantı hedefi, durum etiketi.
- **Bileşen adayı:** `ModuleCard`.
- **Liste bileşeni adayı:** Birden fazla kartı düzenleyen `ModuleGrid`.

Bu ayrım, bileşenin gelecekte nasıl yazılacağına doğrudan zemin hazırlar. Bölüm 5’te props öğrendiğimizde `ModuleCard` bileşeninin `title`, `description`, `status` ve `href` gibi değerler alabileceğini göreceğiz.

### 3.7.1 Bileşen sınırı belirleme

Bileşen sınırı, bir bileşenin nerede başlayıp nerede bittiğini ifade eder. İyi bir bileşen sınırı, bileşenin sorumluluğunu netleştirir. Örneğin `Header` bileşeni uygulama adını ve ana gezinmeyi taşıyabilir. Ancak tüm duyuru listesini de `Header` içine koymak yanlış bir sınır olur. Çünkü duyurular üst bilginin değil, ana içeriğin sorumluluğudur.

Aşağıdaki sorular bileşen sınırı belirlerken yararlıdır:

1. Bu parça tek bir görevi mi yerine getiriyor?
2. Bu parça başka yerde yeniden kullanılabilir mi?
3. Bu parçanın verisi üst parçadan bağımsız düşünülebilir mi?
4. Bu parçayı adlandırmak kolay mı?
5. Bu parçayı test etmek veya görsel olarak incelemek anlamlı mı?

Bu soruların çoğuna evet yanıtı veriliyorsa bileşen adayı güçlenir.

### 3.7.2 Bileşen adlandırma

React bileşenleri genellikle `PascalCase` ile adlandırılır: `Header`, `ModuleCard`, `AnnouncementList`, `UserSummary` gibi. Ad, bileşenin ne yaptığını açık biçimde anlatmalıdır. `Box`, `Thing`, `Part`, `Component1` gibi belirsiz adlar öğrenme sürecinde bile kaçınılmalıdır.

KampüsHub için önerilen bazı bileşen adları şöyledir:

| Arayüz parçası | Bileşen adayı | Sorumluluk |
|---|---|---|
| Uygulama kabuğu | `AppShell` | Sayfa iskeletini ve ortak düzeni taşır |
| Üst bilgi | `Header` | Uygulama adı ve kısa üst alanı gösterir |
| Ana menü | `MainNavigation` | Ana bağlantıları listeler |
| Karşılama alanı | `HeroPanel` | Ana mesajı ve kısa açıklamayı sunar |
| Modül kartı | `ModuleCard` | Tek bir modülün özetini gösterir |
| Kart ızgarası | `ModuleGrid` | Modül kartlarını düzenler |
| Duyuru listesi | `AnnouncementList` | Duyuruları liste yapısında gösterir |
| Tek duyuru | `AnnouncementItem` | Bir duyuru satırı veya kartı gösterir |
| Etkinlik önizleme | `EventPreview` | Yaklaşan etkinlikleri özetler |
| Kullanıcı özeti | `UserSummary` | Oturum açmış kullanıcı bilgisini gösterir |
| Alt bilgi | `Footer` | Telif, bağlantı ve kısa notları taşır |

[SCREENSHOT:b03_02_kampushub_bilesen_haritasi]

<!-- CODE_META
id: react_ch03_code03
chapter_id: chapter_03
language: javascript
kind: example
title_key: kampushub_component_inventory
file: kampushub_component_inventory.js
extract: true
test: compile_run_assert
expected_stdout_contains: "KampüsHub bileşen sayısı: 11"
timeout_sec: 10
-->
```javascript
const componentInventory = [
  "AppShell",
  "Header",
  "MainNavigation",
  "HeroPanel",
  "ModuleGrid",
  "ModuleCard",
  "AnnouncementList",
  "AnnouncementItem",
  "EventPreview",
  "UserSummary",
  "Footer"
];

function summarizeInventory(components) {
  return `KampüsHub bileşen sayısı: ${components.length}`;
}

console.log(summarizeInventory(componentInventory));
```

**Kodun amacı:** KampüsHub ana ekranı için belirlenen bileşen adaylarını sayısal olarak özetlemek.

**Kritik satır:** `components.length`, envanterdeki bileşen adayı sayısını verir.

**Beklenen terminal davranışı:** Kod çalıştırıldığında `KampüsHub bileşen sayısı: 11` metni görünür.

## 3.8 CSS sınıfları, düzen ve erişilebilirlik

React bileşen düşüncesine geçerken CSS de yeniden düşünülmelidir. CSS yalnızca renk ve boşluk ayarlama aracı değildir; aynı zamanda arayüz parçalarının sınırlarını görünür kılan bir adlandırma sistemidir. Karmaşık ve genel sınıf adları yerine bileşenle ilişkili sınıf adları kullanmak, kodun okunabilirliğini artırır.

Örneğin `card`, `title`, `text`, `button` gibi çok genel sınıf adları küçük örneklerde iş görür. Fakat uygulama büyüdüğünde hangi `title` sınıfının hangi parçaya ait olduğu belirsizleşebilir. Bunun yerine `module-card`, `module-card__title`, `module-card__description`, `module-card__link` gibi daha bağlamsal adlar tercih edilebilir.

Bu kitapta belirli bir CSS metodolojisini katı biçimde zorunlu tutmayacağız. Ancak şu ilkeler izlenmelidir:

1. Sınıf adı bileşenin bağlamını yansıtmalıdır.
2. Çok genel adlardan kaçınılmalıdır.
3. Durum sınıfları açık olmalıdır: `is-active`, `is-disabled`, `module-card--featured` gibi.
4. CSS, HTML anlamını bozmamalıdır.
5. Başlık ve bağlantıların anlamı CSS ile gizlenmemelidir.
6. Responsive davranış erken düşünülmelidir.

### 3.8.1 CSS sınıf adlandırma örüntüsü

Aşağıdaki örnek, bir modül kartı için daha okunabilir sınıf adları kullanır:

```html
<article class="module-card module-card--active">
  <h3 class="module-card__title">Duyurular</h3>
  <p class="module-card__description">Güncel ders duyurularını takip edin.</p>
  <a class="module-card__link" href="/announcements">Duyuruları aç</a>
</article>
```

Bu adlandırma, kartın hangi bileşene ait olduğunu ve hangi parçalarının bulunduğunu açıkça gösterir. `module-card--active` sınıfı kartın durumunu belirtir. İleride React içinde bu sınıf koşula bağlı olarak üretilebilir; ancak bu bölümde yalnızca sınıf adlandırma mantığına odaklanıyoruz.

<!-- CODE_META
id: react_ch03_code04
chapter_id: chapter_03
language: javascript
kind: example
title_key: module_card_class_name_builder
file: module_card_class_name_builder.js
extract: true
test: compile_run_assert
expected_stdout_contains: "module-card module-card--active"
timeout_sec: 10
-->
```javascript
function createModuleCardClassName(isActive) {
  const baseClass = "module-card";
  return isActive ? `${baseClass} ${baseClass}--active` : baseClass;
}

console.log(createModuleCardClassName(true));
```

**Kodun amacı:** Bir kartın temel sınıfına durum sınıfı ekleme mantığını göstermek.

**Kritik satır:** Koşullu ifade, `isActive` doğruysa ek sınıf üretir.

**Beklenen terminal davranışı:** Kod çalıştırıldığında `module-card module-card--active` metni görünür.

### 3.8.2 Responsive düzen

KampüsHub ana ekranı hem masaüstü hem de dar ekranlarda okunabilir olmalıdır. Bu nedenle kartların tek satırda sıkışması yerine ekran genişliğine göre yeniden dizilmesi gerekir. CSS Grid veya Flexbox bu amaçla kullanılabilir. Öğrenme düzeyinde aşağıdaki örüntü yeterlidir:

```css
.module-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

.module-card {
  border: 1px solid #d8dee9;
  border-radius: 12px;
  padding: 1rem;
}
```

Burada `module-grid` kartları taşıyan düzen bileşenini, `module-card` ise tek kartın görünümünü temsil eder. Bu ayrım React bileşen tasarımına da yansır: `ModuleGrid` listeyi ve düzeni, `ModuleCard` ise tek kartın içeriğini temsil eder.

[SCREENSHOT:b03_03_responsive_kart_duzeni]

### 3.8.3 Erişilebilirlik düşüncesi

Erişilebilirlik, sonradan eklenecek bir süsleme değil, arayüz tasarımının temel parçasıdır. React bileşenlerine geçmeden önce HTML/CSS düzeyinde şu sorular sorulmalıdır:

1. Sayfada anlamlı bir başlık hiyerarşisi var mı?
2. Bağlantı metinleri yalnızca “tıkla” veya “detay” gibi belirsiz ifadelerden mi oluşuyor?
3. Butonlar gerçekten eylem, bağlantılar gerçekten yönlendirme için mi kullanılıyor?
4. Form alanlarının etiketleri var mı?
5. Görseller için anlamlı alternatif metin düşünülmüş mü?
6. Renk tek başına bilgi taşımıyor mu?
7. Klavye ile gezinme engellenmiyor mu?

<!-- CODE_META
id: react_ch03_code05
chapter_id: chapter_03
language: javascript
kind: example
title_key: accessibility_warning_counter
file: accessibility_warning_counter.js
extract: true
test: compile_run_assert
expected_stdout_contains: "Eksik erişilebilirlik uyarısı: 2"
timeout_sec: 10
-->
```javascript
const accessibilityChecks = [
  { name: "Başlık hiyerarşisi", passed: true },
  { name: "Bağlantı metinleri açıklayıcı", passed: false },
  { name: "Form etiketleri", passed: true },
  { name: "Görsel alternatif metinleri", passed: false }
];

function countMissingAccessibilityItems(checks) {
  return checks.filter((check) => !check.passed).length;
}

console.log(`Eksik erişilebilirlik uyarısı: ${countMissingAccessibilityItems(accessibilityChecks)}`);
```

**Kodun amacı:** Basit bir erişilebilirlik kontrol listesinde başarısız maddeleri saymak.

**Kritik satır:** `filter((check) => !check.passed)` yalnızca eksik kalan maddeleri seçer.

**Beklenen terminal davranışı:** Kod çalıştırıldığında `Eksik erişilebilirlik uyarısı: 2` metni görünür.

## 3.9 KampüsHub bileşen haritası

Bu bölümün KampüsHub açısından en önemli çıktısı, ana ekranın bileşen haritasıdır. Bu harita, Bölüm 4’te JSX yazarken hangi parçaların hangi sırayla oluşacağını gösterecektir. Harita, uygulamanın görsel düzenini ve sorumluluklarını birlikte ifade etmelidir.

Önerilen ilk bileşen ağacı şöyledir:

```text
AppShell
├── Header
│   └── MainNavigation
├── MainContent
│   ├── HeroPanel
│   ├── ModuleGrid
│   │   ├── ModuleCard
│   │   ├── ModuleCard
│   │   ├── ModuleCard
│   │   └── ModuleCard
│   ├── AnnouncementList
│   │   ├── AnnouncementItem
│   │   └── AnnouncementItem
│   ├── EventPreview
│   └── UserSummary
└── Footer
```

Bu ağaçta `AppShell` uygulamanın genel kabuğunu temsil eder. `Header` üst bilgiyi, `MainNavigation` bağlantıları, `MainContent` ana içerik alanını, `HeroPanel` karşılama mesajını, `ModuleGrid` modül kartlarının düzenini, `ModuleCard` tek bir modülü, `AnnouncementList` duyuru grubunu, `AnnouncementItem` tek duyuruyu, `EventPreview` yaklaşan etkinlikleri, `UserSummary` kullanıcı özetini ve `Footer` alt bilgiyi temsil eder.

Bu yapı henüz kesin ve değişmez değildir. Kitap ilerledikçe bazı bileşenler ayrılabilir veya birleşebilir. Örneğin kullanıcı oturumu eklendiğinde `UserSummary` daha ayrıntılı hâle gelebilir. Router bölümünde bazı parçalar sayfa bileşenlerine taşınabilir. Ancak başlangıç için bu harita, öğrencinin arayüzü tek parça HTML olarak değil, görevleri belirli parçalardan oluşan bir sistem olarak görmesini sağlar.

### 3.9.1 Veri ile bileşen ilişkisi

Bölüm 2’de KampüsHub için duyuru, etkinlik, modül kartı ve profil verileri hazırlamıştık. Bölüm 3’te bu verilerin hangi bileşenlere karşılık gelebileceğini planlıyoruz. Bu ilişki şu şekilde düşünülebilir:

| Veri türü | Olası bileşen | Açıklama |
|---|---|---|
| `navigationLinks` | `MainNavigation` | Menü bağlantılarını üretir |
| `modules` | `ModuleGrid`, `ModuleCard` | Modül kartlarını listeler |
| `announcements` | `AnnouncementList`, `AnnouncementItem` | Duyuruları gösterir |
| `events` | `EventPreview` | Yaklaşan etkinlikleri özetler |
| `studentProfile` | `UserSummary` | Kullanıcı profilini özetler |

Bu tablo, React’te veriden arayüz üretme yaklaşımının ilk planıdır. Bölüm 4’te JSX ile HTML benzeri çıktı üreteceğiz. Bölüm 5’te props kavramı sayesinde bu verileri bileşenlere aktaracağız. Bölüm 6’da state ile değişen verileri yöneteceğiz.

### 3.9.2 KampüsHub için başlangıç CSS planı

Bu aşamada CSS planının amacı görsel tasarımı son hâline getirmek değildir. Amaç, bileşen sınırlarını destekleyen anlaşılır bir sınıf yapısı oluşturmaktır. Başlangıç için şu sınıf adları kullanılabilir:

| Bileşen adayı | CSS sınıfı | Görev |
|---|---|---|
| `AppShell` | `app-shell` | Sayfa kabuğu |
| `Header` | `app-header` | Üst bilgi |
| `MainNavigation` | `main-navigation` | Menü bağlantıları |
| `HeroPanel` | `hero-panel` | Karşılama alanı |
| `ModuleGrid` | `module-grid` | Kart düzeni |
| `ModuleCard` | `module-card` | Tek modül kartı |
| `AnnouncementList` | `announcement-list` | Duyuru listesi |
| `AnnouncementItem` | `announcement-item` | Tek duyuru |
| `EventPreview` | `event-preview` | Etkinlik özeti |
| `UserSummary` | `user-summary` | Kullanıcı bilgisi |
| `Footer` | `app-footer` | Alt bilgi |

Bu adlandırma sistemi ileride CSS dosyalarını da daha okunabilir kılar. Örneğin `module-card` ile ilgili kuralların nerede olduğunu bulmak kolaylaşır. Ayrıca screenshot üretim hattında belirli alanları seçmek için `data-book-shot` gibi öznitelikler eklenebilir.

## 3.10 Sık yapılan hatalar ve yanlış sezgiler

### 3.10.1 Her `div` parçasını bileşen sanmak

Başlangıç düzeyinde sık yapılan hatalardan biri, her `div` etiketini ayrı bir React bileşenine dönüştürmeye çalışmaktır. Bu yaklaşım dosya sayısını artırır, fakat tasarımı her zaman iyileştirmez. Bileşen, anlamlı bir sorumluluk taşımalıdır. Yalnızca boşluk vermek için kullanılan bir kapsayıcı çoğu zaman ayrı bileşen olmamalıdır.

### 3.10.2 Çok büyük bileşen tasarlamak

Ters yöndeki hata ise tüm sayfayı tek bir bileşende toplamaktır. `App` veya `MainPage` içinde yüzlerce satır HTML benzeri kod bulunması, klasik tek dosya problemini React içine taşır. İyi tasarım, gereksiz parçalanma ile aşırı büyüklük arasında dengeli bir sınır kurar.

### 3.10.3 CSS sınıflarını çok genel adlandırmak

`box`, `content`, `left`, `right`, `blue`, `big` gibi sınıf adları kısa vadede kolay görünür. Ancak uygulama büyüdükçe bu adlar bağlamı kaybeder. Bileşen düşüncesinde sınıf adının hangi parçaya ait olduğu anlaşılmalıdır. Örneğin `module-card__title`, `announcement-item__date` veya `user-summary__name` daha açıklayıcıdır.

### 3.10.4 Semantik HTML’i yalnız erişilebilirlik ayrıntısı sanmak

Semantik HTML yalnızca ekran okuyucu desteği için değil, kodun mimarisini anlamak için de yararlıdır. `header`, `main`, `section` ve `article` gibi etiketler arayüzün anlamlı parçalarını gösterir. Bu parçalar, React bileşeni tasarlarken doğal sınırlar sunar.

### 3.10.5 Görsel benzerliği tek ölçüt yapmak

İki arayüz parçası görsel olarak benziyor diye her zaman aynı bileşen olmak zorunda değildir. Bileşen tasarımında görsel benzerlik kadar veri yapısı, davranış ve sorumluluk da önemlidir. Örneğin duyuru kartı ile etkinlik kartı görünüşte benzer olabilir; ancak farklı veri alanları ve farklı davranışları varsa ayrı bileşen olarak kalmaları daha sağlıklı olabilir.

## 3.11 Hata ayıklama egzersizi

Aşağıdaki HTML parçasını inceleyin:

```html
<div class="box">
  <div class="title">KampüsHub</div>
  <div>
    <span>Duyurular</span>
    <span>Etkinlikler</span>
    <span>Profil</span>
  </div>
</div>
<div class="box">
  <div class="title">Duyurular</div>
  <div class="card">Laboratuvar yönergesi yayınlandı.</div>
  <div class="card">Proje grupları açıklandı.</div>
</div>
```

Bu parçada birkaç sorun vardır. İlk olarak, uygulama başlığı `div` yerine uygun bir başlık etiketiyle ifade edilmelidir. Menü bağlantıları yalnızca `span` olarak verilmiştir; kullanıcıyı başka bölümlere götürecekse `a` etiketleri kullanılmalıdır. `box`, `title` ve `card` sınıfları çok geneldir. Duyuruların bulunduğu alan `section`, tek duyurular ise `article` veya liste elemanı olarak düşünülebilir.

Daha iyi bir yaklaşım şu olabilir:

```html
<header class="app-header">
  <h1 class="app-header__title">KampüsHub</h1>
  <nav class="main-navigation" aria-label="Ana menü">
    <a href="/announcements">Duyurular</a>
    <a href="/events">Etkinlikler</a>
    <a href="/profile">Profil</a>
  </nav>
</header>

<section class="announcement-list" aria-labelledby="announcements-title">
  <h2 id="announcements-title">Duyurular</h2>
  <article class="announcement-item">Laboratuvar yönergesi yayınlandı.</article>
  <article class="announcement-item">Proje grupları açıklandı.</article>
</section>
```

Bu düzenleme yalnızca görsel bir iyileştirme değildir. Aynı zamanda bileşen adaylarını da görünür hâle getirir: `Header`, `MainNavigation`, `AnnouncementList` ve `AnnouncementItem`. Böylece Bölüm 4’te JSX’e geçerken hangi parçaların ayrı fonksiyon bileşeni olabileceği daha açık görülür.

**Mini görev:** Yukarıdaki düzeltilmiş HTML parçasında hangi satırların bileşen sınırı olabileceğini işaretleyin. Ardından her bileşene bir sorumluluk cümlesi yazın. Örneğin `Header`: “Uygulama adını ve ana menüyü gösterir.”

## 3.12 Bölüm özeti ve terim sözlüğü

Bu bölümde HTML ve CSS bilgisini React bileşen düşüncesine bağladık. Klasik tek parça HTML yaklaşımının küçük örneklerde yararlı olduğunu, ancak büyüyen arayüzlerde tekrar, belirsiz sınıf adları ve sorumluluk karmaşası üretebildiğini gördük. Semantik HTML’in yalnız erişilebilirlik için değil, bileşen sınırlarını düşünmek için de güçlü bir başlangıç noktası sunduğunu inceledik.

Tekrar eden kart yapılarından `ModuleCard`, kartları düzenleyen yapıdan `ModuleGrid`, duyuru satırlarından `AnnouncementItem` ve tüm liste yapısından `AnnouncementList` gibi bileşen adayları çıkardık. CSS sınıf adlarının bileşen bağlamını yansıtmasının okunabilirliği artırdığını vurguladık. Responsive düzen ve erişilebilirlik kararlarının bileşen tasarımında erken düşünülmesi gerektiğini belirttik.

KampüsHub için başlangıç bileşen haritası hazırladık. Bu harita, Bölüm 4’te JSX ve fonksiyon bileşenlerine geçerken doğrudan kullanılacaktır.

### Terim sözlüğü

| Terim | Açıklama |
|---|---|
| Semantik HTML | Etiketlerin yalnız görünüş için değil, anlam ve yapı için seçilmesi |
| Bileşen adayı | Ayrı React bileşeni olmaya uygun arayüz parçası |
| Bileşen sınırı | Bir bileşenin nerede başlayıp nerede bittiğini belirleyen tasarım kararı |
| Sorumluluk ayrımı | Her arayüz parçasının açık ve sınırlı bir görev taşıması |
| Başlık hiyerarşisi | `h1`–`h6` etiketlerinin anlamsal sırayla kullanılması |
| Kart yapısı | Benzer içerikleri görsel olarak gruplayan tekrar edebilir arayüz parçası |
| Responsive düzen | Arayüzün farklı ekran genişliklerine uyum sağlaması |
| Erişilebilirlik | Arayüzün farklı kullanıcı ihtiyaçlarına ve yardımcı teknolojilere uygun tasarlanması |
| CSS sınıf adlandırma | Stil kurallarını okunabilir ve sürdürülebilir kılmak için sınıf adlarının sistemli seçilmesi |
| Bileşen haritası | Arayüz parçalarının hiyerarşik ve sorumluluk temelli gösterimi |

## 3.13 Kavramsal sorular

1. Klasik HTML/CSS sayfa düşüncesi ile React bileşen düşüncesi arasındaki temel fark nedir?
2. Her semantik HTML bölgesi ayrı React bileşeni olmak zorunda mıdır? Gerekçesiyle açıklayın.
3. `header`, `nav`, `main`, `section`, `article` ve `footer` etiketlerinin bileşen tasarımına nasıl katkı sağladığını tartışın.
4. Bir HTML parçasının bileşen adayı olup olmadığına karar verirken hangi sorular sorulmalıdır?
5. Görsel olarak benzer iki kartın aynı bileşen olması hangi koşullarda doğru, hangi koşullarda sakıncalı olabilir?
6. CSS sınıf adlarının çok genel seçilmesi büyük uygulamalarda ne tür sorunlara yol açabilir?
7. Başlık hiyerarşisi neden yalnız görsel tasarım konusu değildir?
8. Responsive düzen kararları neden bileşen tasarımından bağımsız düşünülmemelidir?
9. KampüsHub ana ekranında `ModuleGrid` ve `ModuleCard` bileşenlerinin sorumlulukları nasıl ayrılmalıdır?
10. Bölüm 4’te JSX’e geçmeden önce bileşen haritası hazırlamak öğrenme sürecini nasıl kolaylaştırır?

## 3.14 Programlama alıştırmaları

1. Aşağıdaki arayüz parçalarını uygun bileşen adlarıyla eşleştirin: uygulama başlığı, ana menü, duyuru kartı, etkinlik özeti, kullanıcı profil kutusu.
2. Üç bağlantıdan oluşan bir menüyü önce HTML olarak yazın, sonra aynı bağlantıları JavaScript nesne dizisi olarak modelleyin.
3. Dört modülden oluşan bir KampüsHub kart listesinin veri modelini oluşturun. Her modül için `title`, `description`, `href` ve `isActive` alanlarını kullanın.
4. `module-card`, `module-card__title`, `module-card__description` ve `module-card--active` sınıflarını kullanan kısa bir HTML kartı yazın.
5. Verilen genel sınıf adlarını daha açıklayıcı hâle getirin: `box`, `big-title`, `text`, `link`, `row`.
6. Bir HTML parçasında başlık hiyerarşisini kontrol edin ve eksik ya da atlanmış başlık seviyelerini düzeltin.
7. KampüsHub ana ekranı için `AppShell` altında yer alacak bileşen ağacını metin tabanlı ağaç formatında çizin.
8. Bir erişilebilirlik kontrol listesi hazırlayın ve en az beş madde yazın.
9. CSS Grid kullanan basit bir `module-grid` düzeni yazın.
10. Bölüm 4’e hazırlık için bir HTML kartını hangi JSX değişikliklerinin beklediğini açıklayın; ancak JSX kodu yazmayın.

## 3.15 Haftalık laboratuvar / proje görevi

Bu laboratuvarın amacı, KampüsHub ana ekranını React bileşenlerine dönüştürmeden önce düzenli bir HTML/CSS ve bileşen planı hazırlamaktır.

### Görev 1: Semantik HTML iskeleti oluşturma

KampüsHub ana ekranı için `header`, `nav`, `main`, `section`, `article` ve `footer` etiketlerini kullanan bir HTML iskeleti hazırlayın. İskelette en az şu alanlar bulunmalıdır:

1. Uygulama adı.
2. Ana menü bağlantıları.
3. Karşılama / hero alanı.
4. Modül kartları bölümü.
5. Duyuru listesi bölümü.
6. Kullanıcı özeti alanı.
7. Alt bilgi.

### Görev 2: Bileşen adayı listesi çıkarma

Hazırladığınız HTML iskeletinden en az sekiz bileşen adayı çıkarın. Her bileşen için şu bilgileri yazın:

| Bileşen adı | Sorumluluk | Tekrar eder mi? | Veri alır mı? |
|---|---|---|---|
| `Header` | Uygulama üst bilgisini gösterir | Hayır | Kısmen |

Tabloyu kendi tasarımınıza göre tamamlayın.

### Görev 3: CSS sınıf adlandırma planı

Her bileşen adayı için en az bir temel CSS sınıfı belirleyin. Sınıf adları bağlamsal ve okunabilir olmalıdır. Çok genel adlardan kaçının.

### Görev 4: Responsive davranış notu

Modül kartlarının dar ekranda tek sütuna, geniş ekranda çok sütunlu düzene geçmesini sağlayacak kısa bir CSS planı yazın. CSS Grid veya Flexbox tercih edebilirsiniz.

### Görev 5: Erişilebilirlik kontrolü

Aşağıdaki maddeleri kontrol edin:

- Sayfada anlamlı bir ana başlık var mı?
- Menü bağlantıları açıklayıcı mı?
- Bölümler uygun başlıklarla tanımlanmış mı?
- Renk tek başına bilgi taşımıyor mu?
- Bağlantı ve buton görevleri karıştırılmamış mı?

### Teslim formatı

Laboratuvar çıktısı tek bir Markdown dosyası olarak teslim edilebilir. Dosyada HTML iskeleti, bileşen adayı tablosu, CSS sınıf planı, responsive notlar ve erişilebilirlik kontrol listesi bulunmalıdır.

## 3.16 İleri okuma ve bir sonraki bölüme geçiş

Bu bölümde React kodu yazmadan önce arayüzü bileşenlere ayırmayı öğrendik. Artık KampüsHub ana ekranının hangi parçalardan oluşacağını, bu parçaların nasıl adlandırılacağını ve CSS sınıflarının bileşen düşüncesini nasıl destekleyeceğini biliyoruz.

Bir sonraki bölümde JSX ve bileşen anatomisine geçeceğiz. Bu bölümde belirlediğimiz `Header`, `MainNavigation`, `ModuleGrid`, `ModuleCard`, `AnnouncementList` ve `Footer` gibi bileşen adaylarını gerçek fonksiyon bileşenlerine dönüştürmeye başlayacağız. HTML ile JSX arasındaki farkları, `className` kullanımını, JavaScript ifadelerinin JSX içinde nasıl yazıldığını ve bileşenlerin nasıl iç içe kullanılacağını adım adım inceleyeceğiz.

### İleri okuma önerileri

- HTML semantik etiketleri ve erişilebilirlik ilişkisi.
- CSS Grid ve Flexbox ile responsive kart düzenleri.
- Bileşen tabanlı tasarım prensipleri.
- Tasarım sistemlerinde adlandırma ve sorumluluk ayrımı.
- React dokümantasyonunda bileşen düşüncesi ve UI parçalama yaklaşımı.

### Programatik ekran çıktısı planı

<!-- SCREENSHOT_META
id: b03_01_semantik_html_bolgeleri
chapter_id: chapter_03
figure: "Şekil 3.1"
title: "KampüsHub semantik HTML bölgeleri"
route: "/__book__/chapter_03/semantic-layout"
waitFor: "[data-book-shot='semantic-layout']"
actions: "none"
output: "workspace/react/assets/screenshots/b03_01_semantik_html_bolgeleri.png"
caption: "KampüsHub ana ekranının header, nav, main, section ve footer bölgeleriyle semantik olarak ayrıştırılmış görünümü."
markdownTarget: "[SCREENSHOT:b03_01_semantik_html_bolgeleri]"
-->

<!-- SCREENSHOT_META
id: b03_02_kampushub_bilesen_haritasi
chapter_id: chapter_03
figure: "Şekil 3.2"
title: "KampüsHub bileşen haritası"
route: "/__book__/chapter_03/component-map"
waitFor: "[data-book-shot='component-map']"
actions: "none"
output: "workspace/react/assets/screenshots/b03_02_kampushub_bilesen_haritasi.png"
caption: "AppShell, Header, MainNavigation, ModuleGrid, ModuleCard, AnnouncementList ve Footer bileşen adaylarının hiyerarşik gösterimi."
markdownTarget: "[SCREENSHOT:b03_02_kampushub_bilesen_haritasi]"
-->

<!-- SCREENSHOT_META
id: b03_03_responsive_kart_duzeni
chapter_id: chapter_03
figure: "Şekil 3.3"
title: "Responsive modül kartı düzeni"
route: "/__book__/chapter_03/responsive-cards"
waitFor: "[data-book-shot='responsive-cards']"
actions: "viewport: desktop-and-mobile"
output: "workspace/react/assets/screenshots/b03_03_responsive_kart_duzeni.png"
caption: "KampüsHub modül kartlarının dar ve geniş ekranlarda yeniden düzenlenmesini gösteren responsive kart ızgarası."
markdownTarget: "[SCREENSHOT:b03_03_responsive_kart_duzeni]"
-->

| id | Şekil | Başlık | Route | waitFor | Çıktı | Markdown hedefi |
|---|---|---|---|---|---|---|
| `b03_01_semantik_html_bolgeleri` | Şekil 3.1 | KampüsHub semantik HTML bölgeleri | `/__book__/chapter_03/semantic-layout` | `[data-book-shot='semantic-layout']` | `workspace/react/assets/screenshots/b03_01_semantik_html_bolgeleri.png` | `[SCREENSHOT:b03_01_semantik_html_bolgeleri]` |
| `b03_02_kampushub_bilesen_haritasi` | Şekil 3.2 | KampüsHub bileşen haritası | `/__book__/chapter_03/component-map` | `[data-book-shot='component-map']` | `workspace/react/assets/screenshots/b03_02_kampushub_bilesen_haritasi.png` | `[SCREENSHOT:b03_02_kampushub_bilesen_haritasi]` |
| `b03_03_responsive_kart_duzeni` | Şekil 3.3 | Responsive modül kartı düzeni | `/__book__/chapter_03/responsive-cards` | `[data-book-shot='responsive-cards']` | `workspace/react/assets/screenshots/b03_03_responsive_kart_duzeni.png` | `[SCREENSHOT:b03_03_responsive_kart_duzeni]` |

### Bir sonraki bölüme geçiş

Bölüm 4’te bu bölümde hazırlanan bileşen haritası JSX ile somutlaştırılacaktır. Öğrenci artık yalnızca HTML etiketi yazmayacak; fonksiyon bileşeni oluşturacak, JSX içinde `className` kullanacak, JavaScript ifadelerini süslü parantezlerle yerleştirecek ve KampüsHub arayüzünü küçük bileşenlerin birleşimi olarak kuracaktır.

### Bölüm sonu kontrol listesi

- [ ] Klasik HTML/CSS yaklaşımının büyüyen uygulamalardaki sınırlarını açıklayabiliyorum.
- [ ] Semantik HTML etiketlerini bileşen sınırlarıyla ilişkilendirebiliyorum.
- [ ] Tekrar eden arayüz örüntülerinden bileşen adayı çıkarabiliyorum.
- [ ] Bileşen adı, sorumluluk ve CSS sınıfı arasında ilişki kurabiliyorum.
- [ ] KampüsHub ana ekranı için bileşen haritası çizebiliyorum.
- [ ] Responsive kart düzeninin neden `ModuleGrid` sorumluluğuyla ilişkili olduğunu açıklayabiliyorum.
- [ ] Temel erişilebilirlik kontrol maddelerini uygulayabiliyorum.
- [ ] Bölüm 4’te JSX’e geçmeye hazırım.
