# DOCX Build ve Biçimlendirme Politikası

Bu politika, Pandoc ile DOCX üretiminde kullanılacak reference DOCX, Lua filter ve DOCX post-process adımlarını tanımlar.

## Reference DOCX

DOCX çıktısının sayfa yapısı, üst bilgi/alt bilgi, temel Word stilleri, kod blokları, başlıklar ve pedagogik kutular için `reference_docx` kullanılmalıdır.

Profil örneği:

```yaml
post_production:
  pandoc:
    reference_docx: "templates/reference_docs/referenceV17_java_temelleri.docx"
```

## Lua filter

Lua filter; callout kutuları, bölüm sekmeleri, Mermaid PNG yerleşimi, sayfa sonları, çoktan seçmeli liste düzeni ve bölüm sonu tekilleştirme gibi dönüşüm mantıklarını yürütür.

Profil örneği:

```yaml
post_production:
  pandoc:
    lua_filter: "templates/lua_filters/styles_revised_v17.lua"
```

## DOCX post-process

Pandoc sonrası DOCX üzerinde şu işlemler yapılabilir:

1. Resim içeren paragrafları ortalama
2. Ana bölüm/ek başlıklarını ortalama
3. Bölüm sonu etiketlerini ortalama
4. Pedagogik kutuları iki yana yaslama
5. Tablo başlık satırlarını okunur hâle getirme
6. Tablo sütun genişliklerini içerik uzunluğuna göre optimize etme

Bu işlemler doğrudan kaynak Markdown’u değiştirmez. Yalnızca DOCX çıktısı üzerinde uygulanır.

## Güvenlik ilkesi

Post-process betikleri yalnızca hedeflenen DOCX öğelerini değiştirmelidir. Genel gövde metni, kod blokları, tablo gövdesi ve kullanıcı tarafından tasarlanmış özel öğeler mümkün olduğunca korunmalıdır.

## Raporlama

Her post-process adımı aşağıdaki bilgileri raporlamalıdır:

- İşlenen dosya
- Üretilen çıktı
- Düzeltilen resim sayısı
- Düzeltilen tablo başlığı hücresi sayısı
- Optimize edilen tablo sayısı
- Hata veya atlanan öğe sayısı
