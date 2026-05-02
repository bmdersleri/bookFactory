# Parametric Computer Book Factory - Detayli Proje Dokumantasyonu

Bu belge, BookFactory reposunun amacini, mimarisini, calisma akisini, CLI/Studio yuzeylerini, manifest modelini, kalite kapilarini ve gelistirme pratiklerini tek yerde aciklar.

Belge ozellikle v3.2 stabilizasyon hattinda kullanilmak uzere hazirlanmistir. README hizli tanitim ve kullanim icin kalir; bu dosya daha ayrintili teknik referans olarak dusunulmelidir.

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

Ornek:

```text
BookFactory/          # framework koku
react-web/            # kitap koku
  book_manifest.yaml
  chapters/
  build/
  assets/
  exports/
```

### Uretim izlenebilir olmalidir

Promptlar, bolum metinleri, kod manifestleri, test raporlari, kalite raporlari ve export ciktilari dosya sisteminde ayrik klasorlerde tutulur.

### Windows ve PowerShell uyumlulugu korunur

Repo Windows ortaminda aktif kullanildigi icin path, encoding, PowerShell ve UTF-8 davranislari kritik kabul edilir.

### Buyuk refactor yerine kucuk guvenli adimlar

v3.2 stabilizasyon yaklasimi mevcut public API ve klasor yapisini bozmadan, dar kapsamli iyilestirmelerle ilerlemeyi hedefler.

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

Bu nedenle:

- `bookfactory` komutu `bookfactory.cli:main` uzerinden baslar.
- `python -m bookfactory` akisi `bookfactory/__main__.py` uzerinden CLI'ya gider.
- Studio komutu `bookfactory_studio.app:main` ile FastAPI/uvicorn sunucusunu baslatir.

## 4. Ana Klasorler

```text
bookfactory/                  Python CLI paketi
bookfactory_studio/           FastAPI tabanli yerel Studio GUI
tools/                        Uretim, kalite, kod, export ve GitHub araclari
schemas/                      Manifest ve CODE_META JSON semalari
configs/                      Varsayilan post-production profilleri
docs/                         Kullanici ve gelistirici dokumantasyonu
examples/                     Minimal kitap ve manifest ornekleri
tests/                        Pytest smoke ve Studio testleri
core/                         LLM uretim sozlesmesi ve prompt standartlari
```

## 5. CLI Mimarisi

CLI katmani iki dosyaya ayrilmistir:

- `bookfactory/cli.py`: public entry point ve init uyumluluk katmani
- `bookfactory/_cli.py`: asil CLI orkestratoru

v3.2 stabilizasyonunda `bookfactory/cli.py`, `init` disindaki komutlari `_cli.py` ana fonksiyonuna devredecek sekilde sade tutulmustur. Boylece public entry point bozulmadan asil komut seti tek orkestratorde toplanir.

Onemli komutlar:

```powershell
python -m bookfactory version
python -m bookfactory doctor --soft
python -m bookfactory test-minimal --fail-on-error
python -m bookfactory init
```

### Lazy import politikasi

`bookfactory.commands.init` importu lazy hale getirilmistir. Bunun nedeni `init` komutunun ek bagimliliklara ihtiyac duyabilmesi, ancak `version`, `doctor` veya `test-minimal` gibi temel komutlarin bu bagimliliklar eksikken de calisabilmesidir.

## 6. Studio GUI Mimarisi

Studio, `bookfactory_studio/` altinda FastAPI tabanli yerel bir web arayuzudur.

Ana dosyalar:

```text
bookfactory_studio/
  app.py              FastAPI endpointleri
  core.py             manifest, proje snapshot, validasyon ve panel mantigi
  jobs.py             uzun sureli production job yonetimi
  static/
    index.html        tek sayfa HTML kabuk
    app.js            frontend durum ve API baglantilari
    styles.css        arayuz stilleri
```

Varsayilan adres:

```text
http://127.0.0.1:8765/
```

Gelistirme veya paralel test icin farkli port da kullanilabilir:

```powershell
.venv\Scripts\python.exe -m uvicorn bookfactory_studio.app:app --host 127.0.0.1 --port 8766
```

### Studio ana panelleri

| Panel | Amac |
|---|---|
| Dashboard | Kitap ozeti, bolum sayisi, manifest durumu ve son raporlar |
| Kontrol Paneli | Proje sagligi, bolum matrisi, kod testleri, screenshot, export ve repair ozeti |
| Kitap Sihirbazi | Manifest/kitap mimarisi icin LLM promptu uretimi |
| Manifest | Form tabanli akilli manifest editoru |
| Bolumler | Bolum promptlari ve tam metin Markdown importu |
| Production | Pipeline adimlarini ve tam uretim hattini calistirma |
| Raporlar | Build/export raporlarini okuma |

## 7. Studio Kontrol Paneli

v3.2 hattinda Studio'yu yalnizca manifest editoru olmaktan cikarip uretim kumanda paneli seviyesine tasimak icin ilk kontrol paneli katmani eklenmistir.

Backend endpoint:

```text
GET /api/control-panel?root=<kitap-koku>
```

Bu endpoint salt-okunur calisir. Production job baslatmaz; mevcut manifest, dosya sistemi, build raporlari, kod test raporu, screenshot markerlari ve export ciktilarindan anlik durum modeli uretir.

Kontrol panelinin ana bloklari:

| Blok | Kaynak | Aciklama |
|---|---|---|
| Proje Sagligi | Manifest, PyYAML, klasorler | Ortam ve temel proje dosyalari kontrol edilir |
| Bolum Durum Matrisi | Manifest, chapters, quality reports, code reports | Her bolum icin taslak, kalite, kod ve screenshot durumu gosterilir |
| Kod Testleri | `build/test_reports/code_test_report.json` | Total/passed/failed/skipped ozeti ve hatali testler gosterilir |
| Gorsel/Screenshot | Markdown markerlari ve `screenshot_plan` | Eksik marker/eksik dosya bilgileri gosterilir |
| Export Gecmisi | `exports/` ve `build/` | DOCX/PDF/EPUB/HTML/ZIP ciktilari listelenir |
| LLM Repair | Basarisiz kod testleri | Hata detayindan otomatik repair promptu olusturulur |

Dogru sekmeyi dogrudan acmak icin:

```text
http://127.0.0.1:8766/#control
```

## 8. Manifest Sistemi

Manifest, kitap projesinin merkezi konfigurasyonudur.

Minimum alanlar:

```yaml
book:
  title: Kitap basligi
  author: Yazar
  year: "2026"

language:
  primary_language: tr
  output_languages:
    - tr

structure:
  chapters:
    - id: chapter_01
      title: Giris
      file: chapter_01_giris.md
      status: planned
```

Kurumsal politika bloklari:

```yaml
schema:
  manifest_version: "1.0"
  bookfactory_min_version: "2.11.0"
  studio_min_version: "3.1.3"

quality_gates:
  require_code_meta: true
  require_code_tests_passed: true
  require_screenshot_plan: true
  require_references: true
  require_outline_compliance: true

outputs:
  docx: true
  pdf: true
  epub: true
  html_site: true

ci:
  enabled: true
  fail_on_code_error: true
  fail_on_missing_screenshot: false
```

Bu bloklarin amaci GUI, CLI ve gelecekteki CI kontrollerinin ayni kurallari okuyabilmesidir.

### Manifest normalizasyonu

`bookfactory_studio.core.normalize_manifest()` su isleri yapar:

- `schema` varsayilanlarini ekler.
- `quality_gates`, `outputs`, `ci` varsayilanlarini ekler.
- Eski `chapters` kok alanini `structure.chapters` altina tasir.
- Eski `output.formats` listesini yeni `outputs` boolean modeline haritalar.
- `project.paths` varsayilanlarini ekler.
- `project.updated_at` alanini gunceller.

### Manifest validasyonu

`validate_manifest()` su siniflarda kontrol yapar:

- Kitap bilgileri
- Dil bilgileri
- Kurumsal boolean politika bloklari
- Proje path guvenligi
- Bolum ID ve dosya adi tutarliligi
- Bolum dosya varligi
- Status degerleri
- Screenshot ve kod politikasi uyarilari

Hatalar kaydi engeller; uyarilar kaydi engellemez fakat kullaniciya gosterilir.

## 9. Kitap Projesi Klasor Modeli

Tipik kitap koku:

```text
book-root/
  book_manifest.yaml
  manifests/
    book_manifest.yaml
  chapters/
    chapter_01_giris.md
  prompts/
    chapter_inputs/
      chapter_01_input.md
  chapter_backups/
  assets/
    auto/
      mermaid/
      qr/
      screenshots/
    manual/
    final/
  build/
    code/
    reports/
    quality_reports/
    test_reports/
    studio_jobs/
  exports/
    docx/
    html/
    epub/
    site/
  configs/
    post_production_profile_studio.yaml
```

`initialize_project()` bu guvenli klasorleri olusturur ve manifesti yazar.

## 10. Uretim Hatti

Studio ve CLI tarafinda kullanilan temel pipeline adimlari:

| Step | Grup | Islev |
|---|---|---|
| `validate_manifest` | Hazirlik | Manifest dogrulama raporu uretir |
| `generate_chapter_prompts` | Hazirlik | Bolum girdi promptlarini uretir |
| `outline_check` | Kalite | Bolum Markdown kalite/outline kontrolu |
| `extract_code` | Kod | CODE_META bloklarini dosyalara cikarir |
| `validate_code` | Kod | Kod manifestini dogrular |
| `test_code` | Kod | Kod orneklerini test eder |
| `mermaid_extract` | Gorsel | Mermaid bloklarini cikarir |
| `mermaid_render` | Gorsel | Mermaid PNG uretir |
| `qr_manifest` | QR | QR manifest uretir |
| `qr_generate` | QR | QR PNG uretir |
| `github_sync` | GitHub | Kodlari GitHub uyumlu yapiya senkronlar |
| `pages_setup` | GitHub | GitHub Pages dosyalarini hazirlar |
| `codespaces_check` | GitHub | Codespaces uygunlugunu kontrol eder |
| `export` | Cikti | DOCX/HTML/EPUB export calistirir |
| `full_production` | Cikti | Tam uretim hattini sirayla calistirir |

`full_production`, varsayilan olarak bir adim basarisiz olursa durur. Bu davranis `stop_on_error` secenegi ile yonetilebilir.

## 11. Kod Dogrulama Sistemi

Kod bloklari Markdown icinde `CODE_META` ile isaretlenir.

Ornek:

```html
<!-- CODE_META
id: chapter_01_code01
chapter_id: chapter_01
language: python
file: hello.py
test: compile_run_assert
expected_stdout_contains:
  - Merhaba
-->
```

Ardindan kod blogu gelir:

```python
print("Merhaba")
```

Kod hattinin temel araclari:

```text
tools/code/extract_code_blocks.py
tools/code/validate_code_meta.py
tools/code/run_code_tests.py
tools/code/generate_llm_repair_prompt.py
```

Desteklenen adapterlar:

```text
tools/code/language_adapters/python_adapter.py
tools/code/language_adapters/javascript_adapter.py
tools/code/language_adapters/java_adapter.py
```

Java adapterinda Windows/Turkce stdout uyumlulugu icin `-Dfile.encoding=UTF-8` kullanilir.

## 12. Markdown Kalite Kontrolu

Kalite kontrol araci:

```text
tools/quality/check_chapter_markdown.py
```

Kontrol ettigi basliklar:

- H1/H2 yapisi
- Bolum ID tutarliligi
- CODE_META varligi ve konumu
- Screenshot markerlari
- Screenshot marker ad standardi
- Kapsam disi teknoloji uyarilari
- Bolum sonu kontrol listesi ve temel ogretim yapisi

Screenshot marker formati:

```text
[SCREENSHOT:b01_01_aciklayici_ad]
```

## 13. Gorsel, Mermaid, QR ve Asset Modeli

Otomatik ve manuel varliklar ayrilir:

```text
assets/
  auto/
    mermaid/
    qr/
    screenshots/
  manual/
  final/
```

Temel ilke: otomasyon `assets/manual/` altindaki dosyalari ezmemelidir. Final cikti icin `assets/final/` tercih edilir.

Ilgili araclar:

```text
tools/postproduction/prepare_mermaid_images.py
tools/postproduction/render_mermaid_png.py
tools/postproduction/build_qr_manifest_from_code_manifest.py
tools/postproduction/generate_qr_codes.py
tools/postproduction/resolve_assets.py
tools/postproduction/inject_qr_references.py
```

## 14. Export ve Post-Production

Export komutu:

```text
tools/export/export_book.py
```

Post-production profilleri:

```text
configs/post_production_profile.template.yaml
configs/post_production_profile_studio.yaml
```

Studio yeni kitap projesi icin minimal profil olusturabilir:

```text
configs/post_production_profile_studio.yaml
```

Tipik cikti klasorleri:

```text
exports/docx/
exports/html/
exports/epub/
exports/site/
```

## 15. GitHub ve Codespaces Entegrasyonu

GitHub araci:

```text
tools/github/sync_code_repository.py
tools/github/render_code_pages.py
tools/github/setup_github_pages.py
```

Codespaces araclari:

```text
tools/cloud/codespaces_check.py
tools/cloud/codespaces_init.py
tools/cloud/write_puppeteer_config.py
```

Bu katman, kitap icindeki kod orneklerini GitHub reposuna aktarilabilir, Pages ile yayinlanabilir ve Codespaces icinde kontrol edilebilir hale getirmeyi hedefler.

## 16. Test ve Kalite Guvencesi

Pytest konfigurasyonu `pyproject.toml` icindedir:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-p no:cacheprovider"
norecursedirs = [
  ".git",
  ".venv",
  "build",
  "dist",
  "pytest-cache-files-*"
]
```

Ana testler:

```text
tests/test_cli_smoke.py
tests/test_studio_gui.py
```

CLI smoke testleri:

- Parser komutlari
- `python -m bookfactory version`
- Public CLI dispatch
- Doctor/test-minimal mock dispatch
- Version metadata ve console script tutarliligi

Studio GUI testleri:

- Health endpoint
- Static shell
- Framework root uyarisi
- Manifest validasyon ve YAML round-trip
- Enterprise manifest bloklari
- Pipeline step listesi
- Frontend route ve DOM ID sozlesmesi
- Control panel snapshot
- Static asset paketleme

Onerilen lokal dogrulama:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
.venv\Scripts\python.exe -m ruff check bookfactory_studio tests\test_studio_gui.py
.venv\Scripts\python.exe -m pytest --basetemp build\pytest-tmp
.venv\Scripts\python.exe tools\check_package_integrity.py .
```

Windows'ta pytest global temp izin sorunlari gorulurse `--basetemp build\pytest-tmp` kullanilmalidir.

## 17. Paket Butunlugu

Paket hijyeni araci:

```text
tools/check_package_integrity.py
```

Kontrol ettigi riskler:

- Yasakli build/cache/bytecode dosyalari
- Paket disi veya yanlis klasorler
- Version tutarliligi
- Console script entry point tutarliligi
- Gerekli dev bagimliliklari

Guncel beklenen sonuc:

```text
No errors found.
No warnings found.
```

## 18. Kurulum

Onerilen Windows kurulumu:

```powershell
cd "C:\OneDrive\OneDrive - mehmetakif.edu.tr\BookFactory"
py -3.14 -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

Genel dogrulama:

```powershell
.venv\Scripts\python.exe -m bookfactory version
.venv\Scripts\python.exe -m bookfactory doctor --soft
.venv\Scripts\python.exe -m bookfactory test-minimal --fail-on-error
```

Studio baslatma:

```powershell
.venv\Scripts\python.exe -m bookfactory_studio.app
```

Alternatif port:

```powershell
.venv\Scripts\python.exe -m uvicorn bookfactory_studio.app:app --host 127.0.0.1 --port 8766
```

## 19. Tipik Kullanim Akislari

### Yeni kitap baslatma

1. Studio'yu ac.
2. Aktif kitap kokunu sec.
3. Kitap Sihirbazi ile mimari promptu uret.
4. Manifest sekmesinde kitap bilgilerini ve bolumleri duzenle.
5. Klasor yapisini olustur.
6. Bolum girdi promptlarini uret.
7. LLM ile bolum tam metinlerini uret.
8. Bolum Markdownlarini ice aktar.
9. Production hattinda kalite ve kod testlerini calistir.
10. Export al.

### Mevcut kitap projesini kontrol etme

1. Studio'da aktif kitap kokunu sec.
2. Dashboard'dan genel durumu kontrol et.
3. Kontrol Paneli sekmesinde proje sagligi ve bolum matrisini incele.
4. Screenshot eksiklerini ve kod test hatalarini ayikla.
5. Raporlar sekmesinden ilgili raporu ac.
6. Hata varsa LLM Repair promptunu kullan.

### CLI ile hizli smoke

```powershell
python -m bookfactory version
python -m bookfactory doctor --soft
python -m bookfactory test-minimal --fail-on-error
```

## 20. LLM ile Calisma Modeli

LLM, serbest uretici degil, manifest ve kalite kapilarina bagli bir uretim ajanidir.

LLM'e verilecek baglam genellikle su kaynaklardan beslenir:

```text
docs/briefs/LLM_PROJECT_BRIEF.md
docs/briefs/brief_core.md
docs/briefs/brief_llm_rules.md
docs/briefs/brief_standards.md
docs/briefs/brief_structure.md
core/00_llm_execution_contract.md
core/03_output_format_standard.md
```

LLM uretiminde korunmasi gerekenler:

- Manifestteki bolum sirasi
- `chapter_id` ve dosya adlari
- CODE_META bloklari
- Screenshot markerlari
- Mermaid/asset/QR planlari
- Kapsam disi teknoloji sinirlari
- Turkce icerik dili ve akademik uslup

## 21. Windows ve Encoding Notlari

Windows ortaminda su riskler ozel olarak izlenir:

- Path icinde bosluk ve Turkce karakter
- PowerShell quoting
- OneDrive path kilitleri
- `C:\Users\...\AppData\Local\Temp\pytest-of-*` izin sorunlari
- cp1254/stdout encoding sorunlari
- Git dubious ownership uyarilari

Oneriler:

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
$env:PYTHONDONTWRITEBYTECODE='1'
```

Git komutlarinda gerekirse:

```powershell
git -c safe.directory='C:/OneDrive/OneDrive - mehmetakif.edu.tr/BookFactory' status
```

## 22. Release Hygiene

Commit oncesi onerilen kontrol listesi:

```powershell
.venv\Scripts\python.exe -m ruff check bookfactory_studio tests\test_studio_gui.py
$env:PYTHONDONTWRITEBYTECODE='1'
.venv\Scripts\python.exe -m pytest --basetemp build\pytest-tmp
.venv\Scripts\python.exe tools\validate_manifest.py manifests\book_manifest.yaml
.venv\Scripts\python.exe tools\check_package_integrity.py .
```

Commit'e dahil edilmemesi gerekenler:

- `__pycache__/`
- `*.pyc`
- `build/pytest-tmp`
- Headless Chrome screenshotlari
- Studio job loglari
- Kullaniciya ait tasinmis veya silinmis dokumanlar, kapsam disi ise

## 23. Public API ve Uyumluluk

Korunmasi gereken yuzeyler:

- `bookfactory = "bookfactory.cli:main"`
- `bookfactory-studio = "bookfactory_studio.app:main"`
- `python -m bookfactory`
- `python -m bookfactory_studio.app`
- `book_manifest.yaml` temel alanlari
- `CODE_META` standardi
- `tools/` komutlarinin mevcut arguman sozlesmeleri

Buyuk refactor yaparken bu yuzeyler icin once smoke test eklenmelidir.

## 24. Guncel v3.2 Stabilizasyon Durumu

Tamamlanan ana isler:

- CLI entry point ve `_cli.py` orkestrasyon uyumu duzeltildi.
- `init` importu lazy hale getirildi.
- Java adapter stdout encoding davranisi UTF-8 ile guclendirildi.
- Pytest smoke testleri eklendi.
- Studio backend/frontend testleri eklendi.
- Package integrity kontrolu guclendirildi.
- Manifest sistemine `schema`, `quality_gates`, `outputs`, `ci` bloklari eklendi.
- Studio kontrol paneli icin `/api/control-panel` snapshot endpointi eklendi.
- Studio arayuzune Kontrol Paneli sekmesi eklendi.

Son dogrulama hedefi:

```text
pytest: 20 passed
ruff: All checks passed
package integrity: No errors/warnings
```

## 25. Yakin Yol Haritasi

Onerilen sonraki adimlar:

1. Kontrol Paneli verisini CLI komutu olarak da sunmak.
2. Screenshot planini manifest semasinda daha ayrintili hale getirmek.
3. Export gecmisini job bazli metadata ile zenginlestirmek.
4. LLM Repair panelinden prompt kopyalama ve rapora bagli filtre eklemek.
5. GitHub Actions icin manifest policy gate workflow'u eklemek.
6. Studio icin daha ayrintili backend contract testleri eklemek.
7. README'ye yalnizca kisa link ekleyip detay dokumani bu dosyada tutmak.

## 26. Sozluk

| Terim | Anlam |
|---|---|
| Framework koku | BookFactory araclarinin bulundugu repo kokudur |
| Kitap koku | Belirli bir kitap projesinin manifest ve bolum dosyalarini tuttugu klasordur |
| Manifest | Kitap yapisi ve uretim politikasinin tek dogruluk kaynagidir |
| CODE_META | Kod blogunun test ve dosya metadata standardidir |
| Quality gate | Uretim adimini gecmek icin saglanmasi gereken kuraldir |
| Studio | Yerel FastAPI tabanli GUI arayuzudur |
| Control panel | Studio icinde uretim durumunu ozetleyen salt-okunur paneldir |
| Post-production | Bolum birlestirme, asset, QR, export ve bicimlendirme hattidir |
| Repair prompt | Basarisiz kod veya blok icin LLM'e verilen duzeltme promptudur |

