# BookFactory Studio Manifest Editörü

Manifest editörü, kitap üretim hattının tek doğruluk kaynağı olan `book_manifest.yaml` dosyasını form tabanlı biçimde yönetmek için tasarlanmıştır.

## Tasarım İlkeleri

- Kullanıcı mümkün olduğunca YAML sözdizimiyle uğraşmamalıdır.
- Kritik hatalar kayıt öncesinde engellenmelidir.
- Uyarılar açık biçimde gösterilmeli, ancak üretimi tamamen engellememelidir.
- Bölüm dosya adları gerçek `chapters/` klasörüyle karşılaştırılmalıdır.
- Kitap kökü, BookFactory framework kökünden bağımsız ele alınmalıdır.

## Sekmeler

- **Kitap Bilgileri:** Başlık, yazar, yıl, dil ve kümülatif uygulama bilgileri.
- **Bölümler:** Bölüm ID, başlık, dosya adı, durum ve gerçek dosya varlığı.
- **Kapsam:** Teknoloji yığını ve kapsam dışı bırakılacak konular.
- **Otomasyon:** Kalite kapıları, kod testi, QR, Mermaid ve GitHub bayrakları.
- **Yollar:** Kitap köküne göre göreli klasör yolları.
- **YAML:** İleri seviye kullanıcılar için ham YAML görünümü.

## Dosya Eşleştirme

`Dosyaları Eşleştir` işlemi, manifestteki bölüm dosya adlarını `chapters/` klasöründeki gerçek Markdown dosyalarıyla eşleştirir. Örneğin:

```yaml
file: chapter_02_javascript_temelleri.md
```

şu gerçek dosyayla değiştirilebilir:

```yaml
file: chapter_02_javascript_es6_react.md
```

Eşleştirme, öncelikle `chapter_XX_*.md` desenine göre yapılır.
