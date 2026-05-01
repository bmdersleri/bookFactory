---
title: "Bölüm 4: JSX ve Bileşen Anatomisi"
chapter_id: "chapter_04"
content_language: "tr-TR"
book_title: "React ile Web Uygulama Geliştirme"
author: "Prof. Dr. İsmail KIRBAŞ"
main_project: "KampüsHub"
numbering_policy: "manual_visible_for_current_pipeline"
automation_profile: "parametric_computer_book_factory_v2_0"
code_policy: "CODE_META blocks precede executable JavaScript fences"
screenshot_policy: "SCREENSHOT_META plus [SCREENSHOT:*] markers"
---

# Bölüm 4: JSX ve Bileşen Anatomisi

## 4.1 Bölümün yol haritası

Bu bölümde React uygulamalarında arayüz yazmanın temel biçimi olan JSX ele alınacaktır. İlk bakışta HTML’e çok benzeyen JSX, aslında JavaScript içinde arayüz tanımlamayı mümkün kılan özel bir sözdizimidir. Bu nedenle JSX’i yalnızca “HTML’i JavaScript dosyasına yazmak” şeklinde görmek eksik ve çoğu zaman yanıltıcıdır. JSX, bileşen tabanlı düşünmeyi görünür hâle getirir; veriyi, arayüzü ve küçük sorumluluk parçalarını aynı zihinsel model içinde birleştirir.

Bölümün temel akışı şu sorular etrafında kurulacaktır:

- JSX nedir ve React projelerinde neden kullanılır?
- JSX ile HTML arasındaki farklar nelerdir?
- Fonksiyon bileşeni hangi parçalardan oluşur?
- `className`, tek kök eleman, self-closing tag ve fragment hangi problemlere çözüm üretir?
- JavaScript ifadeleri JSX içinde nasıl kullanılır?
- KampüsHub ana ekranı küçük bileşenlere nasıl ayrılır?

Bu bölümün sonunda KampüsHub projesi, tek parça ekran fikrinden çıkıp daha düzenli bir bileşen ağacına kavuşacaktır. Henüz `useState`, `useEffect`, React Router veya API bağlantısı kullanılmayacaktır. Ama bu bölümde kurulacak bileşen anatomisi, Bölüm 5’te işlenecek `props` ve veri akışı konusunun doğrudan temelini oluşturacaktır.

## 4.2 Bölümün konumu ve pedagojik rolü

Önceki bölümlerde üç önemli hazırlık yapılmıştı. Bölüm 1’de modern web uygulamalarının SPA yaklaşımı, React ekosistemi, Node.js, npm, Vite, HMR, React DevTools, `npm create vite@latest`, `npm install`, `npm run dev`, `package.json`, `index.html`, `main.jsx` ve `App.jsx` gibi temel kavramlar tanıtıldı. Bölüm 2’de React kodlarını anlamak için gerekli modern JavaScript ES6+ kavramları ele alındı. Bölüm 3’te ise HTML ve CSS ile yazılmış bir sayfanın bileşen adaylarına nasıl ayrılabileceği tartışıldı.

Bölüm 4 bu üç hazırlığı bir araya getirir. Öğrenci artık yalnızca HTML/CSS parçası görmeyecek; aynı arayüzü React bileşeni olarak düşünmeye başlayacaktır. Bu geçiş, React öğreniminde kritik bir eşiktir. Çünkü React’te başarılı olmak, yalnızca sözdizimini ezberlemekle değil, arayüzü küçük, anlamlı ve tekrar kullanılabilir bileşenlere ayırmakla mümkündür.

Bu bölümde amaç, öğrencinin JSX’i mekanik olarak yazması değil, JSX’in neden böyle davrandığını anlamasıdır. Örneğin `class` yerine `className` yazılması basit bir isim değişikliği değildir; JSX’in JavaScript’e yakın doğasını gösteren önemli bir ipucudur. Benzer şekilde bir bileşenin tek kök eleman döndürmesi, React’in arayüz ağacını tutarlı biçimde kurabilmesiyle ilgilidir.

## 4.3 Öğrenme çıktıları

Bu bölümü tamamlayan bir öğrenci aşağıdaki yeterlikleri kazanmış olmalıdır:

1. JSX’in HTML olmadığını, JavaScript içinde arayüz tanımlama sözdizimi olduğunu açıklar.
2. JSX ile HTML arasındaki temel farkları örnekler üzerinden karşılaştırır.
3. `className`, fragment, self-closing tag ve tek kök eleman kurallarını doğru uygular.
4. Basit bir fonksiyon bileşeninin ad, gövde, dönüş değeri ve export parçalarını ayırt eder.
5. JSX içinde JavaScript ifadelerini `{}` kullanarak gösterir.
6. Koşullu görünüm ve liste üretimi için başlangıç düzeyinde doğru JSX kalıplarını tanır.
7. KampüsHub arayüzünü `Header`, `HeroSection`, `DashboardPreview`, `ModuleCard` ve `Footer` gibi bileşenlere ayırır.
8. Bileşen adlandırma ve dosya adlandırma kararlarını tutarlı biçimde verir.
9. JSX kaynaklı yaygın hata mesajlarını çözümleyerek düzeltme önerisi üretir.

Bu çıktılar özellikle uygulamalı derslerde önemlidir. Çünkü öğrencinin sonraki bölümlerde `props`, `state`, `useEffect`, React Router ve form yönetimi gibi konuları sağlıklı öğrenebilmesi için önce bileşenin yapısını güvenle okuyabilmesi gerekir.

## 4.4 Ön bilgi ve başlangıç varsayımları

Bu bölümde öğrencinin temel HTML etiketlerini, CSS sınıf mantığını ve modern JavaScript sözdizimini bildiği varsayılır. Özellikle `const`, arrow function, template literal, dizi `map` metodu ve nesne özelliklerine erişim bu bölümde sık kullanılacaktır. Bu kavramlar Bölüm 2’de ayrıntılı biçimde ele alındığı için burada tekrar ana konu yapılmayacaktır.

Ayrıca öğrencinin Vite ile oluşturulmuş bir React projesinde şu dosyaların temel rolünü bilmesi beklenir:

| Dosya | Rolü |
|---|---|
| `index.html` | React uygulamasının bağlanacağı kök HTML dosyasıdır. |
| `src/main.jsx` | React uygulamasını DOM içindeki kök elemana bağlar. |
| `src/App.jsx` | Başlangıç uygulama bileşenidir. |
| `src/App.css` | Uygulama düzeyinde stillerin yazılabileceği CSS dosyasıdır. |

Bölümde kullanılan örnekler KampüsHub projesi üzerinden ilerleyecektir. KampüsHub; ders duyuruları, etkinlik takvimi, not paylaşımı ve kullanıcı profili modüllerinden oluşan kümülatif bir React uygulamasıdır. Bu bölümde söz konusu modüller henüz dinamik veriyle çalışmayacak; fakat bileşen yapısı sonraki bölümlerde genişletilebilecek biçimde kurulacaktır.

## 4.5 JSX nedir?

JSX, JavaScript dosyası içinde arayüz yapısını tanımlamaya yarayan bir sözdizimidir. JSX yazarken HTML’e benzeyen etiketler kullanırız; ancak yazdığımız şey doğrudan tarayıcıya gönderilen klasik HTML değildir. Vite ve React derleme süreci, JSX kodunu tarayıcının anlayabileceği JavaScript çağrılarına dönüştürür. Bu nedenle JSX, React bileşenlerinin ne göstereceğini ifade eden okunabilir bir arayüz tanımı olarak düşünülebilir.

Basit bir JSX örneği şu şekildedir:

```jsx
function WelcomeMessage() {
  return <h2>KampüsHub'a hoş geldiniz</h2>;
}
```

Bu örnekte `WelcomeMessage` bir fonksiyon bileşenidir. Fonksiyonun dönüş değeri JSX’tir. JSX, ekranda bir `h2` başlığı oluşacağını ifade eder. Ancak burada kritik nokta şudur: JSX, JavaScript fonksiyonunun dönüş değeri olarak yazılır. Bu durum, React’te arayüzün veri ve mantıkla aynı bileşen sınırı içinde düşünülmesini sağlar.

JSX’in en önemli yararı, arayüzü bileşenler hâlinde yazmayı kolaylaştırmasıdır. Klasik HTML sayfasında tüm yapı tek dosyada büyüyebilir. React’te ise her anlamlı arayüz parçası bir fonksiyon bileşenine dönüştürülebilir. Örneğin KampüsHub için başlık alanı, kahraman alanı, modül kartı ve alt bilgi alanı ayrı bileşenler olabilir.

```jsx
function App() {
  return (
    <main>
      <Header />
      <HeroSection />
      <DashboardPreview />
      <Footer />
    </main>
  );
}
```

Bu kod parçası HTML’e benzer görünür; fakat aslında `Header`, `HeroSection`, `DashboardPreview` ve `Footer` gibi özel React bileşenlerini kullanır. Bu özel bileşenler büyük harfle başlar. React, küçük harfle başlayan etiketleri HTML etiketi; büyük harfle başlayanları ise kullanıcı tanımlı bileşen olarak yorumlar.

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
  - "Aktif modül: Duyurular"
timeout_sec: 5
github: true
qr: dual
-->
```javascript
const appName = "KampüsHub";
const activeModule = "Duyurular";

function renderTitle(name, moduleName) {
  return `${name} | Aktif modül: ${moduleName}`;
}

console.log(renderTitle(appName, activeModule));
```

Bu test edilebilir örnek doğrudan JSX kullanmaz; çünkü mevcut otomatik test hattı Node.js üzerinde saf JavaScript kodlarını çalıştırır. Ancak örnek, JSX içindeki ifade mantığını anlamaya yardımcı olur. Gerçek JSX içinde aynı değerler `{appName}` veya `{activeModule}` biçiminde arayüze yerleştirilebilir.

```jsx
function PageTitle() {
  const appName = "KampüsHub";
  const activeModule = "Duyurular";

  return (
    <h2>
      {appName} | Aktif modül: {activeModule}
    </h2>
  );
}
```

Burada süslü parantezler, JSX içinde JavaScript ifadesi çalıştırmak için kullanılır. Bu ifade bir değişken, fonksiyon çağrısı, template literal sonucu veya dizi `map` çıktısı olabilir. Ancak JSX içine doğrudan `if` bloğu gibi statement yazılmaz; ifade döndüren yapılar tercih edilir.

## 4.6 JSX ile HTML arasındaki farklar

JSX HTML’e benzediği için yeni başlayan öğrenciler çoğu zaman ikisini aynı kabul eder. Bu benzerlik öğrenmeyi kolaylaştırır; ancak bazı farklar gözden kaçırılırsa hata mesajlarıyla karşılaşılır. Bu bölümde en sık karşılaşılan farklar ele alınacaktır.

İlk önemli fark `class` yerine `className` kullanılmasıdır. HTML’de CSS sınıfı vermek için `class` niteliği kullanılır. JSX’te ise `class`, JavaScript’te ayrılmış bir kelime olduğu için `className` tercih edilir.

```jsx
function Header() {
  return <header className="site-header">KampüsHub</header>;
}
```

İkinci önemli fark, etiketlerin kapatılmasıdır. HTML’de bazı etiketler kapatılmadan kullanılabilir. JSX’te ise self-closing etiketler açıkça kapatılmalıdır.

```jsx
function UserAvatar() {
  return <img src="/avatar.png" alt="Kullanıcı profil görseli" />;
}
```

Üçüncü fark, bileşenin tek bir kök yapı döndürmesi gerekliliğidir. Aşağıdaki kullanım hatalıdır; çünkü `Header` ve `main` yan yana iki kök eleman olarak döndürülmektedir.

```jsx
function App() {
  return (
    <Header />
    <main>KampüsHub içerik alanı</main>
  );
}
```

Bu durumda bir kapsayıcı eleman veya fragment kullanılmalıdır.

```jsx
function App() {
  return (
    <>
      <Header />
      <main>KampüsHub içerik alanı</main>
    </>
  );
}
```

Fragment, gereksiz DOM elemanı oluşturmadan birden fazla JSX parçasını tek kök altında toplamak için kullanılır. Bu yaklaşım özellikle semantik HTML düzeninin bozulmaması gereken durumlarda yararlıdır.

Dördüncü fark, bazı nitelik adlarının JavaScript adlandırma biçimine yaklaşmasıdır. Örneğin HTML’de `for` olarak yazılan label bağlantısı JSX’te `htmlFor` olur. Inline style ise string değil, nesne olarak verilir.

```jsx
function SearchLabel() {
  return (
    <label htmlFor="campus-search" style={{ fontWeight: "bold" }}>
      KampüsHub içinde ara
    </label>
  );
}
```

Inline style bu bölümde yalnızca tanıtım düzeyinde kullanılmalıdır. Kitap genelinde okunabilirlik için çoğu stil `className` ve CSS dosyaları üzerinden verilecektir.

| HTML yaklaşımı | JSX yaklaşımı | Açıklama |
|---|---|---|
| `class="card"` | `className="card"` | CSS sınıfı JSX’te `className` ile yazılır. |
| `<img>` | `<img />` | Boş etiketler kapatılır. |
| `for="id"` | `htmlFor="id"` | Label bağlantısı JavaScript uyumlu adla yazılır. |
| `style="color:red"` | `style={{ color: "red" }}` | Inline style nesne olarak verilir. |
| Çoklu kök | Fragment veya kapsayıcı | Bileşen tek kök yapı döndürmelidir. |

<!-- CODE_META
id: react_ch04_code02
chapter_id: chapter_04
language: javascript
kind: example
title_key: "component_return_model"
file: "component_return_model.js"
extract: true
test: compile_run_assert
expected_stdout_contains:
  - "Header bileşeni"
  - "PascalCase"
timeout_sec: 5
github: true
qr: dual
-->
```javascript
function createComponentDescription(componentName, role) {
  const startsWithUppercase = /^[A-Z]/.test(componentName);
  const namingRule = startsWithUppercase ? "PascalCase" : "küçük harfle başlamış";

  return `${componentName} bileşeni ${role}. Adlandırma: ${namingRule}`;
}

console.log(createComponentDescription("Header", "uygulama başlığını temsil eder"));
```

Bu örnek, bileşen adlarının neden büyük harfle başladığını vurgular. React’te `header` küçük harfle yazıldığında HTML etiketi olarak algılanır. `Header` ise geliştiricinin tanımladığı özel bileşendir.

## 4.7 Fonksiyon bileşeninin anatomisi

React’te modern başlangıç yaklaşımı fonksiyon bileşenleriyle çalışmaktır. Fonksiyon bileşeni, arayüzün belirli bir parçasını döndüren JavaScript fonksiyonudur. Basit bir bileşenin temel anatomisi şu parçalardan oluşur:

1. Bileşen adı
2. Fonksiyon gövdesi
3. Gerekli yerel sabitler veya yardımcı hesaplamalar
4. `return` ifadesi
5. JSX çıktısı
6. Dışa aktarma biçimi

Aşağıdaki örnek, KampüsHub için sade bir `Header` bileşenidir:

```jsx
function Header() {
  return (
    <header className="app-header">
      <p className="app-eyebrow">Üniversite yaşam asistanı</p>
      <h1>KampüsHub</h1>
    </header>
  );
}

export default Header;
```

Bu bileşende `Header` adı PascalCase biçimindedir. Fonksiyon herhangi bir parametre almadan statik bir JSX çıktısı üretmektedir. `return` içinde bir `header` etiketi vardır. Bu `header` etiketi küçük harfle başladığı için HTML semantik etiketi olarak yorumlanır. Buna karşılık `Header` fonksiyon adı büyük harfle başladığı için React bileşeni olarak kullanılır.

Bir bileşen başka bileşenleri kullanabilir. Bu yaklaşım bileşen ağacını oluşturur.

```jsx
function App() {
  return (
    <main className="app-shell">
      <Header />
      <HeroSection />
      <DashboardPreview />
    </main>
  );
}
```

Burada `App` üst bileşendir. `Header`, `HeroSection` ve `DashboardPreview` alt bileşenlerdir. React uygulaması büyüdükçe her bileşenin sorumluluğunu küçük tutmak okunabilirliği artırır. Tek bir `App.jsx` dosyası içinde yüzlerce satır JSX yazmak kısa vadede hızlı görünse de uzun vadede bakım zorluğu doğurur.

Bileşen anatomisini anlamak için şu kontrol soruları kullanılabilir:

- Bileşenin adı arayüzdeki sorumluluğunu anlatıyor mu?
- Bileşen tek bir kavramsal işi mi yapıyor?
- Bileşen gereğinden fazla HTML/CSS ayrıntısı içeriyor mu?
- Bileşen ileride `props` ile veri alabilecek biçimde tasarlanmış mı?
- Bileşen başka sayfalarda tekrar kullanılabilir mi?

Bu bölümde henüz `props` ayrıntısına girilmeyecektir. Fakat bileşenlerin ileride dışarıdan veri alacak şekilde düşünülmesi önemlidir. Örneğin `ModuleCard` bileşeni şimdilik statik metinle yazılabilir; ancak Bölüm 5’te `title`, `description` ve `status` gibi değerleri `props` üzerinden alacaktır.

## 4.8 JSX içinde ifade, koşul ve liste mantığı

JSX’in güçlü yönlerinden biri, JavaScript ifadelerini arayüz içine kontrollü biçimde yerleştirmesidir. Bir ifade, değer üreten JavaScript parçasıdır. Değişken okumak, fonksiyon çağırmak, ternary operatörü kullanmak veya `map` ile dizi dönüştürmek JSX içinde sık görülen ifade örnekleridir.

Basit ifade kullanımı şu şekildedir:

```jsx
function WelcomePanel() {
  const studentName = "Ayşe";
  const unreadAnnouncements = 3;

  return (
    <section className="welcome-panel">
      <h2>Merhaba, {studentName}</h2>
      <p>Okunmamış duyuru sayısı: {unreadAnnouncements}</p>
    </section>
  );
}
```

Bu örnekte `{studentName}` ve `{unreadAnnouncements}` JSX içine yerleştirilen JavaScript ifadeleridir. Süslü parantezin içinde değer döndüren ifade bulunur. Ancak aşağıdaki gibi doğrudan `if` bloğu yazılmaz:

```jsx
function WrongExample() {
  const isActive = true;

  return <p>{if (isActive) { "Aktif" }}</p>;
}
```

Bunun yerine ternary operatörü veya önceden hesaplanmış değişken kullanılabilir.

```jsx
function StatusText() {
  const isActive = true;

  return <p>{isActive ? "Aktif" : "Pasif"}</p>;
}
```

Liste üretimi için JavaScript’in `map` metodu kullanılır. Bu konu Bölüm 2’de JavaScript düzeyinde görülmüştü. React’te `map`, veri dizisini JSX parçası dizisine dönüştürmek için sık kullanılır.

```jsx
function ModuleList() {
  const modules = ["Duyurular", "Etkinlikler", "Not Paylaşımı", "Profil"];

  return (
    <ul>
      {modules.map((moduleName) => (
        <li key={moduleName}>{moduleName}</li>
      ))}
    </ul>
  );
}
```

Burada `key` niteliği önemlidir. React listelerde hangi elemanın değiştiğini anlayabilmek için kararlı bir anahtara ihtiyaç duyar. Bu bölümde `key` konusu başlangıç düzeyinde tanıtılmalı, ayrıntılı liste güncelleme senaryoları sonraki bölümlere bırakılmalıdır.

<!-- CODE_META
id: react_ch04_code03
chapter_id: chapter_04
language: javascript
kind: example
title_key: "module_card_summary"
file: "module_card_summary.js"
extract: true
test: compile_run_assert
expected_stdout_contains:
  - "Duyurular: 4 yeni kayıt"
  - "Profil: 1 yeni kayıt"
timeout_sec: 5
github: true
qr: dual
-->
```javascript
const modules = [
  { title: "Duyurular", newItems: 4 },
  { title: "Etkinlikler", newItems: 2 },
  { title: "Not Paylaşımı", newItems: 7 },
  { title: "Profil", newItems: 1 },
];

const summaries = modules.map((moduleItem) => {
  return `${moduleItem.title}: ${moduleItem.newItems} yeni kayıt`;
});

console.log(summaries.join("\n"));
```

Bu test edilebilir JavaScript örneği, JSX içinde kullanılacak `map` mantığının temelini gösterir. Aynı veri React bileşeninde `ModuleCard` üretmek için kullanılabilir:

```jsx
function DashboardPreview() {
  const modules = [
    { title: "Duyurular", newItems: 4 },
    { title: "Etkinlikler", newItems: 2 },
    { title: "Not Paylaşımı", newItems: 7 },
    { title: "Profil", newItems: 1 },
  ];

  return (
    <section className="dashboard-preview">
      {modules.map((moduleItem) => (
        <article className="module-card" key={moduleItem.title}>
          <h3>{moduleItem.title}</h3>
          <p>{moduleItem.newItems} yeni kayıt</p>
        </article>
      ))}
    </section>
  );
}
```

Koşullu sınıf adı üretimi de JSX içinde sık görülür. Örneğin önemli duyurular için farklı CSS sınıfı eklemek gerekebilir.

<!-- CODE_META
id: react_ch04_code04
chapter_id: chapter_04
language: javascript
kind: example
title_key: "conditional_classname"
file: "conditional_classname.js"
extract: true
test: compile_run_assert
expected_stdout_contains:
  - "announcement-card announcement-card--urgent"
  - "announcement-card"
timeout_sec: 5
github: true
qr: dual
-->
```javascript
function getAnnouncementClassName(isUrgent) {
  const baseClass = "announcement-card";
  return isUrgent ? `${baseClass} ${baseClass}--urgent` : baseClass;
}

console.log(getAnnouncementClassName(true));
console.log(getAnnouncementClassName(false));
```

Bu mantık JSX içinde şu şekilde kullanılabilir:

```jsx
function AnnouncementCard() {
  const isUrgent = true;
  const className = isUrgent
    ? "announcement-card announcement-card--urgent"
    : "announcement-card";

  return (
    <article className={className}>
      <h3>Ders programı güncellendi</h3>
      <p>Yeni derslik bilgilerini kontrol ediniz.</p>
    </article>
  );
}
```

Bu bölümde koşullu görünüm ve liste üretimi yalnızca temel düzeyde ele alınır. Amaç, öğrencinin JSX içinde JavaScript ifadelerinin nasıl yer aldığını görmesidir. Daha karmaşık etkileşimler `state`, `effect` ve veri akışı bölümlerinde geliştirilecektir.

## 4.9 KampüsHub bileşen iskeleti

KampüsHub arayüzü bu bölümde ilk kez gerçek bir bileşen iskeletine dönüştürülecektir. Bölüm 3’te semantik HTML ve CSS üzerinden belirlenen arayüz bölgeleri, artık React bileşenleri hâline getirilecektir. İlk hedef, çalışan ve okunabilir bir statik arayüz kurmaktır.

Önerilen klasör yapısı şu şekildedir:

```text
src/
  App.jsx
  App.css
  main.jsx
  components/
    Header.jsx
    HeroSection.jsx
    DashboardPreview.jsx
    ModuleCard.jsx
    Footer.jsx
```

Bu yapı küçük bir proje için yeterince anlaşılırdır. Daha büyük projelerde `components`, `features`, `pages` ve `shared` gibi ayrımlar yapılabilir; ancak bu kitapta aşamalı öğrenme amacıyla sade bir klasör düzeni tercih edilecektir.

KampüsHub için başlangıç `App.jsx` dosyası şu şekilde düşünülebilir:

```jsx
import "./App.css";
import Header from "./components/Header";
import HeroSection from "./components/HeroSection";
import DashboardPreview from "./components/DashboardPreview";
import Footer from "./components/Footer";

function App() {
  return (
    <div className="app-shell">
      <Header />
      <main>
        <HeroSection />
        <DashboardPreview />
      </main>
      <Footer />
    </div>
  );
}

export default App;
```

Bu örnekte `App` bileşeni ekranın bütün ayrıntılarını bilmek zorunda değildir. Onun görevi ana bileşenleri doğru sırayla yerleştirmektir. Bu yaklaşım, uygulama büyüdükçe `App.jsx` dosyasının okunabilir kalmasını sağlar.

`Header.jsx` dosyası şu şekilde yazılabilir:

```jsx
function Header() {
  return (
    <header className="app-header">
      <a className="app-logo" href="/">
        KampüsHub
      </a>
      <nav className="app-nav" aria-label="Ana menü">
        <a href="#announcements">Duyurular</a>
        <a href="#events">Etkinlikler</a>
        <a href="#notes">Notlar</a>
        <a href="#profile">Profil</a>
      </nav>
    </header>
  );
}

export default Header;
```

Bu bileşen henüz React Router kullanmaz. Bağlantılar sayfa içi örnek bağlantılar olarak yazılmıştır. React Router Bölüm 10’da ayrıntılı olarak ele alınacaktır.

`HeroSection.jsx` dosyası uygulamanın tanıtıcı alanını temsil eder:

```jsx
function HeroSection() {
  return (
    <section className="hero-section">
      <p className="hero-kicker">Öğrenci odaklı dijital kampüs paneli</p>
      <h2>Ders, etkinlik ve not akışını tek ekranda takip edin.</h2>
      <p>
        KampüsHub; duyuruları, yaklaşan etkinlikleri, ders notlarını ve profil
        bilgilerini düzenli bir arayüzde birleştirir.
      </p>
    </section>
  );
}

export default HeroSection;
```

`DashboardPreview` ve `ModuleCard` bileşenleri bu bölümde statik olarak yazılabilir. Bölüm 5’te `ModuleCard` bileşenine `props` aktarılacaktır.

```jsx
function ModuleCard() {
  return (
    <article className="module-card">
      <h3>Duyurular</h3>
      <p>Ders ve bölüm duyurularını takip edin.</p>
      <span>4 yeni kayıt</span>
    </article>
  );
}

export default ModuleCard;
```

```jsx
import ModuleCard from "./ModuleCard";

function DashboardPreview() {
  return (
    <section className="dashboard-preview" aria-labelledby="dashboard-title">
      <h2 id="dashboard-title">KampüsHub modülleri</h2>
      <div className="module-grid">
        <ModuleCard />
        <ModuleCard />
        <ModuleCard />
      </div>
    </section>
  );
}

export default DashboardPreview;
```

Bu örnekte üç `ModuleCard` aynı içeriği gösterir. Bu durum bilinçli olarak bırakılmıştır; çünkü Bölüm 5’te aynı bileşene farklı `props` değerleri verilecek ve her kart farklı görünecektir. Böylece öğrenci, `props` konusuna gerçek bir ihtiyaç üzerinden geçecektir.

KampüsHub bileşen ağacı şu şekilde özetlenebilir:

<!-- CODE_META
id: react_ch04_code05
chapter_id: chapter_04
language: javascript
kind: example
title_key: "component_tree_summary"
file: "component_tree_summary.js"
extract: true
test: compile_run_assert
expected_stdout_contains:
  - "App > Header"
  - "Toplam bileşen: 7"
timeout_sec: 5
github: true
qr: dual
-->
```javascript
const componentTree = {
  name: "App",
  children: [
    { name: "Header", children: [] },
    { name: "HeroSection", children: [] },
    {
      name: "DashboardPreview",
      children: [
        { name: "ModuleCard", children: [] },
        { name: "ModuleCard", children: [] },
      ],
    },
    { name: "Footer", children: [] },
  ],
};

function flattenTree(node, parentPath = "") {
  const currentPath = parentPath ? `${parentPath} > ${node.name}` : node.name;
  const childPaths = node.children.flatMap((child) => flattenTree(child, currentPath));
  return [currentPath, ...childPaths];
}

const paths = flattenTree(componentTree);
console.log(paths.join("\n"));
console.log(`Toplam bileşen: ${paths.length}`);
```

Bu saf JavaScript örneği, bileşen ağacını veri yapısı olarak düşünmeyi sağlar. React DevTools kullanıldığında benzer bir hiyerarşi görsel olarak incelenebilir. Bu nedenle bileşenleri anlamlı isimlerle ayırmak yalnızca kod okunabilirliği için değil, hata ayıklama deneyimi için de önemlidir.

## 4.10 Sık yapılan hatalar ve yanlış sezgiler

### 4.10.1 JSX’i doğrudan HTML sanmak

JSX’in HTML’e benzemesi öğrenmeyi kolaylaştırır; ancak JSX bir JavaScript sözdizimi uzantısıdır. Bu nedenle `class`, `for`, kapanmayan etiketler ve çoklu kök eleman gibi HTML’de tolere edilebilen bazı kullanımlar JSX’te sorun çıkarır. Öğrenci, JSX yazarken HTML bilgisini kullanmalı; fakat JavaScript bağlamında yazdığını unutmamalıdır.

### 4.10.2 Bileşen adını küçük harfle başlatmak

React’te özel bileşen adları büyük harfle başlamalıdır. `moduleCard` veya `dashboardPreview` gibi isimler JavaScript fonksiyonu olarak çalışabilir; fakat JSX içinde bileşen gibi kullanıldığında doğru yorumlanmayabilir. Doğru yaklaşım `ModuleCard` ve `DashboardPreview` biçimidir.

### 4.10.3 Gereğinden büyük bileşen yazmak

Yeni başlayanlar çoğu zaman tüm ekranı `App.jsx` içinde yazmaya çalışır. Bu yaklaşım kısa örneklerde kabul edilebilir görünse de gerçek uygulamalarda bakım zorluğu üretir. Bir bileşen çok fazla sorumluluk taşıyorsa bölünmelidir. KampüsHub örneğinde `Header`, `HeroSection`, `DashboardPreview` ve `Footer` ayrımı bu nedenle yapılmaktadır.

### 4.10.4 `return` sonrasında satır kırılımı hatası yapmak

JavaScript’te `return` ifadesinden hemen sonra satır sonu gelirse otomatik noktalı virgül ekleme davranışı beklenmeyen sonuç doğurabilir. JSX döndürürken parantez kullanmak güvenli ve okunabilir bir yaklaşımdır.

```jsx
function Header() {
  return (
    <header className="app-header">
      KampüsHub
    </header>
  );
}
```

### 4.10.5 Liste üretirken `key` kullanmayı unutmak

Dizi `map` ile JSX listesi üretildiğinde her üst düzey öğeye `key` verilmelidir. `key`, React’in liste elemanlarını kararlı biçimde takip etmesini sağlar. Bu bölümde ayrıntılı algoritmik açıklamaya girilmese de öğrenci `key` uyarısını ciddiye almalıdır.

### 4.10.6 CSS sınıfını koşullu üretirken okunabilirliği kaybetmek

JSX içinde çok karmaşık ternary ifadeleri yazmak kodu zor okunur hâle getirebilir. Böyle durumlarda sınıf adını `return` öncesinde bir değişkende hesaplamak daha anlaşılırdır.

## 4.11 Hata ayıklama egzersizi

Aşağıdaki bileşen kodunda birden fazla JSX hatası bulunmaktadır. Önce kodu okuyun, ardından hataları belirleyin.

```jsx
function campusHeader() {
  return (
    <header class="app-header">
      <img src="/logo.png">
      <h1>KampüsHub</h1>
    </header>
    <main>Hoş geldiniz</main>
  );
}
```

Bu kodda en az dört temel sorun vardır:

1. Bileşen adı küçük harfle başlamaktadır; `campusHeader` yerine `CampusHeader` kullanılmalıdır.
2. JSX’te `class` yerine `className` yazılmalıdır.
3. `img` etiketi self-closing biçimde kapatılmalıdır.
4. Bileşen iki kök eleman döndürmektedir; fragment veya kapsayıcı kullanılmalıdır.

Düzeltilmiş sürüm şu şekilde olabilir:

```jsx
function CampusHeader() {
  return (
    <>
      <header className="app-header">
        <img src="/logo.png" alt="KampüsHub logosu" />
        <h1>KampüsHub</h1>
      </header>
      <main>Hoş geldiniz</main>
    </>
  );
}
```

Bu düzeltmede ayrıca `img` etiketi için `alt` metni eklenmiştir. Bu, erişilebilirlik açısından önemlidir. React öğrenirken erişilebilirlik ayrıntılarını başlangıçtan itibaren doğru alışkanlık hâline getirmek gerekir.

Mini hata ayıklama görevi olarak öğrenciden aşağıdaki adımları yapması istenebilir:

- Kodda JSX kurallarına aykırı satırları işaretleyin.
- Her hata için bir cümlelik açıklama yazın.
- Bileşen adını PascalCase biçimine dönüştürün.
- Gerekirse fragment kullanın.
- `className` ve self-closing tag düzeltmelerini yapın.
- Kodun hangi dosyada tutulacağını belirtin.

## 4.12 Bölüm özeti ve terim sözlüğü

Bu bölümde JSX’in React arayüz geliştirmedeki temel rolü incelendi. JSX’in HTML’e benzediği, fakat JavaScript içinde çalışan özel bir arayüz tanımlama sözdizimi olduğu vurgulandı. `className`, self-closing tag, fragment, tek kök eleman ve süslü parantezle ifade kullanımı gibi temel kurallar açıklandı.

Fonksiyon bileşeninin anatomisi; bileşen adı, fonksiyon gövdesi, `return` ifadesi, JSX çıktısı ve export yapısı üzerinden ele alındı. KampüsHub projesi için `App`, `Header`, `HeroSection`, `DashboardPreview`, `ModuleCard` ve `Footer` bileşenlerinden oluşan başlangıç iskeleti önerildi. Bu iskelet, sonraki bölümde `props` ile veri aktarımı yapmaya uygun biçimde tasarlandı.

### Terim sözlüğü

| Terim | Açıklama |
|---|---|
| JSX | JavaScript içinde arayüz yapısını tanımlamak için kullanılan sözdizimi. |
| Fonksiyon bileşeni | JSX döndüren ve arayüzün belirli bir parçasını temsil eden JavaScript fonksiyonu. |
| PascalCase | Bileşen adlarında kullanılan, her kelimenin büyük harfle başladığı adlandırma biçimi. |
| `className` | JSX içinde CSS sınıfı tanımlamak için kullanılan nitelik. |
| Fragment | Gereksiz DOM elemanı üretmeden birden fazla JSX parçasını sarmalayan yapı. |
| Self-closing tag | İçeriği olmayan etiketlerin `<img />` gibi kapatılmış biçimi. |
| JSX expression | JSX içinde `{}` kullanılarak yerleştirilen JavaScript ifadesi. |
| Bileşen ağacı | React bileşenlerinin üst-alt ilişkisini gösteren hiyerarşik yapı. |
| `key` | Liste üretiminde React’in öğeleri takip etmesine yardımcı olan kararlı anahtar. |

## 4.13 Kavramsal sorular

1. JSX neden doğrudan HTML olarak değerlendirilmemelidir?
2. React’te özel bileşen adlarının büyük harfle başlamasının nedeni nedir?
3. `class` ile `className` arasındaki fark JSX bağlamında nasıl açıklanır?
4. Fragment hangi durumda kapsayıcı `div` kullanımına göre daha uygun olabilir?
5. Bir bileşenin tek kök yapı döndürmesi neden beklenir?
6. JSX içinde JavaScript ifadesi yazmak için neden `{}` kullanılır?
7. `map` ile liste üretirken `key` kullanımının amacı nedir?
8. KampüsHub ana ekranında `ModuleCard` bileşeninin ayrı yazılması hangi bakım avantajlarını sağlar?
9. `App.jsx` dosyasında tüm arayüzü yazmak ile küçük bileşenlere ayırmak arasında ne fark vardır?
10. Bu bölümde `props` ayrıntısına girilmemesinin pedagojik gerekçesi ne olabilir?

## 4.14 Programlama alıştırmaları

### Kolay düzey

1. `WelcomeBanner` adlı bir bileşen yazın. Bileşen `KampüsHub'a hoş geldiniz` metnini bir `section` içinde göstersin.
2. Aşağıdaki HTML parçasını JSX’e dönüştürün: `div`, `class`, `img` ve `label for` kullanımlarına dikkat edin.
3. `Header` bileşeninde `nav` içinde dört bağlantı oluşturun: Duyurular, Etkinlikler, Notlar ve Profil.

### Orta düzey

1. `ModuleCard` adlı bir bileşen oluşturun. Şimdilik statik olarak `Duyurular`, `4 yeni kayıt` ve kısa açıklama göstersin.
2. `DashboardPreview` bileşeni içinde üç adet `ModuleCard` kullanın. Kartların aynı görünmesi bu aşamada sorun değildir.
3. `HeroSection` bileşeninde bir başlık, bir açıklama ve bir çağrı metni oluşturun. CSS sınıflarını `className` ile verin.

### Zor düzey

1. Bir modül dizisini `map` ile `article` elemanlarına dönüştüren bir JSX örneği yazın. Her öğeye kararlı bir `key` verin.
2. `isUrgent` değişkenine göre duyuru kartının CSS sınıfını değiştiren bir bileşen yazın.
3. `App.jsx` dosyasını `Header`, `HeroSection`, `DashboardPreview` ve `Footer` bileşenlerini kullanacak biçimde düzenleyin.

### Hata ayıklama alıştırması

Aşağıdaki sorunları içeren bir bileşen oluşturun ve sonra düzeltin:

- Bileşen adı küçük harfle başlıyor.
- `class` kullanılmış.
- `img` etiketi kapatılmamış.
- İki kök eleman yan yana döndürülmüş.
- Liste öğelerinde `key` yok.

Düzeltmeden sonra her değişikliğin neden gerekli olduğunu kısa yorumlarla açıklayın.

## 4.15 Haftalık laboratuvar / proje görevi

Bu haftanın laboratuvar görevi, KampüsHub ana ekranını JSX ve fonksiyon bileşenleriyle statik olarak kurmaktır. Amaç, henüz dinamik veri yönetimine geçmeden önce bileşen sınırlarını doğru belirlemektir.

### Görev 1: Klasör yapısını oluşturma

Projenizde `src/components` klasörünü oluşturun. Aşağıdaki dosyaları ekleyin:

```text
src/components/Header.jsx
src/components/HeroSection.jsx
src/components/DashboardPreview.jsx
src/components/ModuleCard.jsx
src/components/Footer.jsx
```

### Görev 2: Bileşenleri yazma

Her dosyada aynı adla başlayan bir fonksiyon bileşeni oluşturun. Bileşenleri `export default` ile dışa aktarın. Bileşen adlarının PascalCase olmasına dikkat edin.

### Görev 3: `App.jsx` içinde bileşenleri birleştirme

`App.jsx` dosyasında bileşenleri import edin ve doğru sırayla kullanın. `App` bileşeni yalnızca ana düzeni kurmalı; ayrıntılı kart içerikleri alt bileşenlerde yer almalıdır.

### Görev 4: Basit stil ekleme

`App.css` dosyasında şu sınıflar için temel stiller yazın:

```text
app-shell
app-header
app-nav
hero-section
dashboard-preview
module-grid
module-card
app-footer
```

Stillerin amacı görsel mükemmellik değil, bileşen sınırlarını görünür hâle getirmektir. Responsive davranış için `module-grid` alanında basit `grid` veya `flex` düzeni kullanılabilir.

### Görev 5: Kontrol listesi

Teslimden önce şu maddeleri kontrol edin:

- Her bileşen PascalCase adlandırılmış mı?
- JSX içinde `className` kullanılmış mı?
- Self-closing etiketler doğru kapatılmış mı?
- Her bileşen tek kök yapı döndürüyor mu?
- `App.jsx` dosyası aşırı büyümeden ana düzen rolünde kalmış mı?
- KampüsHub modülleri ekranda anlaşılır biçimde görünüyor mu?
- React DevTools içinde bileşen ağacı okunabiliyor mu?

### Teslim formatı

Öğrenci şu çıktıları teslim etmelidir:

1. `src/components` klasör ekran görüntüsü
2. `App.jsx` dosyası
3. En az üç bileşen dosyası
4. Uygulama ekran görüntüsü
5. Kısa açıklama: “Bu bileşenleri neden bu şekilde ayırdım?”

## 4.16 İleri okuma ve bir sonraki bölüme geçiş

Bu bölümden sonra öğrencinin React belgelerinde özellikle JSX, rendering lists ve conditional rendering başlıklarını incelemesi yararlı olacaktır. Ayrıca erişilebilir HTML ve semantik yapı konularının React bileşenleri içinde de geçerliliğini koruduğu unutulmamalıdır.

Bu bölümde `ModuleCard` bileşeni statik yazıldı. Aynı kartın birden fazla yerde kullanılması, fakat her seferinde aynı içeriği göstermesi doğal olarak bir soruna işaret eder. Gerçek uygulamada her kart farklı başlık, açıklama, durum ve sayaç bilgisi göstermelidir. İşte bu ihtiyaç Bölüm 5’in ana konusudur: `props`.

Bölüm 5’te bileşenler arası veri akışı ele alınacak, `ModuleCard` bileşeni dışarıdan veri alan yeniden kullanılabilir bir yapıya dönüştürülecektir. Böylece KampüsHub arayüzü statik bileşenlerden veriyle beslenen esnek bileşenlere doğru ilerleyecektir.

### Programatik ekran çıktısı planı

Aşağıdaki ekran çıktıları, bölümün görsel doğrulama ve otomatik üretim hattı için planlanmıştır.

<!-- SCREENSHOT_META
id: b04_01_jsx_ifade_modeli
chapter_id: chapter_04
title_key: "jsx_ifade_modeli"
route: /__book__/chapter-04/jsx-ifade-modeli
waitFor: ".jsx-expression-demo"
actions: []
output: assets/auto/screenshots/b04_01_jsx_ifade_modeli.png
manual_path: assets/manual/screenshots/b04_01_jsx_ifade_modeli.png
final_path: assets/final/screenshots/b04_01_jsx_ifade_modeli.png
manual_override: true
-->
[SCREENSHOT:b04_01_jsx_ifade_modeli]

Bu ekran çıktısı, JSX içinde değişken ve ifade kullanımını gösteren küçük bir KampüsHub başlık panelini belgelemek için kullanılacaktır.

<!-- SCREENSHOT_META
id: b04_02_kampushub_bilesen_agaci
chapter_id: chapter_04
title_key: "kampushub_bilesen_agaci"
route: /__book__/chapter-04/kampushub-bilesen-agaci
waitFor: ".component-tree-demo"
actions: []
output: assets/auto/screenshots/b04_02_kampushub_bilesen_agaci.png
manual_path: assets/manual/screenshots/b04_02_kampushub_bilesen_agaci.png
final_path: assets/final/screenshots/b04_02_kampushub_bilesen_agaci.png
manual_override: true
-->
[SCREENSHOT:b04_02_kampushub_bilesen_agaci]

Bu ekran çıktısı, `App`, `Header`, `HeroSection`, `DashboardPreview`, `ModuleCard` ve `Footer` ilişkisini görselleştiren bileşen ağacı demosu için planlanmıştır.

<!-- SCREENSHOT_META
id: b04_03_modul_kartlari_jsx
chapter_id: chapter_04
title_key: "modul_kartlari_jsx"
route: /__book__/chapter-04/modul-kartlari-jsx
waitFor: ".module-grid"
actions: []
output: assets/auto/screenshots/b04_03_modul_kartlari_jsx.png
manual_path: assets/manual/screenshots/b04_03_modul_kartlari_jsx.png
final_path: assets/final/screenshots/b04_03_modul_kartlari_jsx.png
manual_override: true
-->
[SCREENSHOT:b04_03_modul_kartlari_jsx]

Bu ekran çıktısı, KampüsHub modül kartlarının JSX ile nasıl düzenlendiğini göstermek için kullanılacaktır.

### Bölüm sonu kontrol listesi

- JSX’in HTML’den farkları açıklanabiliyor.
- `className`, fragment ve self-closing tag kullanımı doğru uygulanabiliyor.
- Fonksiyon bileşeni anatomisi okunabiliyor.
- KampüsHub ana ekranı küçük bileşenlere ayrılabiliyor.
- JSX içinde ifade, koşul ve liste mantığı başlangıç düzeyinde kurulabiliyor.
- Bölüm 5’te ele alınacak `props` ihtiyacı gerekçelendirilebiliyor.
