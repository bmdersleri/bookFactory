# Parametric Computer Book Factory — LLM Project Brief

**Önerilen dosya adı:** `LLM_PROJECT_BRIEF.md`  
**Belge amacı:** Bu belge, BookFactory / Parametric Computer Book Factory projesinin amacını, güncel klasör yapısını, üretim mantığını, kalite kontrol akışlarını ve bir LLM modelinden beklenen davranışları tanımlar.  
**Belge dili:** Türkçe  
**Teknik dosya adları:** İngilizce  
**Geçerli framework durumu:** v2.11.x çizgisi; kod doğrulama, test otomasyonu, GitHub sync, QR/code pages, export pipeline, dashboard, Dev Container / GitHub Codespaces ve UTF-8 odaklı Windows/PowerShell iyileştirmeleri dâhil.  
**Aktif kitap bağlamı:** `React ile Web Uygulama Geliştirme`  
**Aktif çalışma alanı:** `workspace/react/`  
**Ana örnek uygulama:** `KampüsHub`  
**Yazar:** Prof. Dr. İsmail KIRBAŞ

---

## 1. Bu proje nedir?

**Parametric Computer Book Factory**, bilgisayar bilimleri, yazılım mühendisliği, veri bilimi, yapay zekâ, web programlama, mobil programlama, IoT ve benzeri teknik alanlarda ders kitabı üretimini standartlaştırmak için geliştirilmiş **manifest tabanlı, LLM destekli, kod doğrulamalı, test raporlu, görsel/screenshot planlı ve post-production uyumlu** bir kitap üretim framework’üdür.

Bu proje, LLM’e yalnızca “bir kitap yaz” demek yerine üretim sürecini aşağıdaki bileşenlerle denetlenebilir hâle getirir:

1. Kitap fikri ve hedef kitlenin netleştirilmesi
2. `book_manifest.yaml` veya proje manifestlerinin hazırlanması
3. Bölüm girdi promptlarının üretilmesi
4. Bölüm outline’larının hazırlanması ve kontrol edilmesi
5. Tam bölüm Markdown metinlerinin üretilmesi
6. Kod bloklarının `CODE_META` ile ayıklanması
7. Kodların otomatik doğrulanması ve test edilmesi
8. Screenshot planlarının `[SCREENSHOT:...]` marker standardıyla tanımlanması
9. Mermaid, asset, QR ve code page üretimlerinin ilişkilendirilmesi
10. GitHub senkronizasyonu ve Codespaces uyumluluğunun yönetilmesi
11. DOCX/HTML/EPUB/PDF gibi yayın çıktılarının hazırlanması
12. Release, dashboard, indeksleme ve kalite raporlarının üretilmesi

Bu sistemde amaç, LLM’in yaratıcı ama kontrolsüz içerik üretmesi değil; **manifest, prompt standartları, test raporları ve kalite kapılarıyla izlenebilir bir akademik/teknik kitap üretim süreci** oluşturmaktır.

---

## 2. Güncel proje bağlamı: React kitabı

Bu belge genel BookFactory projesi için geçerlidir; ancak mevcut çalışma özelinde aktif kitap şudur:

```text
React ile Web Uygulama Geliştirme
```

Aktif çalışma klasörü:

```text
workspace/react/
```

Ana kümülatif uygulama:

```text
KampüsHub
```

`KampüsHub`, üniversite öğrencileri için geliştirilen öğretim amaçlı bir React web uygulamasıdır. Kitap boyunca aşağıdaki modüller kademeli olarak geliştirilir:

- ders duyuruları,
- etkinlik takvimi,
- not paylaşımı,
- kullanıcı profili,
- yönlendirme,
- form yönetimi,
- API entegrasyonu,
- state yönetimi,
- test,
- performans ve dağıtım.

Aktif bölüm dosyaları şu yapıda tutulur:

```text
workspace/react/chapters/
```

Bölüm 1 ana dosyası:

```text
workspace/react/chapters/chapter_01_modern_web_giris.md
```

Bölüm 1 için kod doğrulama hattı çalıştırılmış ve üç `CODE_META` bloğu başarıyla test edilmiştir. Bölüm 2’ye geçmeden önce proje belgeleri, kullanım kılavuzu, kurulum notları ve LLM proje özeti güncel tutulmalıdır.

---

## 3. Projenin temel amacı

BookFactory şu hedeflere sahiptir:

1. Teknik ders kitabı üretimini manifest, prompt, test ve kalite kapılarıyla standartlaştırmak.
2. LLM destekli üretimi rastgele içerik üretiminden çıkarıp tekrar üretilebilir mühendislik sürecine dönüştürmek.
3. Bölüm metni, kod, görsel, screenshot, QR, GitHub linki ve final yayın çıktısını aynı üretim zincirine bağlamak.
4. Kod örneklerini çalıştırılabilir, ayıklanabilir ve test raporuyla doğrulanabilir hâle getirmek.
5. Öğretim tasarımı, pedagojik akış, erişilebilirlik ve güvenlik notlarını bölüm standardına yerleştirmek.
6. Türkçe içerik üretirken dosya adları, kalıcı ID’ler ve otomasyon anahtarlarını İngilizce tutmak.
7. Post-production sürecini kitap üretiminin doğal parçası yapmak.
8. İnsan editör müdahalesini, özellikle manuel görsel düzenlemelerini ve akademik kalite kararlarını korumak.
9. Windows + PowerShell 7, Python, Node.js, GitHub Codespaces ve Dev Container akışlarıyla uyumlu çalışmak.
10. Gereksiz dosya birikimini raporlama, arşivleme ve kontrollü temizlik betikleriyle yönetmek.

---

## 4. Bu proje ne değildir?

BookFactory:

- Manifest veya proje standardı olmadan rastgele kitap yazdırma aracı değildir.
- LLM’in varsayımlarına dayalı otomatik kapsam genişletme sistemi değildir.
- Kaynak uydurmaya veya doğrulanmamış teknik iddiaları kesin bilgi gibi yazmaya izin vermez.
- Kod bloklarını yalnızca metin olarak gören bir Markdown üreticisi değildir; kodlar test hattıyla ilişkilidir.
- Görselleri, screenshot’ları ve QR kodları sonradan elle ilişkilendirilecek kopuk varlıklar olarak görmez.
- Kullanıcı onayı olmadan bölümden bölüme geçmeyi veya kapsamı değiştirmeyi normal kabul etmez.
- `assets/manual/`, `assets/locked/`, bölüm metinleri ve manifestleri otomatik temizlenebilir geçici dosyalar olarak değerlendirmez.

---

## 5. Temel ilke: Manifest ve proje standardı tek doğruluk kaynağıdır

Genel BookFactory üretiminde ana doğruluk kaynağı:

```text
book_manifest.yaml
```

React kitabı gibi proje özelinde ek doğruluk kaynakları şunlardır:

```text
workspace/react/
core/
docs/
configs/
manifests/
README.md
SETUP.md
KULLANIM_KILAVUZU.md
LLM_PROJECT_BRIEF.md
RELEASE_CHECKLIST.md
```

LLM, manifestte, prompt paketinde veya proje standardında yer almayan kritik bilgileri kesin bilgi gibi kullanmamalıdır.

Kural:

```text
Eksik bilgi varsa tahmin etme.
Belirsizlik varsa uydurma.
Kritik karar varsa kullanıcıdan onay al.
Teknik bilgi sürüm bağımlıysa resmi kaynakla doğrula.
```

---

## 6. LLM modelinden beklenen temel davranış

Bir LLM modeli bu projede şu şekilde davranmalıdır:

1. Önce proje belgelerini ve ilgili bölüm girdilerini okumalıdır.
2. Aktif kitap bağlamını ve çalışma klasörünü doğru anlamalıdır.
3. Kullanıcının istediği işin hangi aşamaya ait olduğunu belirlemelidir.
4. Manifest, prompt standardı ve kalite kapılarıyla çelişmemelidir.
5. Gerektiğinde kullanıcıya kısa, hedefli ve iş akışını ilerleten sorular sormalıdır.
6. Onay gerektiren aşamalarda onay almadan ileri geçmemelidir.
7. Kod bloklarını `CODE_META` standardıyla uyumlu üretmelidir.
8. `CODE_META` bilgisini çalıştırılabilir kod bloğunun içine yorum satırı olarak koymamalıdır.
9. Screenshot marker’larını ve screenshot manifest alanlarını korumalıdır.
10. Dosya adlarında Türkçe karakter, boşluk ve özel karakter önermemelidir.
11. Kapsam dışı konuları ana akışa almamalıdır.
12. Teknik doğruluğundan emin olmadığı konularda belirsizliği açıkça belirtmelidir.
13. Hata raporlarını yorumlamalı, kök neden ve çözüm adımı önermelidir.
14. Gereksiz dosya temizliği, arşivleme ve release hazırlığında kaynak dosyaları korumalıdır.

---

## 7. LLM modelinin rolleri

| Rol | Açıklama |
|---|---|
| Proje başlatma ajanı | Kitap fikrini analiz eder, belirsiz alanları sorar, manifest taslağı üretir. |
| Manifest yorumlayıcı | `book_manifest.yaml` ve proje standardını tek doğruluk kaynağı olarak kullanır. |
| Prompt üretici | Manifestten bölüm girdi promptları üretir veya mevcut promptları revize eder. |
| Öğretim tasarımcısı | Hedef kitleye uygun pedagojik akış ve etkinlik yapısı kurar. |
| Teknik editör | Kapsam, sürüm, kod, kaynak ve format tutarlılığını denetler. |
| Kod kalite ajanı | `CODE_META`, kod çıkarma, test ve GitHub uyumluluğunu kontrol eder. |
| Screenshot planlayıcı | `[SCREENSHOT:...]` marker’larını ve ekran çıktısı planlarını yönetir. |
| Post-production yönlendirici | Mermaid, asset, QR, DOCX/HTML/EPUB/PDF ve paketleme adımlarını açıklar. |
| Hata ayıklama ajanı | PowerShell, Python, Node, UTF-8, path ve test hatalarını yorumlar. |
| Yayın kalite ajanı | Release checklist, dashboard, arşivleme ve final paket kontrollerini yürütür. |

---

## 8. LLM modelinin yapmaması gerekenler

LLM modeli aşağıdakileri yapmamalıdır:

1. Manifestte veya proje standardında olmayan bölüm eklememelidir.
2. Kaynak, API davranışı veya teknik sürüm uydurmamalıdır.
3. Kapsam dışı teknolojileri ana akışa almamalıdır.
4. Hatalı kodu çalışır kod gibi sunmamalıdır.
5. `CODE_META` bilgisini `// CODE_META` biçiminde JavaScript/Java/Python kod bloğunun içine yazmamalıdır.
6. QR görsellerinin manuel düzenlenmesini önermemelidir.
7. `assets/manual/` ve `assets/locked/` klasörlerini temizlenebilir geçici çıktı gibi değerlendirmemelidir.
8. Bölüm başlığında birden fazla H1 oluşturacak Markdown yapısı üretmemelidir.
9. Kod bloklarını tablo, blockquote veya iç içe liste içine gömmemelidir.
10. Windows path, PowerShell komutu veya UTF-8 ayarlarında denenmemiş kesinlikte öneriler vermemelidir.
11. Kullanıcının aktif yerel çalışma ortamını değiştirecek komutlarda riskleri belirtmeden işlem önermemelidir.

---

## 9. Güncel klasör yapısı

Güncel BookFactory yapısı genel olarak aşağıdaki gibidir:

```text
BookFactory/
├── .devcontainer/
├── .github/
│   ├── codespaces/
│   └── workflows/
├── assets/
│   ├── auto/
│   ├── final/
│   ├── locked/
│   └── manual/
├── bookfactory/
├── build/
├── configs/
├── core/
├── docs/
├── examples/
├── manifests/
├── schemas/
├── templates/
├── tests/
├── tools/
├── workspace/
│   └── react/
├── README.md
├── SETUP.md
├── KULLANIM_KILAVUZU.md
├── LLM_PROJECT_BRIEF.md
├── RELEASE_CHECKLIST.md
├── CHANGELOG.md
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── checksums.sha256
```

Not: Bazı klasörler proje sürümüne veya kullanıcının yerel arşivleme işlemlerine göre bulunmayabilir. LLM, bir dosyanın varlığından emin değilse kullanıcıdan çıktı istemeli veya dosya listesini temel almalıdır.

---

## 10. `core/` klasörü

`core/` klasörü, LLM’in çalışma kurallarını ve üretim standartlarını içerir.

Güncel çekirdek dosya ailesi şunları kapsar:

```text
core/
├── 00_llm_execution_contract.md
├── 01_book_manifest_schema.md
├── 02_general_system_prompt.md
├── 03_output_format_standard.md
├── 04_chapter_structure_standard.md
├── 05_chapter_input_generator_prompt.md
├── 06_outline_review_prompt.md
├── 07_full_text_generation_prompt.md
├── 08_quality_gate_contract.md
├── 09_manual_asset_override_policy.md
├── 10_multilingual_generation_policy.md
├── 11_approval_gate_policy.md
├── 12_project_starter_prompt.md
├── 13_post_production_pipeline_standard.md
├── 14_docx_build_and_formatting_policy.md
├── 15_generated_package_protocol.md
├── 16_code_validation_and_test_policy.md
├── 17_github_sync_and_qr_policy.md
├── 18_export_pipeline_policy.md
├── 19_indexing_dashboard_policy.md
└── 20_cloud_ide_codespaces_policy.md
```

### 10.1 Ana çekirdek belgeler

| Dosya | Amaç |
|---|---|
| `00_llm_execution_contract.md` | LLM’in genel çalışma sözleşmesi. |
| `01_book_manifest_schema.md` | Manifest alanları ve anlamları. |
| `02_general_system_prompt.md` | Genel kitap üretim sistemi promptu. |
| `03_output_format_standard.md` | Markdown çıktı, tablo, kod ve kutu standartları. |
| `04_chapter_structure_standard.md` | Bölüm içi pedagojik yapı. |
| `05_chapter_input_generator_prompt.md` | Manifestten bölüm girdi promptu üretimi. |
| `06_outline_review_prompt.md` | Outline kontrol ve karar standardı. |
| `07_full_text_generation_prompt.md` | Onaylı outline’dan tam metin üretimi. |
| `08_quality_gate_contract.md` | Kalite kapıları ve karar türleri. |
| `09_manual_asset_override_policy.md` | Manuel görsel önceliği. |
| `10_multilingual_generation_policy.md` | Çok dilli üretim politikası. |
| `11_approval_gate_policy.md` | Onay kapıları. |
| `12_project_starter_prompt.md` | Yeni kitap projesi başlatma. |
| `13_post_production_pipeline_standard.md` | Post-production hattı. |
| `14_docx_build_and_formatting_policy.md` | DOCX üretim ve biçimlendirme. |
| `15_generated_package_protocol.md` | Paket üretim protokolü. |
| `16_code_validation_and_test_policy.md` | Kod çıkarma, manifest doğrulama ve test hattı. |
| `17_github_sync_and_qr_policy.md` | GitHub senkronizasyonu, QR ve code page standardı. |
| `18_export_pipeline_policy.md` | HTML/EPUB/PDF/export akışı. |
| `19_indexing_dashboard_policy.md` | Dashboard, indeksleme ve raporlama. |
| `20_cloud_ide_codespaces_policy.md` | Dev Container ve GitHub Codespaces entegrasyonu. |

---

## 11. `workspace/react/` klasörü

React kitabı üretimi için aktif çalışma alanı şu yapıdadır:

```text
workspace/react/
├── chapters/
├── chapter_inputs/
├── build/
│   ├── code/
│   └── test_reports/
├── assets/
├── screenshots/
├── manifests/
└── dist/
```

Önemli yollar:

```text
workspace/react/chapters/chapter_01_modern_web_giris.md
workspace/react/build/code_manifest.json
workspace/react/build/code_manifest.yaml
workspace/react/build/test_reports/code_test_report.json
workspace/react/build/test_reports/code_test_report.md
workspace/react/build/test_reports/chapter_01_markdown_quality_report.md
```

Bölüm üretiminde dosya adları küçük harfli, İngilizce slug veya açık ASCII karakterlerle tutulmalıdır:

```text
chapter_02_javascript_temelleri.md
chapter_03_html_css_bilesen_dusuncesi.md
```

---

## 12. `docs/` klasörü

`docs/` klasörü kullanıcı ve geliştirici belgelerini içerir. Güncel belgeler şunları kapsayabilir:

```text
docs/
├── cli_usage.md
├── codespaces_integration.md
├── code_pages.md
├── code_validation.md
├── dashboard.md
├── export_pipeline.md
├── github_sync.md
├── indexing_glossary.md
├── llm_loading_order.md
├── LLM_PROJECT_BRIEF.md
├── postproduction_troubleshooting.md
├── project_starter_prompt_usage.md
├── quickstart.md
├── usage.md
└── windows_setup.md
```

Kök dizinde ise sade ve güncel bir belge seti önerilir:

```text
README.md
SETUP.md
KULLANIM_KILAVUZU.md
LLM_PROJECT_BRIEF.md
RELEASE_CHECKLIST.md
CHANGELOG.md
```

Eski sürüm notları, geçici raporlar ve kısa süreli Markdown açıklamaları `docs/archive/` altına taşınabilir.

---

## 13. `tools/` klasörü

`tools/` klasörü Python ve PowerShell tabanlı yardımcı araçları içerir.

Önemli araç aileleri:

```text
tools/
├── check_environment.py
├── check_package_integrity.py
├── validate_manifest.py
├── generate_chapter_inputs.py
├── code/
├── quality/
├── postproduction/
└── react_clean_rebuild.ps1
```

### 13.1 Kod doğrulama araçları

React kitabı için kod blokları şu araç zinciriyle işlenir:

```text
tools.code.extract_code_blocks
tools.code.validate_code_meta
tools.code.run_code_tests
```

Bu zincir:

1. Markdown içindeki `CODE_META` bloklarını bulur.
2. Kodları `workspace/react/build/code/` altına çıkarır.
3. `code_manifest.json` ve `code_manifest.yaml` üretir.
4. Metadata doğrulaması yapar.
5. Node.js veya ilgili çalışma zamanı ile kodları test eder.
6. JSON ve Markdown test raporu üretir.

### 13.2 Markdown kalite araçları

Bölüm kalitesi şu araçla denetlenebilir:

```text
tools/quality/check_chapter_markdown.py
```

Bu araç tipik olarak şu sorunları yakalar:

- birden fazla H1,
- yanlış `CODE_META` yerleşimi,
- eksik screenshot marker’ı,
- standart bölüm başlıklarından sapma,
- kapsam dışı konu uyarıları,
- CODE_META ve Markdown biçim hataları.

### 13.3 Temizlik ve arşivleme betikleri

Proje ilerledikçe geçici raporlar ve eski Markdown dosyaları artabilir. Bu nedenle kök dizinde veya araçlar altında şu tür betikler bulunabilir:

```text
cleanup_bookfactory_project.ps1
archive_legacy_bookfactory_md_pwsh7.ps1
fix_chapter_01_quality.ps1
```

Bu betiklerde varsayılan yaklaşım güvenli olmalıdır:

```text
Önce rapor üret.
Doğrudan silme.
Gerekirse karantinaya veya docs/archive altına taşı.
Kalıcı silme için açık parametre kullan.
```

PowerShell 7 kullanımı için `pwsh` tercih edilmelidir.

---

## 14. `assets/` klasörü ve görsel politikası

Görsel varlıklar şu öncelik mantığıyla yönetilir:

```text
assets/
├── auto/
├── manual/
├── locked/
└── final/
```

Öncelik:

```text
manual > locked > auto
```

LLM ve araçlar şu kurala uymalıdır:

```text
assets/manual/ ve assets/locked/ otomatik silinmez.
Otomatik üretilen görsel, manuel düzenlenmiş görselin üzerine yazmaz.
```

---

## 15. `CODE_META` standardı

Kod örnekleri otomasyon tarafından ayıklanacaksa her çalıştırılabilir kod bloğundan önce `CODE_META` HTML yorum bloğu yer almalıdır.

Doğru örnek:

```markdown
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
```

Yanlış örnek:

```javascript
// CODE_META: { "id": "react_ch02_code01" }
console.log("KampüsHub");
```

Kural:

```text
CODE_META, çalıştırılacak kod bloğunun içine yorum satırı olarak yazılmaz.
CODE_META, kod bloğundan önce HTML yorum bloğu olarak yazılır.
```

---

## 16. Hatalı kod örnekleri politikası

Eğitim amaçlı hatalı kod gösterilecekse, bu kodun otomatik test hattında çalıştırılması istenmiyorsa metadata açıkça bunu belirtmelidir.

Örnek:

```markdown
<!-- CODE_META
id: react_ch02_broken01
chapter_id: chapter_02
language: javascript
kind: broken_example
title: "Hatalı const yeniden atama örneği"
file: "broken_const_reassignment.js"
extract: false
test: skip
github: false
qr: none
-->
```

Hatalı kod örnekleri pedagojik olarak şu sırayla verilmelidir:

1. Hatalı kullanım
2. Hata açıklaması
3. Düzeltilmiş kullanım
4. React/KampüsHub bağlamında çıkarım

---

## 17. Screenshot planı standardı

React kitabında programatik ekran çıktıları kitap kalitesinin temel parçasıdır.

Markdown içinde marker standardı:

```text
[SCREENSHOT:bXX_YY_aciklayici_ad]
```

Örnek:

```text
[SCREENSHOT:b02_01_js_console_output]
[SCREENSHOT:b02_02_kampushub_module_list]
```

Her screenshot için manifestte veya plan dosyasında aşağıdaki alanlar tanımlanmalıdır:

```yaml
id: b02_01_js_console_output
chapter: 2
figure: 2.1
title: "JavaScript console çıktısı"
route: "/__book__/chapter-02/console-output"
waitFor: "#screenshot-ready"
actions: []
output: "workspace/react/screenshots/b02_01_js_console_output.png"
caption: "JavaScript temel sözdizimi örneğinin tarayıcı konsolundaki çıktısı."
markdownTarget: "[SCREENSHOT:b02_01_js_console_output]"
```

Kural:

```text
Her bölümde en az 1 screenshot planlanmalıdır.
Görsel ağırlıklı bölümlerde 2–4 screenshot önerilir.
Screenshot marker’ı ile manifest ID’si bire bir eşleşmelidir.
```

---

## 18. Mermaid ve diyagram politikası

Diyagramlar için `MERMAID_META` veya `DIAGRAM_META` kullanılabilir.

Örnek:

```markdown
<!-- DIAGRAM_META
id: react_ch02_data_flow01
chapter_id: chapter_02
type: mermaid
title: "Veriden arayüze akış"
auto_path: "assets/auto/diagrams/react_ch02_data_flow01.png"
manual_path: "assets/manual/diagrams/react_ch02_data_flow01.png"
final_path: "assets/final/diagrams/react_ch02_data_flow01.png"
manual_override: true
-->
```

Mermaid diyagramları sade, PNG dönüşümüne uygun ve öğretim amacına hizmet edecek düzeyde tutulmalıdır.

---

## 19. QR, GitHub ve code pages politikası

BookFactory, kod örneklerini GitHub bağlantıları ve QR kodlarla ilişkilendirebilir.

QR türleri:

| QR türü | Açıklama |
|---|---|
| Source QR | Doğrudan kaynak kod dosyasına gider. |
| Page QR | Açıklamalı kod sayfasına gider. |
| Dual QR | Hem kaynak hem açıklamalı sayfa stratejisini destekler. |

Kural:

```text
QR görselleri manuel düzenlenmez.
QR matrisinin bozulması veri bütünlüğünü bozabilir.
Kod dosyası yolu değişirse QR/code page manifesti de güncellenmelidir.
```

---

## 20. Başlık politikası

Genel BookFactory ilkesi, başlık numaralandırmasının mümkünse build/post-production tarafından yönetilmesidir. Ancak bazı kitap projelerinde, özellikle bölüm kalite kontrol scriptleri manuel bölüm numarası bekleyebilir.

Bu nedenle kural şudur:

```text
Proje özelindeki bölüm standardı genel ilkeden önce gelir.
```

React kitabı mevcut bölüm kalite akışında şu ilkelere uyulmalıdır:

1. Her bölüm dosyasında yalnızca bir H1 olmalıdır.
2. H1 biçimi proje standardına uygun olmalıdır.
3. README taslağı, örnek Markdown veya kod içinde ikinci H1 oluşturulmamalıdır.
4. Alt başlık numaraları tutarlı olmalıdır.
5. `# KampüsHub` gibi örnek README başlıkları bölüm Markdown’ında ikinci H1 olarak bırakılmamalıdır; gerekirse düz metne veya kod bloğu dışı açıklamaya dönüştürülmelidir.

---

## 21. React kitabı kapsam politikası

React kitabında varsayılan yaklaşım:

```text
React 19 uyumlu modern React yaklaşımı
Fonksiyon bileşenleri
Hooks
Vite
React Router v7 Declarative Mode
REST API istemci entegrasyonu
TanStack Query
Redux Toolkit
Zustand
React Hook Form
Vitest + React Testing Library + user-event
MSW
```

Ana kapsam dışı konular:

```text
Next.js
SSR/SSG/ISR
React Server Components ana akışı
Server Actions ana akışı
React Native
GraphQL/Apollo/Relay
İleri TypeScript
Backend endpoint yazımı
Veritabanı/ORM/migration
Docker/Kubernetes ileri altyapı
Mikro front-end
WebGL/Three.js ileri görselleştirme
```

Bu konular yalnızca “ileri okuma”, “sonraki adımlar” veya “Kitap 2” bağlamında anılabilir.

---

## 22. React kitabı bölüm akışı

React kitabı için tipik bölüm akışı:

| Bölüm | Ana odak |
|---:|---|
| 1 | Modern Web’e giriş, geliştirme ortamı, Vite ve KampüsHub iskeleti |
| 2 | React için gerekli modern JavaScript temelleri |
| 3 | HTML/CSS’ten bileşen düşüncesine geçiş |
| 4 | JSX ve render mantığı |
| 5 | Props ve bileşen kompozisyonu |
| 6 | State ve event yönetimi |
| 7 | `useEffect`, yan etkiler ve API’ye hazırlık |
| 8 | Hook kuralları, memoization farkındalığı |
| 9 | Custom hook tasarımı |
| 10 | React Router v7 Declarative Mode |
| 11 | Formlar, validation ve erişilebilirlik |
| 12 | Redux Toolkit |
| 13 | REST API, TanStack Query ve MSW |
| 14 | Zustand ve alternatif state yönetimi |
| 15 | Performans, test ve dağıtım |
| 16 | KampüsHub final entegrasyonu |

---

## 23. Bölüm üretim iş akışı

Bir bölüm üretilirken LLM şu sırayı izlemelidir:

```text
1. İlgili bölüm girdi promptunu oku.
2. Manifest/proje standardı ile karşılaştır.
3. Outline üret veya mevcut outline’ı kontrol et.
4. Kapsam dışı konuları ayıkla.
5. Kod örnekleri, CODE_META, screenshot ve KampüsHub bağlantısını planla.
6. Tam bölüm metnini Pandoc uyumlu Markdown olarak üret.
7. Kod bloklarını test edilebilir metadata ile yaz.
8. Markdown kalite kontrolüne uygun tek H1 ve tutarlı başlık yapısı kullan.
9. Bölüm sonu soruları, alıştırmalar, laboratuvar görevi ve sonraki bölüme köprü ekle.
10. Kod testleri ve Markdown kalite kontrolü için komutları açıkla.
```

---

## 24. Kod doğrulama komutları

React kitabı için standart kod test akışı:

```powershell
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
```

Başarı ölçütü:

```text
CODE_META validation: OK
Failed: 0
Skipped: yalnızca bilerek skip edilen broken/example dışı bloklarda kabul edilebilir
```

---

## 25. Markdown kalite kontrol komutu

Bölüm kalite kontrolü için örnek komut:

```powershell
python -m tools.quality.check_chapter_markdown `
  --chapter .\workspace\react\chapters\chapter_01_modern_web_giris.md `
  --chapter-id chapter_01 `
  --chapter-no 1 `
  --report .\workspace\react\build\test_reports\chapter_01_markdown_quality_report.md
```

Rapor filtreleme:

```powershell
Select-String `
  -Path .\workspace\react\build\test_reports\chapter_01_markdown_quality_report.md `
  -Pattern "❌|⚠️|FAIL|WARN"
```

Başarı ölçütü:

```text
FAIL: 0
```

Kapsam dışı konu uyarıları, ilgili ifade yalnızca “bu kitapta ana akışa alınmayacaktır” bağlamında geçiyorsa kritik kabul edilmeyebilir.

---

## 26. PowerShell 7 ve VS Code çalışma standardı

Windows ortamında önerilen terminal:

```text
PowerShell 7.x / pwsh
```

VS Code terminalinde komutlar mümkünse doğrudan `pwsh` profili üzerinden çalıştırılmalıdır. `powershell` komutu çoğu sistemde Windows PowerShell 5.1’i açabilir.

Örnek:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\archive_legacy_bookfactory_md_pwsh7.ps1 -Apply
```

PowerShell profilinde UTF-8 için önerilen ayar:

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
```

VS Code için proje bazlı ayar dosyası:

```text
.vscode/settings.json
```

Önerilen temel ayarlar:

```json
{
  "terminal.integrated.defaultProfile.windows": "PowerShell 7",
  "terminal.integrated.cwd": "${workspaceFolder}",
  "files.encoding": "utf8",
  "files.autoGuessEncoding": true,
  "files.eol": "\r\n"
}
```

---

## 27. Dev Container ve GitHub Codespaces politikası

BookFactory içinde `.devcontainer/` klasörü varsa VS Code şu uyarıyı gösterebilir:

```text
Folder contains a Dev Container configuration file. Reopen folder to develop in a container.
```

Bu uyarı normaldir. Yerel Windows + PowerShell 7 ortamı çalışıyorsa container’a geçmek zorunlu değildir.

Kullanım kararı:

| Durum | Öneri |
|---|---|
| Yerel Python/Node/Pandoc kurulumu sorunsuz | Yerel ortamla devam et. |
| Her kullanıcıda aynı ortam isteniyor | Dev Container veya Codespaces kullan. |
| Windows path/UTF-8 sorunları sık yaşanıyor | Dev Container değerlendirilebilir. |
| GitHub üzerinden tarayıcıda çalışma isteniyor | GitHub Codespaces uygundur. |

LLM, container geçişini zorunlu gibi sunmamalıdır.

---

## 28. Temizlik ve arşivleme politikası

Proje ilerledikçe aşağıdaki dosyalar birikebilir:

```text
geçici Markdown notları
eski release notları
test raporları
cleanup raporları
backup dosyaları
*.bak / *.old / *.tmp
__pycache__
*.pyc
build çıktıları
```

Güvenli temizlik sırası:

```text
1. Önce aday raporu üret.
2. Raporu kullanıcı kontrol etsin.
3. Gerekirse dosyaları docs/archive altına taşı.
4. Kalıcı silme yalnızca açık parametreyle yapılsın.
```

Kök dizinde korunması önerilen ana Markdown dosyaları:

```text
README.md
SETUP.md
KULLANIM_KILAVUZU.md
LLM_PROJECT_BRIEF.md
RELEASE_CHECKLIST.md
CHANGELOG.md
```

---

## 29. LLM’e dosyalar hangi sırayla verilmelidir?

### 29.1 Yeni kitap projesi başlatma

```text
1. LLM_PROJECT_BRIEF.md
2. core/00_llm_execution_contract.md
3. core/01_book_manifest_schema.md
4. core/12_project_starter_prompt.md
5. Kullanıcının kitap fikri
```

### 29.2 Bölüm girdi promptu üretme

```text
1. LLM_PROJECT_BRIEF.md
2. core/00_llm_execution_contract.md
3. core/01_book_manifest_schema.md
4. core/05_chapter_input_generator_prompt.md
5. book_manifest.yaml veya proje manifesti
```

### 29.3 Outline üretme

```text
1. LLM_PROJECT_BRIEF.md
2. core/00_llm_execution_contract.md
3. core/02_general_system_prompt.md
4. core/03_output_format_standard.md
5. core/04_chapter_structure_standard.md
6. İlgili chapter_input.md
```

### 29.4 Outline kontrolü

```text
1. core/06_outline_review_prompt.md
2. İlgili chapter_input.md
3. Üretilen outline
```

### 29.5 Tam metin üretimi

```text
1. LLM_PROJECT_BRIEF.md
2. core/00_llm_execution_contract.md
3. core/02_general_system_prompt.md
4. core/03_output_format_standard.md
5. core/04_chapter_structure_standard.md
6. core/07_full_text_generation_prompt.md
7. İlgili chapter_input.md
8. Onaylanmış outline
```

### 29.6 React kitabı bölüm kalite kontrolü

```text
1. LLM_PROJECT_BRIEF.md
2. KULLANIM_KILAVUZU.md
3. İlgili bölüm dosyası
4. tools/quality/check_chapter_markdown.py
5. code_test_report.md
6. markdown_quality_report.md
```

---

## 30. Genel çalışma mantığı

```text
Kitap fikri
   ↓
Project Starter Prompt
   ↓
Netleştirme soruları
   ↓
Manifest / proje standardı
   ↓
Bölüm girdi promptları
   ↓
Outline üretimi
   ↓
Outline kontrolü
   ↓
Tam bölüm Markdown metni
   ↓
CODE_META ile kod çıkarma
   ↓
Kod doğrulama ve test
   ↓
Markdown kalite kontrol
   ↓
Screenshot / Mermaid / asset / QR planı
   ↓
GitHub sync / code pages
   ↓
Post-production
   ↓
Final DOCX / HTML / EPUB / PDF / ZIP
```

---

## 31. Onay kapıları

Onay kapıları manifest veya proje iş akışından yönetilir.

Örnek:

```yaml
approval_gates:
  manifest_validation: "required"
  chapter_input_generation: "optional"
  outline_review: "required"
  full_text_generation: "required"
  code_validation: "required"
  markdown_quality_check: "required"
  post_production_build: "optional"
```

LLM şu kurala uymalıdır:

```text
Bir aşamada kritik hata varsa sonraki aşamaya geçilmez.
FAIL: 0 hedeflenir.
WARN varsa bağlamına göre kritik olup olmadığı değerlendirilir.
```

---

## 32. Çok dilli üretim mantığı

Framework çok dilli üretimi destekler.

Örnek:

```yaml
language:
  primary_language: "tr"
  output_languages:
    - "tr"
    - "en"
  generation_mode: "parallel"
  file_naming_language: "en"
  manifest_language: "en"
  automation_language: "en"
```

Kurallar:

1. Dosya adları İngilizce/ASCII slug kalır.
2. Manifest anahtarları İngilizce kalır.
3. Kalıcı ID’ler İngilizce slug olur.
4. İçerik hedef dile göre üretilir.
5. Kod tanımlayıcıları genellikle İngilizce kalır.
6. Öğretici açıklamalar kitabın hedef dilinde yazılır.
7. Terminoloji glossary ile tutarlı tutulur.

---

## 33. Kaynak ve doğruluk politikası

LLM şu kaynak politikasına uymalıdır:

1. Resmi dokümantasyon birincil kaynaktır.
2. Sürüm bağımlı bilgiler güncel kaynakla doğrulanmalıdır.
3. React, Vite, React Router, TanStack Query, Redux Toolkit, Zustand, React Hook Form, Vitest ve Testing Library gibi araçlarda sürüm farklılığı açıkça belirtilmelidir.
4. Kaynak uydurulmaz.
5. Akademik içerikte telif ve atıf ilkelerine uyulur.
6. Kararsız veya yeni API davranışları kesin anlatım yerine “sürüm notu” olarak verilir.
7. Kitap başlangıç düzeyindeyse ileri konular ana akışı bozacak biçimde genişletilmez.

---

## 34. Kalite kontrol kararları

LLM kalite kontrol aşamalarında şu kararlardan birini vermelidir:

```text
TAM METNE GEÇİLEBİLİR
KÜÇÜK DÜZELTME GEREKİR
REVİZYON GEREKİR
BLOKE
```

Karar kriterleri:

| Karar | Anlam |
|---|---|
| `TAM METNE GEÇİLEBİLİR` | Kritik eksik yoktur. |
| `KÜÇÜK DÜZELTME GEREKİR` | İçerik üretimi mümkün; küçük iyileştirmeler gereklidir. |
| `REVİZYON GEREKİR` | Kapsam, yapı veya teknik eksikler düzeltilmelidir. |
| `BLOKE` | Kritik hata vardır; sonraki aşamaya geçilmemelidir. |

Kod ve Markdown kalite kontrollerinde hedef:

```text
Failed: 0
FAIL: 0
```

---

## 35. Hata durumunda LLM nasıl davranmalıdır?

Hata varsa LLM:

1. Hatanın hangi komut, dosya veya aşamada oluştuğunu belirtmelidir.
2. Hata mesajını sadeleştirerek açıklamalıdır.
3. Muhtemel kök nedeni ayırmalıdır.
4. Güvenli çözüm komutu veya düzeltme adımı vermelidir.
5. Riskli işlemlerde yedekleme veya dry-run önermelidir.
6. Emin değilse bunu açıkça söylemelidir.
7. Başarısız komut sonrası “bir sorun yok” gibi yüzeysel yanıt vermemelidir.

Örnek iyi yanıt:

```text
Bu hata PowerShell 5.1 ile çalıştırmadan kaynaklanıyor olabilir. Siz PowerShell 7 kullanıyorsunuz; bu nedenle komutu `powershell` yerine `pwsh` ile çalıştırın. Ayrıca betiğe `#requires -Version 7.0` eklenmesi yanlış sürümde çalıştırmayı engeller.
```

---

## 36. React kitabı Bölüm 2’ye geçiş ilkeleri

Bölüm 2’ye geçmeden önce aşağıdaki kontroller tamamlanmalıdır:

```text
[ ] Bölüm 1 Markdown kalite raporunda FAIL: 0
[ ] Bölüm 1 CODE_META testlerinde Failed: 0
[ ] Kök dizindeki eski Markdown dosyaları arşivlendi
[ ] README.md / SETUP.md / KULLANIM_KILAVUZU.md / LLM_PROJECT_BRIEF.md güncel
[ ] VS Code terminali PowerShell 7 / pwsh kullanıyor
[ ] UTF-8 karakter sorunu kontrol edildi
[ ] workspace/react/build/test_reports altında son raporlar mevcut
[ ] Bölüm 2 için chapter_input veya prompt hazır
```

Bölüm 2 içerik odağı:

```text
React için Modern JavaScript Temelleri
```

Bölüm 2’de ele alınması beklenenler:

- `let` / `const`
- arrow function
- template literal
- destructuring
- spread/rest
- array methods: `map`, `filter`, `reduce`, `find`, `some`
- object/array immutability sezgisi
- Promise ve `async/await`
- modül import/export temelleri
- React ile doğrudan bağlantı
- KampüsHub veri yapılarının ilk örnekleri

---

## 37. LLM için kısa görev özeti

Bir LLM bu projeyi şu şekilde anlamalıdır:

> Benim görevim, kullanıcının teknik ders kitabı projesini manifest ve proje standartlarına bağlı bir üretim hattı içinde yürütmek; belirsiz alanları soru sorarak netleştirmek; bölüm girdi promptu, outline, tam metin, kod testi, Markdown kalite kontrolü, screenshot planı, QR/GitHub/code page ve post-production süreçlerini tutarlı biçimde yönetmek; dosya adlarını ve otomasyon kimliklerini İngilizce/ASCII tutmak; içerik dilini proje standardından almak; akademik doğruluk, pedagojik tutarlılık, kod çalışırlığı ve yayın çıktısı kalitesini korumaktır.

---

## 38. LLM için başlangıç komutu

Yeni bir LLM oturumuna şu komut verilebilir:

```text
Sen Parametric Computer Book Factory projesi için çalışan bir kitap üretim ve kalite kontrol ajanısın.

Önce `LLM_PROJECT_BRIEF.md`, ardından gerekiyorsa `README.md`, `SETUP.md`, `KULLANIM_KILAVUZU.md`, `core/00_llm_execution_contract.md`, `core/01_book_manifest_schema.md` ve aktif kitapla ilgili bölüm girdi dosyalarını oku.

Aktif çalışma bağlamı `React ile Web Uygulama Geliştirme` kitabıdır. Çalışma klasörü `workspace/react/` ve kümülatif uygulama `KampüsHub` olarak kabul edilir.

Eksik veya muallak bilgileri tahmin ederek doldurma. Kritik kararlar için kullanıcıya kısa ve hedefli sorular sor.

Bölüm üretirken `CODE_META`, `[SCREENSHOT:...]`, Markdown başlık standardı, kapsam sınırları, kod test hattı ve kalite kontrol raporlarını dikkate al.

Kritik hata varsa sonraki aşamaya geçme. Hata raporlarını kök neden ve çözüm adımıyla birlikte açıkla.
```

---

## 39. Sonuç

BookFactory, LLM tabanlı teknik kitap üretimini rastgele ve kontrolsüz bir süreç olmaktan çıkarıp **manifest tabanlı, kod doğrulamalı, test raporlu, screenshot planlı, GitHub/QR/code page destekli, Dev Container/Codespaces uyumlu ve yayın çıktısına hazır** bir üretim sistemine dönüştürmeyi amaçlar.

Bir LLM modelinin bu sistemi doğru kullanabilmesi için şu ilkeler sürekli korunmalıdır:

1. **Manifest ve proje standardı tek doğruluk kaynağıdır.**
2. **Belirsizlik varsa tahmin değil, soru sorulur.**
3. **Kod örnekleri test hattına uygun üretilir.**
4. **Markdown kalite kontrolünde `FAIL: 0` hedeflenir.**
5. **Screenshot, QR, GitHub ve post-production çıktıları metinden kopuk değil, üretim zincirinin parçasıdır.**
6. **Manuel varlıklar ve kaynak dosyalar korunur.**
7. **Her aşama kalite kapılarıyla ilerler.**
