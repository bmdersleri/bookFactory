# Parametric Computer Book Factory - Detayli Proje Dokumantasyonu

Bu belge, BookFactory reposunun amacini, mimarisini, calisma akisini, CLI/Studio yuzeylerini, manifest modelini, kalite kapilarini ve gelistirme pratiklerini tek yerde aciklar.

Belge ozellikle v3.4.0 sürümü için hazırlanmış olup, yazar odaklı (Author-Centric) ve modüler servis mimarisini temel alır.

## 1. Projenin Amaci

Parametric Computer Book Factory, teknik ders kitabi uretimini standart, izlenebilir ve tekrar uretilebilir hale getirmek icin gelistirilen Python tabanli bir frameworktur.

Temel hedef, LLM destekli kitap uretimini serbest metin uretiminden cikarip manifest, bolum plani, kod dogrulama, test raporlari, gorsel/screenshot plani, QR/GitHub entegrasyonu ve export hattiyla yonetilebilir bir uretim sistemine donusturmektir.

## 2. Temel Tasarim Ilkeleri

### Manifest tek dogruluk kaynagidir
`book_manifest.yaml`, kitap yapisi ve uretim kararlarinin merkezidir. Tüm süreçler bu dosyaya sadık kalarak işletilir.

### Modüler Servis Mimarisi (v3.4+)
Monolitik yapı yerine, her biri spesifik bir alandan sorumlu servis katmanları kullanılır:
- **ManifestService:** Manifest IO, doğrulama ve normalizasyon.
- **PathService:** Merkezi yol çözümü ve güvenli dizin yönetimi.
- **HealthService:** Proje sağlığı, test raporları ve snapshot üretimi.
- **PromptService:** LLM prompt yönetimi ve RAG enjeksiyonu.

### Windows ve PowerShell uyumlulugu
Path, encoding, PowerShell ve UTF-8 davranislari Windows ortamı için optimize edilmiştir.

## 3. Paket ve Entry Point Yapisi

```toml
[project]
name = "bookfactory"
version = "3.4.0"
```

Komut entry pointleri:
- `bookfactory`: Ana CLI paketi.
- `bookfactory-studio`: FastAPI tabanlı modern GUI.

## 4. Ana Klasorler

```text
bookfactory/                  Python CLI paketi
bookfactory_studio/           FastAPI tabanlı Studio GUI
bookfactory_studio/services/  Modüler iş mantığı servisleri
tools/                        Uretim, kalite, kod ve export araclari
tools/memory/                 ChromaDB tabanlı RAG motoru
tools/indexing/               Glossary ve Index jeneratörleri
tools/l10n/                   Çok dilli çeviri araçları
schemas/                      Manifest ve CODE_META JSON semalari
docs/                         Teknik dokümantasyon
```

## 5. Studio GUI ve Yazar Odaklı (Author-Centric) Özellikler

Studio v3.4, teknik yazarlar için optimize edilmiş bir çalışma ortamı sunar:

- **Canlı Markdown Önizleme:** Bölüm içeriği yazılırken sağ panelde anlık HTML önizlemesi sunulur.
- **Akıllı Rehber (Smart Guide):** "Sırada Ne Var?" kartı ile kullanıcıya projenin durumuna göre bir sonraki adımı önerir.
- **Project Switcher:** Son çalışılan projeler arasında hızlı geçiş imkanı.
- **Gece Modu (Dark Mode):** Uzun süreli yazım seansları için göz yorgunluğunu azaltan tema.
- **Klavye Kısayolları:** 
    - `Alt + [1-7]`: Paneller arası geçiş.
    - `Ctrl + S`: Manifest kaydetme.
    - `Ctrl + Enter`: Üretim adımını çalıştırma.

## 6. Güvenlik: Katı Manifest Kontrolü (Strict Manifest Guard)

Studio, geçerli bir `book_manifest.yaml` dosyası olmayan dizinlerde işlem yapılmasına izin vermez. Kullanıcıyı otomatik olarak "Yeni Proje Başlatma Sihirbazı"na veya proje seçimine yönlendirir.

## 7. Manifest ve Akademik Standartlar

### Akademik Blok (`academic`)
Müfredat uyumu için `course_code`, `ects_credits`, `learning_outcomes` ve `weekly_schedule_mapping` alanlarını içerir. Bu verilerle otomatik **Syllabus (Ders İzlence Formu)** üretilir.

### Sözlük ve Dizin (`glossary`)
Manifestte tanımlanan terimler, tüm bölümlerde taranarak otomatik **Terimler Sözlüğü (Glossary)** ve **Dizin (Index)** dosyalarına (`exports/indexing/`) dönüştürülür.

## 8. Görsel Otomasyon

- **Dinamik Grafik Yakalama:** Python kodlarındaki Matplotlib çıktılarını headless (Agg) modda yakalayıp Markdown'a enjekte eder.
- **UI Screenshot:** Flutter integration testleri üzerinden emülatörden otomatik ekran görüntüsü alır ve `[SCREENSHOT:id]` markerları ile eşleştirir.

## 9. RAG Tabanlı Bağlam Belleği (Context Memory)

ChromaDB ve `all-MiniLM-L6-v2` modeli kullanılarak bölümler vektör veritabanına indekslenir. Yeni prompt üretimlerinde "Human-in-the-Loop" akışına önceki bölümlerdeki teknik bağlam (kod stili, veri yapıları) otomatik hatırlatıcı olarak eklenir.

## 10. Guncel v3.4.0 Durumu

Tamamlanan ana isler:
- RAG ve Bağlam Belleği entegrasyonu.
- Modüler servis mimarisine geçiş (Refactoring).
- Akademik Syllabus ve Glossary/Index otomasyonu.
- Gelişmiş Studio UX (Live Preview, Dark Mode, Switcher).
- Tam otomatik görsel yakalama (Plots & Screenshots).
- Sürüm birliği ve 13/13 Studio test başarısı.

*Belge v3.4.0 sürümü için güncellenmiştir.*
