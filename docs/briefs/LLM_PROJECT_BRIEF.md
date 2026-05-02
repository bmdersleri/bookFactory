# Parametric Computer Book Factory — LLM Project Brief (Index)

**Framework sürümü:** v2.11.x
**Belge dili:** Türkçe | Teknik dosya adları: İngilizce
**Konum:** `docs/briefs/LLM_PROJECT_BRIEF.md`

> Bu dosya bir **router/index**'tir. İçeriği kendisi taşımaz; hangi modülün ne zaman
> yükleneceğini gösterir. Aktif kitap bağlamı ve proje detayları kitabın kendi
> `book_manifest.yaml` dosyasından ve varsa proje özgü brief dosyasından okunur.

---

## Modül haritası

| Dosya | İçerik | Ne zaman yükle |
|---|---|---|
| [`brief_core.md`](brief_core.md) | Projenin ne olduğu, temel ilkeler, hedefler | Her oturumda — ilk yükle |
| [`brief_llm_rules.md`](brief_llm_rules.md) | LLM rolleri, yapması/yapmaması gerekenler, hata davranışı | Her oturumda — ikinci yükle |
| [`brief_structure.md`](brief_structure.md) | Framework ve kitap proje klasör yapısı, araçlar | Dosya/klasör işlemi yapılacaksa |
| [`brief_standards.md`](brief_standards.md) | CODE_META, screenshot, Mermaid, QR/GitHub standartları | Bölüm üretimi veya kod işlemi yapılacaksa |
| [`brief_react_context.md`](brief_react_context.md) | React kitabı proje bağlamı (kitaba özgü) | React kitabıyla çalışılacaksa |
| [`brief_environment.md`](brief_environment.md) | PowerShell 7, UTF-8, VS Code, Dev Container, Codespaces | Ortam kurulumu veya Windows sorunu varsa |
| [`brief_loading_order.md`](brief_loading_order.md) | Dosya yükleme sırası, iş akışı, onay kapıları | Üretim aşaması planlanırken |

---

## Minimum başlangıç komutu (genel)

```
Aşağıdaki dosyalar Parametric Computer Book Factory v2.11.x çerçevesine aittir.

Önce `brief_core.md`, ardından `brief_llm_rules.md` dosyasını oku.
Aktif kitap bağlamına özgü brief dosyası varsa onu da yükle.
Bölüm üretimi yapacaksan `brief_standards.md` ve `brief_loading_order.md` dosyalarını da oku.

Aktif kitap yolu ve manifest: kullanıcı sağlayacak.
Manifesti doğrula. Eksik veya çelişkili alan varsa üretime geçmeden raporla.
```

---

## Hızlı senaryo rehberi

**Yeni oturum — genel BookFactory çalışması:**
→ `brief_core.md` + `brief_llm_rules.md`

**Yeni oturum — React kitabıyla çalışma:**
→ `brief_core.md` + `brief_llm_rules.md` + `brief_react_context.md`

**Bölüm üretimi:**
→ Yukarıdakilere ek: `brief_standards.md` + `brief_loading_order.md`

**Dosya/klasör yapısını anlamak:**
→ `brief_structure.md`

**Ortam sorunu (PowerShell, UTF-8, Codespaces):**
→ `brief_environment.md`

**Yeni kitap projesi başlatma:**
→ `brief_core.md` + `brief_llm_rules.md` + `core/12_project_starter_prompt.md`

---

## Aktif kitap bağlamı nasıl belirlenir?

1. `book_manifest.yaml` → `book.title`, `book.author`, `cumulative_app.name`
2. Proje özgü brief dosyası varsa → `brief_{project_slug}_context.md`
3. Studio GUI → aktif kitap yolu `.studio_config.json`'da saklanır

LLM, kitap bağlamını her zaman manifestten okur. Bağlamı tahmin etmez.
