# Parametric Computer Book Factory - Detayli Proje Dokumantasyonu

Bu belge, BookFactory reposunun amacini, mimarisini, calisma akisini, CLI/Studio yuzeylerini, manifest modelini, kalite kapilarini ve gelistirme pratiklerini tek yerde aciklar.

Belge ozellikle v4.0.0 sürümü için hazırlanmış olup, teknik dikey özelleştirme (Technical Verticalization) ve modüler yayıncılık mimarisini temel alır.

## 1. Projenin Amaci

Parametric Computer Book Factory, teknik ders kitabi uretimini standart, izlenebilir ve tekrar uretilebilir hale getirmek icin gelistirilen Python tabanli bir frameworktur.

Temel hedef, LLM destekli kitap uretimini serbest metin uretiminden cikarip manifest, bolum plani, kod dogrulama, test raporlari, gorsel/screenshot plani, QR/GitHub entegrasyonu ve export hattiyla yonetilebilir bir uretim sistemine donusturmektir.

## 2. Temel Tasarim Ilkeleri

### Manifest tek dogruluk kaynagidir
`book_manifest.yaml`, kitap yapisi ve uretim kararlarinin merkezidir. Tüm süreçler bu dosyaya sadık kalarak işletilir.

### Modüler Servis Mimarisi (v4.0+)
Monolitik yapı yerine, her biri spesifik bir alandan sorumlu servis katmanları kullanılır:
- **ManifestService:** Manifest IO, doğrulama ve normalizasyon.
- **PathService:** Merkezi yol çözümü ve güvenli dizin yönetimi.
- **HealthService:** Proje sağlığı, test raporları ve snapshot üretimi.
- **PromptService:** Adaptif prompt üretimi ve fragman birleştirme.
- **AssetService:** Medya kütüphanesi ve veri seti yönetimi.
- **CodeService:** Kod bloklarının cerrahi yönetimi ve projeli snippetler.

### Windows ve PowerShell uyumlulugu
Path, encoding, PowerShell ve UTF-8 davranislari Windows ortamı için optimize edilmiştir.

## 3. Paket ve Entry Point Yapisi

```toml
[project]
name = "bookfactory"
version = "4.0.0"
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
core/fragments/               Adaptif prompt talimat blokları
tools/memory/                 ChromaDB tabanlı RAG motoru
tools/indexing/               Glossary ve Index jeneratörleri
tools/l10n/                   Çok dilli çeviri araçları
tools/quality/                Akıllı denetim (Consistency Audit) araçları
schemas/                      Manifest ve CODE_META JSON semalari
docs/                         Teknik dokümantasyon
```

## 5. Studio GUI ve Kullanıcı Deneyimi (v4.0+)

Studio v4.0, teknik eğitimciler için optimize edilmiştir:

- **Görsel Komuta Merkezi:** Dashboard üzerinde tamamlanma oranını gösteren grafikler ve bölüm sağlık ısı haritası.
- **Medya ve Veri Kütüphanesi:** Görsellerin yanı sıra CSV, JSON veri setlerini sürükle-bırak ile yönetme.
- **Dahili Hata Ayıklama:** Hatalı kod bloklarını Studio içinden düzenleme (IDE Mode).
- **Akıllı Yazım Toolbarı:** Markdown formatlama ve CODE_META sihirbazı.

## 6. Teknik Dikey Özelleştirme (Technical Verticalization)

v4.0 sürümü, Veri Bilimi ve Programlama dilleri kitapları için özel yetenekler sunar:

- **Kaynak Takibi:** Kitapta kullanılan veri setlerinin (`resources`) manifest üzerinden yönetimi ve otomatik dağıtımı.
- **Interactive Sandbox:** Kod bloklarından otomatik Google Colab ve Wokwi (IoT simülatör) linkleri üretimi.
- **Projeli Snippetler:** Birden fazla kod bloğunun `group_id` ile tek bir proje klasörü olarak paketlenmesi.
- **Comparison Mode:** Diller arası karşılaştırma için yan yana (Side-by-Side) kod görünümü.

## 7. Yayıncılık ve Digital Twin

- **Digital Twin (Web Release):** Kitabın MkDocs tabanlı profesyonel bir web sitesi olarak yayınlanması (`dist/web_site/`).
- **Syllabus & Index:** Akademik standartlarda Ders İzlence Formu ve Terimler İndeksi üretimi.

## 8. Akıllı Dizgi (Smart Layout)

- **Akıllı QR Yerleşimi:** 15 satır altındaki kısa kod bloklarına QR eklenmesini otomatik filtreler.

## 10. Guncel v4.0.0 Durumu

Tamamlanan ana isler:
- v4.0 Technical Verticalization: Veri seti yönetimi, Sandbox ve Karşılaştırma modu.
- v3.9 Adaptive Intelligence: Fragman tabanlı dinamik prompt motoru.
- v3.8 Smart Layout: Akıllı QR yerleşimi ve dizgi iyileştirmeleri.
- v3.7 Pedagogical Excellence: Bloom Taksonomisi ve Editör denetimi.
- v3.6 UX Mastery: Görsel Dashboard ve Bildirim sistemi.
- v3.5 Intelligent Quality: RAG, Media Library ve Digital Twin.

*Belge v4.0.0 sürümü için güncellenmiştir.*
