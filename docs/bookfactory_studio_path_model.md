# BookFactory Studio Yol Modeli

BookFactory Studio iki farklı kökü bilinçli olarak ayırır:

1. **Framework kökü**: `tools/`, `schemas/`, `bookfactory_studio/`, `bookfactory/` klasörlerinin bulunduğu BookFactory uygulama klasörüdür.
2. **Kitap kökü**: Belirli bir kitaba ait `book_manifest.yaml`, `chapters/`, `prompts/`, `assets/`, `build/`, `exports/` klasörlerinin bulunduğu bağımsız çalışma klasörüdür.

Arayüzdeki **Kitap kökü** alanına framework klasörü değil, doğrudan kitap klasörü yazılmalıdır. Örnekler:

```text
C:\OneDrive\...\react-web
C:\OneDrive\...\BookFactory\workspace\react
D:\Kitaplar\javanin-temelleri
```

Studio artık `BookFactory` framework kökü seçildiğinde alt klasörlerde rastgele `book_manifest.yaml` arayıp chapter dosyalarını yanlış yerde çözümlemez. Bunun yerine altta bulunan kitap çalışmalarını listeler ve kullanıcının kitap kökünü seçmesini ister.

## Eski manifestlerdeki `path` alanları

Bazı eski manifestlerde bölüm yolu şu biçimde olabilir:

```yaml
chapters:
  - id: chapter_01
    path: workspace/react/chapters/chapter_01_modern_web_giris.md
```

Kitap kökü zaten `workspace/react` ise Studio bu yolu otomatik olarak şu konuma çözümler:

```text
chapters/chapter_01_modern_web_giris.md
```

Bu nedenle eski manifestlerle geriye dönük uyumluluk korunur.

## Production komutları

Production komutları framework araçlarını kullanır; ancak çıktıların tamamı kitap kökü altında üretilir:

```text
<kitap-kökü>/build
<kitap-kökü>/assets
<kitap-kökü>/exports
<kitap-kökü>/prompts
<kitap-kökü>/chapters
```

Bu model sayesinde aynı BookFactory kurulumu ile birden fazla kitap projesi bağımsız klasörlerde yönetilebilir.
