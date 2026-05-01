# BookFactory Studio MVP

BookFactory Studio, mevcut BookFactory komut satırı araçlarını bozmadan çalışan yerel bir web arayüzüdür. Amaç; kitap fikrinden manifest üretimine, bölüm promptlarına, Markdown içe aktarmaya, kalite kontrolüne, kod testine, Mermaid/QR üretimine, GitHub/Codespaces/Pages hazırlığına ve export sürecine kadar bütün hattı tek ekrandan takip etmektir.

## Kurulum

```powershell
cd C:\OneDrive\OneDrive - mehmetakif.edu.tr\BookFactory
python -m pip install -e .
python -m pip install fastapi "uvicorn[standard]" pydantic pyyaml
```

veya paket güncellendikten sonra:

```powershell
python -m pip install -r requirements.txt
```

## Çalıştırma

```powershell
python -m bookfactory_studio.app
```

Tarayıcıda şu adresi açın:

```text
http://127.0.0.1:8765
```

Windows için hazır başlatıcılar:

```powershell
.\run_studio.ps1
```

veya:

```bat
run_studio.bat
```

## Ana ekranlar

1. **Dashboard**: kitap başlığı, yazar, bölüm sayısı, manifest geçerliliği ve son raporlar.
2. **Kitap Sihirbazı**: temel kitap bilgileriyle LLM kitap kurgusu/manifest promptu üretir.
3. **Manifest**: mevcut manifesti görüntüler, klasör yapısını oluşturur.
4. **Bölümler**: bölüm input promptlarını üretir, LLM’den gelen tam metin Markdown dosyasını ilgili bölüme kaydeder.
5. **Production**: kalite, kod, Mermaid, QR, GitHub, Codespaces ve export adımlarını çalıştırır.
6. **Raporlar**: `build/` ve `exports/` altındaki raporları okur.

## Production adımları

- `validate_manifest`: `book_manifest.yaml` temel alanlarını denetler.
- `generate_chapter_prompts`: `prompts/chapter_inputs` altında bölüm promptlarını üretir.
- `outline_check`: `tools/quality/check_chapter_markdown.py` ile bölüm raporları üretir.
- `extract_code`: Markdown içindeki `CODE_META` bloklarını `build/code` altına çıkarır.
- `validate_code`: kod manifestini doğrular.
- `test_code`: JavaScript/Python/Java kodlarını test eder.
- `mermaid_extract`: Markdown içindeki Mermaid bloklarını `.mmd` olarak çıkarır.
- `mermaid_render`: Mermaid dosyalarını PNG’ye dönüştürür.
- `qr_manifest`: kod manifestinden QR manifest üretir.
- `qr_generate`: QR PNG dosyalarını üretir.
- `github_sync`: kodları GitHub uyumlu klasör yapısına hazırlar; push varsayılan olarak kapalıdır.
- `pages_setup`: GitHub Pages dosyalarını hazırlar.
- `codespaces_check`: `.devcontainer` ve Codespaces yapılandırmasını kontrol eder.
- `export`: DOCX/HTML/EPUB/PDF üretim hattını tetikler.
- `full_production`: adımları sırasıyla çalıştırır.

## Güvenli kullanım notları

- GitHub push varsayılan olarak kapalıdır. Push için Production ekranındaki seçenekler JSON alanına `{ "push": true, "commit": true }` yazılması gerekir.
- Uzun işlemlerde loglar `build/studio_jobs/` altında saklanır.
- Bölüm Markdown içe aktarımında mevcut dosya varsa önce `chapter_backups/` altına yedeklenir.
- GUI, mevcut CLI araçlarını orkestre eder; üretim mantığını yeniden yazmaz.

## Önerilen ilk çalışma sırası

1. Proje kökünü seçin ve projeyi açın.
2. Manifest doğrulama çalıştırın.
3. Bölüm girdi promptlarını üretin.
4. LLM’den gelen bölüm Markdown dosyalarını tek tek içe aktarın.
5. Outline check çalıştırın.
6. Code extract → validate code → test code sırasını çalıştırın.
7. Mermaid extract/render ve QR adımlarını çalıştırın.
8. GitHub/Codespaces/Pages ayarlarını test edin.
9. Export ile DOCX/HTML çıktısını üretin.

## v3.1.1 Yol Modeli Düzeltmesi

Bu sürümde BookFactory Studio'nun kitap dosyalarını yanlış kökte araması düzeltilmiştir.

- Arayüzdeki yol alanı artık **Kitap kökü** olarak adlandırılır.
- BookFactory framework kökü ile kitap çalışma kökü ayrılmıştır.
- Framework kökü seçilirse Studio artık `workspace/react/book_manifest.yaml` gibi alt manifestleri otomatik aktif proje kabul etmez.
- Bunun yerine bulunan kitap çalışmalarını listeler ve kullanıcının doğrudan kitap kökünü seçmesini ister.
- Eski manifestlerdeki `workspace/react/chapters/...` biçimli bölüm yolları, kitap kökü `workspace/react` seçildiğinde otomatik olarak `chapters/...` biçimine çözümlenir.
- Production araçları framework içinden çağrılır, ancak `build/`, `assets/`, `exports/`, `chapters/` ve `prompts/` çıktıları tamamen seçilen kitap kökü altında tutulur.

Doğru kullanım örneği:

```powershell
python -m bookfactory_studio.app
```

Tarayıcıda **Kitap kökü** alanına şunlardan biri girilmelidir:

```text
C:\OneDrive\...\react-web
C:\OneDrive\...\BookFactory\workspace\react
```

Yanlış kullanım:

```text
C:\OneDrive\...\BookFactory
```

Bu yol framework köküdür; doğrudan kitap kökü değildir.
