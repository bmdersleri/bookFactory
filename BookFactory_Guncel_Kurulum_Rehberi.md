# BookFactory Güncel Kurulum ve İlk Çalıştırma Rehberi

Bu dosya, **BookFactory / Parametric Computer Book Factory** projesinin güncel kurulum, kontrol ve ilk çalıştırma adımlarını tek yerde toplamak için hazırlanmıştır. Amaç, proje kökünde biriken eski sürüm notları, ara raporlar ve geçici Markdown dosyaları yerine kurulum için sade ve güvenilir bir ana başvuru dosyası kullanmaktır.

> Önerilen dosya adı: `SETUP.md`  
> Önerilen konum: `C:\OneDrive\OneDrive - mehmetakif.edu.tr\BookFactory\SETUP.md`

---

## 1. Kapsam

Bu rehber aşağıdaki bileşenleri kapsar:

- BookFactory Python paketi kurulumu
- Windows PowerShell ortam hazırlığı
- Python sanal ortam kurulumu
- Temel bağımlılıkların yüklenmesi
- Ortam doğrulama komutları
- React kitabı çalışma alanı için kod çıkarma, CODE_META doğrulama ve test akışı
- Markdown kalite kontrol akışı
- Opsiyonel DOCX/HTML/EPUB üretim bağımlılıkları
- Opsiyonel GitHub Codespaces, dashboard, QR ve code pages kontrolleri
- Proje kökündeki Markdown dosyalarını sadeleştirme önerisi

---

## 2. Proje kökü

Bu rehberde proje kökü aşağıdaki klasör kabul edilmiştir:

```powershell
C:\OneDrive\OneDrive - mehmetakif.edu.tr\BookFactory
```

Çalışmaya başlamadan önce PowerShell ile proje köküne geçin:

```powershell
cd "C:\OneDrive\OneDrive - mehmetakif.edu.tr\BookFactory"
```

Kök klasörde aşağıdaki dosya ve klasörlerin bulunması beklenir:

```text
bookfactory/
tools/
configs/
core/
docs/
examples/
workspace/
pyproject.toml
requirements.txt
requirements-dev.txt
README.md
```

React kitabı için özel çalışma alanı:

```text
workspace/react/
workspace/react/book_manifest.yaml
workspace/react/chapters/
workspace/react/prompts/
workspace/react/build/
workspace/react/configs/
```

---

## 3. Gerekli yazılımlar

### 3.1 Zorunlu temel bileşenler

| Bileşen | Önerilen durum | Amaç |
|---|---:|---|
| Python | 3.10 veya üzeri | BookFactory araçlarını çalıştırmak |
| pip | Güncel | Python paketlerini kurmak |
| PowerShell | Windows PowerShell 5.1 veya PowerShell 7+ | Betikleri çalıştırmak |

### 3.2 React kitabı ve kod testleri için önerilen bileşenler

| Bileşen | Amaç |
|---|---|
| Node.js | JavaScript/React kod bloklarını test etmek |
| npm | Mermaid CLI, Puppeteer ve Node tabanlı araçlar için |
| Git | Sürüm kontrolü, GitHub entegrasyonu ve Codespaces için |

### 3.3 Yayın sonrası üretim için opsiyonel bileşenler

| Bileşen | Amaç |
|---|---|
| Pandoc | Markdown → DOCX/HTML/EPUB üretimi |
| Mermaid CLI (`mmdc`) | Mermaid diyagramlarını PNG/SVG çıktıya dönüştürmek |
| Java JDK | Java kitapları veya Java kod testleri için |
| Streamlit | Yerel dashboard için |

Not: React kitabının Bölüm 1 kod doğrulama akışı için öncelikli dış bağımlılık `node` komutudur.

---

## 4. Python sanal ortam kurulumu

Proje kökünde sanal ortam oluşturun:

```powershell
python -m venv .venv
```

Sanal ortamı etkinleştirin:

```powershell
.\.venv\Scripts\Activate.ps1
```

PowerShell execution policy engeli alınırsa yalnızca geçerli kullanıcı için şu ayar yapılabilir:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Alternatif olarak tek komutluk bypass kullanılabilir:

```powershell
powershell -ExecutionPolicy Bypass -File .\ilgili_betik.ps1
```

pip güncelleyin:

```powershell
python -m pip install --upgrade pip
```

---

## 5. BookFactory paket kurulumu

Temel kurulum:

```powershell
pip install -r requirements.txt
pip install -e .
```

Geliştirme, test ve dashboard bileşenleriyle kurulum:

```powershell
pip install -r requirements-dev.txt
pip install -e ".[dashboard,dev,ci]"
```

Kurulumu kontrol edin:

```powershell
python -m bookfactory version
```

Beklenen çıktı örneği:

```text
2.11.0
```

---

## 6. UTF-8 uyumluluğu

Windows ortamında Türkçe karakterlerin bozulmaması için gerektiğinde oturum bazında şu ayarlar kullanılabilir:

```powershell
chcp 65001
$env:PYTHONUTF8="1"
$env:PYTHONIOENCODING="utf-8"
```

Projede `install_v2_11_2_utf8_subprocess_hotfix.ps1` dosyası bulunuyorsa ve daha önce uygulanmadıysa proje kökünde şu şekilde çalıştırılabilir:

```powershell
powershell -ExecutionPolicy Bypass -File .\install_v2_11_2_utf8_subprocess_hotfix.ps1
```

Bu düzeltme özellikle Node.js veya Python alt süreçlerinden dönen `KampüsHub` gibi Türkçe karakterli çıktıların yanlış okunmasını engellemek içindir.

---

## 7. Ortam kontrolü

Önce yumuşak kontrol çalıştırın:

```powershell
python -m bookfactory doctor --soft
```

Alternatif doğrudan araç komutu:

```powershell
python tools/check_environment.py --soft
```

Bu kontrol şu araçları raporlar:

```text
python
pandoc
mmdc
node
npm
java
git
puppeteer/chrome
```

Eksik araçların tamamı her iş akışı için kritik değildir. Örneğin yalnızca React Bölüm 1 kod testleri yapılacaksa Pandoc veya Mermaid eksikliği kritik değildir.

---

## 8. Paket bütünlük kontrolü

Proje dosya bütünlüğünü kontrol etmek için:

```powershell
python tools/check_package_integrity.py .
```

CLI üzerinden temel komutların çalışıp çalışmadığını görmek için:

```powershell
python -m bookfactory version
python -m bookfactory doctor --soft
```

---

## 9. Manifest doğrulama

Genel örnek manifest doğrulama:

```powershell
python -m bookfactory validate --manifest .\manifests\java_fundamentals_manifest.yaml
```

React kitabı manifest doğrulama:

```powershell
python -m bookfactory validate --manifest .\workspace\react\book_manifest.yaml
```

Manifest, kitap üretiminde tek doğruluk kaynağı kabul edilmelidir.

---

## 10. React kitabı kod doğrulama akışı

React kitabı için ana bölüm klasörü:

```text
workspace/react/chapters
```

Bölüm 1 dosyası:

```text
workspace/react/chapters/chapter_01_modern_web_giris.md
```

### 10.1 CODE_META bloklarını çıkarma

```powershell
python -m tools.code.extract_code_blocks `
  --package-root . `
  --out-dir .\workspace\react\build\code `
  --manifest .\workspace\react\build\code_manifest.json `
  --yaml-manifest .\workspace\react\build\code_manifest.yaml `
  --chapters-dir .\workspace\react\chapters
```

### 10.2 CODE_META doğrulama

```powershell
python -m tools.code.validate_code_meta `
  .\workspace\react\build\code_manifest.json `
  --package-root .
```

### 10.3 Kod testlerini çalıştırma

```powershell
python -m tools.code.run_code_tests `
  --manifest .\workspace\react\build\code_manifest.json `
  --package-root . `
  --report-json .\workspace\react\build\test_reports\code_test_report.json `
  --report-md .\workspace\react\build\test_reports\code_test_report.md `
  --node node `
  --fail-on-error
```

Başarılı Bölüm 1 çıktısı şu yapıda olmalıdır:

```text
Total: 3 | Passed: 3 | Failed: 0 | Skipped: 0
```

---

## 11. React kitabı temiz kod test akışı

Projede `tools/react_clean_rebuild.ps1` dosyası varsa temiz kod test akışı için şu komut kullanılabilir:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\react_clean_rebuild.ps1
```

Bu betik şunları yapar:

1. `workspace/react/build/code` klasörünü temizler.
2. Eski kod test raporlarını temizler.
3. CODE_META bloklarını yeniden çıkarır.
4. Metadata doğrulaması yapar.
5. Kod testlerini yeniden çalıştırır.

---

## 12. Markdown kalite kontrol akışı

Bölüm 1 kalite kontrolü için:

```powershell
python -m tools.quality.check_chapter_markdown `
  --chapter .\workspace\react\chapters\chapter_01_modern_web_giris.md `
  --chapter-id chapter_01 `
  --chapter-no 1 `
  --report .\workspace\react\build\test_reports\chapter_01_markdown_quality_report.md
```

Hata ve uyarı filtreleme:

```powershell
Select-String `
  -Path .\workspace\react\build\test_reports\chapter_01_markdown_quality_report.md `
  -Pattern "❌|⚠️|FAIL|WARN"
```

Hedef kalite sonucu:

```text
FAIL: 0
```

`Server Components`, `GraphQL`, `React Native` gibi ifadeler yalnızca kapsam dışı konu notu olarak geçiyorsa pedagojik uyarı kabul edilebilir; kritik hata sayılmamalıdır.

---

## 13. DOCX / HTML / EPUB üretimi

Yayın sonrası üretim için profil dosyası gerekir. React kitabı için örnek profil:

```text
workspace/react/configs/post_production_profile_react.yaml
```

Dry-run kontrol:

```powershell
python -m bookfactory build `
  --profile .\workspace\react\configs\post_production_profile_react.yaml `
  --dry-run
```

Gerçek üretim:

```powershell
python -m bookfactory build `
  --profile .\workspace\react\configs\post_production_profile_react.yaml
```

Export komutu:

```powershell
python -m bookfactory export `
  --profile .\workspace\react\configs\post_production_profile_react.yaml `
  --format all `
  --merge-if-missing
```

DOCX üretimi için Pandoc kurulmuş olmalıdır. Mermaid diyagramlarından görsel üretilecekse `mmdc` de kurulmalıdır.

---

## 14. Mermaid CLI kurulumu

Mermaid CLI gerekiyorsa Node.js kurulu olduktan sonra:

```powershell
npm install -g @mermaid-js/mermaid-cli
```

Kontrol:

```powershell
mmdc --version
```

Puppeteer/Chrome sorunlarında ortam kontrolü tekrar çalıştırılmalıdır:

```powershell
python -m bookfactory doctor --soft
```

---

## 15. Pandoc kurulumu kontrolü

Pandoc kurulum kontrolü:

```powershell
pandoc --version
```

Pandoc sistem PATH içinde değilse `.env` veya PowerShell oturumunda yol belirtilebilir:

```powershell
$env:PANDOC_BIN="C:\Program Files\Pandoc\pandoc.exe"
```

---

## 16. GitHub Codespaces kontrolü

Codespaces dosyalarını oluşturmak veya güncellemek için:

```powershell
python -m bookfactory codespaces-init --force
```

Kontrol:

```powershell
python -m bookfactory codespaces-check --fail-on-error
```

Raporlar varsayılan olarak şu konuma yazılır:

```text
build/codespaces_check_report.json
build/codespaces_check_report.md
```

---

## 17. Dashboard kontrolü

Dashboard bağımlılıkları kuruluysa:

```powershell
python -m bookfactory dashboard --check
```

Dashboard çalıştırma:

```powershell
python -m bookfactory dashboard `
  --profile .\workspace\react\configs\post_production_profile_react.yaml
```

Streamlit eksikse:

```powershell
pip install streamlit
```

---

## 18. GitHub kod senkronizasyonu, code pages ve QR akışı

Kod testleri başarılı olduktan sonra GitHub uyumlu kod klasörü hazırlanabilir.

Örnek:

```powershell
python -m bookfactory sync-github `
  --code-manifest .\workspace\react\build\code_manifest.json `
  --test-report .\workspace\react\build\test_reports\code_test_report.json `
  --out-dir .\workspace\react\build\github_repo `
  --owner bmdersleri `
  --repo react-web-programlama `
  --branch main `
  --code-root kodlar `
  --pages-root docs/kodlar `
  --folder-style numbered `
  --require-tests-passed `
  --clean
```

Code pages üretimi:

```powershell
python -m bookfactory render-code-pages `
  --manifest .\workspace\react\build\code_manifest_github.json `
  --test-report .\workspace\react\build\test_reports\code_test_report.json `
  --out-dir .\workspace\react\build\code_pages `
  --clean
```

QR manifest üretimi:

```powershell
python -m bookfactory qr-from-code `
  --code-manifest .\workspace\react\build\code_manifest_github.json `
  --output .\workspace\react\build\qr_manifest.yaml `
  --output-prefix assets/auto/qr
```

QR görsellerini üretmek için:

```powershell
python .\tools\postproduction\generate_qr_codes.py `
  --manifest .\workspace\react\build\qr_manifest.yaml `
  --output-dir .\workspace\react\assets\auto\qr `
  --report .\workspace\react\build\test_reports\qr_generation_report.md
```

---

## 19. Proje kökündeki Markdown dosyalarını sadeleştirme önerisi

Proje kökünde çok sayıda eski sürüm notu, rapor ve geçici Markdown dosyası birikmiş olabilir. Kurulum açısından kök dizinde yalnızca şu dosyaların kalması yeterlidir:

```text
README.md
SETUP.md
CHANGELOG.md
LLM_PROJECT_BRIEF.md
RELEASE_CHECKLIST.md
```

Aşağıdaki türde dosyalar `docs/archive/` veya `arsiv/` altına taşınabilir:

```text
RELEASE_NOTES_v*.md
BookFactory_v*_Degisiklik_Raporu.md
BookFactory_v*_Kurulum_ve_Kullanim_Kilavuzu.md
v*_test_report.md
devam_promptu.md
geçici kalite kontrol raporları
eski düzeltme açıklamaları
```

Ancak aşağıdaki dosyalar doğrudan silinmemelidir:

```text
README.md
SETUP.md
usage.md veya docs/usage.md
LLM_PROJECT_BRIEF.md veya docs/LLM_PROJECT_BRIEF.md
core/*.md
docs/*.md
workspace/react/chapters/*.md
workspace/react/prompts/**/*.md
```

Temizlik işlemi yapılacaksa önce rapor üreten güvenli temizlik betiği çalıştırılmalıdır:

```powershell
powershell -ExecutionPolicy Bypass -File .\cleanup_bookfactory_project.ps1
```

Rapor kontrol edildikten sonra silmek yerine karantinaya taşıma tercih edilmelidir:

```powershell
powershell -ExecutionPolicy Bypass -File .\cleanup_bookfactory_project.ps1 -MoveToQuarantine
```

Kalıcı silme ancak rapor manuel kontrol edildikten sonra yapılmalıdır.

---

## 20. Önerilen ilk kurulumdan sonra kontrol sırası

Yeni veya temizlenmiş bir BookFactory klasöründe önerilen kontrol sırası:

```powershell
cd "C:\OneDrive\OneDrive - mehmetakif.edu.tr\BookFactory"

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
pip install -e ".[dashboard,dev,ci]"

python -m bookfactory version
python -m bookfactory doctor --soft
python tools/check_package_integrity.py .
python -m bookfactory validate --manifest .\workspace\react\book_manifest.yaml
```

React Bölüm 1 için hızlı kontrol:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\react_clean_rebuild.ps1

python -m tools.quality.check_chapter_markdown `
  --chapter .\workspace\react\chapters\chapter_01_modern_web_giris.md `
  --chapter-id chapter_01 `
  --chapter-no 1 `
  --report .\workspace\react\build\test_reports\chapter_01_markdown_quality_report.md
```

Başarı ölçütleri:

```text
CODE_META validation: OK
Total: 3 | Passed: 3 | Failed: 0 | Skipped: 0
Markdown quality: FAIL: 0
```

---

## 21. Sık karşılaşılan sorunlar

### 21.1 Execution Policy hatası

Belirti:

```text
File ... cannot be loaded because running scripts is disabled on this system.
```

Çözüm:

```powershell
powershell -ExecutionPolicy Bypass -File .\script_adi.ps1
```

veya:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 21.2 Türkçe karakter bozulması

Belirti:

```text
KampÃ¼sHub
```

Çözüm:

```powershell
chcp 65001
$env:PYTHONUTF8="1"
$env:PYTHONIOENCODING="utf-8"
```

Gerekiyorsa hotfix:

```powershell
powershell -ExecutionPolicy Bypass -File .\install_v2_11_2_utf8_subprocess_hotfix.ps1
```

### 21.3 `node` bulunamadı

Belirti:

```text
node is not recognized
```

Çözüm:

1. Node.js LTS sürümünü kurun.
2. PowerShell penceresini kapatıp yeniden açın.
3. Kontrol edin:

```powershell
node --version
npm --version
```

### 21.4 Pandoc bulunamadı

Belirti:

```text
pandoc: MISSING
```

Çözüm:

Pandoc kurulumundan sonra:

```powershell
pandoc --version
```

DOCX/EPUB üretmeyecekseniz bu eksiklik React kod testleri için kritik değildir.

### 21.5 CODE_META doğrulama hatası

Kontrol edilecekler:

- `CODE_META` bilgisi çalıştırılabilir kod bloğunun içine yazılmamalıdır.
- Metadata, kod bloğundan hemen önce HTML yorum bloğu olarak yer almalıdır.
- Kod bloğu dili doğru olmalıdır: `javascript`, `jsx`, `tsx`, `python`, `java` vb.
- `expected_stdout` ile gerçek çıktı birebir uyumlu olmalıdır.

---

## 22. Önerilen günlük çalışma akışı

React kitabı üzerinde her bölüm güncellemesinden sonra:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\react_clean_rebuild.ps1
```

Sonra ilgili bölüm için Markdown kalite kontrolü:

```powershell
python -m tools.quality.check_chapter_markdown `
  --chapter .\workspace\react\chapters\chapter_XX_dosya_adi.md `
  --chapter-id chapter_XX `
  --chapter-no XX `
  --report .\workspace\react\build\test_reports\chapter_XX_markdown_quality_report.md
```

Büyük değişikliklerden sonra:

```powershell
python -m bookfactory doctor --soft
python tools/check_package_integrity.py .
python -m bookfactory validate --manifest .\workspace\react\book_manifest.yaml
```

---

## 23. Kurulum tamamlandıktan sonra beklenen durum

Başarılı bir kurulumdan sonra aşağıdaki komutlar çalışmalıdır:

```powershell
python -m bookfactory version
python -m bookfactory doctor --soft
python -m bookfactory validate --manifest .\workspace\react\book_manifest.yaml
powershell -ExecutionPolicy Bypass -File .\tools\react_clean_rebuild.ps1
```

React Bölüm 1 için beklenen çıktı:

```text
Extracted CODE_META blocks: 3
CODE_META validation: OK
Total: 3 | Passed: 3 | Failed: 0 | Skipped: 0
```

Markdown kalite kontrol hedefi:

```text
FAIL: 0
```

---

## 24. Notlar

- `workspace/react/build/` içeriği üretim çıktısıdır; gerektiğinde yeniden oluşturulabilir.
- `__pycache__/`, `.pyc`, `.bak`, `.tmp`, `.log` dosyaları kalıcı kaynak değildir.
- `workspace/react/chapters/` altındaki bölüm Markdown dosyaları kaynak kabul edilmelidir.
- `workspace/react/prompts/` altındaki bölüm girdi promptları korunmalıdır.
- Temizlik yapılırken silme yerine önce karantina yaklaşımı tercih edilmelidir.

