# BookFactory — Üretim Standartları

**Modül:** `brief_standards.md`  
**Yükleme önceliği:** 4 — Bölüm üretimi veya kod işlemi yapılacaksa yükle  
**İlgili modüller:** [`brief_llm_rules.md`](brief_llm_rules.md), [`brief_structure.md`](brief_structure.md)

---

## 1. CODE_META standardı

Kod örnekleri otomasyon tarafından ayıklanacaksa her çalıştırılabilir kod bloğundan **önce** `CODE_META` HTML yorum bloğu yer almalıdır.

### Doğru kullanım

```
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

### Yanlış kullanım

```javascript
// CODE_META: { "id": "react_ch02_code01" }
console.log("KampüsHub");
```

**Kural:**

```
CODE_META, çalıştırılacak kod bloğunun içine yorum satırı olarak yazılmaz.
CODE_META, kod bloğundan önce HTML yorum bloğu olarak yazılır.
```

---

## 2. Hatalı kod örnekleri politikası

Eğitim amaçlı hatalı kod gösterilecekse metadata açıkça belirtmelidir:

```
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

## 3. Screenshot planı standardı

### Markdown marker formatı

```
[SCREENSHOT:bXX_YY_aciklayici_ad]
```

**Örnekler:**

```
[SCREENSHOT:b02_01_js_console_output]
[SCREENSHOT:b02_02_kampushub_module_list]
```

### Screenshot manifest alanları

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

**Kural:**

```
Her bölümde en az 1 screenshot planlanmalıdır.
Görsel ağırlıklı bölümlerde 2–4 screenshot önerilir.
Screenshot marker ID'si ile manifest ID'si bire bir eşleşmelidir.
```

---

## 4. Mermaid ve diyagram politikası

```
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

## 5. QR ve code pages politikası

| QR türü | Açıklama |
|---|---|
| Source QR | Doğrudan kaynak kod dosyasına gider. |
| Page QR | Açıklamalı kod sayfasına gider. |
| Dual QR | Hem kaynak hem açıklamalı sayfa stratejisini destekler. |

**Kural:**

```
QR görselleri manuel düzenlenmez.
QR matrisinin bozulması veri bütünlüğünü bozabilir.
Kod dosyası yolu değişirse QR/code page manifesti de güncellenmelidir.
```

---

## 6. Başlık politikası

React kitabı bölüm kalite akışında şu ilkelere uyulmalıdır:

1. Her bölüm dosyasında yalnızca **bir H1** olmalıdır.
2. H1 biçimi proje standardına uygun olmalıdır.
3. README taslağı, örnek Markdown veya kod içinde ikinci H1 oluşturulmamalıdır.
4. Alt başlık numaraları tutarlı olmalıdır.
5. `# KampüsHub` gibi örnek README başlıkları bölüm Markdown'ında ikinci H1 olarak bırakılmamalıdır; gerekirse düz metne veya kod bloğu dışı açıklamaya dönüştürülmelidir.

---

## 7. Çok dilli üretim özeti

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

**Kurallar:**

1. Dosya adları İngilizce/ASCII slug kalır.
2. Manifest anahtarları İngilizce kalır.
3. Kalıcı ID'ler İngilizce slug olur.
4. İçerik hedef dile göre üretilir.
5. Kod tanımlayıcıları genellikle İngilizce kalır.
6. Öğretici açıklamalar kitabın hedef dilinde yazılır.
7. Terminoloji glossary ile tutarlı tutulur.

---

## 8. Temizlik ve arşivleme politikası

Proje ilerledikçe birikebilecek dosyalar:

```
geçici Markdown notları, eski release notları, test raporları,
cleanup raporları, *.bak / *.old / *.tmp, __pycache__, build çıktıları
```

**Güvenli temizlik sırası:**

```
1. Önce aday raporu üret.
2. Raporu kullanıcı kontrol etsin.
3. Gerekirse docs/archive altına taşı.
4. Kalıcı silme yalnızca açık parametreyle yapılsın.
```

**Kök dizinde korunması gereken dosyalar:**

```
README.md
SETUP.md
KULLANIM_KILAVUZU.md
LLM_PROJECT_BRIEF.md
RELEASE_CHECKLIST.md
CHANGELOG.md
```

---

## 9. Markdown kalite kontrol komutu

```powershell
python -m tools.quality.check_chapter_markdown `
  --chapter .\workspace\react\chapters\chapter_01_modern_web_giris.md `
  --chapter-id chapter_01 `
  --chapter-no 1 `
  --report .\workspace\react\build\test_reports\chapter_01_markdown_quality_report.md
```

Başarı ölçütü: `FAIL: 0`

---

## 10. Kod doğrulama komutları

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

Başarı ölçütü: `CODE_META validation: OK` ve `Failed: 0`
