# BookFactory Studio v3.1.1 PathFix Patch

Bu paket, Studio'nun chapter dosyalarını yanlış kökte aramasını düzeltir.

## Kurulum

Patch ZIP içeriğini mevcut BookFactory klasörünüzün üzerine çıkarın. Var olan dosyaların üzerine yazılmasına izin verin.

Örnek doğru çalışma modeli:

```powershell
cd C:\OneDrive\OneDrive - mehmetakif.edu.tr\BookFactory
python -m bookfactory_studio.app
```

Tarayıcıdaki **Kitap kökü** alanına BookFactory framework klasörünü değil, ilgili kitabın klasörünü yazın:

```text
C:\OneDrive\OneDrive - mehmetakif.edu.tr\react-web
```

veya BookFactory içinde çalışıyorsa:

```text
C:\OneDrive\OneDrive - mehmetakif.edu.tr\BookFactory\workspace\react
```

## Düzeltilen problem

Önceki sürümde Studio, `BookFactory` framework kökü seçildiğinde alttaki `workspace/react/book_manifest.yaml` dosyasını buluyor fakat chapter dosyalarını `BookFactory/chapters` altında arıyordu. Bu patch ile:

- Framework kökü ile kitap kökü ayrıldı.
- Framework kökü aktif kitap projesi kabul edilmiyor.
- Bulunan kitap kökleri dashboard üzerinde listeleniyor.
- Eski `workspace/react/chapters/...` yolları kitap kökü altında otomatik `chapters/...` olarak çözümleniyor.
- Production komutları framework araçlarını kullanıyor; fakat çıktıları seçilen kitap kökü altında üretiyor.
