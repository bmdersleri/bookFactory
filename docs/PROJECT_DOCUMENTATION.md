# Parametric Computer Book Factory - Detayli Proje Dokumantasyonu

Bu belge, BookFactory reposunun amacini, mimarisini, calisma akisini, CLI/Studio yuzeylerini, manifest modelini, kalite kapilarini ve gelistirme pratiklerini tek yerde aciklar.

Belge ozellikle v3.4.0 stabilizasyon hattinda kullanilmak uzere hazirlanmistir.
 README hizli tanitim ve kullanim icin kalir; bu dosya daha ayrintili teknik referans olarak dusunulmelidir.

## 1. Projenin Amaci

Parametric Computer Book Factory, teknik ders kitabi uretimini standart, izlenebilir ve tekrar uretilebilir hale getirmek icin gelistirilen Python tabanli bir frameworktur.

Temel hedef, LLM destekli kitap uretimini serbest metin uretiminden cikarip manifest, bolum plani, kod dogrulama, test raporlari, gorsel/screenshot plani, QR/GitHub entegrasyonu ve export hattiyla yonetilebilir bir uretim sistemine donusturmektir.

Sistem su sorulara net cevap vermeyi hedefler:

- Kitabin tek dogruluk kaynagi nedir?
- Hangi bolumler var, durumlari nedir?
- Her bolumun Markdown dosyasi var mi?
- Kod bloklari CODE_META standardina uyuyor mu?
- Kod ornekleri calisiyor mu?
- Screenshot, Mermaid, QR ve asset uretimi planli mi?
- DOCX, HTML, EPUB, PDF gibi ciktilar hangi profille uretilecek?
- GUI, CLI ve CI ayni kalite kurallarini okuyabiliyor mu?

## 2. Temel Tasarim Ilkeleri

### Manifest tek dogruluk kaynagidir

`book_manifest.yaml`, kitap yapisi ve uretim kararlarinin merkezidir. Kitap basligi, yazar, dil, bolum listesi, kapsam, otomasyon tercihleri, kalite kapilari, cikti hedefleri ve CI politikalari manifestten okunur.

### Framework koku ile kitap koku ayridir

BookFactory reposu framework kokudur. Belirli bir kitap projesi ise ayri bir kitap kokune sahiptir. Studio ve CLI komutlari aktif kitap kokunu hedef alirken araclari framework kokunden calistirir.

### Windows ve PowerShell uyumlulugu korunur

Repo Windows ortaminda aktif kullanildigi icin path, encoding, PowerShell ve UTF-8 davranislari kritik kabul edilir.

### Buyuk refactor yerine kucuk guvenli adimlar

v3.4.0 stabilizasyon yaklasimi mevcut public API ve klasor yapisini bozmadan, dar kapsamli iyilestirmelerle ilerlemeyi hedefler.

## 3. Paket ve Entry Point Yapisi

Proje Python paketi olarak `pyproject.toml` ile tanimlanir.

Ana paket bilgileri:

```toml
[project]
name = "bookfactory"
version = "2.11.0"
requires-python = ">=3.10"
```

Komut entry pointleri:

```toml
[project.scripts]
bookfactory = "bookfactory.cli:main"
bookfactory-studio = "bookfactory_studio.app:main"
```

## 4. Ana Klasorler

```text
bookfactory/                  Python CLI paketi
bookfactory_studio/           FastAPI tabanli yerel Studio GUI
tools/                        Uretim, kalite, kod, export ve GitHub araclari
tools/memory/                 ChromaDB tabanlı RAG (Bağlam Belleği) motoru
tools/l10n/                   Çok dilli çeviri (Localization) araçları
schemas/                      Manifest ve CODE_META JSON semalari
configs/                      Varsayilan post-production profilleri
docs/                         Kullanici ve gelistirici dokumantasyonu
examples/                     Minimal kitap ve manifest ornekleri
tests/                        Pytest smoke ve Studio testleri
core/                         LLM uretim sozlesmesi ve prompt standartlari
```

## 5. CLI Mimarisi

Onemli komutlar:

```powershell
python -m bookfactory version
python -m bookfactory doctor --soft
python -m bookfactory test-minimal --fail-on-error
python -m bookfactory init      # İnteraktif Proje Başlatma Sihirbazı
```

## 6. Studio GUI Mimarisi

Studio, `bookfactory_studio/` altinda FastAPI tabanli yerel bir web arayuzudur.

### Studio ana panelleri

| Panel | Amac |
|---|---|
| Dashboard | Kitap ozeti, bolum sayisi, manifest durumu ve son raporlar |
| Kontrol Paneli | Proje sagligi, bolum matrisi, kod testleri, screenshot, export ve repair ozeti |
| Yeni Proje Sihirbazı| Adım adım yönlendirme ile yeni `book_manifest.yaml` ve klasör yapısı oluşturma |
| Kitap Sihirbazi | Manifest/kitap mimarisi icin LLM promptu uretimi (RAG desteğiyle) |
| Manifest | Form tabanli akilli manifest editoru |
| Bolumler | Bolum promptlari ve tam metin Markdown importu (RAG desteğiyle) |
| Production | Pipeline adimlarini ve tam uretim hattini calistirma |

## 7. Studio Güvenlik ve Kontrol Katmanı

### Katı Manifest Kontrolü (Strict Manifest Guard)
v3.4.0 sürümüyle birlikte, Studio backend endpoint'leri (Control Panel, Manifest, Reports vb.) çalışmadan önce aktif dizinde geçerli bir `book_manifest.yaml` olup olmadığını kontrol eder.
 Eğer manifest yoksa, sistem işlemlerin yapılmasına izin vermez ve kullanıcıyı "Yeni Proje Başlatma Sihirbazı"na yönlendirir.

## 8. Manifest Sistemi

Manifest, kitap projesinin merkezi konfigurasyonudur.

### Akademik Blok (`academic`)
Üniversite müfredat uyumu için eklenen yeni bloktur:

```yaml
academic:
  course_code: "CENG201"
  course_name: "Nesneye Yönelik Programlama"
  ects_credits: 5
  learning_outcomes:
    - "Dersin temel kazanimlari..."
  weekly_schedule_mapping:
    "Hafta 1": "chapter_01"
```

Bu bilgiler, otomatik **Syllabus (Ders İzlence Formu)** üretimi için kullanılır.

## 9. Kitap Projesi Klasor Modeli

```text
book-root/
  book_manifest.yaml
  chapters/
    en/                       # İngilizce varyasyonlar
    fr/                       # Fransızca varyasyonlar
  assets/
    auto/
      plots/                  # Otomatik üretilen dinamik grafikler
      screenshots/            # Otomatik UI ekran görüntüleri
  exports/
    academic/                 # Syllabus.md çıktısı
```

## 10. Uretim Hatti (Pipeline)

Yeni eklenen pipeline adımları:

| Step | Grup | Islev |
|---|---|---|
| `generate_syllabus` | Akademik | Üniversite standartlarında Syllabus.md üretir |
| `capture_ui_screenshots`| Görsel | UI kodlarından otomatik ekran görüntüsü alır |

## 11. Kod Doğrulama ve Grafik/UI Adaptörleri

### Dinamik Grafik Yakalama (Plot Interception)
Python adaptörü, `expected_plot` tanımlı kodları çalıştırırken arka planda Matplotlib'i headless modda (`Agg`) çalıştırır ve üretilen grafiği otomatik olarak `assets/auto/plots/` dizinine kaydeder. Ardından Markdown dosyasına görsel referansını enjekte eder.

### UI Screenshot Yakalama
- **Flutter Adapter:** `captures_screenshot` tanımlı blokları integration test modunda çalıştırarak emülatör/cihaz üzerinden gerçek ekran görüntülerini yakalar.
- **Marker Eşleşmesi:** Üretilen görseller, Markdown içindeki `[SCREENSHOT:id]` markerları ile otomatik eşleştirilir.

## 12. RAG Tabanlı Bağlam Belleği (Context Memory)

BookFactory v3.4.0, "Human-in-the-Loop" çalışma modelini ChromaDB tabanlı bir RAG (Retrieval-Augmented Generation) sistemiyle güçlendirir.

- **Dizin:** `tools/memory/`
- **Çalışma Prensibi:** 
  1. Tamamlanan bölümler `rag_cli.py index` komutuyla vektör veritabanına kaydedilir.
  2. Yeni bir bölüm veya mimari promptu üretilirken, `rag_query` üzerinden önceki bölümlerdeki ilgili kavramlar (kod stili, veri modelleri vb.) çekilir.
  3. Çekilen bağlam, LLM'e sunulan promptun içine "HATIRLATMA (CONTEXT)" bloğu olarak otomatik enjekte edilir.
- **Avantajı:** LLM'in önceki bölümlerdeki teknik kararları unutmasını engeller ve kitap genelinde tutarlılık sağlar.

## 13. Çok Dilli Akademik Varyasyon (L10n Pipeline)

- **Yapı:** `chapters/{dil_kodu}/` alt klasör mimarisi kullanılır.
- **Prompt Jeneratörü:** `tools/l10n/generate_translation_prompt.py` aracıyla, kod bloklarını (CODE_META) koruyan ve sadece metni akademik dile çeviren "çeviri promptları" üretilir.

## 24. Guncel v3.4.0 Stabilizasyon Durumu

Tamamlanan ana isler:

- **RAG Belleği:** ChromaDB tabanlı bağlam yönetimi entegre edildi.
- **Syllabus Jeneratörü:** Akademik blok ve Syllabus.md üretimi eklendi.
- **UI Screenshot:** Flutter adaptörü ve otomatik görsel yakalama mimarisi kuruldu.
- **Dinamik Grafikler:** Python Matplotlib interception yapısı tamamlandı.
- **Başlatma Sihirbazı:** Studio içi Project Init Wizard ve Strict Manifest Guard eklendi.
- CLI entry point ve `_cli.py` orkestrasyon uyumu duzeltildi.

## 26. Sozluk

| Terim | Anlam |
|---|---|
| RAG | Retrieval-Augmented Generation; bağlam destekli metin üretimi |
| Syllabus | Üniversite standartlarında ders izlence formu |
| Agg Backend | Matplotlib için GUI penceresi açmayan "headless" mod |
| L10n | Localization; yerelleştirme ve çeviri süreci |

*Belge v3.4.0 sürümü için güncellenmiştir.*
