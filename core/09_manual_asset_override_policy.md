# Manual Asset Override Policy — Manuel Görsel Önceliği Politikası

## Temel ilke

Aynı asset ID'ye sahip manuel görsel varsa, DOCX/PDF/HTML üretiminde otomatik görsel yerine manuel görsel kullanılır.

## Klasör yapısı

```text
assets/
├── auto/
├── manual/
├── locked/
└── final/
```

## Öncelik sırası

1. `assets/manual/`
2. `assets/locked/`
3. `assets/auto/`

`assets/manual/` ve `assets/locked/` otomatik temizlik sırasında silinemez.

## QR istisnası

QR görsellerinin matris kısmı manuel olarak değiştirilmemelidir.
