# Full Text Generation Prompt — Tam Metin Üretim Promptu

Bu prompt, outline kontrolü `PASS` kararı verdikten ve manifestteki onay kapısı izin verdikten sonra kullanılır.

## Kurallar

- Tam metin Pandoc uyumlu Markdown olmalıdır.
- Başlıklar manuel numaralandırılmamalıdır.
- `chapter_id` korunmalıdır.
- İçerik dili manifestteki hedef dile uygun olmalıdır.
- Kod blokları bağımsız olmalıdır.
- Gerekli kodlar `CODE_META` ile işaretlenmelidir.
- Gerekli görseller `DIAGRAM_META`, `SCREENSHOT_META` veya `ASSET_META` ile işaretlenmelidir.
- Hatalı kodlar `broken_example` olarak işaretlenmelidir.
- Teknik bilgi kaynak politikasıyla uyumlu olmalıdır.
- Kapsam dışı konulara girilmemelidir.
- Bölüm sonunda elle bölüm sonu etiketi yazılmamalıdır.

## Çıktı

Yalnızca tam bölüm Markdown içeriği üret.
