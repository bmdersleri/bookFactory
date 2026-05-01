# BookFactory Studio v3.1.2 UTF-8 + Outline Patch

Bu patch iki kritik sorunu giderir:

1. Windows Türkçe yerel ayarında (`cp1254`) kalite kontrol aracının emoji/Türkçe karakter yazdırırken `UnicodeEncodeError` vermesi.
2. `outline_check` sırasında manifestte tanımlı ama henüz `chapters/` altında bulunmayan bölüm dosyalarının tüm işi başarısız göstermesi.

## Değişen dosyalar

```text
BookFactory/bookfactory_studio/jobs.py
BookFactory/tools/quality/check_chapter_markdown.py
BookFactory/STUDIO_V3_1_2_UTF8_OUTLINE_PATCH_README.md
```

## Ne değişti?

- Studio job çalıştırıcısı alt Python süreçleri için `PYTHONUTF8=1` ve `PYTHONIOENCODING=utf-8` ortam değişkenlerini ayarlar.
- `check_chapter_markdown.py` stdout/stderr akışlarını UTF-8 olarak yeniden yapılandırır.
- Kalite kontrol aracının modül açıklaması raw string yapıldığı için Python 3.14 `SyntaxWarning: "\w" is an invalid escape sequence` uyarısı giderilir.
- Eksik chapter dosyaları artık `[MISSING]` olarak raporlanır.
- Eksik chapter listesi şu dosyalara yazılır:

```text
<kitap-kökü>/build/quality_reports/missing_chapters_report.md
<kitap-kökü>/build/quality_reports/missing_chapters_report.json
```

- Varsayılan davranışta eksik bölüm dosyaları `outline_check` işini başarısız yapmaz. Bunun nedeni kitap üretim sürecinde bazı bölümlerin henüz LLM'den dönmemiş olabilmesidir.
- Katı davranış istenirse job options içinde `fail_on_missing_chapters=true` gönderilebilir.

## Kurulum

ZIP içeriğini mevcut `BookFactory` klasörünüzün üzerine çıkarın ve dosyaların üzerine yazılmasına izin verin.

Sonra Studio'yu yeniden başlatın:

```powershell
cd "C:\OneDrive\OneDrive - mehmetakif.edu.tr\BookFactory"
python -m bookfactory_studio.app
```

Ardından arayüzden `outline_check` adımını tekrar çalıştırın.

## Beklenen sonuç

Önceki hata:

```text
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705'
```

artık oluşmamalıdır.

Eksik bölümler için logda örnek çıktı:

```text
[MISSING] chapter_02: dosya yok: chapters/chapter_02_javascript_temelleri.md
[INFO] 12 bölüm dosyası henüz yok. Ayrıntı: build/quality_reports/missing_chapters_report.md
```
