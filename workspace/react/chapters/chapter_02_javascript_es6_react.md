---
title: "Bölüm 2: JavaScript ES6+ — React için Zorunlu Kavramlar"
subtitle: "React ile Web Uygulama Geliştirme"
author: "Prof. Dr. İsmail KIRBAŞ"
date: "2026"
lang: tr-TR
documentclass: report
toc: true
toc-depth: 3
numbersections: true
chapter_id: chapter_02
automation_profile: "parametric_computer_book_factory_v2"
---

# Bölüm 2: JavaScript ES6+ — React için Zorunlu Kavramlar

## 2.1 Bölümün yol haritası

React öğrenirken yalnızca yeni bir kütüphanenin adlarını ezberlemek yeterli değildir. React kodu, modern JavaScript sözdizimi üzerine kurulur. `const`, arrow function, destructuring, spread, array metotları, modül sistemi ve `async/await` gibi kavramlar ilk bakışta bağımsız JavaScript ayrıntıları gibi görünür. Ancak React bileşenlerinde arayüz metni üretirken, liste render ederken, kullanıcı profilini güncellerken veya API’den veri beklerken bu kavramlar doğrudan karşımıza çıkar.

Bölüm 1’de modern web, SPA, React, Node.js, npm, Vite, HMR, React DevTools, `package.json`, `index.html`, `main.jsx` ve `App.jsx` gibi temel kavramları tanıdık. KampüsHub projesini Vite ile çalıştırılabilir bir başlangıç iskeletine dönüştürdük. Bu bölümde aynı projenin veri ve dil altyapısını kuracağız. Henüz JSX ve bileşen anatomisine girmeyeceğiz; bunun yerine React’te sık kullanılan JavaScript kalıplarını sade ve test edilebilir örneklerle öğreneceğiz.

Bu bölümde şu sorulara yanıt arayacağız:

1. React kodlarında neden çoğunlukla `const` kullanılır?
2. Template literal, kullanıcı arayüzü metinlerini nasıl okunabilir hâle getirir?
3. Arrow function sözdizimi React örneklerinde neden sık görülür?
4. KampüsHub duyuruları, etkinlikleri ve modül kartları JavaScript nesneleriyle nasıl modellenir?
5. Destructuring, bileşenlere hazırlık açısından ne kazandırır?
6. Spread/rest sözdizimi veriyi değiştirmeden yeni kopyalar üretmek için nasıl kullanılır?
7. `map`, `filter`, `find`, `some` ve `reduce` metotları React listelerine nasıl temel oluşturur?
8. Modül sistemi, büyüyen bir React projesinde dosya düzenini nasıl destekler?
9. `Promise`, `async` ve `await` kavramları ilerideki API entegrasyonuna nasıl hazırlık sağlar?
10. BookFactory hattında test edilebilir JavaScript örnekleri nasıl işaretlenir?

> **Bölüm Hedefi:** Bu bölümün sonunda öğrenci, React kodlarını okuyabilmek ve ilerleyen bölümlerde JSX, props ve state konularına geçebilmek için gerekli modern JavaScript kavramlarını KampüsHub örnekleri üzerinden açıklayabilecek ve küçük veri dönüştürme görevlerini güvenle yazabilecektir.

> **Dikkat:** Bu bölüm kapsamlı bir JavaScript referansı değildir. Amaç, React öğrenimi için zorunlu dil kalıplarını doğru bağlamda öğretmektir.

[SCREENSHOT:b02_01_es6_console_ciktisi]

## 2.2 Bölümün konumu ve pedagojik rolü

Bu bölüm, kitabın temeller kısmında yer alır ve Bölüm 1’de oluşturulan geliştirme ortamı ile ileride yazılacak React bileşenleri arasında köprü kurar. Öğrenci artık Vite projesinin nasıl başlatılacağını, `npm run dev` komutunun hangi klasörde çalıştırılacağını ve tarayıcı geliştirici araçlarında Console panelinin neden önemli olduğunu bilmektedir. Ancak React bileşenleri yazıldığında karşılaşılacak kodların büyük kısmı modern JavaScript kalıplarından oluşur.

Örneğin bir duyuru kartı ileride JSX içinde şöyle bir düşünceyle üretilecektir: elimizde bir duyuru nesnesi vardır, bu nesneden başlık ve ders adı çekilir, liste içindeki her duyuru için bir kart oluşturulur, aktif duyurular filtrelenir ve kullanıcının rolüne göre bazı bilgiler gösterilir. Bu işlemlerin React’e özgü kısmı kadar JavaScript kısmı da önemlidir. Eğer öğrenci `map` ve destructuring mantığını bilmezse, JSX içinde liste üretme konusu gereğinden zor görünür.

KampüsHub açısından bu bölümde gerçek görsel bileşenler tamamlanmayacaktır. Bunun yerine uygulamanın içerik modelini oluşturacak veri yapıları tanıtılacaktır. Duyurular, etkinlikler, modül kartları ve kullanıcı profili düz JavaScript nesneleriyle temsil edilecek; bu veriler üzerinde filtreleme, dönüştürme ve özetleme yapılacaktır. Böylece Bölüm 4’te JSX çıktısı üretirken ve Bölüm 5’te props ile veri aktarırken hazır bir veri zemini bulunacaktır.

> **React İdiomu:** React öğrenirken “önce DOM elemanını seç, sonra içeriğini değiştir” düşüncesi yerine “veriyi tanımla, veriden arayüz üret” düşüncesi benimsenir. Bu bölüm, veriden arayüz üretme fikrinin JavaScript tarafını güçlendirir.

## 2.3 Öğrenme çıktıları

Bu bölümün sonunda öğrenci:

1. `let`, `const` ve yeniden atama kavramlarını React kod okuma bağlamında ayırt edebilir.
2. Template literal kullanarak değişken değerlerini okunabilir metinlere dönüştürebilir.
3. Arrow function ile klasik fonksiyon yazımı arasındaki temel sözdizimsel farkı açıklayabilir.
4. KampüsHub duyuru, etkinlik, modül ve profil verilerini object ve array literal ile modelleyebilir.
5. Object destructuring ve array destructuring sözdizimini temel düzeyde kullanabilir.
6. Spread/rest sözdizimiyle veriyi mutasyona uğratmadan yeni kopya oluşturabilir.
7. `map`, `filter`, `find`, `some` ve `reduce` metotlarını veri dönüştürme görevlerinde kullanabilir.
8. Optional chaining ve nullish coalescing operatörlerinin güvenli erişim açısından rolünü açıklayabilir.
9. `export` ve `import` kavramlarını dosya ölçekli düzenleme mantığıyla ilişkilendirebilir.
10. `Promise`, `async` ve `await` kavramlarını gerçek API entegrasyonuna hazırlık düzeyinde yorumlayabilir.
11. React bileşenlerine geçmeden önce verinin temiz, okunabilir ve tahmin edilebilir biçimde hazırlanmasının önemini açıklayabilir.
12. BookFactory standardına uygun `CODE_META` bloklarıyla test edilebilir JavaScript örnekleri yazabilir.

## 2.4 Ön bilgi ve başlangıç varsayımları

Bu bölümde öğrencinin Bölüm 1’deki geliştirme ortamını kurduğu varsayılır. En azından Node.js ve npm komutlarının terminalde çalıştığı, `npm create vite@latest` ile başlatılan ve `npm install` sonrasında bağımlılıkları kurulmuş Vite tabanlı KampüsHub klasörünün açılabildiği ve basit JavaScript dosyalarının Node ile çalıştırılabildiği kabul edilir.

Öğrencinin temel HTML ve CSS bilgisine sahip olması beklenir. Çünkü React bileşenleri ileride HTML benzeri JSX çıktıları üretecektir. Buna karşın bu bölümde henüz JSX ayrıntılarına girilmeyecektir. `className`, JSX içinde süslü parantez kullanımı, bileşen dosyalarının ayrıntılı yapısı ve props ile veri aktarımı sonraki bölümlerde ele alınacaktır.

Öğrenci daha önce JavaScript’te `var`, klasik `function` tanımı veya `for` döngüsü görmüş olabilir. Bu bilgi yararlıdır; ancak bu bölümde modern React projelerinde daha sık karşılaşılan ES6+ yaklaşımı esas alınacaktır. Eski sözdizimleri yalnızca karşılaştırma amacıyla kısa şekilde anılacaktır.

> **İpucu:** Bu bölümdeki örnekler terminalde Node.js ile çalıştırılabilir. Böylece React arayüzüne geçmeden önce veri dönüştürme mantığını izole biçimde test etmek mümkün olur.

## 2.5 React için modern JavaScript düşüncesi

React uygulamalarında arayüz çoğu zaman verinin bir yansımasıdır. KampüsHub ana sayfasında üç duyuru varsa üç duyuru kartı, iki yaklaşan etkinlik varsa iki etkinlik satırı ve dört aktif modül varsa dört modül kartı göstermek isteriz. Bu yaklaşımda JavaScript’in görevi, veriyi uygun biçimde hazırlamak ve arayüze sunulacak yapıya dönüştürmektir.

Klasik DOM odaklı yaklaşımlarda geliştirici çoğu zaman bir elemanı seçer, metnini değiştirir, yeni HTML parçaları üretir ve bunları sayfaya elle ekler. React yaklaşımında ise bileşenler, kendilerine verilen veriye göre nasıl görüneceklerini bildirir. Bu nedenle verinin dizi, nesne, fonksiyon ve modül düzeyinde düzenli olması çok önemlidir.

Aşağıdaki tablo, bu bölümdeki JavaScript kavramlarının ileride hangi React konularına zemin hazırladığını gösterir:

| JavaScript kavramı | React öğrenimindeki karşılığı |
|---|---|
| `const` | Bileşen içinde sabit referanslar ve okunabilir veri tanımları |
| Template literal | Dinamik metin, başlık ve açıklama üretimi |
| Arrow function | Event handler, helper fonksiyon ve kısa dönüşler |
| Object literal | Props’a gönderilecek veri yapıları |
| Array literal | Liste render etme hazırlığı |
| Destructuring | Props ve state değerlerini okunabilir biçimde açma |
| Spread | State güncelleme ve nesne/dizi kopyalama mantığına hazırlık |
| `map` | Listeyi arayüz elemanlarına dönüştürme |
| `filter` | Görüntülenecek veriyi seçme |
| Modül sistemi | Bileşen ve veri dosyalarını düzenleme |
| `async/await` | API’den veri çekme mantığına hazırlık |

Bu tabloyu ezberlemek gerekmez. Önemli olan, React öğreniminde zor görünen birçok kod parçasının aslında bu JavaScript kavramlarının birleşiminden oluştuğunu fark etmektir.

## 2.6 Değişkenler, template literal ve fonksiyonlar

### 2.6.1 `let` ve `const`

Modern JavaScript’te değişken tanımlarken genellikle `const` ve gerektiğinde `let` kullanılır. `const`, değişken adının başka bir değere yeniden atanmasını engeller. Bu, değerin her durumda derinlemesine değişmez olduğu anlamına gelmez; özellikle nesne ve dizilerde referans sabit kalırken içerik mutasyona uğratılabilir. React kodlarında önemli olan, bu ayrımı bilmek ve veriyi güncellerken çoğunlukla yeni kopyalar üretmektir.

Basit bir kural olarak, değer yeniden atanmayacaksa `const` kullanmak daha okunabilir bir tercih olur. Döngü sayacı veya koşula göre değişen ara değer gibi yeniden atama gerektiren durumlarda `let` kullanılabilir.

```javascript
const appName = "KampüsHub";
let unreadAnnouncementCount = 3;

unreadAnnouncementCount = unreadAnnouncementCount + 1;

console.log(appName);
console.log(unreadAnnouncementCount);
```

Bu küçük örnekte `appName` uygulama adını temsil eder ve yeniden atanmaz. `unreadAnnouncementCount` ise kullanıcı yeni duyuru aldıkça değişebilir. React içinde state konusuna geçtiğimizde değer değişimlerini doğrudan bu şekilde yapmayacağız; ancak değişken mantığını anlamak ilk adımdır.

### 2.6.2 Template literal

Template literal, metin içinde değişken kullanmayı kolaylaştırır. Çift tırnak veya tek tırnakla uzun birleştirmeler yapmak yerine ters tırnak kullanılır ve değişkenler `${...}` biçiminde metne yerleştirilir.

<!-- CODE_META
id: react_ch02_code01
chapter_id: chapter_02
language: javascript
kind: example
title_key: js_template_literal_kampushub
file: kampushub_template_literal.js
extract: true
test: compile_run_assert
expected_stdout_contains: "KampüsHub: 3 aktif duyuru"
timeout_sec: 10
-->
```javascript
const appName = "KampüsHub";
const activeAnnouncementCount = 3;

function createDashboardMessage(name, count) {
  return `${name}: ${count} aktif duyuru`;
}

console.log(createDashboardMessage(appName, activeAnnouncementCount));
```

**Kodun amacı:** Template literal ile değişken içeren okunabilir bir KampüsHub mesajı üretmek.

**Kritik satır:** `${name}` ve `${count}` ifadeleri, metnin içine dinamik değer yerleştirir.

**Beklenen terminal davranışı:** Kod çalıştırıldığında `KampüsHub: 3 aktif duyuru` metni görünür.

Template literal, ileride JSX içinde metin üretirken de dolaylı olarak işimize yarar. JSX içinde doğrudan template literal kullanmak her zaman gerekli değildir; ancak dinamik metin hazırlayan yardımcı fonksiyonlarda oldukça okunabilirdir.

### 2.6.3 Arrow function

Arrow function, fonksiyon yazımı için kısa bir sözdizimi sunar. React örneklerinde event handler, dizi metodu callback’i ve küçük yardımcı fonksiyonlarda sık görülür. Bu bölümde `this` bağlamı gibi ileri ayrıntılara girmeyeceğiz. Başlangıç için temel kullanım yeterlidir.

```javascript
const formatCourse = (courseCode, courseName) => `${courseCode} - ${courseName}`;

console.log(formatCourse("BMU204", "Web Programlama"));
```

Bu fonksiyon, iki parametre alır ve tek satırda bir metin döndürür. Tek satırlık dönüşlerde süslü parantez ve `return` yazmak gerekmez. Fonksiyon gövdesi birden fazla satırsa süslü parantez ve açık `return` kullanmak daha anlaşılırdır.

> **Dikkat:** Kısa yazmak her zaman daha iyi yazmak değildir. Özellikle öğrenme aşamasında, fonksiyonun ne döndürdüğü belirsizleşiyorsa açık `return` kullanmak daha sağlıklıdır.

## 2.7 Nesneler, diziler ve destructuring

KampüsHub gibi bir uygulamada veriler çoğunlukla nesneler ve dizilerle temsil edilir. Tek bir duyuru nesne, duyuruların tamamı ise dizi olarak düşünülebilir. Bu model, ileride React bileşenlerine veri aktarmayı kolaylaştırır.

```javascript
const announcement = {
  id: 1,
  courseCode: "BMU204",
  title: "Hafta 2 laboratuvar yönergesi yayınlandı",
  isPinned: true
};

const announcements = [announcement];
```

Burada `announcement` tek bir duyurudur. `announcements` ise birden fazla duyuruyu taşıyabilecek listedir. React’te liste render ederken genellikle bu tür dizilerle çalışılır.

### 2.7.1 Object destructuring

Destructuring, nesne veya dizi içinden değerleri kısa ve okunabilir biçimde çekmeyi sağlar. React bileşenlerinde props değerlerini açarken sık karşımıza çıkar. Bu bölümde props’a geçmeden önce aynı mantığı düz JavaScript nesneleri üzerinde görelim.

<!-- CODE_META
id: react_ch02_code02
chapter_id: chapter_02
language: javascript
kind: example
title_key: js_destructuring_profile_summary
file: kampushub_profile_summary.js
extract: true
test: compile_run_assert
expected_stdout_contains: "Elif | Bilgisayar Mühendisliği | 2. sınıf"
timeout_sec: 10
-->
```javascript
const studentProfile = {
  fullName: "Elif",
  department: "Bilgisayar Mühendisliği",
  year: 2,
  role: "student"
};

function createProfileSummary(profile) {
  const { fullName, department, year } = profile;
  return `${fullName} | ${department} | ${year}. sınıf`;
}

console.log(createProfileSummary(studentProfile));
```

**Kodun amacı:** Profil nesnesindeki alanları destructuring ile çekip okunabilir bir özet üretmek.

**Kritik satır:** `const { fullName, department, year } = profile;` ifadesi, nesnenin üç alanını ayrı sabitlere açar.

**Beklenen terminal davranışı:** Kod çalıştırıldığında öğrencinin profil özeti tek satır olarak yazdırılır.

### 2.7.2 Array destructuring

Dizi destructuring, dizinin belirli konumlarındaki değerleri ayrı değişkenlere alır. KampüsHub’da yaklaşan etkinlik listesinin ilk elemanını almak gibi durumlarda kullanılabilir.

```javascript
const upcomingEvents = ["React çalışma grubu", "Proje teslim oturumu", "Kariyer günü"];
const [firstEvent, secondEvent] = upcomingEvents;

console.log(firstEvent);
console.log(secondEvent);
```

Bu örnekte ilk iki etkinlik ayrı değişkenlere alınmıştır. Ancak uzun listeleri işlemek için genellikle destructuring yerine `map`, `filter` veya `find` gibi dizi metotları kullanılır.

### 2.7.3 Varsayılan değerler

Destructuring sırasında varsayılan değer verilebilir. Bu yaklaşım, eksik alanlara karşı daha güvenli kod yazmayı sağlar.

```javascript
const profile = {
  fullName: "Ahmet"
};

const { fullName, department = "Bölüm bilgisi yok" } = profile;

console.log(`${fullName} - ${department}`);
```

Bu kodda `department` alanı nesnede bulunmadığı için varsayılan metin kullanılır. React bileşenlerinde eksik props veya opsiyonel veri durumlarıyla karşılaşıldığında benzer düşünce yararlı olur.

[SCREENSHOT:b02_02_kampushub_veri_modeli]

## 2.8 Dizi metotları ve mutasyonsuz veri güncelleme

React öğreniminde en kritik JavaScript becerilerinden biri, dizileri ve nesneleri doğrudan değiştirmek yerine yeni kopyalar üretmektir. State konusuna henüz girmedik; ancak React’te arayüz güncellemelerinin tahmin edilebilir olması için mutasyonsuz düşünme alışkanlığı erken kazanılmalıdır.

### 2.8.1 `map`, `filter`, `find`, `some` ve `reduce`

Dizi metotları, liste verisini işlemek için güçlü ve okunabilir araçlardır. KampüsHub ana sayfasında aktif modülleri seçmek, modül adlarını listelemek veya toplam bildirim sayısını hesaplamak için kullanılabilirler.

<!-- CODE_META
id: react_ch02_code03
chapter_id: chapter_02
language: javascript
kind: example
title_key: js_array_methods_module_cards
file: kampushub_module_cards.js
extract: true
test: compile_run_assert
expected_stdout_contains: "Aktif modüller: Duyurular, Etkinlikler, Profil"
timeout_sec: 10
-->
```javascript
const modules = [
  { id: "announcements", title: "Duyurular", isActive: true, unreadCount: 3 },
  { id: "events", title: "Etkinlikler", isActive: true, unreadCount: 1 },
  { id: "notes", title: "Not Paylaşımı", isActive: false, unreadCount: 0 },
  { id: "profile", title: "Profil", isActive: true, unreadCount: 0 }
];

const activeModuleTitles = modules
  .filter((module) => module.isActive)
  .map((module) => module.title);

console.log(`Aktif modüller: ${activeModuleTitles.join(", ")}`);
```

**Kodun amacı:** Aktif KampüsHub modüllerini filtrelemek ve başlıklarını okunabilir metne dönüştürmek.

**Kritik satırlar:** `filter` yalnızca aktif modülleri seçer; `map` seçilen modülleri başlık listesine dönüştürür.

**Beklenen terminal davranışı:** Kod çalıştırıldığında aktif modül adları tek satırda listelenir.

Bu örnek, ileride JSX içinde liste render ederken kullanılacak zihinsel modele çok yakındır. React tarafında `map` genellikle bir veri listesini arayüz elemanları listesine dönüştürmek için kullanılır. Bu bölümde henüz arayüz elemanı üretmiyoruz; sadece veri dönüşümünü öğreniyoruz.

### 2.8.2 `find` ve `some`

`find`, koşulu sağlayan ilk elemanı döndürür. `some`, koşulu sağlayan en az bir eleman olup olmadığını `true` veya `false` olarak bildirir.

```javascript
const announcements = [
  { id: 1, title: "Laboratuvar yönergesi", isPinned: true },
  { id: 2, title: "Okuma listesi", isPinned: false }
];

const pinnedAnnouncement = announcements.find((item) => item.isPinned);
const hasPinnedAnnouncement = announcements.some((item) => item.isPinned);

console.log(pinnedAnnouncement.title);
console.log(hasPinnedAnnouncement);
```

Bu metotlar özellikle koşullu gösterimlere hazırlık sağlar. Örneğin sabitlenmiş duyuru varsa ana sayfanın üst kısmında özel alan gösterilebilir.

### 2.8.3 `reduce` ile özet üretme

`reduce`, listedeki değerlerden tek bir özet değer üretmek için kullanılır. Başlangıç düzeyinde dikkatli kullanılmalıdır; bazı durumlarda `map` ve `filter` daha okunabilir olabilir.

```javascript
const modules = [
  { title: "Duyurular", unreadCount: 3 },
  { title: "Etkinlikler", unreadCount: 1 },
  { title: "Profil", unreadCount: 0 }
];

const totalUnread = modules.reduce((sum, module) => sum + module.unreadCount, 0);

console.log(totalUnread);
```

Bu örnekte tüm modüllerdeki okunmamış bildirimlerin toplamı hesaplanır. İleride bu değer bir bildirim rozeti olarak gösterilebilir.

### 2.8.4 Spread ile mutasyonsuz güncelleme

Aşağıdaki örnek, bir duyuruyu doğrudan değiştirmek yerine yeni bir nesne üreterek günceller. Bu yaklaşım, React state güncelleme mantığına hazırlık için çok önemlidir.

<!-- CODE_META
id: react_ch02_code04
chapter_id: chapter_02
language: javascript
kind: example
title_key: js_immutable_announcement_update
file: kampushub_immutable_update.js
extract: true
test: compile_run_assert
expected_stdout_contains: "Güncel başlık: Laboratuvar saati değişti"
timeout_sec: 10
-->
```javascript
const announcement = {
  id: 7,
  title: "Laboratuvar saati duyurusu",
  courseCode: "BMU204",
  isPinned: false
};

function updateAnnouncementTitle(item, newTitle) {
  return {
    ...item,
    title: newTitle
  };
}

const updatedAnnouncement = updateAnnouncementTitle(
  announcement,
  "Laboratuvar saati değişti"
);

console.log(`Eski başlık: ${announcement.title}`);
console.log(`Güncel başlık: ${updatedAnnouncement.title}`);
```

**Kodun amacı:** Spread sözdizimiyle mevcut duyurudan yeni ve güncellenmiş bir duyuru nesnesi üretmek.

**Kritik satır:** `...item` mevcut alanları yeni nesneye taşır; ardından `title` alanı yeni değerle değiştirilir.

**Beklenen terminal davranışı:** Kod hem eski başlığı hem yeni başlığı gösterir. Eski nesne doğrudan değiştirilmez.

> **Dikkat:** `const` ile tanımlanmış bir nesnenin alanları teknik olarak değiştirilebilir. Ancak React öğreniminde sağlıklı alışkanlık, var olan nesneyi değiştirmek yerine yeni nesne üretmektir.

[SCREENSHOT:b02_03_modul_kartlari_onizleme]

## 2.9 KampüsHub veri modeli ve modül hazırlığı

Bölüm 2’nin KampüsHub çıktısı, görsel olarak tamamlanmış bir React arayüzü değil; ileride arayüzü besleyecek temiz veri modelidir. Bu veri modeli, `src/data` klasörü altında ayrı dosyalara taşınabilecek şekilde tasarlanmalıdır.

Aşağıdaki tablo, bölüm sonunda hazırlanması beklenen veri dosyalarını özetler:

| Dosya | Amaç | İleride kullanılacağı konu |
|---|---|---|
| `src/data/announcements.js` | Ders duyurularını tutmak | Liste render etme, props, filtreleme |
| `src/data/events.js` | Etkinlik takvimi verisini tutmak | Koşullu gösterim, tarih sıralama |
| `src/data/modules.js` | Ana sayfa modül kartlarını tutmak | JSX ile kart üretimi |
| `src/data/profile.js` | Kullanıcı profil özetini tutmak | Props ve profil bileşeni |

Bu bölümde dosya düzenini kavramsal olarak şu şekilde düşünebiliriz:

```text
src/
  data/
    announcements.js
    events.js
    modules.js
    profile.js
```

Bu klasör yapısı, Bölüm 1’de hazırlanan KampüsHub proje iskeletiyle uyumludur. Öğrencinin bu dosyaları hemen React içinde kullanması gerekmez. Amaç, verinin uygulama mantığından ve arayüzden ayrı düşünülmesi gerektiğini erken göstermektir.

### 2.9.1 Örnek veri modeli

```javascript
const announcements = [
  {
    id: 1,
    courseCode: "BMU204",
    title: "Hafta 2 laboratuvar yönergesi yayınlandı",
    summary: "ES6+ alıştırmalarını tamamlayınız.",
    isPinned: true
  },
  {
    id: 2,
    courseCode: "BMU210",
    title: "Proje ekipleri oluşturuluyor",
    summary: "Ekip tercih formu cuma gününe kadar açıktır.",
    isPinned: false
  }
];
```

Bu veri, ileride tek tek duyuru kartlarına dönüştürülebilir. Her nesnede benzersiz `id` bulunması önemlidir. React listelerinde `key` kullanımı ileride anlatılacaktır; ancak şimdiden her veri öğesine kalıcı bir kimlik vermek iyi bir alışkanlıktır.

### 2.9.2 Modül sistemiyle düşünme

Modern JavaScript projelerinde her şeyi tek dosyada tutmak sürdürülebilir değildir. KampüsHub büyüdükçe duyuru verileri, etkinlik verileri, yardımcı fonksiyonlar ve bileşenler ayrı dosyalara bölünmelidir. JavaScript modül sistemi, dosyalar arasında değer paylaşmayı sağlar.

```javascript
export const moduleTitle = "Duyurular";

export function formatModuleTitle(title) {
  return title.toUpperCase("tr-TR");
}
```

Başka bir dosyada bu değerler `import` ile alınabilir. Bu bölümde modül sistemi yalnızca temel fikir düzeyinde ele alınır. İlerleyen bölümlerde React bileşenleri ve veri dosyaları ayrıldığında bu yapı doğal olarak kullanılacaktır.

### 2.9.3 Optional chaining ve nullish coalescing

Gerçek uygulamalarda her veri her zaman eksiksiz olmayabilir. Kullanıcı profilinde bölüm bilgisi eksik olabilir veya bir duyurunun ek açıklaması bulunmayabilir. Optional chaining (`?.`) ve nullish coalescing (`??`) bu durumlarda güvenli erişim sağlar.

```javascript
const profile = {
  fullName: "Yasemin",
  contact: {
    email: "yasemin@example.edu.tr"
  }
};

const phone = profile.contact?.phone ?? "Telefon bilgisi yok";

console.log(phone);
```

Burada `profile.contact?.phone` alanı yoksa hata fırlatmak yerine `undefined` döner. `??` operatörü ise değer `null` veya `undefined` olduğunda varsayılan metni kullanır.

## 2.10 Sık yapılan hatalar ve yanlış sezgiler

### 2.10.1 `const` değerleri hiç değişmez sanmak

`const`, değişken adının başka bir değere yeniden atanmasını engeller. Ancak nesne veya dizi içeriğinin mutasyona uğratılmasını tek başına engellemez.

```javascript
const profile = { fullName: "Elif" };
profile.fullName = "Elif K.";
```

Bu kod teknik olarak çalışır. Ancak React öğreniminde bu tarz doğrudan güncellemelere alışmak ileride sorun çıkarabilir. Daha sağlıklı yaklaşım, yeni nesne üretmektir.

```javascript
const updatedProfile = {
  ...profile,
  fullName: "Elif K."
};
```

### 2.10.2 `map` ile `forEach` arasındaki farkı karıştırmak

`forEach`, listedeki her eleman için işlem yapar ancak yeni bir dizi döndürmez. `map` ise her elemanı dönüştürerek yeni bir dizi üretir. React’te listeyi arayüz elemanlarına dönüştürmek için genellikle `map` kullanılır.

```javascript
const titles = modules.map((module) => module.title);
```

Bu kod, modül başlıklarından oluşan yeni bir dizi üretir.

### 2.10.3 Arrow function dönüşünü unutmak

Süslü parantez kullanıldığında açık `return` gerekir.

```javascript
const titles = modules.map((module) => {
  return module.title;
});
```

Tek satırlık dönüşlerde süslü parantez kullanılmazsa değer otomatik döner.

```javascript
const titles = modules.map((module) => module.title);
```

### 2.10.4 Veriyi doğrudan değiştirmek

Aşağıdaki yaklaşım başlangıçta kolay görünür; ancak React state mantığı açısından sağlıklı değildir.

```javascript
announcement.title = "Yeni başlık";
```

Bunun yerine yeni nesne üretmek tercih edilmelidir.

```javascript
const updatedAnnouncement = {
  ...announcement,
  title: "Yeni başlık"
};
```

### 2.10.5 Asenkron sonucu beklemeden kullanmak

`async` fonksiyonlar sonuçlarını hemen doğrudan değer olarak değil, Promise üzerinden verir. Bu nedenle `await` kullanılması gereken yerlerde sonucu beklemek gerekir.

<!-- CODE_META
id: react_ch02_code05
chapter_id: chapter_02
language: javascript
kind: example
title_key: js_async_await_mock_announcements
file: kampushub_async_announcements.js
extract: true
test: compile_run_assert
expected_stdout_contains: "Yüklenen duyuru sayısı: 2"
timeout_sec: 10
-->
```javascript
function fetchAnnouncementsMock() {
  return Promise.resolve([
    { id: 1, title: "ES6+ çalışma notları yayınlandı" },
    { id: 2, title: "KampüsHub veri modeli hazırlanacak" }
  ]);
}

async function printAnnouncementCount() {
  const announcements = await fetchAnnouncementsMock();
  console.log(`Yüklenen duyuru sayısı: ${announcements.length}`);
}

printAnnouncementCount();
```

**Kodun amacı:** Gerçek API kullanmadan, Promise ve `async/await` mantığını sahte duyuru verisiyle göstermek.

**Kritik satır:** `await fetchAnnouncementsMock()` ifadesi, Promise sonucunu bekleyip duyuru dizisini alır.

**Beklenen terminal davranışı:** Kod çalıştırıldığında yüklenen duyuru sayısı ekrana yazdırılır.

## 2.11 Hata ayıklama egzersizi

Aşağıdaki kodda iki sorun vardır. Amaç, aktif modül başlıklarını listelemek ve toplam okunmamış bildirim sayısını hesaplamaktır.

```javascript
const modules = [
  { title: "Duyurular", isActive: true, unreadCount: 3 },
  { title: "Etkinlikler", isActive: true, unreadCount: 1 },
  { title: "Profil", isActive: false, unreadCount: 0 }
];

const activeTitles = modules.filter((module) => {
  module.isActive;
}).map((module) => module.title);

const totalUnread = modules.reduce((sum, module) => {
  sum + module.unreadCount;
}, 0);

console.log(activeTitles);
console.log(totalUnread);
```

**Beklenen davranış:** `activeTitles` içinde `Duyurular` ve `Etkinlikler` bulunmalıdır. `totalUnread` değeri `4` olmalıdır.

**Sorun analizi:** Süslü parantez kullanılan arrow function gövdelerinde açık dönüş yapılmamıştır. `filter` callback’i `true` veya `false` döndürmediği için filtreleme doğru çalışmaz. `reduce` callback’i de yeni toplamı döndürmediği için sonuç beklenen biçimde oluşmaz.

Düzeltilmiş sürüm:

```javascript
const modules = [
  { title: "Duyurular", isActive: true, unreadCount: 3 },
  { title: "Etkinlikler", isActive: true, unreadCount: 1 },
  { title: "Profil", isActive: false, unreadCount: 0 }
];

const activeTitles = modules
  .filter((module) => module.isActive)
  .map((module) => module.title);

const totalUnread = modules.reduce(
  (sum, module) => sum + module.unreadCount,
  0
);

console.log(activeTitles);
console.log(totalUnread);
```

**Öğrenme noktası:** Arrow function kısa dönüş biçimi ile blok gövde biçimi karıştırılmamalıdır. Blok gövde kullanılıyorsa açık `return` gerekir.

## 2.12 Bölüm özeti ve terim sözlüğü

Bu bölümde React öğrenimi için gerekli modern JavaScript kavramlarını KampüsHub bağlamında ele aldık. `let` ve `const` ile değişken tanımlamayı, template literal ile okunabilir metin üretmeyi, arrow function ile kısa fonksiyonlar yazmayı, nesne ve dizilerle veri modellemeyi, destructuring ile değerleri açmayı ve spread ile mutasyonsuz kopyalar üretmeyi inceledik.

Dizi metotları bölümün en önemli parçalarından biridir. `map`, `filter`, `find`, `some` ve `reduce`, React listelerine ve koşullu arayüz üretimine doğrudan zemin hazırlar. Ayrıca modül sistemi ve `async/await` kavramları, ileride bileşen dosyalarını düzenlerken ve API entegrasyonu yaparken kullanılacaktır.

Bu bölümde öğrendiğimiz yapıların tamamı, ilerleyen bölümlerde JSX, props, state, hooks, React Router, API entegrasyonu ve test konularına temel oluşturacaktır.

| Terim | Açıklama |
|---|---|
| ES6+ | JavaScript’in modern sürümlerinde gelen sözdizimi ve dil özelliklerini ifade eden genel ad |
| `const` | Yeniden atanmayan değişken referansı tanımlamak için kullanılan anahtar sözcük |
| `let` | Yeniden atanabilir blok kapsamlı değişken tanımlamak için kullanılan anahtar sözcük |
| Template literal | Ters tırnakla yazılan ve `${...}` içinde ifade alabilen metin biçimi |
| Arrow function | `=>` sözdizimiyle yazılan kısa fonksiyon biçimi |
| Destructuring | Nesne veya dizi içinden değerleri kısa biçimde değişkenlere alma |
| Spread | Nesne veya dizi içeriğini yeni bir yapıya yayma sözdizimi |
| Rest | Kalan değerleri tek değişkende toplama sözdizimi |
| Mutasyon | Var olan nesne veya dizinin doğrudan değiştirilmesi |
| Mutasyonsuz güncelleme | Var olan veriyi değiştirmeden yeni kopya üretme yaklaşımı |
| `map` | Listedeki elemanları dönüştürerek yeni dizi üreten metot |
| `filter` | Koşulu sağlayan elemanlardan yeni dizi üreten metot |
| `reduce` | Dizi elemanlarından tek bir özet değer üreten metot |
| Promise | Asenkron işlemin gelecekte tamamlanacak sonucunu temsil eden yapı |
| `async/await` | Promise tabanlı asenkron kodu daha okunabilir yazmayı sağlayan sözdizimi |
| CODE_META | BookFactory hattında kod bloklarını tanımlamak ve test etmek için kullanılan metadata bloğu |

## 2.13 Kavramsal sorular

1. React öğrenirken modern JavaScript kavramlarını önceden öğrenmek neden önemlidir?
2. `const` ile tanımlanan bir nesnenin alanlarının değiştirilebilmesi, React açısından neden dikkat edilmesi gereken bir durumdur?
3. Template literal ile klasik metin birleştirme arasında okunabilirlik açısından ne fark vardır?
4. Arrow function kısa dönüş biçiminde süslü parantez kullanılmadığında ne olur?
5. Destructuring, ileride props kullanırken nasıl bir kolaylık sağlar?
6. Spread sözdizimi mutasyonsuz veri güncellemede nasıl bir rol oynar?
7. `map` ve `forEach` arasındaki temel fark nedir?
8. `filter` ve `find` hangi durumlarda tercih edilir?
9. Optional chaining hangi tür hataları önlemeye yardımcı olur?
10. `async/await` kavramı API entegrasyonuna geçmeden önce neden öğrenilmelidir?

## 2.14 Programlama alıştırmaları

### Kolay düzey

1. `courseCode`, `courseName` ve `instructor` alanlarına sahip bir ders nesnesi oluşturun. Template literal kullanarak tek satırlık ders özeti üretin.
2. Üç etkinlik adından oluşan bir dizi tanımlayın. Array destructuring ile ilk etkinliği ayrı değişkene alın.
3. `fullName` ve `department` alanlarına sahip bir profil nesnesinden destructuring ile değerleri çekin.

### Orta düzey

1. KampüsHub duyurularını temsil eden en az dört nesnelik bir dizi oluşturun. Yalnızca sabitlenmiş duyuruları `filter` ile seçin.
2. Modül listesindeki başlıkları `map` ile yeni bir diziye dönüştürün.
3. Duyuru nesnesini doğrudan değiştirmeden, spread kullanarak `isPinned` değerini güncelleyen bir fonksiyon yazın.
4. Etkinlik listesinde belirli bir kategoriye ait ilk etkinliği `find` ile bulun.

### Zor düzey

1. Modüllerdeki toplam okunmamış bildirim sayısını `reduce` ile hesaplayın.
2. Eksik `contact` alanı bulunan profil nesnesinde optional chaining ve nullish coalescing kullanarak güvenli e-posta metni üretin.
3. Promise döndüren sahte bir `fetchEventsMock` fonksiyonu yazın. `async/await` kullanarak etkinlik sayısını yazdırın.
4. Duyuru listesini önce aktif duyurulara filtreleyen, sonra başlıklarını büyük harfe dönüştüren ve en sonunda virgülle birleştiren zincirleme bir ifade yazın.

### Hata ayıklama alıştırması

Aşağıdaki kodda beklenen çıktı alınamıyorsa nedeni açıklayın ve düzeltin:

```javascript
const events = [
  { title: "Seminer", isOnline: true },
  { title: "Atölye", isOnline: false }
];

const onlineTitles = events.filter((event) => {
  event.isOnline;
}).map((event) => {
  event.title;
});

console.log(onlineTitles);
```

Beklenen sonuç, yalnızca çevrim içi etkinlik başlıklarını içeren bir dizidir.

## 2.15 Haftalık laboratuvar / proje görevi

Bu haftaki laboratuvar görevi, KampüsHub projesinin veri altyapısını hazırlamaktır. Öğrenci, Vite ile oluşturulmuş KampüsHub projesinde `src/data` klasörünü oluşturmalı ve aşağıdaki veri dosyalarını tasarlamalıdır:

```text
src/data/announcements.js
src/data/events.js
src/data/modules.js
src/data/profile.js
```

Görev adımları:

1. `announcements.js` dosyasında en az dört duyuru nesnesi içeren bir dizi oluşturun.
2. Her duyuru nesnesinde `id`, `courseCode`, `title`, `summary` ve `isPinned` alanları bulunsun.
3. `events.js` dosyasında en az üç etkinlik nesnesi oluşturun.
4. Her etkinlikte `id`, `title`, `date`, `location` ve `category` alanları bulunsun.
5. `modules.js` dosyasında KampüsHub ana modüllerini temsil eden kart verileri bulunsun.
6. Her modülde `id`, `title`, `description`, `isActive` ve `unreadCount` alanları yer alsın.
7. `profile.js` dosyasında tek bir kullanıcı profil nesnesi oluşturun.
8. Ayrı bir deneme dosyasında bu verileri kullanarak aktif modülleri, sabitlenmiş duyuruları ve toplam okunmamış bildirim sayısını hesaplayın.
9. Veriyi doğrudan değiştiren örneklerden kaçının; güncelleme gereken durumlarda spread ile yeni kopya üretin.
10. Kodunuzu Node.js ile çalıştırarak en az üç beklenen çıktıyı terminalde doğrulayın.

Değerlendirme ölçütleri:

| Ölçüt | Beklenen düzey |
|---|---|
| Veri modeli | Nesne ve dizi alanları tutarlı, okunabilir ve KampüsHub bağlamına uygun |
| ES6+ kullanımı | `const`, template literal, destructuring, spread ve dizi metotları doğru kullanılmış |
| Mutasyonsuz yaklaşım | Var olan veri doğrudan değiştirilmemiş, yeni kopyalar üretilmiş |
| Kod okunabilirliği | Değişken adları anlamlı, dosya düzeni sade |
| Test edilebilirlik | Kod Node.js ile çalıştırıldığında beklenen çıktılar alınabiliyor |

## 2.16 İleri okuma ve bir sonraki bölüme geçiş

Bu bölümde modern JavaScript kavramlarını React’e hazırlık amacıyla öğrendik. Bir sonraki bölümde HTML ve CSS’ten bileşen düşüncesine geçeceğiz. Orada arayüzü tek büyük sayfa olarak değil; başlık, kart, liste, profil özeti ve içerik alanı gibi küçük parçalara ayırmayı tartışacağız. Bu ayrım, Bölüm 4’te JSX ve bileşen anatomisine geçerken KampüsHub arayüzünü daha düzenli kurmamızı sağlayacaktır.

Bir sonraki bölüme geçmeden önce şu kontrol listesini tamamlayın:

- `const` ve `let` arasındaki farkı açıklayabiliyorum.
- Template literal ile dinamik metin üretebiliyorum.
- Nesne ve dizi destructuring sözdizimini okuyabiliyorum.
- Spread ile yeni nesne veya dizi kopyası oluşturabiliyorum.
- `map`, `filter`, `find`, `some` ve `reduce` metotlarının temel amacını biliyorum.
- `async/await` kullanılan basit bir kodu okuyabiliyorum.
- KampüsHub için temel veri dosyalarını tasarlayabiliyorum.
- Kod örneklerinde `CODE_META` bloğunun kod bloğundan önce yer alması gerektiğini biliyorum.

### Programatik ekran çıktısı planı

<!-- SCREENSHOT_META
id: b02_01_es6_console_ciktisi
chapter_id: chapter_02
title_key: es6_console_output
route: /__book__/chapter_02/es6-console
waitFor: "[data-book-shot='es6-console']"
actions: []
output: workspace/react/assets/screenshots/b02_01_es6_console_ciktisi.png
manual_path: assets/manual/screenshots/b02_01_es6_console_ciktisi.png
final_path: assets/final/screenshots/b02_01_es6_console_ciktisi.png
manual_override: true
-->

<!-- SCREENSHOT_META
id: b02_02_kampushub_veri_modeli
chapter_id: chapter_02
title_key: kampushub_data_model
route: /__book__/chapter_02/data-model
waitFor: "[data-book-shot='data-model']"
actions: []
output: workspace/react/assets/screenshots/b02_02_kampushub_veri_modeli.png
manual_path: assets/manual/screenshots/b02_02_kampushub_veri_modeli.png
final_path: assets/final/screenshots/b02_02_kampushub_veri_modeli.png
manual_override: true
-->

<!-- SCREENSHOT_META
id: b02_03_modul_kartlari_onizleme
chapter_id: chapter_02
title_key: module_cards_preview
route: /__book__/chapter_02/module-cards
waitFor: "[data-book-shot='module-cards']"
actions: []
output: workspace/react/assets/screenshots/b02_03_modul_kartlari_onizleme.png
manual_path: assets/manual/screenshots/b02_03_modul_kartlari_onizleme.png
final_path: assets/final/screenshots/b02_03_modul_kartlari_onizleme.png
manual_override: true
-->

| id | Şekil | Başlık | Route | waitFor | Çıktı | Markdown hedefi |
|---|---|---|---|---|---|---|
| `b02_01_es6_console_ciktisi` | Şekil 2.1 | ES6 örneklerinin konsol çıktısı | `/__book__/chapter_02/es6-console` | `[data-book-shot='es6-console']` | `workspace/react/assets/screenshots/b02_01_es6_console_ciktisi.png` | `[SCREENSHOT:b02_01_es6_console_ciktisi]` |
| `b02_02_kampushub_veri_modeli` | Şekil 2.2 | KampüsHub veri modelinin görsel özeti | `/__book__/chapter_02/data-model` | `[data-book-shot='data-model']` | `workspace/react/assets/screenshots/b02_02_kampushub_veri_modeli.png` | `[SCREENSHOT:b02_02_kampushub_veri_modeli]` |
| `b02_03_modul_kartlari_onizleme` | Şekil 2.3 | Modül kartlarının statik önizlemesi | `/__book__/chapter_02/module-cards` | `[data-book-shot='module-cards']` | `workspace/react/assets/screenshots/b02_03_modul_kartlari_onizleme.png` | `[SCREENSHOT:b02_03_modul_kartlari_onizleme]` |

### Bir sonraki bölüme geçiş

Bölüm 3’te HTML ve CSS bilgisini React’in bileşen düşüncesine bağlayacağız. KampüsHub veri modelini artık daha görünür arayüz parçalarına dönüştürmeye başlayacağız. Böylece Bölüm 4’te JSX ve bileşen anatomisi, yalnızca yeni bir sözdizimi olarak değil; bu bölümde hazırlanan veriyi arayüze taşıyan doğal bir adım olarak anlaşılacaktır.
