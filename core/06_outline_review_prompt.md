# Outline Review Prompt — Outline Kontrol Promptu

Bu prompt, bölüm-girdi promptu üretildikten ve ilgili bölüm için outline oluşturulduktan sonra kalite kontrol yapmak için kullanılır.

## Kontrol alanları

1. Manifest uyumu
2. Bölüm amacıyla uyum
3. Hedef kitleye uygunluk
4. Öğrenme çıktılarının ölçülebilirliği
5. Zorunlu kavramların kapsanması
6. Kapsam dışı konulara girilmemesi
7. Kod/görsel/screenshot varlık planı
8. Meta blok hazırlığı
9. Dil politikası uyumu
10. Başlık numaralandırma politikası
11. Pedagojik akış
12. Teknik doğruluk riski
13. Onay kapısı uyumu
14. Tam metin üretimine hazır olma

## Karar seçenekleri

- `PASS`: Tam metne geçilebilir.
- `REVISION_REQUIRED`: Revizyon gerekir.
- `BLOCKED`: Tam metne geçilmemelidir.

## Çıktı formatı

```markdown
# Outline Review Report

## 1. Decision

**Decision:** PASS / REVISION_REQUIRED / BLOCKED

## 2. Checklist

| Control item | Status | Notes |
|---|---|---|
| Manifest alignment | PASS | ... |

## 3. Required revisions

1. ...
```

Bu prompt çalıştırılırken tam bölüm metni üretilmez.
