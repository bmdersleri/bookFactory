# BookFactory Studio v3.1.3 — Akıllı Manifest Editörü Patch

Bu patch, BookFactory Studio manifest ekranını YAML textarea ağırlıklı yapıdan form tabanlı, doğrulamalı ve kullanıcı hatalarını önleyen bir editöre dönüştürür.

## İçerik

- `bookfactory_studio/core.py`
  - Gelişmiş manifest doğrulama
  - Kitap kökü / framework kökü ayrımını koruyan path çözümleme
  - Bölüm dosyalarını gerçek `chapters/*.md` dosyalarıyla eşleştirme
- `bookfactory_studio/app.py`
  - Güvenli kayıt API uçları
  - YAML render / parse API uçları
  - Bölüm dosya eşleştirme API ucu
- `bookfactory_studio/static/index.html`
  - Sekmeli manifest editörü
- `bookfactory_studio/static/app.js`
  - Formdan manifest üretimi
  - Canlı doğrulama
  - Bölüm tablosu düzenleme
  - Dosya adı üretme ve eşleştirme
- `bookfactory_studio/static/styles.css`
  - Yeni manifest editörü stilleri
- `tools/quality/check_chapter_markdown.py`
  - Windows UTF-8 konsol uyumluluğu

## Yeni Manifest Editörü Sekmeleri

1. Kitap Bilgileri
2. Bölümler
3. Kapsam
4. Otomasyon
5. Yollar
6. YAML

## Hatalı Giriş Önleme

Kayıt öncesinde aşağıdakiler kontrol edilir:

- `book.title` boş olamaz.
- `book.author` boş olamaz.
- `book.year` dört haneli olmalıdır.
- `language.primary_language` eksik olmamalıdır.
- Bölüm ID'leri tekrarlanmamalıdır.
- Bölüm dosya adları tekrarlanmamalıdır.
- Bölüm dosya adları güvenli ASCII biçiminde ve `.md` uzantılı olmalıdır.
- `project.paths` göreli yol olmalıdır; mutlak yol ve `..` engellenir.
- `done`, `draft`, `review`, `in_progress` durumundaki bölümlerde dosya yoksa uyarı gösterilir.

## Kurulum

ZIP içindeki `BookFactory` klasörünü mevcut BookFactory klasörünüzün üzerine çıkarın ve dosyaların üzerine yazılmasına izin verin.

Ardından:

```powershell
cd "C:\OneDrive\OneDrive - mehmetakif.edu.tr\BookFactory"
python -m bookfactory_studio.app
```

Tarayıcı:

```text
http://127.0.0.1:8765
```

## Önerilen Kullanım

1. Kitap kökü olarak doğrudan kitap klasörünü yazın:
   - `C:\OneDrive\OneDrive - mehmetakif.edu.tr\react-web`
   - veya `C:\OneDrive\OneDrive - mehmetakif.edu.tr\BookFactory\workspace\react`
2. Manifest sekmesine girin.
3. `Kontrol Et` düğmesine basın.
4. Bölüm dosya adlarında uyumsuzluk varsa `Dosyaları Eşleştir` düğmesini kullanın.
5. `Formdan Kaydet` ile manifesti güvenli biçimde kaydedin.

## Not

Bu patch, v3.1.1 yol düzeltmesi ve v3.1.2 UTF-8 outline düzeltmesiyle uyumlu dosyaları içerir.
