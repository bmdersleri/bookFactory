# Parametric Computer Book Factory - Detayli Proje Dokumantasyonu

Bu belge, BookFactory reposunun amacini, mimarisini, calisma akisini, CLI/Studio yuzeylerini, manifest modelini, kalite kapilarini ve gelistirme pratiklerini tek yerde aciklar.

Belge ozellikle v4.1.0 sürümü için hazırlanmış olup, bulut tabanlı yayıncılık (Cloud-Native Publishing) ve modüler yayıncılık mimarisini temel alır.

## 1. Projenin Amaci

Parametric Computer Book Factory, teknik ders kitabi uretimini standart, izlenebilir ve tekrar uretilebilir hale getirmek icin gelistirilen Python tabanli bir frameworktur.

Temel hedef, LLM destekli kitap uretimini serbest metin uretiminden cikarip manifest, bolum plani, kod dogrulama, test raporlari, gorsel/screenshot plani, QR/GitHub entegrasyonu ve export hattiyla yonetilebilir bir uretim sistemine donusturmektir.

## 2. Temel Tasarim Ilkeleri

### Manifest tek dogruluk kaynagidir
`book_manifest.yaml`, kitap yapisi ve uretim kararlarinin merkezidir. Tüm süreçler bu dosyaya sadık kalarak işletilir.

### Modüler Servis Mimarisi (v4.1+)
Monolitik yapı yerine, her biri spesifik bir alandan sorumlu servis katmanları kullanılır:
- **ManifestService:** Manifest IO, doğrulama ve normalizasyon.
- **PathService:** Merkezi yol çözümü ve güvenli dizin yönetimi.
- **HealthService:** Proje sağlığı, test raporları ve snapshot üretimi.
- **PromptService:** Adaptif prompt üretimi ve fragman birleştirme.
- **AssetService:** Medya kütüphanesi ve veri seti yönetimi.
- **CloudService:** Codespace ve GitHub Actions yapılandırma yönetimi.
- **CodeService:** Kod bloklarının cerrahi yönetimi ve projeli snippetler.

### Windows ve PowerShell uyumlulugu
Path, encoding, PowerShell ve UTF-8 davranislari Windows ortamı için optimize edilmiştir.

## 3. Paket ve Entry Point Yapisi

```toml
[project]
name = "bookfactory"
version = "4.1.0"
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
templates/cloud/              Codespace ve Actions şablonları
core/fragments/               Adaptif prompt talimat blokları
tools/memory/                 ChromaDB tabanlı RAG motoru
tools/indexing/               Glossary ve Index jeneratörleri
tools/l10n/                   Çok dilli çeviri araçları
tools/quality/                Akıllı denetim (Consistency Audit) araçları
schemas/                      Manifest ve CODE_META JSON semalari
docs/                         Teknik dokümantasyon
```

## 5. Studio GUI ve Kullanıcı Deneyimi (v4.1+)

Studio v4.1, modern teknik yazarlar için tam bulut entegrasyonu sunar:

- **GitHub & Cloud Hub:** Codespace ve GitHub Pages kurulumlarını tek tıkla yapma.
- **Görsel Komuta Merkezi:** Dashboard üzerinde tamamlanma oranını gösteren grafikler.
- **Medya ve Veri Kütüphanesi:** Görsellerin ve veri setlerinin yönetimi.
- **Dahili Hata Ayıklama:** Hatalı kod bloklarını Studio içinden düzenleme.

## 6. Bulut Tabanlı Yayıncılık (Cloud-Native)

v4.1 sürümü ile hazırlanan kitaplar bulut ekosistemine tam uyumludur:

- **GitHub Codespaces:** Kitap projesi bulutta anında çalışmaya hazır hale gelir (`.devcontainer`).
- **GitHub Pages Deployment:** Her push işleminde kitap otomatik olarak web sitesine (Digital Twin) dönüştürülür ve yayınlanır.
- **Continuous Validation:** GitHub Actions üzerinden manifest doğruluğu ve kod testleri otomatik olarak her commit'te çalıştırılır.

## 7. Teknik Dikey Özelleştirme

- **Kaynak Takibi:** Veri setlerinin (`resources`) manifest üzerinden yönetimi.
- **Interactive Sandbox:** Kod bloklarından otomatik Google Colab ve Wokwi linkleri üretimi.
- **Comparison Mode:** Diller arası karşılaştırma için yan yana (Side-by-Side) kod görünümü.

## 10. Guncel v4.1.0 Durumu

Tamamlanan ana isler:
- v4.1 Cloud-Native: Codespace, GitHub Actions ve Pages tam entegrasyonu.
- v4.0 Technical Verticalization: Veri seti yönetimi ve Karşılaştırma modu.
- v3.9 Adaptive Intelligence: Dinamik prompt motoru.
- v3.8 Smart Layout: Akıllı QR yerleşimi.
- v3.5-3.7: RAG, Media Library, Pedagogical flow ve UX iyileştirmeleri.

*Belge v4.1.0 sürümü için güncellenmiştir.*
