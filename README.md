# Parametric Computer Book Factory

**Manifest tabanlı, LLM destekli, kod doğrulamalı teknik kitap üretim framework'ü**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-green)](https://nodejs.org/)
[![Pandoc](https://img.shields.io/badge/Pandoc-3.x-orange)](https://pandoc.org/)
[![Sürüm](https://img.shields.io/badge/Sürüm-v2.11.x-purple)]()
[![Lisans](https://img.shields.io/badge/Lisans-MIT-lightgrey)]()

---

## İçindekiler

- [Proje nedir?](#proje-nedir)
- [Temel ilkeler](#temel-ilkeler)
- [Özellikler](#özellikler)
- [Proje yapısı](#proje-yapısı)
- [Gereksinimler](#gereksinimler)
- [Kurulum](#kurulum)
- [Hızlı başlangıç](#hızlı-başlangıç)
- [Kitap projesi oluşturma](#kitap-projesi-oluşturma)
- [CLI referansı](#cli-referansı)
- [Üretim hattı](#üretim-hattı)
- [LLM entegrasyonu](#llm-entegrasyonu)
- [Sürüm geçmişi](#sürüm-geçmişi)

---

## Proje nedir?

**Parametric Computer Book Factory**, bilgisayar bilimleri, yazılım mühendisliği, veri bilimi, yapay zekâ, web/mobil programlama ve IoT gibi teknik alanlarda ders kitabı üretimini standartlaştırmak için geliştirilmiş bir framework'tür.

LLM'e yalnızca "bir kitap yaz" demek yerine, üretim sürecini manifest, prompt standartları, kod doğrulama ve kalite kapılarıyla **izlenebilir ve tekrar üretilebilir** hale getirir.

```
Kitap fikri → Manifest → Promptlar → Bölüm taslakları → Tam metin
     → Kod doğrulama → Markdown kalite kontrolü → Screenshot planı
          → QR & GitHub sync → Post-production → DOCX / EPUB / PDF
```

---

## Temel ilkeler

> **`book_manifest.yaml` tek doğruluk kaynağıdır.**

| İlke | Açıklama |
|---|---|
| Manifest önceliği | Tüm üretim kararları manifest'ten beslenir |
| Belirsizlikte dur | Eksik bilgiyi tahmin etme, kullanıcıdan sor |
| Kod çalışırlığı | Her kod bloğu `CODE_META` standardıyla test edilebilir |
| Manuel varlık koruması | `assets/manual/` ve `assets/locked/` hiçbir araç tarafından silinmez |
| İnsan onayı | Kritik aşamalar kullanıcı onayı olmadan geçilmez |
| Dil tutarlılığı | Dosya adları/ID'ler İngilizce, içerik hedef dilde |

---

## Özellikler

### Çekirdek
- 📋 **Manifest tabanlı üretim** — `book_manifest.yaml` ile kitap yapısı, dil, kapsam ve onay kapıları yönetilir
- 🤖 **LLM yürütme sözleşmesi** — LLM'in ne yapıp yapmaması gerektiği `core/` altında 20+ politika dosyasıyla tanımlanır
- 📝 **Modüler LLM briefingi** — Büyük tek belge yerine senaryoya göre yüklenen 7 modüler dosya (`brief_*.md`)

### Kod kalitesi
- 🔍 **CODE_META standardı** — Her kod bloğu HTML yorum bloğuyla etiketlenir
- ✅ **Otomatik test hattı** — `extract → validate → test` zinciri, Node.js/Python ile çalıştırılır
- 📊 **Çift format rapor** — JSON + Markdown test raporları üretilir

### İçerik kalitesi
- 🏗️ **Markdown kalite kontrolü** — H1 sayısı, CODE_META yerleşimi, screenshot marker, kapsam sapması denetlenir
- 📸 **Screenshot planı** — `[SCREENSHOT:id]` marker standardı ile programatik ekran çıktısı yönetimi
- 📐 **Mermaid entegrasyonu** — Diyagramlar PNG'ye dönüştürülür, manuel override desteklenir

### Çıktı & dağıtım
- 📄 **DOCX** — Pandoc + Lua filter + referans şablon ile biçimlendirilmiş Word belgesi
- 🌐 **HTML** — Tek sayfa veya bölüm bazlı statik site
- 📱 **EPUB** — E-kitap formatı
- 📦 **PDF** — Baskıya hazır çıktı
- 🔗 **QR & GitHub sync** — Kod örnekleri QR koduyla ve GitHub Pages ile ilişkilendirilir

### Geliştirici deneyimi
- 💻 **GitHub Codespaces** — `.devcontainer/` ile tek tıkla hazır ortam
- 🪟 **Windows/PowerShell 7** — UTF-8 ve path sorunlarına karşı sertleştirilmiş araçlar
- 🏗️ **Scaffold aracı** — Yeni kitap projesi tek komutla oluşturulur
- 📊 **Streamlit dashboard** — Proje durumu ve kalite metrikleri görselleştirmesi

---

## Proje yapısı

```
bookFactory/
├── .devcontainer/             # GitHub Codespaces yapılandırması
├── .github/
│   ├── codespaces/
│   └── workflows/             # CI/CD
│
├── core/                      # LLM politika ve prompt dosyaları (20+)
│   ├── 00_llm_execution_contract.md
│   ├── 01_book_manifest_schema.md
│   ├── 02_general_system_prompt.md
│   └── ...
│
├── bookfactory/               # Python paketi (CLI)
│   └── cli.py
│
├── tools/                     # Yardımcı araçlar
│   ├── scaffold_book_project.py   ← Yeni kitap projesi oluşturur
│   ├── check_environment.py
│   ├── check_package_integrity.py
│   ├── validate_manifest.py
│   ├── generate_chapter_inputs.py
│   ├── code/                  # Kod doğrulama zinciri
│   │   ├── extract_code_blocks.py
│   │   ├── validate_code_meta.py
│   │   └── run_code_tests.py
│   ├── quality/
│   │   └── check_chapter_markdown.py
│   └── postproduction/        # Post-production hattı
│       ├── post_production_pipeline.py
│       ├── generate_qr_codes.py
│       └── resolve_assets.py
│
├── manifests/                 # Örnek manifest dosyaları
│   └── java_fundamentals_manifest.yaml
│
├── schemas/                   # JSON Schema dosyaları
│   └── code_meta_schema.json
│
├── templates/                 # Terim sözlüğü ve çeviri belleği şablonları
├── examples/                  # Örnek bölüm ve minimal kitap demosu
├── configs/                   # Post-production profil şablonları
├── docs/                      # Kullanıcı ve geliştirici belgeleri
│
# LLM Briefing Modülleri (kök dizin)
├── LLM_PROJECT_BRIEF.md       # Index / router
├── brief_core.md              # Proje özeti ve temel ilkeler
├── brief_llm_rules.md         # LLM davranış kuralları
├── brief_structure.md         # Klasör yapısı rehberi
├── brief_standards.md         # CODE_META, screenshot, Mermaid standartları
├── brief_react_context.md     # React kitabı bağlamı (örnek)
├── brief_environment.md       # PowerShell/Codespaces ortam rehberi
├── brief_loading_order.md     # Yükleme sırası ve iş akışı
│
├── README.md
├── SETUP.md
├── KULLANIM_KILAVUZU.md
├── RELEASE_CHECKLIST.md
├── CHANGELOG.md
├── requirements.txt
├── requirements-dev.txt
└── pyproject.toml
```

> **Not:** Kitap içeriği (`workspace/`) bu repoda bulunmaz.  
> Her kitap projesi kendi bağımsız reposunda yaşar. Bkz. [Kitap projesi oluşturma](#kitap-projesi-oluşturma).

---

## Gereksinimler

| Araç | Minimum sürüm | Zorunlu |
|---|---|---|
| Python | 3.10+ | ✅ |
| Node.js | 18+ | ✅ (kod testleri için) |
| Pandoc | 3.x | ✅ (DOCX üretimi için) |
| Mermaid CLI (`mmdc`) | 10+ | ⚡ (diyagram PNG üretimi için) |
| PowerShell | 7.x | ⚡ (Windows'ta önerilir) |
| Java | 17+ | ⚡ (bazı araçlar için) |
| Git | 2.x | ✅ |

---

## Kurulum

```powershell
# 1. Repoyu klonla
git clone https://github.com/bmdersleri/bookFactory.git
cd bookFactory

# 2. Python bağımlılıklarını kur
pip install -r requirements.txt

# 3. Ortamı doğrula
python tools/check_environment.py --soft

# 4. Paket bütünlüğünü kontrol et
python tools/check_package_integrity.py .
```

**Hızlı ortam kontrolü (CLI üzerinden):**

```powershell
python -m bookfactory doctor --soft
python -m bookfactory test-minimal --fail-on-error
```

---

## Hızlı başlangıç

```powershell
# Sürümü kontrol et
python -m bookfactory version

# Ortam tanısı
python -m bookfactory doctor --soft

# Minimal kitap demosu ile uçtan uca test
python -m bookfactory test-minimal --fail-on-error

# Manifest doğrulama (kendi manifestiniz için)
python tools/validate_manifest.py manifests/book_manifest.yaml
```

---

## Kitap projesi oluşturma

Her kitap, BookFactory'den **bağımsız bir Git reposunda** yaşar. Yeni bir proje başlatmak için:

```powershell
python tools/scaffold_book_project.py `
  --name react-web `
  --title "React ile Web Uygulama Geliştirme" `
  --author "Prof. Dr. İsmail KIRBAŞ" `
  --lang tr `
  --output ".."
```

Bu komut şu yapıyı oluşturur:

```
../react-web/
├── .bookfactory           # Framework bağlantı dosyası
├── README.md
├── .gitignore
├── chapters/              # Bölüm Markdown dosyaları
├── chapter_inputs/        # LLM bölüm girdi promptları
├── manifests/
│   └── book_manifest.yaml
├── configs/
│   └── post_production_profile.yaml
├── assets/
│   ├── auto/   manual/   locked/   final/
├── build/
│   ├── code/
│   └── test_reports/
├── screenshots/
└── dist/
```

**Kitap reposunda kod doğrulama çalıştırma:**

```powershell
# PYTHONPATH'i BookFactory'ye yönlendir
$env:PYTHONPATH = "..\bookFactory"

# Kod bloklarını çıkar ve test et
python -m tools.code.extract_code_blocks `
  --package-root . `
  --out-dir .\build\code `
  --manifest .\build\code_manifest.json `
  --chapters-dir .\chapters

python -m tools.code.run_code_tests `
  --manifest .\build\code_manifest.json `
  --package-root . `
  --report-json .\build\test_reports\code_test_report.json `
  --report-md .\build\test_reports\code_test_report.md `
  --node node --fail-on-error
```

---

## CLI referansı

```powershell
python -m bookfactory version              # Framework sürümü
python -m bookfactory doctor --soft        # Ortam tanısı
python -m bookfactory test-minimal         # Minimal demo testi
python -m bookfactory test-code `          # Bölüm kod testi
  --chapters-dir <klasör> --fail-on-error
python -m bookfactory repair-prompts       # LLM prompt onarımı
python -m bookfactory sync-github `        # GitHub senkronizasyonu
  --code-manifest <dosya> --push
python -m bookfactory qr-from-code `       # QR kod üretimi
  --code-manifest <dosya>
python -m bookfactory export `             # Çıktı üretimi
  --profile <profil> --format all
python -m bookfactory build-index `        # Terim dizini
  --profile <profil>
python -m bookfactory dashboard --check    # Dashboard kontrolü
python -m bookfactory codespaces-check     # Codespaces uyumluluk
python -m bookfactory codespaces-init      # Codespaces başlatma
```

---

## Üretim hattı

### CODE_META standardı

Her çalıştırılabilir kod bloğundan önce HTML yorum bloğu zorunludur:

```markdown
<!-- CODE_META
id: ch02_code01
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
```

### Post-production

```powershell
python tools/postproduction/post_production_pipeline.py `
  --profile configs/post_production_profile.yaml `
  --stage all
```

Desteklenen aşamalar: `merge_chapters`, `extract_mermaid`, `render_mermaid`, `build_docx`, `build_html`, `build_epub`, `generate_qr`

### Markdown kalite kontrolü

```powershell
python -m tools.quality.check_chapter_markdown `
  --chapter .\chapters\chapter_01.md `
  --chapter-id chapter_01 --chapter-no 1 `
  --report .\build\test_reports\chapter_01_quality.md

# Sadece hataları filtrele
Select-String -Path .\build\test_reports\chapter_01_quality.md -Pattern "❌|FAIL"
```

---

## LLM entegrasyonu

### Modüler briefing sistemi

Büyük tek belge yerine senaryoya göre yüklenen modüler yapı:

| Dosya | Ne zaman yükle |
|---|---|
| `brief_core.md` | Her oturumda — ilk |
| `brief_llm_rules.md` | Her oturumda — ikinci |
| `brief_standards.md` | Bölüm üretiminde |
| `brief_structure.md` | Klasör işlemlerinde |
| `brief_environment.md` | Ortam sorunlarında |
| `brief_loading_order.md` | Aşama planlarken |

### Minimum başlangıç komutu

```
Aşağıdaki dosyalar Parametric Computer Book Factory v2.11.x çerçevesine aittir.

Önce `brief_core.md`, ardından `brief_llm_rules.md` dosyasını oku.
Kitap bağlamı için ilgili `brief_*context.md` dosyasını yükle.
Bölüm üretimi yapacaksan `brief_standards.md` dosyasını da oku.

Manifesti doğrula. Eksik alan varsa üretime geçmeden raporla.
Eksik bilgiyi tahmin etme — kullanıcıdan sor.
```

---

## Sürüm geçmişi

| Sürüm | Öne çıkan özellikler |
|---|---|
| **v2.11.x** | Modüler LLM briefing sistemi, workspace/framework ayrıştırması |
| **v2.9.x** | GitHub Codespaces desteği, `codespaces-init` CLI komutu |
| **v2.8.0** | Glossary/Index, Streamlit dashboard |
| **v2.7.0** | EPUB, tek sayfa HTML ve statik site export pipeline |
| **v2.6.0** | GitHub sync ve QR hardening |
| **v2.5.0** | CODE_META kod doğrulama hattı, CLI foundation |
| **v2.4.0** | Asset manifest örnekleri, chapter order güncelleme aracı |
| **v2.3.x** | Manifest doğrulama, paket bütünlük kontrolü, quickstart |
| **v2.1.0** | Post-production hattı (Mermaid, DOCX, Lua filter) |

---

## Katkı

Katkı sürecine başlamadan önce `CONTRIBUTING.md` dosyasını okuyun.

```powershell
# Geliştirme bağımlılıklarını kur
pip install -r requirements-dev.txt

# Testleri çalıştır
python -m bookfactory test-minimal --fail-on-error
```

---

## Lisans

MIT Lisansı — ayrıntılar için `LICENSE` dosyasına bakın.

---

**Yazar:** Prof. Dr. İsmail KIRBAŞ  
**Repo:** [github.com/bmdersleri/bookFactory](https://github.com/bmdersleri/bookFactory)  
**Bağlı kitap projesi:** [github.com/bmdersleri/react-web](https://github.com/bmdersleri/react-web)


## BookFactory Studio

Bu paket, mevcut CLI araçlarını bozmadan çalışan yerel bir web arayüzü içerir. Başlatmak için:

```powershell
python -m pip install -r requirements.txt
python -m bookfactory_studio.app
```

Ardından tarayıcıda `http://127.0.0.1:8765` adresini açın. Ayrıntılar için `docs/bookfactory_studio_mvp.md` dosyasına bakın.
