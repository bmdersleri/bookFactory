# BookFactory — Proje Özeti ve Temel İlkeler

**Modül:** `brief_core.md`  
**Yükleme önceliği:** 1 — Her oturumda ilk yükle  
**İlgili modüller:** [`brief_llm_rules.md`](brief_llm_rules.md), [`brief_loading_order.md`](brief_loading_order.md)

---

## 1. Bu proje nedir?

**Parametric Computer Book Factory**, bilgisayar bilimleri, yazılım mühendisliği, veri bilimi, yapay zekâ, web programlama, mobil programlama, IoT ve benzeri teknik alanlarda ders kitabı üretimini standartlaştırmak için geliştirilmiş **manifest tabanlı, LLM destekli, kod doğrulamalı, test raporlu, görsel/screenshot planlı ve post-production uyumlu** bir kitap üretim framework'üdür.

Bu proje, LLM'e yalnızca "bir kitap yaz" demek yerine üretim sürecini aşağıdaki bileşenlerle denetlenebilir hâle getirir:

1. Kitap fikri ve hedef kitlenin netleştirilmesi
2. `book_manifest.yaml` veya proje manifestlerinin hazırlanması
3. Bölüm girdi promptlarının üretilmesi
4. Bölüm outline'larının hazırlanması ve kontrol edilmesi
5. Tam bölüm Markdown metinlerinin üretilmesi
6. Kod bloklarının `CODE_META` ile ayıklanması
7. Kodların otomatik doğrulanması ve test edilmesi
8. Screenshot planlarının `[SCREENSHOT:...]` marker standardıyla tanımlanması
9. Mermaid, asset, QR ve code page üretimlerinin ilişkilendirilmesi
10. GitHub senkronizasyonu ve Codespaces uyumluluğunun yönetilmesi
11. DOCX/HTML/EPUB/PDF gibi yayın çıktılarının hazırlanması
12. Release, dashboard, indeksleme ve kalite raporlarının üretilmesi

---

## 2. Projenin temel amacı

BookFactory şu hedeflere sahiptir:

1. Teknik ders kitabı üretimini manifest, prompt, test ve kalite kapılarıyla standartlaştırmak.
2. LLM destekli üretimi rastgele içerik üretiminden çıkarıp tekrar üretilebilir mühendislik sürecine dönüştürmek.
3. Bölüm metni, kod, görsel, screenshot, QR, GitHub linki ve final yayın çıktısını aynı üretim zincirine bağlamak.
4. Kod örneklerini çalıştırılabilir, ayıklanabilir ve test raporuyla doğrulanabilir hâle getirmek.
5. Öğretim tasarımı, pedagojik akış, erişilebilirlik ve güvenlik notlarını bölüm standardına yerleştirmek.
6. Türkçe içerik üretirken dosya adları, kalıcı ID'ler ve otomasyon anahtarlarını İngilizce tutmak.
7. Post-production sürecini kitap üretiminin doğal parçası yapmak.
8. İnsan editör müdahalesini, özellikle manuel görsel düzenlemelerini ve akademik kalite kararlarını korumak.
9. Windows + PowerShell 7, Python, Node.js, GitHub Codespaces ve Dev Container akışlarıyla uyumlu çalışmak.
10. Gereksiz dosya birikimini raporlama, arşivleme ve kontrollü temizlik betikleriyle yönetmek.

---

## 3. Bu proje ne değildir?

BookFactory:

- Manifest veya proje standardı olmadan rastgele kitap yazdırma aracı **değildir**.
- LLM'in varsayımlarına dayalı otomatik kapsam genişletme sistemi **değildir**.
- Kaynak uydurmaya veya doğrulanmamış teknik iddiaları kesin bilgi gibi yazmaya izin **vermez**.
- Kod bloklarını yalnızca metin olarak gören bir Markdown üreticisi **değildir**; kodlar test hattıyla ilişkilidir.
- Görselleri, screenshot'ları ve QR kodları sonradan elle ilişkilendirilecek kopuk varlıklar olarak **görmez**.
- Kullanıcı onayı olmadan bölümden bölüme geçmeyi veya kapsamı değiştirmeyi normal kabul **etmez**.
- `assets/manual/`, `assets/locked/`, bölüm metinleri ve manifestleri otomatik temizlenebilir geçici dosyalar olarak **değerlendirmez**.

---

## 4. Temel ilke: Manifest ve proje standardı tek doğruluk kaynağıdır

Genel BookFactory üretiminde ana doğruluk kaynağı:

```
book_manifest.yaml
```

React kitabı gibi proje özelinde ek doğruluk kaynakları:

```
workspace/react/
core/
docs/
configs/
manifests/
README.md
SETUP.md
KULLANIM_KILAVUZU.md
LLM_PROJECT_BRIEF.md   ← bu index dosyası
RELEASE_CHECKLIST.md
```

**Dört temel kural:**

```
Eksik bilgi varsa tahmin etme.
Belirsizlik varsa uydurma.
Kritik karar varsa kullanıcıdan onay al.
Teknik bilgi sürüm bağımlıysa resmi kaynakla doğrula.
```

---

## 5. Genel üretim akışı

```
Kitap fikri
   ↓
Project Starter Prompt
   ↓
Netleştirme soruları
   ↓
Manifest / proje standardı
   ↓
Bölüm girdi promptları
   ↓
Outline üretimi → Outline kontrolü
   ↓
Tam bölüm Markdown metni
   ↓
CODE_META ile kod çıkarma → Kod doğrulama ve test
   ↓
Markdown kalite kontrol
   ↓
Screenshot / Mermaid / asset / QR planı
   ↓
GitHub sync / code pages
   ↓
Post-production (DOCX / HTML / EPUB / PDF / ZIP)
```

---

## 6. LLM için kısa görev özeti

> Benim görevim, kullanıcının teknik ders kitabı projesini manifest ve proje standartlarına bağlı bir üretim hattı içinde yürütmek; belirsiz alanları soru sorarak netleştirmek; bölüm girdi promptu, outline, tam metin, kod testi, Markdown kalite kontrolü, screenshot planı, QR/GitHub/code page ve post-production süreçlerini tutarlı biçimde yönetmek; dosya adlarını ve otomasyon kimliklerini İngilizce/ASCII tutmak; içerik dilini proje standardından almak; akademik doğruluk, pedagojik tutarlılık, kod çalışırlığı ve yayın çıktısı kalitesini korumaktır.
