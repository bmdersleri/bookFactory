# BookFactory React Kitabı Detaylı Kullanım Kılavuzu

**Proje:** BookFactory / Parametric Computer Book Factory  
**Kitap:** React ile Web Uygulama Geliştirme  
**Yazar:** Prof. Dr. İsmail KIRBAŞ  
**Ana örnek uygulama:** KampüsHub  
**Önerilen proje kökü:** `C:\OneDrive\OneDrive - mehmetakif.edu.tr\BookFactory`  
**Önerilen terminal:** PowerShell 7.x / `pwsh`  

---

## 1. Bu kılavuzun amacı

Bu belge, React kitabı üretim sürecinde BookFactory klasörünün nasıl kullanılacağını, bölüm üretiminde hangi dosyaların esas alınacağını, kod testlerinin nasıl çalıştırılacağını, Markdown kalite kontrolünün nasıl yapılacağını ve geçici dosyaların nasıl yönetileceğini adım adım açıklamak için hazırlanmıştır.

Bu kılavuz özellikle Bölüm 2’ye geçmeden önce çalışma düzenini sabitlemek için kullanılmalıdır. Amaç, her bölümde aynı üretim ve kontrol protokolünü uygulayarak kitabın bütünlüğünü, kodların çalışabilirliğini, ekran görüntüsü planlarının izlenebilirliğini ve çıktıların tekrar üretilebilirliğini güvence altına almaktır.

---

## 2. Temel çalışma ilkeleri

BookFactory ile çalışırken aşağıdaki ilkeler korunmalıdır:

1. **Tek doğruluk kaynağı manifesttir.** React kitabı için ana manifest dosyası `workspace/react/book_manifest.yaml` dosyasıdır.
2. **Bölüm metinleri yalnızca `workspace/react/chapters/` altında tutulmalıdır.** Build, test ve rapor klasörleri kaynak metin olarak kabul edilmemelidir.
3. **Kod blokları metadata ile yönetilmelidir.** Çalıştırılabilir her kod bloğundan önce `CODE_META` HTML yorum bloğu bulunmalıdır.
4. **Kod bloğu içine metadata yazılmamalıdır.** `// CODE_META` gibi kullanım hatalıdır.
5. **Her bölüm kalite kontrolünden geçmelidir.** Markdown yapısı, başlık düzeni, screenshot marker’ları ve CODE_META yerleşimi kontrol edilmelidir.
6. **Her bölümde kod testleri tekrar çalıştırılmalıdır.** Kod blokları yalnızca metin olarak değil, çalıştırılabilir örnekler olarak ele alınmalıdır.
7. **Build klasörü üretilebilir çıktı alanıdır.** Silinebilir; kaynak kabul edilmemelidir.
8. **Eski raporlar ve geçici Markdown dosyaları arşive taşınmalıdır.** Kök dizin gereksiz `.md` dosyalarıyla şişirilmemelidir.

---

## 3. Önerilen klasör yapısı

BookFactory ana klasöründe sadeleştirilmiş yapı şu şekilde tutulmalıdır:

```text
BookFactory/
  README.md
  SETUP.md
  CHANGELOG.md
  LLM_PROJECT_BRIEF.md
  RELEASE_CHECKLIST.md
  pyproject.toml
  requirements.txt
  requirements-dev.txt

  core/
  configs/
  docs/
  examples/
  manifests/
  schemas/
  templates/
  tests/
  tools/

  workspace/
    react/
      book_manifest.yaml
      chapters/
      prompts/
      configs/
      assets/
      build/
      exports/
      chapter_backups/

  docs/
    archive/

  cleanup_reports/
```

### 3.1. React kitabı için kritik klasörler

| Klasör | Amaç |
|---|---|
| `workspace/react/chapters/` | Bölüm Markdown dosyaları |
| `workspace/react/prompts/` | Bölüm girdi promptları ve kitap özel promptları |
| `workspace/react/assets/screenshots/` | Programatik veya manuel ekran görüntüleri |
| `workspace/react/build/code/` | Kod bloklarından çıkarılan çalıştırılabilir dosyalar |
| `workspace/react/build/test_reports/` | Kod testi ve kalite kontrol raporları |
| `workspace/react/exports/` | DOCX, HTML, EPUB, PDF gibi nihai çıktılar |
| `workspace/react/chapter_backups/` | Bölüm düzeltmeleri öncesi alınan yedekler |

---

## 4. VS Code ve PowerShell çalışma düzeni

### 4.1. VS Code terminal profili

VS Code içinde terminal olarak PowerShell 7 kullanılmalıdır. Terminalde şu komut çalıştırıldığında sürüm 7.x görünmelidir:

```powershell
$PSVersionTable.PSVersion
```

Beklenen çıktı örneği:

```text
Major  Minor  Patch
-----  -----  -----
7      6      1
```

### 4.2. Komutlarda `pwsh` kullanımı

PowerShell 7 ile script çalıştırmak için şu biçim tercih edilmelidir:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\script_adi.ps1
```

Örneğin:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\archive_legacy_bookfactory_md_pwsh7.ps1 -Apply
```

### 4.3. Proje köküne geçiş

Her çalışmaya şu komutla başlanmalıdır:

```powershell
cd "C:\OneDrive\OneDrive - mehmetakif.edu.tr\BookFactory"
```

Proje kökünde olduğunuzu kontrol etmek için:

```powershell
Get-ChildItem
```

Şu dosya ve klasörlerden bazıları görünmelidir:

```text
workspace
core
tools
README.md
pyproject.toml
requirements.txt
```

---

## 5. Ortam kurulumu ve kontrolü

### 5.1. Python sanal ortamı

İlk kurulumda veya temiz ortamda:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .
```

PowerShell yürütme politikası engellerse:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 5.2. Python modüllerini kontrol etme

```powershell
python --version
python -m pip --version
python -m bookfactory --help
```

### 5.3. Node.js kontrolü

React bölümlerindeki JavaScript örnekleri için Node.js gereklidir:

```powershell
node --version
npm --version
```

### 5.4. BookFactory ortam kontrolü

```powershell
python -m tools.check_environment
```

Bu komut sistemdeki temel bağımlılıkları ve çalışma ortamını kontrol etmek için kullanılabilir.

---

## 6. React kitabı üretim mantığı

React kitabı kümülatif proje yaklaşımıyla yazılır. Ana proje **KampüsHub** uygulamasıdır. Her bölümde uygulamaya yeni bir kavram veya modül eklenir.

Örnek ilerleme:

| Bölüm | Odak | KampüsHub katkısı |
|---:|---|---|
| 1 | Modern web, ortam kurulumu, Vite, CODE_META | Proje iskeleti ve temel çalışma disiplini |
| 2 | React bileşen mantığı, JSX, props | İlk arayüz bileşenleri |
| 3 | State ve event yönetimi | Etkileşimli duyuru/not alanları |
| 4 | Listeleme ve koşullu render | Ders ve etkinlik listeleri |
| 5 | Formlar | Duyuru veya not ekleme formları |
| 6+ | Routing, veri yönetimi, API, test, dağıtım | Tam KampüsHub uygulaması |

Her bölüm bir önceki bölümün çıktılarını bozmadan ilerlemelidir.

---

## 7. Bölüm üretim iş akışı

Her bölüm için önerilen standart akış şudur:

```text
1. Bölüm girdi promptunu kontrol et.
2. Bölüm Markdown dosyasını üret veya güncelle.
3. CODE_META bloklarını kontrol et.
4. Kod bloklarını çıkar.
5. CODE_META manifestini doğrula.
6. Kod testlerini çalıştır.
7. Markdown kalite kontrolünü çalıştır.
8. Screenshot marker ve manifest uyumunu kontrol et.
9. Gerekirse düzeltme scripti hazırla.
10. Raporları arşivle veya build altında tut.
11. Bölümü onayla.
12. Sonraki bölüme geç.
```

---

## 8. Bölüm dosyası standardı

Bölüm dosyaları şu klasörde bulunmalıdır:

```text
workspace/react/chapters/
```

Dosya adlandırma standardı:

```text
chapter_XX_kisa_aciklayici_ad.md
```

Örnekler:

```text
chapter_01_modern_web_giris.md
chapter_02_react_bilesenleri_jsx.md
chapter_03_state_event_yonetimi.md
```

Bölüm dosyasında yalnızca bir adet H1 başlığı olmalıdır:

```markdown
# Bölüm 2: React Bileşenleri, JSX ve Props
```

Bölüm içinde README taslağı, örnek Markdown metni veya kullanıcıya gösterilecek doküman parçası varsa bunlar gerçek H1/H2 olarak yazılmamalıdır. Kod veya metin bloğu içinde sunulmalı ya da düz metin biçiminde verilmelidir.

---

## 9. CODE_META standardı

### 9.1. Doğru kullanım

Çalıştırılabilir her kod bloğundan önce HTML yorum bloğu içinde `CODE_META` bulunmalıdır:

```markdown
<!-- CODE_META
{
  "id": "react_ch02_code01",
  "chapter": "chapter_02",
  "language": "javascript",
  "filename": "kampushub_baslik.js",
  "runnable": true,
  "expected_output": "KampüsHub"
}
-->

```javascript
console.log("KampüsHub");
```
```

### 9.2. Hatalı kullanım

Aşağıdaki kullanım hatalıdır:

```javascript
// CODE_META: { "id": "react_ch02_code01" }
console.log("KampüsHub");
```

Çünkü metadata çalıştırılabilir JavaScript kodunun içine yorum satırı olarak yerleştirilmiştir. Bu durum kod çıkarma, test ve kalite kontrol süreçlerini bozabilir.

### 9.3. ID standardı

React kitabı için önerilen ID biçimi:

```text
react_chXX_codeYY
```

Örnekler:

```text
react_ch02_code01
react_ch02_code02
react_ch03_code01
```

---

## 10. Kod çıkarma ve test komutları

React kitabı için kod bloklarını çıkarmak:

```powershell
python -m tools.code.extract_code_blocks `
  --package-root . `
  --out-dir .\workspace\react\build\code `
  --manifest .\workspace\react\build\code_manifest.json `
  --yaml-manifest .\workspace\react\build\code_manifest.yaml `
  --chapters-dir .\workspace\react\chapters
```

CODE_META doğrulaması:

```powershell
python -m tools.code.validate_code_meta `
  .\workspace\react\build\code_manifest.json `
  --package-root .
```

Kod testleri:

```powershell
python -m tools.code.run_code_tests `
  --manifest .\workspace\react\build\code_manifest.json `
  --package-root . `
  --report-json .\workspace\react\build\test_reports\code_test_report.json `
  --report-md .\workspace\react\build\test_reports\code_test_report.md `
  --node node `
  --fail-on-error
```

Başarılı sonuç örneği:

```text
Total: 3 | Passed: 3 | Failed: 0 | Skipped: 0
```

---

## 11. Markdown kalite kontrolü

Her bölüm için Markdown kalite kontrolü çalıştırılmalıdır.

Bölüm 1 örneği:

```powershell
python -m tools.quality.check_chapter_markdown `
  --chapter .\workspace\react\chapters\chapter_01_modern_web_giris.md `
  --chapter-id chapter_01 `
  --chapter-no 1 `
  --report .\workspace\react\build\test_reports\chapter_01_markdown_quality_report.md
```

Bölüm 2 için önerilen komut:

```powershell
python -m tools.quality.check_chapter_markdown `
  --chapter .\workspace\react\chapters\chapter_02_react_bilesenleri_jsx.md `
  --chapter-id chapter_02 `
  --chapter-no 2 `
  --report .\workspace\react\build\test_reports\chapter_02_markdown_quality_report.md
```

Hata ve uyarıları filtrelemek için:

```powershell
Select-String `
  -Path .\workspace\react\build\test_reports\chapter_02_markdown_quality_report.md `
  -Pattern "❌|⚠️|FAIL|WARN"
```

Başarı hedefi:

```text
FAIL: 0
```

Uyarılar pedagojik kapsam notu, ileri konu uyarısı veya bilinçli dışlama açıklaması düzeyindeyse kritik kabul edilmeyebilir. Ancak H1 fazlalığı, CODE_META hatası, eksik screenshot marker’ı veya bozuk kod bloğu kritik kabul edilmelidir.

---

## 12. Screenshot planı standardı

Her bölümde en az bir programatik ekran çıktısı planlanmalıdır. Görsel ağırlıklı bölümlerde 2–4 screenshot önerilir.

Markdown içindeki marker standardı:

```text
[SCREENSHOT:b02_01_kampushub_ana_bilesen]
```

Önerilen ID biçimi:

```text
bXX_YY_aciklayici_ad
```

Örnekler:

```text
[SCREENSHOT:b02_01_jsx_baslik_bileseni]
[SCREENSHOT:b02_02_props_ile_kart_bileseni]
[SCREENSHOT:b02_03_kampushub_bilesen_agaci]
```

Her screenshot için manifestte veya bölüm içinde şu bilgiler planlanmalıdır:

| Alan | Açıklama |
|---|---|
| `id` | Screenshot benzersiz kimliği |
| `chapter` | Bölüm numarası veya bölüm ID’si |
| `figure` | Şekil numarası |
| `title` | Kısa başlık |
| `route` | Uygulama rotası, örn. `/__book__/chapter-02/example-01` |
| `waitFor` | Ekran hazır olduğunda beklenecek seçici/metin |
| `actions` | Tıklama, yazma, seçim gibi işlemler |
| `output` | Üretilecek görsel dosya yolu |
| `caption` | Kitaba girecek şekil açıklaması |
| `markdownTarget` | Markdown içindeki marker |

---

## 13. Bölüm 2’ye geçiş için özel kontrol listesi

Bölüm 2’ye başlamadan önce Bölüm 1 için şu kontroller tamamlanmış olmalıdır:

| Kontrol | Beklenen durum |
|---|---|
| Bölüm 1 Markdown dosyası | `workspace/react/chapters/chapter_01_modern_web_giris.md` mevcut |
| H1 sayısı | 1 |
| `// CODE_META` kullanımı | Yok |
| CODE_META blokları | HTML yorum bloğu biçiminde |
| Kod testi | Passed |
| Markdown kalite kontrolü | `FAIL: 0` |
| Screenshot marker’ları | Mevcut ve isimlendirme standardına uygun |
| Eski raporlar | Gerekirse `docs/archive/` altına taşınmış |
| VS Code terminali | PowerShell 7.x / `pwsh` |

Bölüm 2’ye başlarken önerilen dosya adı:

```text
workspace/react/chapters/chapter_02_react_bilesenleri_jsx.md
```

Bölüm 2 için önerilen ana başlık:

```markdown
# Bölüm 2: React Bileşenleri, JSX ve Props
```

Bölüm 2’de yer alması beklenen asgari bileşenler:

```text
- React bileşeni kavramı
- JSX sözdizimi
- Props mantığı
- Bileşenlerin parçalanması
- KampüsHub için Header, AnnouncementCard veya ModuleCard örneği
- En az 3 çalıştırılabilir CODE_META örneği
- En az 2 screenshot marker’ı
- Kavramsal sorular
- Programlama alıştırmaları
- Haftalık laboratuvar görevi
```

---

## 14. Geçici dosyaları ve eski Markdown dosyalarını yönetme

Kök dizinde gereksiz Markdown dosyaları birikmemelidir. Kalıcı tutulması önerilen ana Markdown dosyaları:

```text
README.md
SETUP.md
CHANGELOG.md
LLM_PROJECT_BRIEF.md
RELEASE_CHECKLIST.md
```

Eski sürüm notları, geçici promptlar, test raporları ve ara açıklamalar arşive taşınabilir.

Önce rapor üretmek için:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\archive_legacy_bookfactory_md_pwsh7.ps1
```

Raporu kontrol ettikten sonra taşıma yapmak için:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\archive_legacy_bookfactory_md_pwsh7.ps1 -Apply
```

Build/test raporlarını da arşivlemek için:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\archive_legacy_bookfactory_md_pwsh7.ps1 -IncludeBuildReports -Apply
```

Koruma listesinde olmayan tüm kök Markdown dosyalarını da arşivlemek için:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\archive_legacy_bookfactory_md_pwsh7.ps1 -ArchiveUnprotectedRootMarkdown -Apply
```

Arşiv hedefi:

```text
docs/archive/archive_md_YYYYMMDD_HHMMSS/
```

---

## 15. Build çıktılarının temizlenmesi

Build çıktıları tekrar üretilebilir dosyalardır. Temizlik için önce rapor üretilmelidir:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\cleanup_bookfactory_project.ps1
```

Karantinaya taşımak için:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\cleanup_bookfactory_project.ps1 -MoveToQuarantine
```

Build çıktıları da dahil edilecekse:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\cleanup_bookfactory_project.ps1 -IncludeBuildOutputs -MoveToQuarantine
```

Kalıcı silme ancak rapor kontrolünden sonra yapılmalıdır:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\cleanup_bookfactory_project.ps1 -Delete
```

Öneri: Bölüm üretim sürecinde doğrudan `-Delete` yerine önce `-MoveToQuarantine` kullanılmalıdır.

---

## 16. Sürüm kontrolü ve Git önerisi

BookFactory klasörü Git ile takip ediliyorsa her kritik aşamada commit alınmalıdır.

Önerilen commit noktaları:

```text
1. Bölüm promptu hazırlandı
2. Bölüm Markdown dosyası üretildi
3. Kod testleri geçti
4. Markdown kalite kontrolü geçti
5. Screenshot planı eklendi
6. Bölüm onaylandı
```

Örnek Git komutları:

```powershell
git status
git add workspace/react/chapters/chapter_02_react_bilesenleri_jsx.md
git add workspace/react/build/test_reports/chapter_02_markdown_quality_report.md
git commit -m "Add React book chapter 02 draft and quality report"
```

Build çıktıları Git’e alınacaksa bilinçli alınmalıdır. Genellikle `workspace/react/build/code_manifest.json`, kalite raporları ve nihai export çıktıları takip edilebilir; geçici kod çıkarma klasörleri ve cache dosyaları takip edilmemelidir.

---

## 17. Dev Container ve Codespaces notu

VS Code, proje içinde `.devcontainer/devcontainer.json` dosyası gördüğünde şu uyarıyı gösterebilir:

```text
Folder contains a Dev Container configuration file. Reopen folder to develop in a container.
```

Yerel Windows + PowerShell 7 iş akışı sorunsuz çalışıyorsa container’a geçmek zorunlu değildir. Bu uyarı için günlük kullanımda `Don't Show Again` seçilebilir.

Dev Container veya GitHub Codespaces şu durumlarda yararlıdır:

```text
- Her kullanıcıda aynı Python/Node/Pandoc ortamını sağlamak
- Docker tabanlı izole test hattı kurmak
- GitHub üzerinden tarayıcıda geliştirme yapmak
- Eğitim ortamında kurulum farklılıklarını azaltmak
```

Codespaces kontrolü için ilgili araçlar `tools/cloud/` altında yer alır.

---

## 18. Dashboard kullanımı

BookFactory içinde yerel dashboard desteği varsa şu komutla çalıştırılabilir:

```powershell
python -m tools.dashboard.local_dashboard
```

Dashboard; manifest, bölüm durumu, kod testleri, QR/code pages çıktıları veya kalite raporlarını izlemek için kullanılabilir. Dashboard kullanımında kaynak dosyalar yine `workspace/react/chapters/` altında kalmalı; dashboard yalnızca izleme ve raporlama aracı olarak düşünülmelidir.

---

## 19. DOCX / HTML / EPUB çıktı üretimi

Kitap veya bölüm çıktıları için export araçları `tools/export/` ve `tools/postproduction/` altında yer alır.

Genel export mantığı:

```text
1. Bölümler Markdown olarak tamamlanır.
2. Gerekirse bölümler birleştirilir.
3. Mermaid görselleri ve manuel görseller çözülür.
4. Kod bağlantıları, QR ve GitHub/code pages entegrasyonları uygulanır.
5. Pandoc veya export scriptleriyle DOCX/HTML/EPUB üretilir.
6. DOCX son biçimlendirme düzeltmeleri uygulanır.
```

React kitabı henüz bölüm üretim aşamasındaysa, nihai export işlemini tüm kritik bölümler kalite kontrolünden geçtikten sonra yapmak daha sağlıklıdır.

---

## 20. Sık karşılaşılan sorunlar

### 20.1. PowerShell script çalışmıyor

Çözüm:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\script_adi.ps1
```

Kalıcı çözüm:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 20.2. Türkçe karakterler bozuk görünüyor

PowerShell profilinize şu satırları ekleyin:

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
```

Profil dosyasını açmak için:

```powershell
notepad $PROFILE
```

### 20.3. Kalite kontrol H1 hatası veriyor

Bölüm dosyasında yalnızca bir H1 bulunmalıdır. Kontrol:

```powershell
Select-String `
  -Path .\workspace\react\chapters\chapter_02_react_bilesenleri_jsx.md `
  -Pattern "^\s*# " `
  -Context 0,2
```

### 20.4. `// CODE_META` hatası veriyor

Kontrol:

```powershell
Select-String `
  -Path .\workspace\react\chapters\chapter_02_react_bilesenleri_jsx.md `
  -Pattern "// CODE_META" `
  -Context 3,3
```

Çözüm: Metadata kod bloğundan önce HTML yorum bloğuna alınmalıdır.

### 20.5. Kod testi başarısız oluyor

Şu sırayla kontrol edilmelidir:

```text
1. CODE_META id benzersiz mi?
2. filename doğru mu?
3. language doğru mu?
4. expected_output gerçek çıktı ile aynı mı?
5. Kod Node.js ile çalıştırılabilir mi?
6. Kod örneği tarayıcı API’si kullanıyor mu?
7. Kod örneği React/Vite ortamı gerektiriyorsa test tipi buna göre ayarlandı mı?
```

---

## 21. Bölüm onay formu

Her bölüm sonunda aşağıdaki kısa form doldurulabilir:

```markdown
## Bölüm Onay Formu

- Bölüm dosyası: `workspace/react/chapters/chapter_XX_....md`
- H1 sayısı: 1
- CODE_META blok sayısı: ...
- Kod testi sonucu: Passed / Failed
- Markdown kalite kontrol sonucu: FAIL: 0 / FAIL var
- Screenshot marker sayısı: ...
- Kapsam dışı konu uyarısı: Yok / Var, kritik değil
- Build raporları üretildi: Evet / Hayır
- Arşiv/temizlik yapıldı: Evet / Hayır
- Sonraki bölüme geçilebilir: Evet / Hayır
```

---

## 22. Bölüm 2 için önerilen başlangıç komut paketi

Bölüm 2 üretildikten sonra aşağıdaki komut paketi kullanılabilir:

```powershell
cd "C:\OneDrive\OneDrive - mehmetakif.edu.tr\BookFactory"

python -m tools.code.extract_code_blocks `
  --package-root . `
  --out-dir .\workspace\react\build\code `
  --manifest .\workspace\react\build\code_manifest.json `
  --yaml-manifest .\workspace\react\build\code_manifest.yaml `
  --chapters-dir .\workspace\react\chapters

python -m tools.code.validate_code_meta `
  .\workspace\react\build\code_manifest.json `
  --package-root .

python -m tools.code.run_code_tests `
  --manifest .\workspace\react\build\code_manifest.json `
  --package-root . `
  --report-json .\workspace\react\build\test_reports\code_test_report.json `
  --report-md .\workspace\react\build\test_reports\code_test_report.md `
  --node node `
  --fail-on-error

python -m tools.quality.check_chapter_markdown `
  --chapter .\workspace\react\chapters\chapter_02_react_bilesenleri_jsx.md `
  --chapter-id chapter_02 `
  --chapter-no 2 `
  --report .\workspace\react\build\test_reports\chapter_02_markdown_quality_report.md

Select-String `
  -Path .\workspace\react\build\test_reports\chapter_02_markdown_quality_report.md `
  -Pattern "❌|⚠️|FAIL|WARN"
```

---

## 23. Pratik günlük çalışma sırası

Her çalışma oturumunda önerilen kısa sıra:

```text
1. VS Code ile BookFactory klasörünü aç.
2. Terminalin PowerShell 7 olduğunu kontrol et.
3. Proje köküne geç.
4. Son bölüm dosyasını aç.
5. Düzenleme yapmadan önce gerekirse yedek al.
6. Bölüm metnini üret veya düzelt.
7. Kod çıkarma ve testleri çalıştır.
8. Markdown kalite kontrolünü çalıştır.
9. Hata varsa düzeltme scripti hazırla.
10. Raporları kontrol et.
11. Gereksiz dosyaları arşivle.
12. Git kullanılıyorsa commit al.
```

---

## 24. Kısa karar tablosu

| Durum | Yapılacak işlem |
|---|---|
| Bölüm yeni üretildi | Kod çıkarma + kod testi + Markdown kalite kontrol |
| `FAIL > 0` | Bölüm düzeltilmeden sonraki bölüme geçme |
| Sadece kapsam dışı konu uyarısı var | Bağlama göre kabul edilebilir |
| Kök dizinde çok sayıda `.md` var | Arşiv scriptini önce dry-run, sonra `-Apply` ile çalıştır |
| Build klasörü şişti | Cleanup scriptini önce rapor modunda çalıştır |
| VS Code container uyarısı veriyor | Yerel akış kullanılacaksa `Don't Show Again` seçilebilir |
| PowerShell karakterleri bozuyor | UTF-8 profil ayarlarını ekle |
| Kod testi geçmiyor | CODE_META, expected output ve runtime uyumunu kontrol et |

---

## 25. Sonuç

Bu kılavuz, React kitabı üretiminde BookFactory’nin yerel Windows + VS Code + PowerShell 7 tabanlı kullanımını standartlaştırır. Bölüm 2’ye geçmeden önce bu rehberin proje kökünde güncel bir kullanım belgesi olarak tutulması önerilir.

Önerilen dosya adı:

```text
KULLANIM_KILAVUZU.md
```

Alternatif olarak:

```text
docs/BOOKFACTORY_REACT_USAGE.md
```

En güvenli çalışma ilkesi şudur:

```text
Her bölüm = Markdown kalite kontrolü + CODE_META doğrulaması + kod testi + screenshot planı + arşiv/temizlik kontrolü
```
