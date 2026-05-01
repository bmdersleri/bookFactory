# BookFactory — React Kitabı Bağlamı

**Modül:** `brief_react_context.md`  
**Yükleme önceliği:** 3 — React kitabıyla çalışılacaksa yükle  
**İlgili modüller:** [`brief_core.md`](brief_core.md), [`brief_standards.md`](brief_standards.md)

---

## 1. Aktif kitap ve çalışma alanı

| Alan | Değer |
|---|---|
| Aktif kitap | React ile Web Uygulama Geliştirme |
| Çalışma klasörü | `workspace/react/` |
| Kümülatif uygulama | KampüsHub |
| Yazar | Prof. Dr. İsmail KIRBAŞ |

**KampüsHub**, üniversite öğrencileri için geliştirilen öğretim amaçlı bir React web uygulamasıdır. Kitap boyunca aşağıdaki modüller kademeli olarak geliştirilir:

- ders duyuruları, etkinlik takvimi, not paylaşımı
- kullanıcı profili, yönlendirme, form yönetimi
- API entegrasyonu, state yönetimi, test
- performans ve dağıtım

---

## 2. React kitabı kapsam politikası

### Kapsam içi teknolojiler

```
React 19 uyumlu modern React yaklaşımı
Fonksiyon bileşenleri ve Hooks
Vite
React Router v7 Declarative Mode
REST API istemci entegrasyonu
TanStack Query
Redux Toolkit
Zustand
React Hook Form
Vitest + React Testing Library + user-event
MSW
```

### Kapsam dışı konular

```
Next.js, SSR/SSG/ISR, React Server Components ana akışı
Server Actions ana akışı
React Native
GraphQL / Apollo / Relay
İleri TypeScript
Backend endpoint yazımı
Veritabanı / ORM / migration
Docker / Kubernetes ileri altyapı
Mikro front-end
WebGL / Three.js ileri görselleştirme
```

Kapsam dışı konular yalnızca "ileri okuma", "sonraki adımlar" veya "Kitap 2" bağlamında anılabilir.

---

## 3. Bölüm akışı

| Bölüm | Ana odak |
|---|---|
| 1 | Modern Web'e giriş, geliştirme ortamı, Vite ve KampüsHub iskeleti |
| 2 | React için gerekli modern JavaScript temelleri |
| 3 | HTML/CSS'ten bileşen düşüncesine geçiş |
| 4 | JSX ve render mantığı |
| 5 | Props ve bileşen kompozisyonu |
| 6 | State ve event yönetimi |
| 7 | `useEffect`, yan etkiler ve API'ye hazırlık |
| 8 | Hook kuralları, memoization farkındalığı |
| 9 | Custom hook tasarımı |
| 10 | React Router v7 Declarative Mode |
| 11 | Formlar, validation ve erişilebilirlik |
| 12 | Redux Toolkit |
| 13 | REST API, TanStack Query ve MSW |
| 14 | Zustand ve alternatif state yönetimi |
| 15 | Performans, test ve dağıtım |
| 16 | KampüsHub final entegrasyonu |

---

## 4. Bölüm üretim iş akışı

Bir bölüm üretilirken LLM şu sırayı izlemelidir:

1. İlgili bölüm girdi promptunu oku.
2. Manifest/proje standardı ile karşılaştır.
3. Outline üret veya mevcut outline'ı kontrol et.
4. Kapsam dışı konuları ayıkla.
5. Kod örnekleri, CODE_META, screenshot ve KampüsHub bağlantısını planla.
6. Tam bölüm metnini Pandoc uyumlu Markdown olarak üret.
7. Kod bloklarını test edilebilir metadata ile yaz.
8. Markdown kalite kontrolüne uygun tek H1 ve tutarlı başlık yapısı kullan.
9. Bölüm sonu soruları, alıştırmalar, laboratuvar görevi ve sonraki bölüme köprü ekle.
10. Kod testleri ve Markdown kalite kontrolü için komutları açıkla.

---

## 5. Bölüm 1 durumu

Bölüm 1 ana dosyası:

```
workspace/react/chapters/chapter_01_modern_web_giris.md
```

Bölüm 1 için kod doğrulama hattı çalıştırılmış ve üç `CODE_META` bloğu başarıyla test edilmiştir.

---

## 6. Bölüm 2'ye geçiş kontrol listesi

Bölüm 2'ye geçmeden önce tamamlanması gerekenler:

```
[ ] Bölüm 1 Markdown kalite raporunda FAIL: 0
[ ] Bölüm 1 CODE_META testlerinde Failed: 0
[ ] Kök dizindeki eski Markdown dosyaları arşivlendi
[ ] README.md / SETUP.md / KULLANIM_KILAVUZU.md / LLM_PROJECT_BRIEF.md güncel
[ ] VS Code terminali PowerShell 7 / pwsh kullanıyor
[ ] UTF-8 karakter sorunu kontrol edildi
[ ] workspace/react/build/test_reports altında son raporlar mevcut
[ ] Bölüm 2 için chapter_input veya prompt hazır
```

### Bölüm 2 içerik odağı: React için Modern JavaScript Temelleri

Ele alınması beklenenler:

- `let` / `const`, arrow function, template literal
- destructuring, spread/rest
- array methods: `map`, `filter`, `reduce`, `find`, `some`
- object/array immutability sezgisi
- Promise ve `async/await`
- modül import/export temelleri
- React ile doğrudan bağlantı
- KampüsHub veri yapılarının ilk örnekleri
