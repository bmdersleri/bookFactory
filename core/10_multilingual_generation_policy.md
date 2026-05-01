# Multilingual Generation Policy — Çok Dilli Üretim Politikası

## Temel ilke

Dosya adları, klasör adları, manifest anahtarları, otomasyon kimlikleri, meta bloklar ve pipeline terimleri İngilizce kalır. İçerik dili manifestteki `language` alanına göre belirlenir.

## Desteklenen modlar

| Mod | Anlam |
|---|---|
| `single` | Tek dilde kitap üretimi |
| `parallel` | Her hedef dil için ayrı kitap üretimi |
| `bilingual` | Aynı içerikte iki dil |
| `multilingual_inline` | Aynı içerikte çok dilli özel yapı |

## Paralel üretim klasörü

```text
generated/{book_id}/
├── tr/
├── en/
└── de/
```

## Kod dili

Kod tanımlayıcıları İngilizce kalmalıdır. Kod yorumları ve konsol çıktıları manifest politikasına göre hedef dilde veya İngilizce olabilir.

## Eksik çeviri

Eksik çeviri varsa model uydurmaz; eksik çeviri raporu üretir veya manifestteki fallback dilini kullanır.
