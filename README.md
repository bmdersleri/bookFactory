# Parametric Computer Book Factory

**Manifest tabanlı, LLM destekli, kod doğrulamalı ve GUI destekli teknik kitap üretim framework'ü**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-green)](https://nodejs.org/)
[![Pandoc](https://img.shields.io/badge/Pandoc-3.x-orange)](https://pandoc.org/)
[![PowerShell](https://img.shields.io/badge/PowerShell-7.x-blueviolet)](https://learn.microsoft.com/powershell/)
[![Sürüm](https://img.shields.io/badge/Framework-v3.4.0-purple)]()
[![Studio](https://img.shields.io/badge/Studio-v3.4.0-teal)]()
[![Lisans](https://img.shields.io/badge/Lisans-MIT-lightgrey)]()

---

## İçindekiler

- [Proje nedir?](#proje-nedir)
- [Son durum](#son-durum)
- [Temel ilkeler](#temel-ilkeler)
- [Öne çıkan özellikler](#öne-çıkan-özellikler)
- [BookFactory Studio](#bookfactory-studio)
- [Proje yapısı](#proje-yapısı)
- [Gereksinimler](#gereksinimler)
- [Kurulum](#kurulum)
- [Hızlı başlangıç](#hızlı-başlangıç)
- [Kitap projesi oluşturma](#kitap-projesi-oluşturma)
- [Kitap kökü ve framework kökü ayrımı](#kitap-kökü-ve-framework-kökü-ayrımı)
- [CLI referansı](#cli-referansı)
- [Üretim hattı](#üretim-hattı)
- [LLM entegrasyonu](#llm-entegrasyonu)
- [Sürüm geçmişi](#sürüm-geçmişi)
- [Katkı ve geliştirme](#katkı-ve-geliştirme)
- [Lisans](#lisans)

---

## Proje nedir?

**Parametric Computer Book Factory**, bilgisayar bilimleri, yazılım mühendisliği, veri bilimi, yapay zekâ, web/mobil programlama ve IoT gibi teknik alanlarda ders kitabı üretimini standartlaştırmak için geliştirilmiş bir framework'tür.

Sistem, LLM'e yalnızca “bir kitap yaz” demek yerine üretim sürecini **manifest**, **prompt standartları**, **kod doğrulama**, **kalite kapıları**, **programatik ekran çıktıları**, **QR/GitHub entegrasyonu** ve **post-production** adımlarıyla izlenebilir ve tekrar üretilebilir hale getirir.

```text
Kitap fikri
  → Manifest
  → Bölüm girdi promptları
  → Bölüm tam metinleri
  → Markdown kalite kontrolü
  → CODE_META çıkarımı ve kod testleri
  → Mermaid / screenshot / QR üretimi
  → GitHub sync / code pages / Codespaces kontrolü
  → Export: Markdown / DOCX / HTML / EPUB / PDF
```

BookFactory iki katmanlı çalışır:

1. **Framework reposu:** BookFactory araçları, CLI, Studio arayüzü, şemalar, kalite kontrol betikleri ve post-production hattı.
2. **Kitap reposu:** Belirli bir kitap projesine ait `book_manifest.yaml`, `chapters/`, `assets/`, `build/`, `screenshots/`, `exports/` ve çıktı dosyaları.

Örnek bağlı kitap projesi: [`bmdersleri/react-web`](https://github.com/bmdersleri/react-web)

---

## Son durum

Bu sürümde README, son geliştirmelerden sonra güncellenmiştir. Güncel odak noktaları şunlardır:

- **BookFactory Studio yerel web arayüzü** ana kullanım yolu haline getirildi.
- **Akıllı Manifest Editörü** eklendi ve YAML textarea ağırlıklı yapıdan form tabanlı, sekmeli ve doğrulamalı yapıya geçirildi.
- Manifest editöründe **Kitap Bilgileri**, **Bölümler**, **Kapsam**, **Otomasyon**, **Yollar** ve **YAML** sekmeleri kullanılabilir hale getirildi.
- Bölüm dosya adları için gerçek `chapters/*.md` dosyalarıyla **dosya eşleştirme** desteği eklendi.
- Hatalı girişleri azaltmak için kayıt öncesi doğrulamalar eklendi.
- Framework kökü ile kitap kökü ayrımı netleştirildi.
- Studio arayüzünde daha okunaklı font ailesi, daha dengeli font ağırlıkları ve iyileştirilmiş form/tablo okunabilirliği uygulandı.
- v2.11.x hattında dashboard, code pages, GitHub sync, Codespaces ve CI odaklı iyileştirmeler yapıldı.

---

## Temel ilkeler

> **`book_manifest.yaml` tek doğruluk kaynağıdır.**

| İlke | Açıklama |
|---|---|
| Manifest önceliği | Kitap yapısı, bölüm sırası, kapsam ve üretim kararları manifestten beslenir. |
| Belirsizlikte dur | Eksik bilgi tahmin edilmez; kritik kararlarda kullanıcı onayı beklenir. |
| Kod çalışırlığı | Çalıştırılabilir kod blokları `CODE_META` standardıyla test edilebilir hale getirilir. |
| İzlenebilir üretim | Prompt, bölüm, kod, rapor ve çıktı dosyaları klasör yapısında ayrıştırılır. |
| Manuel varlık koruması | `assets/manual/` ve `assets/locked/` altındaki dosyalar otomasyon tarafından ezilmez. |
| İnsan onayı | Manifest, bölüm, kod testi, export ve yayın aşamalarında kalite kapıları kullanılır. |
| Dil tutarlılığı | Dosya adları ve ID'ler mümkün olduğunca İngilizce; içerik hedef dilde tutulur. |

---

## Öne çıkan özellikler

### Çekirdek üretim

- **Manifest tabanlı kitap üretimi:** `book_manifest.yaml` ile başlık, yazar, dil, bölüm listesi, kapsam ve otomasyon tercihleri yönetilir.
- **LLM yürütme sözleşmesi:** LLM'in üretim sırasında uyması gereken kurallar `core/` ve `docs/briefs/` altında tanımlanır.
- **Bölüm girdi promptu üretimi:** Her bölüm için manifest uyumlu, kontrollü ve tekrar üretilebilir girdi promptları oluşturulur.
- **Kümülatif uygulama yaklaşımı:** Özellikle React gibi uygulamalı kitaplarda bölümler ilerledikçe tek bir proje üzerinde inşa edilen örnek senaryolar desteklenir.

### Kod kalitesi

- **CODE_META standardı:** Kod blokları ID, dil, dosya adı, test tipi, beklenen çıktı, GitHub ve QR bilgileriyle etiketlenir.
- **Kod çıkarımı:** Markdown içindeki kod blokları dosya sistemine çıkarılır.
- **Kod doğrulama:** JSON/YAML kod manifestleri üretilir ve doğrulanır.
- **Test adaptörleri:** JavaScript, Python ve Java örnekleri için test adaptörleri desteklenir.
- **Onarım promptları:** Hatalı kodlar için LLM'e verilecek onarım promptları üretilebilir.

### İçerik ve görsel kalite

- **Markdown kalite kontrolü:** H1 sayısı, bölüm ID'si, CODE_META yerleşimi, screenshot markerları ve kapsam sapmaları denetlenir.
- **Mermaid entegrasyonu:** Mermaid diyagramları `.mmd` olarak çıkarılır ve PNG çıktısına dönüştürülür.
- **Programatik ekran çıktısı planı:** `[SCREENSHOT:id]` marker standardı ile bölüm içinde ekran görüntüsü hedefleri yönetilir.
- **QR üretimi:** Kod sayfası ve kaynak kod bağlantıları için QR görselleri üretilebilir.

### Çıktı ve dağıtım

- **Markdown birleşik çıktı**
- **DOCX** üretimi: Pandoc, Lua filter ve referans şablon desteği
- **HTML** üretimi: tek sayfa veya site yapısı
- **EPUB** üretimi
- **PDF** üretimi
- **GitHub sync:** Kod örneklerini GitHub uyumlu klasör yapısına hazırlar.
- **Code pages:** Kod örnekleri için açıklamalı statik HTML/Markdown sayfaları oluşturur.
- **GitHub Pages hazırlığı:** Kod ve sayfa çıktıları yayınlanabilir yapıya getirilebilir.
- **GitHub Codespaces desteği:** Bulut IDE ortamı için kontrol ve başlatma komutları bulunur.

### Geliştirici deneyimi

- **BookFactory Studio:** Yerel web arayüzü ile manifest, bölüm, production ve rapor işlemleri tek yerden yürütülür.
- **PowerShell 7 uyumluluğu:** Windows ortamında UTF-8 ve path sorunlarına karşı daha güvenli kullanım hedeflenir.
- **Streamlit dashboard:** Kod testleri, export çıktıları, glossary/index, GitHub sync ve Codespaces raporları okunabilir panellerle izlenebilir.
- **Scaffold/init araçları:** Yeni kitap projeleri kontrollü klasör yapısıyla başlatılabilir.

---

## BookFactory Studio

BookFactory Studio, mevcut CLI araçlarını bozmadan çalışan **FastAPI tabanlı yerel web arayüzüdür**. Varsayılan adres:

```text
http://127.0.0.1:8765
```

### Başlatma

PowerShell ile:

```powershell
cd "C:\OneDrive\OneDrive - mehmetakif.edu.tr\BookFactory"
python -m pip install -r requirements.txt
python -m bookfactory_studio.app
```

veya hazır başlatıcılarla:

```powershell
.\run_studio.ps1
```

```bat
run_studio.bat
```

### Ana ekranlar

| Ekran | Amaç |
|---|---|
| Dashboard | Kitap başlığı, yazar, bölüm sayısı, manifest durumu ve son raporları gösterir. |
| Kitap Sihirbazı | Yeni kitap mimarisi ve manifest üretimi için LLM promptu hazırlar. |
| Manifest | Form tabanlı akıllı manifest editörünü sunar. |
| Bölümler | Bölüm girdi promptlarını üretir ve LLM'den gelen Markdown metinlerini kaydeder. |
| Production | Kalite, kod, Mermaid, QR, GitHub, Codespaces ve export adımlarını çalıştırır. |
| Raporlar | `build/`, `reports/`, `exports/` altındaki raporları listeler ve görüntüler. |

### Akıllı Manifest Editörü

Manifest editörü, `book_manifest.yaml` dosyasını doğrudan YAML yazmadan yönetebilmek için sekmeli ve form tabanlı olarak tasarlanmıştır.

| Sekme | İçerik |
|---|---|
| Kitap Bilgileri | Başlık, alt başlık, yazar, yıl, baskı, framework sürümü ve dil bilgileri |
| Bölümler | Bölüm ID'si, başlığı, dosya adı, durum bilgisi ve gerçek dosya varlığı |
| Kapsam | Teknoloji yığını, kapsam dışı konular ve pedagojik sınırlar |
| Otomasyon | Manifest validation, code tests, QR, Mermaid, GitHub sync ve export kapıları |
| Yollar | Kitap köküne göre göreli klasör yolları |
| YAML | İleri kullanıcılar için ham YAML görüntüleme, önizleme ve kaydetme |

### Hatalı giriş önleme

Kayıt öncesinde aşağıdaki kontroller yapılır:

- `book.title` boş olamaz.
- `book.author` boş olamaz.
- `book.year` dört haneli olmalıdır.
- `language.primary_language` eksik olmamalıdır.
- Bölüm ID'leri tekrarlanmamalıdır.
- Bölüm dosya adları tekrarlanmamalıdır.
- Bölüm dosya adları güvenli ASCII biçiminde ve `.md` uzantılı olmalıdır.
- `project.paths` alanlarında mutlak yol ve `..` kullanımı engellenir.
- `done`, `draft`, `review`, `in_progress` durumundaki bölümlerde gerçek dosya yoksa kullanıcı uyarılır.

### Bölüm dosyalarını eşleştirme

`Dosyaları Eşleştir` işlemi, manifestteki bölüm dosya adlarını `chapters/` klasöründeki gerçek Markdown dosyalarıyla karşılaştırır. Böylece manifestte örneğin:

```yaml
file: chapter_02_javascript_temelleri.md
```

gerçekte var olan şu dosyayla eşleştirilebilir:

```yaml
file: chapter_02_javascript_es6_react.md
```

Eşleştirme öncelikle `chapter_XX_*.md` desenine göre yapılır.

---

## Proje yapısı

```text
BookFactory/
├── bookfactory/                    # Python CLI paketi
│   ├── cli.py
│   └── commands/
│       └── init.py
│
├── bookfactory_studio/             # FastAPI tabanlı yerel web arayüzü
│   ├── app.py
│   ├── core.py
│   ├── jobs.py
│   └── static/
│       ├── index.html
│       ├── app.js
│       └── styles.css
│
├── bookfactory-gui/                # VS Code / GUI deneysel arayüz bileşenleri
│
├── core/                           # LLM politika ve üretim standartları
│   ├── 00_llm_execution_contract.md
│   ├── 01_book_manifest_schema.md
│   ├── 02_general_system_prompt.md
│   └── ...
│
├── docs/                           # Kullanıcı, Studio, path modeli ve LLM briefing belgeleri
│   ├── bookfactory_studio_mvp.md
│   ├── bookfactory_studio_manifest_editor.md
│   ├── bookfactory_studio_path_model.md
│   ├── quickstart.md
│   ├── windows_setup.md
│   └── briefs/
│       ├── LLM_PROJECT_BRIEF.md
│       ├── brief_core.md
│       ├── brief_llm_rules.md
│       ├── brief_standards.md
│       └── ...
│
├── tools/                          # Üretim, kalite, export, GitHub, QR ve dashboard araçları
│   ├── code/                       # CODE_META çıkarımı, doğrulama ve testler
│   ├── cloud/                      # Codespaces kontrol ve başlatma araçları
│   ├── dashboard/                  # Yerel dashboard
│   ├── export/                     # Markdown/HTML/EPUB/PDF export araçları
│   ├── github/                     # GitHub sync, code pages ve Pages hazırlığı
│   ├── indexing/                   # Glossary / back-index üretimi
│   ├── postproduction/             # Mermaid, QR, DOCX ve birleşik çıktı hattı
│   ├── quality/                    # Markdown kalite kontrolü
│   └── utils/                      # Ortak YAML/JSON ve süreç yardımcıları
│
├── schemas/                        # Manifest ve CODE_META JSON Schema dosyaları
├── templates/                      # Export, Lua filter, Codespaces ve sözlük şablonları
├── configs/                        # Post-production profil şablonları
├── examples/                       # Örnek prompt ve meta bloklar
├── build/                          # Framework çalışma çıktıları
│
├── README.md
├── CHANGELOG.md
├── SETUP.md
├── RELEASE_CHECKLIST.md
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── run_studio.ps1
└── run_studio.bat
```

> **Not:** Gerçek kitap içerikleri ideal olarak bu framework reposu içinde değil, bağımsız kitap reposunda tutulur. Örneğin `react-web` projesi ayrı bir kitap reposu olarak yönetilir.

---

## Gereksinimler

| Araç | Minimum sürüm | Kullanım |
|---|---:|---|
| Python | 3.10+ | CLI, Studio, kalite kontrol ve post-production |
| Node.js | 18+ | JavaScript/React kod testleri ve Mermaid CLI |
| Pandoc | 3.x | DOCX/EPUB/PDF üretimi |
| Mermaid CLI (`mmdc`) | 10+ | Mermaid diyagramlarını PNG'ye dönüştürme |
| PowerShell | 7.x | Windows'ta önerilen terminal ortamı |
| Git | 2.x | Repo yönetimi, GitHub sync ve yayınlama |
| Java/JDK | 17+ | Java örneklerinin test edilmesi gereken kitaplarda |
| Chrome / Chromium | Güncel | Mermaid, screenshot ve web tabanlı doğrulama senaryoları |

---

## Kurulum

### 1. Repoyu klonlayın

```powershell
git clone https://github.com/bmdersleri/bookFactory.git
cd bookFactory
```

### 2. Python bağımlılıklarını kurun

```powershell
python -m pip install -r requirements.txt
```

Geliştirme bağımlılıkları için:

```powershell
python -m pip install -r requirements-dev.txt
```

veya editable kurulum:

```powershell
python -m pip install -e .
```

### 3. Ortamı doğrulayın

```powershell
python tools/check_environment.py --soft
python tools/check_package_integrity.py .
```

CLI üzerinden:

```powershell
python -m bookfactory doctor --soft
python -m bookfactory test-minimal --fail-on-error
```

---

## Hızlı başlangıç

### Studio ile önerilen başlangıç

```powershell
cd "C:\OneDrive\OneDrive - mehmetakif.edu.tr\BookFactory"
.\run_studio.ps1
```

Tarayıcıda:

```text
http://127.0.0.1:8765
```

Arayüzde **Aktif Kitap / Kitap kökü** alanına framework klasörü değil, doğrudan kitap klasörü yazılmalıdır:

```text
C:\OneDrive\OneDrive - mehmetakif.edu.tr\react-web
```

veya framework altında çalışma klasörü kullanılıyorsa:

```text
C:\OneDrive\OneDrive - mehmetakif.edu.tr\BookFactory\workspace\react
```

### CLI ile hızlı kontrol

```powershell
python -m bookfactory version
python -m bookfactory doctor --soft
python -m bookfactory test-minimal --fail-on-error
```

Manifest doğrulama:

```powershell
python tools/validate_manifest.py manifests/book_manifest.yaml
```

---

## Kitap projesi oluşturma

Her kitap, BookFactory framework'ünden bağımsız bir Git reposunda yaşayabilir. Yeni bir proje başlatmak için scaffold aracı veya CLI init komutu kullanılabilir.

### Scaffold örneği

```powershell
python tools/scaffold_book_project.py `
  --name react-web `
  --title "React ile Web Uygulama Geliştirme" `
  --author "Prof. Dr. İsmail KIRBAŞ" `
  --lang tr `
  --output ".."
```

Örnek kitap repo yapısı:

```text
react-web/
├── .bookfactory
├── README.md
├── book_manifest.yaml veya manifests/book_manifest.yaml
├── chapters/                  # Bölüm Markdown dosyaları
├── prompts/
│   └── chapter_inputs/        # LLM bölüm girdi promptları
├── configs/
│   └── post_production_profile.yaml
├── assets/
│   ├── auto/
│   ├── manual/
│   ├── locked/
│   └── final/
├── build/
│   ├── code/
│   ├── reports/
│   └── test_reports/
├── screenshots/
├── exports/ veya dist/
└── docs/
```

### Init komutu

```powershell
python -m bookfactory init --output ..
```

Simülasyon için:

```powershell
python -m bookfactory init --output .. --dry-run
```

---

## Kitap kökü ve framework kökü ayrımı

BookFactory Studio iki farklı kökü bilinçli olarak ayırır:

| Kök | Açıklama |
|---|---|
| Framework kökü | `tools/`, `bookfactory/`, `bookfactory_studio/`, `schemas/` klasörlerinin bulunduğu BookFactory uygulama klasörüdür. |
| Kitap kökü | Belirli bir kitaba ait `book_manifest.yaml`, `chapters/`, `assets/`, `build/`, `exports/` klasörlerinin bulunduğu çalışma klasörüdür. |

Doğru kullanım:

```text
C:\OneDrive\OneDrive - mehmetakif.edu.tr\react-web
```

veya:

```text
C:\OneDrive\OneDrive - mehmetakif.edu.tr\BookFactory\workspace\react
```

Yanlış kullanım:

```text
C:\OneDrive\OneDrive - mehmetakif.edu.tr\BookFactory
```

Bu yol framework köküdür; doğrudan kitap kökü değildir. Studio framework kökü seçildiğinde alt klasörlerdeki kitap manifestlerini otomatik aktif proje kabul etmek yerine kullanıcıyı doğru kitap kökünü seçmeye yönlendirir.

---

## CLI referansı

```powershell
python -m bookfactory version              # Framework sürümünü gösterir
python -m bookfactory doctor --soft        # Ortam tanısı yapar
python -m bookfactory test-minimal         # Minimal demo testi çalıştırır
python -m bookfactory test-code `          # Bölüm kodlarını test eder
  --chapters-dir <klasör> --fail-on-error
python -m bookfactory repair-prompts       # Hatalı kodlar için onarım promptu üretir
python -m bookfactory sync-github `        # Kodları GitHub uyumlu yapıya hazırlar
  --code-manifest <dosya> --push
python -m bookfactory qr-from-code `       # Kod manifestinden QR manifesti üretir
  --code-manifest <dosya>
python -m bookfactory export `             # Markdown/DOCX/HTML/EPUB/PDF çıktıları üretir
  --profile <profil> --format all
python -m bookfactory build-index `        # Terim dizini / back-index üretir
  --profile <profil>
python -m bookfactory dashboard --check    # Dashboard bağımlılıklarını kontrol eder
python -m bookfactory codespaces-check     # Codespaces uyumluluğunu kontrol eder
python -m bookfactory codespaces-init      # Codespaces yapılandırmasını hazırlar
python -m bookfactory init                 # İnteraktif yeni kitap projesi başlatır
```

---

## Üretim hattı

### CODE_META standardı

Her çalıştırılabilir kod bloğundan önce HTML yorum bloğu önerilir/zorunlu tutulur:

````markdown
<!-- CODE_META
id: react_ch02_code01
chapter_id: chapter_02
language: javascript
kind: example
title: "const ve let kullanımı"
file: "const_let_example.js"
extract: true
test: run
expected_output: "KampüsHub"
github: true
qr: dual
-->

```javascript
const appName = "KampüsHub";
console.log(appName);
```
````

### Kod bloklarını çıkarma ve test etme

Kitap reposu içinde:

```powershell
$env:PYTHONPATH = "..\bookFactory"

python -m tools.code.extract_code_blocks `
  --package-root . `
  --out-dir .\build\code `
  --manifest .\build\code_manifest.json `
  --yaml-manifest .\build\code_manifest.yaml `
  --chapters-dir .\chapters

python -m tools.code.validate_code_meta `
  .\build\code_manifest.json `
  --package-root .

python -m tools.code.run_code_tests `
  --manifest .\build\code_manifest.json `
  --package-root . `
  --report-json .\build\test_reports\code_test_report.json `
  --report-md .\build\test_reports\code_test_report.md `
  --fail-on-error
```

### Markdown kalite kontrolü

```powershell
python -m tools.quality.check_chapter_markdown `
  --chapter .\chapters\chapter_01.md `
  --chapter-id chapter_01 `
  --chapter-no 1 `
  --report .\build\test_reports\chapter_01_quality.md

Select-String -Path .\build\test_reports\chapter_01_quality.md -Pattern "❌|FAIL"
```

### Post-production

```powershell
python tools/postproduction/post_production_pipeline.py `
  --profile configs/post_production_profile.yaml `
  --stage all
```

Yaygın aşamalar:

```text
merge_chapters
extract_mermaid
render_mermaid
build_docx
build_html
build_epub
generate_qr
```

Studio içinde Production ekranı bu adımları tek tek veya tam hat halinde çalıştırabilir.

---

## LLM entegrasyonu

BookFactory, LLM modelleriyle çalışırken tek ve devasa bir açıklama dosyası yerine modüler briefing yaklaşımı kullanır.

| Dosya | Ne zaman kullanılır? |
|---|---|
| `docs/briefs/brief_core.md` | Her oturumun başında |
| `docs/briefs/brief_llm_rules.md` | Her oturumun başında, davranış kuralları için |
| `docs/briefs/brief_standards.md` | Bölüm üretimi, CODE_META, screenshot ve Mermaid standartları için |
| `docs/briefs/brief_structure.md` | Klasör/dosya yapısı işlemlerinde |
| `docs/briefs/brief_environment.md` | Windows, PowerShell, Codespaces ve ortam sorunlarında |
| `docs/briefs/brief_loading_order.md` | Yeni oturum veya aşama planlamasında |
| `docs/briefs/brief_react_context.md` | React kitabı gibi özel kitap bağlamlarında |

Minimum başlangıç komutu:

```text
Aşağıdaki dosyalar Parametric Computer Book Factory v2.11.x çerçevesine aittir.

Önce `docs/briefs/brief_core.md`, ardından `docs/briefs/brief_llm_rules.md` dosyasını oku.
Kitap bağlamı için ilgili `brief_*context.md` dosyasını yükle.
Bölüm üretimi yapacaksan `docs/briefs/brief_standards.md` dosyasını da oku.

Manifesti doğrula. Eksik alan varsa üretime geçmeden raporla.
Eksik bilgiyi tahmin etme; kullanıcıdan sor.
```

---

## Sürüm geçmişi

| Sürüm | Öne çıkan özellikler |
|---|---|
| **Studio v3.1.x** | FastAPI tabanlı yerel GUI, akıllı manifest editörü, kitap/framework kökü ayrımı, form tabanlı kayıt, bölüm dosyası eşleştirme ve okunabilirlik iyileştirmeleri |
| **v2.11.x** | Dashboard panelleri, GitHub Actions/CI, rich static code pages, `render-code-pages`, GitHub sync düzeltmeleri |
| **v2.10.x** | Ortak YAML/JSON ve process helper modülleri, adapter tabanlı kod test mimarisi |
| **v2.9.x** | GitHub Codespaces desteği ve Codespaces kontrol araçları |
| **v2.8.x** | Dashboard, glossary/index ve proje metrikleri |
| **v2.7.x** | EPUB, tek sayfa HTML ve statik site export hattı |
| **v2.6.x** | GitHub sync ve QR hardening |
| **v2.5.x** | CODE_META kod doğrulama hattı ve CLI foundation |
| **v2.4.x** | Asset manifest örnekleri ve chapter order araçları |
| **v2.3.x** | Manifest doğrulama, paket bütünlük kontrolü ve quickstart |
| **v2.1.x** | Post-production hattı, Mermaid, DOCX ve Lua filter |

Ayrıntılı kayıt için `CHANGELOG.md` dosyasına bakın.

---

## Katkı ve geliştirme

Geliştirme ortamını hazırlamak için:

```powershell
python -m pip install -r requirements-dev.txt
python -m pip install -e .
```

Temel kontroller:

```powershell
python -m bookfactory doctor --soft
python -m bookfactory test-minimal --fail-on-error
python tools/check_package_integrity.py .
```

Studio geliştirmesi sırasında:

```powershell
python -m bookfactory_studio.app
```

Arayüz dosyaları:

```text
bookfactory_studio/static/index.html
bookfactory_studio/static/app.js
bookfactory_studio/static/styles.css
```

---

## Lisans

MIT Lisansı — ayrıntılar için `LICENSE` dosyasına bakın.

---

**Yazar:** Prof. Dr. İsmail KIRBAŞ  
**Framework repo:** [github.com/bmdersleri/bookFactory](https://github.com/bmdersleri/bookFactory)  
**Bağlı React kitap projesi:** [github.com/bmdersleri/react-web](https://github.com/bmdersleri/react-web)
