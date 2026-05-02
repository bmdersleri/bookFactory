# Parametric Computer Book Factory - Detayli Proje Dokumantasyonu

Bu belge, BookFactory reposunun amacini, mimarisini, calisma akisini, CLI/Studio yuzeylerini, manifest modelini, kalite kapilarini ve gelistirme pratiklerini tek yerde aciklar.

Belge ozellikle v3.8.0 sürümü için hazırlanmış olup, akıllı dizgi (Smart Layout) ve modüler yayıncılık mimarisini temel alır.

## 1. Projenin Amaci

Parametric Computer Book Factory, teknik ders kitabi uretimini standart, izlenebilir ve tekrar uretilebilir hale getirmek icin gelistirilen Python tabanli bir frameworktur.

Temel hedef, LLM destekli kitap uretimini serbest metin uretiminden cikarip manifest, bolum plani, kod dogrulama, test raporlari, gorsel/screenshot plani, QR/GitHub entegrasyonu ve export hattiyla yonetilebilir bir uretim sistemine donusturmektir.

## 2. Temel Tasarim Ilkeleri

### Manifest tek dogruluk kaynagidir
`book_manifest.yaml`, kitap yapisi ve uretim kararlarinin merkezidir. Tüm süreçler bu dosyaya sadık kalarak işletilir.

### Modüler Servis Mimarisi (v3.8+)
Monolitik yapı yerine, her biri spesifik bir alandan sorumlu servis katmanları kullanılır:
- **ManifestService:** Manifest IO, doğrulama ve normalizasyon.
- **PathService:** Merkezi yol çözümü ve güvenli dizin yönetimi.
- **HealthService:** Proje sağlığı, test raporları ve snapshot üretimi.
- **PromptService:** LLM prompt yönetimi ve RAG enjeksiyonu.
- **AssetService:** Medya kütüphanesi ve görsel optimizasyonu.
- **CodeService:** Markdown içindeki kod bloklarının cerrahi yönetimi.

### Windows ve PowerShell uyumlulugu
Path, encoding, PowerShell ve UTF-8 davranislari Windows ortamı için optimize edilmiştir.

## 3. Paket ve Entry Point Yapisi

```toml
[project]
name = "bookfactory"
version = "3.8.0"
```

Komut entry pointleri:
- `bookfactory`: Ana CLI paketi.
- `bookfactory-studio`: FastAPI tabanlı akıllı üretim merkezi (GUI).

## 4. Ana Klasorler

```text
bookfactory/                  Python CLI paketi
bookfactory_studio/           FastAPI tabanlı Studio GUI
bookfactory_studio/services/  Modüler iş mantığı servisleri
tools/                        Uretim, kalite, kod ve export araclari
tools/memory/                 ChromaDB tabanlı RAG motoru
tools/indexing/               Glossary ve Index jeneratörleri
tools/l10n/                   Çok dilli çeviri araçları
tools/quality/                Akıllı denetim (Consistency Audit) araçları
schemas/                      Manifest ve CODE_META JSON semalari
docs/                         Teknik dokümantasyon
```

## 5. Studio GUI ve Kullanıcı Deneyimi (UX Mastery)

Studio v3.8, profesyonel yazarlar için "Sürtünmesiz" (Frictionless) bir çalışma ortamı sunar:

- **Görsel Komuta Merkezi:** Dashboard üzerinde tamamlanma oranını gösteren grafikler ve bölüm sağlık ısı haritası.
- **Markdown Yazım Toolbarı:** Kalın, eğik, tablo ve link ekleme butonları ile hızlandırılmış yazım.
- **CODE_META Sihirbazı:** Form üzerinden hatasız metadata blokları üretimi.
- **Medya Kütüphanesi:** Sürükle-bırak görsel yönetimi ve otomatik Markdown link üretimi.
- **In-Studio Debugging:** Hatalı kod bloklarını Studio içinden düzenleme ve anlık test etme (IDE Mode).

## 6. Güvenlik ve Doğruluk

### Katı Manifest Kontrolü (Strict Manifest Guard)
Studio, geçerli bir manifest olmayan dizinlerde çalışmayı reddederek veri bütünlüğünü korur.

### Semantik Tutarlılık Denetimi (Consistency Audit)
RAG altyapısını kullanarak bölümler arası terminoloji ve kod modeli çelişkilerini yapay zeka ile tespit eder.

## 7. Yayıncılık ve Digital Twin

- **Digital Twin (Web Release):** Kitabın MkDocs tabanlı profesyonel bir web sitesi olarak tek tıkla yayınlanması (`dist/web_site/`).
- **Syllabus & Index:** Akademik standartlarda Ders İzlence Formu ve Terimler İndeksi üretimi.

## 8. Akıllı Dizgi (Smart Layout)

### Akıllı QR Yerleşimi
Okunabilirliği artırmak için kısa kod bloklarına QR kod eklenmesi otomatik olarak filtrelenir.
- **Eşik Değeri:** Varsayılan olarak 15 satır altındaki kod bloklarına QR eklenmez.
- **Denetim:** `CODE_META` içinde `qr: force` kullanılarak bu kural aşılabilir.
- **Ayarlar:** Manifest üzerinden `qr_threshold_lines` ile global eşik değiştirilebilir.

## 10. Guncel v3.8.0 Durumu

Tamamlanan ana isler:
- v3.8 Smart Layout: Akıllı QR yerleşimi ve dizgi iyileştirmeleri.
- v3.7 Pedagogical Excellence: Bloom Taksonomisi ve Editör denetimi.
- v3.6 UX Mastery: Görsel Dashboard ve Bildirim sistemi.
- v3.5 Intelligent Quality: RAG, Media Library ve Digital Twin.
- Modüler servis mimarisi ve tam unit test başarısı.

*Belge v3.8.0 sürümü için güncellenmiştir.*
